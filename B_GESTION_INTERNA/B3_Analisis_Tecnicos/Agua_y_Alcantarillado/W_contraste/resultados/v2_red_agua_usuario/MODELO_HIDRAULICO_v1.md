# Modelo hidraulico preliminar de la red de agua dibujada (regimen permanente)

**Estado:** PRELIMINAR, sin revision independiente. No es EPANET: solver propio (metodo del gradiente, Hazen-Williams C=140, numpy/scipy) en `scripts/modelo_hidraulico_agua_usuario.py`. Fecha: 2026-10-31.
**Entradas:** `datos/v5_habilitacion_1341/red_agua_sectores_usuario_v1.json` (Civil 3D, revision 3, sector2 = reservorio 2), demanda base de `resultados/v1_demanda_agua_1341/`, TIN de 2 m.

## Supuestos
- Dos redes independientes (fronteras R1/R2 cerradas): R1 = sector1; R2 = matriz + sector2..6.
- Niveles: R1 Nmin 132.7 / Nmax 134.7 (del calculo anterior); R2 Nmin 118.2 / Nmax 120.2 (terreno 116.2 + 2 y + 4; NO definidos por el usuario).
- Hora punta: K2 = 2.5 (sensibilidad 2.0 y 3.0), reservorios en Nmin. Estatica: sin demanda, reservorios en Nmax.
- Demanda de cada lote concentrada en el nodo mas cercano de su red; todos los lotes incluidos (los 4 lotes de la manzana Z, sin tuberia cercana, cargan al nodo mas proximo).
- Cota del nodo = terreno (TIN), no rasante ni cota de tuberia. Sin perdidas locales, sin demanda contra incendio, sin bombeo (reservorios de carga fija).
- Diametros: predimensionamiento automatico (v <= 1.2 m/s y <= 8 m/km; minimo DN110; diametro interior ~0.9 DN). No son diametros de diseno.
- Union de tramos: se conectan extremos a <= 1 m (incluye uniones en T). Huecos mayores quedan como puntas muertas.

## Resultados (K2 = 2.5)
| | R1 | R2 |
|---|---:|---:|
| Lotes | 333 | 1,008 |
| Longitud de red | 1,677 m | 7,286 m |
| Qmh | 10.9 L/s | 37.3 L/s |
| Presion minima en punta | 14.4 m (E01MZS046-049, cota 115-118) | 18.6 m (E02MZU009/010, cota ~96) |
| Mediana en punta | 29.2 m | 30.8 m |
| Nodos < 10 m | 0 | 0 |
| Estatica maxima | 39.7 m | 41.7 m |
| Nodos > 50 m | 0 | 0 |
| Velocidad max / perdida max | 0.84 m/s / 7.8 m/km | 0.93 m/s / 6.4 m/km |
| DN resultantes | 110 (61 tramos), 160 (8) | 110 (277), 160 (12), 200 (7), 250 (16) |
| Puntas muertas (nodos de grado 1) | 4 | 21 |

Matriz (888 m): DN250 los primeros 386 m, DN200 154 m, DN160 161 m, DN110 187 m; caudal maximo 37.3 L/s, 3.6 m/km; presion en el extremo este 21-23 m.

## Sensibilidad a K2
| K2 | R1 pmin | R2 pmin | R2 Qmh |
|---|---:|---:|---:|
| 2.0 | 14.7 | 17.7 | 29.8 L/s |
| 2.5 | 14.4 | 18.6 | 37.3 L/s |
| 3.0 | 14.5 | 18.6 | 44.7 L/s |
(La presion minima casi no cambia con K2: las perdidas por friccion son de pocos metros; manda la carga estatica.)

## Lectura
- Con los reservorios en esos niveles y la red como esta dibujada, todos los nodos cumplen >= 10 m en punta y <= 50 m estaticos.
- R1: presion minima 14.4 m; para llegar justo a 10 m bastaria Nmin ~128.3 m, es decir el nivel puede quedar cerca del terreno del reservorio (130.2 m) sin torre; conservar >= 2-3 m de margen por incertidumbre de cotas.
- R2: sobran ~8.6 m sobre el minimo; el nivel podria bajar hasta ~8 m y seguir cumpliendo.
- Pendiente: fronteras (valvulas), linea de llenado de R1, aduccion del medidor, manzana Z sin tuberia, puntas muertas, escenarios de falla (rotura de la matriz) y de reservorio en Nmax con demanda minima.
