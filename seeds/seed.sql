-- Real educational data for Area 1 - Cs. Sociales, Políticas y Económicas

-- 2 generic coordinators
INSERT INTO users (email, name, phone) VALUES
    ('coordinador1@demo.edu', 'Coordinador Demo 1', '+5491112345001'),
    ('coordinador2@demo.edu', 'Coordinador Demo 2', '+5491112345002');

-- 3 teachers
INSERT INTO users (email, name, phone) VALUES
    ('docente1@escuelademo.edu', 'María González', '+5491112345003'),
    ('docente2@escuelademo.edu', 'Carlos Rodríguez', '+5491112345004'),
    ('docente3@escuelademo.edu', 'Ana Martínez', '+5491112345005');

-- 7 real areas
INSERT INTO areas (coordinator_id, name, description) VALUES
    (1, 'Cs. Sociales, Políticas y Económicas', NULL),
    (1, 'Lenguajes y Producción Cultural', NULL),
    (2, 'Ciencias Naturales', NULL),
    (2, 'Matemática - Informática', NULL),
    (1, 'Integración Tecnológica', NULL),
    (2, 'EFI', NULL),
    (2, 'ESI', NULL);

-- 18 subjects with disciplinary nuclei for Area 1
-- Area 1 - Cs. Sociales (5 subjects with full disciplinary nuclei)
INSERT INTO subjects (area_id, name, description) VALUES
    (1, 'Historia', 'Las categorías de tiempo y territorio. Las historias, los tiempos y los espacios. Sociedades igualitarias: ausencia de explotación, divisiones de trabajos sin jerarquías ni opresiones. División desigual de los trabajos; génesis del patriarcado, subordinación del trabajo de cuidados. Herida colonial: dominio de la temporalidad y espacialidad eurocentrada.'),
    (1, 'Geografía', 'Distintas miradas pluriversales de los territorios y del ambiente: territorios y bienes comunes. Antes y después de la revolución neolítica. Antes y después de la hegemonía de la mirada europea del territorio. Relaciones capitalistas heteropatriarcales y coloniales con los bienes comunes y los territorios.'),
    (1, 'Economía', 'El ejercicio del poder-saber en la selección socio-cultural de las necesidades, los satisfactores y los bienes comunes. Economías del Buen Vivir / decrecimiento. Ecofeminismo: ética del cuidado en la economía. Economía ecológica. Economías populares, solidarias.'),
    (1, 'Construcción de Ciudadanías', 'El binarismo humano/subhumano a partir del género, la raza, la naturaleza, la religión, la clase social, el origen, etc. Deconstrucción de prácticas racistas y discriminatorias. La disputa por el cuerpo-territorio como espacio de derechos.');

-- Area 2 - Lenguajes y Producción Cultural (7 subjects)
INSERT INTO subjects (area_id, name, description) VALUES
    (2, 'Lengua', NULL),
    (2, 'Literatura', NULL),
    (2, 'Lenguas Otras (Inglés)', NULL),
    (2, 'Artes Visuales', NULL),
    (2, 'Comunicación y Medios', NULL),
    (2, 'Lengua preexistente', NULL),
    (2, 'Lengua y literatura', NULL);

-- Area 3 - Ciencias Naturales (3 subjects)
INSERT INTO subjects (area_id, name, description) VALUES
    (3, 'Biología', NULL),
    (3, 'Química', NULL),
    (3, 'Física', NULL);

-- Area 4 - Matemática-Informática (2 subjects)
INSERT INTO subjects (area_id, name, description) VALUES
    (4, 'Matemática', NULL),
    (4, 'Informática', NULL);

-- Area 5 - Integración Tecnológica (1 subject)
INSERT INTO subjects (area_id, name, description) VALUES
    (5, 'Integración tecnológica', NULL);

-- 1 real problematic nucleus
INSERT INTO problematic_nuclei (name, description) VALUES
    ('Las lógicas de poder y saber', 'Las lógicas de poder y saber en las sociedades disputan en los territorios, el control sobre los bienes comunes, las sexualidades y sus productos, los trabajos y sus productos, y la subjetividad social, produciendo relaciones de dominación y explotación como génesis de la crisis civilizatoria.');

-- 1 knowledge area
INSERT INTO knowledge_areas (nucleus_id, name, description) VALUES
    (1, 'Revolución Neolítica', NULL);

-- 12 real categories
INSERT INTO categories (knowledge_area_id, name, description) VALUES
    (1, 'Tiempos/territorios', NULL),
    (1, 'Subjetividad', NULL),
    (1, 'Trabajos', NULL),
    (1, 'Revolución', NULL),
    (1, 'Estado', NULL),
    (1, 'Acumulación', NULL),
    (1, 'Naturaleza', NULL),
    (1, 'Derechos', NULL),
    (1, 'Ética', NULL),
    (1, 'Necesidades', NULL),
    (1, 'Satisfactores', NULL),
    (1, 'Bienes Comunes', NULL);

-- Course "2do año 1era" with complete schedule including EPAs
-- EPAs (shared classes) are represented by duplicate entries at the same time slot
INSERT INTO courses (name, schedule) VALUES
    ('2do año 1era', '{
  "monday": [
    {"time": "07:45-08:25", "subject": "Matemática"},
    {"time": "07:45-08:25", "subject": "Informática"},
    {"time": "08:25-09:05", "subject": "Matemática"},
    {"time": "08:25-09:05", "subject": "Informática"},
    {"time": "09:10-09:50", "subject": "Economía"},
    {"time": "09:10-09:50", "subject": "Geografía"},
    {"time": "09:50-10:30", "subject": "Economía"},
    {"time": "09:50-10:30", "subject": "Geografía"},
    {"time": "10:40-11:20", "subject": "Historia"},
    {"time": "10:40-11:20", "subject": "Construcción de Ciudadanías"},
    {"time": "11:20-12:00", "subject": "Historia"},
    {"time": "11:20-12:00", "subject": "Construcción de Ciudadanías"},
    {"time": "12:00-12:40", "subject": "Integración tecnológica"}
  ],
  "tuesday": [
    {"time": "07:45-08:25", "subject": "Informática"},
    {"time": "08:25-09:05", "subject": "Economía"},
    {"time": "09:10-09:50", "subject": "Biología"},
    {"time": "09:50-10:30", "subject": "Artes Visuales"},
    {"time": "10:40-11:20", "subject": "Lenguas Otras (Inglés)"},
    {"time": "11:20-12:00", "subject": "Física"},
    {"time": "12:00-12:40", "subject": "Física"}
  ],
  "wednesday": [
    {"time": "07:45-08:25", "subject": "Artes Visuales"},
    {"time": "08:25-09:05", "subject": "Lengua"},
    {"time": "09:10-09:50", "subject": "Integración tecnológica"},
    {"time": "09:50-10:30", "subject": "Integración tecnológica"},
    {"time": "10:40-11:20", "subject": "Geografía"},
    {"time": "11:20-12:00", "subject": "Biología"},
    {"time": "11:20-12:00", "subject": "Química"},
    {"time": "12:00-12:40", "subject": "Biología"},
    {"time": "12:00-12:40", "subject": "Química"}
  ],
  "thursday": [
    {"time": "07:45-08:25", "subject": "Literatura"},
    {"time": "08:25-09:05", "subject": "Literatura"},
    {"time": "09:10-09:50", "subject": "Química"},
    {"time": "09:50-10:30", "subject": "Integración tecnológica"},
    {"time": "10:40-11:20", "subject": "Historia"},
    {"time": "10:40-11:20", "subject": "Construcción de Ciudadanías"},
    {"time": "11:20-12:00", "subject": "Historia"},
    {"time": "11:20-12:00", "subject": "Construcción de Ciudadanías"},
    {"time": "12:00-12:40", "subject": "Comunicación y Medios"}
  ],
  "friday": [
    {"time": "07:45-08:25", "subject": "Lengua preexistente"},
    {"time": "08:25-09:05", "subject": "Lengua preexistente"},
    {"time": "09:10-09:50", "subject": "Lengua y literatura"},
    {"time": "09:10-09:50", "subject": "Lenguas Otras (Inglés)"},
    {"time": "09:50-10:30", "subject": "Lengua y literatura"},
    {"time": "09:50-10:30", "subject": "Lenguas Otras (Inglés)"},
    {"time": "10:40-11:20", "subject": "Matemática"},
    {"time": "11:20-12:00", "subject": "Matemática"},
    {"time": "12:00-12:40", "subject": "Matemática"}
  ]
}'),
    ('2do año 2da', '{
  "monday": [
    {"time": "07:45-08:25", "subject": "Lengua"},
    {"time": "08:25-09:05", "subject": "Lengua"},
    {"time": "09:10-09:50", "subject": "Historia"},
    {"time": "09:10-09:50", "subject": "Geografía"},
    {"time": "09:50-10:30", "subject": "Historia"},
    {"time": "09:50-10:30", "subject": "Geografía"},
    {"time": "10:40-11:20", "subject": "Matemática"},
    {"time": "10:40-11:20", "subject": "Informática"},
    {"time": "11:20-12:00", "subject": "Matemática"},
    {"time": "11:20-12:00", "subject": "Informática"},
    {"time": "12:00-12:40", "subject": "Integración tecnológica"}
  ],
  "tuesday": [
    {"time": "07:45-08:25", "subject": "Literatura"},
    {"time": "08:25-09:05", "subject": "Economía"},
    {"time": "09:10-09:50", "subject": "Física"},
    {"time": "09:50-10:30", "subject": "Biología"},
    {"time": "10:40-11:20", "subject": "Lenguas Otras (Inglés)"},
    {"time": "11:20-12:00", "subject": "Química"},
    {"time": "12:00-12:40", "subject": "Artes Visuales"}
  ],
  "wednesday": [
    {"time": "07:45-08:25", "subject": "Economía"},
    {"time": "07:45-08:25", "subject": "Construcción de Ciudadanías"},
    {"time": "08:25-09:05", "subject": "Economía"},
    {"time": "08:25-09:05", "subject": "Construcción de Ciudadanías"},
    {"time": "09:10-09:50", "subject": "Integración tecnológica"},
    {"time": "09:50-10:30", "subject": "Integración tecnológica"},
    {"time": "10:40-11:20", "subject": "Geografía"},
    {"time": "11:20-12:00", "subject": "Biología"},
    {"time": "11:20-12:00", "subject": "Química"},
    {"time": "12:00-12:40", "subject": "Comunicación y Medios"}
  ],
  "thursday": [
    {"time": "07:45-08:25", "subject": "Matemática"},
    {"time": "08:25-09:05", "subject": "Matemática"},
    {"time": "09:10-09:50", "subject": "Química"},
    {"time": "09:50-10:30", "subject": "Física"},
    {"time": "10:40-11:20", "subject": "Historia"},
    {"time": "10:40-11:20", "subject": "Construcción de Ciudadanías"},
    {"time": "11:20-12:00", "subject": "Historia"},
    {"time": "11:20-12:00", "subject": "Construcción de Ciudadanías"},
    {"time": "12:00-12:40", "subject": "Integración tecnológica"}
  ],
  "friday": [
    {"time": "07:45-08:25", "subject": "Lengua preexistente"},
    {"time": "08:25-09:05", "subject": "Lengua preexistente"},
    {"time": "09:10-09:50", "subject": "Lengua y literatura"},
    {"time": "09:10-09:50", "subject": "Lenguas Otras (Inglés)"},
    {"time": "09:50-10:30", "subject": "Lengua y literatura"},
    {"time": "09:50-10:30", "subject": "Lenguas Otras (Inglés)"},
    {"time": "10:40-11:20", "subject": "Artes Visuales"},
    {"time": "11:20-12:00", "subject": "Informática"},
    {"time": "12:00-12:40", "subject": "Biología"}
  ]
}'),
    ('3er año 1era', '{
  "monday": [
    {"time": "07:45-08:25", "subject": "Matemática"},
    {"time": "08:25-09:05", "subject": "Matemática"},
    {"time": "09:10-09:50", "subject": "Historia"},
    {"time": "09:10-09:50", "subject": "Economía"},
    {"time": "09:50-10:30", "subject": "Historia"},
    {"time": "09:50-10:30", "subject": "Economía"},
    {"time": "10:40-11:20", "subject": "Geografía"},
    {"time": "10:40-11:20", "subject": "Construcción de Ciudadanías"},
    {"time": "11:20-12:00", "subject": "Geografía"},
    {"time": "11:20-12:00", "subject": "Construcción de Ciudadanías"},
    {"time": "12:00-12:40", "subject": "Integración tecnológica"}
  ],
  "tuesday": [
    {"time": "07:45-08:25", "subject": "Lengua"},
    {"time": "08:25-09:05", "subject": "Literatura"},
    {"time": "09:10-09:50", "subject": "Física"},
    {"time": "09:50-10:30", "subject": "Química"},
    {"time": "10:40-11:20", "subject": "Lenguas Otras (Inglés)"},
    {"time": "11:20-12:00", "subject": "Biología"},
    {"time": "12:00-12:40", "subject": "Artes Visuales"}
  ],
  "wednesday": [
    {"time": "07:45-08:25", "subject": "Informática"},
    {"time": "08:25-09:05", "subject": "Economía"},
    {"time": "09:10-09:50", "subject": "Integración tecnológica"},
    {"time": "09:50-10:30", "subject": "Integración tecnológica"},
    {"time": "10:40-11:20", "subject": "Historia"},
    {"time": "11:20-12:00", "subject": "Biología"},
    {"time": "11:20-12:00", "subject": "Química"},
    {"time": "12:00-12:40", "subject": "Comunicación y Medios"}
  ],
  "thursday": [
    {"time": "07:45-08:25", "subject": "Matemática"},
    {"time": "08:25-09:05", "subject": "Matemática"},
    {"time": "09:10-09:50", "subject": "Física"},
    {"time": "09:50-10:30", "subject": "Geografía"},
    {"time": "10:40-11:20", "subject": "Historia"},
    {"time": "10:40-11:20", "subject": "Construcción de Ciudadanías"},
    {"time": "11:20-12:00", "subject": "Historia"},
    {"time": "11:20-12:00", "subject": "Construcción de Ciudadanías"},
    {"time": "12:00-12:40", "subject": "Integración tecnológica"}
  ],
  "friday": [
    {"time": "07:45-08:25", "subject": "Lengua preexistente"},
    {"time": "08:25-09:05", "subject": "Lengua preexistente"},
    {"time": "09:10-09:50", "subject": "Lengua y literatura"},
    {"time": "09:10-09:50", "subject": "Lenguas Otras (Inglés)"},
    {"time": "09:50-10:30", "subject": "Lengua y literatura"},
    {"time": "09:50-10:30", "subject": "Lenguas Otras (Inglés)"},
    {"time": "10:40-11:20", "subject": "Artes Visuales"},
    {"time": "11:20-12:00", "subject": "Informática"},
    {"time": "12:00-12:40", "subject": "Biología"}
  ]
}'),
    ('3er año 2da', '{
  "monday": [
    {"time": "07:45-08:25", "subject": "Lengua"},
    {"time": "08:25-09:05", "subject": "Lengua"},
    {"time": "09:10-09:50", "subject": "Geografía"},
    {"time": "09:10-09:50", "subject": "Economía"},
    {"time": "09:50-10:30", "subject": "Geografía"},
    {"time": "09:50-10:30", "subject": "Economía"},
    {"time": "10:40-11:20", "subject": "Matemática"},
    {"time": "10:40-11:20", "subject": "Informática"},
    {"time": "11:20-12:00", "subject": "Matemática"},
    {"time": "11:20-12:00", "subject": "Informática"},
    {"time": "12:00-12:40", "subject": "Integración tecnológica"}
  ],
  "tuesday": [
    {"time": "07:45-08:25", "subject": "Literatura"},
    {"time": "08:25-09:05", "subject": "Historia"},
    {"time": "09:10-09:50", "subject": "Física"},
    {"time": "09:50-10:30", "subject": "Biología"},
    {"time": "10:40-11:20", "subject": "Lenguas Otras (Inglés)"},
    {"time": "11:20-12:00", "subject": "Química"},
    {"time": "12:00-12:40", "subject": "Artes Visuales"}
  ],
  "wednesday": [
    {"time": "07:45-08:25", "subject": "Historia"},
    {"time": "07:45-08:25", "subject": "Construcción de Ciudadanías"},
    {"time": "08:25-09:05", "subject": "Historia"},
    {"time": "08:25-09:05", "subject": "Construcción de Ciudadanías"},
    {"time": "09:10-09:50", "subject": "Integración tecnológica"},
    {"time": "09:50-10:30", "subject": "Integración tecnológica"},
    {"time": "10:40-11:20", "subject": "Economía"},
    {"time": "11:20-12:00", "subject": "Biología"},
    {"time": "11:20-12:00", "subject": "Química"},
    {"time": "12:00-12:40", "subject": "Comunicación y Medios"}
  ],
  "thursday": [
    {"time": "07:45-08:25", "subject": "Matemática"},
    {"time": "08:25-09:05", "subject": "Matemática"},
    {"time": "09:10-09:50", "subject": "Química"},
    {"time": "09:50-10:30", "subject": "Física"},
    {"time": "10:40-11:20", "subject": "Geografía"},
    {"time": "10:40-11:20", "subject": "Construcción de Ciudadanías"},
    {"time": "11:20-12:00", "subject": "Geografía"},
    {"time": "11:20-12:00", "subject": "Construcción de Ciudadanías"},
    {"time": "12:00-12:40", "subject": "Integración tecnológica"}
  ],
  "friday": [
    {"time": "07:45-08:25", "subject": "Lengua preexistente"},
    {"time": "08:25-09:05", "subject": "Lengua preexistente"},
    {"time": "09:10-09:50", "subject": "Lengua y literatura"},
    {"time": "09:10-09:50", "subject": "Lenguas Otras (Inglés)"},
    {"time": "09:50-10:30", "subject": "Lengua y literatura"},
    {"time": "09:50-10:30", "subject": "Lenguas Otras (Inglés)"},
    {"time": "10:40-11:20", "subject": "Artes Visuales"},
    {"time": "11:20-12:00", "subject": "Informática"},
    {"time": "12:00-12:40", "subject": "Biología"}
  ]
}');

-- Moment types (static data)
INSERT INTO moment_types (name, description) VALUES
    ('Apertura/Motivación', 'Momento inicial de la clase para captar la atención'),
    ('Desarrollo/Construcción/Práctica', 'Momento central de la clase para desarrollar el contenido'),
    ('Cierre/Metacognición', 'Momento final para reflexionar y consolidar aprendizajes');

-- Activities (static data) - organized by moment_type
-- APERTURA (5 activities - select 1)
INSERT INTO activities (name, description, moment_type) VALUES
    ('Análisis de una Situación-Problema', 'Presentar una situación real, concreta y cercana al estudiante que genere conflicto cognitivo y motive la exploración del tema. El problema debe ser abierto, permitiendo múltiples enfoques y soluciones.', 'apertura'),
    ('Provocación con Imágenes o Objetos Reales (Multimodalidad)', 'Mostrar una imagen publicitaria, una foto histórica, un objeto cotidiano o un fragmento audiovisual que active conocimientos previos y genere preguntas. Se busca conectar lo sensorial con lo conceptual.', 'apertura'),
    ('Torbellino de Ideas y Categorización (Brainstorming)', 'Lluvia de ideas sobre el tema central donde los estudiantes expresan libremente asociaciones, conceptos y experiencias previas. Luego se organizan las ideas en categorías para estructurar el conocimiento emergente.', 'apertura'),
    ('Predicción de Fenómenos (P.O.E)', 'Técnica Predecir-Observar-Explicar. Los estudiantes predicen qué sucederá ante un fenómeno o situación, luego observan el resultado real y finalmente explican las diferencias entre predicción y realidad.', 'apertura'),
    ('Organizador Previo (Puente Cognitivo)', 'Presentar un esquema, mapa conceptual o analogía que conecte el nuevo contenido con lo que los estudiantes ya saben. Funciona como andamiaje para estructurar el aprendizaje que vendrá.', 'apertura');

-- DESARROLLO (7 activities - select up to 3)
INSERT INTO activities (name, description, moment_type) VALUES
    ('Investigación Guiada con Contrastación de Fuentes', 'Los estudiantes buscan información para resolver una pregunta o problema, comparando diferentes fuentes (textos, videos, entrevistas) para desarrollar pensamiento crítico y habilidades de investigación.', 'desarrollo'),
    ('Simulación o Juego de Roles (Role-Playing)', 'Los alumnos asumen roles para resolver situaciones, dramatizar eventos históricos o simular procesos científicos. Permite vivenciar conceptos abstractos y desarrollar empatía cognitiva.', 'desarrollo'),
    ('Método de Casos', 'Análisis profundo de un caso real o ficticio que presenta un dilema o problema complejo. Los estudiantes deben tomar decisiones fundamentadas, considerando múltiples perspectivas y consecuencias.', 'desarrollo'),
    ('Enseñanza Recíproca (Rompecabezas)', 'Cada estudiante o grupo se especializa en una parte del contenido y luego lo enseña a sus compañeros. Promueve la interdependencia positiva y el aprendizaje profundo a través de la enseñanza entre pares.', 'desarrollo'),
    ('Debate Jurisprudencial (Simulación de Juicio)', 'Los estudiantes representan un juicio donde deben argumentar posiciones opuestas sobre un tema controversial. Desarrolla habilidades de argumentación, oratoria y pensamiento crítico.', 'desarrollo'),
    ('Taller de Exploración con Simuladores (TIC)', 'Uso de software, simuladores virtuales o laboratorios digitales para experimentar con fenómenos que serían difíciles de observar directamente. Permite manipular variables y observar resultados.', 'desarrollo'),
    ('Escritura de Invención (Cambio de Género)', 'Transformar un texto o contenido a otro género discursivo (convertir un informe en carta, un cuento en noticia, etc.). Desarrolla comprensión profunda y habilidades de escritura creativa.', 'desarrollo');

-- CIERRE (4 activities - select 1)
INSERT INTO activities (name, description, moment_type) VALUES
    ('Ticket de Salida / Diario Metacognitivo', 'Los estudiantes escriben brevemente qué aprendieron, qué dudas les quedaron y cómo se sintieron durante la clase. Permite evaluar comprensión y promover la reflexión metacognitiva.', 'cierre'),
    ('Transferencia a Situación Nueva (Evaluación Auténtica)', 'Aplicar lo aprendido a un contexto diferente al trabajado en clase. Evalúa la comprensión profunda y la capacidad de transferir conocimientos a nuevas situaciones.', 'cierre'),
    ('Portafolio de Evidencias (Selección)', 'Los estudiantes seleccionan y justifican qué trabajos o producciones de la clase incluirían en su portafolio, explicando qué demuestran sobre su aprendizaje.', 'cierre'),
    ('Producción Multimedia para Difusión', 'Crear un producto comunicable (video corto, infografía, podcast, presentación) que sintetice lo aprendido. Se orienta a una audiencia real o simulada, dando sentido social al aprendizaje.', 'cierre');

-- 25 students for "2do año 1era" (course_id = 1)
INSERT INTO students (course_id, name) VALUES
    (1, 'Lucía Fernández'),
    (1, 'Mateo López'),
    (1, 'Valentina García'),
    (1, 'Santiago Pérez'),
    (1, 'Camila Rodríguez'),
    (1, 'Benjamín Martínez'),
    (1, 'Sofía Sánchez'),
    (1, 'Tomás Romero'),
    (1, 'Emma Torres'),
    (1, 'Nicolás Flores'),
    (1, 'Isabella Díaz'),
    (1, 'Lautaro Gómez'),
    (1, 'Martina Ruiz'),
    (1, 'Joaquín Hernández'),
    (1, 'Emilia Morales'),
    (1, 'Thiago Acosta'),
    (1, 'Olivia Castro'),
    (1, 'Felipe Vargas'),
    (1, 'Renata Méndez'),
    (1, 'Bautista Silva'),
    (1, 'Catalina Ortiz'),
    (1, 'Juan Cruz Aguirre'),
    (1, 'Delfina Medina'),
    (1, 'Agustín Navarro'),
    (1, 'Alma Figueroa');

-- Teacher assignments for Cs. Sociales subjects
-- Subject IDs: Historia(1), Geografía(2), Economía(3), Construcción de Ciudadanías(4)
-- Teacher IDs: María(3), Carlos(4), Ana(5)
INSERT INTO course_subjects (course_id, subject_id, teacher_id, start_date, end_date, school_year) VALUES
    -- 2do año 1era (course_id = 1)
    (1, 1, 3, '2026-03-01', '2026-12-15', 2026),  -- María -> Historia
    (1, 2, 4, '2026-03-01', '2026-12-15', 2026),  -- Carlos -> Geografía
    (1, 3, 4, '2026-03-01', '2026-12-15', 2026),  -- Carlos -> Economía
    (1, 4, 5, '2026-03-01', '2026-12-15', 2026),  -- Ana -> Construcción de Ciudadanías
    -- 2do año 2da (course_id = 2)
    (2, 1, 3, '2026-03-01', '2026-12-15', 2026),  -- María -> Historia
    (2, 3, 3, '2026-03-01', '2026-12-15', 2026),  -- María -> Economía
    (2, 2, 4, '2026-03-01', '2026-12-15', 2026),  -- Carlos -> Geografía
    (2, 4, 5, '2026-03-01', '2026-12-15', 2026),  -- Ana -> Construcción de Ciudadanías
    -- 3er año 1era (course_id = 3)
    (3, 2, 3, '2026-03-01', '2026-12-15', 2026),  -- María -> Geografía
    (3, 1, 4, '2026-03-01', '2026-12-15', 2026),  -- Carlos -> Historia
    (3, 3, 4, '2026-03-01', '2026-12-15', 2026),  -- Carlos -> Economía
    (3, 4, 5, '2026-03-01', '2026-12-15', 2026),  -- Ana -> Construcción de Ciudadanías
    -- 3er año 2da (course_id = 4)
    (4, 4, 3, '2026-03-01', '2026-12-15', 2026),  -- María -> Construcción de Ciudadanías
    (4, 1, 4, '2026-03-01', '2026-12-15', 2026),  -- Carlos -> Historia
    (4, 2, 5, '2026-03-01', '2026-12-15', 2026),  -- Ana -> Geografía
    (4, 3, 5, '2026-03-01', '2026-12-15', 2026);  -- Ana -> Economía
