# Releases

Este archivo contiene las notas que el workflow publica para cada versión. La versión debe coincidir en los manifiestos de Codex, Claude Code y `package.json`. Las releases existentes no se sobrescriben.

## 1.0.1

- Renombrado el plugin a `igor-builder`.
- Añadido soporte de toolchain para Go, OpenTofu, Docker, Argo CD, Argo Workflows, Kubernetes, Helm, Nix, PHP, Ruby, Swift, Bash, Pulumi y Jenkins en `references/tech.md`.
- Config de Prettier migrada de JSON a YAML (`.prettierrc.yaml`).
- Añadido commitlint con Conventional Commits (`.commitlintrc.yaml`) y hook `commit-msg` en pre-commit.
- Release workflow disparado desde rama `release/v*` en lugar de tags.
- Añadidos `LICENSE` (MIT), `CONTRIBUTING.md` y `CODE_OF_CONDUCT.md`.

## 1.0.0

- Skill compartido para Codex y Claude Code.
- Creación de repositorios GitHub o GitLab tras preguntar nombre, lenguaje y proveedor.
- EditorConfig, Prettier, pre-commit y controles de calidad, lint y seguridad en cada push.
- Preparación de ramas main/develop y release GitFlow deshabilitado para los repositorios generados.
- Distribución del plugin como ZIP con checksum SHA-256.

## Proceso GitFlow

1. Desarrolla en `feature/*` desde `develop` y abre un PR hacia `develop`.
2. Crea `release/X.Y.Z` desde `develop`; actualiza los tres manifiestos y añade aquí un encabezado `## X.Y.Z` con notas reales. Si cambia `package.json`, actualiza también `package-lock.json` con `npm install --package-lock-only`.
3. Ejecuta los checks y abre un PR de la rama de release hacia `main`.
4. Después del merge y con CI aprobado, crea el tag en el commit de main:

   ```sh
   git switch main
   git pull --ff-only origin main
   git tag -a v1.0.0 -m "Release 1.0.0"
   git push origin v1.0.0
   ```

   Sustituye `1.0.0` por la versión correspondiente. El tag debe coincidir exactamente con los manifiestos y apuntar a un commit incluido en `main`.

5. GitHub Actions vuelve a ejecutar los checks, empaqueta el plugin y sube el ZIP y `SHA256SUMS` a GitHub Releases usando su token integrado. No requiere un PAT ni publica automáticamente en directorios de plugins.
6. Abre un PR de `main` hacia `develop` para sincronizar la versión publicada. Para un hotfix, crea `hotfix/X.Y.Z` desde main y luego integra en ambas ramas.

En GitHub deben estar habilitados Actions y los permisos de escritura del token para el job de release. Para recuperar un fallo, vuelve a ejecutar el workflow del mismo tag; si la release ya existe, inspecciónala antes de actuar. No muevas tags publicados ni borres releases como parte de un reintento.
