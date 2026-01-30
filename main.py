import os
import re
import json
import copy
import asyncio
import logging
import urllib.request
import psycopg2
from dotenv import load_dotenv

load_dotenv()
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from openai import AzureOpenAI, AsyncAzureOpenAI

app = FastAPI(title="Annual Planning API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5480/av3")

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5-mini")

KAPSO_WEBHOOK_URL = os.getenv("KAPSO_WEBHOOK_URL", "")  # Kapso workflow API trigger URL

logger = logging.getLogger(__name__)

ai_client = AzureOpenAI(
    api_version="2024-02-15-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY
)

async_ai_client = AsyncAzureOpenAI(
    api_version="2024-02-15-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY
)


def get_db():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


class MethodologicalStrategies(BaseModel):
    type: str  # proyecto, taller_laboratorio, ateneo_debate
    context: str


class CoordinationDocumentCreate(BaseModel):
    name: str
    area_id: int
    start_date: str
    end_date: str
    problem_edge: Optional[str] = None
    methodological_strategies: Optional[dict] = None  # {type, context}
    eval_criteria: Optional[str] = None
    subjects_data: Optional[dict] = None
    nucleus_ids: List[int] = []
    category_ids: List[int] = []


class CoordinationDocumentUpdate(BaseModel):
    name: Optional[str] = None
    problem_edge: Optional[str] = None
    methodological_strategies: Optional[dict] = None  # {type, context}
    eval_criteria: Optional[str] = None
    subjects_data: Optional[dict] = None
    status: Optional[str] = None


class ChatHistoryItem(BaseModel):
    role: str
    content: str

class ChatMessage(BaseModel):
    history: List[ChatHistoryItem]


class GenerateRequest(BaseModel):
    generate_strategy: bool = True
    generate_class_plans: bool = True


class TeacherLessonPlanCreate(BaseModel):
    course_subject_id: int
    coordination_document_id: int
    class_number: int
    title: Optional[str] = None
    category_ids: List[int] = []
    objective: Optional[str] = None
    knowledge_content: Optional[str] = None
    didactic_strategies: Optional[str] = None
    class_format: Optional[str] = None
    moments: Optional[dict] = None
    custom_instruction: Optional[str] = None
    resources_mode: Optional[str] = 'global'
    global_font_id: Optional[int] = None
    moment_font_ids: Optional[dict] = None


class TeacherLessonPlanUpdate(BaseModel):
    title: Optional[str] = None
    category_ids: Optional[List[int]] = None
    objective: Optional[str] = None
    knowledge_content: Optional[str] = None
    didactic_strategies: Optional[str] = None
    class_format: Optional[str] = None
    moments: Optional[dict] = None
    status: Optional[str] = None
    custom_instruction: Optional[str] = None
    resources_mode: Optional[str] = None
    global_font_id: Optional[int] = None
    moment_font_ids: Optional[dict] = None


# Response Models
from datetime import datetime, date as date_type

class RootResponse(BaseModel):
    message: str
    docs: str

class DeleteResponse(BaseModel):
    message: str
    id: int

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime

class AreaResponse(BaseModel):
    id: int
    coordinator_id: Optional[int]
    name: str
    description: Optional[str]
    created_at: datetime

class SubjectResponse(BaseModel):
    id: int
    area_id: int
    name: str
    description: Optional[str]
    created_at: datetime

class CourseResponse(BaseModel):
    id: int
    name: str
    schedule: Optional[dict]
    created_at: datetime

class StudentResponse(BaseModel):
    id: int
    course_id: int
    name: str
    created_at: datetime

class CourseSubjectResponse(BaseModel):
    id: int
    course_id: int
    subject_id: int
    teacher_id: int
    start_date: date_type
    end_date: date_type
    school_year: int
    course_name: Optional[str] = None
    subject_name: Optional[str] = None
    teacher_name: Optional[str] = None
    created_at: datetime

class ProblematicNucleusResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

class KnowledgeAreaResponse(BaseModel):
    id: int
    nucleus_id: int
    name: str
    description: Optional[str]
    created_at: datetime

class CategoryResponse(BaseModel):
    id: int
    knowledge_area_id: int
    name: str
    description: Optional[str]
    created_at: datetime

class MomentTypeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

class ActivityResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    moment_type: Optional[str] = None
    created_at: datetime


class ActivitiesByMomentResponse(BaseModel):
    apertura: List[ActivityResponse]
    desarrollo: List[ActivityResponse]
    cierre: List[ActivityResponse]


class ActivityRecommendationRequest(BaseModel):
    objective: str
    category_ids: List[int]


class ActivityRecommendationResponse(BaseModel):
    apertura_recommended_id: int
    desarrollo_recommended_ids: List[int]
    cierre_recommended_id: int

class FontResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    file_url: str
    file_type: str
    thumbnail_url: Optional[str]
    area_id: Optional[int]
    is_validated: bool
    created_at: datetime

class CoordinationDocumentResponse(BaseModel):
    id: int
    name: str
    area_id: int
    start_date: date_type
    end_date: date_type
    status: str
    problem_edge: Optional[str] = None
    methodological_strategies: Optional[dict] = None  # {type, context}
    eval_criteria: Optional[str] = None
    subjects_data: Optional[dict]
    nucleus_ids: List[int]
    category_ids: List[int]
    created_at: datetime

class CoordinationDocumentDetailResponse(CoordinationDocumentResponse):
    area: Optional[AreaResponse] = None
    subjects: List[SubjectResponse] = []
    categories: List[CategoryResponse] = []
    nuclei: List[ProblematicNucleusResponse] = []

class TeacherLessonPlanResponse(BaseModel):
    id: int
    course_subject_id: int
    coordination_document_id: int
    class_number: int
    title: Optional[str]
    category_ids: List[int]
    objective: Optional[str]
    knowledge_content: Optional[str]
    didactic_strategies: Optional[str]
    class_format: Optional[str]
    moments: Optional[dict]
    status: str
    created_at: datetime
    updated_at: datetime
    course_name: Optional[str] = None
    subject_name: Optional[str] = None
    document_name: Optional[str] = None
    is_shared_class: Optional[bool] = None
    shared_with_subject: Optional[str] = None
    is_own_plan: Optional[bool] = None
    created_by_teacher: Optional[str] = None
    created_by_subject: Optional[str] = None
    custom_instruction: Optional[str] = None
    resources_mode: Optional[str] = None
    global_font_id: Optional[int] = None
    moment_font_ids: Optional[dict] = None

class TeacherLessonPlanDetailResponse(TeacherLessonPlanResponse):
    moment_types: List[MomentTypeResponse] = []
    activities: List[ActivityResponse] = []
    categories: List[CategoryResponse] = []

class SharedClassSlot(BaseModel):
    day: str
    time: str
    subject: str
    shared_with: str

class SharedClassesResponse(BaseModel):
    course_id: int
    area_id: int
    shared_classes: List[SharedClassSlot]


# Resource Models
class ResourceCreate(BaseModel):
    title: str
    resource_type: str  # 'lecture_guide' | 'course_sheet'
    user_id: int


class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class ResourceResponse(BaseModel):
    id: int
    title: str
    resource_type: str
    content: Optional[str]
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime


RESOURCE_TEMPLATES = {
    'lecture_guide': """Guía de lectura – Ciencias Sociales (2° año)

Tema: Cambios en la forma de vida y en la organización de las sociedades

1. Según los textos, ¿qué es la Revolución Neolítica y por qué fue un momento importante en la historia de la humanidad?
Respondé con tus propias palabras.

2. ¿Cómo vivían los grupos humanos antes de la agricultura y cómo cambió su vida cuando comenzaron a cultivar plantas y criar animales?
Nombrá al menos dos cambios.

3. Los textos explican que la vida de los cazadores-recolectores no era necesariamente mala. ¿Qué aspectos positivos tenía esa forma de vida?

4. ¿Qué razones mencionan los autores para explicar por qué las personas empezaron a practicar la agricultura?
Explicá brevemente cada una.

5. ¿Qué significa que las sociedades se hayan vuelto sedentarias? ¿Qué cambios trajo el sedentarismo en la organización social?

6. Explicá qué es un excedente de producción y por qué fue tan importante en las sociedades agrícolas.

7. Según los textos, ¿cómo influyó la aparición del excedente en el surgimiento de diferencias sociales y desigualdades?

8. Uno de los textos propone pensar la economía de otra manera, relacionada con el cuidado de la vida y la naturaleza. ¿Qué ideas nuevas aparecen sobre el uso de la tierra y los recursos?

9. Compará la forma en que las sociedades antiguas y las sociedades actuales se relacionan con la naturaleza. ¿Qué diferencias y similitudes encontrás?

10. Después de leer los textos, ¿pensás que todos los cambios históricos significaron mejoras para todas las personas? ¿Por qué?
Fundamentá tu respuesta usando ideas de las lecturas.
""",
    'course_sheet': """La Revolución Industrial Inglesa

La Revolución Industrial Inglesa es un proceso económico, cultural y social que se llevó a cabo en el territorio que hoy conocemos como Inglaterra en el período que abarca el final del Siglo XVIII y principios del Siglo XIX. Es un período de fuertes transformaciones en la forma de producción económica, cultural y, por ende, en la forma de vivir de los sujetos de esa época. El impacto de este proceso sociohistórico aceleró cambios fundamentales en la economía y en los modos de vida del mundo occidental. A partir de la implementación de diversas innovaciones tecnológicas que se aplicaban en la forma de organización de los talleres manufactureros, se modifica radicalmente la actividad productiva de las trabajadoras y los trabajadores en las nuevas industrias, así como también se introducen cambios en la organización de los territorios y la forma de vivir de la gente.

Esto significa que también los cuerpos sufren una modificación sustancial. A partir de la industrialización, el cuerpo comienza a ser visto y tratado como una máquina de trabajo que convive a la par de la máquina de vapor utilizada en distintas industrias.

La migración de la población desde el campo hacia las grandes ciudades, la expropiación de las tierras, implica un cambio de concepción en la relación que los campesinos y las campesinas tenían en y con la naturaleza. Los procesos de explotación, como por ejemplo la mina de carbón, convierten a la naturaleza -y a los cuerpos que la trabajan- en una mercancía más del sistema capitalista. De esta concepción se desprende la necesidad de disciplinar los cuerpos de los hombres, las mujeres y los niños. Junto con la invención de la fábrica, conviven otras instituciones como las escuelas, los orfanatos, los hospitales, las cárceles, cuyo objetivo es controlar el tiempo y la vida de las personas para poder aumentar las fuerzas de trabajo del cuerpo y transformarlo en una máquina productiva que aporte de manera útil al sistema económico. Al mismo tiempo, se pretendía disminuir la desobediencia de los cuerpos. De esta manera, se instaura una vigilancia, un control, un castigo, normalizadores de los cuerpos.

Para esto, fue necesario el desarrollo de distintos mecanismos de disciplinamiento que permitan un orden social, un comportamiento de los cuerpos, específico. Estas formas de control del tiempo y de la vida, si bien surgieron hace varios siglos atrás, conservan su vigencia en la época actual. En primer lugar, podemos pensar el modelo del panóptico, diseñada por Jeremy Bentham. Esta forma implica el uso de una gran visión que organiza el espacio productivo de modo tal que se centra en la posibilidad de que cientos de cuerpos, gestos, movimientos, etc. sean supervisados por una "gran visión", la del capataz, el supervisor, etc. Es decir, los cuerpos son sometidos a un control minucioso y constante lo que tiene por resultado la creación de sujetos que -al no saber en qué momento están siendo o no observados- son obedientes.

En segundo lugar, podemos pensar el modelo maquínico de disciplinamiento. A partir de la introducción de la máquina en las fábricas, es decir, a partir de la introducción de las distintas innovaciones tecnológicas, los obreros y las obreras se ven obligados a adecuar sus gestos y movimientos -sus cuerpos- al ritmo que impone la máquina. Se crea una disciplina intensa, regular, alejada del tiempo e impersonal.

A partir del uso de estas nuevas lógicas, de estas nuevas formas de trabajar, los cuerpos y sus tiempos quedan atrapados dentro de poderes sutiles que les imponen coacciones, obligaciones, controles. Es a partir del ejercicio del poder disciplinar que se construye una nueva forma de ser y estar en el mundo, de vincularse con la naturaleza y los seres humanos que nos rodean. Se crea el obrero.
"""
}

class SharedClassNumbersResponse(BaseModel):
    shared_class_numbers: List[int]
    shared_class_info: dict

class ClassPlanItem(BaseModel):
    class_number: int
    title: str
    objective: Optional[str] = None
    category_ids: List[int] = []

class CoordinationStatusResponse(BaseModel):
    has_published_document: bool
    document_id: Optional[int]
    document_name: Optional[str]
    coordinator_name: Optional[str]
    class_plan: List[ClassPlanItem]
    subject_category_ids: List[int]
    category_ids: List[int]
    nucleus_ids: List[int]

class ChatResponse(BaseModel):
    response: str
    document: Optional[CoordinationDocumentResponse] = None

class TeacherChatResponse(BaseModel):
    response: str
    plan: Optional[TeacherLessonPlanResponse] = None
    changes_made: List[str] = []

class GenerateMomentResponse(BaseModel):
    moment_type: str
    generated_content: str
    plan: TeacherLessonPlanResponse


# AI Helper Functions

# Strategy types with descriptions for AI prompt
STRATEGY_TYPES = {
    "proyecto": "Construimos como area un resultado entregable final, trabajandose de manera individual en cada disciplina y EPAs para lograr los hitos intermedios",
    "taller_laboratorio": "Actividad/es que combina/n los saberes teoricos desarrollados en cada disciplina-EPAs con saberes practicos que privilegien la dimension experiencial",
    "ateneo_debate": "Actividad que propone la construccion de posiciones, criterios e ideas a partir del desarrollo del pensamiento critico y reflexivo"
}


def generate_problem_edge(area_name: str, subjects: list, categories: list, nuclei: list) -> str:
    """Generate the problem edge (problem statement) for a coordination document."""
    subject_names = [s["name"] for s in subjects]
    category_names = [c["name"] for c in categories]
    nucleus_names = [n["name"] for n in nuclei]

    prompt = f"""Eres un experto en planificación educativa. Genera un planteamiento de problema para el área de {area_name}.

Materias involucradas: {', '.join(subject_names)}
Núcleos problemáticos: {', '.join(nucleus_names)}
Categorías/conceptos a enseñar: {', '.join(category_names)}

Debes responder con:
1. Una pregunta breve (máximo 20 palabras) que funcione como eje problemático
2. Una oración que comience con "A través de este eje los alumnos..." explicando qué lograrán

Responde solo con la pregunta y la oración, sin títulos ni encabezados."""

    try:
        response = ai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=16000
        )
        content = response.choices[0].message.content
        print(f"[AI] Generated problem_edge: {content[:100] if content else 'EMPTY'}...")
        return content or ""
    except Exception as e:
        print(f"[AI] Error generating problem_edge: {type(e).__name__}: {e}")
        raise


def generate_methodological_strategies(area_name: str, subjects: list, categories: list, nuclei: list) -> dict:
    """Generate methodological strategies with type and context."""
    subject_names = [s["name"] for s in subjects]
    category_names = [c["name"] for c in categories]
    nucleus_names = [n["name"] for n in nuclei]

    strategy_types_desc = "\n".join([f"- {k}: {v}" for k, v in STRATEGY_TYPES.items()])

    prompt = f"""Eres un experto en planificación educativa. Genera una estrategia metodológica para el área de {area_name}.

Materias involucradas: {', '.join(subject_names)}
Núcleos problemáticos: {', '.join(nucleus_names)}
Categorías/conceptos a enseñar: {', '.join(category_names)}

Tipos de estrategia disponibles:
{strategy_types_desc}

Debes:
1. Elegir el tipo de estrategia más apropiado según el contexto (proyecto, taller_laboratorio, o ateneo_debate)
2. Escribir UN solo párrafo corto y enfocado explicando cómo se implementará

Responde en formato JSON con esta estructura exacta:
{{"type": "proyecto|taller_laboratorio|ateneo_debate", "context": "Párrafo breve..."}}

Solo responde con el JSON, sin explicaciones adicionales."""

    try:
        response = ai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=16000
        )
        content = response.choices[0].message.content
        content = content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        result = json.loads(content)
        # Validate type
        if result.get("type") not in STRATEGY_TYPES:
            result["type"] = "proyecto"
        print(f"[AI] Generated strategy: type={result.get('type')}, context={result.get('context', '')[:100]}...")
        return result
    except Exception as e:
        print(f"[AI] Error generating strategy: {type(e).__name__}: {e}")
        # Fallback
        return {"type": "proyecto", "context": ""}


def generate_eval_criteria(area_name: str, subjects: list, categories: list, nuclei: list) -> str:
    """Generate evaluation criteria for a coordination document."""
    subject_names = [s["name"] for s in subjects]
    category_names = [c["name"] for c in categories]
    nucleus_names = [n["name"] for n in nuclei]

    prompt = f"""Eres un experto en planificación educativa. Genera criterios de evaluación para el área de {area_name}.

Materias involucradas: {', '.join(subject_names)}
Núcleos problemáticos: {', '.join(nucleus_names)}
Categorías/conceptos a evaluar: {', '.join(category_names)}

Requisitos:
1. Máximo 5 criterios
2. Cada criterio debe tener máximo 40 caracteres
3. Formato simple: solo el criterio, sin escalas ni notas numéricas

Responde solo con bullets (guiones), sin títulos ni encabezados."""

    try:
        response = ai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=16000
        )
        content = response.choices[0].message.content
        print(f"[AI] Generated eval_criteria: {content[:100] if content else 'EMPTY'}...")
        return content or ""
    except Exception as e:
        print(f"[AI] Error generating eval_criteria: {type(e).__name__}: {e}")
        raise


# Async versions of generate functions for parallel execution

async def async_generate_problem_edge(area_name: str, subjects: list, categories: list, nuclei: list) -> str:
    """Async version: Generate the problem edge for a coordination document."""
    subject_names = [s["name"] for s in subjects]
    category_names = [c["name"] for c in categories]
    nucleus_names = [n["name"] for n in nuclei]

    prompt = f"""Eres un experto en planificación educativa. Genera un planteamiento de problema para el área de {area_name}.

Materias involucradas: {', '.join(subject_names)}
Núcleos problemáticos: {', '.join(nucleus_names)}
Categorías/conceptos a enseñar: {', '.join(category_names)}

Debes responder con:
1. Una pregunta breve (máximo 20 palabras) que funcione como eje problemático
2. Una oración que comience con "A través de este eje los alumnos..." explicando qué lograrán

Responde solo con la pregunta y la oración, sin títulos ni encabezados."""

    try:
        response = await async_ai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=16000
        )
        content = response.choices[0].message.content
        print(f"[AI] Generated problem_edge: {content[:100] if content else 'EMPTY'}...")
        return content or ""
    except Exception as e:
        print(f"[AI] Error generating problem_edge: {type(e).__name__}: {e}")
        raise


async def async_generate_methodological_strategies(area_name: str, subjects: list, categories: list, nuclei: list) -> dict:
    """Async version: Generate methodological strategies with type and context."""
    subject_names = [s["name"] for s in subjects]
    category_names = [c["name"] for c in categories]
    nucleus_names = [n["name"] for n in nuclei]

    strategy_types_desc = "\n".join([f"- {k}: {v}" for k, v in STRATEGY_TYPES.items()])

    prompt = f"""Eres un experto en planificación educativa. Genera una estrategia metodológica para el área de {area_name}.

Materias involucradas: {', '.join(subject_names)}
Núcleos problemáticos: {', '.join(nucleus_names)}
Categorías/conceptos a enseñar: {', '.join(category_names)}

Tipos de estrategia disponibles:
{strategy_types_desc}

Debes:
1. Elegir el tipo de estrategia más apropiado según el contexto (proyecto, taller_laboratorio, o ateneo_debate)
2. Escribir UN solo párrafo corto y enfocado explicando cómo se implementará

Responde en formato JSON con esta estructura exacta:
{{"type": "proyecto|taller_laboratorio|ateneo_debate", "context": "Párrafo breve..."}}

Solo responde con el JSON, sin explicaciones adicionales."""

    try:
        response = await async_ai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=16000
        )
        content = response.choices[0].message.content
        content = content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        result = json.loads(content)
        if result.get("type") not in STRATEGY_TYPES:
            result["type"] = "proyecto"
        print(f"[AI] Generated strategy: type={result.get('type')}, context={result.get('context', '')[:100]}...")
        return result
    except Exception as e:
        print(f"[AI] Error generating strategy: {type(e).__name__}: {e}")
        return {"type": "proyecto", "context": ""}


async def async_generate_eval_criteria(area_name: str, subjects: list, categories: list, nuclei: list) -> str:
    """Async version: Generate evaluation criteria for a coordination document."""
    subject_names = [s["name"] for s in subjects]
    category_names = [c["name"] for c in categories]
    nucleus_names = [n["name"] for n in nuclei]

    prompt = f"""Eres un experto en planificación educativa. Genera criterios de evaluación para el área de {area_name}.

Materias involucradas: {', '.join(subject_names)}
Núcleos problemáticos: {', '.join(nucleus_names)}
Categorías/conceptos a evaluar: {', '.join(category_names)}

Requisitos:
1. Máximo 5 criterios
2. Cada criterio debe tener máximo 40 caracteres
3. Formato simple: solo el criterio, sin escalas ni notas numéricas

Responde solo con bullets (guiones), sin títulos ni encabezados."""

    try:
        response = await async_ai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=16000
        )
        content = response.choices[0].message.content
        print(f"[AI] Generated eval_criteria: {content[:100] if content else 'EMPTY'}...")
        return content or ""
    except Exception as e:
        print(f"[AI] Error generating eval_criteria: {type(e).__name__}: {e}")
        raise


def generate_class_plans(subjects_data: dict, subjects: list, categories: list) -> dict:
    category_map = {c["id"]: c["name"] for c in categories}
    subject_map = {s["id"]: s["name"] for s in subjects}

    updated_subjects_data = {}

    for subject_id, data in subjects_data.items():
        subject_name = subject_map.get(int(subject_id), f"Materia {subject_id}")
        class_count = data.get("class_count", 10)
        subject_category_ids = data.get("category_ids", [])
        subject_category_names = [category_map.get(cid, f"Cat {cid}") for cid in subject_category_ids]

        prompt = f"""Genera un plan de clases para la materia {subject_name}.
Total de clases: {class_count}
Categorías/conceptos a cubrir: {', '.join(subject_category_names)}

Para cada clase, genera:
- Un título breve y descriptivo
- Un objetivo de aprendizaje específico para esa clase
- Los IDs de categorías que se trabajan en esa clase (de la lista: {subject_category_ids})

Responde en formato JSON como un array de objetos con esta estructura:
[{{"class_number": 1, "title": "Título de la clase", "objective": "Objetivo de aprendizaje de la clase", "category_ids": [1, 2]}}]

Solo responde con el JSON, sin explicaciones adicionales."""

        try:
            response = ai_client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT,
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=16000
            )
            content = response.choices[0].message.content
            # Parse JSON from response
            content = content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            class_plan = json.loads(content)
        except Exception as e:
            # Fallback: generate basic plan without AI
            class_plan = []
            cats_per_class = max(1, len(subject_category_ids) // class_count) if subject_category_ids else 0
            for i in range(class_count):
                start_idx = (i * cats_per_class) % len(subject_category_ids) if subject_category_ids else 0
                end_idx = start_idx + cats_per_class
                class_cats = subject_category_ids[start_idx:end_idx] if subject_category_ids else []
                class_plan.append({
                    "class_number": i + 1,
                    "title": f"Clase {i + 1}",
                    "objective": "",
                    "category_ids": class_cats
                })

        updated_subjects_data[subject_id] = {
            **data,
            "class_plan": class_plan
        }

    return updated_subjects_data


def generate_lesson_moment_content(
    moment_type: str,
    subject_name: str,
    class_title: str,
    objective: str,
    activity_names: list,
    custom_text: str = ""
) -> str:
    """Generate content for a lesson moment (apertura, desarrollo, cierre) using AI."""

    moment_descriptions = {
        "apertura": "Apertura/Motivación - el momento inicial de la clase para captar la atención y motivar a los estudiantes",
        "desarrollo": "Desarrollo/Construcción - el momento central de la clase donde se desarrolla el contenido principal",
        "cierre": "Cierre/Metacognición - el momento final para reflexionar, consolidar aprendizajes y evaluar comprensión"
    }

    moment_desc = moment_descriptions.get(moment_type, moment_type)
    activities_str = ", ".join(activity_names) if activity_names else "actividades variadas"

    prompt = f"""Eres un experto en planificación educativa. Genera una descripción para el momento de {moment_desc} de una clase.

Materia: {subject_name}
Tema de la clase: {class_title}
Objetivo: {objective}
Estrategias/Actividades seleccionadas: {activities_str}
{f'Notas adicionales del docente: {custom_text}' if custom_text else ''}

IMPORTANTE - Estilo de redacción:
- Escribe en tercera persona del singular, presente indicativo, como documento de planificación formal
- Usa frases como: "Se inicia la clase...", "El docente presenta...", "Se propone a los estudiantes...", "Se cierra la actividad..."
- NO uses imperativo (no digas "presente", "haga", "pida")
- NO uses primera persona (no digas "presento", "hago")

Ejemplo del estilo correcto:
"Al iniciar la clase se capta la atención de los estudiantes presentando una situación problemática real. El docente plantea preguntas orientadoras que conectan el tema con experiencias cotidianas. Se promueve la participación mediante una lluvia de ideas..."

Escribe 2-3 párrafos describiendo qué sucede en este momento de la clase, aplicando las estrategias seleccionadas. No uses encabezados ni listas numeradas."""

    try:
        response = ai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=16000
        )
        content = response.choices[0].message.content
        print(f"[AI] Generated {moment_type} content: {content[:100] if content else 'EMPTY'}...")
        return content or ""
    except Exception as e:
        print(f"[AI] Error generating {moment_type} content: {type(e).__name__}: {e}")
        return f"Error al generar contenido. Por favor, usa el chat con Alizia para generar el contenido de {moment_type}."


# Chat function calling tools
CHAT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "update_document_title",
            "description": "Actualiza el título del documento de coordinación",
            "parameters": {
                "type": "object",
                "properties": {
                    "new_title": {
                        "type": "string",
                        "description": "El nuevo título para el documento"
                    }
                },
                "required": ["new_title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_problem_edge",
            "description": "Actualiza el planteamiento del problema del documento",
            "parameters": {
                "type": "object",
                "properties": {
                    "new_problem_edge": {
                        "type": "string",
                        "description": "El nuevo planteamiento del problema"
                    }
                },
                "required": ["new_problem_edge"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_methodological_strategy",
            "description": "REEMPLAZA COMPLETAMENTE la estrategia metodológica del documento. Puede cambiar el tipo (proyecto, taller_laboratorio, ateneo_debate) y/o el contexto.",
            "parameters": {
                "type": "object",
                "properties": {
                    "strategy_type": {
                        "type": "string",
                        "enum": ["proyecto", "taller_laboratorio", "ateneo_debate"],
                        "description": "El tipo de estrategia: proyecto, taller_laboratorio, o ateneo_debate"
                    },
                    "context": {
                        "type": "string",
                        "description": "El contexto/descripción de la estrategia metodológica"
                    }
                },
                "required": ["strategy_type", "context"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "append_to_methodological_strategy",
            "description": "AGREGA texto al final del contexto de la estrategia metodológica existente. Usar cuando el usuario quiere añadir algo sin borrar lo existente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text_to_append": {
                        "type": "string",
                        "description": "El texto a agregar al final del contexto de la estrategia existente"
                    }
                },
                "required": ["text_to_append"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_eval_criteria",
            "description": "Actualiza los criterios de evaluación del documento",
            "parameters": {
                "type": "object",
                "properties": {
                    "new_eval_criteria": {
                        "type": "string",
                        "description": "Los nuevos criterios de evaluación"
                    }
                },
                "required": ["new_eval_criteria"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_class_title",
            "description": "Actualiza el título de una clase específica de una materia",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject_id": {
                        "type": "integer",
                        "description": "ID de la materia"
                    },
                    "class_number": {
                        "type": "integer",
                        "description": "Número de la clase (1-indexed)"
                    },
                    "new_title": {
                        "type": "string",
                        "description": "El nuevo título para la clase"
                    }
                },
                "required": ["subject_id", "class_number", "new_title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_class_objective",
            "description": "Actualiza el objetivo de una clase específica de una materia",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject_id": {
                        "type": "integer",
                        "description": "ID de la materia"
                    },
                    "class_number": {
                        "type": "integer",
                        "description": "Número de la clase (1-indexed)"
                    },
                    "new_objective": {
                        "type": "string",
                        "description": "El nuevo objetivo para la clase"
                    }
                },
                "required": ["subject_id", "class_number", "new_objective"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_class_categories",
            "description": "Actualiza las categorías asignadas a una clase específica",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject_id": {
                        "type": "integer",
                        "description": "ID de la materia"
                    },
                    "class_number": {
                        "type": "integer",
                        "description": "Número de la clase (1-indexed)"
                    },
                    "category_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Lista de IDs de categorías para asignar a la clase"
                    }
                },
                "required": ["subject_id", "class_number", "category_ids"]
            }
        }
    }
]


# Proposal chat tools for agreements and decisions
PROPOSAL_CHAT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "complete_agreement",
            "description": "Registra la decisión y marca el acuerdo como completado. Usar cuando el docente expresa una decisión clara o confirma su elección.",
            "parameters": {
                "type": "object",
                "properties": {
                    "decision": {
                        "type": "string",
                        "description": "La decisión tomada (ej: 'Aparato respiratorio', 'Presentación a familias')"
                    }
                },
                "required": ["decision"]
            }
        }
    }
]


def format_alizia_context(context: dict) -> str:
    """Convert alizia_context dict to formatted text for the system prompt."""
    if not context:
        return ""

    sections = []

    # Valid options
    if context.get("valid_options"):
        options_text = "\n".join([
            f"  - {opt.get('value', '')}" + (f" ({opt.get('element', '')})" if opt.get('element') else "") + (f": {opt.get('notes', '')}" if opt.get('notes') else "")
            for opt in context["valid_options"]
        ])
        sections.append(f"OPCIONES VÁLIDAS:\n{options_text}")

    # Knowledge/background
    if context.get("knowledge"):
        knowledge_text = "\n".join([f"  - {k}" for k in context["knowledge"]])
        sections.append(f"CONOCIMIENTO DE CONTEXTO:\n{knowledge_text}")

    # Guiding questions
    if context.get("guiding_questions"):
        questions_text = "\n".join([f"  - {q}" for q in context["guiding_questions"]])
        sections.append(f"PREGUNTAS ORIENTADORAS (usa estas para guiar la conversación):\n{questions_text}")

    # Warning signals
    if context.get("warning_signals"):
        warnings_text = "\n".join([
            f"  - Si {w.get('trigger', '')}: {w.get('response', '')}"
            for w in context["warning_signals"]
        ])
        sections.append(f"SEÑALES DE ALERTA:\n{warnings_text}")

    # Stance
    if context.get("stance"):
        stance_text = context["stance"]
        if context.get("stance_examples"):
            examples = "\n".join([f"    Ejemplo: \"{ex}\"" for ex in context["stance_examples"]])
            stance_text += f"\n{examples}"
        sections.append(f"POSTURA A ADOPTAR: {stance_text}")

    # Acceptance criteria
    if context.get("acceptance_criteria"):
        sections.append(f"CRITERIO DE ACEPTACIÓN (cuándo marcar como completado):\n  {context['acceptance_criteria']}")

    if not sections:
        return ""

    return "\n\n--- CONTEXTO ESPECÍFICO PARA ESTA DECISIÓN ---\n" + "\n\n".join(sections) + "\n--- FIN CONTEXTO ESPECÍFICO ---\n"


def get_proposal_chat_system_prompt(
    agreement_title: str,
    agreement_description: str,
    responsible_type: str,
    proposal_name: str,
    existing_value: str = None,
    alizia_context: dict = None,
    teacher_name: str = None,
    subject_name: str = None
) -> str:
    """Generate system prompt based on responsible type."""

    teacher_info = f"Estás hablando con {teacher_name}" if teacher_name else "Estás hablando con un docente"
    if subject_name:
        teacher_info += f" que está trabajando en la materia {subject_name}"

    base_context = f"""Eres Alizia, una Docente Remota (DR) de tecnología educativa que ayuda a docentes de aula (DA) a implementar proyectos de pensamiento computacional.

{teacher_info}.

Proyecto actual: {proposal_name}
Acuerdo en discusión: {agreement_title}
Descripción: {agreement_description}
"""

    if existing_value:
        base_context += f"\nValor actual del acuerdo: {existing_value}\n"

    if responsible_type == "da_solo":
        tone = """
TONO: Sugerente y orientador
- El DA tiene la decisión final sobre este acuerdo
- Tu rol es ofrecer sugerencias, hacer preguntas que ayuden a reflexionar, y validar las decisiones del DA
- NO impongas tu criterio, pero sí puedes ofrecer alternativas o señalar consideraciones importantes
- Cuando el DA exprese una decisión clara, usa complete_agreement para registrarla y cerrar el acuerdo
- AL USAR complete_agreement: SIEMPRE genera también un mensaje de texto validando la decisión del docente (ej: "Excelente decisión, queda registrado que...")
"""
    else:  # conjunto
        tone = """
TONO: Firme y co-decisor
- Este es un acuerdo CONJUNTO donde tú (Alizia, la Docente Remota) participas activamente en la decisión
- Puedes y DEBES expresar tu opinión fundamentada
- Puedes proponer alternativas y negociar hasta llegar a un acuerdo mutuo
- No aceptes decisiones que consideres pedagógicamente inadecuadas sin discutirlas primero
- Cuando lleguen a un acuerdo conjunto, usa complete_agreement para registrarlo y cerrar el acuerdo
- AL USAR complete_agreement: SIEMPRE genera también un mensaje celebrando el acuerdo conjunto (ej: "¡Perfecto! Hemos acordado juntos que...")
"""

    # Add contextual prompt if available
    context_prompt = format_alizia_context(alizia_context) if alizia_context else ""

    return base_context + tone + context_prompt + """

IMPORTANTE:
- Responde siempre en español, de manera cálida pero profesional
- Mantén las respuestas concisas (2-3 párrafos máximo)
- Haz preguntas clarificadoras cuando sea necesario
- Celebra las buenas decisiones del docente
"""


def process_proposal_chat(
    agreement_title: str,
    agreement_description: str,
    responsible_type: str,
    proposal_name: str,
    history: list,
    existing_value: str = None,
    alizia_context: dict = None,
    teacher_name: str = None,
    subject_name: str = None
) -> dict:
    """Process chat messages for proposal agreements."""

    system_prompt = get_proposal_chat_system_prompt(
        agreement_title, agreement_description, responsible_type, proposal_name, existing_value, alizia_context,
        teacher_name, subject_name
    )

    messages = [{"role": "system", "content": system_prompt}]
    for item in history:
        messages.append({"role": item["role"], "content": item["content"]})

    response = ai_client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
        tools=PROPOSAL_CHAT_TOOLS,
        tool_choice="auto",
        max_completion_tokens=16000
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    result = {
        "response": response_message.content or "",
        "agreement_completed": False,
        "decision_value": None
    }

    if tool_calls:
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"[ProposalChat] Function: {function_name}, Args: {args}")

            if function_name == "complete_agreement":
                result["decision_value"] = args["decision"]
                result["agreement_completed"] = True
                if not result["response"]:
                    result["response"] = f"Perfecto, he registrado: {args['decision']}. ¡Acuerdo completado!"

    return result


# Teacher lesson plan chat tools
TEACHER_LESSON_CHAT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "update_moment_content",
            "description": "Actualiza el contenido de un momento de la clase (apertura, desarrollo o cierre)",
            "parameters": {
                "type": "object",
                "properties": {
                    "moment_type": {
                        "type": "string",
                        "enum": ["apertura", "desarrollo", "cierre"],
                        "description": "El momento a actualizar"
                    },
                    "new_content": {
                        "type": "string",
                        "description": "El nuevo contenido para el momento. Debe estar escrito en tercera persona, presente indicativo (ej: 'Se inicia la clase...', 'El docente presenta...')"
                    }
                },
                "required": ["moment_type", "new_content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_objective",
            "description": "Actualiza el objetivo de la clase",
            "parameters": {
                "type": "object",
                "properties": {
                    "new_objective": {
                        "type": "string",
                        "description": "El nuevo objetivo de la clase"
                    }
                },
                "required": ["new_objective"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_title",
            "description": "Actualiza el título de la clase",
            "parameters": {
                "type": "object",
                "properties": {
                    "new_title": {
                        "type": "string",
                        "description": "El nuevo título de la clase"
                    }
                },
                "required": ["new_title"]
            }
        }
    }
]


def process_teacher_lesson_chat(plan: dict, history: list, activities: list) -> dict:
    """Process chat messages for teacher lesson plan editing."""
    activity_map = {a["id"]: a["name"] for a in activities}
    moments = plan.get("moments") or {}

    # Build info about current moments
    moments_info = []
    for moment_type in ["apertura", "desarrollo", "cierre"]:
        moment_data = moments.get(moment_type, {})
        content = moment_data.get("generatedContent", "Sin contenido")
        activity_ids = moment_data.get("activities", [])
        activity_names = [activity_map.get(aid, f"Actividad {aid}") for aid in activity_ids]
        moments_info.append(f"- {moment_type.capitalize()}: Estrategias: {', '.join(activity_names) or 'ninguna'}. Contenido: {content[:200]}...")

    system_prompt = f"""Eres Alizia, una asistente de IA para planificación de clases. Ayudas a los docentes a mejorar sus planes de clase.

Plan de clase actual:
- Título: {plan.get('title', 'Sin título')}
- Materia: {plan.get('subject_name', 'Desconocida')}
- Objetivo: {plan.get('objective', 'Sin objetivo')}

Momentos de la clase:
{chr(10).join(moments_info)}

IMPORTANTE sobre el estilo de redacción:
- El contenido debe estar en TERCERA PERSONA, PRESENTE INDICATIVO
- Usa frases como: "Se inicia la clase...", "El docente presenta...", "Se propone a los estudiantes...", "Se cierra la actividad..."
- NO uses imperativo (no digas "presente", "haga", "pida")
- NO uses primera persona (no digas "presento", "hago")

Cuando el usuario pida cambios, usa las funciones disponibles para modificar el plan.
Responde siempre en español de manera amigable y concisa."""

    messages = [{"role": "system", "content": system_prompt}]
    for item in history:
        messages.append({"role": item["role"], "content": item["content"]})

    response = ai_client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
        tools=TEACHER_LESSON_CHAT_TOOLS,
        tool_choice="auto",
        max_completion_tokens=16000
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    updates = {}
    changes_made = []

    if tool_calls:
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"[TeacherChat] Function: {function_name}, Args: {args}")

            if function_name == "update_moment_content":
                moment_type = args["moment_type"]
                new_content = args["new_content"]
                if "moments" not in updates:
                    # Deep copy to preserve all nested data
                    updates["moments"] = copy.deepcopy(moments)
                if moment_type not in updates["moments"]:
                    updates["moments"][moment_type] = moments.get(moment_type, {}).copy()
                updates["moments"][moment_type]["generatedContent"] = new_content
                changes_made.append(f"contenido de {moment_type} actualizado")

            elif function_name == "update_objective":
                updates["objective"] = args["new_objective"]
                changes_made.append("objetivo actualizado")

            elif function_name == "update_title":
                updates["title"] = args["new_title"]
                changes_made.append("título actualizado")

    response_text = response_message.content or ""
    if changes_made and not response_text:
        response_text = f"¡Listo! He realizado los siguientes cambios: {', '.join(changes_made)}."

    return {
        "response": response_text,
        "updates": updates,
        "changes_made": changes_made
    }


def process_chat_message(doc: dict, history: list, subjects: list, categories: list) -> dict:
    category_map = {c["id"]: c["name"] for c in categories}
    subject_map = {s["id"]: s["name"] for s in subjects}
    # Also create a name-to-id map for subjects
    subject_name_to_id = {s["name"].lower(): s["id"] for s in subjects}

    subjects_data = doc.get("subjects_data") or {}
    subjects_info = []
    for sid, sdata in subjects_data.items():
        sname = subject_map.get(int(sid), f"Materia {sid}")
        class_plan = sdata.get("class_plan", [])
        classes_info = [f"Clase {c['class_number']}: {c.get('title', 'Sin título')} (obj: {c.get('objective', 'sin objetivo')[:50]}...)" for c in class_plan[:5]]
        subjects_info.append(f"- {sname} (ID: {sid}): {len(class_plan)} clases. Primeras: {', '.join(classes_info)}")

    # Handle methodological_strategies (now JSONB with type and context)
    current_strategy = doc.get('methodological_strategies') or {}
    if isinstance(current_strategy, str):
        # Legacy string format
        strategy_display = f"Contexto: {current_strategy}"
    elif current_strategy:
        strategy_type = current_strategy.get('type', 'proyecto')
        strategy_context = current_strategy.get('context', '')
        strategy_display = f"Tipo: {strategy_type}\nContexto: {strategy_context}"
    else:
        strategy_display = 'No generada aún'

    current_problem_edge = doc.get('problem_edge', '') or 'No generado aún'
    current_eval_criteria = doc.get('eval_criteria', '') or 'No generados aún'

    system_prompt = f"""Eres Alizia, una asistente de IA para planificación educativa. Ayudas a modificar documentos de coordinación.

Documento actual:
- Título: {doc['name']}

- Planteamiento del problema:
\"\"\"
{current_problem_edge}
\"\"\"

- Estrategia metodológica (NO la modifiques a menos que te lo pidan explícitamente):
\"\"\"
{strategy_display}
\"\"\"

- Criterios de evaluación:
\"\"\"
{current_eval_criteria}
\"\"\"

Materias y sus clases (USA ESTOS IDs EXACTOS):
{chr(10).join(subjects_info)}

Categorías disponibles:
{', '.join([f"{c['name']} (ID: {c['id']})" for c in categories[:20]])}

IMPORTANTE:
- Cuando modifiques una clase, usa el ID de la materia que aparece entre paréntesis arriba.
- Para modificar el planteamiento del problema, usa update_problem_edge.
- Si el usuario pide AGREGAR algo al final de la estrategia, usa append_to_methodological_strategy (NO reemplaces todo).
- Si el usuario pide REEMPLAZAR o CAMBIAR completamente la estrategia (tipo o contexto), usa update_methodological_strategy.
  - Tipos de estrategia disponibles: proyecto, taller_laboratorio, ateneo_debate
- Para modificar los criterios de evaluación, usa update_eval_criteria.
- Para modificar el objetivo de una clase, usa update_class_objective.
- Cuando el usuario pida modificar algo, usa las funciones disponibles para hacer los cambios.
- Si no hay una función para lo que pide, explica qué puedes hacer.
Responde siempre en español de manera amigable y concisa."""

    # Build messages array from history
    messages = [{"role": "system", "content": system_prompt}]
    for item in history:
        messages.append({"role": item["role"], "content": item["content"]})

    response = ai_client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
        tools=CHAT_TOOLS,
        tool_choice="auto",
        max_completion_tokens=16000
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    updates = {}
    changes_made = []

    if tool_calls:
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"[Chat] Function: {function_name}, Args: {args}")  # Debug log

            if function_name == "update_document_title":
                updates["name"] = args["new_title"]
                changes_made.append(f"título cambiado a '{args['new_title']}'")

            elif function_name == "update_problem_edge":
                updates["problem_edge"] = args["new_problem_edge"]
                changes_made.append("planteamiento del problema actualizado")

            elif function_name == "update_methodological_strategy":
                updates["methodological_strategies"] = {
                    "type": args["strategy_type"],
                    "context": args["context"]
                }
                changes_made.append(f"estrategia metodológica actualizada (tipo: {args['strategy_type']})")

            elif function_name == "append_to_methodological_strategy":
                current_strategy = doc.get('methodological_strategies') or {}
                if isinstance(current_strategy, str):
                    # Handle legacy string format
                    current_strategy = {"type": "proyecto", "context": current_strategy}
                current_context = current_strategy.get('context', '') or ''
                new_text = args["text_to_append"]
                updates["methodological_strategies"] = {
                    "type": current_strategy.get("type", "proyecto"),
                    "context": current_context.rstrip() + " " + new_text
                }
                changes_made.append("texto agregado al final de la estrategia metodológica")

            elif function_name == "update_eval_criteria":
                updates["eval_criteria"] = args["new_eval_criteria"]
                changes_made.append("criterios de evaluación actualizados")

            elif function_name == "update_class_title":
                sid = str(args["subject_id"])
                class_num = args["class_number"]
                new_title = args["new_title"]
                found = False

                # Try to find the subject in subjects_data
                for key in subjects_data.keys():
                    if str(key) == sid:
                        if "class_plan" in subjects_data[key]:
                            for c in subjects_data[key]["class_plan"]:
                                if c["class_number"] == class_num:
                                    c["title"] = new_title
                                    found = True
                                    break
                        if found:
                            updates["subjects_data"] = subjects_data
                            subject_name = subject_map.get(int(key), f"Materia {key}")
                            changes_made.append(f"título de clase {class_num} de {subject_name} cambiado a '{new_title}'")
                            break

                if not found:
                    print(f"[Chat] Could not find subject {sid} or class {class_num}. Available keys: {list(subjects_data.keys())}")

            elif function_name == "update_class_objective":
                sid = str(args["subject_id"])
                class_num = args["class_number"]
                new_objective = args["new_objective"]
                found = False

                for key in subjects_data.keys():
                    if str(key) == sid:
                        if "class_plan" in subjects_data[key]:
                            for c in subjects_data[key]["class_plan"]:
                                if c["class_number"] == class_num:
                                    c["objective"] = new_objective
                                    found = True
                                    break
                        if found:
                            updates["subjects_data"] = subjects_data
                            subject_name = subject_map.get(int(key), f"Materia {key}")
                            changes_made.append(f"objetivo de clase {class_num} de {subject_name} actualizado")
                            break

                if not found:
                    print(f"[Chat] Could not find subject {sid} or class {class_num}. Available keys: {list(subjects_data.keys())}")

            elif function_name == "update_class_categories":
                sid = str(args["subject_id"])
                class_num = args["class_number"]
                new_cats = args["category_ids"]
                found = False

                for key in subjects_data.keys():
                    if str(key) == sid:
                        if "class_plan" in subjects_data[key]:
                            for c in subjects_data[key]["class_plan"]:
                                if c["class_number"] == class_num:
                                    c["category_ids"] = new_cats
                                    found = True
                                    break
                        if found:
                            updates["subjects_data"] = subjects_data
                            subject_name = subject_map.get(int(key), f"Materia {key}")
                            changes_made.append(f"categorías de clase {class_num} de {subject_name} actualizadas")
                            break

    # Build response based on what actually happened
    if changes_made:
        assistant_response = f"Listo! He realizado los siguientes cambios: {', '.join(changes_made)}."
    elif response_message.content:
        assistant_response = response_message.content
    else:
        assistant_response = "No pude realizar los cambios solicitados. Por favor, verifica el nombre de la materia y el número de clase."

    return {
        "response": assistant_response,
        "updates": updates
    }


# Shared classes helper function
def get_shared_classes_for_area(course_schedule: dict, area_subject_names: list) -> list:
    """
    Detects slots with shared_with where both subjects belong to the area.
    Returns: [{ day, time, subject, shared_with }]
    """
    shared_classes = []
    if not course_schedule:
        return shared_classes

    for day, slots in course_schedule.items():
        if not isinstance(slots, list):
            continue
        for slot in slots:
            if not isinstance(slot, dict):
                continue
            subject = slot.get("subject")
            shared_with = slot.get("shared_with")
            time = slot.get("time")

            # Check if this is a shared class and both subjects are in the area
            if shared_with and subject in area_subject_names and shared_with in area_subject_names:
                shared_classes.append({
                    "day": day,
                    "time": time,
                    "subject": subject,
                    "shared_with": shared_with
                })

    return shared_classes


def calculate_shared_class_numbers(course_schedule: dict, subject_name: str,
                                    area_subject_names: list, total_classes: int) -> dict:
    """
    Calcula qué números de clase caen en horarios compartidos y con qué materia.

    Args:
        course_schedule: Schedule del curso
        subject_name: Nombre de la materia
        area_subject_names: Lista de materias del área
        total_classes: Total de clases planificadas para la materia

    Returns:
        Dict mapping class numbers to shared subject name: {3: "Física", 8: "Física", ...}
    """
    if not course_schedule or total_classes <= 0:
        return {}

    days_order = ["monday", "tuesday", "wednesday", "thursday", "friday"]

    # First pass: find weekly pattern
    weekly_class_count = 0
    shared_positions = []  # (position, shared_with_subject_name)

    for day in days_order:
        slots = course_schedule.get(day, [])
        if not isinstance(slots, list):
            continue

        for slot in slots:
            if not isinstance(slot, dict):
                continue

            slot_subject = slot.get("subject")
            slot_shared_with = slot.get("shared_with")

            # Check if this subject appears in this slot
            is_subject_direct = slot_subject == subject_name
            is_subject_shared = slot_shared_with == subject_name

            if is_subject_direct or is_subject_shared:
                # Check if this is a shared class with another area subject
                shared_with_name = None
                if is_subject_direct and slot_shared_with and slot_shared_with in area_subject_names:
                    shared_with_name = slot_shared_with
                elif is_subject_shared and slot_subject in area_subject_names:
                    shared_with_name = slot_subject

                if shared_with_name:
                    shared_positions.append((weekly_class_count, shared_with_name))

                weekly_class_count += 1

    if weekly_class_count == 0:
        return {}

    # Generate all shared class numbers up to total_classes
    shared_class_info = {}
    for pos, shared_with_name in shared_positions:
        class_num = pos + 1  # 1-indexed
        while class_num <= total_classes:
            shared_class_info[class_num] = shared_with_name
            class_num += weekly_class_count

    return shared_class_info


def find_partner_course_subject_id(cur, course_subject_id: int, shared_class_info: dict, class_number: int) -> int | None:
    """
    Encuentra el course_subject_id del profesor compañero para una clase compartida.

    Args:
        cur: Database cursor
        course_subject_id: Current teacher's course_subject_id
        shared_class_info: Dict from calculate_shared_class_numbers {class_num: partner_subject_name}
        class_number: The class number to check

    Returns:
        Partner's course_subject_id or None if not a shared class
    """
    if class_number not in shared_class_info:
        return None

    partner_subject_name = shared_class_info[class_number]

    # Get current course_subject details
    cur.execute("""
        SELECT cs.course_id, s.area_id
        FROM course_subjects cs
        JOIN subjects s ON cs.subject_id = s.id
        WHERE cs.id = %s
    """, (course_subject_id,))
    current = cur.fetchone()

    if not current:
        return None

    # Find partner course_subject (same course, partner subject name, same area)
    cur.execute("""
        SELECT cs.id
        FROM course_subjects cs
        JOIN subjects s ON cs.subject_id = s.id
        WHERE cs.course_id = %s
          AND s.name = %s
          AND s.area_id = %s
          AND cs.id != %s
    """, (current['course_id'], partner_subject_name, current['area_id'], course_subject_id))

    partner = cur.fetchone()
    return partner['id'] if partner else None


def get_shared_class_info_for_course_subject(cur, course_subject_id: int) -> dict:
    """
    Get shared class info for a course_subject.
    Returns dict mapping class_number to partner_subject_name.
    """
    # Get course_subject details
    cur.execute("""
        SELECT cs.*, s.name as subject_name, s.area_id, c.schedule
        FROM course_subjects cs
        JOIN subjects s ON cs.subject_id = s.id
        JOIN courses c ON cs.course_id = c.id
        WHERE cs.id = %s
    """, (course_subject_id,))
    cs = cur.fetchone()

    if not cs:
        return {}

    # Get all subjects in the same area
    cur.execute("SELECT name FROM subjects WHERE area_id = %s", (cs['area_id'],))
    area_subjects = [s['name'] for s in cur.fetchall()]

    # Get total classes from coordination document
    cur.execute("""
        SELECT subjects_data FROM coordination_documents
        WHERE area_id = %s AND status = 'published'
        ORDER BY created_at DESC LIMIT 1
    """, (cs['area_id'],))
    doc = cur.fetchone()

    total_classes = 0
    if doc and doc.get('subjects_data'):
        subject_data = doc['subjects_data'].get(str(cs['subject_id']), {})
        total_classes = len(subject_data.get('class_plan', []))

    if total_classes == 0:
        return {}

    return calculate_shared_class_numbers(
        cs.get('schedule') or {},
        cs['subject_name'],
        area_subjects,
        total_classes
    )


@app.get("/", response_model=RootResponse)
async def root():
    return {"message": "Annual Planning API", "docs": "/docs"}


@app.get("/users", response_model=List[UserResponse])
async def get_users():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users")
            return cur.fetchall()


@app.get("/users/by-phone/{phone}")
async def get_user_by_phone(phone: str):
    # Normalize phone: add + prefix if missing
    if not phone.startswith("+"):
        phone = f"+{phone}"
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE phone = %s", (phone,))
            user = cur.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            # Determine role: coordinator if referenced in areas.coordinator_id
            cur.execute("SELECT id, name FROM areas WHERE coordinator_id = %s", (user["id"],))
            coordinated_areas = cur.fetchall()
            # Check if teacher (has course_subjects)
            cur.execute("SELECT COUNT(*) as cnt FROM course_subjects WHERE teacher_id = %s", (user["id"],))
            is_teacher = cur.fetchone()["cnt"] > 0
            role = "coordinator" if coordinated_areas else ("teacher" if is_teacher else "user")
            return {
                **dict(user),
                "role": role,
                "coordinated_areas": coordinated_areas if coordinated_areas else []
            }


@app.get("/areas", response_model=List[AreaResponse])
async def get_areas():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM areas")
            return cur.fetchall()


@app.get("/subjects", response_model=List[SubjectResponse])
async def get_subjects():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM subjects")
            return cur.fetchall()


@app.get("/courses", response_model=List[CourseResponse])
async def get_courses():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM courses")
            return cur.fetchall()


@app.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
            return cur.fetchone()


@app.get("/courses/{course_id}/students", response_model=List[StudentResponse])
async def get_course_students(course_id: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM students WHERE course_id = %s ORDER BY name",
                (course_id,),
            )
            return cur.fetchall()


@app.get("/courses/{course_id}/shared-classes", response_model=SharedClassesResponse)
async def get_course_shared_classes(course_id: int, area_id: int):
    """Get shared classes for a course filtered by area."""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Get the course schedule
            cur.execute("SELECT schedule FROM courses WHERE id = %s", (course_id,))
            result = cur.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Course not found")

            schedule = result.get("schedule") or {}

            # Get subject names for the area
            cur.execute("SELECT name FROM subjects WHERE area_id = %s", (area_id,))
            area_subjects = cur.fetchall()
            area_subject_names = [s["name"] for s in area_subjects]

            # Get shared classes
            shared_classes = get_shared_classes_for_area(schedule, area_subject_names)

            return {
                "course_id": course_id,
                "area_id": area_id,
                "shared_classes": shared_classes
            }


@app.get("/course-subjects", response_model=List[CourseSubjectResponse])
async def get_course_subjects():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT cs.*,
                       c.name as course_name,
                       s.name as subject_name,
                       u.name as teacher_name
                FROM course_subjects cs
                JOIN courses c ON cs.course_id = c.id
                JOIN subjects s ON cs.subject_id = s.id
                JOIN users u ON cs.teacher_id = u.id
                ORDER BY cs.course_id, cs.subject_id
            """)
            return cur.fetchall()


@app.get("/teachers/{teacher_id}/courses", response_model=List[CourseSubjectResponse])
async def get_teacher_courses(teacher_id: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT cs.*,
                       c.name as course_name,
                       s.name as subject_name,
                       s.area_id
                FROM course_subjects cs
                JOIN courses c ON cs.course_id = c.id
                JOIN subjects s ON cs.subject_id = s.id
                WHERE cs.teacher_id = %s
                ORDER BY c.name, s.name
            """, (teacher_id,))
            return cur.fetchall()


@app.get("/problematic-nuclei", response_model=List[ProblematicNucleusResponse])
async def get_problematic_nuclei():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM problematic_nuclei")
            return cur.fetchall()


@app.get("/knowledge-areas", response_model=List[KnowledgeAreaResponse])
async def get_knowledge_areas():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM knowledge_areas")
            return cur.fetchall()


@app.get("/categories", response_model=List[CategoryResponse])
async def get_categories():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM categories")
            return cur.fetchall()


@app.get("/coordination-documents", response_model=List[CoordinationDocumentResponse])
async def get_coordination_documents():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM coordination_documents")
            return cur.fetchall()


@app.get("/coordination-documents/{doc_id}", response_model=CoordinationDocumentDetailResponse)
async def get_coordination_document(doc_id: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM coordination_documents WHERE id = %s", (doc_id,))
            doc = cur.fetchone()
            if not doc:
                raise HTTPException(status_code=404, detail="Document not found")

            # Fetch related data
            cur.execute("SELECT * FROM areas WHERE id = %s", (doc["area_id"],))
            area = cur.fetchone()

            cur.execute("SELECT * FROM subjects WHERE area_id = %s", (doc["area_id"],))
            subjects = cur.fetchall()

            # Fetch categories for this document
            category_ids = doc.get("category_ids") or []
            categories = []
            if category_ids:
                cur.execute("SELECT * FROM categories WHERE id = ANY(%s)", (category_ids,))
                categories = cur.fetchall()

            # Fetch nuclei for this document
            nucleus_ids = doc.get("nucleus_ids") or []
            nuclei = []
            if nucleus_ids:
                cur.execute("SELECT * FROM problematic_nuclei WHERE id = ANY(%s)", (nucleus_ids,))
                nuclei = cur.fetchall()

            return {
                **doc,
                "area": area,
                "subjects": subjects,
                "categories": categories,
                "nuclei": nuclei
            }


@app.patch("/coordination-documents/{doc_id}", response_model=CoordinationDocumentResponse)
async def update_coordination_document(doc_id: int, updates: CoordinationDocumentUpdate):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM coordination_documents WHERE id = %s", (doc_id,))
            doc = cur.fetchone()
            if not doc:
                raise HTTPException(status_code=404, detail="Document not found")

            update_fields = []
            values = []

            if updates.name is not None:
                update_fields.append("name = %s")
                values.append(updates.name)

            if updates.problem_edge is not None:
                update_fields.append("problem_edge = %s")
                values.append(updates.problem_edge)

            if updates.methodological_strategies is not None:
                update_fields.append("methodological_strategies = %s")
                values.append(json.dumps(updates.methodological_strategies))

            if updates.eval_criteria is not None:
                update_fields.append("eval_criteria = %s")
                values.append(updates.eval_criteria)

            if updates.subjects_data is not None:
                update_fields.append("subjects_data = %s")
                values.append(json.dumps(updates.subjects_data))

            if updates.status is not None:
                update_fields.append("status = %s")
                values.append(updates.status)

            if not update_fields:
                return doc

            values.append(doc_id)
            query = f"UPDATE coordination_documents SET {', '.join(update_fields)} WHERE id = %s RETURNING *"
            cur.execute(query, values)
            conn.commit()
            updated_doc = cur.fetchone()

            # Notify via webhook when document is published
            if updates.status == "published" and KAPSO_WEBHOOK_URL:
                try:
                    cur.execute("SELECT name FROM areas WHERE id = %s", (updated_doc["area_id"],))
                    area = cur.fetchone()
                    payload = json.dumps({
                        "event": "document_published",
                        "document_id": updated_doc["id"],
                        "document_name": updated_doc["name"],
                        "area_id": updated_doc["area_id"],
                        "area_name": area["name"] if area else "",
                    }).encode()
                    req = urllib.request.Request(
                        KAPSO_WEBHOOK_URL,
                        data=payload,
                        headers={"Content-Type": "application/json"},
                        method="POST",
                    )
                    urllib.request.urlopen(req, timeout=5)
                except Exception as e:
                    logger.warning(f"Failed to send publish webhook: {e}")

            return updated_doc


@app.delete("/coordination-documents/{doc_id}", response_model=DeleteResponse)
async def delete_coordination_document(doc_id: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM coordination_documents WHERE id = %s", (doc_id,))
            doc = cur.fetchone()
            if not doc:
                raise HTTPException(status_code=404, detail="Document not found")

            cur.execute("DELETE FROM coordination_documents WHERE id = %s", (doc_id,))
            conn.commit()
            return {"message": "Document deleted", "id": doc_id}


@app.post("/coordination-documents/{doc_id}/generate", response_model=CoordinationDocumentResponse)
async def generate_document_content(doc_id: int, request: GenerateRequest):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM coordination_documents WHERE id = %s", (doc_id,))
            doc = cur.fetchone()
            if not doc:
                raise HTTPException(status_code=404, detail="Document not found")

            cur.execute("SELECT * FROM areas WHERE id = %s", (doc["area_id"],))
            area = cur.fetchone()

            cur.execute("SELECT * FROM subjects WHERE area_id = %s", (doc["area_id"],))
            subjects = cur.fetchall()

            category_ids = doc.get("category_ids") or []
            categories = []
            if category_ids:
                cur.execute("SELECT * FROM categories WHERE id = ANY(%s)", (category_ids,))
                categories = cur.fetchall()

            nucleus_ids = doc.get("nucleus_ids") or []
            nuclei = []
            if nucleus_ids:
                cur.execute("SELECT * FROM problematic_nuclei WHERE id = ANY(%s)", (nucleus_ids,))
                nuclei = cur.fetchall()

            updates = {}
            area_name = area["name"] if area else "General"

            if request.generate_strategy:
                try:
                    # Run 3 AI calls in parallel using async versions
                    problem_edge, strategy, eval_criteria = await asyncio.gather(
                        async_generate_problem_edge(area_name, subjects, categories, nuclei),
                        async_generate_methodological_strategies(area_name, subjects, categories, nuclei),
                        async_generate_eval_criteria(area_name, subjects, categories, nuclei)
                    )
                    updates["problem_edge"] = problem_edge
                    updates["methodological_strategies"] = strategy
                    updates["eval_criteria"] = eval_criteria
                except Exception as e:
                    raise HTTPException(
                        status_code=503,
                        detail=f"Error al conectar con el servicio de IA: {type(e).__name__}"
                    )

            if request.generate_class_plans and doc.get("subjects_data"):
                subjects_data = generate_class_plans(
                    doc["subjects_data"],
                    subjects,
                    categories
                )
                updates["subjects_data"] = subjects_data

            # Update document
            if updates:
                update_fields = []
                values = []

                if "problem_edge" in updates:
                    update_fields.append("problem_edge = %s")
                    values.append(updates["problem_edge"])

                if "methodological_strategies" in updates:
                    update_fields.append("methodological_strategies = %s")
                    values.append(json.dumps(updates["methodological_strategies"]))

                if "eval_criteria" in updates:
                    update_fields.append("eval_criteria = %s")
                    values.append(updates["eval_criteria"])

                if "subjects_data" in updates:
                    update_fields.append("subjects_data = %s")
                    values.append(json.dumps(updates["subjects_data"]))

                values.append(doc_id)
                query = f"UPDATE coordination_documents SET {', '.join(update_fields)} WHERE id = %s RETURNING *"
                cur.execute(query, values)
                conn.commit()
                return cur.fetchone()

            return doc


@app.post("/coordination-documents/{doc_id}/chat", response_model=ChatResponse)
async def chat_with_document(doc_id: int, chat: ChatMessage):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM coordination_documents WHERE id = %s", (doc_id,))
            doc = cur.fetchone()
            if not doc:
                raise HTTPException(status_code=404, detail="Document not found")

            cur.execute("SELECT * FROM subjects WHERE area_id = %s", (doc["area_id"],))
            subjects = cur.fetchall()

            category_ids = doc.get("category_ids") or []
            categories = []
            if category_ids:
                cur.execute("SELECT * FROM categories WHERE id = ANY(%s)", (category_ids,))
                categories = cur.fetchall()

            # Convert history to list of dicts
            history = [{"role": item.role, "content": item.content} for item in chat.history]
            result = process_chat_message(doc, history, subjects, categories)

            # Apply updates if any
            if result["updates"]:
                update_fields = []
                values = []

                if "name" in result["updates"]:
                    update_fields.append("name = %s")
                    values.append(result["updates"]["name"])

                if "problem_edge" in result["updates"]:
                    update_fields.append("problem_edge = %s")
                    values.append(result["updates"]["problem_edge"])

                if "methodological_strategies" in result["updates"]:
                    update_fields.append("methodological_strategies = %s")
                    values.append(json.dumps(result["updates"]["methodological_strategies"]))

                if "eval_criteria" in result["updates"]:
                    update_fields.append("eval_criteria = %s")
                    values.append(result["updates"]["eval_criteria"])

                if "subjects_data" in result["updates"]:
                    update_fields.append("subjects_data = %s")
                    values.append(json.dumps(result["updates"]["subjects_data"]))

                if update_fields:
                    values.append(doc_id)
                    query = f"UPDATE coordination_documents SET {', '.join(update_fields)} WHERE id = %s RETURNING *"
                    cur.execute(query, values)
                    conn.commit()
                    updated_doc = cur.fetchone()
                    return {
                        "response": result["response"],
                        "document": updated_doc
                    }

            return {
                "response": result["response"],
                "document": doc
            }


@app.post("/coordination-documents", response_model=CoordinationDocumentResponse)
async def create_coordination_document(doc: CoordinationDocumentCreate):
    with get_db() as conn:
        with conn.cursor() as cur:
            # Validate that categories belong to selected nuclei
            if doc.category_ids and doc.nucleus_ids:
                cur.execute(
                    """
                    SELECT c.id FROM categories c
                    JOIN knowledge_areas ka ON c.knowledge_area_id = ka.id
                    WHERE c.id = ANY(%s) AND ka.nucleus_id = ANY(%s)
                    """,
                    (doc.category_ids, doc.nucleus_ids),
                )
                valid_category_ids = {row["id"] for row in cur.fetchall()}
                invalid_ids = set(doc.category_ids) - valid_category_ids
                if invalid_ids:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Categories {list(invalid_ids)} do not belong to the selected nuclei",
                    )

            cur.execute(
                """
                INSERT INTO coordination_documents
                (name, area_id, start_date, end_date, problem_edge, methodological_strategies, eval_criteria, subjects_data, nucleus_ids, category_ids)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    doc.name,
                    doc.area_id,
                    doc.start_date,
                    doc.end_date,
                    doc.problem_edge or '',
                    json.dumps(doc.methodological_strategies) if doc.methodological_strategies else None,
                    doc.eval_criteria or '',
                    json.dumps(doc.subjects_data) if doc.subjects_data else None,
                    doc.nucleus_ids,
                    doc.category_ids,
                ),
            )
            conn.commit()
            return cur.fetchone()


# ============= Catalog Endpoints =============

@app.get("/moment-types", response_model=List[MomentTypeResponse])
async def get_moment_types():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM moment_types ORDER BY id")
            return cur.fetchall()


@app.get("/activities", response_model=ActivitiesByMomentResponse)
async def get_activities():
    """Get all activities grouped by moment_type."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM activities ORDER BY id")
            all_activities = cur.fetchall()

            result = {
                "apertura": [],
                "desarrollo": [],
                "cierre": []
            }

            for activity in all_activities:
                moment_type = activity.get("moment_type")
                if moment_type in result:
                    result[moment_type].append(activity)

            return result


@app.post("/activities/recommend", response_model=ActivityRecommendationResponse)
async def recommend_activities(request: ActivityRecommendationRequest):
    """Use AI to recommend activities based on objective and categories."""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Get all activities grouped by moment
            cur.execute("SELECT id, name, description, moment_type FROM activities ORDER BY id")
            all_activities = cur.fetchall()

            activities_by_moment = {"apertura": [], "desarrollo": [], "cierre": []}
            for act in all_activities:
                moment_type = act.get("moment_type")
                if moment_type in activities_by_moment:
                    activities_by_moment[moment_type].append(act)

            # Get category names
            category_names = []
            if request.category_ids:
                placeholders = ','.join(['%s'] * len(request.category_ids))
                cur.execute(f"SELECT name FROM categories WHERE id IN ({placeholders})", tuple(request.category_ids))
                category_names = [row["name"] for row in cur.fetchall()]

            # Build prompt for AI
            apertura_opts = "\n".join([f"- ID {a['id']}: {a['name']} - {a['description']}" for a in activities_by_moment["apertura"]])
            desarrollo_opts = "\n".join([f"- ID {a['id']}: {a['name']} - {a['description']}" for a in activities_by_moment["desarrollo"]])
            cierre_opts = "\n".join([f"- ID {a['id']}: {a['name']} - {a['description']}" for a in activities_by_moment["cierre"]])

            prompt = f"""Eres un experto en planificación educativa. Basándote en el objetivo de la clase y las categorías a trabajar, recomienda las mejores actividades pedagógicas.

OBJETIVO DE LA CLASE:
{request.objective}

CATEGORÍAS/CONCEPTOS A TRABAJAR:
{', '.join(category_names) if category_names else 'No especificadas'}

ACTIVIDADES DISPONIBLES POR MOMENTO:

APERTURA (selecciona 1):
{apertura_opts}

DESARROLLO (selecciona hasta 3):
{desarrollo_opts}

CIERRE (selecciona 1):
{cierre_opts}

Responde SOLO con un JSON en este formato exacto:
{{"apertura_recommended_id": <id>, "desarrollo_recommended_ids": [<id1>, <id2>, <id3>], "cierre_recommended_id": <id>}}

Selecciona las actividades que mejor se adapten al objetivo y los conceptos a trabajar.
Para desarrollo, selecciona exactamente 3 actividades complementarias.
Solo responde con el JSON, sin explicaciones."""

            try:
                response = ai_client.chat.completions.create(
                    model=AZURE_OPENAI_DEPLOYMENT,
                    messages=[{"role": "user", "content": prompt}],
                    max_completion_tokens=500
                )
                content = response.choices[0].message.content.strip()

                # Parse JSON from response
                if content.startswith("```"):
                    content = content.split("```")[1]
                    if content.startswith("json"):
                        content = content[4:]
                    content = content.strip()

                recommendations = json.loads(content)

                # Validate the response has valid IDs
                apertura_ids = [a["id"] for a in activities_by_moment["apertura"]]
                desarrollo_ids = [a["id"] for a in activities_by_moment["desarrollo"]]
                cierre_ids = [a["id"] for a in activities_by_moment["cierre"]]

                apertura_id = recommendations.get("apertura_recommended_id")
                if apertura_id not in apertura_ids and activities_by_moment["apertura"]:
                    apertura_id = activities_by_moment["apertura"][0]["id"]

                desarrollo_rec_ids = recommendations.get("desarrollo_recommended_ids", [])
                desarrollo_rec_ids = [did for did in desarrollo_rec_ids if did in desarrollo_ids][:3]
                if not desarrollo_rec_ids and activities_by_moment["desarrollo"]:
                    desarrollo_rec_ids = [a["id"] for a in activities_by_moment["desarrollo"][:3]]

                cierre_id = recommendations.get("cierre_recommended_id")
                if cierre_id not in cierre_ids and activities_by_moment["cierre"]:
                    cierre_id = activities_by_moment["cierre"][0]["id"]

                return {
                    "apertura_recommended_id": apertura_id,
                    "desarrollo_recommended_ids": desarrollo_rec_ids,
                    "cierre_recommended_id": cierre_id
                }

            except Exception as e:
                print(f"[AI] Error recommending activities: {type(e).__name__}: {e}")
                # Fallback: return first activity of each type
                return {
                    "apertura_recommended_id": activities_by_moment["apertura"][0]["id"] if activities_by_moment["apertura"] else 1,
                    "desarrollo_recommended_ids": [a["id"] for a in activities_by_moment["desarrollo"][:3]] if activities_by_moment["desarrollo"] else [6, 7, 8],
                    "cierre_recommended_id": activities_by_moment["cierre"][0]["id"] if activities_by_moment["cierre"] else 13
                }


@app.get("/fonts", response_model=List[FontResponse])
async def get_fonts(area_id: Optional[int] = None):
    with get_db() as conn:
        with conn.cursor() as cur:
            if area_id:
                cur.execute(
                    "SELECT * FROM fonts WHERE (area_id = %s OR area_id IS NULL) AND is_validated = true ORDER BY name",
                    (area_id,)
                )
            else:
                cur.execute("SELECT * FROM fonts WHERE is_validated = true ORDER BY name")
            return cur.fetchall()


@app.get("/fonts/{font_id}", response_model=FontResponse)
async def get_font(font_id: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM fonts WHERE id = %s", (font_id,))
            font = cur.fetchone()
            if not font:
                raise HTTPException(status_code=404, detail="Font not found")
            return font


# ============= Teacher Lesson Plan Endpoints =============

@app.get("/teachers/{teacher_id}/lesson-plans", response_model=List[TeacherLessonPlanResponse])
async def get_teacher_lesson_plans(teacher_id: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT tlp.*,
                       c.name as course_name,
                       s.name as subject_name,
                       cd.name as document_name
                FROM teacher_lesson_plans tlp
                JOIN course_subjects cs ON tlp.course_subject_id = cs.id
                JOIN courses c ON cs.course_id = c.id
                JOIN subjects s ON cs.subject_id = s.id
                JOIN coordination_documents cd ON tlp.coordination_document_id = cd.id
                WHERE cs.teacher_id = %s
                ORDER BY tlp.course_subject_id, tlp.class_number
            """, (teacher_id,))
            return cur.fetchall()


@app.get("/course-subjects/{course_subject_id}/lesson-plans", response_model=List[TeacherLessonPlanResponse])
async def get_course_subject_lesson_plans(course_subject_id: int):
    """
    Get lesson plans for a course_subject, including plans from partner teachers
    for shared classes.
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            # Get shared class info for this course_subject
            shared_class_info = get_shared_class_info_for_course_subject(cur, course_subject_id)

            # Find all partner course_subject_ids for shared classes
            partner_cs_ids = set()
            for class_num in shared_class_info.keys():
                partner_id = find_partner_course_subject_id(cur, course_subject_id, shared_class_info, class_num)
                if partner_id:
                    partner_cs_ids.add(partner_id)

            # Query plans from both own and partner course_subjects
            all_cs_ids = [course_subject_id] + list(partner_cs_ids)

            cur.execute("""
                SELECT tlp.*,
                       tlp.course_subject_id as owner_course_subject_id,
                       u.name as created_by_teacher,
                       s.name as created_by_subject
                FROM teacher_lesson_plans tlp
                JOIN course_subjects cs ON tlp.course_subject_id = cs.id
                JOIN users u ON cs.teacher_id = u.id
                JOIN subjects s ON cs.subject_id = s.id
                WHERE tlp.course_subject_id = ANY(%s)
                ORDER BY tlp.class_number
            """, (all_cs_ids,))
            all_plans = cur.fetchall()

            # Filter: for shared classes, only return one plan (prioritize partner's if exists)
            result_plans = []
            seen_class_numbers = set()

            for plan in all_plans:
                class_num = plan['class_number']
                is_shared = class_num in shared_class_info
                is_own_plan = plan['owner_course_subject_id'] == course_subject_id

                # Include plan if:
                # 1. It's our own plan and we haven't seen this class number, OR
                # 2. It's a shared class from partner and we haven't seen this class number
                if class_num not in seen_class_numbers:
                    plan_dict = dict(plan)
                    plan_dict['is_shared_class'] = is_shared
                    plan_dict['shared_with_subject'] = shared_class_info.get(class_num)
                    plan_dict['is_own_plan'] = is_own_plan
                    result_plans.append(plan_dict)
                    seen_class_numbers.add(class_num)

            return result_plans


@app.get("/course-subjects/{course_subject_id}/coordination-status", response_model=CoordinationStatusResponse)
async def get_course_subject_coordination_status(course_subject_id: int):
    """Check if there's a published coordination document for this course-subject"""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Get the course_subject details
            cur.execute("""
                SELECT cs.*, s.area_id, s.name as subject_name, c.name as course_name
                FROM course_subjects cs
                JOIN subjects s ON cs.subject_id = s.id
                JOIN courses c ON cs.course_id = c.id
                WHERE cs.id = %s
            """, (course_subject_id,))
            cs = cur.fetchone()

            if not cs:
                raise HTTPException(status_code=404, detail="Course subject not found")

            # Find published coordination document for this area
            cur.execute("""
                SELECT cd.*, u.name as coordinator_name
                FROM coordination_documents cd
                JOIN areas a ON cd.area_id = a.id
                LEFT JOIN users u ON a.coordinator_id = u.id
                WHERE cd.area_id = %s
                  AND cd.status = 'published'
                ORDER BY cd.created_at DESC
                LIMIT 1
            """, (cs["area_id"],))
            doc = cur.fetchone()

            if doc:
                # Get class plan for this subject from the document
                subjects_data = doc.get("subjects_data") or {}
                subject_id = str(cs["subject_id"])
                class_plan = []
                if subject_id in subjects_data:
                    class_plan = subjects_data[subject_id].get("class_plan", [])

                # Get document-level category_ids (all categories available in the document)
                document_category_ids = doc.get("category_ids") or []
                document_nucleus_ids = doc.get("nucleus_ids") or []

                return {
                    "has_published_document": True,
                    "document_id": doc["id"],
                    "document_name": doc["name"],
                    "coordinator_name": doc.get("coordinator_name"),
                    "class_plan": class_plan,
                    "subject_category_ids": subjects_data.get(subject_id, {}).get("category_ids", []),
                    "category_ids": document_category_ids,  # All categories from the document
                    "nucleus_ids": document_nucleus_ids  # Nuclei from the document
                }

            return {
                "has_published_document": False,
                "document_id": None,
                "document_name": None,
                "coordinator_name": None,
                "class_plan": [],
                "subject_category_ids": [],
                "category_ids": [],
                "nucleus_ids": []
            }


@app.get("/course-subjects/{course_subject_id}/shared-class-numbers", response_model=SharedClassNumbersResponse)
async def get_shared_class_numbers(course_subject_id: int):
    """Get list of class numbers that fall on shared time slots"""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Get course_subject details
            cur.execute("""
                SELECT cs.*, s.name as subject_name, s.area_id, c.schedule
                FROM course_subjects cs
                JOIN subjects s ON cs.subject_id = s.id
                JOIN courses c ON cs.course_id = c.id
                WHERE cs.id = %s
            """, (course_subject_id,))
            cs = cur.fetchone()

            if not cs:
                raise HTTPException(status_code=404, detail="Course subject not found")

            # Get all subjects in the same area (for shared class detection)
            cur.execute("SELECT name FROM subjects WHERE area_id = %s", (cs["area_id"],))
            area_subjects = cur.fetchall()
            area_subject_names = [s["name"] for s in area_subjects]

            # Get the coordination document to find total classes for this subject
            cur.execute("""
                SELECT cd.subjects_data
                FROM coordination_documents cd
                WHERE cd.area_id = %s AND cd.status = 'published'
                ORDER BY cd.created_at DESC
                LIMIT 1
            """, (cs["area_id"],))
            doc = cur.fetchone()

            total_classes = 0
            if doc and doc.get("subjects_data"):
                subject_id = str(cs["subject_id"])
                if subject_id in doc["subjects_data"]:
                    class_plan = doc["subjects_data"][subject_id].get("class_plan", [])
                    total_classes = len(class_plan)

            if total_classes == 0:
                return {"shared_class_numbers": []}

            # Calculate which class numbers are shared and with which subject
            schedule = cs.get("schedule") or {}
            shared_info = calculate_shared_class_numbers(
                schedule,
                cs["subject_name"],
                area_subject_names,
                total_classes
            )

            return {
                "shared_class_numbers": list(shared_info.keys()),
                "shared_class_info": shared_info  # {class_number: shared_with_subject_name}
            }


@app.get("/teacher-lesson-plans/{plan_id}", response_model=TeacherLessonPlanDetailResponse)
async def get_teacher_lesson_plan(plan_id: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT tlp.*,
                       cs.course_id, cs.subject_id, cs.teacher_id,
                       c.name as course_name,
                       s.name as subject_name,
                       cd.name as document_name,
                       cd.subjects_data
                FROM teacher_lesson_plans tlp
                JOIN course_subjects cs ON tlp.course_subject_id = cs.id
                JOIN courses c ON cs.course_id = c.id
                JOIN subjects s ON cs.subject_id = s.id
                JOIN coordination_documents cd ON tlp.coordination_document_id = cd.id
                WHERE tlp.id = %s
            """, (plan_id,))
            plan = cur.fetchone()

            if not plan:
                raise HTTPException(status_code=404, detail="Lesson plan not found")

            # Get moment types and activities for the form
            cur.execute("SELECT * FROM moment_types ORDER BY id")
            moment_types = cur.fetchall()

            cur.execute("SELECT * FROM activities ORDER BY id")
            activities = cur.fetchall()

            # Get categories for the plan
            category_ids = plan.get("category_ids") or []
            categories = []
            if category_ids:
                cur.execute("SELECT * FROM categories WHERE id = ANY(%s)", (category_ids,))
                categories = cur.fetchall()

            return {
                **plan,
                "moment_types": moment_types,
                "activities": activities,
                "categories": categories
            }


@app.post("/teacher-lesson-plans", response_model=TeacherLessonPlanResponse)
async def create_teacher_lesson_plan(plan: TeacherLessonPlanCreate):
    with get_db() as conn:
        with conn.cursor() as cur:
            # Verify course_subject exists
            cur.execute("SELECT * FROM course_subjects WHERE id = %s", (plan.course_subject_id,))
            cs = cur.fetchone()
            if not cs:
                raise HTTPException(status_code=404, detail="Course subject not found")

            # Verify coordination document exists
            cur.execute("SELECT * FROM coordination_documents WHERE id = %s", (plan.coordination_document_id,))
            doc = cur.fetchone()
            if not doc:
                raise HTTPException(status_code=404, detail="Coordination document not found")

            # Validate activities per moment
            if plan.moments:
                apertura_activities = plan.moments.get("apertura", {}).get("activities", [])
                desarrollo_activities = plan.moments.get("desarrollo", {}).get("activities", [])
                cierre_activities = plan.moments.get("cierre", {}).get("activities", [])

                if len(apertura_activities) != 1:
                    raise HTTPException(
                        status_code=400,
                        detail="Apertura debe tener exactamente 1 actividad"
                    )
                if len(desarrollo_activities) < 1 or len(desarrollo_activities) > 3:
                    raise HTTPException(
                        status_code=400,
                        detail="Desarrollo debe tener entre 1 y 3 actividades"
                    )
                if len(cierre_activities) != 1:
                    raise HTTPException(
                        status_code=400,
                        detail="Cierre debe tener exactamente 1 actividad"
                    )

            # Check if this is a shared class and if partner already has a plan
            shared_class_info = get_shared_class_info_for_course_subject(cur, plan.course_subject_id)
            if plan.class_number in shared_class_info:
                partner_cs_id = find_partner_course_subject_id(
                    cur, plan.course_subject_id, shared_class_info, plan.class_number
                )
                if partner_cs_id:
                    # Check if partner already created a plan for this class
                    cur.execute("""
                        SELECT tlp.*, u.name as created_by_teacher, s.name as created_by_subject
                        FROM teacher_lesson_plans tlp
                        JOIN course_subjects cs ON tlp.course_subject_id = cs.id
                        JOIN users u ON cs.teacher_id = u.id
                        JOIN subjects s ON cs.subject_id = s.id
                        WHERE tlp.course_subject_id = %s
                          AND tlp.coordination_document_id = %s
                          AND tlp.class_number = %s
                    """, (partner_cs_id, plan.coordination_document_id, plan.class_number))
                    existing_partner_plan = cur.fetchone()

                    if existing_partner_plan:
                        # Return existing partner plan instead of creating duplicate
                        plan_dict = dict(existing_partner_plan)
                        plan_dict['is_shared_class'] = True
                        plan_dict['shared_with_subject'] = shared_class_info.get(plan.class_number)
                        plan_dict['is_own_plan'] = False
                        plan_dict['existing_shared_plan'] = True
                        return plan_dict

            cur.execute("""
                INSERT INTO teacher_lesson_plans
                (course_subject_id, coordination_document_id, class_number, title, category_ids,
                 objective, knowledge_content, didactic_strategies, class_format, moments, status,
                 custom_instruction, resources_mode, global_font_id, moment_font_ids)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending', %s, %s, %s, %s)
                ON CONFLICT (course_subject_id, coordination_document_id, class_number)
                DO UPDATE SET
                    title = EXCLUDED.title,
                    category_ids = EXCLUDED.category_ids,
                    objective = EXCLUDED.objective,
                    knowledge_content = EXCLUDED.knowledge_content,
                    didactic_strategies = EXCLUDED.didactic_strategies,
                    class_format = EXCLUDED.class_format,
                    moments = EXCLUDED.moments,
                    custom_instruction = EXCLUDED.custom_instruction,
                    resources_mode = EXCLUDED.resources_mode,
                    global_font_id = EXCLUDED.global_font_id,
                    moment_font_ids = EXCLUDED.moment_font_ids,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING *
            """, (
                plan.course_subject_id,
                plan.coordination_document_id,
                plan.class_number,
                plan.title,
                plan.category_ids,
                plan.objective,
                plan.knowledge_content,
                plan.didactic_strategies,
                plan.class_format,
                json.dumps(plan.moments) if plan.moments else None,
                plan.custom_instruction,
                plan.resources_mode,
                plan.global_font_id,
                json.dumps(plan.moment_font_ids) if plan.moment_font_ids else None
            ))
            conn.commit()
            return cur.fetchone()


class GenerateMomentRequest(BaseModel):
    moment_type: str  # apertura, desarrollo, cierre


# ============= Proposal Models =============

class ProposalResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    duration_weeks: int
    tools: list
    curriculum_card: dict
    alizia_info: dict
    initial_agreements: list
    stages: list
    is_active: bool
    status: str  # 'completed', 'recommended', 'upcoming'
    created_at: datetime

class ProposalProgressCreate(BaseModel):
    user_id: int
    proposal_id: int
    course_subject_id: int

class ProposalProgressResponse(BaseModel):
    id: int
    user_id: int
    proposal_id: int
    course_subject_id: int
    status: str
    agreements_data: dict
    stages_data: dict
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime

class AgreementUpdate(BaseModel):
    status: Optional[str] = None
    decision_value: Optional[str] = None
    conversation_history: Optional[list] = None

class DecisionUpdate(BaseModel):
    status: Optional[str] = None
    decision_value: Optional[str] = None
    conversation_history: Optional[list] = None

class ProposalChatMessage(BaseModel):
    history: List[ChatHistoryItem]

class ProposalChatResponse(BaseModel):
    response: str
    agreement_completed: bool = False
    decision_value: Optional[str] = None


@app.post("/teacher-lesson-plans/{plan_id}/generate-moment", response_model=GenerateMomentResponse)
async def generate_lesson_plan_moment(plan_id: int, request: GenerateMomentRequest):
    """Generate AI content for a specific moment of a lesson plan."""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Get the lesson plan with subject info
            cur.execute("""
                SELECT tlp.*, s.name as subject_name
                FROM teacher_lesson_plans tlp
                JOIN course_subjects cs ON tlp.course_subject_id = cs.id
                JOIN subjects s ON cs.subject_id = s.id
                WHERE tlp.id = %s
            """, (plan_id,))
            plan = cur.fetchone()

            if not plan:
                raise HTTPException(status_code=404, detail="Lesson plan not found")

            # Get all activities to map IDs to names
            cur.execute("SELECT * FROM activities")
            all_activities = {a["id"]: a["name"] for a in cur.fetchall()}

            # Get moment data
            moments = plan.get("moments") or {}
            moment_data = moments.get(request.moment_type, {})
            activity_ids = moment_data.get("activities", [])
            custom_text = moment_data.get("customText", "")

            # Get activity names
            activity_names = [all_activities.get(aid, f"Actividad {aid}") for aid in activity_ids]

            # Generate content using AI
            generated_content = generate_lesson_moment_content(
                moment_type=request.moment_type,
                subject_name=plan["subject_name"],
                class_title=plan.get("title") or "",
                objective=plan.get("objective") or "",
                activity_names=activity_names,
                custom_text=custom_text
            )

            # Update the moments with generated content
            moments[request.moment_type] = {
                **moment_data,
                "generatedContent": generated_content
            }

            # Save back to database
            cur.execute("""
                UPDATE teacher_lesson_plans
                SET moments = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING *
            """, (json.dumps(moments), plan_id))
            conn.commit()

            return {
                "moment_type": request.moment_type,
                "generated_content": generated_content,
                "plan": cur.fetchone()
            }


@app.patch("/teacher-lesson-plans/{plan_id}", response_model=TeacherLessonPlanResponse)
async def update_teacher_lesson_plan(plan_id: int, updates: TeacherLessonPlanUpdate):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM teacher_lesson_plans WHERE id = %s", (plan_id,))
            plan = cur.fetchone()
            if not plan:
                raise HTTPException(status_code=404, detail="Lesson plan not found")

            update_fields = ["updated_at = CURRENT_TIMESTAMP"]
            values = []

            if updates.title is not None:
                update_fields.append("title = %s")
                values.append(updates.title)

            if updates.category_ids is not None:
                update_fields.append("category_ids = %s")
                values.append(updates.category_ids)

            if updates.objective is not None:
                update_fields.append("objective = %s")
                values.append(updates.objective)

            if updates.knowledge_content is not None:
                update_fields.append("knowledge_content = %s")
                values.append(updates.knowledge_content)

            if updates.didactic_strategies is not None:
                update_fields.append("didactic_strategies = %s")
                values.append(updates.didactic_strategies)

            if updates.class_format is not None:
                update_fields.append("class_format = %s")
                values.append(updates.class_format)

            if updates.moments is not None:
                update_fields.append("moments = %s")
                values.append(json.dumps(updates.moments))

            if updates.status is not None:
                update_fields.append("status = %s")
                values.append(updates.status)

            if updates.custom_instruction is not None:
                update_fields.append("custom_instruction = %s")
                values.append(updates.custom_instruction)

            if updates.resources_mode is not None:
                update_fields.append("resources_mode = %s")
                values.append(updates.resources_mode)

            if updates.global_font_id is not None:
                update_fields.append("global_font_id = %s")
                values.append(updates.global_font_id)

            if updates.moment_font_ids is not None:
                update_fields.append("moment_font_ids = %s")
                values.append(json.dumps(updates.moment_font_ids))

            values.append(plan_id)
            query = f"UPDATE teacher_lesson_plans SET {', '.join(update_fields)} WHERE id = %s RETURNING *"
            cur.execute(query, values)
            conn.commit()
            return cur.fetchone()


@app.delete("/teacher-lesson-plans/{plan_id}", response_model=DeleteResponse)
async def delete_teacher_lesson_plan(plan_id: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM teacher_lesson_plans WHERE id = %s", (plan_id,))
            plan = cur.fetchone()
            if not plan:
                raise HTTPException(status_code=404, detail="Lesson plan not found")

            cur.execute("DELETE FROM teacher_lesson_plans WHERE id = %s", (plan_id,))
            conn.commit()
            return {"message": "Lesson plan deleted", "id": plan_id}


@app.post("/teacher-lesson-plans/{plan_id}/chat", response_model=TeacherChatResponse)
async def chat_with_teacher_lesson_plan(plan_id: int, chat: ChatMessage):
    with get_db() as conn:
        with conn.cursor() as cur:
            # Get plan with subject name
            cur.execute("""
                SELECT tlp.*, s.name as subject_name
                FROM teacher_lesson_plans tlp
                JOIN course_subjects cs ON tlp.course_subject_id = cs.id
                JOIN subjects s ON cs.subject_id = s.id
                WHERE tlp.id = %s
            """, (plan_id,))
            plan = cur.fetchone()
            if not plan:
                raise HTTPException(status_code=404, detail="Lesson plan not found")

            # Get all activities
            cur.execute("SELECT * FROM activities")
            activities = cur.fetchall()

            # Convert history to list of dicts
            history = [{"role": item.role, "content": item.content} for item in chat.history]
            result = process_teacher_lesson_chat(dict(plan), history, activities)

            # Apply updates if any
            if result["updates"]:
                update_fields = ["updated_at = CURRENT_TIMESTAMP"]
                values = []

                if "title" in result["updates"]:
                    update_fields.append("title = %s")
                    values.append(result["updates"]["title"])

                if "objective" in result["updates"]:
                    update_fields.append("objective = %s")
                    values.append(result["updates"]["objective"])

                if "moments" in result["updates"]:
                    update_fields.append("moments = %s")
                    values.append(json.dumps(result["updates"]["moments"]))

                if len(values) > 0:
                    values.append(plan_id)
                    query = f"UPDATE teacher_lesson_plans SET {', '.join(update_fields)} WHERE id = %s RETURNING *"
                    cur.execute(query, values)
                    conn.commit()
                    updated_plan = cur.fetchone()
                    return {
                        "response": result["response"],
                        "plan": updated_plan,
                        "changes_made": result["changes_made"]
                    }

            return {
                "response": result["response"],
                "plan": plan,
                "changes_made": []
            }


# ============= Proposal Endpoints =============

@app.get("/proposals", response_model=List[ProposalResponse])
async def get_proposals():
    """Get all active proposals."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM proposals WHERE is_active = true ORDER BY id")
            return cur.fetchall()


@app.get("/proposals/{proposal_id}", response_model=ProposalResponse)
async def get_proposal(proposal_id: int):
    """Get a proposal by ID with full details."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM proposals WHERE id = %s", (proposal_id,))
            proposal = cur.fetchone()
            if not proposal:
                raise HTTPException(status_code=404, detail="Proposal not found")
            return proposal


@app.get("/teachers/{teacher_id}/proposals", response_model=List[ProposalResponse])
async def get_teacher_proposals(teacher_id: int):
    """Get all proposals available for a teacher."""
    with get_db() as conn:
        with conn.cursor() as cur:
            # For now, return all active proposals
            # In the future, this could filter based on teacher's subjects/areas
            cur.execute("SELECT * FROM proposals WHERE is_active = true ORDER BY id")
            return cur.fetchall()


@app.post("/proposal-progress", response_model=ProposalProgressResponse)
async def create_proposal_progress(progress: ProposalProgressCreate):
    """Start a proposal for a teacher in a specific course-subject."""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Check if progress already exists
            cur.execute("""
                SELECT * FROM proposal_progress
                WHERE user_id = %s AND proposal_id = %s AND course_subject_id = %s
            """, (progress.user_id, progress.proposal_id, progress.course_subject_id))
            existing = cur.fetchone()
            if existing:
                return existing

            # Create new progress
            cur.execute("""
                INSERT INTO proposal_progress (user_id, proposal_id, course_subject_id, status, started_at)
                VALUES (%s, %s, %s, 'in_progress', CURRENT_TIMESTAMP)
                RETURNING *
            """, (progress.user_id, progress.proposal_id, progress.course_subject_id))
            conn.commit()
            return cur.fetchone()


@app.get("/proposal-progress/{user_id}/{proposal_id}/{course_subject_id}", response_model=ProposalProgressResponse)
async def get_proposal_progress(user_id: int, proposal_id: int, course_subject_id: int):
    """Get current progress for a proposal."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM proposal_progress
                WHERE user_id = %s AND proposal_id = %s AND course_subject_id = %s
            """, (user_id, proposal_id, course_subject_id))
            progress = cur.fetchone()
            if not progress:
                raise HTTPException(status_code=404, detail="Progress not found")
            return progress


@app.get("/proposal-progress/{progress_id}", response_model=ProposalProgressResponse)
async def get_proposal_progress_by_id(progress_id: int):
    """Get proposal progress by ID."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM proposal_progress WHERE id = %s", (progress_id,))
            progress = cur.fetchone()
            if not progress:
                raise HTTPException(status_code=404, detail="Progress not found")
            return progress


@app.patch("/proposal-progress/{progress_id}/agreements/{agreement_id}")
async def update_agreement(progress_id: int, agreement_id: str, update: AgreementUpdate):
    """Update an agreement's status and value."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM proposal_progress WHERE id = %s", (progress_id,))
            progress = cur.fetchone()
            if not progress:
                raise HTTPException(status_code=404, detail="Progress not found")

            agreements_data = progress.get("agreements_data") or {}
            if agreement_id not in agreements_data:
                agreements_data[agreement_id] = {}

            if update.status is not None:
                agreements_data[agreement_id]["status"] = update.status
            if update.decision_value is not None:
                agreements_data[agreement_id]["decision_value"] = update.decision_value
            if update.conversation_history is not None:
                agreements_data[agreement_id]["conversation_history"] = update.conversation_history

            # Check if all agreements are completed to potentially update overall status
            cur.execute("SELECT initial_agreements FROM proposals WHERE id = %s", (progress["proposal_id"],))
            proposal = cur.fetchone()
            total_agreements = len(proposal.get("initial_agreements", []))
            completed_agreements = sum(1 for a in agreements_data.values() if a.get("status") == "completed")

            new_status = progress["status"]
            if completed_agreements == total_agreements and total_agreements > 0:
                new_status = "agreements_completed"

            cur.execute("""
                UPDATE proposal_progress
                SET agreements_data = %s, status = %s
                WHERE id = %s
                RETURNING *
            """, (json.dumps(agreements_data), new_status, progress_id))
            conn.commit()
            return cur.fetchone()


@app.patch("/proposal-progress/{progress_id}/stages/{stage_number}/decisions/{decision_id}")
async def update_stage_decision(progress_id: int, stage_number: int, decision_id: str, update: DecisionUpdate):
    """Update a stage decision's status and value."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM proposal_progress WHERE id = %s", (progress_id,))
            progress = cur.fetchone()
            if not progress:
                raise HTTPException(status_code=404, detail="Progress not found")

            stages_data = progress.get("stages_data") or {}
            stage_key = str(stage_number)
            if stage_key not in stages_data:
                stages_data[stage_key] = {}
            if decision_id not in stages_data[stage_key]:
                stages_data[stage_key][decision_id] = {}

            if update.status is not None:
                stages_data[stage_key][decision_id]["status"] = update.status
            if update.decision_value is not None:
                stages_data[stage_key][decision_id]["decision_value"] = update.decision_value
            if update.conversation_history is not None:
                stages_data[stage_key][decision_id]["conversation_history"] = update.conversation_history

            cur.execute("""
                UPDATE proposal_progress
                SET stages_data = %s
                WHERE id = %s
                RETURNING *
            """, (json.dumps(stages_data), progress_id))
            conn.commit()
            return cur.fetchone()


@app.post("/proposal-progress/{progress_id}/agreements/{agreement_id}/chat", response_model=ProposalChatResponse)
async def chat_with_agreement(progress_id: int, agreement_id: str, chat: ProposalChatMessage):
    """Chat with Alizia about a specific agreement."""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Get progress
            cur.execute("SELECT * FROM proposal_progress WHERE id = %s", (progress_id,))
            progress = cur.fetchone()
            if not progress:
                raise HTTPException(status_code=404, detail="Progress not found")

            # Get proposal
            cur.execute("SELECT * FROM proposals WHERE id = %s", (progress["proposal_id"],))
            proposal = cur.fetchone()
            if not proposal:
                raise HTTPException(status_code=404, detail="Proposal not found")

            # Get teacher name
            teacher_name = None
            if progress.get("user_id"):
                cur.execute("SELECT name FROM users WHERE id = %s", (progress["user_id"],))
                user = cur.fetchone()
                if user:
                    teacher_name = user["name"]

            # Get subject name from course_subject
            subject_name = None
            if progress.get("course_subject_id"):
                cur.execute("""
                    SELECT s.name FROM subjects s
                    JOIN course_subjects cs ON cs.subject_id = s.id
                    WHERE cs.id = %s
                """, (progress["course_subject_id"],))
                subject = cur.fetchone()
                if subject:
                    subject_name = subject["name"]

            # Find the agreement
            initial_agreements = proposal.get("initial_agreements", [])
            agreement = next((a for a in initial_agreements if a["id"] == agreement_id), None)
            if not agreement:
                raise HTTPException(status_code=404, detail="Agreement not found")

            # Get existing value if any
            agreements_data = progress.get("agreements_data") or {}
            existing_value = agreements_data.get(agreement_id, {}).get("decision_value")

            # Get alizia_context if available
            alizia_context = agreement.get("alizia_context")

            # Process chat
            history = [{"role": item.role, "content": item.content} for item in chat.history]
            result = process_proposal_chat(
                agreement_title=agreement["title"],
                agreement_description=agreement["description"],
                responsible_type=agreement["responsible_type"],
                proposal_name=proposal["name"],
                history=history,
                existing_value=existing_value,
                alizia_context=alizia_context,
                teacher_name=teacher_name,
                subject_name=subject_name
            )

            # Update progress if value or completion changed
            if result["decision_value"] or result["agreement_completed"]:
                if agreement_id not in agreements_data:
                    agreements_data[agreement_id] = {}

                if result["decision_value"]:
                    agreements_data[agreement_id]["decision_value"] = result["decision_value"]

                if result["agreement_completed"]:
                    agreements_data[agreement_id]["status"] = "completed"

                # Save conversation history
                agreements_data[agreement_id]["conversation_history"] = history + [
                    {"role": "assistant", "content": result["response"]}
                ]

                # Check if all agreements completed
                total_agreements = len(initial_agreements)
                completed_agreements = sum(1 for a in agreements_data.values() if a.get("status") == "completed")
                new_status = "agreements_completed" if completed_agreements == total_agreements else progress["status"]

                cur.execute("""
                    UPDATE proposal_progress
                    SET agreements_data = %s, status = %s
                    WHERE id = %s
                """, (json.dumps(agreements_data), new_status, progress_id))
                conn.commit()

            return result


@app.post("/proposal-progress/{progress_id}/stages/{stage_number}/decisions/{decision_id}/chat", response_model=ProposalChatResponse)
async def chat_with_stage_decision(progress_id: int, stage_number: int, decision_id: str, chat: ProposalChatMessage):
    """Chat with Alizia about a specific stage decision."""
    with get_db() as conn:
        with conn.cursor() as cur:
            # Get progress
            cur.execute("SELECT * FROM proposal_progress WHERE id = %s", (progress_id,))
            progress = cur.fetchone()
            if not progress:
                raise HTTPException(status_code=404, detail="Progress not found")

            # Get proposal
            cur.execute("SELECT * FROM proposals WHERE id = %s", (progress["proposal_id"],))
            proposal = cur.fetchone()
            if not proposal:
                raise HTTPException(status_code=404, detail="Proposal not found")

            # Get teacher name
            teacher_name = None
            if progress.get("user_id"):
                cur.execute("SELECT name FROM users WHERE id = %s", (progress["user_id"],))
                user = cur.fetchone()
                if user:
                    teacher_name = user["name"]

            # Get subject name from course_subject
            subject_name = None
            if progress.get("course_subject_id"):
                cur.execute("""
                    SELECT s.name FROM subjects s
                    JOIN course_subjects cs ON cs.subject_id = s.id
                    WHERE cs.id = %s
                """, (progress["course_subject_id"],))
                subject = cur.fetchone()
                if subject:
                    subject_name = subject["name"]

            # Find the stage and decision
            stages = proposal.get("stages", [])
            stage = next((s for s in stages if s["number"] == stage_number), None)
            if not stage:
                raise HTTPException(status_code=404, detail="Stage not found")

            decision = next((d for d in stage.get("decisions", []) if d["id"] == decision_id), None)
            if not decision:
                raise HTTPException(status_code=404, detail="Decision not found")

            # Get existing value if any
            stages_data = progress.get("stages_data") or {}
            stage_key = str(stage_number)
            existing_value = stages_data.get(stage_key, {}).get(decision_id, {}).get("decision_value")

            # Get alizia_context if available
            alizia_context = decision.get("alizia_context")

            # Process chat
            history = [{"role": item.role, "content": item.content} for item in chat.history]
            result = process_proposal_chat(
                agreement_title=decision["title"],
                agreement_description=decision["description"],
                responsible_type=decision["responsible_type"],
                proposal_name=proposal["name"],
                history=history,
                existing_value=existing_value,
                alizia_context=alizia_context,
                teacher_name=teacher_name,
                subject_name=subject_name
            )

            # Update progress if value or completion changed
            if result["decision_value"] or result["agreement_completed"]:
                if stage_key not in stages_data:
                    stages_data[stage_key] = {}
                if decision_id not in stages_data[stage_key]:
                    stages_data[stage_key][decision_id] = {}

                if result["decision_value"]:
                    stages_data[stage_key][decision_id]["decision_value"] = result["decision_value"]

                if result["agreement_completed"]:
                    stages_data[stage_key][decision_id]["status"] = "completed"

                # Save conversation history
                stages_data[stage_key][decision_id]["conversation_history"] = history + [
                    {"role": "assistant", "content": result["response"]}
                ]

                cur.execute("""
                    UPDATE proposal_progress
                    SET stages_data = %s
                    WHERE id = %s
                """, (json.dumps(stages_data), progress_id))
                conn.commit()

            return result


# Resources Endpoints
@app.get("/resources", response_model=List[ResourceResponse])
async def get_resources(user_id: Optional[int] = None):
    """List all resources, optionally filtered by user_id."""
    with get_db() as conn:
        with conn.cursor() as cur:
            if user_id:
                cur.execute("SELECT * FROM resources WHERE user_id = %s ORDER BY updated_at DESC", (user_id,))
            else:
                cur.execute("SELECT * FROM resources ORDER BY updated_at DESC")
            return cur.fetchall()


@app.post("/resources", response_model=ResourceResponse)
async def create_resource(resource: ResourceCreate):
    """Create a new resource with template content."""
    if resource.resource_type not in RESOURCE_TEMPLATES:
        raise HTTPException(status_code=400, detail=f"Invalid resource_type. Must be one of: {list(RESOURCE_TEMPLATES.keys())}")

    content = RESOURCE_TEMPLATES[resource.resource_type]

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO resources (title, resource_type, content, user_id, status)
                VALUES (%s, %s, %s, %s, 'draft')
                RETURNING *
            """, (resource.title, resource.resource_type, content, resource.user_id))
            conn.commit()
            return cur.fetchone()


@app.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int):
    """Get a specific resource by ID."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM resources WHERE id = %s", (resource_id,))
            resource = cur.fetchone()
            if not resource:
                raise HTTPException(status_code=404, detail="Resource not found")
            return resource


@app.patch("/resources/{resource_id}", response_model=ResourceResponse)
async def update_resource(resource_id: int, update: ResourceUpdate):
    """Update a resource's title or content."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM resources WHERE id = %s", (resource_id,))
            resource = cur.fetchone()
            if not resource:
                raise HTTPException(status_code=404, detail="Resource not found")

            updates = []
            values = []
            if update.title is not None:
                updates.append("title = %s")
                values.append(update.title)
            if update.content is not None:
                updates.append("content = %s")
                values.append(update.content)

            if updates:
                updates.append("updated_at = CURRENT_TIMESTAMP")
                values.append(resource_id)
                cur.execute(f"""
                    UPDATE resources SET {', '.join(updates)}
                    WHERE id = %s RETURNING *
                """, values)
                conn.commit()
                return cur.fetchone()
            return resource


@app.delete("/resources/{resource_id}", response_model=DeleteResponse)
async def delete_resource(resource_id: int):
    """Delete a resource."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM resources WHERE id = %s", (resource_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Resource not found")

            cur.execute("DELETE FROM resources WHERE id = %s", (resource_id,))
            conn.commit()
            return {"message": "Resource deleted successfully", "id": resource_id}


# ==================== INCLUSION MODULE ====================

class RampResponse(BaseModel):
    id: int
    name: str
    description: str
    short_description: Optional[str] = None
    sort_order: int = 0

class DeviceResponse(BaseModel):
    id: int
    ramp_id: int
    name: str
    description: str
    image_url: Optional[str] = None
    qr_code: Optional[str] = None
    how_to_use: Optional[str] = None
    recommendations: Optional[str] = None
    rationale: Optional[str] = None
    classroom_benefit: Optional[str] = None
    needs_description: Optional[str] = None
    evaluation_criteria: Optional[str] = None
    quantity: int = 1
    sort_order: int = 0
    ramp_name: Optional[str] = None

class StudentInclusionProfileResponse(BaseModel):
    id: int
    student_id: int
    student_name: Optional[str] = None
    is_transitory: bool = False
    difficulties: List[str] = []
    free_description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class StudentInclusionProfileCreate(BaseModel):
    is_transitory: bool = False
    difficulties: List[str] = []
    free_description: Optional[str] = None

class InclusionRecommendRequest(BaseModel):
    subject: str
    objective: str
    duration: Optional[str] = None
    dynamic: Optional[str] = None
    materials: Optional[str] = None
    student_id: int
    history: List[ChatHistoryItem] = []

class InclusionAssistRequest(BaseModel):
    message: str
    student_id: Optional[int] = None
    history: List[ChatHistoryItem] = []


@app.get("/ramps")
async def list_ramps():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM ramps ORDER BY sort_order")
            return cur.fetchall()


@app.get("/ramps/{ramp_id}")
async def get_ramp(ramp_id: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM ramps WHERE id = %s", (ramp_id,))
            ramp = cur.fetchone()
            if not ramp:
                raise HTTPException(status_code=404, detail="Ramp not found")
            cur.execute("SELECT d.*, r.name as ramp_name FROM devices d JOIN ramps r ON d.ramp_id = r.id WHERE d.ramp_id = %s ORDER BY d.sort_order", (ramp_id,))
            devices = cur.fetchall()
            return {**ramp, "devices": devices}


@app.get("/devices")
async def list_devices(ramp_id: Optional[int] = None):
    with get_db() as conn:
        with conn.cursor() as cur:
            if ramp_id:
                cur.execute("SELECT d.*, r.name as ramp_name FROM devices d JOIN ramps r ON d.ramp_id = r.id WHERE d.ramp_id = %s ORDER BY d.sort_order", (ramp_id,))
            else:
                cur.execute("SELECT d.*, r.name as ramp_name FROM devices d JOIN ramps r ON d.ramp_id = r.id ORDER BY d.ramp_id, d.sort_order")
            return cur.fetchall()


@app.get("/devices/{device_id}")
async def get_device(device_id: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT d.*, r.name as ramp_name FROM devices d JOIN ramps r ON d.ramp_id = r.id WHERE d.id = %s", (device_id,))
            device = cur.fetchone()
            if not device:
                raise HTTPException(status_code=404, detail="Device not found")
            return device


@app.get("/students/{student_id}/inclusion-profile")
async def get_student_inclusion_profile(student_id: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT sip.*, s.name as student_name
                FROM student_inclusion_profiles sip
                JOIN students s ON sip.student_id = s.id
                WHERE sip.student_id = %s
            """, (student_id,))
            profile = cur.fetchone()
            if not profile:
                raise HTTPException(status_code=404, detail="Inclusion profile not found")
            return profile


@app.post("/students/{student_id}/inclusion-profile")
async def create_or_update_inclusion_profile(student_id: int, data: StudentInclusionProfileCreate):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM students WHERE id = %s", (student_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Student not found")

            cur.execute("SELECT id FROM student_inclusion_profiles WHERE student_id = %s", (student_id,))
            existing = cur.fetchone()

            if existing:
                cur.execute("""
                    UPDATE student_inclusion_profiles
                    SET is_transitory = %s, difficulties = %s, free_description = %s, updated_at = NOW()
                    WHERE student_id = %s
                    RETURNING *
                """, (data.is_transitory, data.difficulties, data.free_description, student_id))
            else:
                cur.execute("""
                    INSERT INTO student_inclusion_profiles (student_id, is_transitory, difficulties, free_description)
                    VALUES (%s, %s, %s, %s)
                    RETURNING *
                """, (student_id, data.is_transitory, data.difficulties, data.free_description))

            conn.commit()
            profile = cur.fetchone()
            cur.execute("SELECT name FROM students WHERE id = %s", (student_id,))
            student = cur.fetchone()
            return {**profile, "student_name": student["name"] if student else None}


@app.get("/courses/{course_id}/inclusion-students")
async def get_course_inclusion_students(course_id: int):
    """Get all students in a course with their inclusion profiles (if any)."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT s.id, s.name, s.course_id,
                       sip.id as profile_id, sip.is_transitory, sip.difficulties,
                       sip.free_description
                FROM students s
                LEFT JOIN student_inclusion_profiles sip ON s.id = sip.student_id
                WHERE s.course_id = %s
                ORDER BY sip.id IS NOT NULL DESC, s.name
            """, (course_id,))
            return cur.fetchall()


INCLUSION_SYSTEM_PROMPT = """Sos Alicia, asistente de inclusion educativa de Educabot.
Tu rol es ayudar a docentes a integrar dispositivos adaptativos de la Valija de Inclusion en sus clases.

CATALOGO DE DISPOSITIVOS:
{devices_catalog}

INSTRUCCIONES:
- Responde en espanol rioplatense, tono amable y profesional.
- Usa lenguaje docente, NO patologizante.
- Cuando recomiendes un dispositivo, siempre explica POR QUE sirve para esa actividad y esa necesidad especifica.
- Si no tenes suficiente informacion, pregunta de forma conversacional.
- Mantene las respuestas concisas y practicas (el docente esta en el aula).
- IMPORTANTE: Cuando recomiendes un dispositivo, incluye al final de tu respuesta una linea con el formato exacto:
  [DEVICE_ID:X] donde X es el id numerico del dispositivo recomendado.
  Esto es para que el sistema pueda mostrar la ficha del dispositivo. Solo incluye un dispositivo principal.
- Estructura tu respuesta de recomendacion asi:
  1. Breve explicacion de por que ese dispositivo es adecuado
  2. Bullets con beneficios especificos para la situacion
  3. Como usarlo en la actividad especifica
  4. Tips de integracion con el grupo
"""


@app.post("/inclusion/recommend")
async def inclusion_recommend(data: InclusionRecommendRequest):
    with get_db() as conn:
        with conn.cursor() as cur:
            # Fetch student profile
            cur.execute("""
                SELECT sip.*, s.name as student_name
                FROM student_inclusion_profiles sip
                JOIN students s ON sip.student_id = s.id
                WHERE sip.student_id = %s
            """, (data.student_id,))
            profile = cur.fetchone()
            if not profile:
                raise HTTPException(status_code=404, detail="Student inclusion profile not found")

            # Fetch all devices with ramp names
            cur.execute("SELECT d.*, r.name as ramp_name FROM devices d JOIN ramps r ON d.ramp_id = r.id ORDER BY d.ramp_id, d.sort_order")
            devices = cur.fetchall()

            # Build catalog JSON
            devices_catalog = json.dumps([{
                "id": d["id"],
                "name": d["name"],
                "ramp": d["ramp_name"],
                "description": d["description"],
                "how_to_use": d["how_to_use"],
                "rationale": d["rationale"],
                "classroom_benefit": d["classroom_benefit"],
                "needs_description": d["needs_description"],
                "quantity": d["quantity"]
            } for d in devices], ensure_ascii=False)

            system_prompt = INCLUSION_SYSTEM_PROMPT.format(devices_catalog=devices_catalog)

            # Add student context
            difficulties_text = ", ".join(profile["difficulties"]) if profile["difficulties"] else "Sin especificar"
            student_context = f"""
FICHA DEL ALUMNO:
- Nombre: {profile['student_name']}
- Condicion: {'Transitoria' if profile['is_transitory'] else 'Permanente'}
- Dificultades: {difficulties_text}
- Descripcion: {profile['free_description'] or 'Sin descripcion adicional'}

ACTIVIDAD PLANIFICADA:
- Asignatura: {data.subject}
- Objetivo: {data.objective}
- Duracion: {data.duration or 'No especificada'}
- Dinamica: {data.dynamic or 'No especificada'}
- Materiales: {data.materials or 'No especificados'}
"""
            system_prompt += student_context

            # For follow-up messages, add instruction to keep it conversational
            if data.history:
                system_prompt += """
Si ya recomendaste un dispositivo en mensajes anteriores, NO lo repitas completo.
Responde de forma conversacional y breve a las preguntas del docente.
No incluyas [DEVICE_ID:X] en respuestas de seguimiento a menos que estes recomendando un dispositivo DIFERENTE.
"""

            # Build messages
            messages = [{"role": "system", "content": system_prompt}]
            for msg in data.history:
                messages.append({"role": msg.role, "content": msg.content})

            # Add the recommendation request as user message if no history
            if not data.history:
                messages.append({"role": "user", "content": f"Necesito una recomendacion de dispositivo para {profile['student_name']} en la actividad de {data.objective} en {data.subject}."})

            try:
                response = ai_client.chat.completions.create(
                    model=AZURE_OPENAI_DEPLOYMENT,
                    messages=messages,
                    max_completion_tokens=1500,
                )
                ai_response = response.choices[0].message.content

                # Extract device ID from response
                import re
                device_id_match = re.search(r'\[DEVICE_ID:(\d+)\]', ai_response)
                recommended_device = None
                if device_id_match:
                    device_id = int(device_id_match.group(1))
                    recommended_device = next((d for d in devices if d["id"] == device_id), None)
                    # Clean the tag from the response
                    clean_response = re.sub(r'\[DEVICE_ID:\d+\]', '', ai_response).strip()
                else:
                    clean_response = ai_response

                return {
                    "response": clean_response,
                    "device": dict(recommended_device) if recommended_device else None,
                    "student_profile": dict(profile),
                }
            except Exception as e:
                logger.error(f"AI recommendation error: {e}")
                raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")


ASSIST_SYSTEM_PROMPT = """Eres Alizia, una asistente amable y efectiva de inclusion educativa en tiempo real para el aula.
Un docente te esta consultando desde el aula para que le ayudes.

CATALOGO DE DISPOSITIVOS DISPONIBLES:
{devices_catalog}

ALUMNOS DEL CURSO (con perfiles de inclusion):
{students_context}

INSTRUCCIONES:
- Responde en espanol rioplatense, tono amable, calmo y profesional.
- Usa lenguaje docente, NO patologizante.
- Mantene las respuestas BREVES y ACCIONABLES (el docente esta en el aula ahora mismo).

IDENTIFICACION DE ALUMNOS:
- Se flexible con los nombres: apodos, diminutivos, nombres parciales o informales deben matchear con el alumno mas probable.
  Ejemplos: "Valen" = "Valentina Garcia", "Facu" = "Facundo ...", "Nico" = "Nicolas ...", "Cami" = "Camila ...", etc.
- Si el nombre es razonablemente claro (aunque sea parcial o informal), identifica al alumno directamente sin preguntar confirmacion.
  Incluye al final: [STUDENT_ID:X] donde X es el id del alumno identificado.
- Solo pregunta "¿A que alumno te referis?" si realmente hay ambiguedad (ej: dos alumnos podrian matchear) o si no menciona ningun nombre.
- Si el docente habla de una situacion sin mencionar a nadie, primero da consejos generales y pregunta: "¿Quien esta pasando por esto?"

RECOMENDACION DE DISPOSITIVOS:
- NUNCA recomiendes un dispositivo hasta que el alumno este identificado (es decir, hasta que hayas incluido [STUDENT_ID:X]).
- Si todavia no sabes quien es el alumno, da consejos pedagogicos generales pero NO recomiendes dispositivo.
- Una vez identificado el alumno, recomienda un dispositivo adecuado a sus dificultades especificas e incluye: [DEVICE_ID:X].

FORMATO DE RESPUESTA (cuando el alumno esta identificado):
  1. Reconoce la situacion brevemente
  2. Da 2-3 sugerencias practicas e inmediatas
  3. Recomienda un dispositivo con breve explicacion

FORMATO DE RESPUESTA (cuando el alumno NO esta identificado):
  1. Reconoce la situacion brevemente
  2. Da 2-3 sugerencias practicas generales
  3. Pregunta quien es el alumno

"""


@app.post("/inclusion/assist")
async def inclusion_assist(data: InclusionAssistRequest):
    with get_db() as conn:
        with conn.cursor() as cur:
            # Fetch all devices
            cur.execute("SELECT d.*, r.name as ramp_name FROM devices d JOIN ramps r ON d.ramp_id = r.id ORDER BY d.ramp_id, d.sort_order")
            devices = cur.fetchall()

            devices_catalog = json.dumps([{
                "id": d["id"], "name": d["name"], "ramp": d["ramp_name"],
                "needs_description": d["needs_description"],
            } for d in devices], ensure_ascii=False)

            # Fetch students with profiles (course 1 for demo)
            cur.execute("""
                SELECT s.id, s.name, sip.is_transitory, sip.difficulties, sip.free_description
                FROM students s
                LEFT JOIN student_inclusion_profiles sip ON s.id = sip.student_id
                WHERE s.course_id = 1
                ORDER BY s.name
            """)
            students = cur.fetchall()

            students_context = json.dumps([{
                "id": s["id"], "name": s["name"],
                "difficulties": s["difficulties"] or [],
            } for s in students], ensure_ascii=False)

            system_prompt = ASSIST_SYSTEM_PROMPT.format(
                devices_catalog=devices_catalog,
                students_context=students_context
            )

            if data.history:
                system_prompt += "\nYa hay conversacion previa. Responde de forma conversacional y breve. No repitas recomendaciones previas."

            messages = [{"role": "system", "content": system_prompt}]
            # Keep only last 10 messages to avoid token overflow
            recent_history = data.history[-10:] if len(data.history) > 10 else data.history
            for msg in recent_history:
                messages.append({"role": msg.role, "content": msg.content})
            messages.append({"role": "user", "content": data.message})

            try:
                ai_response = ""
                for attempt in range(3):
                    response = ai_client.chat.completions.create(
                        model=AZURE_OPENAI_DEPLOYMENT,
                        messages=messages,
                        max_completion_tokens=2000,
                    )
                    choice = response.choices[0]
                    ai_response = choice.message.content or ""
                    finish_reason = choice.finish_reason
                    # Log full debug info
                    print(f"AI assist attempt {attempt+1}: finish_reason={finish_reason}, len={len(ai_response)}")
                    print(f"AI assist response preview: {repr(ai_response[:200])}")
                    print(f"AI assist full choice model_dump: {choice.model_dump()}")
                    if ai_response.strip():
                        break
                    logger.warning(f"AI assist empty response (attempt {attempt+1}/3), retrying...")

                if not ai_response.strip():
                    return {
                        "response": "No pude generar una respuesta. ¿Podes repetir la consulta?",
                        "identified_student": None,
                        "device": None,
                    }

                # Extract student ID
                student_id_match = re.search(r'\[STUDENT_ID:(\d+)\]', ai_response)
                identified_student = None
                if student_id_match:
                    sid = int(student_id_match.group(1))
                    identified_student = next((s for s in students if s["id"] == sid), None)
                    if identified_student:
                        identified_student = dict(identified_student)

                # Extract device ID
                device_id_match = re.search(r'\[DEVICE_ID:(\d+)\]', ai_response)
                recommended_device = None
                if device_id_match:
                    did = int(device_id_match.group(1))
                    recommended_device = next((d for d in devices if d["id"] == did), None)
                    if recommended_device:
                        recommended_device = dict(recommended_device)

                # Clean tags from response
                clean_response = re.sub(r'\[STUDENT_ID:\d+\]', '', ai_response)
                clean_response = re.sub(r'\[DEVICE_ID:\d+\]', '', clean_response).strip()

                return {
                    "response": clean_response,
                    "identified_student": identified_student,
                    "device": recommended_device,
                }
            except Exception as e:
                logger.error(f"AI assist error: {e}")
                raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")
