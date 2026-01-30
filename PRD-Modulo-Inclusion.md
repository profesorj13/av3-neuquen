# PRD: Modulo de Inclusion - Alicia (Valija Adaptativa)

> **Producto:** Alicia - Modulo de Inclusion Educativa
> **Empresa:** Educabot - Tecnologia Educativa
> **Version:** 1.0
> **Fecha:** 30 de Enero 2026
> **Autor:** Equipo de Producto
> **Estado:** Draft

---

## Tabla de Contenidos

1. [Vision General](#1-vision-general)
2. [Contexto y Problema](#2-contexto-y-problema)
3. [Usuarios Objetivo](#3-usuarios-objetivo)
4. [Alcance del Producto](#4-alcance-del-producto)
5. [Flujos de Usuario](#5-flujos-de-usuario)
6. [Requerimientos Funcionales](#6-requerimientos-funcionales)
7. [Modelo de Datos](#7-modelo-de-datos)
8. [Matriz de Recomendacion de Dispositivos](#8-matriz-de-recomendacion-de-dispositivos)
9. [Catalogo de Dispositivos por Rampa](#9-catalogo-de-dispositivos-por-rampa)
10. [Alcance MVP / Demo](#10-alcance-mvp--demo)
11. [Roadmap y Fases](#11-roadmap-y-fases)
12. [Consideraciones Tecnicas](#12-consideraciones-tecnicas)
13. [Integracion con Codebase Existente (av3-neuquen)](#13-integracion-con-codebase-existente-av3-neuquen)
14. [Plan de Implementacion Tecnico](#14-plan-de-implementacion-tecnico)
15. [Metricas de Exito](#15-metricas-de-exito)

---

## 1. Vision General

### Que es

Un modulo integrado dentro de la plataforma Alicia que permite la planificación y el dictado de clases para alumnos con inclusión. Asiste a docentes en el uso de la **Valija Adaptativa de Inclusion** — un kit fisico de dispositivos tecnologicos y analogicos organizados en tres "rampas" tematicas, disenado para eliminar barreras de aprendizaje en el aula.

### Proposito

Alicia, como asistente virtual con IA, guia al docente en:
- **Conocer** los dispositivos de la valija y su proposito pedagogico.
- **Planificar** que dispositivo usar para cada clase segun la actividad y las necesidades del alumno.
- **Usar** los dispositivos en tiempo real durante la clase.
- **Registrar** como le fue al alumno con el dispositivo (feedback loop).

### Propuesta de Valor

> "Un docente sin formacion en psicopedagogia ni tecnologia adaptativa puede, con la guia de Alicia, integrar dispositivos de inclusion en su clase de forma practica, agil y efectiva."

El sistema es:
- **Practico**: se usa desde el celular, en el aula.
- **Facil**: conversacion guiada, no requiere formacion previa.
- **Escalable**: funciona con cualquier asignatura y tipo de necesidad.
- **Dinamico**: aprende de cada experiencia y mejora sus recomendaciones.

---

## 2. Contexto y Problema

### Problema

Las escuelas reciben estudiantes con discapacidad o necesidades de aprendizaje diversas. La normativa vigente garantiza su derecho a la educacion comun. Sin embargo:

- Los docentes **no son psicopedagogos** ni terapeutas especializados.
- Los docentes **no son especialistas** en tecnologia adaptativa ni informatica aplicada a accesibilidad.
- **Carecen de herramientas practicas** para adaptar contenidos y dinamicas.
- La mayoria de los estudiantes **no han utilizado previamente** dispositivos accesibles en contextos escolares.
- Los docentes **no tienen acompanamiento tecnico** especializado disponible.

### Solucion

El Programa de Inclusion de Educabot combina:

| Componente | Descripcion |
|---|---|
| **Hardware (Valija)** | Kit fisico con dispositivos adaptativos organizados en 3 rampas |
| **Software (Alicia)** | Asistente virtual IA que guia al docente en el uso de la valija |
| **Datos** | Sistema de trazabilidad, metricas de uso e impacto |

### Stakeholders del Proyecto

| Rol | Persona | Responsabilidad |
|---|---|---|
| Producto / Pedagogia | Micaela Unamuno | Definicion de flujos, contenido pedagogico, rampas |
| Producto / Coordinacion | Agustina B. | Coordinacion general, prioridades de demo |
| Desarrollo | Juan M. | Implementacion tecnica, integracion con Alicia |
| Pedagogia | Ivana Marchettini | Contenido de rampas, materiales |
| Cliente | Ministra de Educacion de Tucuman | Destinataria de la demo inicial |

---

## 3. Usuarios Objetivo

### Usuario Primario: Docente de Aula

- Trabaja en escuelas que reciben la Valija Adaptativa.
- No tiene formacion especializada en inclusion/accesibilidad.
- Tiene alumnos con diversas necesidades de aprendizaje.
- Necesita soluciones **rapidas y practicas** para usar en clase.
- Usa celular en el aula, computadora para planificacion en casa.

### Usuario Secundario: Gestores Educativos / Ministerio

- Necesitan datos de trazabilidad: que valijas se usan, que dispositivos, frecuencia, impacto.
- Dashboards con metricas agregadas.

---

## 4. Alcance del Producto

### 4 Caminos de Entrada al Modulo de Inclusion

Segun el flujo definido en la reunion y el diagrama, cuando el usuario pide ayuda a Alicia en contexto de inclusion, tiene **4 caminos posibles**:

```
Usuario pide ayuda a Alicia
         |
    ┌────┼─────────────┬──────────────────┐
    │    │             │                  │
    v    v             v                  v
 Escaneo  Planificacion  Asistencia     Onboarding
 de QR    de clase        en clase       de valija
                                          │
                                    ┌─────┼─────┐
                                    v     v     v
                                 Rampa  Rampa  Rampa
                                Digital Pedag. Sensor.
```

### Camino 1: Escaneo de QR (Acceso directo a dispositivo)

- El docente escanea con la **camara nativa** del celular el QR de un dispositivo de la valija.
- Se abre un link que lleva a Alicia en el navegador.
- Alicia da la bienvenida y muestra la **ficha del dispositivo**: nombre, descripcion, para que sirve, como usarlo, en que situaciones es util.
- Desde ahi puede navegar a "Planificar uso con un alumno" o "Buscar otra herramienta".

### Camino 2: Planificacion de Clase (Modo Planificador)

Flujo completo de planificacion asistida:

1. **Relevamiento de la actividad** (conversacion con Alicia):
   - Asignatura y eje tematico
   - Objetivo de la clase
   - Duracion de la actividad
   - Dinamica (grupal, individual, con tecnologia, etc.)
   - Materiales o herramientas a utilizar

2. **Relevamiento de la necesidad del alumno**:
   - Seleccion de alumnos (fichas precargadas en Alicia)
   - Si el alumno ya tiene ficha: Alicia permite seleccionar
   - Si es nuevo: se puede crear nuevo alumno; preguntas de relevamiento (ver seccion 6)
   - Tipo de dificultad (motricidad, comunicacion, atencion, acceso digital, etc.)
   - Condicion transitoria o permanente

3. **Insumo propuesto para la actividad** (output de Alicia):
   - Dispositivo recomendado con justificacion pedagogica
   - De que rampa proviene
   - Como usarlo en la actividad especifica
   - Tips de integracion con el grupo
   - Consideraciones ("reduce frustracion", "da autonomia inmediata", etc.)
   - Muestra una card con acceso a la ficha del producto. 

4. **Onboarding y uso del producto**:
   - Ficha completa del dispositivo recomendado
   - Guia paso a paso
   - Enlace a video/contenido complementario (futuro)

### Camino 3: Asistencia en Clase (Tiempo Real)

- El docente esta EN el aula y necesita ayuda rapida.
- Conversa con Alicia: "Tengo un alumno que no puede agarrar el lapiz, que uso?"
- Alicia responde con recomendacion directa basada en los datos de actividad y necesidad.
- Input por texto o por voz con speech-to-text a desarrollar

### Camino 4: Onboarding de Valija

- Primer contacto del docente con la valija.
- Alicia presenta una landing, y las 3 rampas con cards informativas:
  - **Rampa Digital**: descripcion + lista de dispositivos (breve)
  - **Rampa Didactico-Pedagogica**: descripcion + lista de dispositivos (breve)
  - **Rampa Autorregulacion Sensorial**: descripcion + lista de dispositivos (breve)
- Al ingresar a una rampa, se ve un titulo grande, un video, una descripción de la rampa y todos los dispositivos que la componen.
- Cada dispositivo tiene una ficha tocable con descripcion, uso y recomendaciones.

---

## 5. Flujos de Usuario

### Flujo 1: Planificacion Completa (Happy Path)

```
Docente abre Alicia → Modulo Inclusion → "Planificar clase"
  │
  ├─ Alicia: "Hola! ¿Con qué trabajamos hoy?"
  │  Docente: "Practicas del lenguaje, dictado de texto, 10 min, individual"
  │
  ├─ Alicia: "Genial! ¿Que materiales vas a usar?"
  │  Docente: "Lapiz y cuaderno"
  │
  ├─ Alicia: "Para que alumno necesitas adaptar?"
  │  → Muestra lista de alumnos con fichas de inclusion precargadas
  │  Docente selecciona: "Tomas"
  │
  ├─ Alicia muestra ficha: "Tomas - Dificultades en motricidad fina,
  │  debilidades musculares en la mano, retrasos madurativos"
  │
  ├─ Alicia: "Por lo que me contas, Tomas necesita un insumo que lo
  │  ayude a sujetar la lapicera de forma adaptada para el dictado.
  │  Te recomiendo el ADAPTADOR DE ESCRITURA (Pinza de escritura),
  │  un recurso de la Rampa Didactico-Pedagogica."
  │
  │  Porque:
  │  - Permite participar de la actividad sin restriccion
  │  - Reduce frustracion
  │  - Da autonomia inmediata
  │  - Se integra facilmente al trabajo grupal
  │
  └─ Docente: "Dale, lo uso" → Alicia registra uso planificado
```

### Flujo 2: Escaneo de QR

```
Docente escanea QR del dispositivo con camara nativa
  │
  ├─ Se abre link en navegador → Alicia
  │
  ├─ Alicia muestra ficha del dispositivo:
  │  - Nombre, imagen, descripcion
  │  - Para que sirve
  │  - Como instalarlo/usarlo
  │  - En que actividades es util
  │  - Para que tipo de necesidad
  │
  ├─ Botones: [Planificar uso] [Buscar otra herramienta] [Volver]
  │
  └─ Si toca "Planificar uso" → entra al flujo de planificacion
```

### Flujo 3: Asistencia en Clase

```
Docente en el aula → Abre Alicia → "Necesito ayuda ahora"
  │
  ├─ Alicia: "Contame que esta pasando"
  │  Docente: "El alumno no puede usar la tijera con la mano izquierda"
  │
  ├─ Alicia: "Te recomiendo las TIJERAS ADAPTADAS de la Rampa
  │  Didactico-Pedagogica. Tienen reapertura automatica y
  │  funcionan para zurdos o estudiantes con movilidad reducida."
  │
  └─ Muestra ficha + como usarla
```

### Flujo 4: Onboarding de Valija

```
Docente recibe valija por primera vez → Abre Alicia → "Conocer la valija"
  │
  ├─ Alicia muestra 3 cards de rampas:
  │  [Rampa Digital] [Rampa Didactico-Pedagogica] [Rampa Autorregulacion]
  │
  ├─ Docente toca "Rampa Digital" →
  │  - Descripcion de la rampa
  │  - Lista de dispositivos con imagen y mini-descripcion
  │  - Toca un dispositivo → ficha completa
  │
  └─ Puede navegar entre rampas o hacer preguntas a Alicia
```

### Flujo 5: Post-Actividad (Feedback)

```
Despues de la clase → Alicia pregunta: "Como le fue a Tomas con el adaptador?"
  │
  ├─ Docente: "Le costo al principio pero despues pudo escribir solo"
  │
  ├─ Alicia registra feedback en la ficha del alumno
  │  Actualiza historial de uso del dispositivo
  │
  └─ Alicia: "La proxima vez te sugiero que le des unos minutos
     de practica antes del dictado para que se acostumbre."
```

---

## 6. Requerimientos Funcionales

### RF01: Modulo de Inclusion en Alicia

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF01.1 | Seccion/entrada "Inclusion" visible desde la home de Alicia | Alta |
| RF01.2 | Boton de acceso al modulo de inclusion desde el modulo de planificacion existente | Alta |
| RF01.3 | Responsive mobile-first (uso principal desde celular en el aula) | Alta |
| RF01.4 | Soporte para tablet (responsive) | Media |

### RF02: Onboarding de Valija

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF02.1 | Pantalla con 3 cards de rampas (Digital, Didactico-Pedagogica, Autorregulacion Sensorial) | Alta |
| RF02.2 | Al tocar una rampa: descripcion + listado de dispositivos | Alta |
| RF02.3 | Ficha de cada dispositivo: nombre, imagen, descripcion, uso, para que tipo de necesidad | Alta |
| RF02.4 | Videos explicativos por rampa | Baja (futuro) |

### RF03: Escaneo de QR

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF03.1 | Cada dispositivo tiene un QR unico que abre un deep link a Alicia | Alta |
| RF03.2 | El link lleva directamente a la ficha del dispositivo en Alicia (navegador) | Alta |
| RF03.3 | Desde la ficha, CTA para "Planificar uso" o "Buscar otra herramienta" | Alta |

### RF04: Modo Planificador

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF04.1 | Conversacion guiada para relevar actividad (asignatura, objetivo, dinamica, duracion, materiales) | Alta |
| RF04.2 | Seleccion de alumno desde fichas precargadas en Alicia | Alta |
| RF04.3 | Visualizacion de ficha del alumno con condiciones de inclusion | Alta |
| RF04.4 | Si alumno nuevo: formulario de relevamiento de necesidad (ver RF06) | Alta |
| RF04.5 | Output: recomendacion de dispositivo con justificacion pedagogica | Alta |
| RF04.6 | Output: ficha de uso del producto recomendado (como usarlo en la actividad especifica) | Alta |
| RF04.7 | Formato conversacional (chat con Alicia) | Alta |
| RF04.8 | Alicia extrae datos de la conversacion sin repreguntar lo ya mencionado | Media |

### RF05: Asistencia en Clase (Tiempo Real)

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF05.1 | Chat rapido con Alicia para resolver dudas sobre dispositivos | Alta |
| RF05.2 | Recomendacion directa basada en situacion descrita | Alta |
| RF05.3 | Input por texto | Alta |
| RF05.4 | Input por voz (speech-to-text) | Media (a desarrollar) |

### RF06: Relevamiento de Necesidad del Alumno

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF06.1 | Pregunta: La condicion es transitoria o permanente? | Alta |
| RF06.2 | Pregunta tipo checkbox (no patologizante): | Alta |
| | - Tiene dificultad para mover o controlar sus manos o brazos | |
| | - Tiene dificultad para comunicarse o expresar respuestas | |
| | - Tiene dificultad para mantener la atencion o regular emociones | |
| | - Tiene dificultad para acceder a la tecnologia digital | |
| | - Tiene varias de estas dificultades | |
| | - No estoy seguro / quiero explorar opciones | |
| RF06.3 | Las respuestas se guardan en la ficha del alumno | Alta |
| RF06.4 | Alicia puede preguntar de forma conversacional en lugar de formulario, aunque formulario para este caso es mas rápido y mejor| Media |

### RF07: Catalogo de Dispositivos

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF07.1 | Base de datos de todos los dispositivos de la valija con: nombre, descripcion, imagen, rampa, para que necesidad sirve, como usarlo | Alta |
| RF07.2 | Cada dispositivo vinculado a su QR unico | Alta |
| RF07.3 | Busqueda y filtrado de dispositivos | Media |

### RF08: Feedback Post-Actividad

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF08.1 | Alicia pregunta como le fue despues de una actividad planificada | Media |
| RF08.2 | El feedback se registra en la ficha del alumno | Media |
| RF08.3 | El feedback alimenta futuras recomendaciones | Baja (futuro) |

### RF09: Integracion con Planificacion Existente

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF09.1 | Desde el modulo de planificacion de Alicia, boton "Adaptar para inclusion" | Alta |
| RF09.2 | Si Alicia detecta que el docente tiene alumnos con ficha de inclusion, sugerir proactivamente | Baja (futuro) |

---

## 7. Modelo de Datos

### Entidades Principales

```
Dispositivo {
  id: UUID
  nombre: string              // "Pinza de escritura"
  descripcion: string         // Descripcion completa
  descripcion_corta: string   // Para cards
  imagen_url: string
  rampa: enum [DIGITAL, DIDACTICO_PEDAGOGICA, AUTORREGULACION_SENSORIAL]
  qr_code: string             // Codigo QR unico
  necesidades_target: string[] // ["motricidad_fina", "escritura"]
  como_usar: string           // Instrucciones de uso
  recomendaciones: string     // Tips pedagogicos
  fundamentacion: string      // Por que funciona
}

FichaInclusionAlumno {
  id: UUID
  alumno_id: UUID             // FK al alumno existente en Alicia
  condicion_transitoria: boolean
  dificultades: enum[] [
    MOTRICIDAD_MANOS_BRAZOS,
    COMUNICACION_EXPRESION,
    ATENCION_REGULACION_EMOCIONAL,
    ACCESO_TECNOLOGIA_DIGITAL,
    MULTIPLES,
    SIN_DEFINIR
  ]
  descripcion_libre: string   // Notas del docente
  historial_uso: RegistroUso[]
  created_at: datetime
  updated_at: datetime
}

RegistroUso {
  id: UUID
  alumno_id: UUID
  dispositivo_id: UUID
  actividad_descripcion: string
  asignatura: string
  fecha: datetime
  feedback_docente: string
  resultado: enum [POSITIVO, NEUTRO, NECESITA_AJUSTE]
}

Rampa {
  id: UUID
  nombre: string              // "Rampa Digital"
  descripcion: string
  descripcion_corta: string
  dispositivos: Dispositivo[]
}

PlanificacionInclusion {
  id: UUID
  docente_id: UUID
  alumno_id: UUID
  asignatura: string
  objetivo_clase: string
  dinamica: string
  duracion: string
  materiales: string
  dispositivo_recomendado_id: UUID
  justificacion: string
  fecha_planificada: datetime
  feedback: string?
  created_at: datetime
}
```

---

## 8. Matriz de Recomendacion de Dispositivos

Esta matriz debe ser construida con el equipo pedagogico. Define **que dispositivo recomendar segun la combinacion de necesidad del alumno + tipo de actividad**.

### Estructura Propuesta

```
Necesidad del Alumno          x  Tipo de Actividad
─────────────────────────────────────────────────────
                              Escritura  Lectura  Digital  Recorte  Grupal
Motricidad fina               Pinza esc  -        Trackball Tijeras  -
Movilidad reducida manos      Pinza esc  Finger   Pulsador  Tijeras  -
Dificultad visual             -          Regla    Stickers  -        -
                                         lupa     teclado
Atencion / concentracion      -          Regla    -         -        Time
                                         ventana                     timer
Regulacion sensorial          Pelota     -        Auric.   -        Elast.
                              anti-est            cancel.            silla
Acceso tecnologia             -          Pen      Teclado  -        -
                                         reader   Clevy
Comunicacion                  -          -        Pulsador -        -
                                                  boton
```


### Logica de Recomendacion

Para el MVP, la recomendacion se basa en:
1. Alicia recibe la descripcion de los dispositivos en su prompt/contexto.
2. Con la informacion de la actividad + necesidad del alumno, la IA sugiere el dispositivo mas adecuado.
3. La IA usa la fundamentacion pedagogica de cada dispositivo para justificar la recomendacion.

Para version futura:
- Matriz codificada con reglas explicitas como fallback.
- IA + matriz como sistema hibrido.
- Feedback loop de docentes alimenta la matriz.

---

## 9. Catalogo de Dispositivos por Rampa

### Rampa Digital

| Dispositivo | Descripcion | Necesidad que atiende |
|---|---|---|
| **Tablet 10" Android** (x3) | 8GB RAM, 128GB disco | Acceso digital general |
| **Auriculares con microfono** (x3) | Aislamiento de ruido, comando de voz | Acceso digital, concentracion |
| **Mouse trackball** (x1) | Para dificultades de control motor. Compatible con contactores para clic | Motricidad, movilidad reducida |
| **Teclado CLEVY** (x1) | Letras grandes, colores diferenciados por grupos de teclas | Motricidad, dificultad visual/cognitiva |
| **Stickers contraste teclado** (x20) | Teclas grandes y colores contrastantes | Dificultad visual |
| **Pulsador boton USB** (x1) | Alternativa a teclado/raton, activacion por presion | Motricidad severa |
| **Soporte flexible celular/tablet** (x1) | Brazo articulado para posicionar dispositivo | Movilidad reducida |

### Rampa Didactico-Pedagogica

| Dispositivo | Descripcion | Necesidad que atiende |
|---|---|---|
| **Pen reader** (x1) | Escanea texto y lo lee en voz alta | Lectura, comprension |
| **Regla lupa** (x2) | Lupa central que destaca una linea de texto | Dificultad visual, lectura |
| **Regla de lectura con ventana** (x2) | Mantiene atencion en una linea, reduce distracciones | Atencion, dificultad cognitiva |
| **Finger focus** (x2) | Mejora autonomia y fluidez lectora | Dificultad aprendizaje/cognitiva |
| **Tijeras adaptadas** (x1) | Reapertura automatica, para zurdos o movilidad reducida | Motricidad, zurdos |
| **Pinzas de escritura** (x3) | Postura correcta de dedos para sostener lapiz | Motricidad fina, dispraxia |

### Rampa de Autorregulacion Sensorial

| Dispositivo | Descripcion | Necesidad que atiende |
|---|---|---|
| **Elastico para silla** (x1) | Libera energia de forma controlada sin interrumpir | Concentracion, hiperactividad |
| **Patas de silla (sopapas)** (x4) | Estimulo sensorial controlado, reduce inquietud | Autorregulacion sensorial |
| **Time timer** (x1) | Referencia visual clara del tiempo para actividades | Ansiedad, concentracion |
| **Pelota antiestres gel** (x1) | Descarga sensorial, alivia estres y ansiedad | Regulacion emocional |
| **Auriculares cancelacion ruido** (x1) | Reduce sobrecarga sensorial sin aislar del grupo | Sensibilidad auditiva, concentracion |

---

## 10. Alcance MVP / Demo

### Contexto de la Demo

- **Audiencia**: Ministra de Educacion de Tucuman
- **Formato**: Demo en celular (mobile-first)
- **Objetivo**: Demostrar que el sistema es practico, facil, escalable y dinamico
- **Dispositivos demo**: Adaptador de escritura (pinza) + Eye tracking

### Funcionalidades MVP (Demo)

| # | Feature | Estado |
|---|---|---|
| 1 | **Entrada al modulo de inclusion** desde Alicia | Construir |
| 2 | **Onboarding de valija**: 3 cards de rampas con descripcion y dispositivos | Construir |
| 3 | **Ficha de dispositivo**: al tocar un dispositivo, ver ficha completa | Construir |
| 4 | **Modo Planificador**: conversacion guiada (actividad → alumno → recomendacion) | Construir |
| 5 | **Fichas de alumnos**: mostrar 3 alumnos precargados con ficha de inclusion | Existente (extender) |
| 6 | **Output de recomendacion**: dispositivo + justificacion pedagogica | Construir |
| 7 | **Escaneo QR**: link desde QR fisico que abre ficha de dispositivo en Alicia | Construir |
| 8 | **Responsive mobile** | Verificar |

### Datos Precargados para Demo

**3 alumnos de ejemplo con fichas de inclusion:**

1. **Alumno 1** — Dificultades en motricidad fina, debilidades musculares en la mano, retrasos madurativos
2. **Alumno 2** — Dificultad para acceder a tecnologia digital (caso eye tracking)
3. **Alumno 3** — Dificultad para mantener la atencion, necesita autorregulacion sensorial

**Escenario demo completo (Modo Planificador):**

> Docente: "Voy a hacer un dictado de texto en Practicas del Lenguaje, 10 minutos, individual, con lapiz y cuaderno."
>
> Selecciona: Alumno 1 (motricidad fina)
>
> Alicia recomienda: "Pinza de escritura" de la Rampa Didactico-Pedagogica
>
> Justificacion: "Permite participar sin restriccion, reduce frustracion, da autonomia inmediata, se integra al trabajo grupal."

### Lo que NO entra en el MVP

- Matriz de recomendacion codificada (se delega a la IA con contexto)
- Feedback post-actividad
- Dashboard de metricas para el Ministerio
- Sistema NFC de deteccion de dispositivos en valija
- Red de experiencias colaborativas entre docentes

---

## 11. Roadmap y Fases

### Fase 0: Demo (actual)
- Entrada al modulo de inclusion
- Onboarding de valija (3 cards + fichas de dispositivos)
- Modo Planificador 
- Escaneo QR → ficha de dispositivo
- 3 alumnos precargados
- Mobile-first

### Fase 1: MVP Completo
- Todos los dispositivos de las 3 rampas cargados con ficha completa
- Formulario de relevamiento de necesidad del alumno
- Persistencia de fichas de inclusion de alumnos
- Asistencia en clase (chat rapido)
- Registro de uso de dispositivos
- Construccion de la matriz de recomendacion completa con equipo pedagogico

### Fase 2: Inteligencia y Feedback
- Feedback post-actividad
- Historial de uso por alumno
- Recomendaciones mejoradas basadas en historial
- Speech-to-text para input por voz
- Videos en onboarding de rampas

### Fase 3: Datos y Escala
- Dashboard de metricas para Ministerio (trazabilidad, uso, impacto)
- Sistema NFC de deteccion de dispositivos en valija
- Red de experiencias colaborativas entre docentes
- Integracion proactiva: Alicia sugiere adaptar automaticamente si detecta alumnos con inclusion
- API de sincronizacion con valija fisica

---

## 12. Consideraciones Tecnicas

### Integracion con Alicia Existente

- El modulo de inclusion se integra como una **seccion nueva dentro de Alicia**, no como app separada.
- Acceso desde: (1) Home de Alicia, (2) Modulo de planificacion existente (boton "Adaptar para inclusion"), (3) Deep link via QR.
- Reutiliza el sistema de alumnos ya existente en Alicia, extendiendolo con la ficha de inclusion.
- Reutiliza el motor de chat/IA existente, agregando contexto de dispositivos y rampas.

### Arquitectura de QR

- Cada dispositivo fisico tiene un QR pegado que codifica una URL tipo: `https://alicia.educabot.com/inclusion/dispositivo/{id}`
- La camara nativa del celular abre el link en el navegador.
- No requiere app nativa ni escaner especial.
- La ruta del QR debe ser **publica** (no requiere login/seleccion de usuario) para acceso inmediato.

### IA y Recomendaciones

- Para el MVP, la recomendacion se basa en prompt engineering: Alicia recibe en su contexto la descripcion completa de todos los dispositivos, rampas y su fundamentacion pedagogica.
- La IA cruza: (actividad del docente) + (necesidad del alumno) + (catalogo de dispositivos) para generar la recomendacion.
- Futuro: matriz codificada como fallback + IA como capa inteligente.

### Mobile-First

- Uso principal: celular en el aula.
- Planificacion: puede hacerse desde computadora (desktop responsive).
- La demo se mostrara 100% desde celular.

### Speech-to-Text (Futuro)

- A desarrollar. Permitira que el docente hable con Alicia por audio.
- El sistema transcribe y procesa como si fuera texto.

---

## 13. Integracion con Codebase Existente (av3-neuquen)

### Stack Actual del Proyecto

| Capa | Tecnologia | Detalle |
|---|---|---|
| **Frontend** | React 19 + TypeScript | Vite 7, Tailwind CSS 4, Radix UI / shadcn |
| **State** | Zustand 5 | Store centralizado en `useStore.ts` (297 lineas) |
| **Routing** | React Router 7 | Rutas en `App.tsx` |
| **Backend** | FastAPI (Python) | Monolito en `main.py` (3,383 lineas) |
| **Base de Datos** | PostgreSQL | 7 migraciones SQL, conexion psycopg2 |
| **IA** | Azure OpenAI | Modelo `gpt-5-mini`, chat completions sync/async |
| **Integracion** | Kapso (WhatsApp) | Workflows para notificaciones |

### Estructura del Proyecto

```
av3-neuquen/
├── demo-alizia/                    # Frontend React
│   └── src/
│       ├── pages/                  # Paginas (Login, TeacherHome, Course, etc.)
│       ├── components/
│       │   ├── layout/             # MainLayout, Header, Sidebar
│       │   └── ui/                 # ChatBot, StudentsList, Cards, Radix components
│       ├── store/useStore.ts       # Zustand - estado global
│       ├── services/api.ts         # Cliente API (fetch wrapper, base: localhost:8000)
│       └── types/index.ts          # TypeScript types
├── main.py                         # Backend FastAPI completo
├── migrations/                     # SQL migrations (001-007)
├── seeds/                          # Datos semilla
├── kapso/                          # WhatsApp integration
└── docker-compose.yml              # PostgreSQL dev (port 5480)
```

### Que Ya Existe y Se Reutiliza

| Componente Existente | Archivo Clave | Como se reutiliza para Inclusion |
|---|---|---|
| **Tabla `students`** | `migrations/001_initial.sql` | Base para fichas de inclusion. Tiene `id`, `course_id`, `name`. Se extiende con tabla `student_inclusion_profiles`. |
| **Tabla `users`** | `migrations/001_initial.sql` | Docentes ya modelados con `id`, `name`, `email`. El rol "teacher" se deduce de `course_subjects`. |
| **ChatBot UI** | `components/ui/ChatBot.tsx` | Componente de chat reutilizable. Panel colapsable, historial, input text, loading state. Se adapta para chat de inclusion con nuevo endpoint. |
| **Patron Wizard** | `pages/TeacherPlanWizard.tsx` | Flujo multi-paso para planificacion. El Modo Planificador de inclusion puede seguir el mismo patron (step-based). |
| **Teacher Home** | `pages/TeacherHome.tsx` | Punto de entrada para docentes. Se agrega card/boton de "Inclusion" aca. |
| **Teacher Lesson Plan** | `pages/TeacherLessonPlan.tsx` | Planificacion de clase con 3 momentos (apertura, desarrollo, cierre). Se agrega boton "Adaptar para inclusion". |
| **Store Zustand** | `store/useStore.ts` | Estado global. Se extiende con slices de inclusion (dispositivos, rampas, fichas, chat de inclusion). |
| **API Client** | `services/api.ts` | Wrapper fetch con base URL. Se agregan funciones para endpoints de inclusion. |
| **Types** | `types/index.ts` | Tipos TS existentes. Se agregan interfaces de inclusion. |
| **MainLayout** | `components/layout/MainLayout.tsx` | Layout con Header + Sidebar. Las paginas de inclusion se renderizan dentro. |
| **Azure OpenAI** | `main.py` (lineas ~426-656) | Patron de chat con system prompt + historial. Se crea nuevo endpoint con system prompt de inclusion que incluye catalogo de dispositivos. |
| **Actividades por momento** | `main.py` `/activities/recommend` | Patron de recomendacion existente. El endpoint `/inclusion/recommend` sigue la misma estructura. |

### Que Hay Que Crear Desde Cero

#### Backend (main.py)

| Componente | Descripcion |
|---|---|
| **Migracion `008_inclusion.sql`** | Tablas: `ramps`, `devices`, `student_inclusion_profiles`, `inclusion_plans`, `device_usage_logs` |
| **Seed `inclusion_seed.sql`** | Datos de las 3 rampas + ~20 dispositivos con descripciones completas |
| **Pydantic Models** | `Ramp`, `Device`, `StudentInclusionProfile`, `InclusionPlan`, `DeviceUsageLog` |
| **CRUD Endpoints** | `GET /ramps`, `GET /devices`, `GET /devices/{id}`, `GET /devices/by-qr/{qr_code}` |
| **Inclusion Profiles** | `GET/POST/PATCH /students/{id}/inclusion-profile` |
| **Inclusion Plans** | `POST /inclusion-plans`, `GET /teachers/{id}/inclusion-plans` |
| **Chat Inclusion** | `POST /inclusion/chat` — chat con system prompt que incluye catalogo de dispositivos + ficha del alumno |
| **Recommend** | `POST /inclusion/recommend` — recibe actividad + necesidad, devuelve dispositivo recomendado |

#### Frontend (demo-alizia/src/)

| Componente | Ruta | Descripcion |
|---|---|---|
| **InclusionHome** | `/inclusion` | Home del modulo: 4 opciones (Onboarding, Planificar, Asistencia, Escanear QR) |
| **ValijOnboarding** | `/inclusion/valija` | 3 cards de rampas, al tocar muestra dispositivos |
| **RampDetail** | `/inclusion/valija/:rampId` | Lista de dispositivos de una rampa |
| **DeviceDetail** | `/inclusion/dispositivo/:id` | Ficha completa del dispositivo (tambien accesible via QR — ruta publica) |
| **InclusionPlanner** | `/inclusion/planificar` | Wizard o chat guiado: actividad → alumno → recomendacion |
| **InclusionChat** | `/inclusion/asistencia` | Chat rapido con Alicia para ayuda en tiempo real |
| **StudentInclusionProfile** | (dialog/modal) | Ficha de inclusion del alumno, accesible desde el planner |

#### Store (useStore.ts — extender)

```typescript
// Nuevos slices a agregar:
interface InclusionState {
  ramps: Ramp[]
  devices: Device[]
  inclusionChatHistory: ChatMessage[]
  currentDevice: Device | null
  currentInclusionPlan: InclusionPlan | null

  // Actions
  setRamps: (ramps: Ramp[]) => void
  setDevices: (devices: Device[]) => void
  setCurrentDevice: (device: Device | null) => void
  addInclusionChatMessage: (msg: ChatMessage) => void
  clearInclusionChatHistory: () => void
}
```

#### Types (types/index.ts — extender)

```typescript
// Nuevos tipos a agregar:
interface Ramp {
  id: string
  name: string
  description: string
  short_description: string
}

interface Device {
  id: string
  name: string
  description: string
  short_description: string
  image_url: string
  ramp_id: string
  ramp_name?: string
  qr_code: string
  target_needs: string[]
  how_to_use: string
  recommendations: string
  rationale: string
  quantity: number
}

interface StudentInclusionProfile {
  id: string
  student_id: string
  student_name?: string
  is_transitory: boolean
  difficulties: string[]  // enum values
  free_description: string
  created_at: string
  updated_at: string
}

interface InclusionPlan {
  id: string
  teacher_id: string
  student_id: string
  subject: string
  class_objective: string
  class_dynamic: string
  duration: string
  materials: string
  recommended_device_id: string
  recommended_device?: Device
  justification: string
  planned_date: string
  feedback?: string
  created_at: string
}
```

### Rutas del Router (App.tsx — extender)

```typescript
// Agregar a las rutas existentes:
<Route path="/inclusion" element={<InclusionHome />} />
<Route path="/inclusion/valija" element={<ValijOnboarding />} />
<Route path="/inclusion/valija/:rampId" element={<RampDetail />} />
<Route path="/inclusion/dispositivo/:id" element={<DeviceDetail />} />  // Publica (QR)
<Route path="/inclusion/planificar" element={<InclusionPlanner />} />
<Route path="/inclusion/asistencia" element={<InclusionChat />} />
```

### Migracion SQL Propuesta (008_inclusion.sql)

```sql
-- Rampas adaptativas
CREATE TABLE ramps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,          -- "Rampa Digital"
    description TEXT NOT NULL,
    short_description VARCHAR(255),
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Dispositivos de la valija
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ramp_id UUID NOT NULL REFERENCES ramps(id),
    name VARCHAR(200) NOT NULL,           -- "Pinza de escritura"
    description TEXT NOT NULL,            -- Descripcion completa
    short_description VARCHAR(255),       -- Para cards
    image_url TEXT,
    qr_code VARCHAR(100) UNIQUE,          -- Codigo QR unico
    target_needs TEXT[],                  -- ARRAY["motricidad_fina","escritura"]
    how_to_use TEXT,                      -- Instrucciones
    recommendations TEXT,                 -- Tips pedagogicos
    rationale TEXT,                       -- Fundamentacion
    quantity INTEGER DEFAULT 1,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Perfil de inclusion del alumno (extiende tabla students existente)
CREATE TABLE student_inclusion_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    is_transitory BOOLEAN DEFAULT FALSE,
    difficulties TEXT[] NOT NULL DEFAULT '{}',
    -- Valores posibles:
    --   'MOTRICIDAD_MANOS_BRAZOS'
    --   'COMUNICACION_EXPRESION'
    --   'ATENCION_REGULACION_EMOCIONAL'
    --   'ACCESO_TECNOLOGIA_DIGITAL'
    --   'MULTIPLES'
    --   'SIN_DEFINIR'
    free_description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(student_id)
);

-- Planes de inclusion (output del Modo Planificador)
CREATE TABLE inclusion_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    teacher_id UUID NOT NULL REFERENCES users(id),
    student_id UUID NOT NULL REFERENCES students(id),
    device_id UUID REFERENCES devices(id),
    subject VARCHAR(200),
    class_objective TEXT,
    class_dynamic VARCHAR(100),
    duration VARCHAR(50),
    materials TEXT,
    justification TEXT,                   -- Generada por IA
    planned_date DATE,
    feedback TEXT,
    feedback_result VARCHAR(20),          -- 'POSITIVO','NEUTRO','NECESITA_AJUSTE'
    created_at TIMESTAMP DEFAULT NOW()
);

-- Log de uso de dispositivos (trazabilidad)
CREATE TABLE device_usage_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id UUID NOT NULL REFERENCES devices(id),
    student_id UUID REFERENCES students(id),
    teacher_id UUID NOT NULL REFERENCES users(id),
    action VARCHAR(50) NOT NULL,          -- 'QR_SCAN','PLANNED','USED','FEEDBACK'
    context JSONB,                        -- Metadata flexible
    created_at TIMESTAMP DEFAULT NOW()
);
```

### System Prompt de Inclusion (para Azure OpenAI)

El chat de inclusion usa un system prompt dedicado que incluye:

```
Sos Alicia, asistente de inclusion educativa de Educabot.
Tu rol es ayudar a docentes a integrar dispositivos adaptativos
de la Valija de Inclusion en sus clases.

CATALOGO DE DISPOSITIVOS:
{JSON con todos los dispositivos, rampas y descripciones cargado desde la DB}

FICHA DEL ALUMNO (si aplica):
{Datos del alumno seleccionado con su perfil de inclusion}

ACTIVIDAD PLANIFICADA (si aplica):
{Datos de la actividad que el docente describio}

INSTRUCCIONES:
- Responde en espanol rioplatense, tono amable y profesional.
- Usa lenguaje docente, NO patologizante.
- Cuando recomiendes un dispositivo, siempre explica POR QUE sirve
  para esa actividad y esa necesidad especifica.
- Si no tenes suficiente informacion, pregunta de forma conversacional.
- Mantene las respuestas concisas y practicas (el docente esta en el aula).
```

### Patron de Integracion: Boton "Adaptar para inclusion"

Desde `TeacherLessonPlan.tsx` (planificacion existente), se agrega un boton que:

1. Toma el contexto de la clase ya cargada (asignatura, objetivo, contenido).
2. Navega a `/inclusion/planificar` pasando ese contexto como state.
3. El Inclusion Planner pre-llena los datos de actividad y solo pide seleccion de alumno.
4. Esto evita que el docente re-escriba la informacion de la clase.

---

## 14. Plan de Implementacion Tecnico

### Orden de Implementacion Sugerido

**Paso 1: Base de datos**
- Crear `migrations/008_inclusion.sql` con las 5 tablas
- Crear `seeds/inclusion_seed.sql` con rampas + dispositivos
- Ejecutar migracion y seed

**Paso 2: Backend API**
- Agregar Pydantic models en `main.py`
- Endpoints CRUD: `/ramps`, `/devices`, `/devices/{id}`, `/devices/by-qr/{qr}`
- Endpoints inclusion profiles: `/students/{id}/inclusion-profile`
- Endpoints inclusion plans: `/inclusion-plans`
- Endpoint chat: `POST /inclusion/chat` con system prompt dedicado
- Endpoint recommend: `POST /inclusion/recommend`

**Paso 3: Frontend Types + Store + API**
- Agregar tipos en `types/index.ts`
- Extender `useStore.ts` con slices de inclusion
- Agregar funciones en `services/api.ts`

**Paso 4: Paginas Frontend**
- `InclusionHome.tsx` — entrada al modulo con 4 opciones
- `ValijOnboarding.tsx` — 3 cards de rampas
- `RampDetail.tsx` — dispositivos de una rampa
- `DeviceDetail.tsx` — ficha completa (tambien ruta publica para QR)
- `InclusionPlanner.tsx` — wizard/chat de planificacion
- `InclusionChat.tsx` — asistencia en tiempo real

**Paso 5: Integracion**
- Agregar boton "Inclusion" en `TeacherHome.tsx`
- Agregar boton "Adaptar para inclusion" en `TeacherLessonPlan.tsx`
- Agregar rutas en `App.tsx`
- Verificar responsive mobile

**Paso 6: Datos demo**
- Seed con 3 alumnos con perfil de inclusion precargado
- Verificar flujo completo de demo end-to-end

### Archivos a Modificar (Existentes)

| Archivo | Cambio |
|---|---|
| `main.py` | Agregar ~400 lineas: models, endpoints de inclusion, chat prompt |
| `demo-alizia/src/App.tsx` | Agregar 6 rutas de inclusion |
| `demo-alizia/src/store/useStore.ts` | Agregar slice de inclusion (~50 lineas) |
| `demo-alizia/src/services/api.ts` | Agregar ~10 funciones API de inclusion |
| `demo-alizia/src/types/index.ts` | Agregar ~5 interfaces |
| `demo-alizia/src/pages/TeacherHome.tsx` | Agregar card/boton de "Inclusion" |
| `demo-alizia/src/pages/TeacherLessonPlan.tsx` | Agregar boton "Adaptar para inclusion" |

### Archivos a Crear (Nuevos)

| Archivo | Tipo |
|---|---|
| `migrations/008_inclusion.sql` | Migracion SQL |
| `seeds/inclusion_seed.sql` | Datos semilla |
| `demo-alizia/src/pages/InclusionHome.tsx` | Pagina |
| `demo-alizia/src/pages/ValijOnboarding.tsx` | Pagina |
| `demo-alizia/src/pages/RampDetail.tsx` | Pagina |
| `demo-alizia/src/pages/DeviceDetail.tsx` | Pagina (publica) |
| `demo-alizia/src/pages/InclusionPlanner.tsx` | Pagina |
| `demo-alizia/src/pages/InclusionChat.tsx` | Pagina |

---

## 15. Metricas de Exito

### Demo
- La ministra comprende el producto y su potencial.
- El flujo de planificacion funciona de punta a punta sin errores.
- El escaneo de QR lleva a la ficha correcta.
- Se percibe como practico, facil y escalable.

### MVP
- % de docentes que usan el modulo de inclusion al menos 1 vez por semana.
- # de planificaciones creadas con adaptacion de inclusion.
- # de dispositivos escaneados por QR.
- Diversidad de dispositivos recomendados (no siempre el mismo).
- NPS de docentes sobre la utilidad de las recomendaciones.

### Producto Maduro
- Reduccion de barreras de participacion medida por feedback.
- Frecuencia de uso de dispositivos por valija.
- Evolucion de fichas de alumnos (historial de mejora).
- Cobertura: % de escuelas activas del total que recibieron valija.

---

## Apendice A: Preguntas de Relevamiento de Necesidad (Lenguaje No Patologizante)

Las preguntas estan disenadas para que el docente pueda responder sin necesidad de diagnostico medico:

1. **La condicion del alumno es transitoria o permanente?** (Ej: yeso temporal vs condicion cronica)

2. **Cual de estas situaciones describe mejor al estudiante?**
   - Tiene dificultad para mover o controlar sus manos o brazos
   - Tiene dificultad para comunicarse o expresar respuestas
   - Tiene dificultad para mantener la atencion o regular emociones
   - Tiene dificultad para acceder a la tecnologia digital
   - Tiene varias de estas dificultades
   - No estoy seguro / quiero explorar opciones

3. **Queres contarme algo mas sobre este alumno?** (campo libre opcional)

---

## Apendice B: Ejemplo de Ficha de Dispositivo

### Pinza de Escritura (Adaptador de Escritura)

| Campo | Valor |
|---|---|
| **Nombre** | Pinza de escritura |
| **Rampa** | Didactico-Pedagogica |
| **Imagen** | [foto del dispositivo] |
| **Descripcion** | Favorece una postura correcta de los dedos al sostener el lapiz |
| **Para quien** | Estudiantes con dificultades cognitivas (dispraxia) o motoras |
| **Como usar** | Colocar la pinza en el lapiz, el alumno inserta los dedos en las guias. No requiere configuracion. |
| **En que actividades** | Escritura, dictado, dibujo, cualquier actividad con lapiz |
| **Cantidad en valija** | 3 unidades |
| **Fundamentacion** | Permite participar sin restriccion, reduce frustracion, da autonomia inmediata, se integra facilmente al trabajo grupal |

---

## Apendice C: Ejemplo de Output de Alicia (Recomendacion)

> **Alicia dice:**
>
> "Por lo que me contas, el estudiante necesita un insumo que lo ayude a sujetar de forma adaptada la lapicera para realizar la actividad de dictado de texto."
>
> "Te recomiendo comenzar con el **Adaptador de Escritura** (Pinza de escritura), un recurso de la **Rampa Didactico-Pedagogica** del kit."
>
> **Por que:**
> - Permite participar de la actividad sin ninguna restriccion
> - Reduce frustracion
> - Da autonomia inmediata
> - Se integra facilmente al trabajo grupal
>
> **Como usarlo:**
> Coloca la pinza en el lapiz del alumno. Tiene guias para los dedos que ayudan a mantener la postura correcta. No requiere configuracion adicional.
>
> [Ver ficha completa] [Buscar otra herramienta] [Planificar otra actividad]
