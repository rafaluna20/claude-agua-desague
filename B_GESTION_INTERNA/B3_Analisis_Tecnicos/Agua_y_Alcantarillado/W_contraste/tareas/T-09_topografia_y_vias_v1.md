# T-09 — Insumo topográfico y vial de Primera Expediente v1

**Estado:** HECHA como preparación de cálculo; no constituye diseño de red ni plano final.

## Resultado trazable

| Producto | Resultado |
|---|---|
| TIN Civil 3D | `terreno natural`, muestreada en grilla de 1 m provisional, 597 × 340 nodos |
| Grilla almacenada | `datos/v4_primera_expediente/topografia/terreno_primera_expediente_1m_v1.f32` — SHA-256 `74985D008B3C478A98DDA77AEE4FE7199C2D05333B533D40CEE7DAC331C20270` |
| Cotas por lote v2 | 444/444 interpoladas, 0 sin dato; rango de centroides 78.958–111.460 |
| Vías seleccionadas | 20 calles y 4 pasajes que intersectan `00_primera_expediente` |
| Auditoría de frente (1.0 m) | 416 lotes con calle, 24 solo con pasaje, 4 sin frente geométrico |
| Ejes viales provisionales v2 | 24/24 polígonos con un eje principal candidato; cada eje derivado individualmente para evitar artefactos en intersecciones |
| Perfiles de terreno | 24/24 completos; 2,882 muestras cada 1 m; 0 valores NoData |
| Grafo vial topológico v3 | 24 ejes, 82 nodos y 91 aristas en 1 solo componente conectado; 33 conectores inferidos por continuidad de polígonos viales |
| Asignación lote–grafo | 440 lotes asociados geométricamente a una arista vial; 4 lotes de parque quedan pendientes de servidumbre |
| Cotas en el grafo | 82/82 nodos y 91/91 aristas con cota/pediente natural interpolada; no son perfiles hidráulicos |

## Hallazgos de diseño preliminar

- El centroide corregido de `E03MZD049P` (PTAR) tiene cota 78.958 y es el más bajo de los 444 lotes. Es un indicio favorable para estudiar desagüe por gravedad; no define la cota de ingreso a PTAR ni el perfil hidráulico.
- El centroide corregido de `E01MZD155P`, referencia de la fuente Santa María, tiene cota de terreno 97.795. No sustituye la coordenada/cota/presión/caudal del punto físico de entrega.
- `E01MZQ055P`, `E01MZQ056P`, `E01MZQ064P` y `E01MZQ065P` no muestran frente geométrico a las vías seleccionadas. Se mantienen bajo S-019: no se trazará su ramal hasta validar la vereda perimetral del parque y la servidumbre.
- El mayor gradiente entre extremos de los perfiles es -8.323% en `CALLE11`. Es una lectura del terreno sobre un eje derivado, no una pendiente de rasante ni de colector; deberá ser revisada cuando se definan la red y las cotas de buzones.

## Archivos de trabajo

- `topografia/LECTURA_CIVIL3D_2026-10-10.md`: origen, cobertura y limitaciones de la TIN/ortofoto.
- `topografia/cotas_lotes_terreno_1m_v2.json`: resultado vigente de cotas con centroide geométrico estable; SHA-256 `3F9323FDB276EB98997A655D727B2904538E4796C3BF315CDFBCE2EC889811B8`.
- `topografia/cotas_lotes_terreno_1m_v1.json` queda **SUPERSEDIDO**: la fórmula de centroide sufría cancelación numérica en coordenadas UTM. Conservado para auditoría; la diferencia máxima de cota con v2 es 3.382 m y 119 lotes exceden 0.10 m.
- `vias/vias_primera_expediente_v1.json`: selección vial; SHA-256 `378BE88BE16212B1EBFDA66F5558125376C995B16939122B572A5B6075220F1C`.
- `vias/auditoria_frente_lotes_v1.json`: auditoría de frentes; SHA-256 `212CA991CAF32630750AD7F7EEC64C6BD9448F7E18C33656109B560401F2B884`.
- `vias/ejes_principales_primera_expediente_v2.json`: 24 ejes principales; SHA-256 `02F5DB6D0BCE57C7F23C6563E95CD601FE7AE5F21B11D23AE14679744FCD989F`.
- `topografia/perfiles_ejes_terreno_v1.json`: perfiles cada 1 m; SHA-256 `B01F860E97D251F52A3039177E3F96E7BC158B0399A36413E18F3E2F60E139D5`.
- `vias/grafo_vial_primera_expediente_v3.json`: grafo vial topológico operativo; SHA-256 `C61C38453D9D62BAA270F7C997CE9F0B308D4055A50E9615E57F54712956890D`. Sus 33 conectores son inferidos por continuidad de los polígonos viales (tolerancia 0.05 m); no representan vértices levantados ni rasantes aprobadas.
- `vias/asignacion_lotes_grafo_v1.json`: asociación geométrica de 440 lotes con el grafo; SHA-256 `61E35990C30DCC111823D0C48C39E82EC2003CD558FD7C4D4A37152741FC3D6A`.
- `topografia/grafo_vial_cotas_terreno_v1.json`: cotas y pendientes de terreno en el grafo; SHA-256 `450177B8D86D6344F1C9A4E72445EA24C937EC02C4FDBE6ECDE704D6AB14410B`.
- `vias/interfaces_referenciales_v1.json`: tres alternativas geométricas junto a cada predio de referencia Santa María/PTAR; SHA-256 `72F146AC429FD9832D4537B593ECD563A28BE56B5D67CA5C1AB79039A4E8381C`.
- `vias/ejes_viales_primera_expediente_v1.json` queda **SUPERSEDIDO**: la esqueletización de todas las vías unidas producía 2,540 aristas cortas de intersección; no se usará como entrada de diseño.
- `vias/grafo_vial_primera_expediente_v1.json` y `vias/grafo_vial_primera_expediente_v2.json` quedan **SUPERSEDIDOS**: su nodificación automática fragmentaba artificialmente la red por redondear o no fijar los puntos de conexión sobre los ejes. No se usarán como entrada de diseño.
- `scripts/procesar_grid_terreno.py`, `seleccionar_vias_primera_expediente.py`, `auditar_frente_lotes_vias.py`, `derivar_ejes_viales.py`, `derivar_ejes_principales_viales.py`, `muestrear_perfiles_ejes.py`, `construir_grafo_vial.py`, `construir_grafo_vial_topologico.py`, `asociar_lotes_grafo_vial.py`, `caracterizar_grafo_topografico.py` e `identificar_interfaces_referencia.py`: pipeline reproducible con Python de QGIS.

## Siguiente puerta

Preparar alternativas paramétricas de trazado de agua y desagüe sobre la base vial validada. El diseño hidráulico aún requiere definir población/unidades, dotación y la interfaz hidráulica de Asociación Santa María; para desagüe también se debe validar la llegada exacta a la PTAR.
