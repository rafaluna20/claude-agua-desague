# Ficha de tarea T-02: Libro de normas de agua y desagüe

- **Responsable:** sanit-normas
- **Objetivo (1 frase):** dejar por escrito, con numeral y texto citado, los criterios de diseño y de verificación de agua potable y alcantarillado que aplican a Terra Lima / Pucusana, indicando cuáles verificó en el texto y cuáles no.
- **Entradas (rutas):**
  - Carpeta `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\obra agua y desague\`: `reglamento_saneamiento_parte 01.md` y `parte 02.md` (reglamento SEDAPAL CTPS-PR-02), `01-tuberias-y-accesorios-para-el-sistema-de-alcantarillado.md` (especificación de alcantarillado), `informe_tecnico_deNoConformidad.md` (borrador sin firma, NO es norma), `SUSTENTO_TECNICO_contratista.md` (NO es norma; es lo que alega el contratista), `resumen de  informacion de renasur.md`.
  - `W_contraste/normas/OS070_texto.txt` (texto de OS.070 ya extraído y leído el 2026-10-09).
  - `W_contraste/supuestos.md` (supuestos S-001 a S-019; los de tipo VERIFICADO-NORMA ya tienen respaldo en OS.070).
  - Notas internas para contexto: `..\TL-TEC-001..005_*.md` y el registro de problemas `B_GESTION_INTERNA\B1_Gestion\04.01_Plan_Ejecucion\TL-GES-009_2026-10-04_Verificacion_Informe_No_Conformidad.md`.
  - Web (WebSearch/WebFetch) solo para lo que no esté en los archivos locales: RNE OS.050, OS.090, IS.010 (incluida la RM 0107-2025-VIVIENDA), A.020, límites máximos permisibles de efluentes de PTAR domésticas. Anotar URL y fecha de cada consulta.
- **Salidas esperadas:**
  1. `normas/libro_normas.md`: tabla con columnas: ID (N-001…), tema, norma, numeral, valor/criterio, texto citado literal (corto), fuente (archivo o URL), estado (VERIFICADO = leído en texto / NO VERIFICADO = resumen o memoria).
  2. `normas/conflictos_y_brechas.md`: (a) contradicciones entre RNE, SEDAPAL CTPS-PR-02/ET y las afirmaciones del informe de no conformidad y del contratista; (b) lista de textos que faltan y a quién pedirlos.
  3. `tareas/T-02_informe.md` con el formato de `PLANTILLA_informe_entrega.md`.
- **Temas obligatorios (cada uno con su fila):**
  - Desagüe: diámetro mínimo; recubrimiento mínimo; separación horizontal y vertical con agua potable; cruces invertidos (protección de concreto: longitud y condiciones); tipo y diámetro de buzones; distancia máxima entre buzones; caídas; pendiente mínima / tensión tractiva; velocidades; relación y/D; conexión domiciliaria; materiales y rigidez de tubería (NTP, SN); pruebas hidráulicas; tolerancias.
  - Agua: dotación y cómo se clasifica el clima (IS.010 actualizada); densidad por vivienda (A.020); coeficientes K1 y K2; presiones mínima y máxima; diámetro mínimo; velocidades; hidrantes; volumen del reservorio (regulación + reserva); material y clase/PN de tuberías bajo vía vehicular; profundidad mínima; pruebas de presión y desinfección; válvulas.
  - PTAR: criterios de OS.090 relevantes para dimensionar y ubicar; límites de efluente aplicables; distancias mínimas a viviendas.
  - Hechos que el usuario ya adoptó y deben contrastarse: S-004 (dotación 169 L/hab/día), S-003 (6 hab/vivienda), S-013 (DN mínimo 200 mm), S-016 (separación agua/desagüe).
- **Criterios de aceptación (verificables):** cada fila tiene fuente y estado; ningún valor marcado VERIFICADO sin texto citado; todos los temas obligatorios aparecen (aunque sea como NO VERIFICADO con la razón); el informe lista qué falta y a quién pedirlo; se responde explícitamente si el reglamento CTPS-PR-02 contiene o no la frase "PN 10 mínimo" y qué dice sobre cruces invertidos (comparar con TL-GES-009).
- **Normas que debe citar:** RNE OS.050, OS.070, OS.090, IS.010, A.020; SEDAPAL CTPS-PR-02 y la especificación de alcantarillado de la carpeta.
- **Prohibido:** inventar valores o numerales; presentar como verificado algo que solo viene de un resumen web; escribir fuera de `W_contraste/`; modificar los archivos de `obra agua y desague/`; emitir opinión legal (marcar PARA VALIDAR CON VALVERDE).
- **Supuestos que puede usar:** los de `supuestos.md`; todo supuesto nuevo se propone, no se asume.
- **Formato del informe de entrega:** `tareas/PLANTILLA_informe_entrega.md`.
