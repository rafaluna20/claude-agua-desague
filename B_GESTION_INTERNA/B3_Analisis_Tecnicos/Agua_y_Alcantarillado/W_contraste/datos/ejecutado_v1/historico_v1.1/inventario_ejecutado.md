# Inventario de la obra ejecutada de agua y alcantarillado — v1.1

**Corte de revisión:** 2026-10-10. **Uso:** contraste técnico interno.  
**Estado profesional y legal:** **PARA VALIDAR CON VALVERDE** y con ingeniero sanitario colegiado. Este inventario no acredita recepción, conformidad, metrados reales ni calidad de obra.

## Método y estados

Se revisaron las fuentes indicadas en `tareas/T-03_ficha.md`, el contrato disponible y el índice de archivos del expediente. Un dato conserva el estado de su evidencia, no la conclusión de quien lo menciona:

| Estado | Significado en este inventario |
|---|---|
| CONFIRMADO | Existencia documental o ausencia documental comprobada en el expediente al corte; no equivale a verificación física de obra. |
| ALEGADO POR EL CONTRATISTA | Declaración de S&G en Carta 014 y su sustento; sin levantamiento independiente adjunto. |
| BORRADOR | Afirmación dentro del informe de no conformidad sin firma ni envío. |
| POR CONFIRMAR | Dato de gestión, fuente secundaria, dato contradictorio o que exige verificación física/documental adicional. |

## 1. Hechos inventariados (corrección de trazabilidad G1-04)

Esta tabla es la representación Markdown de `inventario_ejecutado.json.hechos`: contiene el mismo conjunto E-001 a E-012, con `id`, `tema`, `valor`, `fuente` y `estado` equivalentes. La versión v1.1 corrige únicamente su correspondencia de identificadores; no modifica la evidencia ni sus estados.

| ID | Tema | Valor | Fuente | Estado | Nota |
|---|---|---|---|---|---|
| E-001 | alcance contractual | Construcción de red de agua potable y alcantarillado del Sector I, Terra Lima, Pucusana; contrato 005-2026-S&G/EDIFICA. | `B_GESTION_INTERNA/B1_Gestion/04.04_Contratos/CON-005_SG-Edifica/TL-CON-005_2026-10-03_FICHA_Contrato.md`, tabla líneas 7-12. | CONFIRMADO | PARA VALIDAR CON VALVERDE contra PDF firmado. |
| E-002 | anexos contractuales | El contrato declara Anexo A (memorias, especificaciones, planos, cronograma) y Anexo B (metrados, ACU, presupuesto, fórmula polinómica); no están archivados en el expediente revisado. | `TL-CON-005_2026-10-03_FICHA_Contrato.md`, sección Anexos que el contrato declara, líneas 23-27. | CONFIRMADO | Ausencia documental, no inexistencia fuera del expediente. |
| E-003 | interferencia puntual | S&G reporta una interferencia entre red de agua y conexión domiciliaria de alcantarillado. | `obra agua y desague/SUSTENTO_TECNICO_contratista.md`, I. Antecedentes, líneas 79-86. | ALEGADO POR EL CONTRATISTA | — |
| E-004 | posición vertical en interferencia | S&G reporta agua aproximadamente 0.30-0.45 m por debajo de conexión predial de alcantarillado. | `SUSTENTO_TECNICO_contratista.md`, V. Análisis, líneas 109-125; conclusiones, líneas 149-158. | ALEGADO POR EL CONTRATISTA | Sin coordenada, cotas absolutas ni levantamiento independiente. |
| E-005 | PN 7.5 | El borrador afirma instalación de PN 7.5; no se hallaron fotos de marcado, guías, certificados ni protocolo de prueba. | `obra agua y desague/informe_tecnico_deNoConformidad.md`, líneas 21-30; `TL-GES-009`, tabla 2, líneas 21-25. | BORRADOR | Evidencia de material instalado: POR CONFIRMAR. |
| E-006 | cruce invertido y protección | El borrador afirma alcantarillado sobre agua y falta de protección; Carta 014 trata una interferencia puntual sin número de cruces. | `informe_tecnico_deNoConformidad.md`, líneas 34-50; `TL-GES-009`, líneas 14-16. | BORRADOR | Cantidad, tipo, cotas y protección existente: POR CONFIRMAR. |
| E-007 | respuesta de S&G sobre PN | Carta 014 no menciona clase ni PN de tubería. | `TL-GES-009`, tabla 2, línea 25; contraste con Carta 014. | CONFIRMADO | Ausencia de respuesta documental. |
| E-008 | avance | Registros internos atribuyen aproximadamente 90% físico y 90% valorizado; otro registro reporta 23.86% anterior. | `TL-GES-005`, líneas 25-28 y 34; `TL-GES-008`, líneas 110-111 y 146-150. | POR CONFIRMAR | Requiere valorizaciones, pagos y metrados reales de Odoo. |
| E-009 | área ejecutada | Registros internos discrepan entre obra solo en Parte 1 y obra a caballo entre Partes 1/2. | `TL-GES-005`, línea 49; `A_EXPEDIENTE_HU/A0_Comun/4_Division_P1_P2/00_LEEME_Division.md`, líneas 78-88. | POR CONFIRMAR | No existe polígono as-built. |
| E-010 | as-built georreferenciado | No se encontró as-built de agua, de alcantarillado ni CAD/GIS UTM de red ejecutada. | `TL-GES-004`, tabla 2, líneas 20-29; búsqueda de archivos del expediente al corte. | CONFIRMADO | Ausencia en expediente revisado. |
| E-011 | pruebas y calidad | No se localizaron protocolos hidráulicos, estanqueidad, certificados de tuberías/accesorios, compactación, concreto ni cuaderno firmado. | `TL-GES-004`, tabla 3, líneas 31-43. | CONFIRMADO | Ausencia en expediente revisado. |
| E-012 | PTAR y descarga | Registros internos indican PTAR no construida y 250 lotes sin punto de descarga. | `TL-GES-008`, líneas 174-188; `P1_Parte_1/00_LEEME_Parte1.md`, líneas 7-12. | POR CONFIRMAR | No hay expediente de PTAR ni inspección física adjunta. |

## 2. Inventario técnico de red construida

No se registran valores verificables de la red ejecutada para los siguientes campos. No se estimaron desde el pre-diseño nuevo.

| Campo requerido para contraste | Valor documentado del ejecutado | Evidencia localizada | Estado |
|---|---:|---|---|
| Trazado, progresivas y coordenadas | No disponible | Sin as-built CAD/GIS ni plano replanteado. | POR CONFIRMAR |
| Diámetro y material de agua | No disponible | Sin Anexo A-2, certificados, guías ni levantamiento. | POR CONFIRMAR |
| PN/clase de agua | No disponible | Solo alegación/borrador sobre PN 7.5; no marcado ni certificado. | POR CONFIRMAR |
| Diámetro, material y clase de alcantarillado | No disponible | Sin planos, certificados ni metrados reales. | POR CONFIRMAR |
| Profundidad de zanja, cotas y recubrimientos | No disponible | Solo referencia puntual alegada, sin cotas absolutas. | POR CONFIRMAR |
| Cruces agua–desagüe | Cantidad, tipo, cotas y protección no disponibles | Carta refiere un punto; documentos internos discrepan sobre extensión. | POR CONFIRMAR |
| Buzones/cajas | Número, tipo, ubicación y cotas no disponibles | Sin planos, metrados, fotos georreferenciadas ni cuaderno. | POR CONFIRMAR |
| Ensayos hidráulicos/estanqueidad | No disponibles | Matriz de recepción los marca FALTA. | CONFIRMADO (ausencia en expediente) |
| Ensayos de compactación/concreto | No disponibles | Matriz de recepción los marca FALTA. | CONFIRMADO (ausencia en expediente) |

## 3. Discrepancias que no se resuelven en esta tarea

| ID | Tema | Versiones localizadas | Acción requerida |
|---|---|---|---|
| D-001 | Avance | ~23.86 % en registros previos frente a ~90 % físico y valorizado comunicado internamente. | Exportar valorizaciones, pagos y metrados reales de Odoo; cotejar con inspección física. |
| D-002 | Extensión de S&G | “Solo Parte 1” frente a “a caballo entre ambas partes”. | Levantamiento de tramos ejecutados y polígono georreferenciado firmado. |
| D-003 | Estado del cruce | Carta: una interferencia puntual; resumen/borrador: problema sistemático. | Inventario de cada cruce con coordenada, cotas, fotografía y protección existente. |
| D-004 | PN 7.5 | Borrador lo afirma; Carta 014 no lo trata; no hay evidencia de material instalado. | Fotos de marcado, guías, certificados y protocolo de prueba; cotejo con Anexo A-2. |
| D-005 | Condiciones contractuales | Ficha contractual y transcripción temporal no coinciden en todos los plazos/retenciones. | Cotejo contra PDF firmado y anexos rubricados. **PARA VALIDAR CON VALVERDE.** |

## 4. Conclusión operativa

La base disponible permite identificar el contrato, alegaciones y brechas, pero **no permite comparar diseño versus ejecutado** en diámetro, material, clase, trazado, profundidad, cruces, buzones, metrados o pruebas. El DXF/PNG de `resultados/v0.4_48calles_pasajes` es un pre-diseño de contraste, no un as-built. El contraste queda bloqueado hasta recibir evidencia de obra y efectuar levantamiento independiente. **PARA VALIDAR CON VALVERDE** antes de emplear este inventario en una reclamación, recepción o documento externo.
