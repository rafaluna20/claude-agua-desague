# Informe de entrega T-03 — Inventario de lo ejecutado (S&G Edifica) y brechas de información — v2.0

Corte: 2026-10-13. Responsable: sanit-datos. **PARA VALIDAR CON VALVERDE** y con ingeniero sanitario colegiado antes de cualquier uso contractual, legal, de recepción o frente a terceros.

## 1. Qué hice (resumen)

- Leí completos la ficha, las reglas del espacio, Carta 014 y sustento de S&G, el borrador de no conformidad, el resumen interno, el contrato (PDF firmado y DOCX editable), la ficha del contrato, TL-GES-004 a 010, los LEEME P1/P2, TL-COR-OUT-001 y TL-TEC-001 a 005.
- Inventarié **44 hechos** con archivo y ubicación (línea, página o cláusula), tipo de fuente y estado: CONFIRMADO 12, ALEGADO POR EL CONTRATISTA 5, BORRADOR 2, POR CONFIRMAR 25. Los CONFIRMADO son documentales (qué dice un documento o que falta uno), no verificación de obra.
- **No existe ningún dato verificado de la red ejecutada** (diámetro, material, PN, profundidad, buzones, longitudes, cruces, pruebas). Lo único numérico sobre obra es la alegación de S&G sobre un punto (agua 0.30-0.45 m bajo una conexión; figuras 0.27/0.30/0.28 m), el 'PN 7.5' del borrador sin firma y el '1.40-1.50 m' de un resumen interno.
- **Plano o dato georreferenciado de la red ejecutada: NO se encontró.** Sí hay georreferenciación de **diseño** (tabla de 202 buzones con coordenadas UTM WGS-84/18S en el plano de 2025 y buzones con cotas en el juego de planos de 2023); no es evidencia de obra.
- Listé 13 discrepancias entre fuentes sin resolverlas y 22 brechas de información con destinatario.
- Hallazgos fuera de la ficha: (a) el PDF 'firmado' del contrato **difiere** del DOCX y de la ficha (plazo hábiles vs calendario, penalidad 3% vs 0.5%/10%, sin anexos ni cláusula de supervisor, 'Sector I' ausente, Tacna vs Lima); (b) **dos juegos de diseño de agua y alcantarillado** fuera del expediente (`05 EXPEDIENTE V2`, 2025; `Control-company\03 renacimiento del sur sac\planos agua y desague`, 2023); (c) una hoja de cálculo sin autor (`cotizacion de  conexiones.xlsx`, 2025-12-20) que lista 'PVC-U ISO 1452 **C-7.5** DN 110 mm', 34 buzones y 225 conexiones.
- Calculé SHA-256 y tamaño de las fuentes; no copié ni modifiqué ningún archivo. Se conservó v1.1 en `datos/ejecutado_v1/historico_v1.1/`.

## 2. Archivos producidos

| Archivo | Versión |
|---|---|
| `W_contraste/datos/ejecutado_v1/inventario_ejecutado.md` | v2.0 |
| `W_contraste/datos/ejecutado_v1/inventario_ejecutado.json` | v2.0 (generado del mismo conjunto de datos que el .md) |
| `W_contraste/datos/ejecutado_v1/brechas_de_informacion.md` | v2.0 |
| `W_contraste/datos/ejecutado_v1/archivos_utiles.md` | v2.0 |
| `W_contraste/datos/ejecutado_v1/historico_v1.1/` | copia de los cuatro archivos de v1.1 |
| `W_contraste/tareas/T-03_informe.md` | este informe, v2.0 |
| `W_contraste/supuestos.md` | **añadida** la sección 'Propuestas T-03' (P-T03-01 a 09); no se tocó ninguna fila existente |

## 3. Supuestos nuevos propuestos

Ninguno de diseño. Se proponen, como **PROPUESTA** y sin adoptarlos, nueve criterios de tratamiento de discrepancias (P-T03-01 a P-T03-09 en `supuestos.md`): no adoptar 23.86% ni ~90% (D-001); tratar 'PN 7.5' como alegación sin evidencia y 'PN 10' como exigencia no acreditada (D-002); registrar un solo cruce documentado (D-003/D-004); escribir 'Parte 1, extensión por confirmar' (D-005); PDF firmado como fuente primaria del contrato hasta que Valverde decida (D-006); no tomar ningún juego de diseño como lo contratado (D-009/D-013); no usar '1.40-1.50 m' (D-010); citar la fuente de cada cifra del diseño 2025 (D-008); 'sin carta formal enviada' como relato (D-007).

## 4. Dudas abiertas (qué necesito del usuario o del ingeniero)

1. Rafael / Lenin Beker: ¿cuál de los dos juegos de diseño (2023 o 2025) se entregó a S&G, cuál es el vigente y quién elaboró `cotizacion de  conexiones.xlsx`? (B-13, B-21).
2. Valverde: ¿qué texto del contrato rige (PDF o DOCX) y existen los Anexos A y B rubricados? (B-06).
3. Usuario: ¿qué es `ia analisis\diseño corte de agua y desague.dwg` y el DWG de Civil 3D tiene alguna capa de red construida? (B-22).
4. María Fernanda / Odoo: valorizaciones y pagos reales de S&G para resolver 23.86% vs ~90% (B-08).
5. Rafael: ¿se envió el borrador de no conformidad o alguna carta formal? Hay un registro que lo duda (D-007).
6. ¿Se amplía T-03 para extraer a CSV la tabla de 202 buzones del plano de 2025 (p.8) como línea base de diseño? No lo hice porque excede la ficha.

## 5. Autocomprobaciones realizadas

- Cada hecho tiene `id`, `tema`, `valor`, `fuente`, `tipo_fuente` y `estado`; el script aborta si falta alguno o si el estado no es uno de los cuatro permitidos. Resultado: 44 de 44 válidos.
- Cada clave de fuente citada (S01 a S26) existe en la tabla de fuentes; cada referencia cruzada E-xxx, D-xxx y B-xx apunta a un elemento existente.
- El .md y el .json salen del mismo conjunto de datos: 44 hechos en cada uno (lección de G1-04).
- Verifiqué en el PDF firmado, página por página, dónde está cada cláusula citada (p.2 a p.5) y comparé su texto con el DOCX; los números de línea de los .md se tomaron de la lectura del corte.
- Verifiqué por listado de directorios que valorizaciones, cronograma, contratos/ofertas, cuaderno de obra, certificados y B5 tienen 0 archivos; que no hay DWG de red ejecutada en `exp.-terraLima_v2` ni en `05 EXPEDIENTE V2`; y que las imágenes incrustadas del PDF firmado son logotipos.
- Contrasté con pypdf que los PDF de planos tienen medida rectilínea (no georreferencia embebida) y conté 202 filas (BZ-1 a BZ-202) en la tabla de buzones del plano de 2025.
- Rutas de los archivos entregados: máximo 170 caracteres (límite 200); nombres sin tildes ni espacios.

## 6. Qué NO pude verificar (explícito)

- Ninguna geometría, cota, profundidad, diámetro, material, PN, buzón, metrado, prueba o certificado de la red ejecutada: no hay documento que lo contenga.
- Firmas y sellos manuscritos del contrato 'firmado' (no pude renderizar el PDF; falta poppler).
- El contenido de `diseño corte de agua y desague.dwg` y del DWG vivo de Civil 3D más allá de las 11 capas exportadas; Odoo (valorizaciones, pagos, bitácora con fotos); discos externos, correo y WhatsApp.
- Las citas normativas de S&G, del borrador y del resumen (corresponde a T-02 y a Beker); no emití opinión sobre cumplimiento ni sobre responsabilidad.
- La búsqueda por palabras clave en el Escritorio no es exhaustiva (carpetas `Downloads`, `escritorio 2025` y otras empresas de `Control-company` solo se revisaron por nombre de archivo o por coincidencias puntuales).
- Todo lo contractual o legal queda **PARA VALIDAR CON VALVERDE**. Sugerencia al principal: actualizar la fila T-03 de `ESTADO.md` (v2.0, con los dos juegos de diseño y la discrepancia del contrato); no la modifiqué.
