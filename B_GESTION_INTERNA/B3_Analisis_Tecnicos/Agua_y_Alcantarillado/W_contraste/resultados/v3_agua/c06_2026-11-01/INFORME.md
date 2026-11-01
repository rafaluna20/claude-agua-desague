# Agua potable Terra Lima - corrida c06_2026-11-01

**Estado: PRELIMINAR.** Fecha de la corrida: 2026-11-01. Motor de verificacion: EPANET 2.2.

Este informe sale de un calculo reproducible (`scripts/agua_potable/correr.py`). No esta revisado por un tercero ni reemplaza el diseno de un especialista.

## 1. Entradas y trazabilidad

| Entrada | SHA-256 (primeros caracteres) / dato |
|---|---|
| parametros_agua_potable_v1.json | c1d7ba2c43043db7 |
| Export de Civil 3D | 9bf03f6f0a78c50a (C:\Users\henry\OneDrive\Escritorio\Control-company\03 renacimiento del sur sac\Lev. Topográfico\sectores de agua.dwg) |
| Red dibujada (red_agua_importada.json) | b0c70b843e8e4429; C:\Users\henry\OneDrive\Escritorio\Control-company\03 renacimiento del sur sac\Lev. Topogr |
| Grilla del terreno | D37A6949EF1C32B9 |
| Cotas de lotes | fc01af207c2547e3 |
| Lotes (parcels_export) | c4e52fc7c079e43a |


Scripts usados (SHA-256 de 12 caracteres): comparar.py `7ab1b5bb6259`, comun.py `8f05b8f66360`, correr.py `d6bfbe1367da`, demanda.py `831b7806ef8a`, epanet.py `d84c72d80cfb`, exportar_dxf.py `15cad07ef2ac`, importar_red.py `d80235e77761`, informe.py `605545c42b6c`, modelo.py `bfeab1f292f4`, pruebas.py `aaab731cc6e9`, vista_previa_dxf.py `fc0ad797b371`


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
| BASE | 9486 | 1665 | 19.27 | 25.05 | 48.17 | 668 |
| K2 = 2.0 | 9486 | 1665 | 19.27 | 25.05 | 38.53 | 668 |
| Clima templado (155 L) | 9486 | 1532 | 17.73 | 23.05 | 44.32 | 622 |
| Multifamiliar por area (60 % cobertura, 80 m2/viv) | 10788 | 1885 | 21.81 | 28.36 | 54.53 | 743 |
| Comercial al 100 % del lote | 9486 | 1706 | 19.74 | 25.66 | 49.35 | 682 |
| Sin comercial (referencia) | 9486 | 1603 | 18.55 | 24.12 | 46.39 | 647 |


Referencia de riego (NO va en la red potable; riego con agua tratada de la PTAR): 108 m3/d sobre 53883 m2.


## 4. Resultados hidraulicos por red (hora punta, K2 = 2.5)

| Dato | R1 | R2 |
|---|---|---|
| Lotes | 461 | 880 |
| Longitud (m) | 2692 | 6451 |
| Qmh (L/s) | 15.05 | 33.12 |
| Presion minima punta (mca) | 13.7 | 18.6 |
| Presion P5 (mca) | 17.9 | 21.9 |
| Nodos < 10 mca | 0 | 0 |
| Nodos < 15 mca | 1 | 0 |
| Estatica maxima (mca) | 49.0 | 41.7 |
| Nodos con estatica > 50 | 0 | 0 |
| Velocidad max (m/s) | 0.92 | 0.83 |
| Velocidad min (m/s) | 0.01 | 0.0 |
| Gradiente max (m/km) | 7.6 | 6.4 |
| Tuberias por DN | {90: 98, 110: 3, 160: 10} | {90: 220, 110: 20, 160: 12, 200: 7, 250: 16} |
| Puntas muertas | 4 | 17 |
| Nodos aislados | 0 | 0 |
| Niveles usados [min, max] | [132.7, 134.7] | [118.2, 120.2] |


**Validacion contra EPANET oficial** (diferencia maxima solver propio vs EPANET): R1: presion 0.010 m, caudal 0.0052 L/s; R2: presion 0.009 m, caudal 0.0060 L/s.


## 5. Escenarios adicionales

### 5.1 Capacidad de los reservorios

| Red | Poblacion (hab) | Volumen diario (m3) | Regulacion (m3) | Reserva (m3) | Contra incendio (m3) | Total (m3) |
|---|---|---|---|---|---|---|
| R1 | 3078 | 520 | 130 | 47 | 32.4 | 210 |
| R2 | 6408 | 1144 | 286 | 104 | 67.6 | 458 |
| Suma | 9486 | 1664 | 416 | 151 | 100.0 | 668 |


Contra incendio INCLUIDO: 100 m3 en total, repartidos entre los reservorios en proporcion a la poblacion que atiende cada uno (R1 32.4 % / R2 67.6 %). La norma exige demanda de incendio desde 10000 hab y la poblacion base es 9486 hab; el volumen (CTPS 7.2.4) se incluye por decision del usuario (2026-11-01).

**Hidrantes: NO ubicados** por decision del usuario (2026-11-01), hasta confirmar si van en el diseno; por eso no se verifica el caudal de incendio en la red.

### 5.2 Simulacion de 24 h (EPANET, reservorio a nivel minimo fijo)

| Red | Presion minima (mca) | Hora | Presion maxima (mca) | Hora |
|---|---|---|---|---|
| R1 | 13.8 | 7:00 | 45.8 | 0:00 |
| R2 | 18.7 | 7:00 | 39.7 | 0:00 |


El reservorio se mantiene a su nivel minimo (no se simula el vaciado/llenado del tanque). Patron SUPUESTO.

### 5.3 Rotura de un tramo (hora punta, tramo de ~30 m)

| Red | Tramos evaluados | Tramos que dejan lotes sin agua | Mayor demanda perdida (L/s) | Mayor n. de lotes sin servicio | Peor presion minima sin corte (mca) |
|---|---|---|---|---|---|
| R1 | 111 | 12 | 15.05 | 461 | 7.6 |
| R2 | 275 | 151 | 33.12 | 880 | 11.7 |


Si se rompe un tramo y no hay otra via de agua, quedan sin servicio todos los lotes aguas abajo. Tramos segun la parte de la red que dejarian sin agua:

| Red | Tramos que dejan sin agua >= 50 % de la red | Entre 10 y 50 % | Menos de 10 % |
|---|---|---|---|
| R1 | 6 | 1 | 5 |
| R2 | 23 | 21 | 107 |


Tramos con menor presion al romperse otro tramo en R1 (sin perder lotes; detalle en `escenarios.json`):

| Tramo roto | X | Y | Presion minima restante (mca) |
|---|---|---|---|
| 21 | 308449 | 8622955 | 7.6 |
| 22 | 308445 | 8622974 | 7.7 |
| 72 | 308421 | 8622984 | 10.1 |
| 73 | 308398 | 8622979 | 10.4 |
| 74 | 308376 | 8622975 | 10.8 |


Tramos con menor presion al romperse otro tramo en R2 (sin perder lotes; detalle en `escenarios.json`):

| Tramo roto | X | Y | Presion minima restante (mca) |
|---|---|---|---|
| 40 | 308663 | 8622979 | 11.7 |
| 41 | 308640 | 8622991 | 11.9 |
| 42 | 308617 | 8623003 | 12.2 |
| 43 | 308594 | 8623015 | 12.5 |
| 44 | 308571 | 8623027 | 12.9 |


### 5.4 Llenado de los reservorios desde el medidor (aduccion y bomba)


**R1:** aduccion de 201.9 m (recta 175.6 m), Qmd 7.83 L/s, caudal de llenado 15.65 L/s en 12 h/d, DN 160, v = 0.96 m/s, hf = 1.43 m, nivel maximo 134.7 m.

| Carga de la fuente (m) | Altura dinamica (m) | Bomba | Potencia (kW) |
|---|---|---|---|
| 131.5 | 4.6 | si | 1.2 |
| 121.5 | 14.6 | si | 3.7 |
| 111.5 | 24.6 | si | 6.3 |


**R2:** aduccion de 91.3 m (recta 79.4 m), Qmd 17.22 L/s, caudal de llenado 34.44 L/s en 12 h/d, DN 250, v = 0.86 m/s, hf = 0.31 m, nivel maximo 120.2 m.

| Carga de la fuente (m) | Altura dinamica (m) | Bomba | Potencia (kW) |
|---|---|---|---|
| 131.5 | -11.0 | gravedad | 0.0 |
| 121.5 | -1.0 | gravedad | 0.0 |
| 111.5 | 9.0 | si | 5.1 |


Aduccion en linea recta x factor; el trazado real no esta dibujado. La carga de la fuente es NO VERIFICADA.


## 6. Puntos a revisar (capa EPANET_REVISAR)

| Tipo | Gravedad | Cantidad |
|---|---|---|
| Frontera R1/R2 | critico | 11 |
| Llenado por bomba | critico | 1 |
| Lote sin tuberia | aviso | 4 |
| Presion < diseno | aviso | 1 |
| Punta muerta | aviso | 19 |


## 7. Presion por lote

7 de 1341 lotes quedan por debajo de 15 mca en hora punta (de ellos 0 por debajo de 10 mca, la norma). Detalle: `presion_lotes.csv`.


## 8. Archivos de la corrida

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
- `red_agua_importada.json`
- `resultados_modelo.json`
- `revisar.json`
- `tuberias_R1.csv`
- `tuberias_R2.csv`
- `INFORME.md`

## 9. Limitaciones

- Hidrantes contra incendio no ubicados ni dimensionados (decision del usuario, pendiente de confirmar si van en el diseno).
- Regimen permanente con Hazen-Williams; diametros interiores supuestos (0.9 DN) y material/clase sin definir.
- Los niveles de los reservorios son supuestos hasta definir su altura real.
- La carga de la fuente (Santa Maria) no esta verificada y no hay factibilidad escrita.
- La rotura de tramos no considera valvulas de aislamiento (no estan dibujadas): se corta solo el tramo de calculo.
- La red no tiene hidrantes, valvulas ni conexiones domiciliarias modeladas; la demanda se asigna al nodo mas cercano de cada lote.
- Este calculo no reemplaza la revision independiente del expediente (pendiente hasta que el proyecto este completo).
