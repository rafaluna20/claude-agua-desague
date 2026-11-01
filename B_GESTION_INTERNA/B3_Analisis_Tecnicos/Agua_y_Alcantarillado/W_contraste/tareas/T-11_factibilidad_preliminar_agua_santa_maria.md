# T-11 — Factibilidad preliminar de agua: Santa María → reservorio → Primera Expediente

**Dictamen:** **ACEPTABLE PARA PREDISEÑO; NO APTA AÚN PARA DISEÑO DEFINITIVO NI FIRMA.**

## Datos disponibles y trazables

| Elemento | Dato |
|---|---:|
| Medidor general Santa María | X=308466.605; Y=8622891.887; terreno TIN=101.526 m |
| Tubería existente | 8 pulgadas (declarada por usuario) |
| Presión disponible | 30 m.c.a. declarados; no se conoce si es estática o residual ni su variación horaria |
| Reservorio proyectado | X=308358.792; Y=8622860.911; terreno TIN=121.327 m |
| Distancia en planta entre puntos | 112.175 m |
| Desnivel de terreno hacia reservorio | +19.801 m |
| Margen terreno/presión referencial | 10.199 m antes de pérdidas, nivel de agua y accesorios |
| Nodo vial más alto de la red | 110.273 m (`NV-0070`) |
| Nodo vial más bajo de la red | 78.316 m (`NV-0061`) |

Fuentes: `datos/v4_primera_expediente/agua/condicion_borde_santa_maria_v1.json` y `topografia/grafo_vial_cotas_terreno_v1.json`.

## Juicio técnico

1. **Llenado del reservorio:** topográficamente es posible estudiar el llenado directo desde Santa María. Comparando sólo terrenos, la presión declarada deja 10.199 m de margen. No basta para garantizar el llenado: la comparación hidráulica correcta es entre la carga residual en el eje de la tubería del medidor y el nivel máximo de agua del reservorio, más las pérdidas de la aducción.
2. **Distribución por gravedad:** la cota de terreno del reservorio supera al corredor vial más alto en 11.054 m. Es una base razonable para prediseñar una red gravitacional, pero el sector alto será crítico cuando se incluyan pérdidas y el nivel mínimo operativo del reservorio.
3. **Zona baja:** la diferencia de terreno hasta el nodo más bajo es 43.011 m antes de sumar la altura del agua del reservorio. Se debe verificar la presión estática máxima y la clase de tubería; podría ser conveniente sectorizar o regular presión según el resultado del modelo.
4. **Longitud real:** los 112.175 m son distancia entre coordenadas; no son la longitud de aducción. El trazo final debe seguir un corredor autorizado, evitar lotes y cuantificar accesorios, cruces y pérdidas.

## Propuesta de mejora

- Modelar dos sistemas vinculados: **aducción de llenado Santa María–reservorio** y **red de distribución desde reservorio**. No usar la presión de Santa María como si fuera directamente la presión garantizada de todos los lotes.
- Definir las cotas de nivel mínimo, máximo y rebose del reservorio antes de fijar su altura. Elevar excesivamente el nivel mejora presión en red, pero reduce el margen de llenado desde Santa María.
- Ejecutar una prueba autorizada de presión–caudal en el medidor: presión estática; presión residual para caudales conocidos; continuidad durante el día; diámetro interior, material y válvulas existentes.
- Trazar la aducción por vialidad o servidumbre formal y levantar un perfil longitudinal; no adoptar la recta geométrica del plano como tubería.
- En EPANET, evaluar al menos nivel mínimo/máximo del reservorio, presión mínima de Santa María y escenarios de demanda. El resultado decidirá si basta alimentación directa, si se requiere bomba de refuerzo o si se necesita válvula reguladora/zona de presión.

## Datos que impiden cerrar el diseño

- Caudal autorizado y curva presión–caudal de Santa María.
- Continuidad del servicio y condiciones de operación.
- Cota del eje de la tubería y material/diámetro interior de los 8 pulgadas.
- Capacidad, dimensiones y niveles operativo mínimo/máximo del reservorio.
- Población, unidades de vivienda, dotación y horizonte de diseño.
- Trazado autorizado de aducción y documento de datum vertical.
