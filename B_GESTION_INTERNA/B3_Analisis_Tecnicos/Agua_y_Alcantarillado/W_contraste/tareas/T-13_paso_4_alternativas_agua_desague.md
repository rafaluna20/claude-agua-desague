# T-13 — Paso 4: alternativas de solución para agua y desagüe

**Corte:** 2026-10-10. **Estado:** comparación técnica preliminar para seleccionar trazas a modelar; **no** es diseño hidráulico, factibilidad, plano constructivo ni cierre de G1/G2. La PTAR tendrá expediente independiente; aquí solo se compara la interfaz del colector con su predio.

## Base y método de comparación

- Alcance: 444 lotes `DENTRO` de `00_primera_expediente`; cuatro lotes junto al parque siguen pendientes de acceso/servidumbre. El punto de Santa María y el reservorio son las coordenadas confirmadas por Henry.
- Se usaron el grafo vial v3 (82 nodos, 91 aristas), la asignación de lotes al grafo, la TIN de Civil 3D muestreada a 1 m y las tres interfaces referenciales de la PTAR, todos en `datos/v4_primera_expediente/`. Las cotas son de **terreno natural**, no de ejes de tubería, bateas ni rasantes aprobadas. WGS84 fue confirmado horizontalmente; faltan zona UTM formal y datum vertical documentado.
- Longitudes de rutas viales: camino más corto por las aristas del grafo, más enlaces geométricos a los dos puntos físicos. Los conectores del grafo son **inferidos** de continuidad vial; se deben verificar en DWG/campo. El control de cruce predial se limitó a los 444 polígonos registrados: ausencia de cruces no demuestra propiedad, derecho de paso ni factibilidad constructiva.
- Para comparar interfaces de PTAR se calculó la distancia vial mínima desde cada una de las 439 asignaciones geométricas distintas del lote PTAR. Esta es una **métrica de accesibilidad**, no suma de tuberías, costo ni prueba de gravedad. Incluye el lote de referencia de Santa María, cuyo uso definitivo aún se debe confirmar; otros cuatro lotes carecen de asignación vial.

## A. Aducción Santa María → reservorio

Medidor general: (308466.605, 8622891.887), terreno 101.526 m; reservorio: (308358.792, 8622860.911), terreno 121.327 m. El desnivel es +19.801 m. La presión de 30 m.c.a. y tubería existente de 8 pulgadas fueron **declaradas**, no ensayadas. Si 30 m.c.a. fuese presión **residual disponible al caudal de llenado** en el medidor, y usando las cotas de terreno como aproximación, la carga de entrada sería 131.526 m. Contra un nivel máximo de ensayo de 124.300 m quedarían 7.226 m para pérdidas, accesorios y diferencias entre terreno y eje de tubería. Si la lectura fuese estática, esta resta no acredita capacidad de llenado.

| Alternativa | Traza geométrica | Longitud aproximada | Cruces con los 444 lotes | Juicio de cribado |
|---|---|---:|---|---|
| **A1 — corredor casi directo** | Medidor a reservorio, por espacio abierto aparente | **112.175 m** en planta; la tubería real será mayor | Ninguno detectado | **Preferida para perfil y validación de derecho de paso.** En 114 muestras de TIN a ~1 m no hay pico de terreno superior al terreno del reservorio; no prueba que la tubería enterrada pueda instalarse sin interferencias. |
| A2 — Av. E/Calle 28/Calle 11 + ramal de ladera | Desde medidor por grafo vial y luego ramal hasta reservorio | **~204 m** | El ramal recto cruza `E01MZD143P` | **Descartada en su traza actual**; solo reconsiderar con variante que evite el predio o servidumbre formal. Los enlaces de intersección vial son inferidos. |
| A3 — Av. E/Calle 10 + ramal norte | Camino vial y ramal recto a ladera | **~254 m** | Ninguno detectado en el ramal ensayado | Reserva si A1 no logra derecho de paso; aumenta longitud, accesorios, pérdidas y obra. El corredor de ladera y conectores viales aún requieren reconocimiento. |

**Selección provisional de traza:** A1. Antes de adoptarla se debe superponer el eje con ortofoto, límites de propiedad, áreas libres, estabilidad del talud, interferencias y acceso para mantenimiento; luego levantar perfil del eje **real** y recalcular pérdidas al caudal autorizado. Si no existe derecho de paso, estudiar A3 u otra servidumbre, no trazar automáticamente por A2.

## B. Niveles de reservorio y distribución

El volumen de **500 m³ en dos celdas** y niveles 122.30–124.30 m del T-12 son **un escenario de predimensionamiento**, no capacidad ni niveles aprobados. OS.030 exige determinar volumen con variación horaria de demanda y reservas de emergencia. Las plantas, unidades de vivienda y dotación continúan condicionadas por el programa urbanístico y el clima; no se pueden convertir 444 lotes directamente en un volumen definitivo.

| Alternativa | Supuesto de comparación | Sector vial alto 110.273 m | Sector vial bajo 78.316 m | Decisión |
|---|---|---:|---:|---|
| **D1 — una zona por gravedad, nivel base** | Nmin/Nmax 122.30/124.30 m | 12.027 m.c.a. estáticos a Nmin: solo **2.027 m** de presupuesto de pérdidas hasta 10 m.c.a. | 45.984 m.c.a. estáticos a Nmax | **Frágil en zona alta**. No seleccionar sin EPANET en hora punta y cotas de acometidas. |
| **D2 — una zona por gravedad, mayor cota operativa** | Ensayo de sensibilidad Nmin/Nmax 125.30/127.30 m, **no propuesta constructiva** | 15.027 m.c.a. estáticos a Nmin: **5.027 m** de presupuesto de pérdidas | 48.984 m.c.a. estáticos a Nmax: **1.016 m** de margen frente a 50 m | **Ensayar primero en EPANET y en balance de llenado**. Requiere comprobar capacidad residual de Santa María, estabilidad/altura del reservorio y presiones en todos los puntos. |
| D3 — zona alta con refuerzo/sectorización | Reservorio base y pequeña zona alta impulsada o regulada según simulación | A definir por EPANET | Sector bajo mantiene gravedad; regulación solo si presión real lo exige | Reserva si D1/D2 fallan. Aumenta energía, mantenimiento, redundancia y control; no dimensionar bomba aún. |

Las presiones de la tabla son solo `nivel de agua – terreno de nodo vial`: no incluyen pérdidas, transitorios, alturas de conexión domiciliaria ni incertidumbre de cota. Según OS.050 §4.8, en hora de máxima demanda la presión dinámica no debe bajar de 10 m y la estática no debe superar 50 m. **La decisión entre D1, D2 y D3 permanece abierta.** La mejora prioritaria es optimizar conjuntamente nivel operativo, capacidad real de llenado y presión de la zona alta, evitando elevar el tanque solo para resolver un nodo.

## C. Colector principal e interfaz con PTAR E03MZD049P

El centroide del lote PTAR tiene terreno 78.958 m. Ninguna alternativa define la cota de batea admisible de llegada ni el punto de ingreso del proceso: los fijará el expediente PTAR coordinado. Los tres frentes son geométricos, no conexiones autorizadas.

| Alternativa de interfaz | Eje vial referencial (X, Y) | Terreno en eje | Separación geométrica lote–eje | Media de distancia vial mínima desde 439 asignaciones | Cribado |
|---|---|---:|---:|---:|---|
| **S1 — Calle 30** | 308851.681, 8622760.300 | **78.556 m** | **0.836 m** | **372.4 m** | **Preferida para perfil longitudinal y coordinación PTAR**: frente inmediato y acceso vial más favorable de las tres. |
| S2 — Calle 32 | 308857.710, 8622761.238 | **78.413 m** | 3.933 m | 372.9 m | Alternativa de respaldo prácticamente equivalente en accesibilidad; el terreno es 0.143 m más bajo que S1, diferencia insuficiente para decidir sin batea de PTAR. |
| S3 — Calle 31 | 308820.557, 8622749.186 | **79.347 m** | 3.821 m | 466.1 m | Menos favorable como salida general por accesibilidad y cota de terreno; conservar si el diseño interno de PTAR exige entrada occidental. |

Dos nodos del grafo están por debajo del terreno de interfaz S1/S2 (78.316 y 78.412 m); cuatro están por debajo de S3. **Esto no obliga a bombear**: la viabilidad gravitacional depende de bateas, recubrimientos, pendientes, caudales y perfiles de cada tramo. El orden correcto es trazar red y cotas de buzón, probar gravedad hacia S1 y S2 con OS.070; solo si un bajo punto no puede resolverse con profundidad constructivamente admisible, estudiar una estación de bombeo localizada. No elegir S1 únicamente por la cota del centroide PTAR.

## Puertas para pasar de alternativas a diseño

1. **Aducción:** prueba autorizada presión–caudal de Santa María (estática y residual a caudales de llenado y en horas críticas), caudal/horario/continuidad autorizados, cota del eje de tubería, diámetro interior, material y derecho de paso del corredor A1. La entidad prestadora/Asociación debe confirmar formalmente condiciones y nombre del punto de entrega.
2. **Demanda y reservorio:** unidades por tipología y etapas, habitantes por unidad, dotación climática sustentada, curvas horarias, reservas de emergencia, área legal disponible, geotecnia/taludes y diseño estructural; recalcular volumen y niveles según OS.030.
3. **Distribución:** modelo EPANET reproducible con Nmin/Nmax, caudal de máxima hora, red mallada, acometidas altas, presión estática máxima, velocidades, pérdidas y escenarios de falla/operación. Comparar D1–D3 con costo de ciclo de vida y operación real.
4. **Alcantarillado:** fijar interfaz y cota de batea de la PTAR; generar perfiles de red S1/S2 con caudal inicial/final, tensión tractiva, recubrimiento, profundidades de excavación, cruces con agua, pasajes y los cuatro lotes de parque. Coordinar con expediente PTAR sin incorporar su planta a este expediente.
5. **Revisión:** actualizar matriz de supuestos y G1/G2. El ingeniero sanitario colegiado debe revisar el cálculo y la solución seleccionada antes de cualquier emisión para construir o tramitar.

## Fuentes normativas consultadas

- MVCS, [RNE — OS.050, redes de distribución de agua](https://cdn.www.gob.pe/uploads/document/file/2686380/OS.050%20Redes%20de%20distribuci%C3%B3n%20de%20agua%20para%20consumo%20humano%20DS%20N%C2%B0%20010-2009.pdf), §4.8 presiones y §4.9 ubicación/interferencias.
- MVCS, [RNE — OS.030, almacenamiento de agua](https://cdn.www.gob.pe/uploads/document/file/2686375/OS.030%20Almacenamiento%20de%20agua%20para%20consumo%20humano.pdf?v=1641411243), §§2 y 3.1–3.4 (función, volumen, ubicación, estudios y vulnerabilidad).
- MVCS, [RNE — OS.070, redes de aguas residuales](https://cdn.www.gob.pe/uploads/document/file/2366336/23%20OS.070%20REDES%20DE%20AGUA%20RESIDUALES%20DS%20N%C2%B0%20010-2009.pdf), §3.1 (caudal inicial/final y tensión tractiva); aplicar el resto de criterios al cálculo de perfiles, no a esta criba geométrica.
