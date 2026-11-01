# Estado del diseño de contraste (actualizado 2026-11-01)

Versión corta. El estado detallado del 2026-10-10 (tabla completa T-00 a T-14, G1, bloqueos) se conserva sin cambios en `ESTADO_2026-10-10_completo.md`. Detalle por tarea: `tareas/`. Supuestos: `supuestos.md`. Plan y puertas: `tareas/PLAN_FASES.md`.

## Dónde estamos
- **Alcance (G0):** diseño desde cero para contrastarlo con lo ejecutado por S&G Edifica (decisión del usuario, 2026-10-09). Nada es presentable hasta la revisión y firma de un ingeniero sanitario colegiado (**PARA VALIDAR CON VALVERDE**).
- **Puerta G1:** NO APTA según `revision/REV-01_G1_criterios_y_base.md` (2026-10-10). No hay en el repositorio una reevaluación posterior. Por eso los resultados siguen siendo **PRELIMINARES**.
- **Revisión independiente final:** NO lanzada, a propósito, hasta que el usuario declare el proyecto completo.
- **Alcance de lotes: POR CONFIRMAR.** `supuestos.md` S-001 y el estado del 10-oct hablan de 444 lotes de "Primera Expediente". El cálculo de agua del 31-oct se hizo para los **1,341 lotes** de toda la habilitación por decisión del usuario. Hay que decidir cuál rige para el expediente y actualizar S-001.

## Agua potable (1,341 lotes) — pipeline reproducible
- **Pipeline:** `scripts/agua_potable/` (`correr.py`, `pruebas.py`, `comparar.py`); parámetros con estado en `datos/parametros_agua_potable_v1.json`; skill `calculo-agua-potable-terralima`. 9 pruebas pasan.
- **Corrida vigente:** `resultados/v3_agua/c06_2026-11-01` (commit `23572a7`).
- **Diseño del usuario** (`sectores de agua.dwg`): R1 y R2 con sectores 1 y 2 en R1. R1 461 lotes (Pmin 13.7 mca, estática máx. 49.0 con 33 lotes >45 m en E01 manzanas P y Q); R2 880 lotes (Pmin 18.6 mca).
- **Demanda base:** 9,486 hab + comercial → 1,665 m³/d; Qp 19.3, Qmd 25.1, Qmh 48.2 L/s. Los coeficientes (169 L/hab·d, K1 1.3, K2 2.5) los elegí yo: **PENDIENTE de confirmar**.
- **Contra incendio incluido por decisión del usuario:** 100 m³ repartidos por población → R1 210 m³, R2 458 m³ (total 668 m³). **Hidrantes sin ubicar** hasta que se confirme si van en el diseño.
- **Contraste con EPANET 2.2:** hecho en la versión del 31-oct. Niveles de R2 (118.2–120.2) son SUPUESTOS.

## Desagüe
- **Prediseño v0.4:** `resultados/v0.4_48calles_pasajes/` (1,338 de 1,341 lotes, 7,913 m, 163 buzones, llegada al PTAR a 5.2 m). Es referencia preliminar. Los pasajes de las manzanas P, Q, R y E04MZD018P están **inferidos**.
- **No reproducible mecánicamente** (T-04): hay que recuperar y versionar el pipeline antes de hacer un v0.5.
- **Criba de corredor (T-13/T-14):** Calle 30 S1 preferida provisionalmente para llegar al PTAR, Calle 32 S2 de respaldo. Sin caudales ni diseño de tuberías.

## Próximas acciones (propuestas, por prioridad)
1. **Cerrar el dibujo de agua:** 11 fronteras R1/R2, línea de llenado de R1 con bomba (R1 queda sobre la carga de Santa María ≈131.5 m), aducción medidor→R2, 4 lotes de la manzana Z sin tubería, puntas muertas (23 en c01) y matriz abierta de 888 m.
2. **Decisiones del usuario:** ¿hidrantes sí o no? ¿La Asociación Santa María se rige por criterios SEDAPAL? ¿Alcance 444 o 1,341 lotes? Confirmar los coeficientes de demanda.
3. **Orden en el repositorio:** commit local de lo pendiente (corridas c02–c05, cambios de parámetros y pruebas) y probar el DXF nuevo abriéndolo en Civil 3D.

## Bloqueos de G1 que dependen de terceros (sin cambios desde 2026-10-10)
- Planos de replanteo/as-built de S&G (o levantamiento independiente); hoy no hay información georreferenciada de lo ejecutado.
- De la Asociación Santa María: factibilidad escrita y curva presión residual–caudal, caudal autorizado, cota del eje de su tubería, horas de servicio. Se asume que abastece todo, sin papel.
- Datum vertical, zona UTM, fecha y control del levantamiento topográfico.
- Identificar al ingeniero sanitario revisor y el alcance de su validación.
- No se tienen la memoria "Anexo A-1" ni el "Cuadro de Consumos" del ingeniero original (TL-TEC-001, TL-TEC-003).

## Normas: reservas abiertas
- Sin verificar en el libro de normas: comercial 6 L/m²·d y riego 2 L/m²·d (supuestos míos). El riego va por red propia con agua tratada y queda fuera de la demanda potable.
- El PN10 de tubería no está verificado en SEDAPAL (solo válvulas).
- Contra incendio: CTPS 4.4.1 y OS.100 1.6 no lo exigen bajo 10,000 hab, pero CTPS 7.2.4 pide 100 m³ sin excepción. Confirmar con SEDAPAL o la municipalidad.

## Pendientes menores de datos (del 2026-10-10; verificar si siguen vigentes)
- 7 lotes con área distinta entre Odoo y CAD (0.1–0.5 m²): E01MZR046P, E01MZP023P, E01MZQ040P, E01MZQ074P, E01MZQ075P, E02MZV027P, E02MZU027P.
- Odoo: faltaba borrar VEREDA194–197 y JARDIN327, y reimportar APORTEREC10. En el DWG, borrar el polígono duplicado de JARDIN652.
