---
name: igor-builder
description: Crea un repositorio nuevo en GitHub o GitLab tras preguntar nombre, lenguaje y proveedor, con EditorConfig, Prettier, pre-commit, CI de calidad y seguridad en cada push y release GitFlow preparado pero deshabilitado. Úsalo para inicializar repositorios; no para modificar proyectos existentes salvo petición expresa.
---

# Crear repositorio

Habla en el idioma del usuario. Este skill puede ejecutarse desde Codex o Claude Code, en un entorno que disponga de archivos, ejecución y acceso autenticado al proveedor. Utiliza el plugin/conector Git disponible para las operaciones remotas; si no lo hay, usa `gh` para GitHub o `glab` para GitLab cuando estén disponibles y autenticados. No inventes nombres de plugins ni herramientas. El skill define el flujo; el conector o CLI realiza las acciones.

## Recoger los datos

Pregunta juntos los datos faltantes, sin volver a pedir respuestas ya dadas:

1. Nombre del repositorio.
2. Lenguaje o lenguajes de programación; framework o gestor si ya los conoce.
3. GitHub o GitLab.

Si no se han indicado, incluye en esa misma consulta propietario/organización/grupo (puede ser la cuenta personal autenticada) y visibilidad (privado por defecto). Pregunta el host si el usuario elige una instancia propia. No pidas que pegue credenciales en el chat. Comprueba identidad y destino antes de escribir. Resuelve versiones y herramientas mediante documentación oficial actual; no uses versiones `latest` sin fijarlas.

Con esas respuestas, la petición de crear el repositorio autoriza su creación y el push inicial. Continúa sin pedir una confirmación redundante, sujeto a los permisos reales del entorno. Un nombre ocupado no autoriza sobrescribir un proyecto: pide otro nombre o autorización para trabajar en el existente.

## Preparar y comprobar

Genera primero un proyecto mínimo en una carpeta nueva y revisable. No inicialices el directorio actual si contiene otro proyecto. Lee [la base común](references/base.md), [los toolchains por tecnología](references/tech.md) y solamente [GitHub](references/github.md) o [GitLab](references/gitlab.md), según la elección.

Adapta herramientas al lenguaje sin crear una aplicación completa. Incluye:

- README con instalación, comandos de checks, funcionamiento de CI y flujo GitFlow.
- `.gitignore`, `.editorconfig`, `.prettierrc.json`, `.prettierignore` y `.pre-commit-config.yaml`.
- Manifiesto y lockfile del ecosistema, fuente mínima y una prueba de humo cuando el lenguaje lo permita.
- Configuración real de formato, lint, tests/typecheck o compilación, escaneo de secretos, SAST y auditoría de dependencias.
- Pipeline activo que ejecute todos esos checks en **cada push a cualquier rama** y también en pull/merge requests.
- Plantilla de release completa y sintácticamente válida en `ci/templates/`, sin conexión con los pipelines activos.

Prettier formatea Markdown/JSON/YAML y los lenguajes que soporte; usa el formateador nativo para los demás. En un proyecto sin Node, aísla Prettier como herramienta de desarrollo, con su manifiesto y lockfile, y documenta esa dependencia. No simules soporte de Prettier para un lenguaje incompatible.

Ejecuta los comandos que CI ejecutará y valida su YAML/configuración con las herramientas disponibles. Corrige fallos antes del push. Comprueba que las rutas, versiones, locks y scripts existen, que cada check puede fallar de verdad y que ningún filtro omite ramas. No uses `echo`, `|| true`, `continue-on-error` ni `allow_failure` para disfrazar controles. Si falta acceso a red, herramientas o runners, conserva lo generado y comunica qué validación quedó pendiente; no declares CI verde sin evidencia.

## Crear y entregar

Después de validar localmente, comprueba que el destino remoto no existe, crea el repositorio con la visibilidad acordada, configura `origin`, crea el commit inicial y publica `main` y `develop`. Usa `main` como rama predeterminada, salvo indicación distinta. No añadas una licencia elegida unilateralmente. No publiques tokens ni habilites releases, despliegues o protecciones adicionales por defecto.

Ante un timeout al crear el remoto, consulta el estado antes de reintentar para evitar duplicados. Si una fase falla, conserva el trabajo y reanuda desde el estado comprobado; no borres el remoto ni fuerces pushes para arreglarlo. Si falta autenticación, completa los archivos locales y pide conectar el proveedor para terminar. No sustituyas el proveedor elegido.

Comprueba ambas ramas remotas y la ejecución de CI del push inicial cuando sea accesible. Entrega enlace del repositorio, ubicación local, lenguaje/herramientas, resultado real de validación/CI y ruta de la plantilla inactiva. Distingue controles configurados de controles ejecutados. No afirmes bloqueo de merges sin una regla de protección configurada.
