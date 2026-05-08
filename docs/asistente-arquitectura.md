# Asistente de Inclusión — Arquitectura propuesta

> **Estado:** Draft 1 — modo arquitecto. Pendiente de aprobación antes de ejecutar.
> **Fecha:** 2026-05-08
> **Alcance de este documento:** propuesta integral del asistente de `/inclusion/asistencia` (modo "asistencia en el aula"). Incluye actualización del catálogo de productos, prompt madre, 3 tools del agente, cambios al backend/frontend, MVP recortado y catálogo de situaciones de prueba.
> **Inputs base:**
> - `Valijas adaptativa - Flujo de demo.md` (lineamientos pedagógicos + 15 casos)
> - `Seguimiento proyecto Valijas 22-04.txt` y `29-04.txt` (acuerdos con Mercedes/Anabela/Agustina)
> - Sheets `Listado productos FINAL`, `Matriz General`, `Matriz Perfil alicia`
> - `PRD-Modulo-Inclusion.md` (versión actual)
> - Estado actual del código: `main.py:3715-3853` y `av3-front/src/pages/InclusionAsistencia.tsx`

---

## 0. TL;DR

El asistente actual funciona pero deja mucho valor sobre la mesa:

1. **Catálogo enviado al LLM es ~30% de lo disponible.** Hoy se mandan `id, name, ramp, needs_description`. La DB tiene `description, how_to_use, recommendations, rationale, classroom_benefit, evaluation_criteria` que el modelo nunca ve.
2. **Prompt madre genérico.** No incorpora los 14 lineamientos de Mercedes, ni DUA, ni la matriz manifestación→producto, ni los 15 casos comunes con su adaptación base.
3. **Catálogo de productos desactualizado.** DB tiene 18 dispositivos; el listado FINAL del Sheets tiene 34 (con 4 etapas de soporte de lápiz, 4 etapas de ayudas para lectura, línea zurdos, etc.).
4. **Flujo rígido.** El prompt obliga a identificar alumno antes de recomendar dispositivo; Mercedes pidió lo opuesto: respuestas escalonadas.
5. **Tags por regex frágiles** (`[STUDENT_ID:X]` / `[DEVICE_ID:X]`). Function calling es más confiable.
6. **No distingue adaptación de material vs adaptación pedagógica** (que Mercedes separó explícitamente: la valija da el dispositivo, la pedagogía da los 3 niveles de actividad).
7. **Sin feedback loop ni alumno nuevo ni manifestaciones-as-input.**

**Plan en 3 oleadas:**

| Oleada | Qué se hace | Esfuerzo | Impacto |
|---|---|---|---|
| **MVP** (esta semana) | Catálogo de 34 productos en DB · prompt madre nuevo con DUA + lineamientos · 3 tools (`identify_student`, `propose_device`, `propose_pedagogical_adaptation`) · 20 casos de prueba | M | Alto |
| **V1** (siguiente sprint) | Tools de `lookup_by_manifestation`, `create_student_profile`, `register_use_outcome` · matriz manifestación→producto cargada · feedback post-clase | M | Alto |
| **V2** | Sugerencia de prolongación fuera del aula · accesibilidad UI (baja visión, dislexia) · soporte multi-curso · dashboard de uso · flujos de planificación / QR / onboarding como modos diferenciados | L | Medio |

---

## 1. Norte y principios pedagógicos

### 1.1 Qué es Alizia (Modo Inclusión)

Asistente conversacional para docentes de aula que no son especialistas en inclusión ni en tecnología adaptativa. Su norte: **eliminar barreras al aprendizaje y a la participación** integrando dispositivos de la Valija + adaptaciones pedagógicas, en menos de 1 minuto de conversación.

### 1.2 Tres ejes / 14 lineamientos (Mercedes Herrera)

**Eje 1 — PRINCIPIOS PEDAGÓGICOS (qué es la inclusión en Alizia):**
1. Entrada pedagógica, no clínica — se parte de situaciones de aula y manifestaciones observables, no de diagnósticos.
2. Remoción de barreras como eje.
3. Universalidad con foco en quienes más lo necesitan — la propuesta sirve para todo el grupo, priorizando a quienes presentan mayores barreras.
4. Equidad con ajustes proporcionales (incluye adaptación curricular cuando hay PPI).
5. Acceso multimodal — visual, oral, manipulativo, temporal y tecnológico.

**Eje 2 — PRINCIPIOS DE FUNCIONAMIENTO (cómo responde Alizia):**
6. Respuestas accionables en contexto real — concretas, breves, aplicables ahora.
7. Adaptación de la enseñanza como prioridad, con posibilidad de intervenciones individuales.
8. Integración con los materiales de la valija — siempre indicando cuándo usar el material, para qué sirve y cómo implementarlo.
9. Diferenciación pedagógica estructurada — **mínimo 3 niveles** de la misma actividad.
10. Coherencia y priorización — 1–3 acciones claras, ordenadas por impacto.

**Eje 3 — PRINCIPIOS DE USO (cómo lo usa el docente):**
11. Simplicidad y rapidez — respuesta útil en menos de 1 minuto.
12. Continuidad y articulación — integra info de familia/profesionales y sugiere prolongación fuera del aula cuando aplica.
13. Articulación con acompañante terapéutico cuando existe.
14. Apoyo en diseño e implementación de PPI cuando corresponde.

### 1.3 Marco teórico operativo

- **DUA** (Diseño Universal del Aprendizaje) como base estructural — múltiples vías de acceso, expresión y participación.
- **Diferenciación pedagógica** estructurada en 3 niveles (bajo / medio / alto).
- **Voz no patologizante** — el docente describe lo que ve (manifestaciones), no lo que diagnostica.
- **Distinción explícita** entre **adaptación de material** (la valija) y **adaptación pedagógica** (currícula, consigna, niveles de actividad).

### 1.4 Límites del sistema

Alizia **NO**:
- Realiza diagnósticos clínicos
- Reemplaza al docente, al psicopedagogo, a la maestra integradora ni al acompañante terapéutico
- Define tratamientos terapéuticos
- Produce informes clínicos

### 1.5 Voz y estilo

- Español rioplatense, vos.
- Tono cálido, profesional, directo. Sin paternalismos.
- Sin jerga clínica (no "TDAH", sí "le cuesta sostener la atención").
- Brevedad: el docente está en el aula. **Máx. 4–6 oraciones por turno** salvo que el docente pida más.

---

## 2. Estado actual (qué hay hoy)

### 2.1 Catálogo en DB (`devices`)

18 dispositivos cargados, todos con campos descriptivos llenos:

| Campo | Llenado | Lo manda al LLM hoy |
|---|---|---|
| `name` | ✓ | ✓ |
| `description` | ✓ (~200 chars/u) | ✗ |
| `needs_description` | ✓ (~250 chars/u) | ✓ |
| `how_to_use` | ✓ (~250 chars/u) | ✗ |
| `recommendations` | ✓ (~250 chars/u) | ✗ |
| `rationale` | ✓ (~200 chars/u) | ✗ |
| `classroom_benefit` | ✓ | ✗ |
| `evaluation_criteria` | ✓ | ✗ |
| `ramp_id` (3 rampas) | ✓ | ✓ (como `ramp_name`) |
| `image_url`, `qr_code`, `quantity` | parcial | ✗ |

**El 70% de la riqueza descriptiva del catálogo nunca llega al modelo.** Es la victoria fácil más grande del MVP.

### 2.2 Prompt actual (`ASSIST_SYSTEM_PROMPT`, `main.py:3715`)

Contiene: voz general, regla de identificación de alumnos por apodo, regla de no recomendar dispositivo sin haber identificado alumno, formato de respuesta. **NO contiene:**
- Marco DUA / lineamientos pedagógicos
- Distinción material vs pedagógica
- Manifestaciones observables como entrada
- Casos típicos con adaptación base
- Restricción de no usar diagnósticos

### 2.3 Endpoint `/inclusion/assist`

- Recibe `{message, history?, student_id?}`.
- `course_id = 1` hardcodeado en la query de students.
- Retry 3x si Azure devuelve respuesta vacía.
- Extrae `[STUDENT_ID:X]` y `[DEVICE_ID:X]` con regex.
- Devuelve `{response, identified_student, device}`.

### 2.4 Frontend

`InclusionAsistencia.tsx` (374 líneas) — chat simple con `useState`, render de `StudentMiniCard` y `DeviceCard`, modal `DeviceDetailModal` con todas las secciones (Beneficio · Cómo usar · Enfoque pedagógico · Tips · Necesidades · Evaluación). El modal **sí** muestra todos los campos al docente. La asimetría es: **el usuario ve más que el LLM**.

---

## 3. Productos: actualización propuesta

### 3.1 Diff DB ↔ Listado FINAL

El listado FINAL (Sheets) tiene **34 productos**, la DB **18**. Resumen del diff:

#### Productos a CONSERVAR sin cambio (mapeo 1:1)
| DB actual | Listado FINAL |
|---|---|
| Tablet educativa (10") | Tablet 10'' Android + 8GB RAM + disco 128 GB |
| Mouse trackball | Mouse trackball |
| Stickers de contraste para teclado | Sticker con contraste para teclado |
| Pulsador boton USB | Pulsador botón USB |
| Pen reader (lapiz lector) | Pen reader |
| Patas de silla (almohadillas sensoriales) | Patas de silla x4 |
| Time Timer (temporizador visual) | Time timer |
| Auriculares cancelacion de ruido | Auriculares de cancelación auditivo |
| Auriculares con microfono | Auriculares (¿con micrófono o no? — **TBD validar con Anabela**) |

#### Productos a RENOMBRAR (mismo objeto, nombre del Sheets es más preciso)
| DB actual | Renombrar a | Razón |
|---|---|---|
| Pinzas de escritura | **Soporte para lápiz 1 — etapa 4** | El Sheets modela 4 etapas progresivas; "Pinzas" corresponde a etapa 4 (la más simple, etapa final del proceso). Las otras 3 etapas hay que **agregarlas**. |
| Tijeras adaptadas | **Tijera adaptada — etapa 1** | La etapa 2 hay que agregarla. |
| Regla lupa | **Ayuda para la lectura — tamaño ajustable — etapa 1** | Es el primer nivel de las ayudas para lectura. |
| Regla de lectura con ventana | **Ayuda para la lectura — tamaño fijo 2 palabras — etapa 2** | Segundo nivel. |
| Finger focus (señalador de dedo) | **Ayuda para la lectura — Reglas de lectura guiada — etapa 3** | Tercer nivel. |
| Elastico para silla | **Banda elástica Bouncyband** | Mismo objeto, naming oficial. |

#### Productos a REEMPLAZAR (cambio de hardware decidido por el equipo)
| DB actual | Listado FINAL — reemplazo |
|---|---|
| Teclado CLEVY | **Teclado Admouse** — pendiente confirmar con Anabela si es 1:1 o coexisten. Por ahora **reemplazar** (alineado con que el Listado FINAL ya no lista CLEVY). |

#### Productos a AGREGAR (nuevos en el catálogo)
1. Soporte para lápiz 2 — etapa 3
2. Soporte para lápiz 3 — etapa 2
3. Soporte para lápiz 4 — etapa 1
4. Pesas para lápices
5. Muñequera sensorial x2
6. Material sensorial de apriete SPEKS
7. Material sensorial de apriete SPEKS con textura
8. Pelota para el pie (vaivén) o muslo (presión)
9. BouncyBand Sit & Twist Cojín de Asiento Activo
10. Ayuda para la lectura — Reglas de lectura transparente con renglón — etapa 4
11. Panel separador de pupitre
12. Sacapuntas para zurdos *(metadata vacía en Sheets — pedir a Mercedes/Anabela)*
13. Lapicera para zurdos *(metadata vacía en Sheets — pedir)*
14. Tijera para zurdos *(metadata vacía en Sheets — pedir)*
15. Organizador de tareas personalizable
16. Mesa plegable portátil para favorecer la concentración y la atención
17. Mouse Admouse
18. Tijera adaptada — etapa 2

#### Productos en DB que NO están en el listado FINAL (decidir)
| Producto | Sugerencia |
|---|---|
| **Pelota antiestrés de gel** | **Conservar.** Anabela la mencionó explícitamente en la reunión 22-04 ("la pelotita merce, cómo lo ves? Que mandemos todo esto?"). El Listado FINAL puede no estar 100% sincronizado. **Validar con Anabela.** |
| **Soporte flexible celular/tablet** | **Conservar.** No está en el Listado FINAL pero es funcionalmente útil para movilidad reducida y la DB ya tiene metadata completa. **Validar con Anabela.** |
| **Teclado CLEVY** | Reemplazar por Teclado Admouse (ver arriba). |

### 3.2 Schema enriquecido (campos nuevos)

Se proponen campos adicionales en `devices` para encajar la información de la Matriz General:

```sql
ALTER TABLE devices
  ADD COLUMN stage           SMALLINT,           -- 1..4 para productos por etapas (NULL si no aplica)
  ADD COLUMN material_class  TEXT[],             -- ["Acceso al aprendizaje","Regulación, atención","Adaptación del entorno","Accesibilidad tecnológica","Organización"]
  ADD COLUMN frequent_profile TEXT[],            -- ["DEA","TEA","discapacidad motora","discapacidad intelectual","altas capacidades","discapacidad visual","discapacidad auditiva"]
  ADD COLUMN specific_profile TEXT[],            -- ["Parálisis cerebral","Síndrome de Down","TEA con apoyo leve","Disgrafía","TDAH","Dislexia",...]
  ADD COLUMN function_summary TEXT,              -- 3-5 frases de Función pedagógica
  ADD COLUMN pedagogical_situations TEXT[],      -- ["Actividades de recorte","Trabajos manuales y plásticos",...]
  ADD COLUMN observable_manifestations TEXT[],   -- ["Sostiene mal el lápiz","Hace mucha fuerza al escribir",...]
  ADD COLUMN active BOOLEAN DEFAULT TRUE;        -- soft-delete para productos retirados
```

**Por qué estos campos:**
- `observable_manifestations` es la **clave** para que el LLM matchee texto del docente ("se le cae el lápiz") → producto. Hoy todo eso vive en `needs_description` mezclado con prosa.
- `pedagogical_situations` permite filtrar por el contexto de la actividad (recorte vs lectura vs escritura).
- `material_class` da una taxonomía para ordenar respuestas: primero clase "Acceso al aprendizaje", luego "Regulación", etc.
- `frequent_profile` y `specific_profile` no se exponen al docente (no patologización) pero el LLM los puede usar como **contexto de razonamiento interno**.
- `stage` permite recomendar progresión: "empezá con etapa 4 (más simple), si funciona avanzamos a etapa 3".
- `active` para hacer soft-delete en lugar de borrar registros con historial de uso.

### 3.3 Migración SQL completa (lista para correr)

Archivo nuevo: `migrations/010_devices_update.sql`. **No se corre en este sprint sin revisión.** El UPDATE → renombre + el INSERT de los 18 productos nuevos van en el mismo archivo para que sea una migración atómica.

```sql
-- 010_devices_update.sql
-- Actualiza el catálogo de devices al Listado FINAL (Valija 2026).
-- Idempotente: usa ON CONFLICT donde aplica.

BEGIN;

-- 1) Schema enrichment
ALTER TABLE devices
  ADD COLUMN IF NOT EXISTS stage                     SMALLINT,
  ADD COLUMN IF NOT EXISTS material_class            TEXT[] DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS frequent_profile          TEXT[] DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS specific_profile          TEXT[] DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS function_summary          TEXT,
  ADD COLUMN IF NOT EXISTS pedagogical_situations    TEXT[] DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS observable_manifestations TEXT[] DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS active                    BOOLEAN DEFAULT TRUE;

-- 2) Renombres + reasignación de etapa para los productos existentes
UPDATE devices SET name = 'Soporte para lápiz 1 — etapa 4',
  stage = 4
  WHERE name = 'Pinzas de escritura';
UPDATE devices SET name = 'Tijera adaptada — etapa 1',
  stage = 1
  WHERE name = 'Tijeras adaptadas';
UPDATE devices SET name = 'Ayuda para la lectura — tamaño ajustable — etapa 1',
  stage = 1
  WHERE name = 'Regla lupa';
UPDATE devices SET name = 'Ayuda para la lectura — tamaño fijo 2 palabras — etapa 2',
  stage = 2
  WHERE name = 'Regla de lectura con ventana';
UPDATE devices SET name = 'Ayuda para la lectura — Reglas de lectura guiada — etapa 3',
  stage = 3
  WHERE name = 'Finger focus (senalador de dedo)';
UPDATE devices SET name = 'Banda elástica Bouncyband'
  WHERE name = 'Elastico para silla';

-- 3) Reemplazo: Teclado CLEVY → Teclado Admouse
UPDATE devices SET
  name = 'Teclado Admouse',
  description = 'Teclado adaptado de gran formato pensado para acceso cognitivo y motor. Letras y teclas grandes con colores diferenciados por grupos.',
  needs_description = 'Acompaña a estudiantes que: tienen dificultades motoras para presionar teclas convencionales, baja visión, dificultades para identificar letras, o se frustran con teclados estándar.'
  WHERE name = 'Teclado CLEVY';

-- 4) Insertar los productos nuevos del Listado FINAL.
-- Estructura: ramp_id, name, description, needs_description, how_to_use, recommendations,
-- rationale, classroom_benefit, evaluation_criteria, observable_manifestations,
-- pedagogical_situations, frequent_profile, specific_profile, material_class, stage, quantity, sort_order.
--
-- Las metadatas largas (description, how_to_use, etc.) se completan con el contenido
-- de la Matriz General — ver Apéndice A para el detalle producto a producto.

-- Rampa Didáctico-Pedagógica (ramp_id = 2)
INSERT INTO devices (ramp_id, name, stage, quantity, sort_order, description, function_summary, observable_manifestations, pedagogical_situations, material_class, frequent_profile, specific_profile)
VALUES
  (2, 'Soporte para lápiz 2 — etapa 3', 3, 10, 21,
   'Soporte adaptador de lápiz progresivo (etapa 3). Mejora la prensión y favorece la postura adecuada de la mano.',
   'Mejora la prensión del lápiz. Favorece la postura adecuada. Facilita el control del trazo. Reduce el esfuerzo en la escritura.',
   ARRAY['Sostiene mal el lápiz','Hace mucha fuerza al escribir','Se le cae el lápiz','Se cansa rápido al escribir','La letra es poco legible','Le cuesta controlar el trazo'],
   ARRAY['Escritura en clase','Actividades de copia','Tareas de producción escrita','Ejercicios de grafomotricidad'],
   ARRAY['Acceso al aprendizaje'],
   ARRAY['DEA','TEA','discapacidad motora','discapacidad intelectual'],
   ARRAY['Parálisis cerebral','Síndrome de Down','TEA con apoyo notable','TEA con mayor necesidad de apoyo','Disgrafía','TDAH']),

  (2, 'Soporte para lápiz 3 — etapa 2', 2, 5, 22,
   'Soporte adaptador de lápiz progresivo (etapa 2).',
   'Mejora la prensión del lápiz. Favorece la postura adecuada. Facilita el control del trazo. Reduce el esfuerzo en la escritura.',
   ARRAY['Sostiene mal el lápiz','Hace mucha fuerza al escribir','Se le cae el lápiz','Se cansa rápido al escribir','La letra es poco legible','Le cuesta controlar el trazo'],
   ARRAY['Escritura en clase','Actividades de copia','Tareas de producción escrita','Ejercicios de grafomotricidad'],
   ARRAY['Acceso al aprendizaje'],
   ARRAY['DEA','TEA','discapacidad motora','discapacidad intelectual'],
   ARRAY['Parálisis cerebral','Síndrome de Down','TEA con apoyo notable','TEA con mayor necesidad de apoyo','Disgrafía','TDAH']),

  (2, 'Soporte para lápiz 4 — etapa 1', 1, 5, 23,
   'Soporte adaptador de lápiz progresivo (etapa 1, mayor sostén).',
   'Mejora la prensión del lápiz. Favorece la postura adecuada. Facilita el control del trazo. Reduce el esfuerzo en la escritura.',
   ARRAY['Sostiene mal el lápiz','Hace mucha fuerza al escribir','Se le cae el lápiz','Se cansa rápido al escribir','La letra es poco legible','Le cuesta controlar el trazo'],
   ARRAY['Escritura en clase','Actividades de copia','Tareas de producción escrita','Ejercicios de grafomotricidad'],
   ARRAY['Acceso al aprendizaje'],
   ARRAY['DEA','TEA','discapacidad motora','discapacidad intelectual'],
   ARRAY['Parálisis cerebral','Síndrome de Down','TEA con apoyo notable','TEA con mayor necesidad de apoyo','Disgrafía','TDAH']),

  (2, 'Pesas para lápices', NULL, 10, 24,
   'Pesas que se colocan sobre el lápiz para aumentar la estabilidad de la mano.',
   'Aumenta la estabilidad de la mano durante la escritura. Disminuye movimientos excesivos. Favorece el control del trazo. Mejora la precisión en la escritura.',
   ARRAY['Mueve mucho la mano al escribir','El trazo es inestable','Escribe con movimientos bruscos','Le cuesta controlar el lápiz','Cambia constantemente la posición de la mano'],
   ARRAY['Actividades de escritura','Tareas que requieren precisión','Trabajos prolongados de escritura','Momentos de copia o dictado'],
   ARRAY['Regulación, atención'],
   ARRAY['DEA','TEA','discapacidad motora','discapacidad intelectual'],
   ARRAY['Parálisis cerebral','Síndrome de Down','TEA con apoyo notable','Disgrafía','TDAH']),

  (2, 'Tijera adaptada — etapa 2', 2, 1, 25,
   'Tijera adaptada con mayor asistencia mecánica (etapa 2).',
   'Facilita el uso funcional de la tijera. Permite el control del movimiento de corte. Reduce el esfuerzo en tareas de recorte.',
   ARRAY['No puede usar la tijera convencional','Tiene movimientos bruscos','No puede sostener la tijera','No puede usar las manos','Necesita ayuda para recortar'],
   ARRAY['Actividades de recorte','Trabajos manuales y plásticos','Tareas de motricidad fina','Actividades guiadas o autónomas'],
   ARRAY['Acceso al aprendizaje'],
   ARRAY['discapacidad motora','TEA','discapacidad intelectual'],
   ARRAY['Parálisis cerebral','Síndrome de Down','TEA con mayor necesidad de apoyo']),

  (2, 'Ayuda para la lectura — Reglas de lectura transparente con renglón — etapa 4', 4, 10, 26,
   'Regla de lectura transparente con renglón resaltado (etapa 4 — última, mayor autonomía).',
   'Facilita el seguimiento visual del texto. Favorece la organización de la lectura. Facilita el acceso al contenido escrito. Favorece el aprendizaje de la lectoescritura. Facilita la concentración y la atención.',
   ARRAY['Salta la línea al leer','Se desorienta en el texto','Lee muy lento','Se cansa al leer','Le cuesta seguir la lectura'],
   ARRAY['Actividades de lectura','Actividades de comprensión lectora','Trabajo individual con textos','Tareas de copia'],
   ARRAY['Acceso al aprendizaje','atención'],
   ARRAY['TEA','discapacidad intelectual','DEA','discapacidad visual'],
   ARRAY['TDAH','Dislexia','Síndrome de Down','baja visión','TEA con apoyo leve']);

-- Rampa de Autorregulación Sensorial (ramp_id = 3)
INSERT INTO devices (ramp_id, name, stage, quantity, sort_order, description, function_summary, observable_manifestations, pedagogical_situations, material_class, frequent_profile, specific_profile)
VALUES
  (3, 'Muñequera sensorial x2', NULL, 2, 31,
   'Par de muñequeras sensoriales con peso liviano que aportan estabilidad propioceptiva.',
   'Aumenta la estabilidad de la mano durante la escritura. Disminuye movimientos excesivos. Favorece el control del trazo. Mejora la precisión en la escritura.',
   ARRAY['Mueve mucho la mano al escribir','El trazo es inestable','Escribe con movimientos bruscos','Le cuesta controlar el lápiz','Cambia constantemente la posición de la mano'],
   ARRAY['Actividades de escritura','Tareas que requieren precisión','Trabajos prolongados','Momentos de copia o dictado'],
   ARRAY['Regulación, atención'],
   ARRAY['DEA','TEA','discapacidad motora','discapacidad intelectual'],
   ARRAY['Disgrafía','TDAH','Parálisis cerebral','Síndrome de Down']),

  (3, 'Material sensorial de apriete SPEKS', NULL, 6, 32,
   'Set de bolitas magnéticas SPEKS para canalizar la necesidad de movimiento manual.',
   'Canaliza la necesidad de movimiento manual. Favorece la autorregulación durante la tarea. Reduce la inquietud motora. Facilita el sostenimiento de la atención.',
   ARRAY['Se inquieta constantemente','Necesita manipular objetos','Lleva objetos a la boca','Se muerde las uñas','Le cuesta quedarse quieto','Se distrae con facilidad','Busca estímulos con las manos','Se pone ansioso durante la tarea'],
   ARRAY['Actividades que requieren concentración','Momentos de escucha (clase expositiva)','Trabajo autónomo','Situaciones de espera / ansiedad'],
   ARRAY['Regulación, atención'],
   ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
   ARRAY['TDAH','TEA con apoyo leve','Dislexia','alto potencial intelectual']),

  (3, 'Material sensorial de apriete SPEKS con textura', NULL, 2, 33,
   'Variante con textura del SPEKS, para input sensorial adicional.',
   'Canaliza la necesidad de movimiento manual. Favorece la autorregulación durante la tarea. Reduce la inquietud motora. Facilita el sostenimiento de la atención.',
   ARRAY['Se inquieta constantemente','Necesita manipular objetos','Lleva objetos a la boca','Se muerde las uñas','Le cuesta quedarse quieto','Se distrae con facilidad','Busca estímulos con las manos','Se pone ansioso durante la tarea'],
   ARRAY['Actividades que requieren concentración','Momentos de escucha','Trabajo autónomo','Situaciones de espera / ansiedad'],
   ARRAY['Regulación, atención'],
   ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
   ARRAY['TDAH','TEA con apoyo leve','Dislexia','alto potencial intelectual']),

  (3, 'Pelota para el pie (vaivén) o muslo (presión)', NULL, 3, 34,
   'Pelota que se usa apoyada en el pie (vaivén) o bajo el muslo (presión) para canalizar el movimiento sin abandonar la tarea.',
   'Permite el movimiento sin abandonar la tarea. Canaliza la inquietud motora. Favorece la permanencia en el lugar. Facilita la concentración y la atención.',
   ARRAY['Mueve constantemente las piernas','Se levanta de la silla','No logra quedarse sentado','Necesita moverse mientras trabaja','Se inquieta durante la actividad'],
   ARRAY['Trabajo en mesa','Actividades largas','Momentos que requieren permanencia sentado','Tareas individuales'],
   ARRAY['Regulación, atención'],
   ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
   ARRAY['TDAH','TEA con apoyo notable','alto potencial intelectual','Dislexia']),

  (3, 'BouncyBand Sit & Twist Cojín de Asiento Activo', NULL, 1, 35,
   'Cojín de asiento activo que permite movimiento controlado en la silla.',
   'Permite el movimiento controlado en la silla. Reduce la necesidad de levantarse. Favorece la autorregulación motora. Facilita la permanencia en la actividad.',
   ARRAY['Se balancea en la silla','Se levanta con frecuencia','Mueve constantemente el cuerpo','Le cuesta permanecer en su lugar','Interrumpe la tarea por movimiento','Pierde la atención con facilidad'],
   ARRAY['Actividades en el pupitre','Trabajo prolongado','Momentos de escucha','Tareas individuales'],
   ARRAY['Regulación, atención'],
   ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
   ARRAY['TDAH','TEA con apoyo leve','TEA con apoyo notable','alto potencial intelectual','Dislexia']);

-- Rampa Didáctico-Pedagógica (organización / entorno)
INSERT INTO devices (ramp_id, name, stage, quantity, sort_order, description, function_summary, observable_manifestations, pedagogical_situations, material_class, frequent_profile, specific_profile)
VALUES
  (2, 'Panel separador de pupitre', NULL, 1, 27,
   'Panel que se coloca alrededor del pupitre para reducir estímulos visuales del entorno.',
   'Reduce estímulos visuales del entorno. Disminuye distractores. Favorece la concentración en la tarea.',
   ARRAY['Se distrae con lo que sucede alrededor','Pierde el foco con facilidad','Le cuesta concentrarse en su tarea','Pierde la atención','Le molesta el entorno'],
   ARRAY['Trabajo individual','Actividades que requieren concentración sostenida','Momentos de sobrecarga de estímulos','Tareas complejas o nuevas'],
   ARRAY['Adaptación del entorno','regulación','atención'],
   ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
   ARRAY['TDAH','TEA con apoyo leve','TEA con apoyo notable','alto potencial intelectual','Dislexia']),

  (2, 'Organizador de tareas personalizable', NULL, 4, 28,
   'Organizador visual configurable para estructurar la secuencia de actividades.',
   'Estructura la secuencia de actividades. Facilita la planificación de la tarea. Mejora la organización personal. Favorece la autonomía. Reduce la ansiedad.',
   ARRAY['Olvida lo que tiene que hacer','No sabe por dónde empezar','Deja tareas sin terminar','Se desorganiza fácilmente','Pierde materiales','Le cuesta seguir una secuencia'],
   ARRAY['Inicio de una actividad','Planificación de tareas','Trabajos por etapas','Seguimiento de actividades'],
   ARRAY['Organización','regulación'],
   ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
   ARRAY['Dislexia','Disgrafía','Síndrome de Down','TDAH','TEA con apoyo leve','TEA con apoyo notable','alto potencial intelectual']),

  (2, 'Mesa plegable portátil', NULL, 1, 29,
   'Mesa plegable portátil para favorecer la concentración generando un espacio individual.',
   'Reduce la exposición a estímulos del entorno. Genera un espacio de trabajo con menor distracción. Favorece la concentración. Facilita la permanencia en la tarea y la atención.',
   ARRAY['Se distrae con lo que sucede alrededor','Pierde el foco con facilidad','Le cuesta concentrarse en su tarea','Se distrae con estímulos del entorno','Le cuesta concentrarse en grupo','Se sobreestimula fácilmente','Busca lugares tranquilos para trabajar'],
   ARRAY['Inicio de una tarea','Actividades con tiempo limitado','Transiciones entre actividades','Trabajo individual','Actividades que requieren concentración sostenida'],
   ARRAY['Adaptación del entorno','regulación','atención'],
   ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
   ARRAY['Dislexia','Síndrome de Down','TDAH','TEA con apoyo leve','TEA con apoyo notable','alto potencial intelectual']),

  (2, 'Sacapuntas para zurdos', NULL, 1, 41,
   'Sacapuntas con orientación adaptada para zurdos.',
   NULL,
   ARRAY['Se cansa al sacar punta','Le cuesta usar el sacapuntas','Necesita herramientas para zurdos'],
   ARRAY['Actividades de escritura','Tareas con lápiz'],
   ARRAY['Acceso al aprendizaje'],
   ARRAY['DEA'],
   ARRAY[]::text[]),
  (2, 'Lapicera para zurdos', NULL, 1, 42,
   'Lapicera ergonómica para zurdos.',
   NULL,
   ARRAY['Mancha el cuaderno al escribir','Le cuesta sostener la lapicera','Necesita herramientas para zurdos'],
   ARRAY['Actividades de escritura'],
   ARRAY['Acceso al aprendizaje'],
   ARRAY['DEA'],
   ARRAY[]::text[]),
  (2, 'Tijera para zurdos', NULL, 1, 43,
   'Tijera con orientación adaptada para zurdos.',
   NULL,
   ARRAY['Le cuesta cortar con tijera convencional','Necesita herramientas para zurdos'],
   ARRAY['Actividades de recorte','Trabajos manuales'],
   ARRAY['Acceso al aprendizaje'],
   ARRAY['DEA'],
   ARRAY[]::text[]);

-- Rampa Digital (ramp_id = 1) — Mouse Admouse
INSERT INTO devices (ramp_id, name, stage, quantity, sort_order, description, function_summary, observable_manifestations, pedagogical_situations, material_class, frequent_profile, specific_profile)
VALUES
  (1, 'Mouse Admouse', NULL, 1, 11,
   'Mouse adaptativo de gran formato. Pensado para acceso motor y cognitivo simplificado.',
   'Facilita el control del cursor sin desplazamiento del dispositivo. Mejora la precisión del movimiento. Reduce la exigencia motora fina. Permite el acceso funcional a la computadora. Favorece la autonomía.',
   ARRAY['No logra usar mouse convencional','No entiende los comandos','Le cuesta orientarse en el espacio','Le cuesta identificar los botones','Le cuesta controlar el movimiento','Necesita movimientos más amplios','Se frustra con dispositivos pequeños'],
   ARRAY['Uso de computadora adaptada','Actividades digitales','Tareas de acceso al dispositivo','Trabajo autónomo con tecnología'],
   ARRAY['Accesibilidad tecnológica'],
   ARRAY['discapacidad intelectual','TEA','discapacidad visual','discapacidad motora'],
   ARRAY['Síndrome de Down','TEA con mayor necesidad de apoyo','TEA con apoyo notable','multidiscapacidad','baja visión','parálisis cerebral']);

-- 5) Backfill de los 18 productos existentes con sus manifestaciones / situaciones / categorías
-- (extraídos de la Matriz General — ver Apéndice A para todo el detalle).
-- Sólo se muestran 3 ejemplos abajo; el archivo final tendrá un UPDATE por cada uno.

UPDATE devices SET
  observable_manifestations = ARRAY['Le cuesta leer textos largos','Evita escribir a mano','Se cansa al escribir','Le cuesta copiar del pizarrón','Tarda mucho en hacer tareas escritas','Necesita apoyo para acceder al contenido'],
  pedagogical_situations = ARRAY['Actividades de lectura digital','Producción escrita','Uso de aplicaciones educativas','Trabajo autónomo'],
  material_class = ARRAY['Acceso al aprendizaje','Accesibilidad tecnológica'],
  frequent_profile = ARRAY['DEA','discapacidad intelectual','TEA','altas capacidades','altas necesidades de apoyo','discapacidad visual','discapacidad auditiva','discapacidad motora'],
  specific_profile = ARRAY['Dislexia','disgrafía','discalculia','síndrome de Down','TEA con apoyo leve','baja visión','hipoacusia','parálisis cerebral']
  WHERE name = 'Tablet educativa (10")';

UPDATE devices SET
  observable_manifestations = ARRAY['se distrae fácilmente con los ruidos','le molestan los sonidos del aula','se desconcentra con facilidad','no logra concentrarse cuando hay ruido','se tapa los oídos','se pone nervioso o incómodo con ciertos sonidos','pierde el foco durante la tarea','le cuesta terminar actividades por distracción','necesita silencio para poder trabajar','presenta sensibilidad al sonido','se sobrecarga con estímulos auditivos'],
  pedagogical_situations = ARRAY['Durante lectura individual','Evaluaciones','Trabajo autónomo','Actividades que requieren concentración','Momentos de sobreestimulación sensorial'],
  material_class = ARRAY['Regulación, atención'],
  frequent_profile = ARRAY['DEA','discapacidad intelectual','TEA','altas capacidades','altas necesidades de apoyo','discapacidad motora'],
  specific_profile = ARRAY['Dislexia','síndrome de Down','TEA con apoyo leve','TEA con apoyo notable','TEA con mayor necesidad de apoyo','alto potencial intelectual','multidiscapacidad','parálisis cerebral','TDAH']
  WHERE name = 'Auriculares cancelacion de ruido';

-- ... (resto de UPDATEs en Apéndice A)

-- 6) Marcar como inactivo el viejo Teclado CLEVY si quedó como registro distinto
-- (no aplica si la fila se reemplazó in-place arriba)

COMMIT;
```

> **Nota:** este SQL es la versión "esqueleto + 5 ejemplos completos". Los UPDATEs de los 18 productos existentes y los INSERTs largos viven en el Apéndice A para no inflar este capítulo. La intención es que el archivo de migración real pegue todos los UPDATEs/INSERTs juntos.

### 3.4 Decisiones pendientes (validar antes de correr)

| # | Decisión | Quién valida | Bloquea |
|---|---|---|---|
| 1 | Pelota antiestrés y Soporte flexible: ¿se mantienen aunque no estén en el Listado FINAL? | Anabela | Migración |
| 2 | Teclado CLEVY ¿se reemplaza por Admouse o coexisten? | Anabela | Migración |
| 3 | Auriculares (con micrófono) vs Auriculares (sin micrófono) — ¿son el mismo objeto o dos? | Anabela | Migración |
| 4 | Metadata de productos para zurdos (sacapuntas, lapicera, tijera) | Mercedes | Calidad de recomendación, no bloqueante |
| 5 | Imágenes (`image_url`) para los 16 productos nuevos | Diseño | Frontend, no bloqueante |

---

## 4. Matriz manifestación → producto

### 4.1 Cómo se usa

La idea: cuando el docente escribe **"a Lucía se le cae el lápiz y hace mucha fuerza al escribir"**, el LLM no tiene que adivinar — busca en el catálogo qué productos tienen esas frases (o frases parecidas) en `observable_manifestations` y razona sobre ese subconjunto.

Dos estrategias posibles:

**A. Embebido en el prompt (MVP).** El catálogo enviado al LLM incluye `observable_manifestations` por producto. El modelo razona en lenguaje natural y matchea por similitud semántica. Bajo esfuerzo, alta cobertura.

**B. Tool de lookup explícito (V1).** El LLM, antes de proponer dispositivo, llama a una tool `lookup_by_manifestation(text)` que devuelve los productos cuyas `observable_manifestations` matchean (por embeddings o por keyword). Más costoso pero más auditable y resistente a alucinación.

**Decisión MVP:** estrategia A. La B se evalúa cuando tengamos métricas de la A.

### 4.2 Tabla compacta (vista global)

Tabla pivote — eje Y: manifestación, eje X: producto. Apéndice A tiene la versión completa. Acá mostramos el patrón:

| Manifestación | Productos sugeridos (ramp) |
|---|---|
| "Se le cae el lápiz" / "Sostiene mal el lápiz" | Soporte para lápiz (etapas 1–4), Pesas para lápices [Didáctico] |
| "Mueve mucho la mano al escribir" / "trazo inestable" | Pesas para lápices, Muñequera sensorial [Sensorial] |
| "Le cuesta usar la tijera" | Tijera adaptada etapa 1 / etapa 2 [Didáctico] |
| "Salta palabras" / "se desorienta en el texto" | Ayudas para lectura etapas 1–4 [Didáctico] |
| "Se inquieta constantemente" / "necesita manipular objetos" | SPEKS, SPEKS textura [Sensorial] |
| "Mueve las piernas" / "no logra quedarse sentado" | Pelota pie/muslo, BouncyBand, Patas de silla, Banda elástica [Sensorial] |
| "Se distrae con ruidos" / "le molestan los sonidos" | Auriculares cancelación, Auriculares con micrófono [Sensorial/Digital] |
| "Se distrae con lo que sucede alrededor" | Panel separador, Mesa plegable portátil [Didáctico] |
| "Olvida lo que tiene que hacer" / "no sabe por dónde empezar" | Organizador de tareas [Didáctico] |
| "No gestiona bien el tiempo" / "no termina en el tiempo previsto" | Time timer [Didáctico] |
| "No puede usar mouse / teclado convencional" | Mouse Admouse, Mouse trackball, Pulsador USB, Teclado Admouse [Digital] |
| "No distingue bien las teclas" | Stickers contraste, Teclado Admouse [Digital] |
| "Le cuesta leer solo" / "necesita escuchar para entender" | Pen reader, Auriculares, Tablet [Digital/Didáctico] |

### 4.3 Reglas de priorización

Cuando varias opciones aplican, Alizia debe ordenar por:
1. **Especificidad de la manifestación** — un producto con match exacto en su `observable_manifestations` gana sobre uno con match parcial.
2. **Mínima intervención que resuelva** — preferir etapa más alta (más simple) que cubra el caso. Solo escalar si es insuficiente.
3. **Compatibilidad con la actividad descrita** — si el docente dice "estoy haciendo dictado", priorizar productos cuya `pedagogical_situations` incluya escritura/dictado/copia.
4. **Material clase** — preferir "Acceso al aprendizaje" (resuelve la tarea) antes que "Regulación" (resuelve el contexto). Sólo si no hay match en acceso, ir a regulación.
5. **Disponibilidad** — `quantity > 0` y `active = true`.

---

## 5. Arquitectura del asistente

### 5.1 Modos de uso (foco en asistencia)

El PRD original define 4 modos: **asistencia en clase**, planificación, escaneo QR, onboarding. **Este sprint sólo se diseña en detalle el modo asistencia** (la URL `/inclusion/asistencia`). Los otros modos quedan apenas esquematizados (sección 11 del roadmap).

### 5.2 Flujo escalonado (general → específico)

Mercedes fue muy clara en la reunión 29-04: **el docente no quiere que el sistema pida 5 datos antes de devolverle algo útil**. La respuesta inicial puede ser general; se afina iterativamente.

```
Turno 1 (docente) — situación cruda, sin nombres
  Ej: "tengo una clase muy inquieta, no me prestan atención"
  ↓
Turno 1 (Alizia)
  - Reconoce + 2-3 sugerencias generales accionables
  - Pregunta por foco (¿hay alguien en particular?)
  - NO recomienda dispositivo todavía si no hay alumno claro
  ↓
Turno 2 (docente) — menciona alumno o describe manifestación específica
  Ej: "sobre todo Mateo, no para de moverse"
  ↓
Turno 2 (Alizia)
  - Llama tool identify_student("Mateo") → student_id
  - Llama tool propose_device(student_id, manifestation, activity_context) → device + justificación
  - Ofrece adaptación pedagógica si aplica
```

**Regla suave (no rígida):** Alizia *prefiere* tener alumno identificado antes de recomendar dispositivo, pero si la manifestación es muy específica y única (ej: "no puede agarrar el lápiz") puede recomendar igual y mencionar "esto sirve para cualquier estudiante que…".

### 5.3 Composición del prompt madre

El prompt se construye en 5 bloques concatenados:

```
[A] IDENTIDAD Y VOZ          (estable, ~600 tokens)
[B] PRINCIPIOS PEDAGÓGICOS   (estable, ~800 tokens — los 14 lineamientos resumidos)
[C] MARCO DUA                (estable, ~300 tokens)
[D] CATÁLOGO ENRIQUECIDO     (dinámico desde DB, ~3000-4000 tokens)
[E] CONTEXTO DE SESIÓN       (dinámico, ~500-1000 tokens)
   - alumnos del curso con perfiles
   - historial reciente
   - alumno actualmente identificado (si lo hay)
```

Total ~6000-7000 tokens de system prompt. Holgado para gpt-5-mini (128k context).

### 5.4 Tool calling vs tags por regex

**Hoy (regex):**
- Modelo emite `[STUDENT_ID:3]` como string
- Backend regex extrae 3
- Frágil: si modelo escribe `[STUDENT_ID: 3]` (con espacio), `[Student_ID:3]`, o lo omite, falla silenciosamente

**Propuesta (tools):**
- Modelo invoca `identify_student(name="Mateo")` como tool call
- Backend ejecuta la lookup, devuelve `{id: 3, name: "Mateo López", profile: {...}}`
- Modelo recibe el resultado y lo incorpora a su próxima respuesta
- Audit trail completo (qué tools llamó, con qué args, qué devolvieron)
- Más confiable, más fácil de testear

---

## 6. Prompt madre + 3 tools

### 6.1 System prompt completo (versión MVP)

```
# IDENTIDAD
Sos Alizia, asistente de inclusión educativa de Educabot. Acompañás a docentes
de aula a remover barreras al aprendizaje y la participación, integrando
dispositivos de la Valija Adaptativa con adaptaciones pedagógicas concretas.

# VOZ
- Español rioplatense, vos.
- Cálida, profesional, directa. Sin paternalismos.
- Sin jerga clínica (no digas "TDAH", "dislexia", "TEA"). Hablá de
  manifestaciones observables: "le cuesta sostener la atención", "necesita
  apoyo para leer", "se distrae con el ruido del aula".
- Brevedad: el docente está en el aula. Máximo 4-6 oraciones por turno
  salvo que el docente pida más detalle.
- Nunca des una lista de más de 3 sugerencias en un turno.

# PRINCIPIOS (te guían siempre)
1. Entrada pedagógica, no clínica. Partís de lo que el docente OBSERVA, no
   de diagnósticos.
2. Remoción de barreras. Tu objetivo es eliminar obstáculos, no etiquetar
   alumnos.
3. Universalidad con foco. Lo que proponés sirve para todo el grupo,
   priorizando a quien tiene mayor barrera.
4. Acceso multimodal (DUA). Considerá vías visual, oral, manipulativa,
   temporal, tecnológica.
5. Respuesta accionable AHORA. El docente está en el aula. Tu sugerencia
   se aplica en menos de 5 minutos.
6. Diferenciación pedagógica. Cuando proponés una adaptación de actividad,
   sugerís 3 niveles (bajo/medio/alto) sobre la misma tarea.
7. Coherencia. 1-3 acciones máximo, ordenadas por impacto.

# DISTINCIÓN CLAVE — material vs pedagógica
Hay DOS tipos de adaptación:
  - ADAPTACIÓN DE MATERIAL: usar un dispositivo de la Valija (ej:
    "ofrecele el SPEKS"). Tool: propose_device.
  - ADAPTACIÓN PEDAGÓGICA: cambiar la consigna/tarea/entorno (ej: "dividí
    el dictado en 3 niveles"). Tool: propose_pedagogical_adaptation.
Muchas veces conviene combinar las dos.

# LÍMITES
NO hacés:
  - Diagnósticos clínicos
  - Tratamientos terapéuticos
  - Informes clínicos
  - Reemplazar al docente, psicopedagogo, maestra integradora ni
    acompañante terapéutico

# FLUJO
Si el docente describe una situación SIN mencionar alumno:
  1. Reconocé brevemente lo que está pasando.
  2. Da 1-2 sugerencias generales accionables.
  3. Preguntá quién está pasando por esto.
  4. NO llames propose_device todavía.

Si el docente menciona alumno (aun por apodo o de forma parcial):
  1. Llamá identify_student. Sé flexible: "Valen"≈"Valentina", "Mati"≈"Matías".
  2. Si el match es razonable, NO pidas confirmación, segui adelante.
  3. Si hay ambigüedad real (dos alumnos posibles), preguntá.
  4. Si el alumno no existe en el curso, decilo claramente y ofrecé seguir
     con consejos generales.

Cuando ya identificaste al alumno y entendés la manifestación:
  1. Llamá propose_device con la justificación pedagógica (qué manifestación
     atendés, por qué este producto).
  2. Si la actividad lo amerita, también llamá propose_pedagogical_adaptation
     con 3 niveles.
  3. Resumí en lenguaje del docente: qué le pasa, qué probás primero, qué
     dispositivo, qué hacer si no funciona.

# CATÁLOGO DE DISPOSITIVOS
{devices_catalog_json}
  - Para cada dispositivo conocés: name, ramp, description, function_summary,
    observable_manifestations, pedagogical_situations, material_class,
    how_to_use, recommendations, rationale, classroom_benefit, stage, quantity.
  - Cuando matcheas la situación del docente contra un dispositivo, buscás
    similitud con observable_manifestations y pedagogical_situations.

# ALUMNOS DEL CURSO
{students_context_json}
  - id, name, perfil (transitorio?, dificultades en lenguaje natural,
    descripción libre del docente).
  - Hay 25 alumnos pero solo algunos tienen perfil cargado. Los que no
    tienen perfil son alumnos para los que el docente todavía no relevó
    necesidades — no asumas nada de ellos.

# HISTORIAL DE LA CONVERSACIÓN
Te paso los últimos 10 mensajes. Si ya recomendaste algo, NO repitas la
recomendación; encadená sobre lo dicho.
```

### 6.2 Tool 1 — `identify_student`

**Propósito:** dado un nombre/apodo/descripción, devolver el alumno del curso que mejor matchea.

```json
{
  "type": "function",
  "function": {
    "name": "identify_student",
    "description": "Identifica un alumno del curso a partir de un nombre, apodo o descripción parcial mencionados por el docente. Devuelve el alumno con mejor match o una lista corta de candidatos si hay ambigüedad.",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "El nombre, apodo o descripción tal como lo escribió el docente. Ej: 'Mateo', 'Valen', 'el chico que se sienta adelante'."
        }
      },
      "required": ["query"]
    }
  }
}
```

**Implementación backend (pseudocódigo):**
```python
def identify_student(query: str, course_id: int) -> dict:
    # 1. Normalizar query (lowercase, sin acentos)
    # 2. Buscar matches por:
    #    a. nombre exacto
    #    b. nombre que empiece con query
    #    c. nombre que contenga query
    #    d. apodos comunes (Valen→Valentina, Mati→Matías, Nico→Nicolás, etc.)
    # 3. Si match único: devolver alumno + perfil
    # 4. Si múltiples: devolver hasta 3 candidatos
    # 5. Si ninguno: { "matches": [], "suggestion": "no encontré ese alumno" }
    return {
      "matches": [
        { "id": 2, "name": "Mateo López", "profile": {...} }
      ]
    }
```

**Cómo lo usa el modelo:** después de la llamada, recibe `{"matches": [...]}` y arma su próxima respuesta sabiendo a quién referirse.

### 6.3 Tool 2 — `propose_device`

**Propósito:** registrar y devolver una recomendación de dispositivo justificada. El backend lo usa para enviar la card al frontend.

```json
{
  "type": "function",
  "function": {
    "name": "propose_device",
    "description": "Propone un dispositivo de la Valija Adaptativa para un alumno y situación específicos. Devolver siempre con justificación pedagógica clara (qué manifestación atiende, por qué este producto vs otros).",
    "parameters": {
      "type": "object",
      "properties": {
        "device_id": { "type": "integer" },
        "student_id": { "type": "integer", "nullable": true,
          "description": "Si la sugerencia es genérica (sin alumno identificado), pasar null." },
        "manifestation_observed": { "type": "string",
          "description": "La manifestación que observa el docente, en sus palabras o reformulada." },
        "activity_context": { "type": "string", "nullable": true,
          "description": "Qué actividad estaba haciendo el alumno (escritura, lectura, recorte, escucha, etc.)." },
        "rationale": { "type": "string",
          "description": "Por qué este dispositivo en 1-2 oraciones, en lenguaje del docente." },
        "alternatives": { "type": "array", "items": { "type": "integer" },
          "description": "device_ids de alternativas si esta no funciona. Máx 2." }
      },
      "required": ["device_id", "manifestation_observed", "rationale"]
    }
  }
}
```

**Implementación backend:**
- Valida que `device_id` exista y esté `active`.
- Si `student_id`, lo loguea (futuro: tabla `device_recommendations` para feedback).
- Devuelve el `Device` completo para que el frontend renderice la card.

### 6.4 Tool 3 — `propose_pedagogical_adaptation`

**Propósito:** generar una adaptación pedagógica en 3 niveles para una actividad. Es lo que Mercedes llamó "diferenciación estructurada".

```json
{
  "type": "function",
  "function": {
    "name": "propose_pedagogical_adaptation",
    "description": "Genera una adaptación pedagógica con 3 niveles (básico/medio/avanzado) para la actividad descrita por el docente. Sirve para responder a la diversidad del aula sin ofrecer 25 propuestas individuales.",
    "parameters": {
      "type": "object",
      "properties": {
        "activity": {
          "type": "string",
          "description": "Descripción breve de la actividad a adaptar (ej: 'dictado de 5 oraciones', 'lectura comprensiva del cuento X')."
        },
        "subject": { "type": "string", "nullable": true,
          "description": "Asignatura si se mencionó." },
        "levels": {
          "type": "array",
          "minItems": 3, "maxItems": 3,
          "items": {
            "type": "object",
            "properties": {
              "label": { "type": "string", "enum": ["básico", "medio", "avanzado"] },
              "task": { "type": "string", "description": "Qué hace el alumno." },
              "support": { "type": "string", "nullable": true,
                "description": "Apoyos sugeridos (material de la valija, presencia del acompañante, etc.)." }
            },
            "required": ["label", "task"]
          }
        },
        "rationale": { "type": "string",
          "description": "Cómo esta diferenciación responde a la diversidad observada en la clase." }
      },
      "required": ["activity", "levels", "rationale"]
    }
  }
}
```

**Implementación backend:** registra la adaptación (futuro: persistir para que el docente la recupere) y devuelve el bloque para que el frontend lo renderice como card de "Adaptación pedagógica".

### 6.5 Comportamiento esperado por turno (resumen)

| Input docente | Tools que llama Alizia | Outputs esperados |
|---|---|---|
| "tengo una clase muy inquieta" | (ninguna) | Texto + 1-2 sugerencias generales + pregunta |
| "Mateo no se queda quieto" | `identify_student("Mateo")` → match | Texto + tal vez `propose_device` (BouncyBand, Pelota pie) |
| "quiero hacer un dictado, ¿cómo lo adapto?" | `propose_pedagogical_adaptation(...)` | Texto + card con 3 niveles |
| "a Lucía se le cae el lápiz" | `identify_student("Lucía")` + `propose_device(Soporte lápiz etapa 4, ...)` | Texto + StudentCard + DeviceCard |
| "mostrame todos los productos para escritura" | (ninguna en MVP — texto explicativo) | Lista textual con 3-4 productos referenciados |

---

## 7. Cambios al backend

### 7.1 Migración de DB
- `migrations/010_devices_update.sql` — ya descripto en sección 3.3.

### 7.2 Refactor del endpoint `/inclusion/assist`

```
main.py:3755 — reescribir handler
```

Cambios:
1. **Aceptar `course_id` como query param** (default 1 para retro-compatibilidad).
2. **Construir el catálogo enriquecido** con todos los campos del producto (description, function_summary, observable_manifestations, pedagogical_situations, how_to_use, recommendations, rationale, classroom_benefit, stage).
3. **Construir el contexto de alumnos** con `is_transitory`, `difficulties`, `free_description`.
4. **Reemplazar regex por function calling**: usar la API de tools de Azure OpenAI (`tools=[...]`, `tool_choice="auto"`).
5. **Loop de tool calling** hasta que el modelo deje de invocar tools (max 5 iteraciones para evitar runaway).
6. **Devolver al frontend** un objeto extendido:

```python
class AssistResponse(BaseModel):
    response: str                                    # texto final del modelo
    identified_student: Optional[Student] = None     # si llamó identify_student
    device: Optional[Device] = None                  # si llamó propose_device
    pedagogical_adaptation: Optional[Adaptation] = None  # si llamó propose_pedagogical_adaptation
    tool_calls: list[dict]                           # audit trail
```

### 7.3 Helpers nuevos

```python
def build_devices_catalog(devices: list[Device]) -> str:
    """JSON compacto pero completo del catálogo para incluir en el prompt."""

def find_student_match(query: str, students: list[Student]) -> list[Student]:
    """Lookup flexible para identify_student: exact, prefix, contains, apodos."""

def execute_tool_call(name: str, args: dict, ctx: SessionCtx) -> dict:
    """Dispatcher para las 3 tools. Devuelve el dict que se le pasa al modelo."""
```

### 7.4 Lo que NO cambia en MVP
- `/inclusion/recommend` (endpoint distinto, modo planificador). Queda igual.
- Tablas `student_inclusion_profiles`, `inclusion_plans`, `device_usage_logs`.
- `/courses/{id}/inclusion-students`, `/students/{id}/inclusion-profile`.

---

## 8. Cambios al frontend

### 8.1 Cards adicionales en `InclusionAsistencia.tsx`

Hoy se renderiza `StudentMiniCard` y `DeviceCard`. Agregar:

- **`PedagogicalAdaptationCard`** — para mostrar los 3 niveles de adaptación. Diseño tipo accordion o steps horizontales.
- **`ToolCallChip`** (opcional, dev-mode) — chip pequeño cuando una tool se ejecutó, p.ej. "🔍 Identifiqué a Mateo López". Útil para entender qué hace el agente.

### 8.2 Tipo `InclusionAssistResponse` extendido

```ts
type InclusionAssistResponse = {
  response: string;
  identified_student: InclusionStudent | null;
  device: Device | null;
  pedagogical_adaptation: PedagogicalAdaptation | null;
  tool_calls?: ToolCall[];   // dev mode only
};

type PedagogicalAdaptation = {
  activity: string;
  subject?: string;
  levels: { label: 'básico'|'medio'|'avanzado'; task: string; support?: string }[];
  rationale: string;
};
```

### 8.3 Lo que NO cambia en MVP
- Layout general, estilos, transiciones.
- Speech-to-text (ya funciona).
- Modal de detalle del dispositivo.

### 8.4 Mejoras V1 (ya planeadas)
- Botón de feedback (👍/👎/✏️) por respuesta para alimentar `device_usage_logs`.
- Botón "Crear perfil de alumno" cuando el docente menciona uno que no existe.
- Sugerencia "¿querés mandarle esto a la familia?" tras una recomendación de dispositivo (prolongación fuera del aula).

---

## 9. MVP recortado — qué hacemos primero

### 9.1 Definición de MVP

| # | Entregable | Responsable | Esfuerzo |
|---|---|---|---|
| 1 | Validación con Anabela/Mercedes de las 5 decisiones pendientes (ver §3.4) | Producto | 1 día |
| 2 | Migración SQL `010_devices_update.sql` con los 34 productos completos | Dev | 0.5 día |
| 3 | Reescritura de `ASSIST_SYSTEM_PROMPT` (sección 6.1) | Dev | 0.5 día |
| 4 | Implementación de las 3 tools en `main.py` | Dev | 1 día |
| 5 | Refactor de `/inclusion/assist` con tool calling loop | Dev | 1 día |
| 6 | `PedagogicalAdaptationCard` + tipos extendidos en frontend | Dev | 0.5 día |
| 7 | `docs/situaciones-de-prueba.md` con 20 casos | Mercedes + Dev | 1 día |
| 8 | `tests/test_assistant_situations.py` (esqueleto, parser MD, LLM-as-judge) | Dev | 1 día |
| 9 | Pasar los 20 casos y revisar respuestas | Equipo | 1 día |
| 10 | Documentación de qué respuesta se considera "buena" para futuras iteraciones | Mercedes | 0.5 día |

**Total estimado:** ~7 días-persona. Plausible en una semana del equipo.

### 9.2 Lo que NO entra en MVP (queda para V1)

- Tools adicionales (`lookup_by_manifestation`, `create_student_profile`, `register_use_outcome`, `suggest_external_use`, `explain_inclusion_concept`).
- Feedback post-clase (👍/👎).
- Creación de alumno desde el chat.
- Sugerencia de prolongación fuera del aula.
- Accesibilidad UI (modos baja visión / dislexia).
- Soporte multi-curso (`course_id` queda como query param pero seguimos demoando con course 1).
- Persistencia de adaptaciones pedagógicas generadas.
- Modos planificación / QR / onboarding / Inclusión 101 (ya hay una entrada de QR pública para la ficha del dispositivo, no se toca).

### 9.3 Métricas de éxito MVP

- **Calidad de identificación:** sobre 20 casos, 18+ identifican correctamente al alumno (90%).
- **Calidad de recomendación:** sobre 20 casos, 17+ recomiendan un dispositivo "correcto o aceptable" según juicio de Mercedes (85%).
- **Tono:** 0 respuestas con jerga clínica explícita en el corpus de prueba.
- **Latencia:** p95 < 8 segundos por turno (gpt-5-mini con ~6k tokens de prompt).
- **Robustez de tool calling:** 0 fallos por tags malformados (regla viva: ya no usamos tags).

---

## 10. Casos de prueba

Documento aparte: `docs/situaciones-de-prueba.md`.

**Estructura propuesta** (cada caso es una sección Markdown con front-matter):

```markdown
## Caso 04 — Manifestación motriz, alumna identificada
status: validated-by-mercedes
tags: [motricidad-fina, escritura, identificacion-flexible]

**Setup**
- course_id: 1
- alumna en perfil: Lucía Fernández (motricidad fina)

**Turno 1 — Docente:**
> "A Lu se le cae el lápiz y se cansa rapidísimo en el dictado"

**Turno 1 — Esperado:**
- identify_student("Lu") → Lucía Fernández (id=1)
- propose_device(Soporte para lápiz etapa 4, manifestation="se le cae el lápiz, se cansa al escribir", activity="dictado")
- Respuesta textual reconoce la situación + ofrece tip de uso (poner el soporte en el lápiz, validar postura)
- NO menciona "disgrafía" ni "TDAH"
```

20 casos iniciales (10 de los del documento de Mercedes + 10 sintéticos cubriendo edge cases):
- 4 casos motricidad / escritura (Soporte lápiz, Tijera, Pesas)
- 3 casos lectura (Ayudas para lectura, Pen reader)
- 4 casos atención / regulación (SPEKS, Time timer, Auriculares cancelación)
- 2 casos movilidad sentado (Pelota pie, BouncyBand, Banda)
- 2 casos acceso digital (Mouse Admouse, Pulsador, Stickers)
- 2 casos identificación ambigua (dos alumnos con el mismo apodo, alumno no existente)
- 2 casos "general → afina" (docente sin alumno identificado, después afina)
- 1 caso adaptación pedagógica sin dispositivo (`propose_pedagogical_adaptation` solo)

### 10.1 Harness Python (esqueleto)

`tests/test_assistant_situations.py`:

```python
"""
Harness para correr los casos de docs/situaciones-de-prueba.md contra
/inclusion/assist y evaluar las respuestas con LLM-as-judge.
"""
import re
import json
import httpx
from pathlib import Path

CASES_FILE = Path(__file__).parent.parent / "docs" / "situaciones-de-prueba.md"
ASSIST_URL = "http://localhost:8000/inclusion/assist"
JUDGE_MODEL = "gpt-5-mini"

def parse_cases(md: str) -> list[dict]:
    """Parsea el markdown y devuelve los casos como lista de dicts."""
    # heurística simple: split por '## Caso ', extraer secciones
    ...

def run_case(case: dict) -> dict:
    """Ejecuta los turnos de un caso contra /inclusion/assist."""
    history = []
    actual = []
    for turn in case["turns"]:
        resp = httpx.post(ASSIST_URL, json={"message": turn["docente"], "history": history})
        actual.append(resp.json())
        history.append({"role": "user", "content": turn["docente"]})
        history.append({"role": "assistant", "content": resp.json()["response"]})
    return actual

def judge(expected: dict, actual: dict) -> dict:
    """LLM-as-judge: ¿la respuesta cumple con lo esperado?"""
    prompt = f"""..."""  # rúbrica clara
    ...

def main():
    md = CASES_FILE.read_text()
    cases = parse_cases(md)
    results = []
    for case in cases:
        actual = run_case(case)
        verdict = judge(case["expected"], actual)
        results.append({"case": case["id"], "verdict": verdict})
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
```

Esto se afina cuando arranquemos a codear. La forma final del MD y del parser deben ir alineados.

---

## 11. Roadmap post-MVP

### V1 (siguiente sprint)

- **Tools adicionales:**
  - `create_student_profile(name, manifestations[], is_transitory)` — el docente puede dar de alta un alumno desde el chat.
  - `register_use_outcome(device_id, student_id, outcome)` — feedback post-clase.
  - `lookup_by_manifestation(text)` — búsqueda explícita en el catálogo (en lugar de razonamiento embebido).
  - `suggest_external_use(student_id, device_id)` — prolongación fuera del aula (familia / terapia).
  - `explain_inclusion_concept(topic)` — Inclusión 101 inline (qué es DUA, qué es PPI, etc.).
- **Feedback loop:** botón 👍/👎/✏️ por respuesta. Guarda en `device_usage_logs` con `action='feedback'` y context.
- **Matriz de manifestaciones** vista al usuario: el docente puede explorar "qué productos hay para X situación".
- **Personalización por institución:** si el cliente desactivó algunos dispositivos (no los compró), el catálogo respeta `active=false` por institución (requiere tabla `institution_devices`).

### V2 (mediano plazo)

- **Modos diferenciados** con sub-prompts: planificación de clase, escaneo QR (ya existe la página, falta integrar al asistente), onboarding de valija, Inclusión 101.
- **Accesibilidad UI:** modos baja visión, dislexia, tamaños de fuente, contraste alto. Mercedes lo planteó como un requisito propio.
- **PPI integrado:** subir documento PPI del alumno, Alizia lo lee y propone adaptaciones alineadas con los acuerdos firmados.
- **Acompañante terapéutico:** rol nuevo, articulación de tareas entre docente y AT desde el chat.
- **Soporte multi-curso real** + onboarding de docente (qué es la valija, qué hay adentro).

### V3 (largo plazo)

- Dashboard para ministerio: trazabilidad de uso, qué productos se usan más, qué situaciones aparecen más, etc.
- Sistema NFC en la valija (detección de qué dispositivos están disponibles físicamente).
- Red de experiencias colaborativas entre docentes ("a mí me funcionó esto con un caso parecido").
- API para vincular con Tuni, Tich u otros productos del ecosistema.

---

## Apéndice A — Manifestaciones, situaciones y categorías por producto

Tabla maestra que hay que cargar en la migración (UPDATE para los 18 existentes + INSERT para los 16 nuevos). Una fila por producto.

| # | Producto | Rampa | Etapa | Categoría material | Manifestaciones (tope 6) | Situaciones pedagógicas |
|---|---|---|---|---|---|---|
| 1 | Tijera adaptada — etapa 1 | Didáctico | 1 | Acceso al aprendizaje | Le cuesta usar la tijera; corta con dificultad; no logra seguir línea; evita recorte; se cansa rápido; necesita ayuda | Recorte; trabajos manuales; motricidad fina |
| 2 | Tijera adaptada — etapa 2 | Didáctico | 2 | Acceso al aprendizaje | No puede usar tijera convencional; movimientos bruscos; no sostiene tijera; no puede usar las manos | Recorte; trabajos manuales; tareas guiadas |
| 3 | Soporte para lápiz 1 — etapa 4 | Didáctico | 4 | Acceso al aprendizaje | Sostiene mal el lápiz; hace mucha fuerza; se le cae; se cansa rápido; letra poco legible; le cuesta controlar el trazo | Escritura; copia; producción escrita; grafomotricidad |
| 4 | Soporte para lápiz 2 — etapa 3 | Didáctico | 3 | Acceso al aprendizaje | (idem 3) | (idem 3) |
| 5 | Soporte para lápiz 3 — etapa 2 | Didáctico | 2 | Acceso al aprendizaje | (idem 3) | (idem 3) |
| 6 | Soporte para lápiz 4 — etapa 1 | Didáctico | 1 | Acceso al aprendizaje | (idem 3) | (idem 3) |
| 7 | Pesas para lápices | Didáctico | — | Regulación, atención | Mueve mucho la mano; trazo inestable; movimientos bruscos; le cuesta controlar el lápiz; cambia posición | Escritura; tareas de precisión; trabajos prolongados; copia o dictado |
| 8 | Muñequera sensorial x2 | Sensorial | — | Regulación, atención | (idem 7) | (idem 7) |
| 9 | SPEKS | Sensorial | — | Regulación, atención | Se inquieta; necesita manipular; lleva objetos a la boca; se muerde uñas; le cuesta quedarse quieto; busca estímulos manuales | Concentración; clase expositiva; trabajo autónomo; ansiedad |
| 10 | SPEKS con textura | Sensorial | — | Regulación, atención | (idem 9) | (idem 9) |
| 11 | Pelota pie/muslo | Sensorial | — | Regulación, atención | Mueve las piernas; se levanta; no se queda sentado; necesita moverse mientras trabaja; se inquieta | Trabajo en mesa; actividades largas; permanencia sentado |
| 12 | Banda elástica Bouncyband | Sensorial | — | Regulación, atención | Se balancea; se levanta seguido; mueve el cuerpo; le cuesta permanecer; interrumpe por movimiento | Trabajo en mesa; actividades largas; permanencia sentado |
| 13 | BouncyBand Sit & Twist Cojín | Sensorial | — | Regulación, atención | (idem 12) | Pupitre; trabajo prolongado; escucha |
| 14 | Patas de silla x4 | Sensorial | — | Regulación, atención | (idem 12) | Pupitre; trabajo prolongado; escucha |
| 15 | Ayuda lectura — ajustable etapa 1 | Didáctico | 1 | Acceso, atención | Le cuesta leer palabras; salta palabras; se desorienta; lee lento; se cansa; le cuesta segmentar | Lectura; comprensión lectora; trabajo individual con textos; copia |
| 16 | Ayuda lectura — fijo 2 palabras etapa 2 | Didáctico | 2 | Acceso, atención | (similar a 15) | (idem 15) |
| 17 | Ayuda lectura — guiada etapa 3 | Didáctico | 3 | Acceso, atención | Salta línea; se desorienta; lee lento; se cansa; mucha dificultad para seguir | (idem 15) |
| 18 | Ayuda lectura — transparente con renglón etapa 4 | Didáctico | 4 | Acceso, atención | (idem 17) | (idem 15) |
| 19 | Panel separador de pupitre | Didáctico | — | Adaptación entorno | Se distrae con el entorno; pierde foco; le cuesta concentrarse; pierde atención; le molesta el entorno | Trabajo individual; concentración sostenida; sobrecarga; tareas complejas |
| 20 | Sacapuntas para zurdos | Didáctico | — | Acceso (zurdos) | (TBD con Mercedes) | (TBD) |
| 21 | Lapicera para zurdos | Didáctico | — | Acceso (zurdos) | (TBD) | (TBD) |
| 22 | Tijera para zurdos | Didáctico | — | Acceso (zurdos) | (TBD) | (TBD) |
| 23 | Organizador de tareas | Didáctico | — | Organización, regulación | Olvida lo que tiene que hacer; no sabe por dónde empezar; deja sin terminar; se desorganiza; pierde materiales | Inicio de actividad; planificación; trabajos por etapas |
| 24 | Time timer | Didáctico | — | Organización, regulación, atención | No gestiona el tiempo; le cuesta empezar; no termina a tiempo; se pone ansioso con cambios; necesita saber cuánto falta | Inicio de actividad; planificación; trabajos por etapas |
| 25 | Mesa plegable portátil | Didáctico | — | Adaptación entorno, regulación | Se distrae; pierde foco; le cuesta concentrarse; se sobreestimula; busca lugares tranquilos | Inicio de tarea; tiempo limitado; transiciones; trabajo individual |
| 26 | Tablet 10" Android | Digital | — | Acceso, accesibilidad tecnológica | Le cuesta leer textos largos; evita escribir a mano; se cansa al escribir; tarda en hacer tareas escritas; necesita apoyo para acceder al contenido | Lectura digital; producción escrita; apps educativas; trabajo autónomo |
| 27 | Auriculares (con micrófono) | Digital | — | Acceso, accesibilidad tecnológica | Le cuesta leer solo; necesita escuchar para entender; se cansa al leer; le cuesta escribir sin ayuda | Lectura asistida; comandos por voz; trabajo con dispositivos |
| 28 | Mouse trackball | Digital | — | Accesibilidad tecnológica | Le cuesta usar el mouse; mueve demasiado el cursor; no logra precisión; se frustra con la computadora | Computadora/tablet; actividades digitales; navegación |
| 29 | Mouse Admouse | Digital | — | Accesibilidad tecnológica | No logra usar mouse convencional; no entiende los comandos; le cuesta orientarse; le cuesta identificar botones; se frustra con dispositivos pequeños | Computadora adaptada; actividades digitales |
| 30 | Teclado Admouse | Digital | — | Acceso, accesibilidad tecnológica | Se equivoca al escribir; no encuentra las teclas; escribe lento; evita escribir; aprieta fuerte | Producción escrita digital; actividades de escritura; teclado |
| 31 | Stickers contraste teclado | Digital | — | Acceso, accesibilidad tecnológica | No distingue bien las teclas; se confunde al escribir; tarda en encontrar letras; necesita apoyo visual | Escritura digital; uso del teclado |
| 32 | Pulsador botón USB | Digital | — | Accesibilidad tecnológica | No puede usar teclado o mouse; le cuesta interactuar con dispositivos; necesita acceso alternativo; dificultades para expresarse | Acceso a dispositivos; computadora; software educativo |
| 33 | Pen reader | Didáctico | — | Acceso, accesibilidad tecnológica | Le cuesta leer palabras; no comprende lo que lee; evita la lectura; se cansa; necesita apoyo para acceder al texto | Lectura de impresos; comprensión; evaluaciones; tareas con material escrito |
| 34 | Auriculares cancelación auditiva | Sensorial | — | Regulación, atención | Se distrae con ruidos; le molestan los sonidos; se desconcentra; se tapa los oídos; pierde foco; sobrecarga auditiva | Lectura individual; evaluaciones; trabajo autónomo; concentración |

> **Nota:** Apéndice intencionalmente compacto. La migración SQL del Apéndice B usa los textos completos de la Matriz General (no abreviados como acá).

---

## Apéndice B — Mapeo DB actual → Listado FINAL (referencia rápida)

| DB id | DB nombre actual | Acción | Nombre destino |
|---|---|---|---|
| 1 | Tablet educativa (10") | conservar+enriquecer | Tablet 10'' Android + 8GB RAM + disco 128 GB |
| 2 | Auriculares con microfono | conservar+enriquecer (validar nombre) | Auriculares (con micrófono) |
| 3 | Mouse trackball | conservar+enriquecer | Mouse trackball |
| 4 | Teclado CLEVY | reemplazar | Teclado Admouse |
| 5 | Stickers de contraste para teclado | conservar+enriquecer | Sticker con contraste para teclado |
| 6 | Pulsador boton USB | conservar+enriquecer | Pulsador botón USB |
| 7 | Soporte flexible celular/tablet | conservar (no en FINAL — validar) | igual |
| 8 | Pen reader (lapiz lector) | conservar+enriquecer | Pen reader |
| 9 | Regla lupa | renombrar+stage | Ayuda para la lectura — tamaño ajustable — etapa 1 |
| 10 | Regla de lectura con ventana | renombrar+stage | Ayuda para la lectura — tamaño fijo 2 palabras — etapa 2 |
| 11 | Finger focus (señalador de dedo) | renombrar+stage | Ayuda para la lectura — Reglas de lectura guiada — etapa 3 |
| 12 | Tijeras adaptadas | renombrar+stage | Tijera adaptada — etapa 1 |
| 13 | Pinzas de escritura | renombrar+stage | Soporte para lápiz 1 — etapa 4 |
| 14 | Elastico para silla | renombrar | Banda elástica Bouncyband |
| 15 | Patas de silla (almohadillas sensoriales) | conservar+enriquecer | Patas de silla x4 |
| 16 | Time Timer (temporizador visual) | conservar+enriquecer | Time timer |
| 17 | Pelota antiestres de gel | conservar (no en FINAL — validar) | igual |
| 18 | Auriculares cancelacion de ruido | conservar+enriquecer | Auriculares de cancelación auditivo |

| Productos a INSERTAR (16) | |
|---|---|
| Soporte para lápiz 2 — etapa 3 | |
| Soporte para lápiz 3 — etapa 2 | |
| Soporte para lápiz 4 — etapa 1 | |
| Pesas para lápices | |
| Muñequera sensorial x2 | |
| Material sensorial de apriete SPEKS | |
| Material sensorial de apriete SPEKS con textura | |
| Pelota para el pie (vaivén) o muslo (presión) | |
| BouncyBand Sit & Twist Cojín de Asiento Activo | |
| Ayuda para la lectura — Reglas de lectura transparente con renglón — etapa 4 | |
| Panel separador de pupitre | |
| Sacapuntas para zurdos (metadata TBD) | |
| Lapicera para zurdos (metadata TBD) | |
| Tijera para zurdos (metadata TBD) | |
| Organizador de tareas personalizable | |
| Mesa plegable portátil | |
| Mouse Admouse | |
| Tijera adaptada — etapa 2 | |

---

## Apéndice C — Decisiones que NO tomó este documento

(Las dejo explícitas para que cuando aparezcan en una conversación futura no se reabran como si nunca se hubieran considerado.)

1. **Multi-tenant / multi-institución del catálogo.** Hoy la valija es la misma para todos. Si el día de mañana cada institución tiene un kit distinto, hace falta tabla `institution_devices`. Por ahora `active` es global.
2. **Embeddings para `lookup_by_manifestation`.** Para el MVP el catálogo va embebido en el prompt como JSON. Si crece a >50 productos o quieren búsqueda determinista, evaluar pgvector.
3. **Memoria a largo plazo del agente.** Hoy cada conversación es efímera (history en frontend). Cuando entre feedback loop hay que pensar dónde persistir conversaciones que aporten contexto entre sesiones.
4. **Idioma.** Todo en español rioplatense. Si Educabot vende en otros países, hay que internacionalizar tanto el prompt como las manifestaciones del catálogo.
5. **Voz natural / TTS.** El docente ya puede dictar (speech-to-text). Reproducir respuesta como audio queda fuera.

---

## Apéndice D — Referencias

- `Valijas adaptativa - Flujo de demo.md` — fuente canónica de los 14 lineamientos y 15 casos.
- `Seguimiento proyecto Valijas 22-04.txt` — acuerdo: foco en asistencia + Inclusión 101.
- `Seguimiento proyecto Valijas 29-04.txt` — DUA, individualización, prolongación, feedback, accesibilidad.
- `Listado de productos Valija 2026 - Listado productos - FINAL.csv` — 34 productos canónicos.
- `Listado de productos Valija 2026 - Matriz General.csv` — fuente de manifestaciones, situaciones, categorías y perfiles.
- `Listado de productos Valija 2026 - Matriz Perfil alicia.csv` — agrupación por perfil de alumno.
- `PRD-Modulo-Inclusion.md` — visión de producto completa (modos, flujos, integración).
- `main.py:3715-3853` — código actual del endpoint `/inclusion/assist`.
- `av3-front/src/pages/InclusionAsistencia.tsx` — UI actual.
