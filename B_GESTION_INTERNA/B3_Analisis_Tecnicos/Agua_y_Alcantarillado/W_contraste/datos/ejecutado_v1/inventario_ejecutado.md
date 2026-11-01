# Inventario de la obra de agua y alcantarillado ejecutada por S&G Edifica — v2.0

**Corte:** 2026-10-13. **Tarea:** T-03 (sanit-datos). **Uso:** contraste técnico interno; no es un documento presentable a terceros.  
**Estado profesional y legal:** **PARA VALIDAR CON VALVERDE** y con ingeniero sanitario colegiado. Este inventario no acredita recepción, conformidad, metrados reales ni calidad de obra.  
**Versión:** v2.0 reemplaza a v1.1 (copia en `historico_v1.1/`). Cambios al final.

## 0. Resumen

- Hechos registrados: **44**. Por estado: **CONFIRMADO 12**, **ALEGADO POR EL CONTRATISTA 5**, **BORRADOR 2**, **POR CONFIRMAR 25**.
- **No hay ningún dato verificado de la red ejecutada** (diámetro, material, clase/PN, profundidad, recubrimiento, número de buzones, longitudes, cruces, pruebas). Todo lo que existe es alegación del contratista, borrador interno sin firma, relato interno sin respaldo, o diseño original (no ejecutado).
- Se localizaron **dos juegos de planos/memorias de DISEÑO** (2023 y 2025) fuera de `exp.-terraLima_v2` (E-033 a E-039, E-043). Son diseño, no obra; cuál fue entregado a S&G es POR CONFIRMAR (D-013, B-13).
- Los hechos con estado CONFIRMADO son **documentales** (qué dice un documento o que falta un documento); no son verificación física de obra.
- Discrepancias entre fuentes listadas y **no resueltas**: **13** (sección 6). Las principales: avance 23.86% vs ~90% (D-001); PN 7.5 vs PN 10 vs diseño original C-10/PN8/clase 6,7 (D-002); versiones del contrato (D-006).

## 1. ¿Se encontró algún plano o dato georreferenciado de la red EJECUTADA?

**NO.** No existe en el expediente ni en las ubicaciones revisadas ningún plano as-built, de replanteo, CAD (DWG/DXF), GIS ni listado de coordenadas de la red de agua o alcantarillado construida por S&G. La matriz de recepción TL-GES-004 lo marca FALTA (2.1, 2.2, 2.3, 2.7).

Lo único georreferenciado que existe es **de otro tipo y no sirve como evidencia de obra**:

| Qué | Dónde | Qué es | Sirve para el contraste como |
|---|---|---|---|
| Tabla de 202 buzones con Este-X, Norte-Y, cota de tapa y fondo (UTM WGS-84/18S) y perfiles por calle | `05 EXPEDIENTE V2\8.00 PLANOS DE REDES.pdf`, pág. 8 y 10-19 (E-036) | **Diseño original** del proyectista (Rev. 03/2025), no obra ejecutada; vínculo con el contrato POR CONFIRMAR | Posible línea base de lo diseñado/contratado, si se confirma que fue entregado a S&G |
| Planos OS-AP/OS-SA 2023 con buzones BZ-400 a BZ-615 (CT, CF, H) y rótulo UTM WGS-84/18S | `Control-company\03 renacimiento del sur sac\planos agua y desague\` (E-043) | **Segundo juego de diseño**, plot 2023-07-11; sin tabla de coordenadas extraída | Otra posible línea base de lo diseñado; vínculo con el contrato POR CONFIRMAR |
| TIN, ortofoto y lotes v3/v4 | `W_contraste/datos/v3_48calles`, `v4_primera_expediente` | Base del terreno y de los lotes; solo la capa de agua trae los reservorios AGUA01/02 | Base geométrica; no contiene la red ejecutada |
| Pre-diseño de desagüe v0.4 | `W_contraste/resultados/v0.4_48calles_pasajes` | Diseño nuevo del contraste | Es el lado 'diseño' del contraste, no el 'ejecutado' |
| Croquis TL-PLA-003 | `A_EXPEDIENTE_HU/.../TL-PLA-003_...png` | Captura de pantalla del mapa web; sin escala ni coordenadas | No prueba tramos construidos |

No se inspeccionó el DWG vivo de Civil 3D (`PTL COMPLETO WGS84 VIS v45.dwg`) en esta tarea; las 11 capas ya exportadas a `datos/v3_48calles` no incluyen red de agua ni de desagüe ejecutada. Tampoco se pudo leer `ia analisis\diseño corte de agua y desague.dwg` (E-044). Pedir al usuario que confirme que ninguno contiene una capa de red ejecutada (B-22).

## 2. Método y estados

Se leyeron completos: Carta 014 y sustento, borrador de no conformidad, resumen interno, contrato (PDF firmado y DOCX editable), ficha del contrato, TL-GES-004 a 010, registros P1/P2, TL-COR-OUT-001 y TL-TEC-001 a 005. Se listaron los directorios B1, B4, B5, B6 y A_EXPEDIENTE_HU y se buscaron DWG/DXF/PDF/imágenes y palabras clave en el expediente, en `05 EXPEDIENTE V2` y en las carpetas de documentos del Escritorio. Cada hecho cita archivo y ubicación (línea para .md, página para PDF, cláusula para contrato). También se listó por completo `Control-company\03 renacimiento del sur sac` (328 archivos) y se leyeron los PDF de diseño localizados con pypdf. No se estimó ni completó ningún dato.

| Estado | Significado en este inventario |
|---|---|
| CONFIRMADO | Existencia documental, contenido literal de un documento primario, o ausencia comprobada al corte. No es verificación física de obra. |
| ALEGADO POR EL CONTRATISTA | Declaración de S&G (Carta 014 y sustento) sin levantamiento independiente. |
| BORRADOR | Afirmación del informe de no conformidad, sin firma ni envío. No es hallazgo verificado. |
| POR CONFIRMAR | Relato interno sin respaldo, fuente secundaria, versión contradictoria, diseño original sin vínculo comprobado, o dato que exige verificación física/documental. Lleva fecha 2026-10-13. |

Cada hecho lleva además `tipo_fuente` para que no se confunda un diseño con una obra o un relato con un documento primario.

## 3. Clave de fuentes

| Clave | Documento | Ruta completa | Bytes | SHA-256 |
|---|---|---|---:|---|
| S01 | Carta 014-2026-S&G/EDIFICA y Sustento Técnico (transcripción .md; documento del contratista) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\obra agua y desague\SUSTENTO_TECNICO_contratista.md` | 18731 | `31dc562209f6d7b815eef8e756a7e1ea6f40c3f4ac6000b7defb3235f6fa76b8` |
| S02 | Informe Técnico de No Conformidad 001-2026 (BORRADOR sin firma) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\obra agua y desague\informe_tecnico_deNoConformidad.md` | 9476 | `4215d1a5c73a725387c1ef755163fcbd0c2d51e62f95786d304c14d8608bdf89` |
| S03 | Resumen interno 'Documento maestro: operaciones y saneamiento' (corte 28/08/2026) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\obra agua y desague\resumen de  informacion de renasur.md` | 4318 | `2644402cea9202629ebe3dc07b0eb8bde7182ce0ad3e3049f79ce88177ffe71a` |
| S04 | Contrato 005-2026, PDF 'FIRMADO' (5 páginas) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B1_Gestion\04.04_Contratos\CON-005_SG-Edifica\originales\TL-CON-005_2026-04-08_Contrato_FIRMADO.pdf` | 443232 | `934f79a39cb10474d410db900a116f3677b20de0c7a9aed21ec502fbcca951b5` |
| S05 | Contrato 005-2026, DOCX 'editable' | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B1_Gestion\04.04_Contratos\CON-005_SG-Edifica\originales\TL-CON-005_2026-04-08_Contrato_editable.docx` | 525675 | `1536040a304df973bb0dbff4b9f5f53d0715645091cf7e2a43d9a63a27e3f4d4` |
| S06 | Ficha del contrato TL-CON-005 (resumen interno) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B1_Gestion\04.04_Contratos\CON-005_SG-Edifica\TL-CON-005_2026-10-03_FICHA_Contrato.md` | 2770 | `ba79854cb42adf51386b6f53e53228ef82b0b730c88d2095811cf29e9c5f0c21` |
| S07 | TL-GES-004 Lista de documentos para la recepción de obras | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B1_Gestion\04.01_Plan_Ejecucion\TL-GES-004_2026-10-03_Recepcion_Obras_Seguimiento.md` | 6808 | `ecc155730d1c32a4ec83355a787d50050018902a7fcad9ca6b77e021dad6c834` |
| S08 | TL-GES-005 Registro de problemas de la HU (relato de Rafael, sin respaldo) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B1_Gestion\04.01_Plan_Ejecucion\TL-GES-005_2026-10-04_Registro_Problemas_HU.md` | 16838 | `fe34e254e3c3f68223e0cd271b8cdaf10d44283bd948953a927ecf350eb1ee20` |
| S09 | TL-GES-006 Expediente Maestro (Gemini) SIN VALIDAR | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B1_Gestion\04.01_Plan_Ejecucion\TL-GES-006_2026-10-04_Expediente_Maestro_Gemini_SIN_VALIDAR.md` | 22166 | `f5047c8a85faf6b7c98fdb60b46afc7a80652924e75a10230dcf7f48e47d29ad` |
| S10 | TL-GES-007 Esquema de entrega en dos partes | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B1_Gestion\04.01_Plan_Ejecucion\TL-GES-007_2026-10-04_Esquema_Entrega_Dos_Partes.md` | 4508 | `9ca4e311416fbcb7ec02d5067fe93373d7f15fb4e581e94eb481072628e60f09` |
| S11 | TL-GES-008 Plan de salida y análisis crítico (con 7 actualizaciones) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B1_Gestion\04.01_Plan_Ejecucion\TL-GES-008_2026-10-04_Plan_Salida_Analisis_Critico.md` | 23902 | `c2cb6aac5f3c831f50db734020c836d5a60f15fa38284e6fca08ea4e7754f021` |
| S12 | TL-GES-009 Verificación del borrador de No Conformidad | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B1_Gestion\04.01_Plan_Ejecucion\TL-GES-009_2026-10-04_Verificacion_Informe_No_Conformidad.md` | 6805 | `a0d9c70188290479a84db56f38c66e47cac1a059d38b5e6a05a606941f6a4499` |
| S13 | TL-GES-010 Propuesta de fases y mejoras | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B1_Gestion\04.01_Plan_Ejecucion\TL-GES-010_2026-10-04_Propuesta_Fases_y_Mejoras.md` | 10080 | `eac08e0cc6498a96076d8cd52173eb86c82e8c47c9b7447cd2d9806bc40ef8c4` |
| S14 | LEEME Parte 1 | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\A_EXPEDIENTE_HU\P1_Parte_1\00_LEEME_Parte1.md` | 2488 | `def9c095488b6bb0a1776d0336174332a7dd2a5121bff5123cd4fc2d32b76fff` |
| S15 | LEEME División P1/P2 | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\A_EXPEDIENTE_HU\A0_Comun\4_Division_P1_P2\00_LEEME_Division.md` | 10893 | `63c3a95f8b619f189dccf80d9bc8cb6ae928931666118efad80791773bd6bff5` |
| S16 | TL-COR-OUT-001 Consulta a Valverde (2026-10-04) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B6_Correspondencia\08.04_Enviados_Recibidos\Cartas_Enviadas\TL-COR-OUT-001_2026-10-04_Consulta_Valverde.md` | 10494 | `7ff88246826e1cb8109b747c7b81eb27dc53087cf97cd5dcf44019a9df9696ad` |
| S17 | Memoria descriptiva del diseño original, Rev A 06/03/2025 (PDF, 23 pág.) | `C:\Users\henry\OneDrive\Escritorio\05 EXPEDIENTE V2\1.00 MEMORIA_DESCRIPTIVA.pdf` | 2235548 | `107b6edd12233192031ef985ce96f652818b018a7a280e2ba39b336b5c9cf819` |
| S18 | Planos de redes del diseño original, ELC_11_625_01, 29/03/25 (PDF, 19 pág.) | `C:\Users\henry\OneDrive\Escritorio\05 EXPEDIENTE V2\8.00 PLANOS DE REDES.pdf` | 47894299 | `ca8b71f0ec672933fdbaf0eb59699026b088de415ac2e66a02504763b0af64be` |
| S19 | Plantilla de contrato y TDR 'Etapa 1' (Akallpa SAC como contratista, enero 2025) | `C:\Users\henry\OneDrive\Escritorio\terra lima documentos\z_archivos_doc\  (CONTRATO DE AGUA Y DESAGUE.docx; TDR DE  AGUA Y DESAGUE.docx)` | 16889 | `7653be4206d489b2dbb018a0e8b27f7fbbb8bdf5fc2fb7220e414b3f5189fc6f (contrato); TDR: 16243 B, 817127a3843b2709672b913761dd2644c6ac7fa8d3acafd0450fd870697b9203` |
| S20 | Croquis TL-PLA-003 v3 (PNG, captura del mapa web; sin coordenadas) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\A_EXPEDIENTE_HU\A0_Comun\4_Division_P1_P2\Plano_Delimitacion_P1_P2\TL-PLA-003_2026-10-04_Croquis_v3_BORRADOR.png` | 903303 | `53292fe046afdc42757f0f8a52be22961990b73c452b7452abacbf47429c296a` |
| S21 | Listado de directorios B1/04.02, 04.03, 04.04 (salvo CON-005), 04.05, 04.06; B4; B5; B6 (verificado el 2026-10-13) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\  (carpetas indicadas)` |  |  |
| S22 | W_contraste/supuestos.md y datos/v4_primera_expediente (alcance de lotes) | `...\Agua_y_Alcantarillado\W_contraste\supuestos.md` |  |  |
| S23 | Documento maestro de estrategia gerencial (28/08/2026; generado con IA; carpeta Control-company) | `C:\Users\henry\OneDrive\Escritorio\Control-company\03 renacimiento del sur sac\gemini-code-1788722337705.md` | 3968 | `32a040272b40ffa9d8818ef3bc36635a934119f91d7f8d1473284469ac672c6d` |
| S24 | Hoja de cálculo 'cotizacion de  conexiones.xlsx' (Hoja1 y Hoja2; autor no consta; modificado 2025-12-20) | `C:\Users\henry\OneDrive\Escritorio\cotizacion de  conexiones.xlsx` | 15629 | `88621d26bac036aaf1ab11cda0540250ffe7a9eb5d5f1bc837556a9b481ac63f` |
| S25 | Segundo juego de planos de diseño: carpeta 'planos agua y desague' (20 PDF, plot AutoCAD 2023-07-11; copiados 2025-11-03) | `C:\Users\henry\OneDrive\Escritorio\Control-company\03 renacimiento del sur sac\planos agua y desague` |  | `ver archivos_utiles.md, sección 3 (SHA-256 por archivo)` |
| S26 | DWG/DXF de la carpeta 'ia analisis': 'diseño corte de agua y desague.dwg' (2026-09-30) y 'secciones de calles.dwg/.dxf' (2026-10-08) | `C:\Users\henry\OneDrive\Escritorio\Control-company\03 renacimiento del sur sac\ia analisis` |  | `ver archivos_utiles.md, sección 3` |

Las referencias 'l.' son números de línea del archivo .md en el estado del corte; 'p.' es la página del PDF; 'cl.' es cláusula del contrato; 'P1..P34' son filas del registro TL-GES-005.

## 4. Hechos por categoría

### A. Alcance y condiciones contractuales

| ID | Tema | Valor | Fuente (archivo y ubicación) | Tipo de fuente | Estado | Nota |
|---|---|---|---|---|---|---|
| E-001 | Contrato y objeto | Contrato N.° 005-2026-S&G/EDIFICA, 08/04/2026, entre Renacimiento del Sur S.A.C. (contratante) y Constructora S&G Edifica S.A.C. (contratista), para ejecutar la obra de red de agua potable y alcantarillado en Terra Lima, Pucusana, como parte de la HU N.° 002-2025-SGOPYC-GDU/MDP. El título del PDF firmado NO dice 'Sector I'; el DOCX editable y la ficha sí ('del Sector I'). | S04 p.2 (cl. 2.1) y portada; S05 cl. segunda; S06 tabla, fila 'Obra' | contrato | **CONFIRMADO** | Confirma que el contrato existe y su objeto general; no hay descripción física de la obra. Ver D-006. PARA VALIDAR CON VALVERDE. |
| E-002 | Anexos del contrato | El PDF firmado (5 pág., cláusulas 1 a 10) no contiene lista de anexos; la cl. 3.1 remite a 'planos de detalle' que no se adjuntan. El DOCX (cl. décima 10.1) y la ficha declaran Anexo A (A-1 memoria y cálculo, A-2 especificaciones, A-3 planos de ejecución con perfiles, buzones y conexiones, A-4 cronograma) y Anexo B (B-1 metrados, B-2 ACU, B-3 presupuesto, B-4 fórmula polinómica). Ninguno está archivado en el expediente. | S04 p.3 (cl. 3.1); S05 cl. décima 10.1-10.2; S06 secciones 'Anexos que el contrato declara' y 'Pendiente'; S16 sección 3, fila 'Saneamiento' | contrato / ficha | **CONFIRMADO** | Confirmada la AUSENCIA en el expediente (no la inexistencia fuera de él). Sin A-2 y A-3 no se sabe qué diámetro, clase y profundidad se contrataron. |
| E-013 | Monto, modalidad y anticipo | S/ 1,481,950.00; suma alzada; partida única 01.01 'Ejecución - Saneamiento', unidad GLB, metrado 277.00 x S/ 5,350.00. Anticipo 20% = S/ 296,390.00 'a la firma'. No hay metrados por diámetro ni por partida. El contrato no precisa si incluye IGV (ficha). | S04 p.3 (cl. 3.2, tabla) y p.4 (cl. 5.1); S06 | contrato | **CONFIRMADO** | Es lo que dice el contrato. El significado del '277.00' no se interpreta (POR CONFIRMAR, 2026-10-13). El pago efectivo del anticipo: POR CONFIRMAR en Odoo. |
| E-014 | Plazo y fechas de ejecución | PDF firmado: 'será de 60 días hábiles', sin fecha de inicio ni de término. DOCX: 60 días calendarios, inicio 15/04/2026, término 15/06/2026. Ficha: 60 días calendario y 'fecha de inicio: por confirmar'. Registros internos hablan de plazo vencido. | S04 p.4 (cl. 6.1); S05 cl. segunda y sexta; S06; S08 P11; S16 pregunta 21 | contrato / registros internos | **POR CONFIRMAR** | Contradicción entre versiones del contrato (D-006). PARA VALIDAR CON VALVERDE. Fecha real de inicio y ampliaciones: POR CONFIRMAR (2026-10-13). |
| E-015 | Penalidad, garantía y pruebas como condición contractual | PDF firmado: penalidad por retraso con máximo de 3% del monto (cl. 8.1); no menciona fondo de garantía ni protocolos. DOCX y ficha: 0.5% diario con tope 10% (S/ 148,195.00); fondo de garantía 5% liberado tras recepción conforme y 'protocolos de pruebas hidráulicas aprobados'. | S04 p.4 (cl. 8.1); S05 cl. quinta y octava; S06 | contrato | **POR CONFIRMAR** | Importa técnicamente porque el DOCX condiciona la liberación a protocolos de prueba, que en el PDF firmado no aparecen. Sin opinión legal: PARA VALIDAR CON VALVERDE. |
| E-016 | Supervisor, cuaderno de obra y aprobación de pruebas | Según el DOCX (cl. novena), el Supervisor designado por el contratante firma las valorizaciones y el Cuaderno de Obra con el Residente, verifica el Anexo A-2 y aprueba pruebas hidráulicas y de estanqueidad antes de la conformidad. El PDF firmado solo dice (9.2) que el contratista realiza las pruebas correspondientes. Ningún documento da el nombre del Supervisor. | S05 cl. novena; S04 p.5 (cl. 9.2); S01 I. Antecedentes (alude al 'Ingeniero Supervisor' sin nombre) | contrato (versión DOCX) | **POR CONFIRMAR** | Depende de cuál versión del contrato rige (D-006). |
| E-017 | Firmas del PDF 'firmado' | El texto del PDF trae líneas de firma con los nombres de ambos gerentes y 'Tacna, a los 08 días del mes de abril del año dos mil veintiséis'. Las imágenes incrustadas de las pág. 1 y 5 son logotipos de S&G; no se identificó imagen de firma o sello. No se pudo renderizar el PDF para inspección visual (falta poppler). Metadatos: Word 2016 / iLovePDF, creado 2026-04-08, autor 'Anali Bustinza Huayllapuma'. | S04 p.5 y metadatos | contrato | **POR CONFIRMAR** | Verificación visual de firmas o sellos manuscritos pendiente (2026-10-13). Pedir el original físico o un escaneo a color (B-19). |

### B. Alegado por el contratista (Carta 014)

| ID | Tema | Valor | Fuente (archivo y ubicación) | Tipo de fuente | Estado | Nota |
|---|---|---|---|---|---|---|
| E-003 | Interferencia puntual agua / alcantarillado | S&G declara que durante la ejecución se identificó 'un punto de interferencia entre la red de agua potable y una conexión domiciliaria de alcantarillado sanitario', y en las conclusiones la califica de 'interferencia puntual'. | S01 I. Antecedentes, párr. 1 (l. 80); VI. Conclusiones, viñetas 1 y 4 (l. 151, 154) | carta del contratista | **ALEGADO POR EL CONTRATISTA** | Un solo punto; sin calle, lote, progresiva ni coordenada (E-021). Ver D-003. |
| E-004 | Posición y separación vertical alegadas | S&G declara que, por mediciones en campo, la red de agua potable está aproximadamente 0.30 a 0.45 m POR DEBAJO de la conexión predial de alcantarillado (el agua más profunda que el desagüe). | S01 V. Análisis, párr. 4 (l. 119); VI viñeta 4 (l. 154); 7.1 panel fotográfico (l. 187) | carta del contratista | **ALEGADO POR EL CONTRATISTA** | Sin cotas absolutas ni levantamiento independiente. Ver D-004. |
| E-018 | Mediciones por fotografía (Fig. 9 a 12) | Fig. 9: separación vertical 'superior a 0,25 m'; Fig. 10: 0.27 m aprox.; Fig. 11: 0.30 m aprox.; Fig. 12: 0.28 m aprox. ('medición directa en campo'). Ninguna figura indica 0.45 m. Las fotografías no están en la transcripción .md; el original físico es '01 file color rojo, 15 folios'. | S01 l. 193-196 y l. 24 | carta del contratista | **ALEGADO POR EL CONTRATISTA** | Las fotos originales son una brecha (B-16). Ver D-004. |
| E-019 | Observación de la Supervisión y razón de S&G para mantener el agua por debajo | S&G afirma que el Ingeniero Supervisor observó que el agua no puede ir por debajo de la conexión y pidió un sustento; S&G sustenta mantener el agua por debajo para conservar el recubrimiento de 1.00 m (que atribuye a OS.050 en vía vehicular) y proteger la tubería durante la ejecución de subrasante, subbase, base y carpeta asfáltica. No propone protección adicional (concreto, tubo sin uniones). | S01 I párr. 2-3 (l. 82-84); II (l. 89); V 5.1-5.2 (l. 129-147); VI (l. 156-158); S12 sección 1, fila 5 | carta del contratista | **ALEGADO POR EL CONTRATISTA** | La observación de la Supervisión solo consta por la carta de S&G y por S08 P24 (relato). Las citas de norma de S&G no se verifican aquí (ver T-02). |
| E-020 | Estado de la vía en el punto | S&G escribe que sobre la zona de instalación 'se ejecutará' la estructura vial proyectada y que el análisis debe hacerse contra el 'nivel definitivo de la vía', pero no informa ese nivel ni la rasante. | S01 V (l. 123, 125, 134); VI (l. 156) | carta del contratista | **ALEGADO POR EL CONTRATISTA** | Rasante o nivel definitivo de la vía: dato ausente. El prediseño de contraste usa rasante propia (S-015), no la real. |
| E-007 | Lo que la Carta 014 NO dice sobre el material | La carta y su sustento no mencionan clase ni PN de tubería, diámetro, material, marca o lote ni certificados. | S01 completo (leído el 2026-10-13); S12 sección 2, fila 5 | carta del contratista | **CONFIRMADO** | Ausencia documental en la carta. S&G no ha respondido por escrito el tema PN 7.5 en lo disponible. |
| E-021 | Lo que la Carta 014 NO dice sobre ubicación y medición | La carta no indica calle, manzana, lote, progresiva ni coordenada del punto; fecha ni autor de la medición; cotas absolutas; número total de cruces; diámetro ni profundidad del desagüe o de la conexión; ni si la tubería sanitaria es colector o conexión. | S01 completo (leído el 2026-10-13); S12 sección 1 ('Faltan datos: cuántos cruces son...') | carta del contratista | **CONFIRMADO** | Ausencia documental en la carta. |
| E-022 | Documento de S&G: existencia y metadatos | Carta fechada en Tacna el 21/08/2026, con bloque de firma a nombre de Santos T. Gómez Choquejahua, ingeniero civil, residente de obra, CIP 169119; entrega '01 file color rojo, 15 folios'. En el expediente solo existe la transcripción .md; B6/Cartas_Recibidas está vacía. La plantilla de S&G trae fechas internas 01-01-2024 y 01/08/2024. | S01 l. 5-37, 49-62; S21 (B6 Cartas_Recibidas) | carta del contratista | **CONFIRMADO** | Existencia del documento, no veracidad de su contenido. En lo disponible el 'sustento' no está firmado por un proyectista ni aprobado por la Supervisión. |

### C. Borrador de no conformidad, resumen interno y relatos

| ID | Tema | Valor | Fuente (archivo y ubicación) | Tipo de fuente | Estado | Nota |
|---|---|---|---|---|---|---|
| E-005 | Tubería de agua PN 7.5 | El borrador afirma que 'el contratista se encuentra instalando tuberías de presión nominal PN 7.5 (resistencia de 7.5 bares)'. No da ubicación, longitud, diámetro, tramo, lote ni evidencia. | S02 Hallazgo N.° 01 (l. 21-30); S12 sección 2, filas 4-5; S08 P9 (l. 25) | borrador interno sin firma | **BORRADOR** | S12: no hay fotos del marcado, guías de remisión, certificados ni protocolo. Evidencia del material instalado: POR CONFIRMAR (2026-10-13). Ver D-002. |
| E-006 | Cruce invertido y falta de protección | El borrador afirma que se colocó 'la tubería de desagüe sobre la tubería de agua potable' (cruce invertido) y que falta la protección de concreto. No da número, tipo (colector o conexión), ubicación ni cotas; cita la separación de 0.27 a 0.30 m 'documentada por el contratista'. | S02 Hallazgo N.° 02 (l. 34-50, en especial l. 36 y 48); S12 sección 1 | borrador interno sin firma | **BORRADOR** | Cantidad, tipo, cotas y protección existente: POR CONFIRMAR (2026-10-13). Ver D-003. |
| E-023 | Condición del borrador de no conformidad | El documento está sin firma ('[Tu Nombre / Firma]'), con autor genérico ('Experto Técnico') y fecha 28/08/2026; S12 lo trata como borrador con defectos y S09 lo rotula 'ejemplo'. | S02 l. 1-6 y 64-68; S12 sección 3; S09 nota l. 1 | borrador interno sin firma | **CONFIRMADO** | Confirma que es un borrador sin firma; NO es un hallazgo verificado. Sus citas normativas fueron cotejadas parcialmente en S12 (no en esta tarea). |
| E-024 | Notificación a S&G | Rafael declara que el borrador 'nunca se envió' y que no se ha enviado ninguna carta formal a S&G; la única observación habría sido la de la Supervisión que motivó la Carta 014. | S08 P24 (l. 40); S09 nota l. 1; S12 sección 3, pto 2; S16 sección 3, fila 'Observaciones de obra' (l. 32) | relato de Rafael recogido en registros internos | **POR CONFIRMAR** | Sin cargo de envío ni constancia. Ver D-007. Cualquier acción frente a S&G: PARA VALIDAR CON VALVERDE. |
| E-025 | Resumen interno: problema 'sistemático' de cruces | El resumen del 28/08/2026 afirma 'negligencia constructiva sistemática': desagüe por encima de la matriz sin 0.25 m de separación y, 'en cruces invertidos obligados por topografía', ausencia de encamisado o dado de concreto armado. No identifica ningún cruce. | S03 sección 2 (l. 18-24) | resumen interno sin respaldo | **POR CONFIRMAR** | Contradice la lectura 'interferencia puntual' de S&G (D-003). |
| E-026 | Profundidad de zanja del desagüe (cita aislada) | El resumen indica que el contratista 'no profundizó la zanja de desagüe (1.40m - 1.50m)' para ahorrar maquinaria. Es ambiguo si 1.40-1.50 m es la profundidad ejecutada o una referencia; no dice en qué tramo. | S03 sección 2, 'El Origen del Error' (l. 24) | resumen interno sin respaldo | **POR CONFIRMAR** | Es el único dato numérico de profundidad del desagüe en todos los documentos. Sin medición ni tramo. Ver D-010. |
| E-027 | Estado posterior al informe de agosto | Registro de Rafael del 2026-10-04: 'S&G no corrigió casi nada: sigue con tubería PN 7.5 y cruces invertidos sin protección'. | S08 P23 (l. 39); S11 tercera actualización (l. 175) | relato de Rafael recogido en registros internos | **POR CONFIRMAR** | Sin verificación en obra. |
| E-028 | Dirección de los colectores construidos | Se indica que los colectores construidos por S&G 'ya apuntan al lote de la PTAR' (punto más bajo, donde el plano aprobado perdido definía el predio PTAR); la PTAR no está construida. | S11 quinta actualización (l. 212); S15 (opción D, l. 46); S16 sección 3, fila 'Desagüe' | relato de Rafael recogido en registros internos | **POR CONFIRMAR** | Único dato cualitativo de trazado del desagüe ejecutado. Sin plano. |
| E-029 | Extensión de lotes alcanzados por la obra | Registros internos mencionan 'los ~250 lotes con obra de saneamiento' (manzanas vendidas ~95%), 'los 250 lotes iniciales sin punto de descarga' y una Parte 1 de 768 lotes (versión anterior). El polígono oficial de la Parte 1 no existe (el croquis TL-PLA-003 es una captura sin coordenadas). | S13 sección 3, fila 1A (l. 17); S14 (l. 10); S08 P28 (l. 44); S20 (imagen) | relato de Rafael recogido en registros internos | **POR CONFIRMAR** | Ver D-005. |
| E-009 | Zona ejecutada: solo Parte 1 o a caballo entre partes | S08 dice 'abarca solo la Parte 1' (P34, 'Resuelto'); S15 trae las dos versiones en el mismo archivo ('queda a caballo entre ambas partes' y más abajo 'abarca solo la Parte 1'); S16 dice 'solo una zona'. | S08 P34 (l. 49); S15 (l. 82 y l. 88); S16 (l. 26) | relato de Rafael recogido en registros internos | **POR CONFIRMAR** | Sin plano de lo construido. Ver D-005. |
| E-012 | PTAR y punto de descarga | PTAR 'no construida ni con expediente'; los 250 lotes iniciales no tienen punto de descarga. SEDAPAL llegaría con un buzón a ~50 m de la PTAR, solo en proyecto. | S08 P6 y P31 (l. 22, 50); S11 tercera actualización (l. 175); S14 (l. 10) | relato de Rafael recogido en registros internos | **POR CONFIRMAR** | Sin inspección física ni expediente de PTAR. |

### D. Avance y estado contractual

| ID | Tema | Valor | Fuente (archivo y ubicación) | Tipo de fuente | Estado | Nota |
|---|---|---|---|---|---|---|
| E-008 | Avance físico y valorizado ~90% | Rafael aclara el 2026-10-04 que S&G lleva ~90% de avance físico y ~90% valorizado (no se aporta valorización, acta ni fecha de corte del 90%). | S11 actualizaciones 1 y 2 (l. 111, 129, 147); S08 P18 (l. 34); S14 (l. 9); S16 (l. 26) | relato de Rafael recogido en registros internos | **POR CONFIRMAR** | Contradice E-030. Requiere valorizaciones, pagos y metrados reales (B-08). Ver D-001. |
| E-030 | Avance 23.86% (dato anterior) | El documento TL-GES-006 (Gemini, sin validar) reporta S&G con avance 23.86%, valorizado S/ 353,587.09, saldo retenible S/ 1,128,362.91 y fondo de garantía S/ 17,679.36; S11 (sección 1) y S08 P11 repiten '23.86%'. S08 P18 y S11 lo declaran 'desactualizado'. | S09 (l. 85); S11 sección 1 (l. 13); S08 P11 (l. 27) y 'Datos nuevos' (l. 54); S08 P18 (l. 34) | documento sin validar (IA) y registros internos | **POR CONFIRMAR** | Origen del 23.86% desconocido (se dice 'cifras de Odoo' sin exportación). Ver D-001. |
| E-031 | Valorizaciones y cronograma en el expediente | B1/04.05_Valorizaciones (con Cuadro_Avance_Acumulado y Valorizacion_Mensual_01), 04.02_Cronograma_Maestro, 04.03_Presupuesto_Consolidado y 04.06_Reuniones_Coordinacion no tienen archivos (0 archivos). No hay valorizaciones, actas, comprobantes de pago ni cronograma de S&G. Odoo no fue consultado en esta tarea. | S21 (listado de directorios 2026-10-13); S07 fila 4.5 | verificación de directorios | **CONFIRMADO** | Ausencia de archivos en el expediente al 2026-10-13. |

### E. Ausencias de evidencia comprobadas

| ID | Tema | Valor | Fuente (archivo y ubicación) | Tipo de fuente | Estado | Nota |
|---|---|---|---|---|---|---|
| E-010 | As-built, replanteo y CAD/GIS de la red ejecutada | No se encontró plano as-built de agua, de alcantarillado ni archivo CAD/GIS UTM de la red ejecutada. La matriz de recepción marca FALTA: 2.1 plano de trazado replanteado, 2.2 as-built de agua, 2.3 as-built de alcantarillado, 2.7 CAD/GIS UTM WGS84 18S. Búsqueda del 2026-10-13: 0 archivos DWG en todo exp.-terraLima_v2 y 0 DWG/DXF en '05 EXPEDIENTE V2'; los únicos DXF de exp.-terraLima_v2 son pre-diseño de W_contraste. En Control-company/03 renacimiento del sur sac hay DWG de lotización, topografía y un 'diseño corte de agua y desague.dwg' cuyo contenido no se pudo leer (E-044); ninguno está identificado como red ejecutada. | S07 sección 2 (l. 20-29); búsqueda de archivos 2026-10-13 (ver archivos_utiles.md); S26 | ausencia verificada | **CONFIRMADO** | Ausencia en las ubicaciones revisadas; no se revisaron discos externos, correo, WhatsApp, Odoo ni el DWG vivo de Civil 3D más allá de las 11 capas ya exportadas. |
| E-011 | Pruebas, certificados y calidad | No existen protocolos de prueba hidráulica (3.1), de estanqueidad (3.2), certificados de calidad de tuberías y accesorios (3.3), ensayos de compactación (3.4), rotura de probetas (3.5) ni cuaderno de obra firmado (3.10); el registro fotográfico solo tiene 2 fotos de BMs (3.8, parcial). | S07 sección 3 (l. 31-43) | ausencia verificada | **CONFIRMADO** | Sin estos documentos el PN, el material y la hermeticidad no se pueden verificar. |
| E-032 | Cuaderno de obra, informes de supervisión y certificados | B4_Supervision_y_Calidad contiene un solo archivo (TL-SUP-001, registro diario de Renacimiento del Sur con 2 entradas del 20/02/2026 sobre preparativos de licitación). Cuaderno_Obra_Digital, Informes_Mensuales/Especiales, Certificados_Calidad_Materiales y No_Conformidades están vacíos. | S21 (listado de directorios 2026-10-13); archivo TL-SUP-001 | verificación de directorios | **CONFIRMADO** | Ausencia al 2026-10-13. |
| E-042 | Carpetas contractuales vacías | B1/04.04_Contratos: Addendas_Modificaciones, Bases_TdR, Contratos_Firmados, Plan_Contrataciones y Propuestas_Ofertas no tienen archivos (0 archivos fuera de CON-005). No está la oferta técnica y económica de S&G que el contrato (cl. 3.2) toma como referencia del presupuesto, ni adendas, ni actas. | S21 (listado de directorios 2026-10-13); S04 p.3 (cl. 3.2); S05 cl. tercera | verificación de directorios | **CONFIRMADO** | Ausencia en el expediente al 2026-10-13 (B-21). |

### F. Diseño original localizado (NO es lo ejecutado)

| ID | Tema | Valor | Fuente (archivo y ubicación) | Tipo de fuente | Estado | Nota |
|---|---|---|---|---|---|---|
| E-033 | Existencia de un diseño original de agua y alcantarillado (fuera del expediente) | La carpeta '05 EXPEDIENTE V2' (en el Escritorio, fuera de exp.-terraLima_v2) contiene memorias y planos del 'Sistema de abastecimiento de agua potable y alcantarillado para la urbanización Renacimiento del Sur': Memoria descriptiva Rev A 06/03/2025 (diseñado por LBLC = Lenin Beker L.C.; revisado por JFS = Jese Fretel S.; consultor Akallpa Ingenieros; 'Aprobado por' = '---') y 'Planos de redes' código ELC_11_625_01, creación 29/03/25, unidad ejecutora Akallpa S.A.C. | S17 p.1; S18 p.1 | diseño original (no ejecutado) | **POR CONFIRMAR** | Contenido leído y confirmado en los PDF; su vínculo con el Anexo A del contrato 005-2026, con lo entregado a S&G y con lo ejecutado es POR CONFIRMAR (2026-10-13). Es DISEÑO, no obra. |
| E-034 | Alcance y diámetros del diseño original | Desagüe: 1,342 lotes con conexión; 8,815.06 m en total (Ø 8" = 8,630.56 m; Ø 10" = 165.05 m; Ø 12" = 19.45 m), tubería PVC-UF NTP ISO 4435, DN 200/250/315 mm; 202 buzones proyectados de D = 1.20 m. Agua: PVC clase C-10 en Ø 3", 4", 6", 8" y 10"; plano: 8" = 184.51 m, 6" = 651.79 m, 4" = 584.92 m, 3" = 7,189.56 m (total distribución 8,610.78 m) más aducción Ø 10" = 93.69 m; 79 válvulas de control, 25 de aire y 16 de purga. Memoria: 8.74 km de desagüe y 8.77 km de agua. | S17 p.16-18 y 20; S18 p.4 y p.7/9 (cuadros resumen) | diseño original (no ejecutado) | **POR CONFIRMAR** | Referencia de lo que se diseñó, no de lo construido. Cifras internamente discrepantes: D-008. |
| E-035 | Buzones: tres cifras en el diseño original | Memoria: encabezado de partida 'Construcción de buzones (63 und)' (p.22) y tabla de metas con 60 + 80 + 40 + 30 = 210 buzones por rango de altura (p.20); planos: 'total de buzones proyectados 202 und' (p.7 y 9) y tabla con 202 filas (p.8). | S17 p.20 y p.22; S18 p.7, p.8 y p.9 | diseño original (no ejecutado) | **POR CONFIRMAR** | Ver D-008. Número de buzones ejecutados: sin dato. |
| E-036 | Dato georreferenciado de DISEÑO: tabla de buzones y perfiles | Los planos traen (p.8) 'Tabla de buzones, UTM-WGS 1984 datum' con 202 filas (BZ-1 a BZ-202): diámetro 1.20 m, cota de tapa, cota de fondo, altura (1.10 a 4.90 m) y coordenadas Este-X / Norte-Y; y (p.10-19) perfiles longitudinales por calle con BZ/CT/CF/H, DN, longitud y pendiente por tramo. El rótulo dice 'Sistema de coordenadas UTM WGS-84/18S'. Los PDF tienen medida rectilínea (no hay georreferencia geoespacial embebida). | S18 p.8, p.10-19 y rótulos | diseño original (no ejecutado) | **POR CONFIRMAR** | Es georreferenciación de DISEÑO. NO existe dato georreferenciado de la red EJECUTADA. Los valores no se superpusieron ni validaron contra datos v3/v4 en esta tarea. |
| E-037 | Especificación de tubería de agua dentro del diseño original | Memoria: 'tuberías de PVC CLASE 10' (p.18) y partidas 'PVC SP NTP 399.002 C-10'. Planos (cuadro de normas, p.4-6): HDPE PE 100 PN8 SDR 26 NTP ISO 4427 y, para DN >= 63 mm, NTP ISO 1452/4422; para DN < 63 mm NTP 399.002; y un texto 'clase y/o tipo ... presión de trabajo de 6, 7 bar o clase 6, 7' para diámetros 'desde 3/4" hasta 1/2"'. | S17 p.18-19; S18 p.4-6 (cuadros 'Normas técnicas vigentes' y 'Especificaciones técnicas') | diseño original (no ejecutado) | **POR CONFIRMAR** | El diseño original no es unívoco sobre la clase; no se infiere equivalencia con PN 7.5. Ver D-002 y D-008. |
| E-038 | Zanja típica de agua en el plano original | Detalle 'zanja típico' (plano de red de agua, p.4): 'H = 0.80 m - 1.00 m'; relleno compactado en capas de 15 cm con material de la excavación y de 10 cm con material seleccionado; cotas del detalle 0.60, 0.10, DN/2 y h = 0.20. | S18 p.4 (detalle de zanja típico) | diseño original (no ejecutado) | **POR CONFIRMAR** | La lectura de 'H' (profundidad total, relleno o recubrimiento) no está establecida; no se compara con el 1.00 m de OS.050. |
| E-039 | Fuente de agua, monto y plazo del diseño original | Derivación de la línea de conducción del proyecto PROVISUR (agua desalinizada de la planta de Santa María) con cámara de derivación y medición; 2 reservorios apoyados de 400 m3; presupuesto S/ 11,938,317.80 con IGV y plazo 354 días calendario para toda la urbanización. | S17 p.14-15, 21 y 23 | diseño original (no ejecutado) | **POR CONFIRMAR** | Difiere del esquema S-006 (Asociación Santa María). Monto y plazo difieren de los del contrato S&G (D-009). |
| E-040 | Plantilla de contrato y TDR 'Etapa 1' (Akallpa SAC) | En terra lima documentos/z_archivos_doc hay una plantilla 'Contrato de ejecución de obra a suma alzada' con contratista Akallpa SAC (campos en blanco, enero 2025, plazo 140 días, valorizaciones quincenales, pago condicionado a protocolo de prueba hidráulica) y un TDR 'Agua y alcantarillado - Etapa 1' que exige como dossier de calidad: as-built firmados, certificados de tuberías, protocolos de prueba hidráulica y de compactación. | S19 (contrato cl. cuarta y quinta; TDR secciones 7 y 9) | plantilla / TDR sin firma | **POR CONFIRMAR** | No es el contrato con S&G. S07 (lectura crítica 2) indica que los ítems 3.3 a 3.10 de recepción vienen de un TDR plantilla y solo son exigibles si el Anexo A-2 o una adenda los incluye. |
| E-041 | Cotización previa con clase C-7.5 y alcance menor (autor no consta) | El archivo 'cotizacion de  conexiones.xlsx' (Escritorio; modificado 2025-12-20; sin autor) tiene dos hojas. Hoja1, 'total presupuesto ofertado S/ 1,222,037.50': red matriz de agua 1,350 ml con 'tubería PVC ISO 1452 (inc. anillos)', alcantarillado 1,350 ml PVC UF ISO 4435 200 mm, 34 buzones de concreto (H promedio 2.00 m) y 225 conexiones domiciliarias de agua y de desagüe. Hoja2, 'total general S/ 1,681,866.04': agua 'Tubería PVC-U ISO 1452 C-7.5 DN 110 mm' (partida 02.02.01, 1,450 ml), alcantarillado 'PVC-U UF ISO 4435 DN 200 mm (S-25)', 34 buzones 'estimado' y conexiones para 225 lotes (partidas con 242 und). | S24 Hoja1 (partidas 02.03, 03.03, 03.04, 04.01-04.02 y total) y Hoja2 (partidas 02.02.01, 03.02.01, 03.03, 04.00 y total) | hoja de cálculo sin autor | **POR CONFIRMAR** | No se sabe quién la elaboró (podría ser una oferta, una estimación interna o la de otro postor); ninguno de los dos totales coincide con S/ 1,481,950.00. NO se afirma que sea la oferta de S&G. Si lo fuera, la clase C-7.5 aparecería en el presupuesto de la oferta (relevante para D-002). Ver D-005 y D-012. |
| E-043 | Segundo juego de planos de diseño (2023): carpeta 'planos agua y desague' | En Control-company/03 renacimiento del sur sac/planos agua y desague hay 20 PDF de AutoCAD 2023 (fecha de plot en metadatos: 2023-07-11; archivos fechados 2025-11-03): OS-AP-01 y 02 (red de agua), OS-SA-01 y 02 (alcantarillado general), láminas OS-SA-07 a 11 y 13 a 17 (por zonas, con buzones) y MC-01 a 03 (muro y cortes del reservorio). Título: 'Construcción del sistema de abastecimiento de agua potable y alcantarillado para la urbanización Renacimiento del Sur'; rótulo 'Lenin B. Lorenzo C. Ingeniería & Construcción'; UTM WGS-84/18S; escala 1/1250. Agua: 'tuberías PVC NTP ISO 1452-2' DN 75, 110, 160, 200 y 250 mm (3, 4, 6, 8 y 10 pulgadas), sin clase/PN legible en el texto extraído; 2 reservorios V = 450 m3, NF 156 msnm. Desagüe: PVC-UF DN 200, 250 y 315 mm (8, 10 y 12 pulgadas), tramos rotulados 'DN 200 SN2'; buzones BZ con CT, CF y H (216 numerados entre BZ-400 y BZ-615 legibles). Faltan en la carpeta las láminas OS-SA-03 a 06 y 12 (el nombre del archivo dice 'OS_SA-03 al 17'). | S25 (metadatos y texto de los 20 PDF; hojas OS-AP-01, OS-SA-01, OS-SA-07 a 17) | diseño original (no ejecutado) | **POR CONFIRMAR** | Es un segundo juego de DISEÑO distinto del de 2025 (E-033 a E-039): otro rotulista, otros DN (75-250 vs 3-10 pulgadas con C-10), reservorios 450 vs 400 m3, numeración BZ-400..615 vs BZ-1..202. Cuál fue el entregado/aprobado/contratado: POR CONFIRMAR. Ver D-013. El texto lleva coordenadas de grilla y cotas de buzón (georreferenciación de DISEÑO). |
| E-044 | DWG 'diseño corte de agua y desague' y 'secciones de calles' | En Control-company/03 renacimiento del sur sac/ia analisis existen 'diseño corte de agua y desague.dwg' (837,194 B, 2026-09-30) y 'secciones de calles.dwg/.dxf' (2026-10-08). El DXF de secciones contiene solo capas 0, Defpoints, texto, Area verde, G-ACHURADO, ETAPA 01 y A. ZONAS DE VOLTEO, sin texto de agua ni desagüe. El DWG 'corte de agua y desague' es binario (AC1032) y su contenido no pudo leerse sin herramienta CAD. | S26 (inspección de cadenas de texto y capas el 2026-10-13) | archivo CAD sin inspeccionar | **POR CONFIRMAR** | Qué contiene, quién lo elaboró y si es diseño o relevamiento: POR CONFIRMAR (B-22). No se abrió Civil 3D (solo lectura y fuera de esta ficha). |

Conteo por categoría y estado:

| Categoría | CONFIRMADO | ALEGADO POR EL CONTRATISTA | BORRADOR | POR CONFIRMAR |
|---|---:|---:|---:|---:|
| A. Alcance y condiciones contractuales | 3 | 0 | 0 | 4 |
| B. Alegado por el contratista (Carta 014) | 3 | 5 | 0 | 0 |
| C. Borrador de no conformidad, resumen interno y relatos | 1 | 0 | 2 | 8 |
| D. Avance y estado contractual | 1 | 0 | 0 | 2 |
| E. Ausencias de evidencia comprobadas | 4 | 0 | 0 | 0 |
| F. Diseño original localizado (NO es lo ejecutado) | 0 | 0 | 0 | 11 |
| **Total** | **12** | **5** | **2** | **25** |

## 5. Qué dice cada fuente sobre cada campo técnico

Los campos que pide la ficha, cruzados con las fuentes. 'no consta' significa que el documento no contiene el dato. Ninguna celda es una conclusión.

| Campo | Contrato | Carta 014 (S&G) | Borrador no conformidad | Resumen interno | Registros internos (GES) | Diseño original (NO ejecutado) |
|---|---|---|---|---|---|---|
| Alcance físico ejecutado (tramos, longitud, calles) | sin descripción física; planos A-3 ausentes (E-002) | no consta | no consta | 'solo una zona' (E-009) | ~250 lotes; Parte 1 vs a caballo (E-029, E-009) | 8,815.06 m desagüe, 8.77 km agua, 1,342 lotes (E-034) |
| Diámetro agua | no consta (A-2 y A-3 ausentes) | no consta | no consta | no consta | no consta | 3", 4", 6", 8", 10" (E-034) |
| Material agua | no consta | no consta | no indica material instalado (cita NTP-ISO 1452 como exigencia) | exige NTP-ISO 1452 (PN 10) | no consta | PVC C-10 (memoria); HDPE PE100 PN8 y PVC 'clase 6,7' en leyendas del plano (E-037) |
| Clase / PN agua instalada | no consta | silencio (E-007) | PN 7.5, sin evidencia (E-005) | exige PN 10; no afirma lo instalado | 'tubería PN 7.5' (E-027); sin respaldo documental (S08 P9) | C-10 (memoria); ver E-037 |
| Diámetro / material / clase desagüe | no consta | no consta | no consta | no consta | no consta | PVC-UF NTP ISO 4435, DN 200/250/315 mm (E-034) |
| Profundidad de zanja | no consta | no informa profundidad | no consta | desagüe '(1.40m - 1.50m)', ambiguo (E-026) | no consta | agua: 'H = 0.80-1.00 m' típico (E-038); buzones 1.10 a 4.90 m de altura (E-036) |
| Recubrimiento sobre clave | no consta | cita 1.00 m como requisito; no mide el real (E-019) | cita 1.00 m como requisito | cita 1.00 m como requisito | no consta | no consta |
| Separación vertical en el cruce | no consta | 0.30-0.45 m (texto); 0.27, 0.30 y 0.28 m (figuras) (E-004, E-018) | cita 0.27-0.30 m | afirma < 0.25 m sin dato | no consta | no consta |
| Número y tipo de cruces | no consta | 1 punto, agua bajo conexión predial (E-003) | no cuantifica; 'red de alcantarillado' sobre agua (E-006) | 'sistemático' (E-025) | S12: faltan cantidad y tipo | no consta |
| Protección en cruces (dado/encamisado) | no consta | no propone (E-019) | afirma ausencia (E-006) | afirma omisión (E-025) | 'sin protección' (E-027) | no consta |
| Buzones (número, tipo) | no consta | no consta | no consta | no consta | no consta número ejecutado | 63 / 210 / 202 (E-035) |
| Avance físico | n/a | obra 'en ejecución' al 21/08/2026 (E-003) | no consta | no consta | ~90% (E-008) vs 23.86% (E-030) | n/a |
| Avance valorizado | S/ 1,481,950.00 total (E-013) | no consta | no consta | no consta | ~90% (E-008) vs S/ 353,587.09 (E-030) | n/a |
| Estado contractual | plazo 60 días (hábiles o calendario según versión); sin inicio en el PDF (E-014) | responde a observación de la Supervisión (E-019) | sin firma, no enviado (E-023, E-024) | ordena retención y anotación en cuaderno; cumplimiento no consta | plazo vencido; sin carta formal (E-014, E-024) | n/a |

## 6. Discrepancias entre fuentes (listadas, NO resueltas)

### D-001 — Avance de S&G: 23.86% vs ~90%

- ~90% físico y ~90% valorizado (Rafael, 2026-10-04): S11 l. 111, 147; S08 P18
- 23.86% de avance y S/ 353,587.09 valorizado, fondo de garantía S/ 17,679.36: S09 l. 85; repetido en S11 l. 13 y S08 P11 l. 27
- S08 se contradice a sí mismo: P11 dice 'hoy 23.86%' y P18 dice que ese dato está desactualizado
- **Por qué importa para el contraste:** Define cuánta red existe y, por tanto, cuánto hay que contrastar. Hechos: E-008, E-030, E-031.
- **Cómo se resolvería (no se resuelve aquí):** No adoptar ninguna cifra. Exportar valorizaciones, aprobaciones del Supervisor y pagos desde Odoo (B-08) y cotejar con inspección física.

### D-002 — Clase de tubería de agua: PN 7.5 vs PN 10 (y PN 8 / clase 6,7 en el diseño original)

- Instalada PN 7.5: borrador S02 l. 23 y relato S08 P9/P23 (sin evidencia del material)
- Exigible PN 10: S02 l. 28 (cita textual de SEDAPAL que S12 no halló en CTPS-PR-02), S03 l. 30, S09 l. 22-25
- Diseño original: PVC C-10 (S17 p.18); HDPE PE100 PN8 y PVC 'clase 6,7' en leyendas del plano (S18 p.4-6)
- Contrato firmado: sin especificación; A-2 ausente
- Carta 014: no menciona clase (E-007)
- Documentos generados con IA (S09 l. 59; S23 sección 2) afirman que la Memoria y los Planos del Expediente Técnico 'exigen PN 10'; la memoria y los planos hallados dicen C-10 / PE100 PN8 / clase 6,7 y el Anexo A-2 sigue ausente
- Hoja de cálculo previa sin autor (S24 Hoja2, partida 02.02.01): 'PVC-U ISO 1452 C-7.5 DN 110 mm' para la red matriz de agua (E-041)
- **Por qué importa para el contraste:** Es el hallazgo 1 del borrador. Sin marcado ni certificados no se sabe ni lo instalado ni lo contratado. Hechos: E-005, E-007, E-027, E-037, E-041.
- **Cómo se resolvería (no se resuelve aquí):** Obtener A-2, fotos de marcado, guías, certificados y protocolos (B-04, B-05, B-06). No resolver aquí. Criterio normativo: T-02 / principal. PARA VALIDAR CON VALVERDE.

### D-003 — Naturaleza y cantidad de los cruces

- S&G: UN punto; agua 0.30-0.45 m bajo una 'conexión domiciliaria / predial' (S01 l. 80, 154)
- Borrador: la 'tubería de desagüe' / 'red de alcantarillado' está sobre el agua (S02 l. 36)
- Resumen interno: 'sistemático', 'cruces invertidos' (S03 l. 18-24)
- S12: 'faltan datos: cuántos cruces son, y si son colectores o conexiones prediales'
- **Por qué importa para el contraste:** La regla aplicable y el remedio dependen de si es colector o conexión y de cuántos cruces hay. Hechos: E-003, E-006, E-025.
- **Cómo se resolvería (no se resuelve aquí):** Inventario físico de cada cruce con coordenada, cotas, fotos y protección (B-03). No resolver aquí.

### D-004 — Separación vertical medida en el punto de la Carta 014

- Texto: 'aproximadamente 0.30 a 0.45 m' (S01 l. 119, 154, 187)
- Figuras: 0.27 m, 0.30 m, 0.28 m y 'superior a 0.25 m' (S01 l. 193-196)
- El borrador cita 'de 0.27 m a 0.30 m' (S02 l. 48)
- **Por qué importa para el contraste:** 0.27 y 0.28 m están por debajo del límite inferior del rango del texto (0.30) y ninguna figura documenta 0.45 m. Hechos: E-004, E-018.
- **Cómo se resolvería (no se resuelve aquí):** Pedir las fotos originales y la memoria de medición con instrumento, fecha y autor (B-14, B-16).

### D-005 — Extensión de lo ejecutado

- Solo Parte 1: S08 P34; S15 l. 88
- A caballo entre Parte 1 y 2: S15 l. 82 (mismo archivo)
- ~250 lotes con obra: S13 l. 17; S14 l. 10
- Parte 1 = 768 lotes (versión anterior): S08 P28 l. 44
- Primera Expediente = 444 lotes dentro del límite 00_primera_expediente (S-001), definido por el usuario para este expediente, no por la obra de S&G
- Diseño original: 1,342 lotes (S18 p.4, 7 y 9)
- Cotización previa sin autor: 225 conexiones domiciliarias y 1,350-1,450 ml de red (S24); es solo una coincidencia de orden de magnitud con los ~250 lotes, sin vínculo documental
- **Por qué importa para el contraste:** Sin el polígono de lo construido no se puede decidir qué parte del diseño nuevo se contrasta. Hechos: E-009, E-029.
- **Cómo se resolvería (no se resuelve aquí):** Plano de tramos ejecutados y polígono oficial de la Parte 1 (B-09). No resolver aquí.

### D-006 — Versiones del contrato 005-2026 (PDF 'firmado' vs DOCX 'editable' vs ficha)

- Título: PDF 'Alcantarillado en Terra Lima' (sin Sector I) vs DOCX/ficha 'del Sector I'
- Plazo: PDF 60 días hábiles, sin fechas vs DOCX 60 calendarios con inicio 15/04/2026 y término 15/06/2026 vs ficha 'inicio por confirmar'
- Penalidad: PDF tope 3% vs DOCX/ficha 0.5% diario con tope 10%
- Anexos A/B, Supervisor, anticipo y amortización, fondo de garantía y protocolos: solo en DOCX/ficha; no en el PDF
- Lugar de firma: PDF Tacna vs DOCX/ficha Lima; oficina registral de la partida: PDF Tacna vs DOCX Lima
- La ficha dice resumir el contrato firmado pero reproduce el texto del DOCX
- **Por qué importa para el contraste:** Define qué documentos de calidad, pruebas y anexos son contractualmente exigibles. Hechos: E-001, E-002, E-014, E-015, E-016, E-017.
- **Cómo se resolvería (no se resuelve aquí):** Decidir con Valverde cuál es el texto vigente y rubricado. PARA VALIDAR CON VALVERDE. Sin opinión legal aquí.

### D-007 — Estado de la notificación a S&G

- S11 tercera actualización, A.2 (l. 179): 'confirmar si el informe del 28/08 se envió por carta notarial y si hubo respuesta'
- S12 sección 3, pto 2; S08 P24; S16 l. 32: 'nunca se envió' / 'no se ha enviado ninguna carta formal'
- S03 l. 37-38 ordena bloqueo de pagos y anotación de la No Conformidad en el cuaderno; no consta que se hizo y el cuaderno firmado no existe en el expediente (S07 3.10)
- **Por qué importa para el contraste:** Afecta la lectura de la secuencia de hechos (carta de S&G del 21/08 vs borrador del 28/08). Hechos: E-023, E-024.
- **Cómo se resolvería (no se resuelve aquí):** Rafael confirma por escrito; Valverde define cualquier notificación. PARA VALIDAR CON VALVERDE.

### D-008 — Cifras internas del diseño original

- Buzones: 63 (encabezado), 210 (tabla de metas), 202 (planos) (E-035)
- Desagüe: memoria 8.74 km vs planos 8,815.06 m
- Agua: memoria 8.77 km con 3" = 7,252.09 m vs plano 3" = 7,189.56 m y total distribución 8,610.78 m más aducción 93.69 m (S17 p.17-18; S18 p.4)
- Clase de tubería: C-10 vs PE100 PN8 vs clase 6,7 (E-037)
- Fuente de agua: PROVISUR / planta Santa María (S17 p.14) vs Asociación Santa María (S-006)
- **Por qué importa para el contraste:** Si el diseño original se usa como línea base del 'contratado', sus propias discrepancias deben resolverse primero. Hechos: E-034 a E-039.
- **Cómo se resolvería (no se resuelve aquí):** Pedir al proyectista la versión final y los archivos CAD (B-13). No resolver aquí.

### D-009 — Vínculo entre el contrato S&G (Sector I) y el diseño original (toda la urbanización)

- Contrato: S/ 1,481,950.00; 60 días; planos y presupuesto 'del Sector I' (S05 cl. segunda)
- Diseño original: S/ 11,938,317.80 con IGV; 354 días; 1,342 lotes; sin sectorización visible (S17 p.21 y 23; S18)
- No hay evidencia en el expediente de que '05 EXPEDIENTE V2' sea el Anexo A del contrato ni de que lo haya recibido S&G
- **Por qué importa para el contraste:** Determina si el diseño original puede usarse como referencia de lo 'contratado'. Hechos: E-002, E-033, E-040.
- **Cómo se resolvería (no se resuelve aquí):** Confirmar con Beker/Rafael qué se entregó a S&G y qué sectorización aplica (B-13).

### D-010 — Profundidad del desagüe

- Resumen: '(1.40m - 1.50m)', sin tramo y ambiguo (S03 l. 24)
- Carta 014: no informa profundidad del desagüe ni de la conexión
- Diseño original: buzones de 1.10 a 4.90 m de altura según la tabla del plano; no hay profundidad ejecutada
- **Por qué importa para el contraste:** La subsanación que propone el borrador (profundizar el desagüe) depende de esa profundidad. Hecho: E-026.
- **Cómo se resolvería (no se resuelve aquí):** Medición en campo / as-built con cotas de tapa y fondo (B-01, B-02).

### D-011 — Metadatos de la Carta 014 (menor)

- Carta del 21 de agosto de 2026 en Tacna y control de cambios 21/08/2026
- Plantilla de S&G con 'Fecha: 01-01-2024' y 'Elaborado ... Fecha: 01/08/2024' (S01 l. 39, 51)
- **Por qué importa para el contraste:** Solo indica reutilización de plantilla; no altera hechos. Hecho: E-022.
- **Cómo se resolvería (no se resuelve aquí):** Ninguna salvo cotejar con el original físico (B-16).

### D-012 — Magnitud de la obra según cada documento

- Contrato: partida única 'GLB 277.00 x S/ 5,350.00' = S/ 1,481,950.00 (S04 p.3)
- Cotización previa sin autor: ~1.35-1.45 km de red, 34 buzones, 225 conexiones; totales S/ 1,222,037.50 y S/ 1,681,866.04 (S24)
- Diseño original: 8.8 km de desagüe, 202 buzones, 1,342 lotes (S18)
- Registros internos: ~250 lotes con obra (S13, S14)
- **Por qué importa para el contraste:** Cuatro escalas distintas; sin A-3/B-1 no se sabe cuál corresponde al Sector I contratado. Hechos: E-013, E-034, E-041, E-029.
- **Cómo se resolvería (no se resuelve aquí):** Obtener Anexos A-3 y B-1 y la oferta de S&G (B-06, B-21). No resolver aquí.

### D-013 — Dos juegos de planos de diseño distintos (2023 y 2025)

- Juego 2023 (S25): rótulo Lenin B. Lorenzo C. Ingeniería & Construcción; agua PVC NTP ISO 1452-2 DN 75-250 mm; reservorios 2 x 450 m3 (NF 156 msnm); desagüe DN 200 SN2/250/315; buzones BZ-400 a BZ-615 (216 legibles); plot 2023-07-11
- Juego 2025 (S17, S18): código ELC_11_625_01, 29/03/25, Akallpa S.A.C.; agua PVC C-10 Ø 3-10 pulgadas; reservorios 2 x 400 m3; desagüe DN 200/250/315; buzones BZ-1 a BZ-202; memoria Rev A 06/03/2025 sin aprobación
- Ninguno está identificado como el Anexo A-3 del contrato ni como el aprobado por la municipalidad (expediente perdido)
- **Por qué importa para el contraste:** Si hay que comparar lo ejecutado con 'lo contratado', primero hay que saber cuál de los dos juegos (u otro) se entregó a S&G. Hechos: E-033 a E-039, E-043.
- **Cómo se resolvería (no se resuelve aquí):** Confirmar con Beker/Rafael la secuencia de versiones y cuál se entregó a S&G (B-13). No resolver aquí.

Cada discrepancia se registra también como propuesta en `supuestos.md` (sección T-03) para que el principal decida con el usuario.

## 7. Conclusión operativa

La base disponible permite identificar el contrato, lo que alega el contratista, lo que afirma el borrador y lo que se diseñó originalmente, pero **no permite comparar diseño versus ejecutado** en diámetro, material, clase, trazado, profundidad, cruces, buzones, metrados o pruebas. El contraste por tramo queda bloqueado hasta recibir evidencia de obra (brechas B-01 a B-05) o realizar un levantamiento independiente (B-02). Los dos juegos de diseño (E-033 a E-039 y E-043) podrían servir de línea base de lo contratado, pero solo si se confirma su vínculo con el contrato (B-13, B-21, B-22). **PARA VALIDAR CON VALVERDE** antes de usar este inventario en una reclamación, recepción o documento externo.

## 8. Cambios respecto de v1.1

- Se leyó el contrato firmado (PDF, 5 págs.) y se halló que difiere del DOCX y de la ficha (D-006); v1.1 había citado solo la ficha.
- Se añadieron las mediciones por figura de la Carta 014 (0.27/0.30/0.28 m), la profundidad aislada 1.40-1.50 m del resumen y el estado de cuaderno, valorizaciones y carpetas contractuales vacías.
- Se encontraron dos juegos de diseño de agua y alcantarillado fuera del expediente (`05 EXPEDIENTE V2`, 2025; `Control-company/.../planos agua y desague`, 2023) y una hoja de cálculo previa con 'C-7.5' (E-041); se mantienen separados del ejecutado (categoría F).
- Se conservaron los identificadores E-001 a E-012; E-005, E-006, E-007, E-008, E-009, E-010, E-011 y E-012 mantienen su tema, con valores y fuentes ampliados y estados revisados (E-007 sigue CONFIRMADO; el 23.86% pasó a E-030).
- El Markdown y el JSON se generan desde el mismo conjunto de datos (equivalencia exacta de ids, valores, fuentes y estados).
