# TL-TEC-015: Plan del diseño de contraste de agua y desagüe

**Fecha:** 2026-10-09. **Estado:** propuesta de trabajo; lo legal y lo técnico final se validan (Valverde / ingeniero sanitario colegiado). No es documento presentable a terceros.

## 1. Decisión de alcance (Puerta G0, 2026-10-09)
El usuario decidió **diseñar el agua y el desagüe desde cero** para **contrastar el diseño con lo ya ejecutado** (obra de S&G Edifica, contrato 005-2026, Parte 1). No se parte del diseño original (perdido) ni se asume que lo ejecutado es correcto.

## 2. Objetivo
Obtener (a) un diseño independiente y trazable que cumpla OS.050, OS.070, IS.010 y el reglamento SEDAPAL CTPS-PR-02, y (b) una **matriz de brechas** entre ese diseño y lo ejecutado (diámetro, material y PN, pendiente, profundidad, cruces agua/desagüe, ubicación y tipo de buzones, protección de concreto).

## 3. Método
1. Datos congelados y supuestos con código (`W_contraste/supuestos.md`).
2. Libro de normas con numerales verificados (`W_contraste/normas/`).
3. Diseño por scripts reproducibles (desagüe: prediseño v0.1 ya hecho; agua: por hacer con reservorios AGUA01/02, matriz por el centro de la Av. E y punto de la Asociación junto al lote E01MZD155P).
4. Verificación independiente con otro método (SWMM para desagüe, EPANET para agua) por un revisor que no escribió el diseño.
5. Contraste con lo ejecutado: **depende de recibir planos de replanteo (as-built) y el polígono de la Parte 1.**

## 4. Equipo (agente principal + subagentes) y puertas
Principal (coordina, no calcula) + `sanit-normas`, `sanit-datos`, `sanit-desague`, `sanit-revisor`; luego agua, metrados, planos y memorias.
Puertas: G0 alcance (hecha) → G1 criterios de diseño aprobados por el ingeniero sanitario → G2 diseño preliminar → G3 revisión final y firma. Detalle de flujo en `W_contraste/ESTADO.md`.

## 5. Datos en conflicto detectados (T-01)
- Lotes: geometría vigente 1,341 (E01 469, E02 227, E03 224, E04 421; reexportación final del 2026-10-09) vs plan comercial 1,350 (468/300/282/300). Odoo carga 538 lotes.
- Área típica del lote: **120 m²** (Odoo y geometría coinciden en 534 lotes); la cifra de 160 m² del documento TL-GES-006 no se sostiene.
- Caudales de TL-TEC-003 (5 hab/lote, 150 L/hab/día) vs prediseño (6 hab/lote, 169 L/hab/día): ver supuestos S-003 y S-004. El prediseño v0.3 da 1,116 m³/día de desagüe medio frente a 810 m³/día de TL-TEC-003: la diferencia se explica por esos dos parámetros y debe resolverla el ingeniero sanitario.

## 6. Riesgos
- Sin planos de lo ejecutado no se puede cerrar el contraste.
- Tras dibujar el usuario las calles del este (48 calles), quedan 32 lotes sin calle y 22,005 m² de huecos en la matriz. El prediseño v0.3 ya no necesita colector provisional.
- El PTAR (871 m²) no es el punto más bajo (hay lotes de la etapa 4 a 78.0 m); el ingreso queda a ~5.2 m de profundidad.
- El esquema de factibilidad (SEDAPAL vs Asociación Santa María + PTAR propia) sigue sin decidirse (TL-TEC-001).

## 7. Registro
Los entregables formales que salgan de `W_contraste/` se codifican TL-TEC-016 en adelante (internos) o TL-ING-001 en adelante (cuando se formalicen para A_EXPEDIENTE_HU) y se registran el mismo día.
