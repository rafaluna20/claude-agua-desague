# T-06 preparacion: condiciones de entrada para metrados, presupuesto y cronograma

**Fecha de verificacion:** 2026-10-10  
**Estado:** PREPARATORIO. No contiene metrados, APU, precios, presupuesto ni cronograma.  
**Alcance:** identifica evidencia y vacios para que T-06 se ejecute despues de G2. No autoriza valorizaciones, compras, cambios en Odoo ni compromisos contractuales.

## 1. Conclusion operativa

T-06 **no puede iniciar la produccion de metrados ni presupuesto**. Su precondicion es el cierre de G2 con trazos, diametros, partidas y versiones coordinadas. La Fase 1 ya produjo el libro de normas y el inventario de brechas, pero G1 permanece **NO APTA**: faltan decisiones técnicas, revisor sanitario, condición de borde de agua y evidencia as-built.

Existe un prediseño de desagüe v0.4 con salidas versionadas. Es una fuente de referencia para definir el formato de entradas, no una base aprobada para medir o costear. No existe una salida de diseño de agua (EPANET, listado de tramos/nodos, perfiles ni memoria) y por ello tampoco una base coordinada de agua y desagüe.

## 2. Fuentes localizadas y uso permitido

| Fuente localizada | Estado observado | Uso en la futura T-06 | Restriccion |
|---|---|---|---|
| `LEEME.md`, `ESTADO.md` y `supuestos.md` | Vigentes en el espacio de trabajo | Reglas, estado de puertas, supuestos y bloqueos | `datos/` esta congelado; los supuestos PENDIENTE no se convierten en datos de costo. |
| `tareas/T-04_ficha_diseno_desague.md` | Disponible | Contrato de entrega del diseño de desagüe | Todo resultado es preliminar y requiere validacion profesional. |
| `tareas/T-05_ficha_diseno_agua.md` | Disponible | Contrato de entrega del diseño de agua | Prohibe inferir capacidades, cotas, presiones o factibilidad. |
| `tareas/T-06_ficha_metrados_presupuesto.md` | Disponible | Precondicion, controles y limitacion de T-06 | Exige G2 cerrada, trazabilidad a resultados versionados y separacion de IGV/indirectos/fecha. |
| `datos/v3_48calles/` y su `MANIFIESTO.json` | Datos geometricos congelados | Referencia de geometria y version de entrada | No editar; un cambio exige nueva version y declaracion de resultados desactualizados. |
| `resultados/v0.4_48calles_pasajes/MANIFIESTO.json` | Congelado 2026-10-09, con hashes | Identificar exactamente las salidas de desagüe de referencia | Prediseño sobre 48 calles y 5 pasajes inferidos; no sustituye G2. |
| `resultados/v0.4_48calles_pasajes/desague_resultado.json`, `buzones_tapas.json`, DXF, XLSX y planos/perfil | Disponibles | Estructura de trazos, buzones y documentación de contraste | El XLSX incluye una hoja llamada `Metrados`, pero no se ha validado ni se debe reutilizar como metrado final antes de G2. |
| `B2_Costos_y_Presupuestos/TL-COS-001_2026-10-03_Cifras_Reales_vs_Supuestos.md` | Disponible | Antecedente para distinguir datos respaldados de supuestos | No es un catálogo de partidas ni fuente de precios para agua/desagüe. |
| `B2_Costos_y_Presupuestos/TL-COS-002` a `TL-COS-004` | Disponibles, identificados como supuestos/ratios | Solo alerta de antecedentes no validados | Excluidos como fuente de precios, cantidades o rendimientos de T-06. |
| Conector local `odoo-agent` | Configurado como MCP de solo lectura | Posible verificacion futura de estructura, si se habilita el alcance correcto | El codigo actual no expone precios, costos, proveedores ni el modulo `obras_presupuesto`; no se consulto ni modifico Odoo. |

No se localizaron, en las rutas revisadas del proyecto y del conector, archivos de APU de agua/desagüe, catálogo de partidas aprobado, cotizaciones de proveedores, rendimientos, cronograma base, archivo MPP ni presupuesto de esas redes.

## 3. Evidencia tecnica disponible y vacios por especialidad

### Desagüe

El resultado v0.4 dispone de un JSON con resumen, buzones, tramos, emisor, lotes sin red y otros registros de excepción; también hay cuadro de buzones/tapas, DXF, Excel, plano y perfil. Esto permite definir el esquema de extracción por tramo y estructura cuando el diseño quede coordinado.

Antes de metrarse se requiere que T-04 entregue una version posterior o ratificada, con identificador de resultado, manifiesto/hash, memoria, perfiles, cruces, excepciones y las decisiones que cierran los supuestos aplicables. Los pasajes inferidos, la llegada a PTAR, los lotes sin servicio deliberadamente excluidos y las condiciones de empalme deben quedar expresamente incluidos o excluidos por tramo.

### Agua potable

No se localizo resultado T-05. Los archivos congelados contienen referencias geometricas de `AGUA01`, `AGUA02`, calles y matriz, pero no constituyen una red diseñada ni un modelo hidraulico. Faltan, entre otros, fuente aprobada, caudal/presion disponible, cotas y capacidades operativas de reservorios, tramos, diametros, material/PN, accesorios, valvulas, hidrantes, conexiones, perfiles, cruces y resultado EPANET reproducible si aplica.

No debe abrirse una partida de agua ni asignarse una cantidad hasta que T-05 entregue esos insumos con version y escenario declarado.

## 4. Catalogo de partidas y unidades: elementos aun por definir

No existe un catalogo contractual aprobado para esta T-06. La siguiente lista es un **checklist de definicion**, no una adopcion de partidas ni de unidades de medida:

| Familia que debe definirse | Desagüe | Agua | Unidad que debe fijar el catalogo | Evidencia que falta para abrir la partida |
|---|---|---|---|---|
| Tuberias | Material, serie/clase, diametro, tramo y empalmes | Material, PN/clase, diametro, tramo y empalmes | Longitud por especificacion | Planos/listado de tramos aprobados y especificacion tecnica. |
| Movimiento de tierras | Zanja, cama, relleno, eliminacion y reposicion | Zanja, cama, relleno, eliminacion y reposicion | Volumen, longitud o superficie segun regla de medicion aprobada | Seccion tipo, profundidad, ancho, suelo, interferencias y destino de excedentes. |
| Estructuras y accesorios | Buzones/buzonetas, tapas, caidas y empalmes | Valvulas, camaras, hidrantes, ventosas, purgas, medidores y anclajes, si el diseño los contempla | Unidad por tipo y rango dimensional/profundidad | Detalle constructivo y listado codificado del diseño. |
| Conexiones e interferencias | Conexiones domiciliarias, cruces, protecciones y enlace PTAR | Conexion a fuente, conexiones domiciliarias, cruces y protecciones | Unidad o longitud segun detalle | Punto exacto, propiedad, cotas, separaciones y aprobacion de la entidad competente. |
| Obras de restitucion y temporales | Vereda/pavimento, desvio, seguridad y control de agua, solo si corresponde | Vereda/pavimento, desvio, seguridad y pruebas, solo si corresponde | Superficie, unidad o periodo definido | Condicion existente, expediente vial y metodo constructivo. |
| Puesta en servicio y control de calidad | Pruebas y recepcion que exijan la norma/especificacion | Pruebas, desinfeccion, pruebas de presion y recepcion que exijan la norma/especificacion | Unidad o lote de prueba definido | Libro de normas cerrado y especificaciones aprobadas. |
| PTAR y obras externas | Solo si quedan dentro del alcance del expediente | No aplica salvo interferencias definidas | Se definira tras delimitar alcance | Ingenieria de proceso, arquitectura/estructura/electromecanica y linderos de alcance. |

Las reglas de medicion, inclusiones, desperdicios, rendimientos y secuencia constructiva no estan definidas. Deben venir de especificaciones aprobadas y del catalogo que se valide; no se deben deducir de un DXF o de una cantidad global.

## 5. Contrato minimo de entradas desde los diseños

El responsable de T-06 debe recibir, para **cada especialidad y cada alternativa vigente**, un paquete con los siguientes campos minimos:

1. Identificador de diseno, revision, fecha, responsable, estado de puerta y manifiesto/hash de sus archivos fuente.
2. Limite de alcance georreferenciado: etapas, calles, pasajes, predios, conexiones, PTAR/fuente y exclusiones expresas. Debe diferenciar diseno nuevo, obra ejecutada a contrastar y obra fuera de alcance.
3. Listado trazable de elementos: ID unico, plano o modelo de origen, coordenadas de inicio/fin, longitud/geometria, cotas, pendientes/profundidades y condicion de cruce/interferencia.
4. Especificacion de cada elemento: material, norma, diametro/seccion, clase/PN, tipo de union, accesorio/estructura, recubrimiento/proteccion y detalle constructivo aplicable.
5. Secciones tipo y condicion constructiva: excavacion, cama, relleno, compactacion, reposicion, suelo/roca, nivel freatico si aplica, accesos y manejo de excedentes.
6. Listado de estructuras y accesorios con tipo, dimensiones, profundidad/altura, tapa, conexion y detalle de armado/proteccion cuando corresponda.
7. Matriz de cruces, separaciones y protecciones, con responsable de resolucion y evidencia de conformidad normativa.
8. Cuadro de conexiones, lotes/usuarios incluidos, puntos de entrega/descarga, reservas y exclusiones.
9. Memoria, especificaciones, planos y modelo consistentes entre si; toda discrepancia se registra como no conformidad antes de medir.
10. Declaracion de riesgos, contingencias y exclusiones tecnicas; no se convierte una contingencia en cantidad sin una regla aprobada.

Cada fila de metrado debera guardar como minimo: codigo de partida, especialidad, elemento/IDs de origen, archivo y revision fuente, regla de medicion aprobada, unidad aprobada, responsable de verificacion y estado de revision. La cantidad solo se calcula luego de recibir el paquete completo y de cerrar G2.

## 6. Verificaciones requeridas en `obras_presupuesto`

**PARA VALIDAR CON VALVERDE** antes de usar informacion del sistema con finalidad contractual, de valorizacion o de compra.

El conector disponible se reviso solo en su codigo local. Es de solo lectura y limita las consultas a elementos urbanos/capas y a un subconjunto de campos de lotes; no permite verificar `obras_presupuesto`, precios, costos, proveedores ni ordenes. Se requiere una via institucional de solo lectura, con permisos y alcance aprobados, para comprobar:

- existencia, version y responsable funcional del modulo `obras_presupuesto`;
- proyectos, centros de costo/cuentas analiticas, etapas y reglas para separar diseno nuevo de contrato S&G y de obra ejecutada;
- catálogo de partidas, codigos, unidades, descripciones tecnicas, reglas de rendimiento y sus historiales de version;
- estructura de APU: insumos, mano de obra, equipos, rendimientos, desperdicios, costos indirectos, gastos generales, utilidad e impuestos, cada uno con vigencia;
- listas de precios, cotizaciones, proveedores aprobados, moneda, flete/entrega a Pucusana, plazo de vigencia y condiciones comerciales;
- configuracion de IGV, redondeo, tipo de cambio y fecha de corte;
- flujo de aprobacion, auditoria, adjuntos de evidencia, exportacion reproducible y permisos de solo lectura;
- posibilidad de importar la matriz de metrado sin sobrescribir presupuestos existentes ni modificar Odoo.

La configuracion MCP existente no debe ampliarse de forma ad hoc. Cualquier habilitacion de modelos/campos o conexion a `obras_presupuesto` debe revisarse por seguridad, quedar documentada y ser inicialmente de solo lectura.

## 7. Trazabilidad obligatoria de precios y APU

No se registro ningun precio en esta preparacion. Cuando se habiliten fuentes, cada precio o componente de APU debe registrar:

- codigo de partida e insumo, especificacion tecnica y unidad;
- fuente primaria (cotizacion, lista, orden, contrato o registro Odoo), numero/URL/archivo y hash del adjunto cuando aplique;
- proveedor, fecha de emision, fecha de captura, vigencia, ubicacion de entrega y condiciones de pago/entrega;
- moneda, tipo de cambio y fecha de tipo de cambio si corresponde;
- separacion explicita entre precio base, flete, merma aprobada, impuestos, indirectos, gastos generales y utilidad;
- responsable que capturo/verifico, fecha de verificacion, version de presupuesto y aprobacion;
- relacion con el elemento y la revision de diseño que generan la necesidad.

Un precio sin fecha, unidad comparable, especificacion o evidencia adjunta se marca **NO UTILIZABLE**. No se usaran ratios historicos como sustituto de APU ni de cotizacion vigente.

## 8. Bloqueos y condiciones para desbloquear T-06

| Bloqueo | Impacto | Condicion de desbloqueo |
|---|---|---|
| G2 no cerrada; G1 y supuestos relevantes siguen pendientes | Impide medir el alcance coordinado | Puertas cerradas por el principal y registro de decisiones/versiones. |
| T-05 no cuenta con diseño/modelo de agua | La preparación T-05 existe, pero no hay base para agua, accesorios ni cruces coordinados | Entrega T-05 completa y escenario/fuente aprobados. |
| Prediseño T-04 aun preliminar; pasajes y empalmes pendientes | Las cantidades de desagüe no son finales | Revision normativa, perfiles/empalmes y exclusiones confirmadas. |
| Falta as-built/replanteo y poligono de Parte 1 | No se puede separar con certeza obra ejecutada, contraste y saldo | Entrega y clasificacion de evidencia ejecutada; **PARA VALIDAR CON VALVERDE** si afecta contrato. |
| No hay catalogo de partidas, APU, cotizaciones ni rendimientos localizados | No se puede formar precio unitario ni secuencia realista | Catalogo aprobado y fuentes trazables de precio/rendimiento. |
| Conector Odoo no alcanza `obras_presupuesto` ni precios | No se puede verificar estructura o historial en el sistema | Acceso institucional de solo lectura y verificacion funcional documentada. |
| No hay cronograma base, frentes, productividad ni plazos de suministro | No se puede generar cronograma defendible | Secuencia constructiva aprobada, disponibilidad de frentes y datos vigentes de suministro/rendimiento. |

## 9. Siguiente accion permitida

Mantener esta ficha como lista de control. Tras el cierre de G2, recibir los dos paquetes de diseño, ejecutar una revision de consistencia planos-memoria-modelo y recien entonces crear la matriz de metrado versionada. La elaboracion de APU, presupuesto y cronograma debe ocurrir despues de validar fuentes y alcances, con los asuntos contractuales marcados **PARA VALIDAR CON VALVERDE**.
