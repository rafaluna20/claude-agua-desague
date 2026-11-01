# Informe de entrega T-02

**Tarea:** T-02 Libro de normas de agua y desagüe (Fase 1)
**Responsable:** sanit-normas
**Versión:** 0.2 (2026-10-13). Repite la tarea y reemplaza a la v0.1 del 2026-10-10.
**Estado profesional:** documento interno. Nada de aquí es dictamen ni opinión legal. **PARA VALIDAR CON VALVERDE.**

## 1. Qué hice

- Leí la ficha, `LEEME.md`, `ESTADO.md`, `supuestos.md`, la plantilla, el informe de no conformidad, el sustento del contratista, el resumen de Renasur y TL-GES-009.
- Releí completos, en el texto, el reglamento CTPS-PR-02 (partes 01 y 02), la especificación CTPS-ET-0060 y OS.070 (local y cotejado con el PDF oficial).
- Descargué y leí los PDF oficiales de OS.050, OS.030, OS.100, OS.090 (secciones 4, 5.1, 5.2 y 5.7), OS.010 (búsqueda dirigida), RM 0107-2025-VIVIENDA (IS.010), A.020 art. 7, DS 003-2010-MINAM y la sección de Lima de SENAMHI "Climas del Perú". Guardé sus textos en `normas/textos_fuente/` con hashes.
- Rehice el libro: 100 IDs (N-001 a N-100) con numeral, valor, cita literal, fuente con línea o URL y estado. Mantuve los ID de la v0.1 para no romper referencias y corregí errores de ella (sección 2 del libro).
- Rehice conflictos y brechas: 19 contradicciones entre normas (C-001 a C-019), 20 afirmaciones del informe, del contratista y del resumen contrastadas con los textos (A-01 a A-20) y la lista de textos que faltan.
- Verifiqué con un script que las citas literales de las 92 filas VERIFICADO están en los textos fuente.

## 2. Archivos producidos

Rutas relativas a `W_contraste/`:

- `normas/libro_normas.md` v0.2: 100 IDs. **VERIFICADO 92** (8 con una reserva expresa sobre numeral, alcance o aplicabilidad), **NO VERIFICADO 7**, **RETIRADO 1**.
- `normas/conflictos_y_brechas.md` v0.2.
- `tareas/T-02_informe.md` (este informe).
- `normas/textos_fuente/` (insumo de verificación, no entregable): copias de texto de OS030, OS050, OS070 (web), OS090, OS100, OS010, IS010 (RM 0107-2025), A020, DS003-2010-MINAM y un extracto de SENAMHI, más `SHA256_textos_fuente.txt`.

No se tocó nada de `obra agua y desague/`, ni `supuestos.md`, ni `ESTADO.md`.

## 3. Supuestos nuevos propuestos

No agregué nada a `supuestos.md`. Propuestas para que el principal decida (ID provisional):

- **P-01** Corregir en S-016 el numeral de la regla de cruce de CTPS: es el art. 8.4.6 (párrafos finales, pág. 38 de 88), no el 8.4.5. Fuente: N-014. Motivo: el 8.4.5 es la tabla de distancias horizontales.
- **P-02** No usar S-004 (169 L/hab/día) como dato firme hasta clasificar el clima del punto con el visor SENAMHI. Fuente: N-036, N-080, N-081. Motivo: el texto SENAMHI describe la costa de Lima como árida y templada, que en IS.010 corresponde a 155.
- **P-03** Citar OS.100 1.3 b) ("por lo menos ... 6 hab/vivienda" en habilitaciones nuevas) como respaldo de S-003, además de CTPS NSE C. Fuente: N-073.
- **P-04** Marcar la regla de cruce de CTPS (0,10 m y concreto 1,00 m por lado) como "alcance por confirmar" en S-016 hasta cotejar el PDF original. Fuente: N-014, N-066.

## 4. Dudas abiertas

1. ¿Qué entidad recibe cada parte (SEDAPAL, Asociación Santa María o ambas)? Define si rige CTPS (C-009).
2. ¿Dónde están los Anexos A-1, A-2 y B del Contrato 005-2026 y la especificación de tubería de agua? Sin ellos no se prueba ninguna exigencia de PN ni de pruebas.
3. ¿Se puede obtener el PDF original de CTPS-PR-02? Hay tres puntos que dependen de su lectura: el numeral y alcance del cruce, el exponente -0.57 de la pendiente mínima y la tabla de buzones.
4. ¿Cuál es el clima de Pucusana en el visor SENAMHI y qué regla de dotación gobierna la red de la habilitación: IS.010, OS.100 o CTPS (C-007, C-019)?
5. ¿Cuántos cruces hay y de qué tipo (colector, ramal o conexión predial), con qué cotas y uniones (C-002, C-005)?
6. ¿Cuál es la tecnología de la PTAR y el destino del efluente (vertimiento, mar o reúso)? De ello dependen la distancia (N-047) y los LMP (N-098).

## 5. Autocomprobaciones realizadas

- **Citas:** un script comparó cada cita literal de la columna "Texto citado" con el texto normalizado de las fuentes. Resultado: 0 citas no halladas. Se corrigieron antes seis citas que mezclaban líneas, viñetas u OCR.
- **Líneas:** un segundo script comprobó que cada cita aparece dentro del rango de líneas indicado (con holgura de 6 líneas). Resultado: sin fallos, salvo una advertencia de formato en N-039 (la cifra sale pegada en la copia local de OS.070; el valor está en la copia web).
- **OS.070:** el texto local se cotejó con el PDF oficial de gob.pe: mismos valores (0,25 m, 3 m, tabla 1, exponente -0,47).
- **OS.050:** dos URL oficiales distintas dieron texto idéntico. Lectura completa: no tiene regla de cruce, ni pruebas, ni PN.
- **Búsquedas negativas:** `PN`, `presión nominal`, `kg/cm`, `clase 10`, `7,5`, `hidrost`, `prueba hidr`, `estanqueidad`, `1,5 veces` sobre CTPS (ambas partes), ET-0060, OS.070, OS.050, OS.010, OS.030 y OS.100. Los resultados están en N-024, N-032, N-041, N-069, N-090 y N-091.
- **Errores de la v0.1 corregidos:** numeral del cruce de CTPS (N-014), cita de N-034, N-047 que sí se pudo verificar, N-048 retirado por no tener texto.
- **Contraste con TL-GES-009:** TL-GES-009 se comparó con los textos (A-17 a A-20): coincide en lo de CTPS y en el PN10 de válvulas, pero trata como "incorrecto" el 3 m a cada lado, que es el valor de OS.070 4.7.

## 6. Qué NO pude verificar

- Pruebas hidráulicas, estanqueidad, tolerancias y desinfección de redes (N-024, N-041): ningún texto leído las desarrolla; falta la especificación de ejecución de SEDAPAL/contrato y CTPS-ET-004.
- Clase o PN de la tubería de agua que exige la especificación de SEDAPAL o el contrato (N-040): falta la especificación y el Anexo A-2. Tampoco verifiqué qué tubería se instaló.
- Carácter de clima de Pucusana (N-081), número y vigencia de la RM que aprueba A.020 (N-083), vigencia del RNE a octubre de 2026 (N-084; solo un resumen web de RM 278-2026) y normas de reúso, ECA y autorización de vertimiento (N-099).
- Si los párrafos del cruce de CTPS valen en general o solo dentro de la excepción de zonas consolidadas (N-014, N-066), el exponente de la fórmula de CTPS (N-054) y la unidad del límite de sólidos en suspensión de DS 003-2010 (N-045): el OCR o el PDF mezclan columnas; hay que cotejar los originales.
- Del texto de OS.090 leí las secciones 4, 5.1, 5.2 y 5.7; no leí las secciones de procesos (5.3 a 5.6, 5.8 y 5.9) salvo búsquedas de distancias.
- No leí CE.010 (citada por el contratista), OS.060, OS.080 ni el texto anterior de IS.010 2.2.
- Que la Asociación Santa María o SEDAPAL apliquen CTPS-PR-02 a este proyecto (C-009), y cualquier conclusión contractual, legal, de recepción o de subsanación: **PARA VALIDAR CON VALVERDE**.

## Anexo: respuestas explícitas pedidas por la ficha

**1. ¿El reglamento CTPS-PR-02 contiene la frase "PN 10 mínimo"?**

**No, como exigencia para la tubería de agua potable.** Búsqueda sobre las dos partes (conversión OCR):

- Parte 01, art. 8.5.6, L2778-2779: “Válvulas Compuerta: serán como mínimo de clase PN10 y se instalarán en la red de distribución.” L2781: “Válvulas Mariposa: serán como mínimo de clase PN16.” El PN10 mínimo es de la **válvula de compuerta**.
- Parte 02, Anexo 2, L716-719: aparecen los encabezados "PN 10" y "PN 16" en la tabla de equivalencias de diámetros de PVC-U y PEAD; no hay frase de mínimo. Las notas del anexo remiten a "especificaciones técnicas de SEDAPAL" y nombran NTP ISO-4422-2003 (PVC-U) y NTP ISO-4427 (PEAD).
- No existe "PN 7.5", "clase 10" ni "kg/cm²" de tubería en el reglamento.
- Fuera del reglamento, en la carpeta la única frase literal “serán para una presión nominal mínimo de PN10” está en CTPS-ET-0060, 6.2.4, para **PEAD de líneas de impulsión de alcantarillado** (DN ≤ 200, HDT ≤ 30 m), no para agua potable.
- La frase que el informe de no conformidad atribuye a las "Especificaciones Técnicas Generales de Materiales de las EPS" (“presión nominal mínima de 10 kg/cm² (PN 10)”) no aparece en ningún texto de la carpeta. Eso no prueba que la especificación de SEDAPAL no la tenga: esa especificación no fue entregada.
- Esto coincide con TL-GES-009 (solo válvulas) y le agrega el PN10 de ET-0060 para impulsión de alcantarillado.

**2. ¿Qué dice CTPS-PR-02 sobre cruces invertidos?** (filas N-014, N-066; compara con TL-GES-009)

- Texto (P1 L2716-2723, pág. 38 de 88, en los párrafos finales que siguen a ART. 8.4.6): “el diseño deberá contemplar de preferencia el pase de las tuberías de agua por encima de las de alcantarillado, con una distancia libre vertical mínima de 0,10 m. Si por razones de niveles, no es posible proyectar la tubería de agua potable por encima de la tubería de alcantarillado, y si fuera imprescindible proyectarla cruzándola por la parte inferior, se tratará en la posible que no coincidan las uniones de tuberías (de los tramos que conforman la linea) de ambos servicios, debiéndose garantizar la hermeticidad de la tubería como del sistema de unión entre tubos, o en su defecto se diseñará una protección con concreto en la tubería de alcantarillado, en una longitud de 1,00 m a cada lado del punto de cruce.”
- Lectura: el cruce invertido (agua por debajo del desagüe) **no está prohibido**; es excepcional y lleva una de dos medidas (no coincidir uniones y garantizar hermeticidad, o concreto en el alcantarillado, 1,00 m por lado). El texto dice "concreto", no "concreto armado". Los casos fuera de rangos "deberán ser debidamente sustentados".
- RNE OS.070 4.7 (otra norma, otro valor): agua por encima con 0,25 m entre tuberías principales; si no es posible, protección de concreto en el colector 3 m a cada lado.
- **Correcciones respecto de la v0.1 y de `supuestos.md`:** el numeral es 8.4.6 (párrafos finales), no 8.4.5. Además, esos párrafos aparecen después de un texto sobre excepciones "sólo en zonas consolidadas"; con el OCR no se puede confirmar si valen en general. Por eso N-014 queda con esa reserva.
- **Contraste con TL-GES-009:** coincide en 0,10 m, en la preferencia por agua arriba, en la excepción con concreto 1,00 m y en la página 38. Difiere en que TL-GES-009 llama "incorrecto" al encamisado de 3 m, que es el valor de OS.070 4.7 (norma que TL-GES-009 no tenía).
- **Contraste con el informe de no conformidad:** su cita de CTPS es literal pero omite la alternativa "o en su defecto", agrega "armado" y lo presenta como obligación; su cita de OS.070 es una paráfrasis presentada como literal; y OS.050 no contiene regla de cruce.
