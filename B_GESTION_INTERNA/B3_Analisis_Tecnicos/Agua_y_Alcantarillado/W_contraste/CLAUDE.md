# W_contraste — diseño de contraste de agua y desagüe (Terra Lima / Pucusana)

Hereda el `CLAUDE.md` de la raíz del expediente (`AGENTS.md`, `00_REGLAS_DE_DOCUMENTOS.md`, `docs/ai/LESSONS.md`). Este archivo solo agrega lo propio de esta carpeta. Las reglas completas están en `LEEME.md`.

## Al empezar una sesión
1. Lee `ESTADO.md` (una página) y di en qué quedamos antes de proponer trabajo.
2. Si vas a usar un supuesto, búscalo en `supuestos.md`; si vas a usar una norma, en `normas/libro_normas.md`.
3. Revisa `git status` antes de editar (Claude y Codex no editan el mismo archivo a la vez). Git en este equipo:
   `git -c safe.directory=C:/Users/henry/OneDrive/Escritorio/exp.-terraLima_v2 <comando>` (nunca `safe.directory=*`).

## Reglas que no se negocian
- **Normas:** toda cifra normativa se cita con norma y numeral, leída del texto original (RNE OS.050/OS.070/IS.010, SEDAPAL CTPS-PR-02). Lo que no se pudo verificar se marca `NO VERIFICADO`. Una respuesta de NotebookLM o mi memoria no son fuente: contrastar con el texto. (Lección: el piso de DN110 era mío; SEDAPAL CTPS-PR-02 Art. 8.1.4 exige DN90.)
- **Números:** salen de scripts reproducibles con parámetros que llevan valor, fuente y estado. Nunca de redacción libre. Agua: `scripts/agua_potable/` + `datos/parametros_agua_potable_v1.json` (skill `calculo-agua-potable-terralima`). Desagüe: skill `diseno-desague-pucusana`.
- **Datos de entrada congelados:** `datos/` no se edita. Si cambia un dato, se crea una versión nueva (`vN_...`) y se dice qué resultados quedan desactualizados.
- **Cada dato técnico** declara fuente, fecha y estado. Los supuestos míos se registran como `PENDIENTE` en `supuestos.md`; no se vuelven definitivos solos.
- **Alcance de escritura:** solo dentro de esta carpeta. Odoo y Civil 3D en solo lectura (los cambios masivos en Odoo se hacen aparte, con lista exacta y respaldo).
- **Lo legal o de firma:** marcar `PARA VALIDAR CON VALVERDE`. Nada de aquí es expediente presentable hasta la firma de un ingeniero sanitario colegiado.
- **Revisión independiente (`sanit-revisor`):** solo cuando el usuario diga que el proyecto está completo. No lanzarla por tramos.
- **Nombres de archivo** sin tildes ni espacios, rutas de máximo 200 caracteres.

## Antes de dar algo por hecho
- Una corrida nueva va en carpeta nueva (`resultados/v3_agua/cNN_fecha`); no se sobreescriben corridas anteriores.
- Después de correr: `python scripts/agua_potable/pruebas.py` (deben pasar todas).
- Un DXF/DWG exportado no está validado hasta abrirlo en Civil 3D.
- Al cerrar la sesión: actualizar `ESTADO.md` (fase, próximas acciones, bloqueos), ofrecer el commit local con su hash y los pendientes.
