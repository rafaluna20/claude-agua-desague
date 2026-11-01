# T-04 — preparación y trazabilidad del prediseño de desagüe

**Proyecto:** Terra Lima / Pucusana  
**Fecha:** 2026-10-10  
**Estado:** PREPARACIÓN PARA FASE 2. No se recalculó ni modificó el prediseño.  
**Límite profesional:** todo diseño, contraste de obra y decisión de aplicabilidad normativa es **PARA VALIDAR CON VALVERDE**.

## 1. Alcance de esta preparación

Se revisó la trazabilidad disponible del prediseño de desagüe `v0.4_48calles_pasajes` para que un calculista pueda iniciar una versión posterior una vez cerrada G1. Esta tarea no acepta el prediseño como definitivo, no lo contrasta con la obra construida y no sustituye una memoria de cálculo ni revisión independiente.

Fuentes revisadas: `LEEME.md`, `ESTADO.md`, `supuestos.md`, `datos/v3_48calles/MANIFIESTO.json`, `resultados/v0.4_48calles_pasajes/MANIFIESTO.json`, `desague_resultado.json`, `ptar_resumen.json`, la ficha `T-04_ficha_diseno_desague.md`, `normas/libro_normas.md` y el inventario de ejecutado disponible al corte.

## 2. Línea base identificada y huellas verificadas

| Elemento | Identificación disponible | Verificación realizada | Resultado |
|---|---|---|---|
| Geometría y datos base | `datos/v3_48calles/`, congelado 2026-10-09; incluye 48 calles, 1,341 lotes y 5 pasajes inferidos. | Se recalculó SHA-256 truncado de los 17 archivos declarados en su manifiesto. | Los 17/17 hashes coinciden. |
| Rasante usada | `Hd_final_calles48.npy`, ruta externa declarada en el manifiesto de datos; S-015. | Existe y su `sha256_16` actual es `9773c64a7dc14fce`. | Coincide con el manifiesto. No es rasante as-built. |
| Salida vigente | `resultados/v0.4_48calles_pasajes/`, congelada 2026-10-09. | Se recalculó SHA-256 truncado de los 7 entregables declarados. | Los 7/7 hashes coinciden. |
| Salidas técnicas | JSON de cálculo, XLSX, DXF, plano, perfil, resumen PTAR y tapas de buzón. | Se comprobó presencia y estructura del JSON/XLSX. | Identificables y consistentes con el manifiesto de salida. |
| Historia | `v0.1_25calles`, `v0.2_40calles`, `v0.3_48calles`, `v0.4_48calles_pasajes`. | Se comprobó que v0.4 es la última carpeta de resultados. | Usar v0.4 como única línea base; las anteriores son historia. |

Las huellas demuestran integridad de los archivos presentes, no la validez hidráulica, topográfica, contractual ni constructiva de su contenido.

## 3. Entradas, método declarado y salidas auditables

La skill del proyecto declara el siguiente flujo: `red_calles.py` para red/rasante; `disenar_desague.py` para caudales, trazado, hidráulica y perfiles; `exportar_desague.py` para XLSX/PNG/JSON; y `exportar_dxf.py` para DXF. Declara uso de Python de QGIS para el cálculo y Python del sistema para el DXF.

En el proyecto técnico revisado no se localizó una copia versionada de esos cuatro scripts ni un manifiesto de versiones de Python, QGIS, bibliotecas, comandos o argumentos usados en v0.4. El JSON conserva parámetros y resultados, pero no permite reconstruir por sí solo el algoritmo de trazado, la interpolación de rasante ni las decisiones de red. Por ello:

- La salida v0.4 es **auditable como archivo congelado**.
- Su reproducción numérica y geométrica completa es **BLOQUEADA** hasta recuperar/versionar el código fuente y ambiente de ejecución.
- No se debe deducir que una nueva corrida será equivalente por el solo hecho de reutilizar el JSON o los planos exportados.

El JSON `desague_resultado.json` expone, entre otros, parámetros de corrida, resumen de caudales y conexiones, buzones, tramos, emisor, lotes sin red, conexiones largas, bombeo, trazados dirigidos y multifamiliares. Cada tramo conserva campos de longitud, caudal, diámetro, pendiente, `yD`, velocidad, tensión tractiva, niveles de batea, cobertura y caídas; cada buzón conserva ubicación, tipo, fondo, cobertura, diámetro interior, profundidad y alertas. El XLSX contiene las hojas `Resumen`, `Tramos`, `Buzones`, `Metrados`, `Lotes sin red` y `PTAR (orden de magnitud)`.

## 4. Controles que un calculista puede repetir o auditar

| Control | Estado para v0.4 | Forma de repetir/auditar | Condición para usarlo en v0.5 |
|---|---|---|---|
| Integridad de entradas y salidas | Repetible ahora. | Verificar manifiestos y SHA-256, incluida la rasante externa. | Mantener nuevos manifiestos con hashes completos. |
| Conteo de lotes, etapas, conectados y sin red | Auditable ahora desde JSON y base v3. | Conciliar `parcels_export.json`, pasajes y las listas de salida. | Resolver S-001, S-012 y la exclusión explícita de lotes antes de congelar. |
| Caudales y carga por tramo | Auditable en la salida; no reproducible integralmente sin código. | Revisar parámetros, asignación de lotes y cálculos independientes de tramos críticos. | Cerrar S-003, S-004, S-005 y S-011; registrar fórmula y escenario. |
| Diámetro, pendiente, velocidad, tensión tractiva y `y/D` | Auditable por tramo; la lógica que los eligió no está recuperada. | Recalcular una muestra y los tramos críticos con método independiente. | Aplicar el libro de normas y la decisión de aplicabilidad contractual. |
| Cobertura, bateas, profundidad y caídas | Auditable por tramo/buzón frente a la rasante declarada. | Revisar perfiles y cotas del JSON/DXF. | Sustituir o validar S-015 con topografía y rasante aplicables. |
| Buzones y separación | Auditable por coordenadas/tipos/longitudes; requiere geometría de red para validación completa. | Revisar inicio, empalmes, cambios y distancias; cotejar con los criterios N-016 a N-019. | Justificar buzonetas de pasaje y caídas; usar el criterio aprobado. |
| Separación y cruces con agua | No verificable en v0.4 como coordinación final. | Superponer red de agua calculada y red de desagüe, e inventariar cada cruce. | Esperar diseño de agua y resolver la diferencia RNE/CTPS registrada en N-012 a N-014. |
| Descarga y llegada a PTAR | Solo escenario preliminar. | Revisar trazado, perfil y cota de empalme contra topografía/expediente PTAR. | Cerrar S-017 y contar con definición del PTAR y destino del efluente. |
| Bombeo y excepciones | Auditable solo como resultado de v0.4. | Revisar los campos de excepciones y método de selección. | Recuperar código y documentar umbrales/escenarios antes de concluir que no se requiere bombeo. |

La ausencia de hallazgos en campos como `tramos_no_cumplen` o `pend_min_tractiva_incumple` es un resultado almacenado de v0.4; no constituye una verificación independiente de los criterios.

## 5. Bloqueos y decisiones que deben preceder al cálculo definitivo

1. **G1 no está cerrada.** Deben quedar decididos o modelados como escenarios aprobados S-001, S-003, S-004, S-006, S-011, S-012, S-013, S-015, S-017 y S-019.
2. **Código no recuperado.** Se requiere una copia inmutable de los cuatro scripts declarados, sus datos auxiliares, comandos, argumentos y ambiente de ejecución. Sin ello, v0.4 no es mecánicamente reproducible.
3. **Rasante/topografía.** La rasante de la línea base es de diseño propio y S-015 la identifica como no ejecutada. Se requiere topografía aplicable y, para contraste, cotas as-built.
4. **Pasajes y frentes especiales.** Los cinco pasajes están inferidos; falta su trazo oficial. También debe verificarse físicamente el acceso de los cuatro lotes frente al parque Q, conforme a S-019.
5. **PTAR y descarga.** Falta definir y verificar en campo el punto de llegada, trazado final y condicionantes de la PTAR, incluidos receptor/reúso y estudios exigibles.
6. **Coordinación con agua.** La matriz y red de agua aún no tienen modelo coordinado. No se pueden validar separaciones, cruces, protecciones ni interferencias.
7. **Criterio aplicable.** El libro de normas registra diferencias entre RNE y CTPS para cruces y mínimos; CTPS requiere confirmar entidad receptora, contrato y aplicabilidad al esquema de la Asociación Santa María. **PARA VALIDAR CON VALVERDE.**
8. **Obra ejecutada.** No existen as-built georreferenciados, cotas, certificados ni ensayos suficientes para el contraste. El inventario concluye que el diseño nuevo no puede compararse aún con diámetro, material, profundidad, cruces, buzones, metrados ni pruebas realmente ejecutadas.

## 6. Separación obligatoria: diseño independiente vs. contraste con ejecutado

| Actividad | Base permitida | Resultado permitido | No permitido |
|---|---|---|---|
| Diseño independiente | Datos congelados v3, supuestos aprobados, criterios de `normas/libro_normas.md`, topografía aplicable y definición de PTAR. | Red preliminar v0.5, perfiles, buzones, memoria y excepciones, todos rotulados PRELIMINAR. | Tratar rasante propia, pasajes inferidos o información alegada como realidad construida. |
| Contraste con obra ejecutada | As-built georreferenciado, levantamiento independiente, fotos con trazabilidad, certificados, protocolos y anexos contractuales. | Matriz de conformidad/no conformidad por tramo o punto, con evidencia y severidad. | Inferir la obra desde DXF/PNG del prediseño, cartas del contratista o borradores. |

## 7. Contrato mínimo para una v0.5 reproducible

Antes de ejecutar v0.5, el principal debe emitir un registro de entrada que incluya como mínimo:

1. **Alcance y escenario:** identificación de que se trata de diseño independiente, límite geográfico, lotes incluidos/excluidos, entidad de servicio y destino PTAR/efluente.
2. **Base congelada:** ruta, fecha y SHA-256 de cada archivo de geometría, rasante/topografía, pasajes, PTAR y red de agua empleada. Si se conserva la rasante v0.4, declararla expresamente como escenario, no as-built.
3. **Supuestos y criterios:** versión de `supuestos.md`, decisión de cada S-xxx que afecte el cálculo, versión del libro de normas y tratamiento escrito de conflictos RNE/CTPS.
4. **Código y ambiente:** copia versionada de `red_calles.py`, `disenar_desague.py`, `exportar_desague.py` y `exportar_dxf.py`; SHA-256 de cada uno; versión de QGIS/Python, dependencias, sistema operativo, comandos y argumentos exactos. No basta una descripción del flujo.
5. **Reglas calculables:** fórmula de aportes, infiltración, factores, elección de diámetro, Manning/rugosidad, límites de velocidad, tensión, `y/D`, cobertura, buzones, caídas, bombeo y tratamiento de pasajes/ramales especiales.
6. **Salidas mínimas versionadas:** `desague_resultado.json`, XLSX, DXF, plano, perfiles, cuadro de buzones, memoria preliminar, tabla de lotes sin servicio, tabla de cruces con agua y manifiesto de salida. Cada salida debe indicar versión de insumos, código y parámetros.
7. **Pruebas de aceptación:** control automático por tramo de diámetro, recubrimiento, pendiente/tensión, velocidad, `y/D`, distancia/tipo de buzón, cambios de diámetro, caídas, conexiones, lotes sin red y excepciones. Los incumplimientos deben exportarse explícitamente, no solo quedar como lista vacía.
8. **Revisión independiente:** muestra definida y recálculo de tramos críticos con otro método/herramienta; conciliación entre JSON, XLSX, DXF, perfil y memoria. La liberación de G2 sigue siendo **PARA VALIDAR CON VALVERDE**.

## 8. Autocomprobaciones de esta tarea

- Se verificaron los 17 archivos declarados por el manifiesto `datos/v3_48calles` y los 7 declarados por el manifiesto de salida v0.4: todos coinciden con sus hashes truncados publicados.
- Se verificó la existencia y hash de la rasante externa declarada.
- Se inspeccionó la estructura del JSON, sus campos de tramos y buzones, y las hojas del XLSX.
- No se editaron datos congelados, scripts, resultados, `supuestos.md` ni `ESTADO.md`.
- No se recalculó ningún caudal, perfil, diámetro ni verificación hidráulica.

## 9. Cierre operativo

La línea v0.4 está preservada e identificable, y sirve como referencia preliminar para preparar escenarios. No debe progresar a diseño definitivo ni a contraste de lo construido mientras G1 esté abierta, falte código reproducible o no exista evidencia as-built. La siguiente acción técnica admisible es recuperar/versionar el pipeline y preparar el registro de entrada v0.5; la siguiente acción de coordinación es cerrar las decisiones y evidencia exigidas por G1.
