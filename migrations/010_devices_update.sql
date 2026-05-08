-- 010_devices_update.sql
-- Actualiza el catalogo de devices al Listado FINAL (Valija 2026):
--   * Schema enrichment (8 columnas nuevas)
--   * Renombres + stage para productos progresivos (Soporte lapiz, Tijera adaptada, Ayuda lectura)
--   * Reemplazo Teclado CLEVY -> Teclado Admouse
--   * Backfill de manifestaciones/situaciones/clases/perfiles para los 18 productos existentes
--   * Insercion de 17 productos nuevos (16 del Listado FINAL + Tijera adaptada etapa 2)
--
-- Idempotente con ADD COLUMN IF NOT EXISTS y filtros WHERE name = '...'.
-- Marker NEEDS_VALIDATION = items pendientes de validacion humana (ver doc 3.4).

BEGIN;

-- 1) Schema enrichment ------------------------------------------------------

ALTER TABLE devices
  ADD COLUMN IF NOT EXISTS stage                     SMALLINT,
  ADD COLUMN IF NOT EXISTS material_class            TEXT[] DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS frequent_profile          TEXT[] DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS specific_profile          TEXT[] DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS function_summary          TEXT,
  ADD COLUMN IF NOT EXISTS pedagogical_situations    TEXT[] DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS observable_manifestations TEXT[] DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS active                    BOOLEAN DEFAULT TRUE;


-- 2) Renombres + asignacion de stage ----------------------------------------

UPDATE devices SET name = 'Soporte para lapiz 1 — etapa 4', stage = 4
  WHERE name = 'Pinzas de escritura';

UPDATE devices SET name = 'Tijera adaptada — etapa 1', stage = 1
  WHERE name = 'Tijeras adaptadas';

UPDATE devices SET name = 'Ayuda para la lectura — tamano ajustable — etapa 1', stage = 1
  WHERE name = 'Regla lupa';

UPDATE devices SET name = 'Ayuda para la lectura — tamano fijo 2 palabras — etapa 2', stage = 2
  WHERE name = 'Regla de lectura con ventana';

UPDATE devices SET name = 'Ayuda para la lectura — Reglas de lectura guiada — etapa 3', stage = 3
  WHERE name = 'Finger focus (senalador de dedo)';

UPDATE devices SET name = 'Banda elastica Bouncyband'
  WHERE name = 'Elastico para silla';


-- 3) Reemplazo in-place: Teclado CLEVY -> Teclado Admouse -------------------
--    NEEDS_VALIDATION: Anabela debe confirmar si reemplazan o coexisten.

UPDATE devices SET
  name = 'Teclado Admouse',
  description = 'Teclado adaptado de gran formato pensado para acceso cognitivo y motor. Letras y teclas grandes con colores diferenciados por grupos.',
  needs_description = 'Acompana a estudiantes que: tienen dificultades motoras para presionar teclas convencionales, baja vision, dificultades para identificar letras, o se frustran con teclados estandar.'
  WHERE name = 'Teclado CLEVY';


-- 4) Backfill de metadata enriquecida para los 18 productos existentes ------

-- 4.1) Rampa Digital ---------------------------------------------------------

UPDATE devices SET
  function_summary = 'Habilita acceso multimodal al contenido. Permite ajustar consigna, lectura, escritura y expresion segun la necesidad. Reduce barreras al aprendizaje y favorece la autonomia.',
  observable_manifestations = ARRAY['Le cuesta leer textos largos','Evita escribir a mano','Se cansa al escribir','Le cuesta copiar del pizarron','Tarda mucho en hacer tareas escritas','Necesita apoyo para acceder al contenido'],
  pedagogical_situations = ARRAY['Actividades de lectura digital','Produccion escrita','Uso de aplicaciones educativas','Trabajo autonomo'],
  material_class = ARRAY['Acceso al aprendizaje','Accesibilidad tecnologica'],
  frequent_profile = ARRAY['DEA','discapacidad intelectual','TEA','altas capacidades','altas necesidades de apoyo','discapacidad visual','discapacidad auditiva','discapacidad motora'],
  specific_profile = ARRAY['Dislexia','disgrafia','discalculia','sindrome de Down','TEA con apoyo leve','baja vision','hipoacusia','paralisis cerebral']
  WHERE name = 'Tablet educativa (10")';

UPDATE devices SET
  function_summary = 'Permite el acceso al contenido por via auditiva. Reduce la interferencia del ruido del aula. Habilita el uso de comandos por voz y lectura asistida.',
  observable_manifestations = ARRAY['Le cuesta leer solo','Necesita escuchar para entender','Se cansa al leer','Le cuesta escribir sin ayuda','Se distrae con el ruido del aula'],
  pedagogical_situations = ARRAY['Lectura asistida','Comandos por voz','Trabajo con dispositivos','Actividades con componente auditivo'],
  material_class = ARRAY['Acceso al aprendizaje','Accesibilidad tecnologica'],
  frequent_profile = ARRAY['DEA','discapacidad intelectual','TEA','altas capacidades','discapacidad visual'],
  specific_profile = ARRAY['Dislexia','TEA con apoyo leve','baja vision','TDAH']
  WHERE name = 'Auriculares con microfono';

UPDATE devices SET
  function_summary = 'Facilita el control del cursor sin desplazamiento del dispositivo. Permite el acceso funcional a la computadora con menor exigencia motora fina.',
  observable_manifestations = ARRAY['Le cuesta usar el mouse','Mueve demasiado el cursor','No logra precision','Se frustra con la computadora','Tiene movimientos involuntarios'],
  pedagogical_situations = ARRAY['Computadora/tablet','Actividades digitales','Navegacion','Software educativo'],
  material_class = ARRAY['Accesibilidad tecnologica'],
  frequent_profile = ARRAY['discapacidad motora','discapacidad intelectual','TEA','altas necesidades de apoyo'],
  specific_profile = ARRAY['paralisis cerebral','sindrome de Down','TEA con mayor necesidad de apoyo','multidiscapacidad']
  WHERE name = 'Mouse trackball';

UPDATE devices SET
  function_summary = 'Teclado de gran formato para acceso cognitivo y motor simplificado. Letras grandes y agrupadas por color reducen carga cognitiva al escribir.',
  observable_manifestations = ARRAY['Se equivoca al escribir','No encuentra las teclas','Escribe lento','Evita escribir','Aprieta fuerte las teclas'],
  pedagogical_situations = ARRAY['Produccion escrita digital','Actividades de escritura','Uso del teclado'],
  material_class = ARRAY['Acceso al aprendizaje','Accesibilidad tecnologica'],
  frequent_profile = ARRAY['discapacidad intelectual','TEA','discapacidad motora','discapacidad visual'],
  specific_profile = ARRAY['sindrome de Down','TEA con apoyo notable','baja vision','paralisis cerebral']
  WHERE name = 'Teclado Admouse';

UPDATE devices SET
  function_summary = 'Aumenta el contraste visual del teclado. Permite identificar las teclas con baja vision o sin acompanamiento.',
  observable_manifestations = ARRAY['No distingue bien las teclas','Se confunde al escribir','Tarda en encontrar letras','Necesita apoyo visual'],
  pedagogical_situations = ARRAY['Escritura digital','Uso del teclado'],
  material_class = ARRAY['Acceso al aprendizaje','Accesibilidad tecnologica'],
  frequent_profile = ARRAY['discapacidad visual','DEA','discapacidad intelectual'],
  specific_profile = ARRAY['baja vision','Dislexia']
  WHERE name = 'Stickers de contraste para teclado';

UPDATE devices SET
  function_summary = 'Permite interactuar con la computadora con un solo movimiento voluntario. Habilita acceso digital cuando teclado y mouse no son posibles.',
  observable_manifestations = ARRAY['No puede usar teclado o mouse','Le cuesta interactuar con dispositivos','Necesita acceso alternativo','Tiene dificultades para expresarse'],
  pedagogical_situations = ARRAY['Acceso a dispositivos','Computadora','Software educativo'],
  material_class = ARRAY['Accesibilidad tecnologica'],
  frequent_profile = ARRAY['discapacidad motora','altas necesidades de apoyo','discapacidad intelectual'],
  specific_profile = ARRAY['paralisis cerebral','multidiscapacidad','TEA con mayor necesidad de apoyo']
  WHERE name = 'Pulsador boton USB';

-- NEEDS_VALIDATION: Soporte flexible no esta en Listado FINAL. Anabela debe confirmar si se conserva.
UPDATE devices SET
  function_summary = 'Posiciona el dispositivo en el angulo optimo y libera las manos del estudiante para interactuar con la pantalla.',
  observable_manifestations = ARRAY['No puede sostener la tablet o celular','Tiene movilidad reducida en brazos o manos','Necesita el dispositivo en un angulo especifico'],
  pedagogical_situations = ARRAY['Uso de tablet o celular','Actividades digitales','Trabajo en mesa con dispositivo'],
  material_class = ARRAY['Adaptacion del entorno','Accesibilidad tecnologica'],
  frequent_profile = ARRAY['discapacidad motora','altas necesidades de apoyo'],
  specific_profile = ARRAY['paralisis cerebral','multidiscapacidad']
  WHERE name = 'Soporte flexible celular/tablet';

-- 4.2) Rampa Didactico-Pedagogica -------------------------------------------

UPDATE devices SET
  function_summary = 'Convierte texto impreso en audio. Permite que el estudiante acceda al contenido escrito por via auditiva, de forma autonoma.',
  observable_manifestations = ARRAY['Le cuesta leer palabras','No comprende lo que lee','Evita la lectura','Se cansa al leer','Necesita apoyo para acceder al texto'],
  pedagogical_situations = ARRAY['Lectura de impresos','Comprension','Evaluaciones','Tareas con material escrito'],
  material_class = ARRAY['Acceso al aprendizaje','Accesibilidad tecnologica'],
  frequent_profile = ARRAY['DEA','discapacidad intelectual','TEA','discapacidad visual'],
  specific_profile = ARRAY['Dislexia','sindrome de Down','baja vision','TEA con apoyo leve']
  WHERE name = 'Pen reader (lapiz lector)';

UPDATE devices SET
  function_summary = 'Amplia visualmente una linea de texto. Facilita el seguimiento visual y reduce la fatiga lectora. Primer nivel de las ayudas para lectura.',
  observable_manifestations = ARRAY['Le cuesta leer palabras','Salta palabras','Se desorienta en el texto','Lee lento','Se cansa al leer','Le cuesta segmentar'],
  pedagogical_situations = ARRAY['Actividades de lectura','Comprension lectora','Trabajo individual con textos','Tareas de copia'],
  material_class = ARRAY['Acceso al aprendizaje','atencion'],
  frequent_profile = ARRAY['TEA','discapacidad intelectual','DEA','discapacidad visual'],
  specific_profile = ARRAY['TDAH','Dislexia','sindrome de Down','baja vision','TEA con apoyo leve']
  WHERE name = 'Ayuda para la lectura — tamano ajustable — etapa 1';

UPDATE devices SET
  function_summary = 'Aisla 2 palabras a la vez. Reduce la sobrecarga visual y mantiene el foco en la lectura. Segundo nivel de progresion.',
  observable_manifestations = ARRAY['Salta palabras','Se desorienta en el texto','Lee lento','Se cansa al leer','Pierde la linea al leer','Se distrae con el resto de la pagina'],
  pedagogical_situations = ARRAY['Actividades de lectura','Comprension lectora','Trabajo individual con textos','Tareas de copia'],
  material_class = ARRAY['Acceso al aprendizaje','atencion'],
  frequent_profile = ARRAY['TEA','discapacidad intelectual','DEA','discapacidad visual'],
  specific_profile = ARRAY['TDAH','Dislexia','sindrome de Down','TEA con apoyo leve']
  WHERE name = 'Ayuda para la lectura — tamano fijo 2 palabras — etapa 2';

UPDATE devices SET
  function_summary = 'Guia visual con el dedo. Mejora la fluidez lectora cuando el estudiante no necesita ampliar ni aislar tanto. Tercer nivel de progresion.',
  observable_manifestations = ARRAY['Salta linea','Se desorienta','Lee lento','Se cansa','Le cuesta seguir la lectura'],
  pedagogical_situations = ARRAY['Actividades de lectura','Comprension lectora','Trabajo individual con textos','Tareas de copia'],
  material_class = ARRAY['Acceso al aprendizaje','atencion'],
  frequent_profile = ARRAY['TEA','discapacidad intelectual','DEA'],
  specific_profile = ARRAY['TDAH','Dislexia','TEA con apoyo leve']
  WHERE name = 'Ayuda para la lectura — Reglas de lectura guiada — etapa 3';

UPDATE devices SET
  function_summary = 'Tijera con apertura automatica. Permite el uso funcional sin abrir y cerrar repetidamente. Primer nivel de adaptacion (mas asistido).',
  observable_manifestations = ARRAY['Le cuesta usar la tijera','Corta con dificultad','No logra seguir linea','Evita el recorte','Se cansa rapido','Necesita ayuda'],
  pedagogical_situations = ARRAY['Actividades de recorte','Trabajos manuales','Motricidad fina'],
  material_class = ARRAY['Acceso al aprendizaje'],
  frequent_profile = ARRAY['discapacidad motora','TEA','discapacidad intelectual'],
  specific_profile = ARRAY['paralisis cerebral','sindrome de Down','TEA con apoyo notable']
  WHERE name = 'Tijera adaptada — etapa 1';

UPDATE devices SET
  stage = 4,
  function_summary = 'Mejora la prension del lapiz. Favorece postura adecuada y control del trazo. Etapa 4 = mas simple, mas autonomia.',
  observable_manifestations = ARRAY['Sostiene mal el lapiz','Hace mucha fuerza al escribir','Se le cae el lapiz','Se cansa rapido al escribir','La letra es poco legible','Le cuesta controlar el trazo'],
  pedagogical_situations = ARRAY['Escritura en clase','Actividades de copia','Tareas de produccion escrita','Ejercicios de grafomotricidad'],
  material_class = ARRAY['Acceso al aprendizaje'],
  frequent_profile = ARRAY['DEA','TEA','discapacidad motora','discapacidad intelectual'],
  specific_profile = ARRAY['paralisis cerebral','sindrome de Down','TEA con apoyo notable','Disgrafia','TDAH']
  WHERE name = 'Soporte para lapiz 1 — etapa 4';

-- 4.3) Rampa de Autorregulacion Sensorial -----------------------------------

UPDATE devices SET
  function_summary = 'Banda elastica para canalizar movimiento de pies sin abandonar la silla. Permite movimiento controlado y silencioso.',
  observable_manifestations = ARRAY['Se balancea en la silla','Se levanta con frecuencia','Mueve constantemente el cuerpo','Le cuesta permanecer en su lugar','Interrumpe la tarea por movimiento'],
  pedagogical_situations = ARRAY['Trabajo en mesa','Actividades largas','Permanencia sentado','Tareas individuales'],
  material_class = ARRAY['Regulacion, atencion'],
  frequent_profile = ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
  specific_profile = ARRAY['TDAH','TEA con apoyo leve','TEA con apoyo notable','alto potencial intelectual']
  WHERE name = 'Banda elastica Bouncyband';

UPDATE devices SET
  function_summary = 'Estimulacion sensorial discreta integrada al mobiliario. Ayuda a regular el nivel de activacion sin senalizar al estudiante.',
  observable_manifestations = ARRAY['Se inquieta','Necesita estimulos sensoriales','Le cuesta mantener la atencion','Mueve mucho la silla'],
  pedagogical_situations = ARRAY['Trabajo en mesa','Actividades largas','Permanencia sentado'],
  material_class = ARRAY['Regulacion, atencion'],
  frequent_profile = ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
  specific_profile = ARRAY['TDAH','TEA con apoyo leve','TEA con apoyo notable']
  WHERE name = 'Patas de silla (almohadillas sensoriales)';

UPDATE devices SET
  function_summary = 'Hace visible el paso del tiempo. Reduce la ansiedad por previsibilidad y favorece la organizacion temporal de la tarea.',
  observable_manifestations = ARRAY['No gestiona el tiempo','Le cuesta empezar','No termina a tiempo','Se pone ansioso con cambios','Necesita saber cuanto falta'],
  pedagogical_situations = ARRAY['Inicio de actividad','Planificacion','Trabajos por etapas','Evaluaciones con tiempo limitado'],
  material_class = ARRAY['Organizacion','regulacion','atencion'],
  frequent_profile = ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
  specific_profile = ARRAY['TDAH','TEA con apoyo leve','TEA con apoyo notable','alto potencial intelectual']
  WHERE name = 'Time Timer (temporizador visual)';

-- NEEDS_VALIDATION: Pelota antiestres no esta en Listado FINAL. Anabela debe confirmar si se conserva.
UPDATE devices SET
  function_summary = 'Canaliza tension y ansiedad de forma silenciosa. Permite sostener la atencion mientras se manipula.',
  observable_manifestations = ARRAY['Se inquieta constantemente','Necesita manipular objetos','Se pone ansioso durante la tarea','Se muerde las unas','Le cuesta quedarse quieto'],
  pedagogical_situations = ARRAY['Actividades que requieren concentracion','Momentos de espera','Trabajo autonomo','Situaciones de ansiedad'],
  material_class = ARRAY['Regulacion, atencion'],
  frequent_profile = ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
  specific_profile = ARRAY['TDAH','TEA con apoyo leve','alto potencial intelectual']
  WHERE name = 'Pelota antiestres de gel';

UPDATE devices SET
  function_summary = 'Reduce la sobrecarga sensorial auditiva. Permite permanecer en la clase con menos interferencia de ruido ambiental.',
  observable_manifestations = ARRAY['Se distrae facilmente con los ruidos','Le molestan los sonidos del aula','Se desconcentra con facilidad','Se tapa los oidos','Pierde el foco durante la tarea','Necesita silencio para poder trabajar','Se sobrecarga con estimulos auditivos'],
  pedagogical_situations = ARRAY['Lectura individual','Evaluaciones','Trabajo autonomo','Actividades que requieren concentracion','Momentos de sobreestimulacion sensorial'],
  material_class = ARRAY['Regulacion, atencion'],
  frequent_profile = ARRAY['TEA','discapacidad intelectual','altas capacidades','altas necesidades de apoyo'],
  specific_profile = ARRAY['TEA con apoyo leve','TEA con apoyo notable','TEA con mayor necesidad de apoyo','alto potencial intelectual','TDAH']
  WHERE name = 'Auriculares cancelacion de ruido';


-- 5) INSERT de los productos nuevos (16 del Listado FINAL + Tijera etapa 2) -

-- 5.1) Soporte para lapiz progresivo (etapas 3, 2, 1)
INSERT INTO devices (
    ramp_id, name, stage, quantity, sort_order, description, function_summary,
    observable_manifestations, pedagogical_situations, material_class,
    frequent_profile, specific_profile, needs_description, qr_code
) VALUES
  ((SELECT id FROM ramps WHERE name='Rampa Didactico-Pedagogica'), 'Soporte para lapiz 2 — etapa 3', 3, 10, 21,
   'Soporte adaptador de lapiz progresivo (etapa 3). Mejora la prension y favorece la postura adecuada.',
   'Mejora la prension del lapiz. Favorece la postura adecuada. Facilita el control del trazo. Reduce el esfuerzo en la escritura.',
   ARRAY['Sostiene mal el lapiz','Hace mucha fuerza al escribir','Se le cae el lapiz','Se cansa rapido al escribir','La letra es poco legible','Le cuesta controlar el trazo'],
   ARRAY['Escritura en clase','Actividades de copia','Tareas de produccion escrita','Ejercicios de grafomotricidad'],
   ARRAY['Acceso al aprendizaje'],
   ARRAY['DEA','TEA','discapacidad motora','discapacidad intelectual'],
   ARRAY['paralisis cerebral','sindrome de Down','TEA con apoyo notable','Disgrafia','TDAH'],
   'Acompana a estudiantes que necesitan apoyo intermedio para sostener el lapiz, con mayor sosten que la etapa 4.',
   'DEVICE-SLA-003'),
  ((SELECT id FROM ramps WHERE name='Rampa Didactico-Pedagogica'), 'Soporte para lapiz 3 — etapa 2', 2, 5, 22,
   'Soporte adaptador de lapiz progresivo (etapa 2).',
   'Mejora la prension del lapiz. Favorece la postura adecuada. Facilita el control del trazo. Reduce el esfuerzo en la escritura.',
   ARRAY['Sostiene mal el lapiz','Hace mucha fuerza al escribir','Se le cae el lapiz','Se cansa rapido al escribir','La letra es poco legible','Le cuesta controlar el trazo'],
   ARRAY['Escritura en clase','Actividades de copia','Tareas de produccion escrita','Ejercicios de grafomotricidad'],
   ARRAY['Acceso al aprendizaje'],
   ARRAY['DEA','TEA','discapacidad motora','discapacidad intelectual'],
   ARRAY['paralisis cerebral','sindrome de Down','TEA con apoyo notable','TEA con mayor necesidad de apoyo','Disgrafia'],
   'Acompana a estudiantes con mayor necesidad de sosten que la etapa 3.',
   'DEVICE-SLA-002'),
  ((SELECT id FROM ramps WHERE name='Rampa Didactico-Pedagogica'), 'Soporte para lapiz 4 — etapa 1', 1, 5, 23,
   'Soporte adaptador de lapiz progresivo (etapa 1, mayor sosten).',
   'Mejora la prension del lapiz. Favorece la postura adecuada. Facilita el control del trazo. Reduce el esfuerzo en la escritura.',
   ARRAY['Sostiene mal el lapiz','Hace mucha fuerza al escribir','Se le cae el lapiz','Se cansa rapido al escribir','La letra es poco legible','Le cuesta controlar el trazo'],
   ARRAY['Escritura en clase','Actividades de copia','Tareas de produccion escrita','Ejercicios de grafomotricidad'],
   ARRAY['Acceso al aprendizaje'],
   ARRAY['DEA','TEA','discapacidad motora','discapacidad intelectual'],
   ARRAY['paralisis cerebral','sindrome de Down','TEA con mayor necesidad de apoyo','Disgrafia'],
   'Acompana a estudiantes con dificultades motoras significativas que necesitan el maximo nivel de sosten.',
   'DEVICE-SLA-001')
ON CONFLICT (qr_code) DO NOTHING;

-- 5.2) Pesas para lapices
INSERT INTO devices (
    ramp_id, name, stage, quantity, sort_order, description, function_summary,
    observable_manifestations, pedagogical_situations, material_class,
    frequent_profile, specific_profile, needs_description, qr_code
) VALUES
  ((SELECT id FROM ramps WHERE name='Rampa Didactico-Pedagogica'), 'Pesas para lapices', NULL, 10, 24,
   'Pesas que se colocan sobre el lapiz para aumentar la estabilidad de la mano.',
   'Aumenta la estabilidad de la mano durante la escritura. Disminuye movimientos excesivos. Favorece el control del trazo. Mejora la precision.',
   ARRAY['Mueve mucho la mano al escribir','El trazo es inestable','Escribe con movimientos bruscos','Le cuesta controlar el lapiz','Cambia constantemente la posicion de la mano'],
   ARRAY['Actividades de escritura','Tareas que requieren precision','Trabajos prolongados de escritura','Momentos de copia o dictado'],
   ARRAY['Regulacion, atencion'],
   ARRAY['DEA','TEA','discapacidad motora','discapacidad intelectual'],
   ARRAY['paralisis cerebral','sindrome de Down','TEA con apoyo notable','Disgrafia','TDAH'],
   'Acompana a estudiantes con trazo inestable o movimientos involuntarios que afectan la escritura.',
   'DEVICE-PLA-001')
ON CONFLICT (qr_code) DO NOTHING;

-- 5.3) Tijera adaptada etapa 2 (la etapa 1 ya existe, esta es la nueva)
INSERT INTO devices (
    ramp_id, name, stage, quantity, sort_order, description, function_summary,
    observable_manifestations, pedagogical_situations, material_class,
    frequent_profile, specific_profile, needs_description, qr_code
) VALUES
  ((SELECT id FROM ramps WHERE name='Rampa Didactico-Pedagogica'), 'Tijera adaptada — etapa 2', 2, 1, 25,
   'Tijera adaptada con mayor asistencia mecanica (etapa 2).',
   'Facilita el uso funcional de la tijera. Permite el control del movimiento de corte. Reduce el esfuerzo en tareas de recorte.',
   ARRAY['No puede usar la tijera convencional','Tiene movimientos bruscos','No puede sostener la tijera','No puede usar las manos','Necesita ayuda para recortar'],
   ARRAY['Actividades de recorte','Trabajos manuales y plasticos','Tareas de motricidad fina','Actividades guiadas o autonomas'],
   ARRAY['Acceso al aprendizaje'],
   ARRAY['discapacidad motora','TEA','discapacidad intelectual'],
   ARRAY['paralisis cerebral','sindrome de Down','TEA con mayor necesidad de apoyo'],
   'Acompana a estudiantes con dificultades severas que no logran usar la tijera adaptada de etapa 1.',
   'DEVICE-TIJ-002')
ON CONFLICT (qr_code) DO NOTHING;

-- 5.4) Ayuda para lectura etapa 4 (transparente con renglon)
INSERT INTO devices (
    ramp_id, name, stage, quantity, sort_order, description, function_summary,
    observable_manifestations, pedagogical_situations, material_class,
    frequent_profile, specific_profile, needs_description, qr_code
) VALUES
  ((SELECT id FROM ramps WHERE name='Rampa Didactico-Pedagogica'), 'Ayuda para la lectura — Reglas de lectura transparente con renglon — etapa 4', 4, 10, 26,
   'Regla de lectura transparente con renglon resaltado (etapa 4 — ultima, mayor autonomia).',
   'Facilita el seguimiento visual del texto. Favorece la organizacion de la lectura. Facilita el acceso al contenido escrito.',
   ARRAY['Salta la linea al leer','Se desorienta en el texto','Lee muy lento','Se cansa al leer','Le cuesta seguir la lectura'],
   ARRAY['Actividades de lectura','Actividades de comprension lectora','Trabajo individual con textos','Tareas de copia'],
   ARRAY['Acceso al aprendizaje','atencion'],
   ARRAY['TEA','discapacidad intelectual','DEA','discapacidad visual'],
   ARRAY['TDAH','Dislexia','sindrome de Down','baja vision','TEA con apoyo leve'],
   'Acompana a estudiantes con buena fluidez que igual se benefician de un guia visual minimo.',
   'DEVICE-AYL-004')
ON CONFLICT (qr_code) DO NOTHING;

-- 5.5) Panel separador, organizador, mesa plegable
INSERT INTO devices (
    ramp_id, name, stage, quantity, sort_order, description, function_summary,
    observable_manifestations, pedagogical_situations, material_class,
    frequent_profile, specific_profile, needs_description, qr_code
) VALUES
  ((SELECT id FROM ramps WHERE name='Rampa Didactico-Pedagogica'), 'Panel separador de pupitre', NULL, 1, 27,
   'Panel que se coloca alrededor del pupitre para reducir estimulos visuales del entorno.',
   'Reduce estimulos visuales del entorno. Disminuye distractores. Favorece la concentracion en la tarea.',
   ARRAY['Se distrae con lo que sucede alrededor','Pierde el foco con facilidad','Le cuesta concentrarse en su tarea','Pierde la atencion','Le molesta el entorno'],
   ARRAY['Trabajo individual','Actividades que requieren concentracion sostenida','Momentos de sobrecarga de estimulos','Tareas complejas o nuevas'],
   ARRAY['Adaptacion del entorno','regulacion','atencion'],
   ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
   ARRAY['TDAH','TEA con apoyo leve','TEA con apoyo notable','alto potencial intelectual','Dislexia'],
   'Acompana a estudiantes que se sobreestimulan con el entorno y necesitan reducir distractores visuales.',
   'DEVICE-PSP-001'),
  ((SELECT id FROM ramps WHERE name='Rampa Didactico-Pedagogica'), 'Organizador de tareas personalizable', NULL, 4, 28,
   'Organizador visual configurable para estructurar la secuencia de actividades.',
   'Estructura la secuencia de actividades. Facilita la planificacion de la tarea. Mejora la organizacion personal. Reduce la ansiedad.',
   ARRAY['Olvida lo que tiene que hacer','No sabe por donde empezar','Deja tareas sin terminar','Se desorganiza facilmente','Pierde materiales','Le cuesta seguir una secuencia'],
   ARRAY['Inicio de una actividad','Planificacion de tareas','Trabajos por etapas','Seguimiento de actividades'],
   ARRAY['Organizacion','regulacion'],
   ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
   ARRAY['Dislexia','Disgrafia','sindrome de Down','TDAH','TEA con apoyo leve','TEA con apoyo notable'],
   'Acompana a estudiantes con dificultades de organizacion y planificacion temporal.',
   'DEVICE-ORG-001'),
  ((SELECT id FROM ramps WHERE name='Rampa Didactico-Pedagogica'), 'Mesa plegable portatil', NULL, 1, 29,
   'Mesa plegable portatil para favorecer la concentracion generando un espacio individual.',
   'Reduce la exposicion a estimulos del entorno. Genera un espacio de trabajo con menor distraccion. Favorece la concentracion.',
   ARRAY['Se distrae con lo que sucede alrededor','Pierde el foco con facilidad','Le cuesta concentrarse en su tarea','Se sobreestimula facilmente','Busca lugares tranquilos para trabajar'],
   ARRAY['Inicio de una tarea','Actividades con tiempo limitado','Transiciones entre actividades','Trabajo individual','Actividades que requieren concentracion sostenida'],
   ARRAY['Adaptacion del entorno','regulacion','atencion'],
   ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
   ARRAY['Dislexia','sindrome de Down','TDAH','TEA con apoyo leve','TEA con apoyo notable','alto potencial intelectual'],
   'Acompana a estudiantes que necesitan retirarse del estimulo grupal sin abandonar el aula.',
   'DEVICE-MPP-001')
ON CONFLICT (qr_code) DO NOTHING;

-- 5.6) Productos para zurdos (NEEDS_VALIDATION: Mercedes debe completar metadata)
INSERT INTO devices (
    ramp_id, name, stage, quantity, sort_order, description, function_summary,
    observable_manifestations, pedagogical_situations, material_class,
    frequent_profile, specific_profile, needs_description, qr_code
) VALUES
  ((SELECT id FROM ramps WHERE name='Rampa Didactico-Pedagogica'), 'Sacapuntas para zurdos', NULL, 1, 41,
   'Sacapuntas con orientacion adaptada para zurdos.',
   NULL,
   ARRAY['Se cansa al sacar punta','Le cuesta usar el sacapuntas','Necesita herramientas para zurdos'],
   ARRAY['Actividades de escritura','Tareas con lapiz'],
   ARRAY['Acceso al aprendizaje'],
   ARRAY['DEA'],
   ARRAY[]::text[],
   'Acompana a estudiantes zurdos que se frustran con sacapuntas convencionales.',
   'DEVICE-ZUR-001'),
  ((SELECT id FROM ramps WHERE name='Rampa Didactico-Pedagogica'), 'Lapicera para zurdos', NULL, 1, 42,
   'Lapicera ergonomica para zurdos.',
   NULL,
   ARRAY['Mancha el cuaderno al escribir','Le cuesta sostener la lapicera','Necesita herramientas para zurdos'],
   ARRAY['Actividades de escritura'],
   ARRAY['Acceso al aprendizaje'],
   ARRAY['DEA'],
   ARRAY[]::text[],
   'Acompana a estudiantes zurdos en actividades de escritura prolongada.',
   'DEVICE-ZUR-002'),
  ((SELECT id FROM ramps WHERE name='Rampa Didactico-Pedagogica'), 'Tijera para zurdos', NULL, 1, 43,
   'Tijera con orientacion adaptada para zurdos.',
   NULL,
   ARRAY['Le cuesta cortar con tijera convencional','Necesita herramientas para zurdos'],
   ARRAY['Actividades de recorte','Trabajos manuales'],
   ARRAY['Acceso al aprendizaje'],
   ARRAY['DEA'],
   ARRAY[]::text[],
   'Acompana a estudiantes zurdos en tareas de recorte.',
   'DEVICE-ZUR-003')
ON CONFLICT (qr_code) DO NOTHING;

-- 5.7) Mouse Admouse (Rampa Digital)
INSERT INTO devices (
    ramp_id, name, stage, quantity, sort_order, description, function_summary,
    observable_manifestations, pedagogical_situations, material_class,
    frequent_profile, specific_profile, needs_description, qr_code
) VALUES
  ((SELECT id FROM ramps WHERE name='Rampa Digital'), 'Mouse Admouse', NULL, 1, 11,
   'Mouse adaptativo de gran formato. Pensado para acceso motor y cognitivo simplificado.',
   'Facilita el control del cursor sin desplazamiento del dispositivo. Mejora la precision del movimiento. Reduce la exigencia motora fina. Favorece la autonomia.',
   ARRAY['No logra usar mouse convencional','No entiende los comandos','Le cuesta orientarse en el espacio','Le cuesta identificar los botones','Le cuesta controlar el movimiento','Necesita movimientos mas amplios','Se frustra con dispositivos pequenos'],
   ARRAY['Uso de computadora adaptada','Actividades digitales','Tareas de acceso al dispositivo','Trabajo autonomo con tecnologia'],
   ARRAY['Accesibilidad tecnologica'],
   ARRAY['discapacidad intelectual','TEA','discapacidad visual','discapacidad motora'],
   ARRAY['sindrome de Down','TEA con mayor necesidad de apoyo','TEA con apoyo notable','multidiscapacidad','baja vision','paralisis cerebral'],
   'Acompana a estudiantes que no logran usar mouse convencional por baja precision o dificultades cognitivas.',
   'DEVICE-ADM-001')
ON CONFLICT (qr_code) DO NOTHING;

-- 5.8) Rampa Sensorial: Munequera, SPEKS, SPEKS textura, Pelota pie/muslo, BouncyBand cojin
INSERT INTO devices (
    ramp_id, name, stage, quantity, sort_order, description, function_summary,
    observable_manifestations, pedagogical_situations, material_class,
    frequent_profile, specific_profile, needs_description, qr_code
) VALUES
  ((SELECT id FROM ramps WHERE name='Rampa de Autorregulacion Sensorial'), 'Munequera sensorial x2', NULL, 2, 31,
   'Par de munequeras sensoriales con peso liviano que aportan estabilidad propioceptiva.',
   'Aumenta la estabilidad de la mano durante la escritura. Disminuye movimientos excesivos. Favorece el control del trazo.',
   ARRAY['Mueve mucho la mano al escribir','El trazo es inestable','Escribe con movimientos bruscos','Le cuesta controlar el lapiz','Cambia constantemente la posicion de la mano'],
   ARRAY['Actividades de escritura','Tareas que requieren precision','Trabajos prolongados','Momentos de copia o dictado'],
   ARRAY['Regulacion, atencion'],
   ARRAY['DEA','TEA','discapacidad motora','discapacidad intelectual'],
   ARRAY['Disgrafia','TDAH','paralisis cerebral','sindrome de Down'],
   'Acompana a estudiantes con trazo inestable que se benefician de input propioceptivo.',
   'DEVICE-MUN-001'),
  ((SELECT id FROM ramps WHERE name='Rampa de Autorregulacion Sensorial'), 'Material sensorial de apriete SPEKS', NULL, 6, 32,
   'Set de bolitas magneticas SPEKS para canalizar la necesidad de movimiento manual.',
   'Canaliza la necesidad de movimiento manual. Favorece la autorregulacion durante la tarea. Reduce la inquietud motora.',
   ARRAY['Se inquieta constantemente','Necesita manipular objetos','Lleva objetos a la boca','Se muerde las unas','Le cuesta quedarse quieto','Se distrae con facilidad','Busca estimulos con las manos','Se pone ansioso durante la tarea'],
   ARRAY['Actividades que requieren concentracion','Momentos de escucha (clase expositiva)','Trabajo autonomo','Situaciones de espera / ansiedad'],
   ARRAY['Regulacion, atencion'],
   ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
   ARRAY['TDAH','TEA con apoyo leve','Dislexia','alto potencial intelectual'],
   'Acompana a estudiantes que necesitan manipular objetos para sostener la atencion.',
   'DEVICE-SPK-001'),
  ((SELECT id FROM ramps WHERE name='Rampa de Autorregulacion Sensorial'), 'Material sensorial de apriete SPEKS con textura', NULL, 2, 33,
   'Variante con textura del SPEKS, para input sensorial adicional.',
   'Canaliza la necesidad de movimiento manual. Favorece la autorregulacion durante la tarea. Reduce la inquietud motora.',
   ARRAY['Se inquieta constantemente','Necesita manipular objetos','Lleva objetos a la boca','Se muerde las unas','Le cuesta quedarse quieto','Se distrae con facilidad','Busca estimulos con las manos','Se pone ansioso durante la tarea'],
   ARRAY['Actividades que requieren concentracion','Momentos de escucha','Trabajo autonomo','Situaciones de espera / ansiedad'],
   ARRAY['Regulacion, atencion'],
   ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
   ARRAY['TDAH','TEA con apoyo leve','Dislexia','alto potencial intelectual'],
   'Para estudiantes que necesitan input sensorial adicional al SPEKS estandar.',
   'DEVICE-SPK-002'),
  ((SELECT id FROM ramps WHERE name='Rampa de Autorregulacion Sensorial'), 'Pelota para el pie (vaiven) o muslo (presion)', NULL, 3, 34,
   'Pelota que se usa apoyada en el pie (vaiven) o bajo el muslo (presion) para canalizar movimiento sin abandonar la tarea.',
   'Permite el movimiento sin abandonar la tarea. Canaliza la inquietud motora. Favorece la permanencia en el lugar.',
   ARRAY['Mueve constantemente las piernas','Se levanta de la silla','No logra quedarse sentado','Necesita moverse mientras trabaja','Se inquieta durante la actividad'],
   ARRAY['Trabajo en mesa','Actividades largas','Momentos que requieren permanencia sentado','Tareas individuales'],
   ARRAY['Regulacion, atencion'],
   ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
   ARRAY['TDAH','TEA con apoyo notable','alto potencial intelectual','Dislexia'],
   'Acompana a estudiantes que necesitan canalizar el movimiento de piernas para sostener la atencion.',
   'DEVICE-PEP-001'),
  ((SELECT id FROM ramps WHERE name='Rampa de Autorregulacion Sensorial'), 'BouncyBand Sit & Twist Cojin de Asiento Activo', NULL, 1, 35,
   'Cojin de asiento activo que permite movimiento controlado en la silla.',
   'Permite el movimiento controlado en la silla. Reduce la necesidad de levantarse. Favorece la autorregulacion motora.',
   ARRAY['Se balancea en la silla','Se levanta con frecuencia','Mueve constantemente el cuerpo','Le cuesta permanecer en su lugar','Interrumpe la tarea por movimiento','Pierde la atencion con facilidad'],
   ARRAY['Actividades en el pupitre','Trabajo prolongado','Momentos de escucha','Tareas individuales'],
   ARRAY['Regulacion, atencion'],
   ARRAY['TEA','discapacidad intelectual','DEA','altas capacidades'],
   ARRAY['TDAH','TEA con apoyo leve','TEA con apoyo notable','alto potencial intelectual','Dislexia'],
   'Acompana a estudiantes que se balancean o no logran permanecer sentados.',
   'DEVICE-BBC-001')
ON CONFLICT (qr_code) DO NOTHING;

COMMIT;
