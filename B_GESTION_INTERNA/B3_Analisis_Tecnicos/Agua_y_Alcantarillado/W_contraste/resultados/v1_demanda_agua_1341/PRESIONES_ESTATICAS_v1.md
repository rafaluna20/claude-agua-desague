# Presiones estaticas preliminares - habilitacion completa (1,341 lotes)

**Estado:** PRELIMINAR, sin revision independiente. Solo presion estatica (sin perdidas por friccion). No es modelo EPANET.
**Fecha:** 2026-10-31

## Fuentes y parametros
- Terreno: TIN `terreno natural` de `Curvas de Nivel.dwg`, grilla de 2 m (523 x 308 nodos, origen X 308140, Y 8622675), `datos/v5_habilitacion_1341/topografia/terreno_habilitacion_2m_v1.f32`, SHA-256 `D37A6949EF1C32B97005C95CF2C13E64D374A2DB7EA2387EE16DCACE187311C7`. 146,792 nodos validos, 14,292 sin dato; los 1,341 centroides tienen cota (interpolacion bilineal).
- Cota de cada lote = terreno en su centroide (NO rasante de calle ni cota de tuberia). Datum vertical sin documentar.
- Reservorio: niveles del escenario T-12 (Nmin 122.300; Nmax 124.300 m). NO aprobados.
- Criterios (N-025/N-050): estatica maxima 50 m.c.a.; dinamica minima 10 m.c.a. en maxima horaria.

## Resultado
Cotas de lotes: 78.0 a 117.7 m (mediana 87.8). T-12 usaba 110.3 m como punto alto porque solo veia la Primera Expediente.

| Nivel del reservorio | Lotes con <10 m | Lotes con <15 m (5 m de perdidas) | Lotes con >50 m en Nmax |
|---|---:|---:|---:|
| Nmin 122.3 (T-12) | 32 | 97 | 0 (max 46.3) |
| 125.0 | 14 | 55 | 0 |
| 127.3 | 1 | 32 | 39 |
| 130.0 | 0 | 14 | 265 |
| 132.7 | 0 | 1 | 474 |

Con una sola zona de presion no hay nivel que cumpla: para que el lote mas alto tenga 15 m hace falta Nmin ~132.7, y entonces 474 lotes pasan de 50 m.c.a. estaticos.

Los 97 lotes con menos de 15 m en T-12: E01 manzanas S (57), T (28) y D (12), a 91-327 m del reservorio.

## Conclusion preliminar
Hace falta una **segunda zona de presion** para los lotes altos de E01, o un reservorio/nivel distinto. Opciones a comparar en EPANET: (a) zona alta con bomba de refuerzo o hidroneumatico para ~100-130 lotes; (b) subir el reservorio con valvulas reductoras de presion en la zona baja; (c) segundo reservorio mas alto.
