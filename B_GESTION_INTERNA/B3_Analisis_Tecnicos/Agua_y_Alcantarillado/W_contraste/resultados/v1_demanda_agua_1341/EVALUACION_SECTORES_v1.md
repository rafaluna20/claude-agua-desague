# Evaluacion de la sectorizacion de agua dibujada (sectores de agua.dwg) - PRELIMINAR

**Fecha:** 2026-10-31. **Fuente:** capas agua_reservorio1/2, agua_matriz principal, agua_sector1..6 leidas de Civil 3D; datos en `datos/v5_habilitacion_1341/red_agua_sectores_usuario_v1.json`. Salida completa: `EVALUACION_SECTORES_salida_v1.txt` (script `scripts/evaluar_sectores_agua_usuario.py`).
**Alcance:** geometria + cotas de terreno + demanda base (1,665 m3/d). NO hay simulacion hidraulica (faltan diametros, aducciones, bombeo).

## Veredicto: ACEPTADO EL CONCEPTO, NO LA ASIGNACION RESERVORIO-SECTOR NI LAS UNIONES
- Concepto (2 reservorios + matriz + mallas por sector): coherente con topografia y presiones.
- Cobertura: 1,337 de 1,341 lotes a <=40 m de una tuberia (4 lotes de manzana Z a 48-76 m). Ningun trazado atraviesa lotes. 6.0 m de tuberia por lote.

## Hallazgos
1. R1 (sector1+2) alimenta 462 lotes con cotas 85.6-117.7; solo 131-168 lotes (cota >103-105) necesitan ese nivel. Con Nmax 134.7 (Nmin 132.7) hay 36 lotes >45 m y el mas bajo llega a 49.1 m (limite 50).
2. R2 (sector3-6) alimenta 838 lotes de cota 78-95.9 con terreno del reservorio 116.2: sobra presion (estatica 24-42 m con Nmin 118) y podria absorber los lotes de cota <=103.
3. Las redes de R1 y R2 se tocan: matriz-sector1 a 2.1 m (308451,8622945) y 4.3 m (308642,8622919); matriz-sector2 a 0.5 m (308440,8622984); sector2-sector3 a 5.2-7.9 m. Sin valvula cerrada/reguladora las zonas se mezclan (R1 empujaria 134.7 m a la zona baja: estatica hasta 56.7 m). El dibujo no esta ajustado (snap).
4. Faltan en el dibujo: linea de llenado de R1 (R1 sobre 134.7 m, mas arriba que la carga de Santa Maria ~131.5 m), aduccion medidor-R2, bombeo.
5. agua_sector4 vacia.
6. Puntas muertas (a revisar): sector3 9, sector2 3, sector1 2 (una es la salida de R1), sector5 2, sector6 2, matriz 2.
7. Matriz: un solo trazo abierto de 888 m, sin anillo; 37 lotes toman directo de ella. DN200 da 3.9 m de perdida a 30 L/s y 8.2 m a 45 L/s en toda su longitud.
8. Sector3 tiene 468 lotes y 3,065 m (2.4 veces sector2).

## Reasignacion propuesta (corte por cota)
| Corte | R1 queda | R1 reservorio | R2 total | R2 Qmh | R2 reservorio |
|---|---|---|---|---|---|
| 100 m | 213 lotes, 229 m3/d, 6.6 L/s | ~78 m3 | 1,124 lotes | 39.9 L/s | ~470 m3 |
| 103 m | 168 lotes, 184 m3/d, 5.3 L/s | ~63 m3 | 1,169 lotes | 41.2 L/s | ~486 m3 |
| 105 m | 131 lotes, 133 m3/d, 3.8 L/s | ~45 m3 | 1,206 lotes | 42.7 L/s | ~503 m3 |

## REVISION 2 (2026-10-31): el usuario cargo agua_sector4
Salida completa: `EVALUACION_SECTORES_salida_v2.txt`. Cambio: 6 trazos pasaron de sector3 a sector4 (74BC, 74C6, 74D1 con un vertice nuevo, 74D2, 74D3, 74D4) y se agregaron 2 nuevos (75F1, 75F3). El resto de las capas no cambio.

**Superados por esta revision:** hallazgo 5 (sector4 vacia), hallazgo 8 (sector3 sobredimensionado) y la cifra de "37 lotes sobre la matriz" (ahora son 11).

| Sector | Lotes | Cotas | Qmh | Trazado | m/lote |
|---|---:|---|---:|---:|---:|
| sector1 (R1) | 269 | 87.2-111.5 | 8.7 L/s | 1,611 m | 6.0 |
| sector2 (R1) | 192 | 96.2-117.7 | 6.4 L/s | 923 m | 4.8 |
| sector3 (R2) | 236 | 82.8-95.9 | 12.6 L/s | 1,720 m | 7.3 |
| sector4 (R2) | 259 | 78.0-90.2 | 7.6 L/s | 1,660 m | 6.4 |
| sector5 (R2) | 196 | 80.0-92.3 | 5.8 L/s | 1,139 m | 5.8 |
| sector6 (R2) | 174 | 78.0-87.9 | 5.1 L/s | 1,044 m | 6.0 |
| matriz directa | 11 | 80.0-101.4 | 0.4 L/s | 888 m | - |

R1: 461 lotes (estatica max 47.5 m con Nmax 134.7). R2: 865 lotes, Qmh 31.1 L/s, reservorio ~366 m3.

**Vigentes:** hallazgos 1 a 4, 6 y 7 (con puntas muertas ahora: sector3 4, sector4 7, sector2 3, sector1 2, sector5 2, sector6 2, matriz 2).
**Nuevo:** extremos de sector4 sin unir: 75F1 a 6.7 m de la matriz y 75F3 a 12.4 m; tres extremos del oeste de sector4 a 12-18 m del lazo grande de sector1 (frontera R1/R2); 74BC a 19 m de sector3.

## REVISION 3 (2026-10-31): el usuario rediseno la parte alta
Salida completa: `EVALUACION_SECTORES_salida_v3_R1solo_sector1.txt`. Respaldo de datos previos: `datos/v5_habilitacion_1341/red_agua_sectores_usuario_v1_rev2_respaldo.json`.

**Cambio:** agua_sector1 ahora es la malla del noroeste (ex trazo grande de sector2) + el lazo sur chico + 74A2 recortada hasta (308443,8622983); agua_sector2 pasa a ser la zona centro-este (74A3, 74A4, 7601, 7603 y el tramo nuevo 7604) y 7604 la une a la matriz en (308646,8622922). La matriz recibio un vertice nuevo en ese punto.

**Supuesto de esta revision (A CONFIRMAR):** reservorio 1 = solo sector1; sector2 pasa al reservorio 2 (esta unido a la matriz).

| | Reservorio 1 (sector1) | Reservorio 2 (sector2 a 6 + 11 lotes de matriz) |
|---|---|---|
| Lotes | 333 | 993 |
| Cotas | 92.7-117.7 m | 78.0-98.9 m |
| Qmd / Qmh | 5.7 / 10.9 L/s | 18.3 / 35.2 L/s |
| Reservorio (25 % + 7 %) | ~129 m3 | ~415 m3 |
| Nivel necesario | Nmin 132.7 / Nmax 134.7 (+2.5 m sobre terreno 130.2) | terreno 116.2: sobra |
| Estatica maxima | 42.0 m (antes 47.5-49.1) | ~38 m con Nmin 116 |

Mejora: el limite de 50 m ya no se roza; el reservorio 1 baja de 177 a 129 m3. Pendiente opcional: 120-165 lotes de sector1 con cota <=100-103 m podrian pasar al reservorio 2 (con corte 103: R1 168 lotes, ~63 m3).

**Fronteras R1/R2 que requieren valvula explicita (puntos aprox.):** (308460,8622907) 74A2 con matriz a 2.8 m; (308440,8622984) 75ED con matriz a 0.5 m (cruce o union); (308443,8622983) 74A2 con 74A4 a 5.9 m; (308451,8622946) 74A2 con 7603 a 4.0 m; (308472,8622858) lazo sur con 7601 a 7.4 m; (308406-308430,8623037-8622997) sector1 con sector3 a 5-8 m.
**Puntas muertas:** sector1 3 (74A9, 74AB, 74AC), sector2 4, sector3 4, sector4 7, sector5 2, sector6 2, matriz 2.
**Siguen vigentes:** falta linea de llenado de R1 y aduccion medidor-R2; 4 lotes de manzana Z sin tuberia (48-76 m); matriz de una sola linea abierta (DN250 como punto de partida: 35 L/s da ~1.7 m de perdida; DN200 da ~5 m).
