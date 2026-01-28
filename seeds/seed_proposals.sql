-- Seed data for Proposals: "Simulador Anatómico"

INSERT INTO proposals (name, description, duration_weeks, tools, curriculum_card, alizia_info, initial_agreements, stages, annexes, status) VALUES
(
    'Simulador Anatómico',
    'Proyecto de Pensamiento Computacional que integra ciencias naturales y programación. Los estudiantes construirán un simulador interactivo del cuerpo humano usando Scratch, explorando sistemas anatómicos mientras desarrollan habilidades de programación.',
    8,
    '["Scratch", "micro:bit", "Pilas Bloques"]',
    '{
        "objectives": [
            "Comprender el funcionamiento de un aparato del cuerpo humano",
            "Desarrollar habilidades de pensamiento computacional",
            "Crear un simulador interactivo usando programación por bloques",
            "Integrar conocimientos de ciencias naturales con tecnología"
        ],
        "competencies": [
            "Pensamiento computacional y algorítmico",
            "Resolución de problemas",
            "Trabajo colaborativo",
            "Comunicación científica",
            "Creatividad e innovación tecnológica"
        ],
        "curricular_links": [
            "Ciencias Naturales: Sistemas del cuerpo humano",
            "Matemáticas: Variables, operaciones, porcentajes",
            "Tecnología: Programación por bloques",
            "Lengua: Producción de textos explicativos"
        ],
        "resources": [
            {"type": "link", "title": "Repositorio de recursos abiertos Ceibal", "url": "https://rea.ceibal.edu.uy/"},
            {"type": "link", "title": "Uruguay Educa Recursos", "url": "https://uruguayeduca.anep.edu.uy/recursos-educativos"}
        ]
    }',
    '{
        "pc_objectives": [
            "Descomponer un sistema complejo (aparato anatómico) en componentes manejables",
            "Identificar patrones en procesos biológicos para su modelado computacional",
            "Abstraer características esenciales para la simulación",
            "Diseñar algoritmos que representen procesos fisiológicos"
        ],
        "stage_structure": "El proyecto se desarrolla en 7 etapas progresivas: desde la investigación del aparato elegido hasta la construcción del simulador completo con variables, parámetros y simulación de factores externos.",
        "spatial_organization": "Se recomienda trabajar en parejas o pequeños grupos (3-4 estudiantes) para fomentar el trabajo colaborativo. Cada grupo puede elegir un aparato diferente o trabajar en diferentes aspectos del mismo aparato.",
        "da_participation": "El Docente de Aula (DA) tiene un rol fundamental como facilitador del aprendizaje. Se espera que guíe las investigaciones, valide conceptos científicos, y apoye la integración entre los contenidos curriculares y el proyecto de programación.",
        "example_project_url": "https://scratch.mit.edu/projects/438140508",
        "bitacora_url": "https://docs.google.com/presentation/d/1gW0AjpE72d9d_3um_VLmCy87PsLIS3UVRtf2lRh6wOs/edit?usp=sharing"
    }',
    '[
        {
            "id": "aparato_elegido",
            "title": "Aparato a trabajar",
            "description": "Selecciona el aparato del cuerpo humano que los estudiantes investigarán y simularán. Considera los contenidos curriculares que estés trabajando y los intereses del grupo.",
            "responsible_type": "da_solo",
            "options": ["Aparato respiratorio", "Aparato circulatorio", "Aparato digestivo", "Sistema nervioso", "Sistema muscular", "Otro"],
            "alizia_context": {
                "valid_options": [
                    {"value": "Aparato respiratorio", "element": "Aire/Oxígeno", "notes": "Proyecto ejemplo disponible, muy visual"},
                    {"value": "Aparato circulatorio", "element": "Sangre/Glóbulos", "notes": "Buen potencial para variables numéricas"},
                    {"value": "Aparato digestivo", "element": "Alimento/Nutrientes", "notes": "Proceso secuencial claro"}
                ],
                "knowledge": [
                    "Los tres aparatos principales (respiratorio, circulatorio, digestivo) están vinculados a la nutrición humana",
                    "El proyecto tiene ejemplos desarrollados especialmente para el aparato respiratorio",
                    "Es importante que el aparato elegido esté alineado con lo que se trabaja en Ciencias del Ambiente"
                ],
                "guiding_questions": [
                    "¿Qué aparato están trabajando actualmente en Ciencias del Ambiente?",
                    "¿Los estudiantes ya tienen conocimientos previos sobre algún aparato en particular?",
                    "¿Hay algún aparato que genere especial curiosidad en el grupo?"
                ],
                "warning_signals": [
                    {"trigger": "quiere trabajar dos aparatos", "response": "Explicar que el proyecto está diseñado para profundizar en uno solo, pero se puede mencionar las conexiones entre sistemas"},
                    {"trigger": "elige sistema nervioso o muscular", "response": "Advertir que estos son más complejos y hay menos recursos de ejemplo disponibles"}
                ],
                "stance": "SUGERENTE - El DA conoce mejor a su grupo y el currículum",
                "stance_examples": [
                    "Los tres aparatos funcionan muy bien para este proyecto. ¿Cuál están trabajando en Ciencias?"
                ],
                "acceptance_criteria": "El DA expresa claramente cuál aparato eligió para trabajar"
            }
        },
        {
            "id": "proyecto_aula",
            "title": "Proyecto de aula y pregunta de investigación",
            "description": "Define el proyecto de aula que enmarca esta propuesta y formula la pregunta de investigación que guiará el trabajo de los estudiantes.",
            "responsible_type": "da_solo",
            "placeholder": "Ej: ¿Cómo funciona nuestro sistema respiratorio y qué factores afectan su funcionamiento?",
            "alizia_context": {
                "knowledge": [
                    "Una buena pregunta de investigación debe ser abierta, relevante y alcanzable",
                    "La pregunta debe conectar el contenido científico con la vida cotidiana de los estudiantes",
                    "El proyecto de aula da contexto y sentido al simulador que construirán"
                ],
                "guiding_questions": [
                    "¿Qué proyecto de aula están desarrollando actualmente?",
                    "¿Qué pregunta podría despertar la curiosidad de los estudiantes sobre este aparato?",
                    "¿Cómo se conecta este tema con la vida cotidiana de los niños?"
                ],
                "warning_signals": [
                    {"trigger": "pregunta muy cerrada (sí/no)", "response": "Sugerir reformular para que sea más abierta y permita exploración"},
                    {"trigger": "pregunta demasiado amplia", "response": "Ayudar a acotar el alcance para que sea manejable en 8 semanas"}
                ],
                "stance": "ORIENTADOR - Ayudar a formular una buena pregunta sin imponer",
                "stance_examples": [
                    "Esa es una pregunta interesante. ¿Cómo podríamos hacerla más específica para el simulador?",
                    "Me gusta la dirección. ¿Qué aspectos del aparato les gustaría que los estudiantes descubran?"
                ],
                "acceptance_criteria": "El DA formula una pregunta de investigación clara y apropiada para el nivel"
            }
        },
        {
            "id": "destinatarios",
            "title": "Destinatarios del simulador",
            "description": "¿A quién estará dirigido el simulador que construyan los estudiantes? Esto ayudará a definir el nivel de complejidad y el enfoque comunicativo.",
            "responsible_type": "da_solo",
            "options": ["Compañeros del mismo grado", "Estudiantes de grados menores", "Familias", "Comunidad escolar", "Otro"],
            "alizia_context": {
                "valid_options": [
                    {"value": "Compañeros del mismo grado", "notes": "Nivel de complejidad estándar"},
                    {"value": "Estudiantes de grados menores", "notes": "Requiere simplificar explicaciones, muy motivador"},
                    {"value": "Familias", "notes": "Buen cierre para jornadas de puertas abiertas"},
                    {"value": "Comunidad escolar", "notes": "Permite presentación en feria de ciencias"}
                ],
                "knowledge": [
                    "El destinatario define el nivel de complejidad y el lenguaje del simulador",
                    "Crear para otros es muy motivador para los estudiantes",
                    "La elección impacta en cómo se documentará y presentará el proyecto"
                ],
                "guiding_questions": [
                    "¿Tienen algún evento escolar donde podrían presentar el simulador?",
                    "¿Los estudiantes han creado productos para otros públicos antes?",
                    "¿Qué audiencia los motivaría más?"
                ],
                "stance": "SUGERENTE - El DA conoce el contexto escolar",
                "acceptance_criteria": "El DA indica claramente quiénes serán los destinatarios del simulador"
            }
        },
        {
            "id": "experiencia_previa",
            "title": "Experiencia previa del grupo",
            "description": "Describe brevemente la experiencia previa del grupo con programación y con el contenido científico relacionado.",
            "responsible_type": "da_solo",
            "placeholder": "Ej: Los estudiantes han trabajado con Scratch en proyectos simples y conocen las partes básicas del aparato respiratorio.",
            "alizia_context": {
                "knowledge": [
                    "La experiencia previa determina el ritmo y profundidad del proyecto",
                    "Es importante conocer tanto la experiencia en programación como en el contenido científico",
                    "Grupos sin experiencia en Scratch necesitarán más tiempo en etapas iniciales"
                ],
                "guiding_questions": [
                    "¿Han trabajado antes con Scratch u otra herramienta de programación?",
                    "¿Qué conceptos del aparato elegido ya conocen los estudiantes?",
                    "¿Hay estudiantes con experiencia que puedan ayudar a sus compañeros?"
                ],
                "warning_signals": [
                    {"trigger": "sin experiencia en programación", "response": "Tranquilizar: el proyecto está diseñado para principiantes, incluiremos actividades de familiarización"},
                    {"trigger": "grupo muy heterogéneo", "response": "Sugerir trabajo en parejas estratégicas para aprovechar las diferencias"}
                ],
                "stance": "RECEPTIVO - Escuchar sin juzgar el nivel del grupo",
                "acceptance_criteria": "El DA describe la experiencia previa del grupo de forma clara"
            }
        },
        {
            "id": "dinamica_vc",
            "title": "Dinámica de las videoconferencias",
            "description": "Acordemos cómo serán las instancias de videoconferencia durante el proyecto: frecuencia, duración y formato.",
            "responsible_type": "conjunto",
            "default_suggestion": "Una videoconferencia semanal de 40 minutos con todo el grupo, más instancias de consulta opcional.",
            "alizia_context": {
                "valid_options": [
                    {"value": "Semanal 40 min", "notes": "Formato estándar, permite seguimiento cercano"},
                    {"value": "Quincenal 60 min", "notes": "Para grupos con más autonomía"},
                    {"value": "Por etapa", "notes": "Una VC al inicio de cada etapa"}
                ],
                "knowledge": [
                    "Las videoconferencias son fundamentales para el acompañamiento del proyecto",
                    "El formato puede ajustarse según las necesidades del grupo",
                    "Es importante acordar también canales de comunicación asincrónica"
                ],
                "guiding_questions": [
                    "¿Qué días y horarios funcionan mejor para el grupo?",
                    "¿Prefieren sesiones más frecuentes y cortas o menos frecuentes y más largas?",
                    "¿Cómo se comunican usualmente con docentes remotos?"
                ],
                "warning_signals": [
                    {"trigger": "quiere muy pocas videoconferencias", "response": "Explicar la importancia del acompañamiento, especialmente en etapas clave"},
                    {"trigger": "horarios muy limitados", "response": "Buscar alternativas creativas, como grabar sesiones o hacer consultas asincrónicas"}
                ],
                "stance": "FIRME pero FLEXIBLE - Asegurar acompañamiento mínimo necesario",
                "stance_examples": [
                    "Necesitamos al menos un encuentro semanal para poder acompañar bien el proceso. ¿Qué día les funciona mejor?",
                    "Podemos ser flexibles con el formato, pero es importante mantener comunicación regular."
                ],
                "acceptance_criteria": "Ambos acuerdan frecuencia, duración y formato de las videoconferencias"
            }
        },
        {
            "id": "cantidad_organos",
            "title": "Cantidad de órganos a incorporar",
            "description": "Definamos cuántos órganos incluirá el simulador. Esto depende del tiempo disponible y la complejidad deseada.",
            "responsible_type": "conjunto",
            "options": ["1-2 órganos (básico)", "3-4 órganos (intermedio)", "5+ órganos (avanzado)"],
            "default_suggestion": "3-4 órganos (intermedio)",
            "alizia_context": {
                "valid_options": [
                    {"value": "1-2 órganos", "notes": "Recomendado para grupos sin experiencia o tiempo limitado"},
                    {"value": "3-4 órganos", "notes": "Nivel intermedio, balance ideal entre profundidad y alcance"},
                    {"value": "5+ órganos", "notes": "Solo para grupos con experiencia previa en Scratch"}
                ],
                "knowledge": [
                    "Más órganos implica más tiempo de desarrollo y mayor complejidad",
                    "Es mejor un simulador con pocos órganos bien desarrollados que muchos incompletos",
                    "Se puede empezar con pocos y agregar más si hay tiempo"
                ],
                "guiding_questions": [
                    "Considerando la experiencia del grupo, ¿qué nivel de complejidad es realista?",
                    "¿Cuántas clases tienen disponibles para el proyecto?"
                ],
                "warning_signals": [
                    {"trigger": "quiere 5+ sin experiencia", "response": "Advertir sobre la complejidad y sugerir comenzar con menos, con posibilidad de ampliar"},
                    {"trigger": "quiere solo 1 órgano", "response": "Puede ser válido, pero explorar si hay margen para al menos 2 para mostrar interacción"}
                ],
                "stance": "CO-DECISOR - Aportar criterio técnico sobre factibilidad",
                "stance_examples": [
                    "Dado que el grupo no tiene experiencia previa, sugiero comenzar con 2-3 órganos. Siempre podemos agregar más.",
                    "3-4 órganos es un buen balance. ¿Te parece bien empezar con ese objetivo?"
                ],
                "acceptance_criteria": "Ambos acuerdan la cantidad de órganos a incluir en el simulador"
            }
        }
    ]',
    '[
        {
            "number": 1,
            "name": "El aparato a investigar",
            "duration_classes": 2,
            "description": "Los estudiantes investigan el aparato elegido: sus órganos, funciones y procesos principales. Utilizan recursos audiovisuales y documentan sus hallazgos en la bitácora.",
            "decisions": [
                {
                    "id": "recorrido_didactico",
                    "title": "Recorrido didáctico",
                    "description": "¿Cómo organizarás la investigación? ¿Qué recursos usarán los estudiantes?",
                    "responsible_type": "da_solo",
                    "alizia_context": {
                        "knowledge": [
                            "Los recursos del anexo están organizados por aparato",
                            "Es importante combinar videos, textos e imágenes para diferentes estilos de aprendizaje",
                            "La bitácora es fundamental para registrar los aprendizajes"
                        ],
                        "guiding_questions": [
                            "¿Qué recursos del anexo planeas utilizar?",
                            "¿Trabajarán en grupos o de forma individual?",
                            "¿Cómo registrarán sus hallazgos en la bitácora?"
                        ],
                        "stance": "SUGERENTE - Ofrecer recursos pero respetar la planificación del DA",
                        "acceptance_criteria": "El DA describe cómo organizará la investigación y qué recursos usará"
                    }
                },
                {
                    "id": "nivel_profundidad",
                    "title": "Nivel de profundidad",
                    "description": "¿Hasta qué nivel de detalle llegarán en la investigación?",
                    "responsible_type": "conjunto",
                    "alizia_context": {
                        "valid_options": [
                            {"value": "Básico", "notes": "Órganos principales y funciones generales"},
                            {"value": "Intermedio", "notes": "Procesos detallados, algunas interacciones"},
                            {"value": "Avanzado", "notes": "Nivel celular, conexiones con otros sistemas"}
                        ],
                        "knowledge": [
                            "El nivel de profundidad debe ser coherente con el grado y la cantidad de órganos acordada",
                            "Es mejor profundizar en menos conceptos que abarcar muchos superficialmente"
                        ],
                        "guiding_questions": [
                            "¿Qué nivel de detalle es apropiado para el grado?",
                            "¿Llegaremos hasta nivel celular o nos quedamos en órganos?"
                        ],
                        "stance": "CO-DECISOR - Asegurar que sea alcanzable y significativo",
                        "acceptance_criteria": "Ambos acuerdan el nivel de detalle de la investigación"
                    }
                },
                {
                    "id": "imagenes_referencia",
                    "title": "Imágenes de referencia",
                    "description": "¿Qué imágenes o esquemas usarán como referencia para el simulador?",
                    "responsible_type": "da_solo",
                    "alizia_context": {
                        "knowledge": [
                            "El banco de imágenes está disponible en la carpeta de recursos",
                            "Los estudiantes pueden dibujar sus propios órganos en Scratch",
                            "Las imágenes deben ser claras y apropiadas para el nivel"
                        ],
                        "guiding_questions": [
                            "¿Usarán imágenes del banco de recursos o los estudiantes dibujarán?",
                            "¿Qué tipo de representación prefieren: realista o esquemática?"
                        ],
                        "stance": "SUGERENTE - Ofrecer opciones sin imponer",
                        "acceptance_criteria": "El DA indica qué tipo de imágenes usarán como referencia"
                    }
                }
            ],
            "resources": [
                {"type": "scratch", "title": "Avance Etapa 1", "url": "https://scratch.mit.edu/projects/628215782"},
                {"type": "template", "title": "Bitácora", "url": "https://docs.google.com/presentation/d/1WuWOt1veaoISH_gGPURvufo3kR5_P5z8e57Yk5x-UxE/edit?usp=sharing"},
                {"type": "link", "title": "Banco de imágenes (carpeta)", "url": "https://drive.google.com/drive/folders/1m3B5O6V8qKRJvHFvjrTjXDXyp8mvqHIK?usp=sharing"},
                {"type": "scratch", "title": "Ejemplo con órganos dibujados en Scratch", "url": "https://scratch.mit.edu/projects/628514005"},
                {"type": "link", "title": "Google Maps (para ejemplo de mapas)", "url": "https://www.google.com.ar/maps/"}
            ]
        },
        {
            "number": 2,
            "name": "Animación del aparato",
            "duration_classes": 2,
            "description": "Comienzan a programar la representación visual del aparato con sus órganos animados. Trabajan en Scratch para crear las primeras animaciones del sistema elegido.",
            "decisions": [
                {
                    "id": "secuencia_proceso",
                    "title": "Secuencia del proceso",
                    "description": "¿En qué orden se animarán los órganos? ¿Seguirá el flujo natural del proceso biológico?",
                    "responsible_type": "da_solo",
                    "alizia_context": {
                        "knowledge": [
                            "Es recomendable seguir el flujo natural del proceso biológico",
                            "Por ejemplo: en respiratorio, aire entra por nariz → tráquea → pulmones",
                            "La secuencia ayuda a los estudiantes a comprender el proceso completo"
                        ],
                        "guiding_questions": [
                            "¿Cuál es el recorrido natural del proceso en el aparato elegido?",
                            "¿Los estudiantes ya comprenden esta secuencia?"
                        ],
                        "stance": "SUGERENTE - Orientar hacia el flujo natural pero flexibilizar",
                        "acceptance_criteria": "El DA define el orden en que se animarán los órganos"
                    }
                },
                {
                    "id": "simultaneidad_secuencia",
                    "title": "Simultaneidad vs secuencia",
                    "description": "¿Las animaciones serán simultáneas o secuenciales? Esto afecta la complejidad del código.",
                    "responsible_type": "conjunto",
                    "alizia_context": {
                        "valid_options": [
                            {"value": "Secuencial", "notes": "Más simple de programar, más fácil de entender"},
                            {"value": "Simultáneo", "notes": "Más realista pero requiere manejo de eventos paralelos"},
                            {"value": "Mixto", "notes": "Algunas animaciones juntas, otras en secuencia"}
                        ],
                        "knowledge": [
                            "Las animaciones simultáneas requieren usar \"enviar mensaje\" y eventos en Scratch",
                            "Para grupos principiantes, la secuencia es más manejable",
                            "Se puede empezar secuencial y agregar simultaneidad después"
                        ],
                        "guiding_questions": [
                            "¿El grupo tiene experiencia con eventos y mensajes en Scratch?",
                            "¿Qué se ajusta mejor al proceso real del aparato?"
                        ],
                        "stance": "CO-DECISOR - Aportar criterio técnico sobre complejidad",
                        "stance_examples": [
                            "Para un grupo sin experiencia, sugiero empezar con animaciones secuenciales. ¿Qué te parece?",
                            "Si el proceso real es simultáneo, podemos intentarlo, pero será más desafiante."
                        ],
                        "acceptance_criteria": "Ambos acuerdan si las animaciones serán secuenciales, simultáneas o mixtas"
                    }
                }
            ],
            "resources": [
                {"type": "scratch", "title": "Avance Etapa 2", "url": "https://scratch.mit.edu/projects/628222181"},
                {"type": "template", "title": "Bitácora", "url": "https://docs.google.com/presentation/d/1WuWOt1veaoISH_gGPURvufo3kR5_P5z8e57Yk5x-UxE/edit?usp=sharing"}
            ]
        },
        {
            "number": 3,
            "name": "¿Qué es un simulador?",
            "duration_classes": 2,
            "description": "Exploran qué es un simulador, analizan ejemplos interactivos (PhET, Stellarium) y definen las características que tendrá el suyo. Trabajan con consignas de predicción.",
            "decisions": [
                {
                    "id": "simulador_explorar",
                    "title": "Simulador a explorar",
                    "description": "¿Qué simulador usarán como ejemplo para analizar?",
                    "responsible_type": "conjunto",
                    "alizia_context": {
                        "valid_options": [
                            {"value": "PhET - Estados de la materia", "notes": "Visual, interactivo, muestra variables"},
                            {"value": "PhET - Movimiento de proyectil", "notes": "Muestra parámetros modificables"},
                            {"value": "Simulación COVID", "notes": "Ejemplo en Scratch, más cercano al proyecto"},
                            {"value": "Stellarium", "notes": "Simulador complejo, bueno para inspirar"}
                        ],
                        "knowledge": [
                            "Los simuladores PhET son excelentes para mostrar interactividad y variables",
                            "Los ejemplos en Scratch son más cercanos a lo que construirán",
                            "Es importante que analicen qué hace que un simulador sea bueno"
                        ],
                        "guiding_questions": [
                            "¿Qué tipo de interactividad quieres que vean los estudiantes?",
                            "¿Prefieren un ejemplo en Scratch o uno más profesional para inspirar?"
                        ],
                        "stance": "CO-DECISOR - Ambos elegimos el ejemplo más apropiado",
                        "acceptance_criteria": "Ambos acuerdan qué simulador(es) usarán como ejemplo"
                    }
                },
                {
                    "id": "consignas_prediccion",
                    "title": "Consignas de predicción",
                    "description": "¿Qué preguntas guiarán la exploración del simulador ejemplo?",
                    "responsible_type": "da_solo",
                    "alizia_context": {
                        "knowledge": [
                            "Las consignas de predicción ayudan a que los estudiantes observen con propósito",
                            "Preguntas como \"¿Qué pasará si...?\" activan el pensamiento científico",
                            "Es importante que relacionen lo observado con su propio simulador"
                        ],
                        "guiding_questions": [
                            "¿Qué aspectos del simulador quieres que observen con atención?",
                            "¿Cómo conectarán lo que observen con lo que van a construir?"
                        ],
                        "stance": "SUGERENTE - Ofrecer ejemplos de preguntas sin imponer",
                        "stance_examples": [
                            "Podrías preguntar: ¿Qué pasa cuando movemos este control? ¿Cómo responde el simulador?",
                            "Una buena consigna sería: Antes de probarlo, predigan qué pasará si..."
                        ],
                        "acceptance_criteria": "El DA define las preguntas que guiarán la exploración"
                    }
                }
            ],
            "resources": [
                {"type": "phet", "title": "Proyecto PhET (general)", "url": "https://phet.colorado.edu/es/simulations/browse"},
                {"type": "phet", "title": "PhET - Estado de la materia", "url": "https://phet.colorado.edu/sims/html/states-of-matter-basics/latest/states-of-matter-basics_es.html"},
                {"type": "phet", "title": "PhET - Movimiento de un proyectil", "url": "https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_es.html"},
                {"type": "phet", "title": "PhET - Ondas", "url": "https://phet.colorado.edu/sims/html/waves-intro/latest/waves-intro_es.html"},
                {"type": "scratch", "title": "Simulación COVID", "url": "https://scratch.mit.edu/projects/376995324/"},
                {"type": "scratch", "title": "Simulador de contagio", "url": "https://scratch.mit.edu/projects/377300767/"},
                {"type": "phet", "title": "PhET para primaria", "url": "https://phet.colorado.edu/es/simulations/filter?levels=elementary-school&type=html&sort=alpha&view=grid"},
                {"type": "link", "title": "Stellarium (astronomía)", "url": "https://stellarium-web.org/"}
            ]
        },
        {
            "number": 4,
            "name": "Simulación del elemento fundamental",
            "duration_classes": 2,
            "description": "Programan la simulación del elemento principal usando condicionales (ej: oxígeno en respiratorio, sangre en circulatorio). Se refuerzan conceptos con Pilas Bloques.",
            "decisions": [
                {
                    "id": "elemento_definido",
                    "title": "Elemento a simular",
                    "description": "¿Cuál será el elemento fundamental que simularán? (ej: molécula de oxígeno, glóbulo rojo)",
                    "responsible_type": "da_solo",
                    "alizia_context": {
                        "valid_options": [
                            {"value": "Molécula de oxígeno", "element": "Respiratorio", "notes": "Visual, movimiento claro"},
                            {"value": "Glóbulo rojo", "element": "Circulatorio", "notes": "Permite mostrar transporte"},
                            {"value": "Partícula de alimento", "element": "Digestivo", "notes": "Transformación visible"}
                        ],
                        "knowledge": [
                            "El elemento fundamental es lo que \"viaja\" por el aparato",
                            "Debe ser algo visual y comprensible para los estudiantes",
                            "Su comportamiento será controlado por condicionales (si toca X, entonces Y)"
                        ],
                        "guiding_questions": [
                            "¿Qué elemento representa mejor el proceso del aparato elegido?",
                            "¿Cómo se moverá este elemento por los órganos?"
                        ],
                        "stance": "SUGERENTE - Orientar hacia opciones pedagógicamente sólidas",
                        "acceptance_criteria": "El DA define qué elemento fundamental simularán"
                    }
                },
                {
                    "id": "acceso_pilas_bloques",
                    "title": "Uso de Pilas Bloques",
                    "description": "¿Incorporaremos desafíos de Pilas Bloques para reforzar conceptos de condicionales?",
                    "responsible_type": "conjunto",
                    "alizia_context": {
                        "valid_options": [
                            {"value": "Sí, antes de Scratch", "notes": "Introduce condicionales de forma guiada"},
                            {"value": "Sí, como apoyo", "notes": "Para estudiantes que necesiten refuerzo"},
                            {"value": "No es necesario", "notes": "Si ya manejan condicionales"}
                        ],
                        "knowledge": [
                            "Pilas Bloques tiene desafíos específicos para condicionales",
                            "Es útil especialmente para grupos sin experiencia previa",
                            "Los desafíos están en el Anexo 2"
                        ],
                        "guiding_questions": [
                            "¿Los estudiantes ya comprenden el concepto de condicional (si-entonces)?",
                            "¿Tienen tiempo para incorporar actividades adicionales?"
                        ],
                        "stance": "CO-DECISOR - Evaluar juntos si es necesario",
                        "acceptance_criteria": "Ambos acuerdan si usarán Pilas Bloques y cómo"
                    }
                }
            ],
            "resources": [
                {"type": "link", "title": "Pilas Bloques", "url": "http://pilasbloques.program.ar"},
                {"type": "scratch", "title": "Etapa 4 - con un sensor", "url": "https://scratch.mit.edu/projects/628226253"},
                {"type": "template", "title": "Bitácora", "url": "https://docs.google.com/presentation/d/1WuWOt1veaoISH_gGPURvufo3kR5_P5z8e57Yk5x-UxE/edit?usp=sharing"},
                {"type": "link", "title": "Edu ciencias", "url": "https://www.ceibal.edu.uy/es/articulo/que-es-edu"},
                {"type": "video", "title": "Video PCtubers 6 - Condicionales", "url": "https://drive.google.com/file/d/1aGTakvb3FuwsNVb8oGJ8BYvioVRhemni/view?usp=sharing"},
                {"type": "link", "title": "Manual Ciencias de la Computación 1er Ciclo", "url": "http://program.ar/manual-primer-ciclo-primaria/"}
            ]
        },
        {
            "number": 5,
            "name": "Variables en el simulador",
            "duration_classes": 2,
            "description": "Incorporan variables para representar estados y cantidades (ej: nivel de oxígeno, ritmo cardíaco). Aprenden a usar operaciones de incremento y decremento.",
            "decisions": [
                {
                    "id": "operacion_definida",
                    "title": "Operación con variables",
                    "description": "¿Qué operaciones realizarán las variables? (incremento, decremento, porcentajes)",
                    "responsible_type": "da_solo",
                    "alizia_context": {
                        "valid_options": [
                            {"value": "Incremento simple", "notes": "+1 cada vez, más sencillo"},
                            {"value": "Incremento y decremento", "notes": "Sube y baja según condiciones"},
                            {"value": "Porcentajes", "notes": "Más complejo, requiere multiplicación"}
                        ],
                        "knowledge": [
                            "El incremento (+1) es el más simple de implementar",
                            "El decremento permite simular consumo o desgaste",
                            "Los porcentajes agregan realismo pero complejidad matemática"
                        ],
                        "guiding_questions": [
                            "¿Qué nivel de matemáticas manejan los estudiantes?",
                            "¿Qué tipo de cambio representa mejor el proceso biológico?"
                        ],
                        "stance": "SUGERENTE - Orientar según nivel del grupo",
                        "acceptance_criteria": "El DA define qué operaciones usarán las variables"
                    }
                },
                {
                    "id": "dinamica_acelerando",
                    "title": "Dinámica de aceleración",
                    "description": "¿Cómo representarán el aumento de actividad? (ej: pulso acelerado al ejercitarse)",
                    "responsible_type": "conjunto",
                    "alizia_context": {
                        "valid_options": [
                            {"value": "Velocidad de animación", "notes": "Más rápido = más actividad"},
                            {"value": "Cantidad de elementos", "notes": "Más partículas = más actividad"},
                            {"value": "Cambio de color", "notes": "Visual, sin cambiar código complejo"}
                        ],
                        "knowledge": [
                            "La velocidad de animación es intuitiva y fácil de implementar",
                            "Más elementos requiere clonación en Scratch",
                            "El color es visual pero no representa cantidad"
                        ],
                        "guiding_questions": [
                            "¿Qué representación visual sería más clara para los destinatarios?",
                            "¿El grupo tiene experiencia con clonación en Scratch?"
                        ],
                        "stance": "CO-DECISOR - Encontrar balance entre realismo y factibilidad",
                        "acceptance_criteria": "Ambos acuerdan cómo representarán la aceleración"
                    }
                }
            ],
            "resources": [
                {"type": "scratch", "title": "Etapa 5 - con una variable", "url": "https://scratch.mit.edu/projects/628416104"}
            ]
        },
        {
            "number": 6,
            "name": "Parámetros y simulación",
            "duration_classes": 2,
            "description": "Agregan parámetros modificables y simulan factores externos que afectan el sistema (ejercicio, enfermedad, altitud). Pueden incorporar fórmulas matemáticas.",
            "decisions": [
                {
                    "id": "factores_externos",
                    "title": "Factores externos",
                    "description": "¿Qué factores externos simularán? (ejercicio, enfermedad, altitud, etc.)",
                    "responsible_type": "da_solo",
                    "alizia_context": {
                        "valid_options": [
                            {"value": "Ejercicio físico", "element": "Todos", "notes": "Aumenta ritmo cardíaco y respiración"},
                            {"value": "Enfermedad/Obstrucción", "element": "Todos", "notes": "Reduce eficiencia del sistema"},
                            {"value": "Altitud", "element": "Respiratorio", "notes": "Menos oxígeno disponible"},
                            {"value": "Tipo de alimento", "element": "Digestivo", "notes": "Diferentes tiempos de digestión"}
                        ],
                        "knowledge": [
                            "Los factores externos hacen el simulador más interactivo",
                            "Deben tener efectos claros y medibles en las variables",
                            "Se implementan como controles deslizantes o botones"
                        ],
                        "guiding_questions": [
                            "¿Qué factores son relevantes para el aparato elegido?",
                            "¿Qué factores conocen los estudiantes de su vida cotidiana?"
                        ],
                        "stance": "SUGERENTE - Conectar con la vida real de los estudiantes",
                        "acceptance_criteria": "El DA define qué factores externos incluirá el simulador"
                    }
                },
                {
                    "id": "formulas_numericas",
                    "title": "Fórmulas numéricas",
                    "description": "¿Incorporarán fórmulas matemáticas para los cálculos del simulador?",
                    "responsible_type": "conjunto",
                    "alizia_context": {
                        "valid_options": [
                            {"value": "No, valores aproximados", "notes": "Más simple, suficiente para mostrar conceptos"},
                            {"value": "Sí, fórmulas simples", "notes": "Operaciones básicas (+, -, ×)"},
                            {"value": "Sí, fórmulas reales", "notes": "Datos científicos reales, más complejo"}
                        ],
                        "knowledge": [
                            "Las fórmulas agregan realismo pero complejidad",
                            "Se pueden usar valores aproximados que mantengan las proporciones",
                            "Es una oportunidad de integración con matemáticas"
                        ],
                        "guiding_questions": [
                            "¿Quieres aprovechar para integrar contenidos de matemáticas?",
                            "¿Los estudiantes manejan las operaciones necesarias?"
                        ],
                        "stance": "CO-DECISOR - Evaluar factibilidad y valor pedagógico",
                        "acceptance_criteria": "Ambos acuerdan el nivel de precisión matemática"
                    }
                }
            ],
            "resources": [
                {"type": "scratch", "title": "Etapa 6 - con un parámetro", "url": "https://scratch.mit.edu/projects/628447232"},
                {"type": "template", "title": "Bitácora", "url": "https://docs.google.com/presentation/d/1WuWOt1veaoISH_gGPURvufo3kR5_P5z8e57Yk5x-UxE/edit?usp=sharing"}
            ]
        },
        {
            "number": 7,
            "name": "Cierre del proyecto",
            "duration_classes": 2,
            "description": "Finalizan el simulador, lo documentan en la bitácora y lo comparten con los destinatarios elegidos. Publican en el Estudio de Pensamiento Computacional de Ceibal.",
            "decisions": [
                {
                    "id": "ideas_socializacion",
                    "title": "Ideas de socialización",
                    "description": "¿Cómo compartirán el proyecto con los destinatarios? (presentación, feria, video)",
                    "responsible_type": "da_solo",
                    "alizia_context": {
                        "valid_options": [
                            {"value": "Presentación en vivo", "notes": "Los estudiantes explican su simulador"},
                            {"value": "Feria de ciencias", "notes": "Stands con los proyectos funcionando"},
                            {"value": "Video explicativo", "notes": "Grabación para compartir ampliamente"},
                            {"value": "Jornada de puertas abiertas", "notes": "Invitar familias a ver los proyectos"}
                        ],
                        "knowledge": [
                            "La socialización es fundamental para dar sentido al trabajo",
                            "Los estudiantes deben poder explicar qué hicieron y qué aprendieron",
                            "Es importante que los destinatarios puedan interactuar con el simulador"
                        ],
                        "guiding_questions": [
                            "¿Hay algún evento escolar próximo donde presentar?",
                            "¿Cómo se sienten los estudiantes presentando su trabajo?"
                        ],
                        "stance": "SUGERENTE - Apoyar las ideas del DA",
                        "acceptance_criteria": "El DA describe cómo se compartirá el proyecto"
                    }
                },
                {
                    "id": "forma_cierre",
                    "title": "Forma de cierre",
                    "description": "¿Cómo celebraremos y evaluaremos el trabajo realizado?",
                    "responsible_type": "conjunto",
                    "alizia_context": {
                        "valid_options": [
                            {"value": "Autoevaluación grupal", "notes": "Los estudiantes reflexionan sobre su proceso"},
                            {"value": "Rúbrica de evaluación", "notes": "Criterios claros de logro"},
                            {"value": "Celebración y reconocimiento", "notes": "Diplomas, menciones especiales"},
                            {"value": "Publicación en estudio Ceibal", "notes": "Compartir con comunidad más amplia"}
                        ],
                        "knowledge": [
                            "Es importante celebrar los logros, no solo evaluar",
                            "La autoevaluación desarrolla metacognición",
                            "Publicar en el estudio de Ceibal da visibilidad al trabajo"
                        ],
                        "guiding_questions": [
                            "¿Cómo sueles cerrar proyectos con tu grupo?",
                            "¿Quieres que publiquemos los proyectos en el estudio de Ceibal?"
                        ],
                        "stance": "CO-DECISOR - Acordar un cierre significativo",
                        "stance_examples": [
                            "Me gustaría que publiquemos los mejores proyectos en el estudio de Ceibal. ¿Qué te parece?",
                            "Propongo una combinación: autoevaluación para el aprendizaje y certificados para celebrar."
                        ],
                        "acceptance_criteria": "Ambos acuerdan la forma de cierre y evaluación del proyecto"
                    }
                }
            ],
            "resources": [
                {"type": "link", "title": "Estudio Pensamiento Computacional | Ceibal", "url": "https://scratch.mit.edu/studios/29176159"}
            ]
        }
    ]',
    '{
        "annexes": [
            {
                "id": "anexo_1",
                "title": "Recursos para identificar órganos y funciones",
                "sections": [
                    {
                        "title": "El aparato respiratorio",
                        "resources": [
                            {"type": "video", "title": "El funcionamiento del sistema respiratorio", "url": "https://youtu.be/CEmcS_FPu2k"},
                            {"type": "video", "title": "El aparato respiratorio (Happy Learning)", "url": "https://youtu.be/thUI3RfZUms"},
                            {"type": "link", "title": "Respiración Pulmonar", "url": "https://rea.ceibal.edu.uy/rea/respiraci-n-pulmonar"},
                            {"type": "link", "title": "Respiremos", "url": "https://rea.ceibal.edu.uy/rea/respiremos"},
                            {"type": "link", "title": "El aire que respiramos", "url": "https://rea.ceibal.edu.uy/rea/el-aire-que-respiramos-pero-como"},
                            {"type": "link", "title": "Los órganos y aparatos respiratorios", "url": "https://uruguayeduca.anep.edu.uy/recursos-educativos/289"}
                        ]
                    },
                    {
                        "title": "El aparato digestivo",
                        "resources": [
                            {"type": "video", "title": "Viaje virtual - La primera digestión de Zaqui", "url": "https://youtu.be/pgiwC_HIYKw"},
                            {"type": "video", "title": "El aparato digestivo y la digestión", "url": "https://youtu.be/CIhwGRIBEQ8"},
                            {"type": "link", "title": "Agrupamiento sobre Nutrición", "url": "https://uruguayeduca.anep.edu.uy/recursos-educativos/5065"},
                            {"type": "link", "title": "Unidad: Alimentos y nutrientes", "url": "https://rea.ceibal.edu.uy/rea/unidad-alimentos-y-nutrientes"}
                        ]
                    },
                    {
                        "title": "El aparato circulatorio",
                        "resources": [
                            {"type": "video", "title": "El Sistema circulatorio", "url": "https://youtu.be/nsSg4Eq3LEo"},
                            {"type": "video", "title": "¿Qué es la sangre?", "url": "https://youtu.be/X6WEMPTHHEc"},
                            {"type": "link", "title": "Acciones para cuidar el corazón", "url": "https://uruguayeduca.anep.edu.uy/recursos-educativos/5360"},
                            {"type": "link", "title": "El aparato circulatorio humano", "url": "https://rea.ceibal.edu.uy/rea/el-aparato-circulatorio-humano"}
                        ]
                    }
                ]
            },
            {
                "id": "anexo_2",
                "title": "Pilas Bloques - Alternativas condicionales",
                "resources": [
                    {"type": "link", "title": "La pelota indecisa", "url": "https://pilasbloques.program.ar/online/#/desafio/13"},
                    {"type": "link", "title": "¿Pelota o paleta?", "url": "https://pilasbloques.program.ar/online/#/desafio/14"},
                    {"type": "link", "title": "Alineando telescopios", "url": "https://pilasbloques.program.ar/online/#/desafio/16"}
                ]
            },
            {
                "id": "anexo_4",
                "title": "Recursos sobre salud",
                "sections": [
                    {
                        "title": "El aparato respiratorio",
                        "resources": [
                            {"type": "link", "title": "Propuesta didáctica riesgos del humo de tabaco", "url": "https://uruguayeduca.anep.edu.uy/efemerides/3152"}
                        ]
                    },
                    {
                        "title": "El aparato digestivo",
                        "resources": [
                            {"type": "link", "title": "Alimentación saludable desde la merienda escolar", "url": "https://uruguayeduca.anep.edu.uy/recursos-educativos/448"},
                            {"type": "link", "title": "Alimentación saludable (ELP)", "url": "https://rea.ceibal.edu.uy/elp/alimentacion-saludable/creciendo_sanos_y_saludables.html"},
                            {"type": "link", "title": "Ni muy muy, ni tan tan", "url": "https://rea.ceibal.edu.uy/rea/ni-muy-muy-ni-tan-tan"},
                            {"type": "link", "title": "Unidad: Alimentos y nutrientes", "url": "https://rea.ceibal.edu.uy/rea/unidad-alimentos-y-nutrientes"}
                        ]
                    },
                    {
                        "title": "El aparato circulatorio",
                        "resources": [
                            {"type": "link", "title": "Propuesta didáctica ejercicio físico", "url": "https://uruguayeduca.anep.edu.uy/recursos-educativos/297"},
                            {"type": "link", "title": "Acciones para cuidar el corazón", "url": "https://uruguayeduca.anep.edu.uy/recursos-educativos/5360"},
                            {"type": "link", "title": "El aparato circulatorio humano", "url": "https://rea.ceibal.edu.uy/rea/el-aparato-circulatorio-humano"}
                        ]
                    }
                ]
            }
        ]
    }',
    'recommended'
);

-- Completed proposals (Realizadas) - minimal data, not functional
INSERT INTO proposals (name, description, status) VALUES
(
    'BiblioDatos',
    'Proyecto de Pensamiento Computacional centrado en el análisis y visualización de datos a partir de colecciones bibliográficas escolares.',
    'completed'
),
(
    'CriptoBit',
    'Proyecto de Pensamiento Computacional que explora conceptos de criptografía y seguridad informática mediante actividades prácticas de codificación.',
    'completed'
),
(
    'SimuLAB',
    'Proyecto de Pensamiento Computacional para crear simulaciones de experimentos científicos en un laboratorio virtual.',
    'completed'
);

-- Upcoming proposals (Próximas) - minimal data, not functional
INSERT INTO proposals (name, description, status) VALUES
(
    'Videojuego matemático',
    'Proyecto de Pensamiento Computacional donde los estudiantes diseñan y programan un videojuego educativo para practicar habilidades matemáticas.',
    'upcoming'
),
(
    'Micro:gim',
    'Proyecto de Pensamiento Computacional que combina programación con micro:bit y actividad física para crear dispositivos de ejercicio interactivo.',
    'upcoming'
),
(
    'RadioInvento',
    'Proyecto de Pensamiento Computacional para crear una radio escolar digital integrando producción de contenido y programación.',
    'upcoming'
);
