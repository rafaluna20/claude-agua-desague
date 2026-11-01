# Lectura topográfica y ortofoto desde Civil 3D — 2026-10-10

## Propósito y alcance

Registro de solo lectura realizado sobre el DWG activo en Civil 3D para incorporar la topografía disponible como insumo del expediente de agua y alcantarillado de la **Primera Expediente**. No se editó el DWG ni se adoptaron cotas de diseño.

- DWG activo: `PTL COMPLETO WGS84 VIS v45.dwg`.
- Límite de trabajo: `00_primera_expediente`; sus 444 lotes clasificados `DENTRO` permanecen como la base del expediente.
- Sistema de referencia horizontal: **WGS84**, confirmado por el usuario el 2026-10-10.
- Precisión declarada del levantamiento: **2 cm**, confirmada por el usuario el 2026-10-10.
- Falta identificar formalmente el datum vertical que deberá declararse en memoria, planos y perfiles.

## Superficie de terreno disponible

| Campo | Lectura Civil 3D |
|---|---:|
| Objeto | Superficie TIN `terreno natural` |
| Handle | `6F25` |
| Capa | `C-TOPO` |
| Extensión X | 308104.580 a 309296.094 |
| Extensión Y | 8622625.475 a 8623385.107 |
| Cota mínima / máxima | 78.000 / 144.000 |
| Cota media | 94.877 |
| Puntos TIN | 59,427 |
| Triángulos TIN | 118,792 |

La TIN cubre holgadamente la caja de la polilínea `00_primera_expediente` (X 308280.972 a 308875.707; Y 8622660.653 a 8622998.454). Es el objeto que debe muestrearse para generar perfiles, cotas de buzones y rasantes preliminares; no se reemplazará por la rasante artificial heredada del prediseño v0.4.

## Curvas de nivel

No se hallaron polilíneas independientes en `C-TOPO-MAJR`, `C-TOPO-MINR`, `K_CURVAS SIN AGRUPAR`, ni en las capas de texto de curvas consultadas. La única geometría topográfica identificada es la TIN en `C-TOPO`; por tanto las curvas visibles en Civil 3D son, previsiblemente, una representación de estilo de la superficie y no una fuente geométrica independiente.

Antes de publicar un plano de curvas se debe verificar en la configuración de estilo de la TIN el intervalo de curva principal/secundaria y las unidades. No se debe inferir ese intervalo de las capas vacías.

## Ortofoto cargada

| Campo | Lectura Civil 3D |
|---|---|
| Raster | ECW, handle `6F2C`, capa `0` |
| Archivo activo | `C:\Users\henry\OneDrive\Escritorio\Control-company\03 renacimiento del sur sac\Lev. Topográfico\Ortofoto_0A_Pucusana.ecw` |
| Archivo origen declarado | `D:\2026\2. Febrero\1. Pucusana\Lev. Topográfico\Ortofoto_0A_Pucusana.ecw` |
| Estado | Cargada y recortada en Civil 3D |
| Origen | (308114.127, 8622631.606) |
| Cobertura en unidades de dibujo | X 308114.127 a 309294.707; Y 8622631.606 a 8623382.977 |
| Dimensiones | 48,647 × 30,961 píxeles |
| Escala nominal deducida | ~0.02427 unidades de dibujo por píxel |

La caja de `00_primera_expediente` está dentro de la cobertura de la ortofoto. La superficie rebasa la imagen aproximadamente 1.39 unidades en X y 2.13 unidades en Y en su extremo noreste; esto no afecta el límite actual del expediente, pero debe considerarse si se amplía el área de estudio.

## Condiciones para usar el insumo en cálculo

1. Identificar el datum vertical que deberá declararse mediante memoria/archivo topográfico firmado.
2. Confirmar fecha de vuelo/levantamiento, puntos de control y si la TIN representa terreno natural vigente.
3. Muestrear la TIN con una malla y resolución acordadas, conservando parámetros y archivo de salida trazables antes de diseñar perfiles.
4. Las cotas de estructuras existentes, punto de agua Santa María, reservorios y llegada a PTAR requieren levantamiento/control específico; la ortofoto no los valida hidráulicamente.

**Estado:** `DISPONIBLE COMO INSUMO PRELIMINAR`; WGS84 y precisión de 2 cm confirmados. Falta el datum vertical y la documentación de control para cerrar la validación topográfica.

## Adaptador preparado para cálculos

El script `scripts/procesar_grid_terreno.py` valida y transforma una grilla `float32` generada por `civil3d_sample_surface_grid` en cotas bilineales por centroide de los 444 lotes. Conserva los parámetros de malla, el hash SHA-256 de la fuente, nodos sin datos y la orientación norte-sur de Civil 3D. La sintaxis fue verificada con el Python de QGIS 3.44.12.

El puente Civil 3D se detuvo inicialmente y la sesión quedó ocupada durante su recarga. No se generó ningún dato incompleto durante ese incidente; tras reactivarlo se exportó la malla íntegra que se documenta a continuación. Todavía no existen perfiles ni cotas de estructuras de diseño: esas se generarán en la siguiente fase a partir de esta fuente.

### Ejecución de malla v1

El puente se reactivó y se exportó desde `Curvas de Nivel.dwg` la grilla `terreno_primera_expediente_1m_v1.f32`, con los siguientes controles:

| Parámetro | Valor |
|---|---:|
| Superficie | `terreno natural` |
| Origen de grilla | X 308280.000; Y 8622660.000 |
| Celda / dimensiones | 1.00 m provisional; 597 × 340 nodos |
| Cobertura | X 308280.000–308876.000; Y 8622660.000–8622999.000 |
| Nodos válidos / sin dato | 202,333 / 647 |
| Rango de la exportación | 78.000–135.384 |
| SHA-256 de la grilla | `74985D008B3C478A98DDA77AEE4FE7199C2D05333B533D40CEE7DAC331C20270` |

El adaptador `scripts/procesar_grid_terreno.py` produjo `cotas_lotes_terreno_1m_v1.json` (`SHA-256: 347B82B17482F77494E2F41667112F7D5C1B56BCF3DAE668D1DC98A5C5779746`). Los 444 lotes tienen cota interpolada, sin valores NoData; el rango de cotas de centroides es 78.959–111.546.

Referencias de control, **solo en el centroide del lote y no en el punto hidráulico definitivo**:

- `E01MZD155P` (referente de la fuente Santa María): 98.614.
- `E03MZD049P` (predio PTAR): 78.959; es el centroide más bajo entre los 444 lotes.
- `E01MZQ039P` (multifamiliar potencial): 87.269.

La unidad de malla se interpretó provisionalmente como metro por la geometría UTM. WGS84 y precisión declarada de 2 cm están confirmados; sigue pendiente documentar zona UTM, datum vertical y control topográfico formal.
