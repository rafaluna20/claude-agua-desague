# Matriz de cierre de la puerta G1

**Corte:** 2026-10-10. **Estado de puerta:** NO APTA.  
**Base:** `revision/REV-01_G1_criterios_y_base.md`, T-02, T-03, T-04 preparación, T-05 preparación, T-06 preparación y `PLAN_FASES.md`.

Esta matriz coordina evidencias y decisiones. No reemplaza al revisor independiente ni la validación profesional; toda decisión técnica, contractual o regulatoria permanece **PARA VALIDAR CON VALVERDE** y el ingeniero sanitario colegiado que se designe.

| Prioridad | Control / observación | Responsable de la evidencia o decisión | Entrega mínima verificable | Efecto si falta | Estado al corte |
|---|---|---|---|---|---|
| Crítica | G1-01: decisiones sobre población/dotación, interfaz PTAR y geometría pendiente | Titular/responsable técnico; ingeniero sanitario | Registro por supuesto: inclusión de E01MZS002P, unidades/dormitorios/habitantes, dotación, pasajes, DN, topografía, llegada PTAR y frentes especiales | No calcular ni emitir diseño coordinado; solo preparación o escenarios rotulados `PRELIMINAR` | Abierta; fuente Asociación y alcance general ya definidos por usuario |
| Crítica | G1-02: identificar revisor sanitario y alcance | Titular / Valverde | Nombre, colegiatura vigente, alcance de revisión y condiciones de firma | No cerrar G1, G2, G3 ni emitir documento externo | Abierta |
| Mayor | G1-03: condición de borde de agua | Asociación Santa María; topografía; responsable técnico | Factibilidad/convenio, punto con coordenada/cota/presión/caudal/continuidad, datos de AGUA01/02, MDT/datum y demanda aprobada | No crear EPANET ni dimensionar red/reservorios | Abierta |
| Mayor | G1-08: evidencia del ejecutado | S&G, supervisión, topógrafo independiente, administración | As-built CAD/GIS/PDF o levantamiento, cruces, cotas, identificación de tubería, certificados, pruebas, Anexos A/B y polígono P1 | No emitir contraste por tramo, no conformidad ni presupuesto de subsanación | Abierta |
| Mayor | G1-09: textos/especificaciones faltantes | Archivo del proyecto, EPS/SEDAPAL, responsable normativo | ET de agua, CTPS-ET-004/008, textos oficiales aplicables, mapa climático SENAMHI, información PTAR/receptor | No consolidar criterios faltantes ni ubicar/dimensionar definitivamente PTAR | Abierta |
| Seguimiento | G1-04: correspondencia inventario MD/JSON | sanit-datos | v1.1: E-001 a E-012 equivalentes en ambos formatos | Evita citas ambiguas; no elimina bloqueos de as-built | Corrección emitida; cierre independiente pendiente |
| Seguimiento | G1-05: selección RNE/CTPS para cruces | sanit-normas; responsable técnico | C-001 condicionado: entidad, tipo de cruce, jerarquía y decisión escrita | No adoptar un único criterio ni calificar obra | Corrección emitida; decisión técnica pendiente |
| Seguimiento | G1-06: separar norma de elección | principal; responsable técnico | S-005, S-008, S-013, S-016 y S-018 actualizados; decisión posterior por escenario | Evita presentar elecciones como norma | Corrección emitida; cierre independiente pendiente |
| Seguimiento | G1-07: estado maestro | principal | `ESTADO.md` actualizado con tareas, salidas y bloqueos | Evita activar fases con información obsoleta | Corrección emitida; cierre independiente pendiente |

## Actividades permitidas antes del cierre

- Preservar y recuperar el código, dependencias y comandos del flujo de desagüe para una v0.5 reproducible.
- Solicitar, organizar y versionar la evidencia indicada arriba, sin modificar datos congelados.
- Formular alternativas internas con todos sus supuestos visibles y la etiqueta `PRELIMINAR`.
- Mantener preparación de metrados, planos y memoria sin cantidades, precios, planos de ejecución ni conclusiones de conformidad.

## Actividades prohibidas antes del cierre

- Declarar conformidad/no conformidad de la obra ejecutada por tramo.
- Emitir un modelo EPANET, diseño definitivo, presupuesto de subsanación, cronograma contractual o plano para construcción.
- Elegir por defecto la fuente de agua, la entidad receptora, la norma de cruce, la capacidad de reservorios o la condición de PTAR.
- Presentar cualquier documento de esta carpeta ante terceros.
