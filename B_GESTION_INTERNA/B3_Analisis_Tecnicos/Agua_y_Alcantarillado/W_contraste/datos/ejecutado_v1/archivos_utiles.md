# Archivos útiles localizados — solo lectura (v2.0)

**Corte de búsqueda:** 2026-10-13. No se copió, movió ni modificó ningún archivo; solo se listan ruta, tamaño y huella SHA-256 (para que el principal pueda congelarlos en `datos/` si decide usarlos).

## Resultado principal

- **DWG localizados: 0** en todo `exp.-terraLima_v2` y 0 DWG/DXF en `05 EXPEDIENTE V2`. Los únicos DXF de `exp.-terraLima_v2` son pre-diseño de `W_contraste/resultados`. En `Control-company\03 renacimiento del sur sac` hay DWG de lotización/topografía y uno de nombre `diseño corte de agua y desague.dwg` que no se pudo leer (sección 3).
- **As-built de agua y alcantarillado: no localizado.** Ninguna ruta o archivo con nombre as-built, replanteo o 'como ejecutado'.
- **Dato georreferenciado de la red EJECUTADA: ninguno.** Hay una tabla de buzones georreferenciada de DISEÑO (sección 2).
- **Hallazgo fuera de lo previsto en la ficha:** hay **dos juegos de diseño** de agua y alcantarillado fuera del expediente: (1) memorias y planos de 2025 en `C:\Users\henry\OneDrive\Escritorio\05 EXPEDIENTE V2\` (sección 2) y (2) 20 PDF de planos de 2023 en `C:\Users\henry\OneDrive\Escritorio\Control-company\03 renacimiento del sur sac\planos agua y desague\` (sección 3). Ambos son diseño, no obra.

Dónde se buscó: `exp.-terraLima_v2` completo (DWG, DXF, DGN, SHP, KML, GPKG, GeoJSON, PDF, imágenes, XLSX, DOCX); `Escritorio\05 EXPEDIENTE V2`; `Escritorio\terra lima documentos` (sin node_modules), `terra_lima_documentos`, `defensa de licencia`, `archivos rafa`, `analisis propiedades`; `Escritorio\Control-company\03 renacimiento del sur sac` (listado completo de 328 archivos; las demás carpetas de Control-company son de otras empresas/proyectos y solo se revisaron por nombre de archivo DWG/DXF); y palabras clave (S&G, Edifica, PN 7.5, C-7.5, buzón, desagüe, alcantarillado) en DOCX/XLSX/MD/TXT del Escritorio y subcarpetas indicadas. No se revisaron discos externos, correo, WhatsApp ni Odoo.

## 1. Documentos del contrato y del conflicto con S&G

| Tipo y utilidad | Ruta completa | Bytes | SHA-256 |
|---|---|---:|---|
| S04: Contrato 005-2026, PDF 'FIRMADO' (5 páginas) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B1_Gestion\04.04_Contratos\CON-005_SG-Edifica\originales\TL-CON-005_2026-04-08_Contrato_FIRMADO.pdf` | 443232 | `934f79a39cb10474d410db900a116f3677b20de0c7a9aed21ec502fbcca951b5` |
| S05: Contrato 005-2026, DOCX 'editable' | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B1_Gestion\04.04_Contratos\CON-005_SG-Edifica\originales\TL-CON-005_2026-04-08_Contrato_editable.docx` | 525675 | `1536040a304df973bb0dbff4b9f5f53d0715645091cf7e2a43d9a63a27e3f4d4` |
| S06: Ficha del contrato TL-CON-005 (resumen interno) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B1_Gestion\04.04_Contratos\CON-005_SG-Edifica\TL-CON-005_2026-10-03_FICHA_Contrato.md` | 2770 | `ba79854cb42adf51386b6f53e53228ef82b0b730c88d2095811cf29e9c5f0c21` |
| S01: Carta 014-2026-S&G/EDIFICA y Sustento Técnico (transcripción .md; documento del contratista) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\obra agua y desague\SUSTENTO_TECNICO_contratista.md` | 18731 | `31dc562209f6d7b815eef8e756a7e1ea6f40c3f4ac6000b7defb3235f6fa76b8` |
| S02: Informe Técnico de No Conformidad 001-2026 (BORRADOR sin firma) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\obra agua y desague\informe_tecnico_deNoConformidad.md` | 9476 | `4215d1a5c73a725387c1ef755163fcbd0c2d51e62f95786d304c14d8608bdf89` |
| S03: Resumen interno 'Documento maestro: operaciones y saneamiento' (corte 28/08/2026) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\obra agua y desague\resumen de  informacion de renasur.md` | 4318 | `2644402cea9202629ebe3dc07b0eb8bde7182ce0ad3e3049f79ce88177ffe71a` |
| S23: Documento maestro de estrategia gerencial (28/08/2026; generado con IA; carpeta Control-company) | `C:\Users\henry\OneDrive\Escritorio\Control-company\03 renacimiento del sur sac\gemini-code-1788722337705.md` | 3968 | `32a040272b40ffa9d8818ef3bc36635a934119f91d7f8d1473284469ac672c6d` |

Otros documentos del conflicto (texto .md; ruta, tamaño y SHA-256 en `inventario_ejecutado.md`, sección 3): `TL-GES-004` a `TL-GES-010` en `...\B1_Gestion\04.01_Plan_Ejecucion\`; `TL-COR-OUT-001` en `...\B6_Correspondencia\08.04_Enviados_Recibidos\Cartas_Enviadas\`; `00_LEEME_Parte1.md` y `00_LEEME_Division.md` en `A_EXPEDIENTE_HU`.

Copias del contrato en otras carpetas (mismo tamaño que S04; hash no cotejado): `...\B6_Correspondencia\...\TL-COR-OUT-001_anexos\Anexo2_Contrato_005-2026_FIRMADO.pdf` (443,232 B) y borradores de texto en `...\_archivo_temporal\contrato_*.txt`.

## 2. Diseño original de agua y alcantarillado — `05 EXPEDIENTE V2` (NO es lo ejecutado)

Carpeta: `C:\Users\henry\OneDrive\Escritorio\05 EXPEDIENTE V2\`. Vínculo con el contrato y con lo ejecutado: **POR CONFIRMAR** (B-13). Texto extraído con pypdf; los planos son PDF vectoriales de 19 láminas (medida rectilínea, sin georreferencia geoespacial embebida).

| Contenido | Archivo | Bytes | SHA-256 |
|---|---|---:|---|
| Memoria descriptiva Rev A 06/03/2025 (23 págs.): población, demanda, caudales, metas físicas, presupuesto, plazo | `1.00 MEMORIA_DESCRIPTIVA.pdf` | 2235548 | `107b6edd12233192031ef985ce96f652818b018a7a280e2ba39b336b5c9cf819` |
| Memoria de parámetros de diseño (26 págs., 2025-03-10) | `2.00 MEMORIA PARAMETROS DE DISEÑO.pdf` | 1937664 | `cb995dd406e356b1c5b31017121ea8951c24b5d24354c2f371f2d29cc58c4784` |
| Memoria de población proyectada (1 pág.) | `3.00 MEMORIA POBLACIÓN_PROYECTADA.pdf` | 174422 | `0b6b55d379fa63dbd68e2023ae1840c967677eb5d747b06285b5dc94cfa17d7f` |
| Memoria de tasa de crecimiento (9 págs.) | `4.00 MEMORIA TASA DE CRECIMIENTO.pdf` | 475976 | `4df56771e3bf006e559ba071f1796d9b23b8e08a094731d510824d3d83355db8` |
| Memoria del reservorio (25 págs.) | `5.00 MEMORIA RESERVORIO.pdf` | 709612 | `0f2222e89b9c168a6dc2ee1af17e3f774952604187927df3f7a918c205421358` |
| Resumen de presupuesto (12 págs.) | `6.00 RESUMEN PRESUPUESTO.pdf` | 569076 | `f2bfa24656b52234b28b7f43d16a56140dbad693201cab2dd4cdd0e47dbdc382` |
| Plano reservorio RAP1 (1 lám.) | `7.00 P6EX-RAP-E01-RAP1.pdf` | 391353 | `a3a5b0b74c4c758394075480263b4e634b262d01305d4e6ff0120bae49000713` |
| Plano reservorio RAP1 (2) | `7.00 P6EX-RAP-E01-RAP1 (2).pdf` | 494569 | `d315feff502bb67e8455a9ba78c46710d4747b039724cb2955cadac8f71c8231` |
| Plano reservorio RAP1 (3) | `7.00 P6EX-RAP-E01-RAP1 (3).pdf` | 532555 | `5bbf7245b9963130d0e397b94e7d8b92a04f478109e7cb2b281e810241a2a650` |
| Plano reservorio RAP1 (4) | `7.00 P6EX-RAP-E01-RAP1 (4).pdf` | 281290 | `bea295be25fc841865c627cabe6c4f155bba4940c4427b6800a477757be7e873` |
| Plano reservorio RAP1 (5) | `7.00 P6EX-RAP-E01-RAP1 (5).pdf` | 242225 | `7b5e2ccdbf2ec8b200a243c726a4777cff0bcc0969299001ec1953da90929dc8` |
| **Planos de redes (19 láminas):** red de agua (p.4), diagrama de presiones (p.5), accesorios (p.6), alcantarillado (p.7 y 9), tabla de 202 buzones con coordenadas UTM (p.8), perfiles longitudinales por calle (p.10-19) | `8.00 PLANOS DE REDES.pdf` | 47894299 | `ca8b71f0ec672933fdbaf0eb59699026b088de415ac2e66a02504763b0af64be` |

Archivos auxiliares en la misma carpeta (no son documentos del proyecto): `extract_pdfs.py`, `lines.txt` y `pdf_extracts.txt` (309,710 B, texto extraído de los PDF el 2026-03-26; su ruta interna dice `terra lima documentos\05 EXPEDIENTE V2`).

**Sugerencia al principal:** decidir si se congela este paquete en `datos/` (con hash) y si se extrae la tabla de buzones del plano p.8 a CSV como línea base de diseño. No se hizo en esta tarea porque excede la ficha y no es evidencia de obra.

## 3. Segundo juego de diseño (2023) y DWG de 'ia analisis' — `Control-company\03 renacimiento del sur sac` (NO es lo ejecutado)

Carpeta: `C:\Users\henry\OneDrive\Escritorio\Control-company\03 renacimiento del sur sac\planos agua y desague\`. Plot AutoCAD 2023 de 2023-07-11 según metadatos; archivos con fecha 2025-11-03. Vínculo con el contrato: **POR CONFIRMAR** (E-043, D-013, B-13).

| Archivo | Bytes | SHA-256 |
|---|---:|---|
| `001 OS_AP-01-OS-AP-01 (1).pdf` | 705245 | `22119a41af1556986aedcb2b0e6b7ef74dc9e4641b79b3f024ab7e9cc6546db2` |
| `002 OS_AP-02-OS-AP-02 (1).pdf` | 3182862 | `8aff6c8f3a19f05d3873e64f8cae3a7a66ffcfd1e8bf6a27840a80084c8ae232` |
| `003 OS_SA_01-OS-AP-01.pdf` | 740551 | `4c16b52ab65a22415c0653ba2f8327610b45e72a6d9dcace76d538bd2a8f3298` |
| `004 OS_SA_02-OS-AP-02.pdf` | 3246956 | `abacf2a3efaecc8e040b8b43d34353034569923b86fd483d280b3f6007b0265e` |
| `005 OS_SA-03 al 17-OS-SA-07.pdf` | 648438 | `18567b4aec916a5595d34177eeb3477296ef0b0be85c290d591cb3e5c1470b2a` |
| `005 OS_SA-03 al 17-OS-SA-08.pdf` | 644021 | `9c6f3f49b8f9e3ae311f6d2e9d5e5064386cdae33d1d0080669666a69e31464f` |
| `005 OS_SA-03 al 17-OS-SA-09.pdf` | 619491 | `d2d28e64fa7c4404d9a8d7259c47e67bfbca4c955a9a78d5afd652c61e78076a` |
| `005 OS_SA-03 al 17-OS-SA-10.pdf` | 656755 | `07d21f864c664abd99898094cbc559db5b7735c15722b73672c28dcf2eccdf15` |
| `005 OS_SA-03 al 17-OS-SA-11.pdf` | 660068 | `286ef25b787776f66416ead4c33a3523028b1c78390785f86d69d552d1b76742` |
| `005 OS_SA-03 al 17-OS-SA-13.pdf` | 622865 | `4af010f3f61fe0bb793bd6e9d1d719d8bc2280f324431378c406f6735ceda10b` |
| `005 OS_SA-03 al 17-OS-SA-14.pdf` | 675992 | `79613ab9ff8d8f53e8f413b1f07f2680819c8db728dad4098e2ba7ccabe9c6c4` |
| `005 OS_SA-03 al 17-OS-SA-15.pdf` | 687449 | `0a335ee542e8e273c8bce8d50aa66b2f7a7d6ae8b7e3a36b3e693594b4609e49` |
| `005 OS_SA-03 al 17-OS-SA-16.pdf` | 662847 | `0e12f5732e5f7ad787ebf73dc97df543eb919308f55861db0a2749d4fd6af7c0` |
| `005 OS_SA-03 al 17-OS-SA-17.pdf` | 664327 | `7730ec650b1ec542e1ebe94df07b0b1a96a0139c39c7dce000792f6b5d7b4075` |
| `ACAD-Muro de Reservorio OK-MC-01.pdf` | 2011772 | `97c8889c6c4d508c2d0412e3e24290b9d44fbee942af933d04d352826e31850d` |
| `ACAD-Muro de Reservorio OK-MC-02.pdf` | 609895 | `ca68fd788b0b7c6aa080d6a6ce707c1282e914211a780e18b71d591abc33a314` |
| `ACAD-Muro de Reservorio OK-MC-03.pdf` | 531335 | `6dab2dfa8da553a5041cea7ea7fd96cf9a6c5e67464def1dcbbeb20e92f112a8` |

Faltan en la carpeta las láminas OS-SA-03 a 06 y OS-SA-12. Los PDF de las tres primeras 'OS_SA' llevan en su rótulo interno el título OS-AP-01/02 por error de nombre de plot; el contenido es de alcantarillado.

Archivos CAD en `...\03 renacimiento del sur sac\ia analisis\` relacionados con redes (no inspeccionados con CAD):

| Archivo | Bytes | SHA-256 | Nota |
|---|---:|---|---|
| `diseño corte de agua y desague.dwg` (2026-09-30) | 837194 | `6cd677ecf0cc460a3e0403ae44be5b5cbdfa9664b53fbd5ce314345e77e2ec0e` | DWG binario AC1032; contenido no leído (E-044, B-22) |
| `secciones de calles.dwg` (2026-10-08) | 1013750 | `b43179c7db57b5343a17788bd6fbbbb6100afb54f4464bbbcef9d8c81498d59b` | Secciones viales; el DXF homónimo no tiene texto de agua o desagüe |
| `secciones de calles.dxf` (2026-10-08) | 2268936 | `fdff810acad361d681e105d84077946446287a768a5a1c10c55f1bf753a5e1f0` | Sin red sanitaria en capas ni textos |

Otros DWG de la misma carpeta (`PTL COMPLETO WGS84 VIS v22/v33/v44/v45`, `PARCELAS TERRALIMA C3D`, `Lev. Topográfico/Curvas de Nivel.dwg`) son lotización y topografía; no se abrieron.

## 4. Otras fuentes con datos de diseño o de alcance (no ejecutado)

| Tipo y utilidad | Ruta completa | Bytes | Nota |
|---|---|---:|---|
| Hoja de cálculo con 'PVC-U ISO 1452 C-7.5 DN 110 mm', 34 buzones y 225 conexiones (E-041) | `C:\Users\henry\OneDrive\Escritorio\cotizacion de  conexiones.xlsx` | 15629 | Autor no consta; modificada 2025-12-20; SHA-256 `88621d26bac036aaf1ab11cda0540250ffe7a9eb5d5f1bc837556a9b481ac63f` |
| Plantilla de contrato y TDR 'Etapa 1' (E-040) | `C:\Users\henry\OneDrive\Escritorio\terra lima documentos\z_archivos_doc\  (CONTRATO DE AGUA Y DESAGUE.docx; TDR DE  AGUA Y DESAGUE.docx)` | 16889 / 16243 | Sin completar; no es el contrato de S&G |
| Plano de lotización 'planos de expediente primera etapa' | `C:\Users\henry\OneDrive\Escritorio\terra lima documentos\analisis_archivos\planos de expediente primera etapa.pdf` | 2852671 | Es lotización (cotas de lotes y nombres de calles), no red sanitaria; descartado |

## 5. Topografía base y croquis (no son as-built)

| Tipo y utilidad | Ruta completa | Bytes |
|---|---|---:|
| Topografía base TP-01 | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\A_EXPEDIENTE_HU\A0_Comun\2_Estudios_Basicos\02.01_Topografia\Planos_Topograficos\TP-01.pdf` | 1501015 |
| Topografía base TP-02 | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\A_EXPEDIENTE_HU\A0_Comun\2_Estudios_Basicos\02.01_Topografia\Planos_Topograficos\TP-02.pdf` | 14777423 |
| Topografía base TP-03 | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\A_EXPEDIENTE_HU\A0_Comun\2_Estudios_Basicos\02.01_Topografia\Planos_Topograficos\TP-03.pdf` | 2421651 |
| Topografía base UL-01 | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\A_EXPEDIENTE_HU\A0_Comun\2_Estudios_Basicos\02.01_Topografia\Planos_Topograficos\UL-01.pdf` | 846427 |
| Informe topográfico | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\A_EXPEDIENTE_HU\A0_Comun\2_Estudios_Basicos\02.01_Topografia\Memoria_Descriptiva\Informe Topográfico.pdf` | 3192463 |
| Fotos de BMs (2 JPEG de WhatsApp, 18/02/2026; única evidencia fotográfica del expediente) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\A_EXPEDIENTE_HU\A0_Comun\2_Estudios_Basicos\02.01_Topografia\BMs_Referencias\WhatsApp Image 2026-02-18 at 10.58.56 AM.jpeg y ... (1).jpeg` | 105387 |
| Croquis de división TL-PLA-001 (v1) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\A_EXPEDIENTE_HU\A0_Comun\4_Division_P1_P2\Plano_Delimitacion_P1_P2\TL-PLA-001_2026-10-04_Croquis_v1_BORRADOR.png` | 625076 |
| Croquis de división TL-PLA-002 (v2) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\A_EXPEDIENTE_HU\A0_Comun\4_Division_P1_P2\Plano_Delimitacion_P1_P2\TL-PLA-002_2026-10-04_Croquis_v2_BORRADOR.png` | 778728 |
| Croquis de división TL-PLA-003 (v3), sin coordenadas ni firma | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\A_EXPEDIENTE_HU\A0_Comun\4_Division_P1_P2\Plano_Delimitacion_P1_P2\TL-PLA-003_2026-10-04_Croquis_v3_BORRADOR.png` | 903303 |

## 6. Pre-diseño de contraste en W_contraste (diseño nuevo, NO es evidencia de obra)

| Tipo | Ruta completa | Bytes |
|---|---|---:|
| DXF del pre-diseño de desagüe v0.4 | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B3_Analisis_Tecnicos\Agua_y_Alcantarillado\W_contraste\resultados\v0.4_48calles_pasajes\Pucusana_desague_prediseno.dxf` | 718226 |
| Plano PNG del pre-diseño v0.4 | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B3_Analisis_Tecnicos\Agua_y_Alcantarillado\W_contraste\resultados\v0.4_48calles_pasajes\plano_desague.png` | 432884 |
| Perfil del colector principal v0.4 | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B3_Analisis_Tecnicos\Agua_y_Alcantarillado\W_contraste\resultados\v0.4_48calles_pasajes\perfil_colector_principal.png` | 87347 |
| Criba de corredores (GeoJSON, v1 Primera Expediente) | `C:\Users\henry\OneDrive\Escritorio\exp.-terraLima_v2\B_GESTION_INTERNA\B3_Analisis_Tecnicos\Agua_y_Alcantarillado\W_contraste\resultados\v1_primera_expediente_desague_criba\desague_corredores_calle30_v1.geojson` |  |

Las versiones v0.1 a v0.3 se excluyen: están reemplazadas por v0.4 y tampoco son as-built.

## 7. Carpetas del expediente sin archivos al 2026-10-13 (relevantes para el ejecutado)

`B1_Gestion/04.02_Cronograma_Maestro`, `04.03_Presupuesto_Consolidado`, `04.04_Contratos/{Addendas_Modificaciones, Bases_TdR, Contratos_Firmados, Plan_Contrataciones, Propuestas_Ofertas}`, `04.05_Valorizaciones`, `04.06_Reuniones_Coordinacion`, `B4_Supervision_y_Calidad/{05.02 Cuaderno_Obra_Digital, Informes_*, 05.03 Certificados_Calidad_Materiales, No_Conformidades}`, `B5_Operacion_y_Mantenimiento` (todo), `B6_Correspondencia/08.04_.../Cartas_Recibidas`. Hay un solo archivo en `B4` (`TL-SUP-001`, registro diario del 20/02/2026 previo al contrato).

## 8. Otros archivos revisados y sin utilidad

- `Escritorio\trabajo agua y desague.docx` y `trabajo de implentacion.docx`: 0 bytes (vacíos).
- `Escritorio\cotizacion.xlsx`: cotización de otra obra (pisos/zócalo); sin relación.
- `Downloads\1.- Presupuesto de obra.xlsx`: estructuras exteriores, no saneamiento. Otras coincidencias de palabras clave en `Downloads` y `escritorio 2025` (presupuestos, estudios y contratos de otras obras) no se abrieron en detalle; la revisión por palabra clave no es exhaustiva.
