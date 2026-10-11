# Colaboración de agentes — Expediente Terra Lima

- Antes de editar, leer `00_REGLAS_DE_DOCUMENTOS.md`, `00_INDICE_MAESTRO.md` y `docs/ai/LESSONS.md`. Para documentos codificados, consultar y actualizar `00_REGISTRO_MAESTRO.md` según sus reglas.
- `A_EXPEDIENTE_HU/` contiene documentación presentable; `B_GESTION_INTERNA/` es interna. No promover borradores, cifras no verificadas ni originales modificados a A.
- La fuente canónica de skills del proyecto es `.agents/skills/`. Promover solo procedimientos revisados; no copiar conversaciones, observaciones crudas, credenciales ni datos personales.
- Declarar fuente, fecha y estado de cada dato técnico. Marcar los supuestos y someter cálculos y documentos del expediente a revisión independiente antes de tratarlos como finales.
- Claude y Codex no deben editar simultáneamente el mismo archivo. Antes de trabajar, revisar `git status`; acordar archivos a cargo. Hacer el relevo mediante un commit local y comunicar su hash y pendientes. Para trabajo paralelo, usar worktrees separados.
- En esta PC, el directorio y `.git` pueden tener propietarios Windows distintos. Si Git informa `dubious ownership`, usar por comando `git -c safe.directory=<ruta absoluta de este repositorio> ...`; nunca confiar en `*` ni cambiar la configuración global sin autorización.
- Este repositorio y el proyecto Unreal son independientes. No asumir que un commit aquí incluye modelos, exports o assets de Unreal.
