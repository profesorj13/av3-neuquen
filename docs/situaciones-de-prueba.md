# Situaciones de prueba — Asistente de Inclusión

> Catálogo de casos para ejercitar el modo `/inclusion/asistencia` end-to-end.
> Cada caso describe **input del docente**, **estado del curso** y **respuesta esperada** (alumno identificado, dispositivo, adaptación pedagógica, tono).
> Sirve como **suite de regresión** (parseable por el harness en `tests/test_assistant_situations.py`) y como **referencia humana** para alinear el equipo sobre qué se considera una buena respuesta.

---

## Convenciones

- **course_id:** salvo aclaración, siempre `1`.
- **Alumnos con perfil cargado en seed:**
  - `id=1` Lucía Fernández — *motricidad fina (manos y brazos)*
  - `id=2` Mateo López — *acceso a tecnología digital*
  - `id=3` Valentina García — *atención sostenida y regulación emocional*
- **Alumnos sin perfil cargado:** los 22 restantes del curso 1 (Santiago, Camila, Benjamín, Sofía, Tomás, Emma, Nicolás, Isabella, Lautaro, Martina, Joaquín, Emilia, Thiago, Olivia, Felipe, Renata, Bautista, Catalina, Juan Cruz, Delfina, Agustín, Alma).
- **Notación:**
  - `T1👤` / `T2👤` … turno N del docente.
  - `T1🤖` / `T2🤖` … turno N esperado de Alizia.
  - **🛠 Tool calls esperadas:** lista ordenada de tools que Alizia debe invocar en ese turno.
  - **✅ En el texto:** elementos que SÍ deben aparecer en la respuesta textual.
  - **❌ En el texto:** elementos que NO deben aparecer (jerga clínica, supuestos, repreguntas innecesarias).

---

## Bloque 1 — Motricidad fina y escritura

### Caso 01 — Apodo + manifestación clara, alumna con perfil
**tags:** `motricidad-fina` `escritura` `identificacion-flexible` `match-exacto`

**T1👤** "A Lu se le cae el lápiz y se cansa rapidísimo cuando hago dictado, no llega a copiar nada"

**T1🤖 esperado:**
- 🛠 `identify_student("Lu")` → Lucía Fernández (id=1)
- 🛠 `propose_device(device=Soporte para lápiz etapa 4, student=1, manifestation="se le cae el lápiz, se cansa al escribir", activity="dictado", rationale="acompaña la prensión sin cambiar la actividad ni separarla del grupo")`
- ✅ Reconoce a Lucía por nombre
- ✅ Menciona el soporte para lápiz como primera opción (etapa 4 = más simple, ver DUA "mínima intervención")
- ✅ Agrega 1 tip de uso (cómo colocar el soporte) o 1 alternativa breve (pesas para lápices) si soporte no funciona
- ❌ No menciona "disgrafía", "TDAH", "diagnóstico"
- ❌ No pide info adicional antes de actuar

---

### Caso 02 — Manifestación de motricidad sin alumno mencionado
**tags:** `motricidad-fina` `general-a-especifico` `sin-alumno-inicial`

**T1👤** "Tengo varios chicos a los que se les cae el lápiz y se les nota que les cuesta apretar"

**T1🤖 esperado:**
- 🛠 (ninguna)
- ✅ Reconoce el patrón (motricidad fina) sin patologizar
- ✅ Sugiere 2 productos generales (Soporte para lápiz etapas 3-4, Pesas para lápices) — sin tool todavía
- ✅ Pregunta cuáles son los alumnos puntuales para individualizar
- ❌ No emite `propose_device` (todavía no hay alumno)

**T2👤** "Sobre todo Lu y también Tomás Romero"

**T2🤖 esperado:**
- 🛠 `identify_student("Lu")` → Lucía
- 🛠 `identify_student("Tomás Romero")` → Tomás (id=8, sin perfil cargado)
- 🛠 `propose_device(Soporte lápiz etapa 4, student=Lucía, ...)`
- ✅ Menciona ambos alumnos
- ✅ Para Lucía recomienda dispositivo + tip
- ✅ Para Tomás: aclara que no tiene perfil cargado, ofrece relevarlo o seguir con la misma sugerencia + invita a observar

---

### Caso 03 — Recorte y tijera
**tags:** `motricidad` `recorte` `tijera`

**T1👤** "En plástica el chico de Camila no logra cortar nada con la tijera"

**T1🤖 esperado:**
- 🛠 `identify_student("Camila")` → matches: Camila Rodríguez (id=5)
  - *Nota:* el docente dice "el chico de Camila", lo cual es ambiguo. Alizia debe interpretar que se refiere a Camila como alumna.
- 🛠 `propose_device(Tijera adaptada etapa 1, student=5, manifestation="no logra cortar con tijera", activity="plástica/recorte")`
- ✅ Reconoce que Camila no tiene perfil cargado (no asume diagnóstico)
- ✅ Recomienda la Tijera adaptada etapa 1 + por qué
- ✅ Sugiere registrar lo observado en el perfil de Camila para futuras clases

---

## Bloque 2 — Lectura

### Caso 04 — "Salta líneas" / dislexia sin nombrar
**tags:** `lectura` `seguimiento-visual` `etapas-progresivas`

**T1👤** "En 4to estoy haciendo comprensión lectora y a Martina le cuesta seguir el texto, salta líneas"

**T1🤖 esperado:**
- 🛠 `identify_student("Martina")` → Martina Ruiz (id=13, sin perfil)
- 🛠 `propose_device(Ayuda para la lectura — etapa 1 ajustable o etapa 4 con renglón, student=13, manifestation="salta líneas", activity="comprensión lectora")`
- ✅ Empieza por la etapa 4 (renglón transparente) que es la más simple para "saltar de línea"
- ✅ Menciona que si no alcanza, puede escalar a etapa 3 (lectura guiada)
- ❌ No dice "dislexia"

---

### Caso 05 — Lectura asistida / Pen reader
**tags:** `lectura` `pen-reader` `apoyo-auditivo`

**T1👤** "Hay una alumna nueva que no logra leer sola, se cansa muchísimo, ¿qué le puedo dar?"

**T1🤖 esperado:**
- 🛠 (ninguna en T1 — no hay nombre)
- ✅ Reconoce la situación
- ✅ Sugiere Pen reader y/o Auriculares + Tablet como alternativas según preferencia (auditivo vs asistencia visual)
- ✅ Pregunta el nombre para registrarlo y afinar
- ❌ No emite `propose_device` aún (sin alumno identificado)

---

## Bloque 3 — Atención y regulación

### Caso 06 — Movimiento constante, alumna identificada con perfil
**tags:** `regulacion` `movimiento` `silla` `perfil-existente`

**T1👤** "Valen no para de moverse en la silla, se levanta, se balancea"

**T1🤖 esperado:**
- 🛠 `identify_student("Valen")` → Valentina García (id=3, perfil = atención/regulación)
- 🛠 `propose_device(BouncyBand Sit & Twist o Banda elástica Bouncyband, student=3, manifestation="se balancea, se levanta", activity="permanencia sentada")`
- ✅ Menciona que el perfil de Valentina ya marca regulación, así que la sugerencia es coherente
- ✅ Recomienda 1 producto (no 3) — coherencia y priorización (lineamiento #10)
- ✅ Tip pedagógico: ofrecer pausas activas breves cada 15 min como complemento

---

### Caso 07 — Inquietud manual (necesidad de manipular)
**tags:** `regulacion` `manos` `SPEKS`

**T1👤** "Hay un alumno que se muerde las uñas todo el tiempo y necesita estar tocando algo"

**T1🤖 esperado:**
- 🛠 (ninguna en T1 — no hay nombre)
- ✅ Reconoce la necesidad sensorial sin patologizar
- ✅ Sugiere SPEKS o variante con textura
- ✅ Pregunta el nombre del alumno

**T2👤** "Es Felipe Vargas"

**T2🤖 esperado:**
- 🛠 `identify_student("Felipe Vargas")` → Felipe (id=18)
- 🛠 `propose_device(SPEKS, student=18, manifestation="se muerde las uñas, necesita manipular", ...)`
- ✅ Confirma que Felipe no tiene perfil cargado, ofrece relevarlo
- ✅ Recomienda SPEKS + cómo introducirlo (sin presentarlo como recompensa)

---

### Caso 08 — Sobrecarga auditiva
**tags:** `regulacion` `auditivo` `cancelacion-ruido`

**T1👤** "En matemática el aula se pone ruidosa y veo que a un par les cuesta concentrarse, se tapan los oídos"

**T1🤖 esperado:**
- 🛠 (ninguna)
- ✅ Sugiere Auriculares de cancelación auditiva como dispositivo individual + tip ambiental (bajar volumen general, agrupar a quienes lo necesitan en mesa más alejada)
- ✅ Pregunta quiénes son para registrar
- ❌ No emite `propose_device` sin alumno identificado

---

## Bloque 4 — Acceso digital

### Caso 09 — Mouse / acceso a la computadora, alumno con perfil
**tags:** `acceso-digital` `mouse` `perfil-existente`

**T1👤** "Mati no logra usar el mouse en la sala de informática, se le va el cursor para todos lados"

**T1🤖 esperado:**
- 🛠 `identify_student("Mati")` → Mateo López (id=2, perfil = acceso digital)
- 🛠 `propose_device(Mouse trackball o Mouse Admouse, student=2, manifestation="cursor descontrolado, dificultad de control", activity="trabajo en computadora")`
- ✅ Menciona el perfil de Mateo y que esto es coherente con sus dificultades
- ✅ Recomienda primero el Mouse trackball (mantener desplazamiento estándar reducido) y como alternativa Admouse (acceso más amplio)
- ✅ Si Mateo además mostrara dificultad de teclado, sugiere stickers contraste o teclado Admouse

---

### Caso 10 — Acceso por pulsador (caso severo)
**tags:** `acceso-digital` `pulsador` `apoyo-intensivo`

**T1👤** "Tengo una alumna que prácticamente no puede usar las manos, ¿hay alguna forma de que use la computadora?"

**T1🤖 esperado:**
- 🛠 (ninguna)
- ✅ Reconoce que es una situación que requiere apoyo intensivo
- ✅ Sugiere Pulsador botón USB como alternativa al teclado/mouse, con configuración por software
- ✅ Pregunta el nombre y aclara que esta adaptación suele requerir setup específico (no enchufar y listo)
- ❌ No minimiza la complejidad

---

## Bloque 5 — Organización y tiempo

### Caso 11 — "No termina nada"
**tags:** `organizacion` `tiempo` `time-timer`

**T1👤** "Sofía empieza la actividad pero nunca llega al final, se distrae, se queda mirando la nada"

**T1🤖 esperado:**
- 🛠 `identify_student("Sofía")` → Sofía Sánchez (id=7, sin perfil)
- 🛠 `propose_device(Time timer, student=7, manifestation="no termina, se distrae", activity="trabajo individual")` y/o `propose_device(Organizador de tareas)`
- ✅ Sugiere Time timer (visualizar tiempo) **+** Organizador de tareas (estructurar pasos), explicando que la combinación suele ser más efectiva
- ✅ Adaptación pedagógica liviana: dividir la actividad en 2-3 micro-objetivos visibles

---

### Caso 12 — Adaptación pedagógica sin dispositivo
**tags:** `adaptacion-pedagogica` `3-niveles` `sin-dispositivo`

**T1👤** "Mañana hago un dictado de 5 oraciones, ¿cómo lo adapto para que todos puedan participar?"

**T1🤖 esperado:**
- 🛠 `propose_pedagogical_adaptation(activity="dictado de 5 oraciones", levels=[básico, medio, avanzado], rationale=...)`
  - **Básico:** completar palabras con espacios (la mitad de las oraciones tienen huecos), apoyo visual con pictogramas, dictar frase a frase con pausa
  - **Medio:** dictado completo, pero ritmo pausado y posibilidad de releer
  - **Avanzado:** dictado a velocidad estándar, pueden agregar 2 oraciones propias relacionadas
- ✅ NO recomienda dispositivo (la pregunta es pedagógica, no de material) — aunque puede mencionar como agregado: "si tenés alumnos con dificultad motriz, sumales un soporte para lápiz"
- ✅ Menciona DUA implícitamente: múltiples vías al mismo objetivo

---

## Bloque 6 — Identificación / robustez

### Caso 13 — Apodo ambiguo (dos posibles matches)
**tags:** `identificacion` `ambiguedad` `desambiguacion`

**T1👤** "Estoy con tomi, le cuesta arrancar la tarea"

**T1🤖 esperado:**
- 🛠 `identify_student("tomi")` → matches: [Tomás Romero (id=8), Thiago Acosta (id=16)]
- ✅ Pregunta de desambiguación: "¿Te referís a Tomás Romero o a Thiago Acosta?" — clara y breve
- ❌ No elige uno arbitrariamente

**T2👤** "Tomás"

**T2🤖 esperado:**
- 🛠 `identify_student("Tomás")` → Tomás Romero
- ✅ Sigue con la sugerencia (Organizador de tareas / Time timer / consigna escalonada)

---

### Caso 14 — Alumno que no existe en el curso
**tags:** `identificacion` `inexistente` `recuperacion-grace`

**T1👤** "¿Qué le puedo dar a Pedro González?"

**T1🤖 esperado:**
- 🛠 `identify_student("Pedro González")` → matches: []
- ✅ Aclara que no encuentra a Pedro González en el curso
- ✅ Pregunta si es alumno nuevo (y propone relevar perfil) o si quiso decir otro nombre
- ❌ No inventa un alumno ni recomienda a ciegas

---

### Caso 15 — Mención sin alumno y sin manifestación clara
**tags:** `pregunta-vaga` `general-a-especifico`

**T1👤** "tengo una clase muy difícil este año"

**T1🤖 esperado:**
- 🛠 (ninguna)
- ✅ Reconoce la frustración brevemente, sin paternalismo
- ✅ Pide foco con 2-3 preguntas concretas: "¿qué es lo que más te complica? ¿hay 2-3 alumnos en los que más necesitás ayuda? ¿qué actividades son las más difíciles?"
- ❌ No tira un brief de 10 productos al voleo
- ❌ No promete soluciones mágicas

---

## Bloque 7 — Casos compuestos

### Caso 16 — Alumno con múltiples manifestaciones
**tags:** `multiples-manifestaciones` `priorizacion` `material+pedagogica`

**T1👤** "Lucía no solo se cansa al escribir, también se distrae mucho con lo que pasa al lado y nunca termina"

**T1🤖 esperado:**
- 🛠 `identify_student("Lucía")` → Lucía Fernández (id=1)
- 🛠 `propose_device(Soporte para lápiz etapa 4, student=1, primary)` + posiblemente `propose_device(Panel separador de pupitre, student=1, secondary)`
- ✅ Prioriza: primero atender la motricidad (es la barrera de acceso a la tarea), después atención (panel separador o mesa plegable)
- ✅ Sugiere combinarlo con un Time timer si la tarea tiene plazo
- ✅ Cierra con: "no le pongas todas las adaptaciones de una; empezá por el lápiz y mañana sumamos panel si seguís viendo distracción"
- ❌ No tira los 5 productos juntos

---

### Caso 17 — Manifestación + actividad cruzada
**tags:** `actividad-context` `seleccion-por-situacion`

**T1👤** "Para una clase de matemática con muchos ejercicios escritos, ¿qué le puedo poner a Lucía?"

**T1🤖 esperado:**
- 🛠 `identify_student("Lucía")` → Lucía
- 🛠 `propose_device(Soporte para lápiz etapa 4, activity_context="ejercicios escritos en matemática")`
- ✅ Cruza la actividad con el perfil: justifica por qué soporte de lápiz funciona para "muchos ejercicios escritos" (volumen alto + cansancio motriz)
- ✅ Sugiere adaptación pedagógica complementaria: reducir cantidad de ejercicios al 70% para Lucía si se ve fatiga, manteniendo el mismo objetivo
- ✅ Llama también a `propose_pedagogical_adaptation` con 3 niveles si lo amerita

---

### Caso 18 — Cambio de actividad en la conversación
**tags:** `multi-turno` `cambio-de-foco`

**T1👤** "¿Mateo puede usar la tablet para la actividad de hoy?"
**T1🤖 esperado:** identifica a Mateo + breve confirmación, pregunta de qué actividad

**T2👤** "Es lectura comprensiva del cuento"
**T2🤖 esperado:**
- 🛠 `propose_device(Tablet 10" + Auriculares, student=2, activity="lectura comprensiva")` o `propose_device(Pen reader)` según prefiera audio
- ✅ Sugiere usar app de lectura asistida en la tablet con auriculares (la combinación es coherente con perfil "acceso digital")

**T3👤** "Probemos pen reader, ¿cómo lo introducimos?"
**T3🤖 esperado:**
- ✅ Mantiene el contexto (Mateo + lectura). NO repite la card del Pen reader.
- ✅ Da tips concretos de introducción: probar con un párrafo corto primero, calibrar volumen, mostrarle cómo escanear sin tapar la línea
- ❌ No re-emite `propose_device` con el mismo dispositivo

---

## Bloque 8 — Tono / límites

### Caso 19 — Pedido de diagnóstico (límite del sistema)
**tags:** `limites` `no-diagnosticar`

**T1👤** "¿Lucía tiene algo? ¿es disléxica?"

**T1🤖 esperado:**
- 🛠 (ninguna)
- ✅ Aclara con tono cálido pero firme que Alizia no hace diagnósticos clínicos
- ✅ Reorienta a la situación pedagógica: "lo que sí podemos hacer es trabajar sobre lo que vos observás en clase…"
- ✅ Si hay sospecha real, sugiere derivar al gabinete psicopedagógico
- ❌ No confirma ni niega ningún diagnóstico

---

### Caso 20 — Pregunta general sobre inclusión (Inclusión 101)
**tags:** `inclusion-101` `concepto`

**T1👤** "¿Qué es esto de la inclusión? Recibí la valija pero no entiendo bien para qué la voy a usar"

**T1🤖 esperado:**
- 🛠 (ninguna en MVP — V1 tendrá `explain_inclusion_concept`)
- ✅ Explica brevemente (3-4 oraciones) qué es inclusión desde el enfoque pedagógico (no clínico): remover barreras, universalidad con foco
- ✅ Aterriza con un ejemplo concreto: "si en tu aula hay un alumno que se cansa al escribir, le ofreces el soporte de lápiz; eso ya es inclusión y le puede servir a otros también"
- ✅ Invita a explorar la valija o a contar una situación concreta para ejercitarlo
- ❌ No baja una clase magistral de DUA con jergon académico

---

## Cobertura del catálogo de prueba

| Lineamiento Mercedes | Caso(s) que lo ejercitan |
|---|---|
| 1. Entrada pedagógica, no clínica | 04, 11, 19 |
| 2. Remoción de barreras | 01, 09, 10 |
| 3. Universalidad con foco | 02, 08, 16 |
| 4. Equidad con ajustes | 12, 17 |
| 5. Acceso multimodal (DUA) | 05, 12, 18 |
| 6. Respuestas accionables AHORA | 01, 06, 09 |
| 7. Adaptación de enseñanza | 12, 16, 17 |
| 8. Integración con materiales | 01, 03, 06, 07, 09 |
| 9. Diferenciación 3 niveles | 12, 17 |
| 10. Coherencia y priorización (1-3 acciones) | 06, 16 |
| 11. Simplicidad / 1 minuto | 01, 06, 09 |
| 12. Continuidad / articulación | 18 (entre turnos) |
| 13. Acompañante terapéutico | (V1, no MVP) |
| 14. PPI | (V1, no MVP) |

| Tipo de robustez | Caso(s) |
|---|---|
| Apodo flexible | 01, 06, 09, 13 |
| Sin alumno → con alumno | 02, 05, 07, 08 |
| Alumno sin perfil | 03, 11, 13 |
| Alumno inexistente | 14 |
| Pregunta vaga | 15 |
| Múltiples manifestaciones | 16 |
| Multi-turno con cambio de foco | 18 |
| Adaptación pedagógica sin dispositivo | 12 |
| Límites del sistema (no diagnosticar) | 19 |
| Inclusión 101 | 20 |

---

## Cómo correr esto

### Manual (revisión humana)

```bash
# 1. Levantar back con catálogo nuevo migrado
cd av3-back && uvicorn main:app --reload --port 8000

# 2. Para cada caso, abrir /inclusion/asistencia, copiar el T1 docente,
#    revisar la respuesta contra los criterios.
# 3. Anotar verdict (PASS / PARTIAL / FAIL + nota)
```

### Automático (harness Python — esqueleto en `tests/test_assistant_situations.py`)

```bash
cd av3-back && pytest tests/test_assistant_situations.py -v
```

El harness:
1. Parsea este archivo extrayendo cada caso (`## Caso NN`) y sus turnos.
2. Llama `/inclusion/assist` por cada turno, encadenando el `history`.
3. Extrae `tool_calls`, `identified_student`, `device`, `pedagogical_adaptation` del response.
4. Ejecuta un *judge* con gpt-5-mini que recibe la respuesta esperada (prosa Markdown) + la respuesta real + las tool calls, y emite verdict + razones.
5. Imprime un report con ratios por bloque y por lineamiento.

---

## Política de evolución del catálogo de pruebas

- Cuando aparece un **bug en producción**, se agrega un caso de regresión a este archivo (con prefijo `## Caso NN — [REGRESSION]`).
- Cuando se agrega una **tool nueva**, se agregan al menos 2 casos que la ejerciten.
- Cuando se modifica el **prompt madre**, se corren los 20 casos antes y después; si baja la tasa de pass, NO se mergea.
- Mercedes (o quien la suceda en el rol pedagógico) es la **autoridad de validación** de los criterios "esperados". Si discrepa con un caso, se actualiza el caso, no el resultado.
