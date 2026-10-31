# Agua potable Terra Lima - corrida c01_2026-10-31

**Estado: PRELIMINAR.** Fecha de la corrida: 2026-10-31. Motor de verificacion: EPANET 2.2.

Este informe sale de un calculo reproducible (`scripts/agua_potable/correr.py`). No esta revisado por un tercero ni reemplaza el diseno de un especialista.

## 1. Entradas y trazabilidad

| Entrada | SHA-256 (primeros caracteres) / dato |
|---|---|
| parametros_agua_potable_v1.json | 303d7d4777c280a7 |
| Red dibujada (red_agua_sectores_usuario_v1.json) | 6a51b12ee354beaa; sectores de agua.dwg, revision 3 (2026-10-31): el usuario rediseno la parte alta: sector1  |
| Grilla del terreno | D37A6949EF1C32B9 |
| Cotas de lotes | fc01af207c2547e3 |
| Lotes (parcels_export) | c4e52fc7c079e43a |


Scripts usados (SHA-256 de 12 caracteres): comun.py `8f05b8f66360`, correr.py `9219f05e7f42`, demanda.py `152d7431b0d4`, epanet.py `d84c72d80cfb`, exportar_dxf.py `15cad07ef2ac`, importar_red.py `d80235e77761`, informe.py `5761aedc864a`, modelo.py `206343c05b0e`, pruebas.py `563437cf014a`


## 2. Parametros sin confirmar que afectan el resultado

| Parametro | Valor | Estado | Fuente / nota |
|---|---|---|---|
| bombeo_llenado.eficiencia_bomba | 0.6 | SUPUESTO | Supuesto de predimensionamiento |
| bombeo_llenado.factor_longitud_aduccion | 1.15 | SUPUESTO | Recorrido real = distancia en linea recta x factor (trazado sin dibujar) |
| bombeo_llenado.horas_bombeo_dia | 12 | SUPUESTO | Supuesto de operacion para dimensionar la linea de llenado |
| bombeo_llenado.perdidas_locales_fraccion | 0.1 | SUPUESTO | Supuesto |
| demanda.comercial_cobertura_lote | 0.6 | NO VERIFICADO | Asistente (area util del lote) |
| demanda.comercial_l_m2_d | 6.0 | NO VERIFICADO | Valor usual de la IS.010 anterior; no esta en los textos del libro de normas |
| demanda.riego_l_m2_d | 2.0 | NO VERIFICADO | Asistente; solo referencia, el riego va por red propia con agua tratada de la PTAR (Usuario 2026-10-31) |
| demanda.viviendas_por_piso_multifamiliar | 2 | SUPUESTO | Asistente 2026-10-31 (igual a T-12); con regla por area la poblacion pasa de 10,000 hab y entra contra incendi |
| fuente_agua.carga_hidraulica_m | 131.5 | NO VERIFICADO | cota 101.5 + 30 m.c.a. |
| fuente_agua.punto_medidor_xy | [308466.6, 8622891.9] | NO VERIFICADO | Punto del medidor de Santa Maria usado en el analisis del 2026-10-31; documento fuente por citar |
| fuente_agua.sensibilidad_carga_m | [131.5, 121.5, 111.5] | SUPUESTO | Cargas alternativas si la presion declarada fuera residual y menor |
| hidraulica.diametros_comerciales_dn_id_m | [[75, 0.068], [90, 0.081], [110, 0.099], [160, 0.144], [200, | SUPUESTO | Diametro interior supuesto = 0.9 DN (depende del material y la clase) |
| hidraulica.hazen_williams_c | 140 | SUPUESTO | Tuberia plastica nueva; material y clase aun por definir |
| hidraulica.patron_24h_forma | [0.4, 0.3, 0.3, 0.3, 0.5, 1.0, 1.8, 2.5, 2.2, 1.5, 1.3, 1.2, | SUPUESTO | Forma tipica de consumo domestico; se reescala para media 1 y maximo K2 |
| reservorios.niveles_calculo_m | {'R1': [132.7, 134.7], 'R2': [118.2, 120.2]} | SUPUESTO | R1: terreno 130.2 + 2.5/4.5 m; R2: terreno 116.2 + 2/4 m. Alturas reales aun por definir |


## 3. Demanda de toda la habilitacion (1341 lotes)

Clases: Vivienda ordinaria: 1315, Multifamiliar: 19, PTAR (sin poblacion): 1, Comercial / grifo (manzana Z): 6.

| Escenario | Poblacion (hab) | Volumen m3/d | Qp L/s | Qmd L/s | Qmh L/s | Reservorio total m3 |
|---|---|---|---|---|---|---|
| BASE | 9486 | 1665 | 19.27 | 25.05 | 48.17 | 568 |
| K2 = 2.0 | 9486 | 1665 | 19.27 | 25.05 | 38.53 | 568 |
| Clima templado (155 L) | 9486 | 1532 | 17.73 | 23.05 | 44.32 | 522 |
| Multifamiliar por area (60 % cobertura, 80 m2/viv) | 10788 | 1885 | 21.81 | 28.36 | 54.53 | 743 |
| Comercial al 100 % del lote | 9486 | 1706 | 19.74 | 25.66 | 49.35 | 582 |
| Sin comercial (referencia) | 9486 | 1603 | 18.55 | 24.12 | 46.39 | 547 |


Referencia de riego (NO va en la red potable; riego con agua tratada de la PTAR): 108 m3/d sobre 53883 m2.


## 4. Resultados hidraulicos por red (hora punta, K2 = 2.5)

| Dato | R1 | R2 |
|---|---|---|
| Lotes | 333 | 1008 |
| Longitud (m) | 1677 | 7286 |
| Qmh (L/s) | 10.91 | 37.25 |
| Presion minima punta (mca) | 14.0 | 18.4 |
| Presion P5 (mca) | 17.2 | 21.4 |
| Nodos < 10 mca | 0 | 0 |
| Nodos < 15 mca | 1 | 0 |
| Estatica maxima (mca) | 39.7 | 41.7 |
| Nodos con estatica > 50 | 0 | 0 |
| Velocidad max (m/s) | 0.84 | 0.93 |
| Velocidad min (m/s) | 0.02 | 0.0 |
| Gradiente max (m/km) | 7.8 | 6.4 |
| Tuberias por DN | {90: 56, 110: 5, 160: 8} | {90: 256, 110: 21, 160: 12, 200: 7, 250: 16} |
| Puntas muertas | 4 | 21 |
| Nodos aislados | 0 | 0 |
| Niveles usados [min, max] | [132.7, 134.7] | [118.2, 120.2] |


**Validacion contra EPANET oficial** (diferencia maxima solver propio vs EPANET): R1: presion 0.008 m, caudal 0.0051 L/s; R2: presion 0.011 m, caudal 0.0060 L/s.


## 5. Escenarios adicionales

### 5.1 Volumen de reservorio (sin contra incendio)

| Red | Volumen diario (m3) | Regulacion (m3) | Reserva (m3) | Total (m3) |
|---|---|---|---|---|
| R1 | 377 | 94 | 34 | 129 |
| R2 | 1287 | 322 | 117 | 439 |


Contra incendio: 100 m3 si la poblacion total llega a 10000 hab (poblacion base: 9486 hab).

### 5.2 Simulacion de 24 h (EPANET, reservorio a nivel minimo fijo)

| Red | Presion minima (mca) | Hora | Presion maxima (mca) | Hora |
|---|---|---|---|---|
| R1 | 14.0 | 7:00 | 37.4 | 0:00 |
| R2 | 18.5 | 7:00 | 39.7 | 0:00 |


El reservorio se mantiene a su nivel minimo (no se simula el vaciado/llenado del tanque). Patron SUPUESTO.

### 5.3 Rotura de un tramo (hora punta, tramo de ~30 m)

| Red | Tramos evaluados | Tramos que dejan lotes sin agua | Mayor demanda perdida (L/s) | Mayor n. de lotes sin servicio | Peor presion minima sin corte (mca) |
|---|---|---|---|---|---|
| R1 | 69 | 19 | 10.91 | 333 | 10.4 |
| R2 | 312 | 175 | 37.25 | 1008 | 11.5 |


Si se rompe un tramo y no hay otra via de agua, quedan sin servicio todos los lotes aguas abajo. Tramos segun la parte de la red que dejarian sin agua:

| Red | Tramos que dejan sin agua >= 50 % de la red | Entre 10 y 50 % | Menos de 10 % |
|---|---|---|---|
| R1 | 12 | 2 | 5 |
| R2 | 23 | 21 | 131 |


Tramos con menor presion al romperse otro tramo en R1 (sin perder lotes; detalle en `escenarios.json`):

| Tramo roto | X | Y | Presion minima restante (mca) |
|---|---|---|---|
| 23 | 308421 | 8622984 | 10.4 |
| 24 | 308398 | 8622979 | 10.7 |
| 25 | 308376 | 8622975 | 11.0 |
| 26 | 308354 | 8622970 | 11.3 |
| 51 | 308429 | 8622998 | 11.6 |


Tramos con menor presion al romperse otro tramo en R2 (sin perder lotes; detalle en `escenarios.json`):

| Tramo roto | X | Y | Presion minima restante (mca) |
|---|---|---|---|
| 77 | 308663 | 8622979 | 11.5 |
| 78 | 308640 | 8622991 | 11.6 |
| 79 | 308617 | 8623003 | 11.9 |
| 80 | 308594 | 8623015 | 12.3 |
| 81 | 308571 | 8623027 | 12.6 |


### 5.4 Llenado de los reservorios desde el medidor (aduccion y bomba)


**R1:** aduccion de 201.9 m (recta 175.6 m), Qmd 5.68 L/s, caudal de llenado 11.35 L/s en 12 h/d, DN 160, v = 0.7 m/s, hf = 0.79 m, nivel maximo 134.7 m.

| Carga de la fuente (m) | Altura dinamica (m) | Bomba | Potencia (kW) |
|---|---|---|---|
| 131.5 | 4.0 | si | 0.7 |
| 121.5 | 14.0 | si | 2.6 |
| 111.5 | 24.0 | si | 4.5 |


**R2:** aduccion de 91.3 m (recta 79.4 m), Qmd 19.37 L/s, caudal de llenado 38.74 L/s en 12 h/d, DN 250, v = 0.97 m/s, hf = 0.39 m, nivel maximo 120.2 m.

| Carga de la fuente (m) | Altura dinamica (m) | Bomba | Potencia (kW) |
|---|---|---|---|
| 131.5 | -10.9 | gravedad | 0.0 |
| 121.5 | -0.9 | gravedad | 0.0 |
| 111.5 | 9.1 | si | 5.8 |


Aduccion en linea recta x factor; el trazado real no esta dibujado. La carga de la fuente es NO VERIFICADA.


## 6. Puntos a revisar (capa EPANET_REVISAR)

| Tipo | Gravedad | Cantidad |
|---|---|---|
| Frontera R1/R2 | critico | 8 |
| Llenado por bomba | critico | 1 |
| Lote sin tuberia | aviso | 4 |
| Presion < diseno | aviso | 1 |
| Punta muerta | aviso | 23 |


## 7. Presion por lote

6 de 1341 lotes quedan por debajo de 15 mca en hora punta (de ellos 0 por debajo de 10 mca, la norma). Detalle: `presion_lotes.csv`.


## 8. Archivos de la corrida

- `INFORME.md`
- `civil3d/nodos_tramos_revisar.xlsx`
- `civil3d/red_agua_modelo_epanet.dxf`
- `demanda.json`
- `epanet/red_R1_24h.inp`
- `epanet/red_R1_punta.inp`
- `epanet/red_R2_24h.inp`
- `epanet/red_R2_punta.inp`
- `escenarios.json`
- `lotes_clasificados.json`
- `presion_lotes.csv`
- `procedencia.json`
- `resultados_modelo.json`
- `revisar.json`
- `tuberias_R1.csv`
- `tuberias_R2.csv`
- `INFORME.md`

## 9. Limitaciones

- Regimen permanente con Hazen-Williams; diametros interiores supuestos (0.9 DN) y material/clase sin definir.
- Los niveles de los reservorios son supuestos hasta definir su altura real.
- La carga de la fuente (Santa Maria) no esta verificada y no hay factibilidad escrita.
- La rotura de tramos no considera valvulas de aislamiento (no estan dibujadas): se corta solo el tramo de calculo.
- La red no tiene hidrantes, valvulas ni conexiones domiciliarias modeladas; la demanda se asigna al nodo mas cercano de cada lote.
- Este calculo no reemplaza la revision independiente del expediente (pendiente hasta que el proyecto este completo).
