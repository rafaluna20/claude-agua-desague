# T-12 — Predimensionamiento del reservorio apoyado

**Estado:** ESCENARIO DE PREDIMENSIONAMIENTO PARA COMPARACIÓN. No es capacidad ni nivel operativo aprobados; requiere validación de demanda, curva horaria, fuente, modelo hidráulico, geotecnia y estructura antes de plano definitivo. La comparación D1–D3 está en `T-13_paso_4_alternativas_agua_desague.md`.

## Criterio de población y demanda adoptado

Para no dimensionar por debajo del horizonte urbano, se adopta un escenario conservador y explícito:

| Componente | Adopción | Población |
|---|---:|---:|
| Lotes ordinarios | 441 lotes × 1 vivienda × 6 hab/vivienda | 2,646 hab |
| Multifamiliar E01MZQ039P | 7 pisos × 2 viviendas/piso × 5 hab/vivienda | 70 hab |
| Predio PTAR y predio de referencia de fuente | Excluidos hasta confirmar su uso | 0 hab |
| **Población de prediseño** |  | **2,716 hab** |

Se usa **169 L/hab·día** únicamente como escenario de clima cálido: demanda media diaria = **459.004 m³/día**. La RM 107-2025-VIVIENDA establece dotaciones diferenciadas por clima, por lo que debe confirmarse el carácter climático en el expediente. [Fuente oficial MVCS](https://www.gob.pe/institucion/vivienda/normas-legales/6667128-107-2025-vivienda).

## Reservorio ensayado como escenario

**Escenario de reservorio apoyado de dos celdas, 500 m³ útiles en total**:

| Parámetro | Cota / valor preliminar |
|---|---:|
| Terreno en ubicación | 121.327 m |
| Fondo interior | 121.800 m |
| Nivel mínimo operativo | 122.300 m |
| Nivel máximo operativo / rebose | 124.300 m |
| Cierre de ingreso por alto nivel | 124.150 m |
| Coronación o intradós mínimo | 124.600 m |
| Profundidad útil entre Nmin y Nmax | 2.00 m |
| Volumen útil | 500 m³ |
| Número de celdas | 2 × 250 m³ útiles |
| Área interior total requerida | 250 m² |
| Referencia por celda | 12.5 m × 10.0 m interiores |

La separación en dos celdas permite limpiar o reparar una sin dejar sin agua a todo el proyecto. El volumen útil equivale a 1.09 días de la demanda conservadora; no sustituye las reservas regulatorias que correspondan si la entidad las exige.

## Control hidráulico preliminar

Con los niveles adoptados, la carga estática antes de pérdidas sería:

| Sector | Nmin | Nmax |
|---|---:|---:|
| Nodo vial más alto (110.273 m) | 12.027 m.c.a. | 14.027 m.c.a. |
| Nodo vial más bajo (78.316 m) | 43.984 m.c.a. | 45.984 m.c.a. |

Esto confirma que la zona alta es la crítica: el modelo debe limitar pérdidas para mantener servicio en condición de nivel mínimo. La zona baja exige comprobar presión máxima, clase de tubería y posible regulación por sectores.

Para llenar 459.004 m³/d se requiere, en promedio, 5.313 L/s si Santa María opera 24 h/d, 10.625 L/s si opera 12 h/d o 21.250 L/s si opera 6 h/d. La tubería declarada de 8 pulgadas parece geométricamente favorable, pero el caudal autorizado y la curva presión–caudal siguen siendo obligatorios antes de cerrar el diseño.

## Próximo cálculo

Construir el modelo EPANET con este reservorio y tres casos: nivel mínimo, nivel máximo y presión mínima de Santa María. Si la presión en zona alta no cumple o el llenado no logra el caudal requerido, se comparará refuerzo por bomba, cambio de cotas operativas o sectorización.
