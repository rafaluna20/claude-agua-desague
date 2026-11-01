# T-05: preparacion documental para el diseno de agua potable

**Fecha de corte:** 2026-10-10  
**Estado:** PRELIMINAR. No contiene calculos, seleccion de alternativa, diametros, cotas, presiones ni un modelo EPANET.  
**Alcance:** identificar insumos disponibles y bloqueos para el futuro diseno de la red mallada, reservorios, matriz por la Av. E y conexion de la Asociacion Santa Maria.  
**Responsable previsto de la fase:** `sanit-agua`.  
**Responsabilidad profesional:** todo criterio de diseno, factibilidad, documento de recepcion o definicion regulatoria queda **PARA VALIDAR CON VALVERDE** y con el ingeniero sanitario colegiado que se designe.

## 1. Conclusion de preparacion

Hay una base espacial congelada suficiente para preparar un trazado conceptual reproducible: calles, lotes, pasajes inferidos, poligonos rotulados `AGUA01`, `AGUA02` y `AVENIDA E`. No existe en los insumos revisados una base hidraulica suficiente para ejecutar ni cerrar un modelo: faltan la fuente decidida y su condicion de entrega, las cotas/volumen/operacion de los reservorios, topografia verificable para el modelo, demanda y criterios aprobados, y el as-built de la red existente.

Por ello T-05 puede preparar escenarios y una estructura de datos, pero no debe emitir un modelo definitivo ni cerrar la Puerta G1/G2 mientras estos faltantes sigan abiertos.

## 2. Evidencia confirmada y utilizable solo como entrada preliminar

| Hecho / insumo | Evidencia y ruta | Uso permitido ahora | Limite expreso |
|---|---|---|---|
| Base geometrica vigente | `W_contraste/datos/v3_48calles/MANIFIESTO.json`, congelado el 2026-10-09; `ESTADO.md` registra 48 calles y 1,341 lotes. | Identificar cobertura, conectividad potencial y nodos que deben definirse. | No contiene cotas de terreno, rasante ejecutada ni red de agua. |
| Huellas de los reservorios | `W_contraste/datos/v3_48calles/agua_import.json` contiene poligonos rotulados `AGUA01` (Reservorio 01) y `AGUA02` (Reservorio 02). S-010 registra sus ubicaciones de referencia. | Ubicar los activos en el plano base y solicitar sus fichas. | El archivo no aporta cota de fondo, nivel de agua, volumen, tuberias, bombeo, condicion operativa ni capacidad de fuente. |
| Corredor de la Av. E | `W_contraste/datos/v3_48calles/calle_import.json` contiene el elemento `AVENIDA E`; S-008 registra como decision del usuario que la matriz de agua vaya por su centro. | Reservar el corredor para desarrollar alternativas cuando se apruebe el diseno. | La geometria es un poligono vial, no una alineacion de tuberia, perfil ni cota. La matriz aun no esta dimensionada ni modelada. |
| Punto de conexion declarado | S-009 en `supuestos.md`: punto de agua con medidor a la derecha del lote `E01MZD155P`, Asociacion Santa Maria. | Registrar la consulta de campo/documental que debe fijar el punto. | S-009 indica expresamente que falta la coordenada exacta; tampoco hay cota, presion, caudal o documento de entrega. |
| Separacion con desague | S-008 y S-016 de `supuestos.md`; el plan exige coordinacion agua-desague. | Mantener una capa de interferencias para el futuro control geometrico. | El libro de normas T-02 debe confirmar criterios de agua y SEDAPAL; no se infiere una solucion de cruce desde esta preparacion. |
| Geometria complementaria | `parcels_export.json`, `calle_import.json`, `veredas_import.json`, `pasajes_inferidos.json` y `matriz_import.json` en `datos/v3_48calles/`. | Preparar la estructura de nodos/sectores y señalar lotes sin frente vial. | Los cinco pasajes son inferidos (S-012); no reemplazan su trazo oficial. |
| Rasante de trabajo existente | El manifiesto referencia `C:\\Users\\henry\\AppData\\Local\\Civil3DAgent\\exports\\unreal_pucusana\\Hd_final_calles48.npy`. S-015 lo identifica como rasante propia de diseno vial. | Mantenerlo separado como antecedente de trabajo. | S-015 declara que no es rasante ni as-built ejecutado; no usarlo como elevacion de nodos EPANET ni para obra. |
| Documentos topograficos ubicados | `A_EXPEDIENTE_HU/A0_Comun/2_Estudios_Basicos/02.01_Topografia/`: `Memoria_Descriptiva/Informe Topografico.pdf`, `Planos_Topograficos/TP-01.pdf`, `TP-02.pdf`, `TP-03.pdf`, `UL-01.pdf` y dos imagenes de BMs. | Son candidatos para recuperar control vertical y superficies, previa verificacion. | La memoria `.md` disponible es una plantilla con campos `[Completar]`; no acredita por si misma cotas, datum, BMs ni un MDT apto para calculo. Se requiere revision del topografo y archivo fuente. |

La integridad de los datos `v3_48calles` se controla con los hashes de su `MANIFIESTO.json`. Cualquier nueva exportacion debe versionarse; no se modifica esta entrada congelada.

## 3. Antecedentes alegados o contradictorios: no son datos de modelo

| Afirmacion | Fuente | Estado para T-05 | Accion previa al uso |
|---|---|---|---|
| Parte 1 se abasteceria con la Asociacion Santa Maria y Parte 2 con SEDAPAL. | `TL-GES-007_2026-10-04_Esquema_Entrega_Dos_Partes.md`. | Propuesta de Rafael, **POR VALIDAR**; el propio documento advierte que la division geografica no coincide necesariamente con las etapas. | Fijar poligono P1/P2 y obtener la factibilidad o convenio vigente. **PARA VALIDAR CON VALVERDE.** |
| Existiria un convenio o factibilidad de la Asociacion para etapas 1 y 2. | Respuestas registradas en `TL-GES-007`. | Alegado; el mismo archivo dice que el documento esta por revisar y no se hallo en la revision. | Obtener copia integra, vigencia, alcance territorial, obligaciones y criterios de aceptacion. |
| SEDAPAL seria alternativa o receptor para parte del proyecto. | `TL-TEC-001_2026-10-03_Alerta_Documentos_Contradictorios.md`, `TL-TEC-004_2026-03-02_Estrategia_Santa_Maria.md`, `TL-TEC-005_2026-03-02_Rol_Intervencion_SEDAPAL.md`. | Los documentos se contradicen; S-006 permanece PENDIENTE. | Definir el esquema de servicio mediante carta de factibilidad vigente y validacion legal/técnica. **PARA VALIDAR CON VALVERDE.** |
| La red de S&G existe en Parte 1 y presenta posibles cruces/informacion de PN. | `SUSTENTO_TECNICO_contratista.md`, `TL-GES-009_2026-10-04_Verificacion_Informe_No_Conformidad.md` y T-03. | Antecedente para contraste, no geometria hidraulica confiable. | Esperar inventario T-03, as-built, protocolos, certificados y levantamiento georreferenciado. |
| Los parametros de poblacion, dotacion y caudales de documentos anteriores permiten disenar. | `TL-TEC-003_2026-03-02_Calculo_Caudales_Estimados.md`. | Referencia historica; sus supuestos difieren de S-003 y S-004 actuales. | El ingeniero sanitario debe aprobar demanda, horizonte y factores antes de cargarlos a EPANET. |

## 4. Datos faltantes y efecto en el diseno

| Grupo | Dato faltante concreto | Para que se necesita | Responsable sugerido / puerta |
|---|---|---|---|
| Esquema de servicio | Decision documentada Asociacion/SEDAPAL y alcance espacial P1/P2. | Determina fuente, fronteras, receptor y escenarios. | Rafael + responsable tecnico; **PARA VALIDAR CON VALVERDE**. G1. |
| Factibilidad de la fuente | Carta/convenio vigente, punto de entrega georreferenciado, cota, presion estatica y residual, caudal o curva disponible, calidad, continuidad, restricciones y titularidad. | Definir la condicion de borde del modelo; sin ello no existe fuente EPANET valida. | Asociacion o SEDAPAL, segun esquema; G1. |
| Reservorios AGUA01/02 | Levantamiento de cota de fondo, rebose, niveles minimo/maximo/inicial, volumen-curva, interconexion, valvulas, tuberias, equipos, fuente electrica y regimen de operacion. | Modelar tanque/reservorio, carga disponible y operacion. | Topografo + operador/proyectista; G1/G2. |
| Topografia y datum | MDT/TIN o puntos con cota, metadatos de datum horizontal/vertical, BMs, fecha/precision y rasantes definitivas o as-built. | Asignar elevaciones a nodos, revisar presiones y coordinar cruces. | Topografo; G1. |
| Demanda aprobada | Lotes efectivamente atendidos, poblacion, dotacion, consumos no domesticos/riego/incendio si aplican, factores, patron horario y horizonte. | Definir demandas nodales y escenarios. | Ingeniero sanitario tras T-02 y decisiones S-001, S-003, S-004, S-011; G1. |
| Criterios tecnicos | Texto y numeral verificados de OS.050, IS.010, criterios de receptor y especificaciones aplicables a agua; metas de presion, velocidad, material, PN, recubrimiento y pruebas. | Definir restricciones y controles de aceptacion. | `sanit-normas` + ingeniero sanitario; G1. |
| Red existente | Planos de replanteo/as-built, inventario de tramos, accesorios, diametros, material/PN, cotas, pruebas y fotos georreferenciadas. | Separar red a proyectar de activos existentes y preparar contraste. | S&G, supervision, Asociacion; T-03/G1. |
| Derecho de via y trazos | Secciones viales, veredas, pasajes oficiales, predios/servidumbres, interferencias y poligono definitivo de Parte 1. | Convertir geometria vial en corredores de tuberia y evitar invadir predios. | Civil/topografia/Valverde; G1. |
| Operacion y resiliencia | Sectorizacion, valvulas, medicion, bombeo, energia, almacenamiento, emergencia, contra incendio y protocolo de calidad. | Definir escenarios operativos y elementos modelables. | Operador previsto + ingeniero sanitario; G2. |

## 5. Contrato minimo de entradas para iniciar el modelo EPANET

El futuro archivo EPANET debe construirse desde un paquete versionado, con tabla de procedencia por cada valor. Este es el contrato minimo; una casilla sin fuente se marca `PENDIENTE`, no se rellena.

| Paquete | Campos minimos | Fuente aceptable |
|---|---|---|
| Control y referencia | Version de geometria, sistema de coordenadas/datum, datum vertical, fecha de levantamiento, responsable y hashes. | Manifiesto + topografia certificada. |
| Nodos de demanda | ID unico, coordenada, elevacion, sector/P1-P2, categoria de consumo, demanda base aprobada y patron. | Base geometrica + topografia + memoria de demanda aprobada. |
| Fuente | Tipo de fuente, titular/operador, punto exacto, carga o presion/curva por horario, caudal disponible, continuidad y calidad. | Factibilidad/convenio vigente y medicion o informacion firmada del proveedor. |
| Reservorios/tanques | ID, coordenada, elevacion de fondo y rebose, niveles operativo minimo/maximo/inicial, volumen o curva nivel-volumen, conexiones y controles. | Planos/as-built y levantamiento; ficha del operador. |
| Tuberias y accesorios proyectados | ID, nodo inicial/final, alineacion, longitud, diametro, material/rugosidad, clase/PN, estado, valvulas, bombas y controles. | Salida del diseno preliminar aprobada; no de una alegacion de obra. |
| Escenarios de demanda y operacion | Horizonte, patrones horarios/estacionales, simultaneidad, condicion de incendio o emergencia si corresponde, curvas de bomba y programacion de controles. | Criterios normativos verificados + operador/proyectista. |
| Coordinacion sanitaria | Cotas de red de desague, cruces, recubrimientos, separaciones y condicion de pasajes. | Diseno coordinado, topografia y libro de normas verificado. |
| Control de calidad | Casos de prueba, resultados, version de software, archivo de entrada, log, revisor independiente y trazabilidad de cambios. | Equipo de diseno y revisor; requisito para G2/G4. |

Este contrato no fija ningun valor de diseno. La seleccion de elementos, calibres y alternativas corresponde al calculista y al ingeniero sanitario.

## 6. Preguntas que deben resolverse antes de modelar

1. ¿Que lotes exactos recibiran agua en la primera etapa de diseno y cual es el poligono P1/P2 aprobado?
2. ¿La fuente de la red sera la Asociacion Santa Maria, SEDAPAL u otra configuracion? Entregar el documento que lo sustenta. **PARA VALIDAR CON VALVERDE.**
3. ¿Donde esta, en coordenadas y cota, el punto de entrega junto a `E01MZD155P`; que medidor, presion, caudal y continuidad garantiza el proveedor?
4. ¿AGUA01 y AGUA02 son reservorios construidos, proyectados o solo reservas de terreno? Entregar planos y datos operativos.
5. ¿Que BM, datum vertical, MDT y rasantes son los vigentes para el proyecto y cuales representan lo ejecutado?
6. ¿Que poblacion, dotacion, factores, horizonte y demandas especiales aprueba el ingeniero sanitario para cada sector y multifamiliar?
7. ¿Cuales son los criterios escritos de aceptacion de la Asociacion, incluidas clases de tuberia, pruebas, medicion y transferencia? **PARA VALIDAR CON VALVERDE.**
8. ¿Que infraestructura de agua se ejecuto realmente por S&G y donde estan sus as-built, protocolos, certificados y fotografias georreferenciadas?
9. ¿Cuales son las secciones viales, pasajes y servidumbres definitivas, especialmente donde S-012 mantiene trazos inferidos?
10. ¿Que niveles y trazos de desague aprobados deben coordinarse con la matriz de agua y las conexiones prediales?

## 7. Puertas de continuidad

### Puerta G1: habilitar el diseno preliminar

No cerrar G1 hasta que, como minimo:

- T-02 entregue los criterios de agua con fuente y numeral verificados.
- T-03 separe la red ejecutada alegada de la verificada y declare la ausencia o presencia de as-built.
- El responsable tecnico resuelva S-001, S-003, S-004, S-006, S-011, S-012, S-013, S-015, S-017 y S-019 que afecten la coordinacion.
- Se designe el ingeniero sanitario revisor y se confirme el esquema de fuente/receptor. **PARA VALIDAR CON VALVERDE** en lo legal y regulatorio.
- Se reciba, o se declare formalmente inexistente, la informacion minima de fuente, reservorios y topografia de la seccion 5.

### Puerta G2: emitir un diseno preliminar coordinado

Solo despues de G1, `sanit-agua` podra elaborar alternativas rotuladas `PRELIMINAR`, el archivo EPANET reproducible y su memoria de calculo. Antes de G2 debe verificarse que la red de agua se coordine con desague, pasajes inferidos, recubrimientos y cruces; ningun resultado sustituye el contraste as-built ni la firma profesional.

## 8. Archivos principales localizados

- `B_GESTION_INTERNA/B3_Analisis_Tecnicos/Agua_y_Alcantarillado/W_contraste/datos/v3_48calles/MANIFIESTO.json`
- `B_GESTION_INTERNA/B3_Analisis_Tecnicos/Agua_y_Alcantarillado/W_contraste/datos/v3_48calles/agua_import.json`
- `B_GESTION_INTERNA/B3_Analisis_Tecnicos/Agua_y_Alcantarillado/W_contraste/datos/v3_48calles/calle_import.json`
- `B_GESTION_INTERNA/B3_Analisis_Tecnicos/Agua_y_Alcantarillado/W_contraste/datos/v3_48calles/{parcels_export,veredas_import,pasajes_inferidos,matriz_import}.json`
- `B_GESTION_INTERNA/B3_Analisis_Tecnicos/Agua_y_Alcantarillado/W_contraste/{supuestos,ESTADO}.md`
- `B_GESTION_INTERNA/B3_Analisis_Tecnicos/Agua_y_Alcantarillado/TL-TEC-001_2026-10-03_Alerta_Documentos_Contradictorios.md`
- `B_GESTION_INTERNA/B3_Analisis_Tecnicos/Agua_y_Alcantarillado/TL-TEC-015_2026-10-09_Plan_Diseno_Contraste.md`
- `B_GESTION_INTERNA/B1_Gestion/04.01_Plan_Ejecucion/TL-GES-007_2026-10-04_Esquema_Entrega_Dos_Partes.md`
- `B_GESTION_INTERNA/B1_Gestion/04.01_Plan_Ejecucion/TL-GES-009_2026-10-04_Verificacion_Informe_No_Conformidad.md`
- `obra agua y desague/SUSTENTO_TECNICO_contratista.md`
- `A_EXPEDIENTE_HU/A0_Comun/2_Estudios_Basicos/02.01_Topografia/Memoria_Descriptiva/Informe Topografico.pdf`
- `A_EXPEDIENTE_HU/A0_Comun/2_Estudios_Basicos/02.01_Topografia/Planos_Topograficos/{TP-01,TP-02,TP-03,UL-01}.pdf`

Las rutas anteriores son inventario documental, no certificacion de contenido tecnico. La recuperacion de planos fuente, metadatos y firmas sigue pendiente.

## 9. Actualizacion de coordinacion 2026-10-10

El usuario definio que el expediente usa `datos/v4_primera_expediente/`: 444 lotes dentro del limite `00_primera_expediente`; E01MZS002P es caso de borde y queda fuera del calculo hasta decision expresa. La fuente sera la Asociacion Santa Maria, con referente espacial a la derecha de E01MZD155P; faltan las condiciones de borde medibles/documentadas. La PTAR se ubicara en E03MZD049P, pero tendra expediente independiente; este modelo solo coordinara el punto de llegada.

El programa urbano confirmado es hasta 3 pisos mas azotea para lotes ordinarios, y 5 a 7 pisos para multifamiliares con area >=300 m2. La geometria identifica E01MZQ039P y E01MZD155P como candidatos residenciales por area, mientras E03MZD049P es PTAR y no debe cargarse como poblacion. Quedan pendientes unidades, dormitorios, habitantes por unidad, dotacion, topografia/datum, reservorios y factibilidad para iniciar EPANET.
