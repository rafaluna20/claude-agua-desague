# REV-01 — Revisión independiente de G1: criterios y base de contraste

**Fecha de revisión:** 2026-10-10  
**Alcance revisado:** Puerta G1 de `tareas/PLAN_FASES.md`, sin recalcular redes ni modificar entregables de autoría.  
**Estado profesional:** revisión interna. Toda decisión técnica, contractual, regulatoria o de firma queda **PARA VALIDAR CON VALVERDE** y el ingeniero sanitario colegiado que se designe.

## 1. Documentos revisados

- `LEEME.md`, `tareas/PLAN_FASES.md`, `supuestos.md` y `ESTADO.md`.
- T-02: `normas/libro_normas.md`, `normas/conflictos_y_brechas.md` y `tareas/T-02_informe.md`.
- T-03: `datos/ejecutado_v1/inventario_ejecutado.md`, `inventario_ejecutado.json`, `brechas_de_informacion.md`, `archivos_utiles.md` y `tareas/T-03_informe.md`.
- Preparación de agua: `tareas/T-05_ficha_diseno_agua.md` y `tareas/T-05_preparacion_agua.md`.

La revisión verificó consistencia documental y trazabilidad declarada; no certifica la autenticidad material de fuentes externas, la condición física de la obra ni la aplicabilidad final de una norma.

## 2. Resultado de los controles de G1

| Control de `PLAN_FASES.md` | Resultado | Evidencia |
|---|---|---|
| 1. Criterios con fuente, numeral y estado | Parcialmente conforme para trabajo interno. T-02 registra N-001 a N-050, incluido el estado `NO VERIFICADO` cuando falta texto. Persisten criterios críticos sin texto/especificación aplicable. | `libro_normas.md`, N-024, N-040, N-041 y N-047; `conflictos_y_brechas.md`, sección 3. |
| 2. Inventario ejecutado con estados y declaración de as-built | Conforme como inventario de brechas, no como base de contraste físico. Distingue estados y declara que no se localizó as-built/CAD/GIS. | `inventario_ejecutado.md`, Método, secciones 2, 3 y 5; `brechas_de_informacion.md`. |
| 3. Decisión del responsable técnico sobre los supuestos condicionantes | No conforme. No hay registro de decisión del responsable técnico para los supuestos requeridos por G1. | `supuestos.md`; `PLAN_FASES.md`, G1.3; `T-05_preparacion_agua.md`, sección 7. |
| 4. Ingeniero sanitario revisor y alcance de validación identificados | No conforme. Los documentos aún lo solicitan como pendiente. | `ESTADO.md`, “Decisiones que esperan al usuario”, punto 3; `T-05_preparacion_agua.md`, secciones 4 y 7. |

## 3. Observaciones

| ID | Severidad | Documento / sección afectada | Observación y evidencia | Acción requerida / condición de cierre | Respuesta del autor | Estado |
|---|---|---|---|---|---|---|
| G1-01 | **Crítica** | `supuestos.md`; `tareas/PLAN_FASES.md`, G1.3 | S-001, S-003, S-004, S-006, S-011, S-013, S-015, S-017 y S-019 continúan `PENDIENTE`. S-012 declara pasajes inferidos sin trazo oficial. G1 exige una decisión registrada del responsable técnico, al menos para esos IDs, antes de abrir Fase 2. T-02 y T-05 confirman que población, dotación, entidad receptora, diámetro, topografía/as-built y descarga/PTAR siguen sin definición suficiente. | El principal debe registrar, para cada supuesto, decisión, responsable, fecha, evidencia y alcance. Cuando no exista decisión o evidencia, mantenerlo como bloqueo y no usarlo como dato definitivo. **PARA VALIDAR CON VALVERDE.** | — | Abierta |
| G1-02 | **Crítica** | `ESTADO.md`, “Decisiones que esperan al usuario”, p. 3; `PLAN_FASES.md`, G1.4 | No se identifica al ingeniero sanitario revisor ni el alcance de su validación. El propio estado lo lista como pendiente. | Identificar al profesional responsable y registrar alcance mínimo: criterios aplicables, supuestos, modelo de agua, desagüe, PTAR/descarga, contraste de obra y condiciones de firma. **PARA VALIDAR CON VALVERDE.** | — | Abierta |
| G1-03 | **Mayor** | `tareas/T-05_preparacion_agua.md`, secciones 2, 4, 5 y 7; `T-05_ficha_diseno_agua.md` | No existe paquete de entrada trazable para modelo de agua: fuente/factibilidad y condición de borde, coordenada-cota-presión-caudal de entrega, cotas/capacidad/operación de AGUA01-02, MDT/datum vertical y demanda aprobada. El documento lo reconoce expresamente, pero no existe declaración formal de inexistencia ni entrega alternativa que habilite esos campos. | Mantener bloqueado EPANET/dimensionamiento. Recibir o declarar formalmente inexistente cada insumo, con responsable y fecha; si se estudian alternativas, rotularlas `PRELIMINAR` y separar sus supuestos. **PARA VALIDAR CON VALVERDE.** | — | Abierta |
| G1-04 | **Mayor** | `datos/ejecutado_v1/inventario_ejecutado.md`, sección 2; `inventario_ejecutado.json`, `hechos` | Los identificadores de la versión Markdown no se corresponden con los del JSON. Por ejemplo, `E-001` en Markdown es “Interferencia”, mientras `E-001` en JSON es “alcance contractual”; el patrón se desplaza en los demás registros. Esto impide citar de forma inequívoca un hecho entre formatos. | Emitir una corrección versionada o una tabla explícita de equivalencias. Conservar contenido, fuente y estado de evidencia; no cambiar los hechos sin nueva evidencia. | 2026-10-10: T-03 emitió v1.1. La tabla Markdown “Hechos inventariados” y `inventario_ejecutado.json.hechos` contienen el mismo conjunto E-001 a E-012 con ID, tema, valor, fuente y estado equivalentes; no se cambiaron valores, fuentes ni estados. | Abierta |
| G1-05 | **Mayor** | `normas/conflictos_y_brechas.md`, C-001; `normas/libro_normas.md`, N-012 a N-014 | C-001 indica diseñar con el criterio RNE “más exigente” hasta una definición de Valverde, aunque N-014 declara que la divergencia RNE/CTPS requiere decisión del revisor y la entidad receptora de S-006 no está definida. La indicación puede convertirse en una selección normativa sin responsable técnico ni alcance confirmado. | Sustituir la instrucción por una alternativa explícitamente condicionada, o registrar la decisión del responsable técnico con entidad, tramo/tipo de cruce y fundamento. No usarla para declarar conformidad de la obra ejecutada. **PARA VALIDAR CON VALVERDE.** | 2026-10-10: C-001 ya no adopta RNE; ordena suspender la selección hasta identificar entidad receptora, tramo/servicio y jerarquía aplicable, y registrar ambos escenarios para contraste. | Abierta |
| G1-06 | **Mayor** | `supuestos.md`, S-005, S-008 y S-018 | El estado de los supuestos mezcla texto normativo verificado con elecciones de diseño no aprobadas: K2=2.0 y recubrimiento de 0.60 m se declaran como valores elegidos por el autor; el lado del desplazamiento de 3 m en S-008 también fue elegido por el autor, pese a figurar `CONFIRMADO`. La fuente normativa permite o encuadra opciones, pero no acredita la selección concreta. | Separar “criterio normativo verificado” de “valor/alternativa elegida”; marcar la selección como pendiente de decisión técnica y vincularla a versión del diseño que la use. **PARA VALIDAR CON VALVERDE.** | 2026-10-10: el principal actualizó S-005, S-008 y S-018; también precisó S-013 y S-016. Las elecciones quedan `PENDIENTE` y los criterios verificados se distinguen de ellas; v0.4 no se modificó. | Abierta |
| G1-07 | **Mayor** | `ESTADO.md`, tabla de tareas; `tareas/T-02_informe.md`; `tareas/T-03_informe.md`; `tareas/T-05_preparacion_agua.md` | El tablero maestro declara T-02 y T-03 “lanzada y cortada” sin salidas, y T-05 “no iniciada”; sin embargo existen entregas fechadas 2026-10-10 para T-02, T-03 y una preparación documental T-05. La coordinación de fase queda desactualizada y puede llevar a reutilizar estados erróneos. | El principal debe actualizar `ESTADO.md` sin alterar los resultados de especialistas: versión, fecha, responsable, estado real, bloqueos y relación con G1. | 2026-10-10: el principal actualizó `ESTADO.md` con salidas T-02 a T-06, REV-01, estado `G1 NO APTA` y bloqueos de continuidad. | Abierta |
| G1-08 | **Mayor** | `datos/ejecutado_v1/inventario_ejecutado.md`, secciones 3 y 5; `brechas_de_informacion.md`; `archivos_utiles.md` | El inventario clasifica correctamente la ausencia documental, pero confirma que no hay trazado, cotas, DN/material/PN, buzones, protocolos ni as-built georreferenciado de obra. Por tanto, la base solo permite formular brechas; no permite todavía el contraste diseño–ejecutado por tramo ni una conclusión de conformidad. | Obtener as-built o levantamiento independiente, inventario de cruces, identificación de materiales, ensayos y anexos contractuales. Mantener toda matriz de no conformidad por tramo bloqueada. **PARA VALIDAR CON VALVERDE.** | — | Abierta |
| G1-09 | **Menor** | `normas/libro_normas.md`, N-024, N-040, N-041 y N-047 | Los criterios sin texto o especificación se rotulan correctamente `NO VERIFICADO`, pero no tienen expediente local archivado de la fuente aplicable; la reproducibilidad futura depende de solicitudes aún abiertas. | Anexar o registrar controladamente las fuentes cuando se reciban; conservar el estado `NO VERIFICADO` hasta entonces. | — | Abierta |

## 4. Aspectos con evidencia suficiente para conservar

- T-02 no convierte el sustento del contratista ni el borrador de no conformidad en norma; diferencia criterios verificados de los no verificados.
- T-03 distingue `CONFIRMADO`, `ALEGADO POR EL CONTRATISTA`, `BORRADOR` y `POR CONFIRMAR`, y declara expresamente la ausencia de as-built y datos georreferenciados en el expediente revisado.
- T-05 no formula un modelo EPANET ni inventa cotas, capacidades, presiones o factibilidad; documenta los faltantes necesarios para agua.

Estos aspectos no cierran G1: describen correctamente el límite actual de la evidencia.

## 5. Dictamen

**G1 no apta.**

La puerta no cumple sus controles 3 y 4: faltan decisiones registradas del responsable técnico para supuestos condicionantes y no está identificado el ingeniero sanitario revisor ni su alcance. Además, la fase de agua carece de condiciones de borde, reservorios y topografía apta para modelo, y la base de contraste ejecutado carece de evidencia física/as-built. Se pueden preparar solicitudes, alternativas y borradores explícitamente `PRELIMINAR`; no corresponde abrir Fase 2 como diseño coordinado ni emitir diseño final o conclusión de conformidad hasta cerrar las observaciones críticas y las mayores pertinentes.

