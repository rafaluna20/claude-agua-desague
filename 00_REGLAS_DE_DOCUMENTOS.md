# Reglas de manejo documental del expediente

## 0. Dos conjuntos separados
- **A_EXPEDIENTE_HU**: solo lo que se presenta o se recibe de la autoridad (municipalidad, SEDAPAL, Luz del Sur, Registros Públicos, etc.) y los proyectos y planos que lo respaldan. Se divide en **A0_Comun** (sirve a ambas partes), **P1_Parte_1** y **P2_Parte_2** (ver `A_EXPEDIENTE_HU/00_LEEME_Estructura_Division.md`). Todo documento aquí debe poder mostrarse a un tercero tal cual: sin notas internas, sin cifras no validadas, sin opiniones.
- **B_GESTION_INTERNA**: lo que Renasur usa para gestionar: contratos con contratistas, costos, valorizaciones, gobernanza, supervisión, análisis estratégicos, correspondencia y marketing. **No se entrega a terceros** salvo que se prepare un PDF específico.

Regla de paso: un documento de B pasa a A solo cuando se formaliza (firmado, sellado o recibido de la entidad). Nunca se copia un borrador de B a A.

## 1. Qué formato se usa
| Tipo | Formato | ¿Se edita? |
|---|---|---|
| Fichas, informes, análisis, protocolos, actas, índices | `.md` (documento de trabajo) | Sí |
| Contratos firmados, licencias, partida registral, factibilidades, resoluciones, cartas recibidas | `.pdf` original | **Nunca** |
| Lo que sale de la empresa (banco, municipalidad, inversionistas, contratistas) | `.pdf` generado desde el `.md` | No, se vuelve a generar |
| Presupuestos, metrados, valorizaciones, cronogramas | `.xlsx` | Sí |
| Planos | `.dwg` y `.pdf` | DWG sí, PDF no |

## 2. Estructura dentro de cada carpeta
```
<carpeta>/
  originales/     PDF firmados o recibidos de terceros. Solo lectura.
  entregas/       PDF generados y enviados, con fecha. Solo lectura.
  *.md            documentos de trabajo vigentes
```

## 3. Códigos y nombres
Formato: `TL-<AREA>-<NNN>_AAAA-MM-DD_Descripcion[_ESTADO].ext`, sin tildes ni espacios.

| Área | Contenido | Carpeta |
|---|---|---|
| LEG | Legal y administrativa (partida, licencia, resoluciones, factibilidades) | A0/1_Legal_Base o P1·P2/1_Legal |
| EST | Estudios básicos (topografía, suelos, ambiental, tráfico, hidrología, riesgos) | A0/2_Estudios_Basicos |
| PLA | Planimetría general (ubicación, lotización, trazado, aportes) | A0/3_Planimetria_General o P1·P2/2_Planos |
| ING | Proyectos de ingeniería por especialidad (agua, alcantarillado, PTAR, electrificación, pistas, drenaje) | P1·P2/3_Ingenieria |
| REC | Recepción de obras (liquidación, as-built, dossier de calidad, recepción municipal, transferencias) | P1·P2/4_Recepcion |
| GES | Gestión del proyecto (incluye los planes de la división en dos partes) | B1 |
| CON | Contratos (número real, ej. 005-2026 = CON-005) | B1 / 04.04 |
| VAL | Valorizaciones | B1 / 04.05 |
| COS | Costos y presupuestos | B2 |
| TEC | Análisis técnicos internos (hipótesis, estrategias, cálculos preliminares) | B3 |
| SUP | Supervisión, calidad, seguridad y ambiente de obra | B4 |
| OYM | Operación y mantenimiento | B5 |
| COR | Correspondencia: `COR-OUT-NNN` enviada, `COR-IN-NNN` recibida | B6 |
| MKT | Presentaciones, renders y marketing | B7 |

Reglas:
1. El correlativo **nunca se reutiliza**, ni aunque el documento se borre. El siguiente libre está en `00_REGISTRO_MAESTRO.md`.
2. Una versión nueva del mismo documento conserva el código y cambia la fecha (o suma `_v2`). Código nuevo = documento nuevo.
3. La fecha es la del documento, no la de archivo. Si no se conoce, se marca "aprox." en el registro.
4. Sufijos: `_FIRMADO` (con firmas y sellos), `_editable`, `_FICHA` (resumen de otro documento), `_SUPUESTOS` (cifras sin validar).
5. Se codifican solo documentos del proyecto. No llevan código los borradores de trabajo, archivos temporales ni las plantillas.
6. Los planos con codificación propia (TP-01, UL-01) y los documentos de terceros con numeración propia **conservan su nombre**; se registran en el maestro.
7. **Largo de ruta: máximo 200 caracteres** (ruta completa, con carpeta de OneDrive y nombre del archivo). Excel y otros programas de Office no abren archivos con rutas de más de unos 218, y Windows falla a partir de 260. Por eso las carpetas y los nombres son cortos: la descripción va en 3 a 5 palabras, nunca la frase completa. Antes de crear subcarpetas nuevas, revisar el largo.
8. Todo documento codificado debe tener su fila en `00_REGISTRO_MAESTRO.md` el mismo día que se crea. Sin registro, el código no sirve.

## 4. Regla de oro sobre las fichas
Un `.md` que resume un documento firmado **nunca lo reemplaza**: cita la fuente y ante discrepancia manda el original. Todo dato sin respaldo se marca `POR CONFIRMAR` con la fecha, no se rellena con estimaciones.

## 5. Cómo generar un PDF para entregar
```
python _herramientas/md2pdf.py ruta/documento.md
```
Genera `entregas/<mismo nombre codificado>.pdf` con Chrome sin interfaz. Requiere Python con el paquete `markdown`. Antes de enviar fuera de la empresa, revisar que el documento no contenga notas internas ni cifras sin confirmar.

## 6. Control de calidad antes de dar un documento por vigente
1. Cada cifra tiene fuente o está marcada como supuesto.
2. Nombres y RUC coinciden con los documentos legales.
3. No hay textos de plantilla (`[XXXX]`) ni tono de conversación.
4. Fecha y responsable indicados.
5. El original firmado correspondiente está en `originales/`.

## 7. Confidencialidad
El contrato contiene cuentas bancarias y datos personales del contratista. No se envía por correo o chat sin necesidad; se comparte solo el PDF del tramo que corresponda.
