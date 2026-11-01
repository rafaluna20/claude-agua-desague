# T-14 — Paso 5: criba del trazado de desagüe hacia Calle 30

**Fecha:** 2026-10-10. **Estado:** corredor topológico y perfiles de terreno **PRELIMINARES**. No se han diseñado tuberías, buzones, caudales, bateas, recubrimientos ni estaciones de bombeo. No es apto para construir ni metrados.

## Insumos y cálculo reproducible

Se usaron el grafo vial v3 (82 nodos, 91 aristas), la asociación geométrica de 444 lotes a las vías, las cotas de terreno natural de la TIN de Civil 3D y las interfaces referenciales a `E03MZD049P`. El punto de salida S1 Calle 30 coincide con el nodo `NV-0055`, X=308851.681, Y=8622760.300, terreno=78.556 m. El script `scripts/cribar_corredores_desague_primera_expediente.py` genera JSON, GeoJSON y dos PNG en `resultados/v1_primera_expediente_desague_criba/`; el JSON conserva SHA-256 de los insumos.

Para **cribar** rutas, cada arista tiene costo `longitud + 1000 × ascenso de terreno hacia la salida`, en metros. La penalidad es deliberadamente alta para evitar contrapendientes del terreno cuando existe otra ruta. **No es una función de costo económica ni una pendiente hidráulica.** Se compara también un enlace hipotético de 33.049 m desde Calle 31 a S1 a través del lote PTAR; no se incorpora al diseño sin coordinación con el expediente independiente de la planta.

## Resultado de la criba

| Indicador | S1 Calle 30 por grafo vial existente | S1 + enlace hipotético dentro de PTAR |
|---|---:|---:|
| Aristas en árbol de corredores | 81 | 81, incluida la virtual |
| Longitud geométrica del árbol | 2,942.390 m | 2,927.566 m |
| Aristas con ascenso de terreno >0.05 m hacia salida | 11 | 10 |
| Mayor ascenso de terreno entre extremos | **7.025 m**, Calle 31 | **1.947 m**, Pasaje 03 |
| Asignaciones de lotes en aristas fuera del árbol | **29** | **30** |

Estas longitudes **no son metrado de colectores**: el árbol no incluye ramales para todos los lotes, ubicación de buzones, la longitud real de conexiones ni ajustes de traza/cota. De las 444 fichas, 440 tienen asociación vial geométrica (incluye el predio PTAR) y cuatro lotes de parque carecen de acceso definido: `E01MZQ055P`, `E01MZQ056P`, `E01MZQ064P`, `E01MZQ065P`.

### Hallazgo 1 — Calle 31: no forzar todo al ingreso S1 por la vía existente

El extremo junto a la PTAR (`NV-0058`) está en terreno **79.347 m** y el otro extremo de `TV-0043` (`NV-0059`) en **86.372 m**, a 142.012 m de eje; la arista tiene **18 lotes asignados**. El árbol vial, para llegar a S1 sin acceso interno al predio, obliga a conducir desde el extremo bajo hacia el alto: **+7.025 m de ascenso de terreno**. Un colector gravitacional allí requeriría estudiar excavación profunda y disposición de bateas; no se puede aceptarlo por una línea azul en planta ni declarar automáticamente que necesita bomba.

Se ensayó un **enlace geométrico de 33.049 m** entre `NV-0058` y S1: intersecta el polígono del lote PTAR y ningún otro de los 444 lotes. La TIN muestreada a ~1 m baja de 79.347 a 78.556 m sin pico intermedio en esa recta. Esta configuración permitiría llevar el sector de Calle 31 directamente a la zona de S1 a nivel de **corredor**, pero solo si la disposición de la PTAR admite una conducción interna y su cota de llegada. La PTAR puede requerir dos ingresos o un cabezal común interno; no se selecciona ninguna de esas obras todavía.

### Hallazgo 2 — Pasaje 03 y otras zonas

El árbol hacia S1 orienta `TV-0057` (Pasaje 03, **8 lotes**) hacia un nodo **1.947 m** más alto en terreno. Además `TV-0011` de Calle 12 (3 lotes) muestra +0.919 m. Los perfiles de terreno `PF-D01` permiten revisar esas inversiones. Antes de prever estaciones de bombeo hay que replantear las conexiones de pasajes, dibujar rasantes y probar alternativas de batea/profundidad; el grafo contiene 33 conectores inferidos que no son alineamientos levantados.

### Hallazgo 3 — Faltan ramales de servicio en el árbol

Con la salida única S1, **29 asignaciones** están sobre cuatro aristas viales no seleccionadas: Av. E `TV-0001` (13) y Calle 15 `TV-0018/0019/0020` (7+7+2). No significa que esos lotes sean irremediablemente inaccesibles; significa que un árbol de caminos de nodos no resuelve por sí solo los ramales en vías que forman ciclos. La variante interna PTAR deja 30 asignaciones fuera del árbol, por añadir `TV-0044` de Calle 31 (1). Hay que diseñar ramales con puntos de empalme y sentido de flujo, no incorporar ciclos de tubería por defecto.

## Decisión técnica para la siguiente iteración

1. **Mantener Calle 30 como salida principal de estudio**, pero no aprobar un único colector que fuerce Calle 31 a subir 7.025 m de terreno.
2. **Coordinar con el expediente PTAR** una solución al frente occidental de Calle 31: segundo ingreso, cabezal interno a S1 o colector externo autorizado; comparar perfiles y costo antes de escoger. El enlace violeta del PNG es solo una hipótesis geométrica.
3. Resolver primero los perfiles y empalmes de Pasaje 03, Calle 12, Av. E, Calle 15 y los cuatro lotes del parque. Definir la rasante de vías y la batea admisible de la PTAR antes de seleccionar diámetros, profundidades o bombeos.
4. Cuando se cierre población/demanda por tipología, calcular Qi/Qf por tramo, retorno, infiltración, pendiente/tensión tractiva, velocidad, llenado, recubrimiento, separación agua–desagüe y buzones con [RNE OS.070](https://cdn.www.gob.pe/uploads/document/file/2366336/23%20OS.070%20REDES%20DE%20AGUA%20RESIDUALES%20DS%20N%C2%B0%20010-2009.pdf). La norma exige caudales inicial y final, diseño con máximo horario y autolimpieza; **nada de eso queda demostrado por esta criba de terreno**.

## Productos

- `resultados/v1_primera_expediente_desague_criba/PL-D01_criba_corredores_calle30_v1.png`: planta de corredores y alertas, con marca de no constructivo.
- `resultados/v1_primera_expediente_desague_criba/PF-D01_perfiles_terreno_criticos_v1.png`: perfiles de terreno de Calle 31 y Pasaje 03, no perfiles de tubería.
- `resultados/v1_primera_expediente_desague_criba/desague_corredores_calle30_v1.geojson`: aristas para cargar en QGIS y revisar en Civil 3D; coordenadas del DWG y referencia espacial formal pendiente.
- `resultados/v1_primera_expediente_desague_criba/desague_corredores_calle30_v1.json`: árbol, alertas y trazabilidad de insumos.

**Puerta:** G1/G2 siguen sin aprobar. El ingeniero sanitario debe revisar la solución que resulte de los perfiles y caudales antes de emitir plano/memoria constructiva.
