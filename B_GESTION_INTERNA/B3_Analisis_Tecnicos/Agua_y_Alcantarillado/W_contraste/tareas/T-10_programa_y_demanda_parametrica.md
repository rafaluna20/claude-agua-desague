# T-10 — Programa urbano y demanda paramétrica de Primera Expediente

**Estado:** PREPARACIÓN HECHA. No contiene población adoptada ni caudales de diseño.

## Base preparada

La clasificación se generó sobre los 444 lotes `DENTRO` y la asociación vial vigente:

| Categoría | Lotes | Tratamiento actual |
|---|---:|---|
| Vivienda ordinaria paramétrica | 441 | Regla urbana: hasta 3 pisos más azotea; faltan unidades y habitantes. |
| Multifamiliar condicional | 1 (`E01MZQ039P`) | Área >=300 m²; regla urbana: 5 a 7 pisos; faltan unidades y habitantes. |
| Uso pendiente junto a Santa María | 1 (`E01MZD155P`) | Área >=300 m², pero no se presupone uso residencial porque referencia la fuente. |
| Infraestructura PTAR | 1 (`E03MZD049P`) | Excluida de demanda residencial; el expediente de PTAR es independiente. |
| Acceso pendiente de servidumbre | 4 | No se asigna red definitiva hasta resolver S-019. |

## Archivo vigente

- `datos/v4_primera_expediente/demanda/programa_lotes_parametrico_v1.json`
  - SHA-256: `B3471674BA4F0CA10C5A4BFE53AB48E1A05EA257839922B8543D1959671FF9A8`
  - deja nulos, de forma intencional: unidades de vivienda, habitantes, población, demanda de agua y aporte de desagüe.

## Puerta antes del cálculo hidráulico

El responsable técnico debe adoptar y registrar:

1. Unidades por lote ordinario y por multifamiliar (o tipologías equivalentes por manzana).
2. Habitantes por unidad, ocupación y horizonte de diseño.
3. Dotación, coeficientes de variación y retorno a desagüe aprobados.
4. Uso final de `E01MZD155P`.
5. Solución de acceso/servidumbre de `E01MZQ055P`, `E01MZQ056P`, `E01MZQ064P` y `E01MZQ065P`.

Con esos datos, las fórmulas trazables son: `P = unidades × habitantes`; `Q agua = P × dotación`; `Q desagüe = Q agua × retorno + aporte no doméstico`.
