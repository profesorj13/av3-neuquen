"""
Harness para correr los casos de docs/situaciones-de-prueba.md contra
/inclusion/assist y evaluar las respuestas con LLM-as-judge.

Uso:
    # 1. Backend corriendo en :8000 con .env de Azure OpenAI configurado.
    # 2. Desde la raiz del repo av3-back:
    python tests/test_assistant_situations.py [--cases 1,3,5] [--out results.json]

El parser entiende el formato actual del MD:
    ### Caso NN — titulo
    **tags:** `tag1` `tag2`
    **T1👤** "mensaje del docente"
    **T1🤖 esperado:**
    - 🛠 herramientas esperadas
    - ✅ que SI debe aparecer
    - ❌ que NO debe aparecer

Cada turno T*N* del docente se envia al endpoint con el history acumulado.
La respuesta cruda (texto + tool_calls + cards) se compara contra el bloque
"esperado" usando gpt-5-mini como juez.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Optional

import httpx
from openai import AzureOpenAI


REPO_ROOT = Path(__file__).resolve().parent.parent
CASES_FILE = REPO_ROOT / "docs" / "situaciones-de-prueba.md"
ASSIST_URL = os.environ.get("ASSIST_URL", "http://localhost:8000/inclusion/assist")

# Azure OpenAI para el judge
AZURE_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
AZURE_KEY = os.environ.get("AZURE_OPENAI_API_KEY", "")
AZURE_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5-mini")


@dataclass
class Turn:
    n: int
    docente: str
    expected: str  # bloque markdown crudo del esperado


@dataclass
class Case:
    id: int
    title: str
    tags: list[str] = field(default_factory=list)
    turns: list[Turn] = field(default_factory=list)


@dataclass
class TurnResult:
    n: int
    docente: str
    response_text: str
    tool_calls: list[dict]
    identified_student: Optional[dict]
    device: Optional[dict]
    pedagogical_adaptation: Optional[dict]


@dataclass
class CaseVerdict:
    case_id: int
    title: str
    pass_: bool
    score: int  # 0..100
    notes: str
    turn_results: list[TurnResult]


_CASE_HEADER_RE = re.compile(r"^###\s*Caso\s+(\d+)\s*[—-]\s*(.+?)\s*$", re.MULTILINE)
_TURN_DOCENTE_RE = re.compile(r"^\*\*T(\d+)👤\*\*\s*(.+?)$", re.MULTILINE)
_TURN_EXPECTED_RE = re.compile(r"^\*\*T(\d+)🤖[^*]*\*\*\s*$", re.MULTILINE)
_TAGS_RE = re.compile(r"^\*\*tags:\*\*\s*(.+?)$", re.MULTILINE)


def parse_cases(md: str) -> list[Case]:
    """Extrae los casos del MD. Conserva el bloque expected como markdown crudo
    (lo usamos despues como input del judge)."""
    cases: list[Case] = []
    headers = list(_CASE_HEADER_RE.finditer(md))
    for i, m in enumerate(headers):
        case_id = int(m.group(1))
        title = m.group(2).strip()
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(md)
        body = md[start:end]

        # tags
        tags_match = _TAGS_RE.search(body)
        tags: list[str] = []
        if tags_match:
            tags = re.findall(r"`([^`]+)`", tags_match.group(1))

        # turnos: emparejar T<N>👤 con T<N>🤖 esperado
        docente_msgs = list(_TURN_DOCENTE_RE.finditer(body))
        expected_starts = list(_TURN_EXPECTED_RE.finditer(body))

        turns: list[Turn] = []
        for dm in docente_msgs:
            n = int(dm.group(1))
            raw = dm.group(2).strip()
            # quitar comillas tipograficas o ascii del mensaje
            text = raw.strip().strip('"').strip('“').strip('”')

            # bloque esperado: desde el T<N>🤖 hasta el siguiente T<N+1>👤 o fin del body
            expected_block = ""
            for em in expected_starts:
                if int(em.group(1)) != n:
                    continue
                e_start = em.end()
                # cortar en el siguiente T*👤 o ---
                next_marker = None
                for cand in docente_msgs:
                    if cand.start() > e_start:
                        next_marker = cand.start()
                        break
                hr_match = re.search(r"^---\s*$", body[e_start:], re.MULTILINE)
                hr_pos = e_start + hr_match.start() if hr_match else None
                cuts = [c for c in (next_marker, hr_pos) if c is not None]
                e_end = min(cuts) if cuts else len(body)
                expected_block = body[e_start:e_end].strip()
                break

            turns.append(Turn(n=n, docente=text, expected=expected_block))

        cases.append(Case(id=case_id, title=title, tags=tags, turns=turns))
    return cases


def run_case(case: Case) -> list[TurnResult]:
    """Ejecuta los turnos contra /inclusion/assist con history acumulado."""
    history: list[dict] = []
    results: list[TurnResult] = []
    with httpx.Client(timeout=60.0) as client:
        for turn in case.turns:
            payload = {"message": turn.docente}
            if history:
                payload["history"] = history
            try:
                r = client.post(ASSIST_URL, json=payload)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                data = {"response": f"[ERROR HTTP] {e}", "tool_calls": [],
                        "identified_student": None, "device": None,
                        "pedagogical_adaptation": None}

            results.append(TurnResult(
                n=turn.n,
                docente=turn.docente,
                response_text=data.get("response", ""),
                tool_calls=data.get("tool_calls", []) or [],
                identified_student=data.get("identified_student"),
                device=data.get("device"),
                pedagogical_adaptation=data.get("pedagogical_adaptation"),
            ))
            history.append({"role": "user", "content": turn.docente})
            history.append({"role": "assistant", "content": data.get("response", "")})
    return results


_JUDGE_PROMPT_HEAD = """Sos un evaluador estricto de respuestas de un asistente de
inclusion educativa. Recibis (1) los criterios esperados de un caso, escritos
en lenguaje natural por la pedagoga responsable, y (2) la respuesta real del
asistente con sus tool calls y cards. Tenes que decidir si la respuesta cumple.

Reglas duras:
- Si el caso espera un tool especifico (identify_student, propose_device,
  propose_pedagogical_adaptation) y NO se invoco, es FAIL.
- Si el caso prohibe terminos ("dislexia", "TDAH", "diagnostico"...) y aparecen
  en el texto del asistente, es FAIL.
- Si el caso pide que NO emita propose_device pero igual lo hizo, es FAIL.

Reglas blandas (PARTIAL):
- Tono cercano pero no se ajusta al estilo (paternalismo leve, jerga educativa
  excesiva): score 60-75.
- Tools llamadas pero con args debatibles (ej: device razonable pero no el optimo):
  score 70-85.
- Falta un detalle accionable que el caso pidio explicitamente: score 60-80.

Devolve EXCLUSIVAMENTE un objeto JSON con tres claves: "pass" (bool),
"score" (entero 0..100) y "notes" (string en espanol, 1-3 oraciones).
NO incluyas nada mas que el JSON.
"""


def _summarize_turn_result(tr: TurnResult) -> dict:
    """Compacta para enviar al judge."""
    return {
        "turn": tr.n,
        "docente": tr.docente,
        "alizia_text": tr.response_text,
        "tool_calls": [{"name": c.get("name"), "args": c.get("args")} for c in tr.tool_calls],
        "identified_student": (tr.identified_student or {}).get("name") if tr.identified_student else None,
        "device": (tr.device or {}).get("name") if tr.device else None,
        "pedagogical_adaptation": tr.pedagogical_adaptation is not None,
    }


def judge(case: Case, results: list[TurnResult], client: AzureOpenAI) -> CaseVerdict:
    expected_blob = "\n\n".join(
        f"### Turno {t.n}\nDocente: {t.docente}\nEsperado:\n{t.expected}" for t in case.turns
    )
    actual_blob = json.dumps([_summarize_turn_result(tr) for tr in results], ensure_ascii=False, indent=2)

    prompt = (
        _JUDGE_PROMPT_HEAD
        + "\nCRITERIOS ESPERADOS (caso):\n"
        + expected_blob
        + "\n\nRESPUESTA REAL DEL ASISTENTE (todos los turnos):\n"
        + actual_blob
    )
    try:
        resp = client.chat.completions.create(
            model=AZURE_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=600,
        )
        raw = resp.choices[0].message.content or "{}"
        # extraer JSON del texto
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        verdict = json.loads(m.group(0)) if m else {"pass": False, "score": 0, "notes": "judge sin respuesta"}
    except Exception as e:
        verdict = {"pass": False, "score": 0, "notes": f"judge error: {e}"}

    return CaseVerdict(
        case_id=case.id,
        title=case.title,
        pass_=bool(verdict.get("pass")),
        score=int(verdict.get("score", 0)),
        notes=str(verdict.get("notes", "")),
        turn_results=results,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", help="comma-separated ids (ej: 1,3,5). Default: todos.")
    parser.add_argument("--out", default="results.json")
    parser.add_argument("--no-judge", action="store_true",
                        help="solo correr los casos contra el endpoint, no juzgar.")
    args = parser.parse_args()

    if not CASES_FILE.exists():
        print(f"No encuentro {CASES_FILE}", file=sys.stderr)
        sys.exit(1)

    md = CASES_FILE.read_text(encoding="utf-8")
    cases = parse_cases(md)
    if args.cases:
        wanted = {int(x.strip()) for x in args.cases.split(",")}
        cases = [c for c in cases if c.id in wanted]

    print(f"Corriendo {len(cases)} casos contra {ASSIST_URL}")

    judge_client: Optional[AzureOpenAI] = None
    if not args.no_judge:
        if not AZURE_ENDPOINT or not AZURE_KEY:
            print("WARN: faltan AZURE_OPENAI_ENDPOINT/_API_KEY; saltando judge.", file=sys.stderr)
        else:
            judge_client = AzureOpenAI(
                api_version="2024-02-15-preview",
                azure_endpoint=AZURE_ENDPOINT,
                api_key=AZURE_KEY,
            )

    verdicts: list[dict] = []
    for case in cases:
        print(f"\n=== Caso {case.id:02d} — {case.title}")
        results = run_case(case)
        for tr in results:
            n_tools = len(tr.tool_calls)
            tool_names = ",".join(c.get("name", "?") for c in tr.tool_calls) or "(none)"
            print(f"  T{tr.n}: tools={n_tools} [{tool_names}]")
            print(f"       text: {tr.response_text[:140]}{'...' if len(tr.response_text) > 140 else ''}")

        if judge_client:
            v = judge(case, results, judge_client)
            print(f"  -> verdict: {'PASS' if v.pass_ else 'FAIL'} score={v.score} :: {v.notes}")
            d = asdict(v)
            d["pass"] = d.pop("pass_", False)
            d["turn_results"] = [asdict(tr) for tr in v.turn_results]
            verdicts.append(d)
        else:
            verdicts.append({
                "case_id": case.id,
                "title": case.title,
                "pass": None,
                "score": None,
                "notes": "judge skipped",
                "turn_results": [asdict(tr) for tr in results],
            })

    out_path = Path(args.out)
    out_path.write_text(json.dumps(verdicts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nResultados escritos en {out_path}")

    if judge_client:
        passed = sum(1 for v in verdicts if v.get("pass"))
        print(f"\nResumen: {passed}/{len(verdicts)} PASS")


if __name__ == "__main__":
    main()
