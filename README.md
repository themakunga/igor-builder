# igor-builder

> *"Could be worse. Could be raining."* — Igor

Plugin con un skill compartido para Codex y Claude Code que te ayuda a crear tus propios monstruos: repositorios GitHub o GitLab con una base de calidad, lint, seguridad y GitFlow deshabilitado.

El skill pregunta nombre, lenguaje/stack y proveedor Git; resuelve propietario y visibilidad. Usa el conector del proveedor o los CLI autenticados `gh`/`glab`. No incluye credenciales ni un servidor MCP propio.

## Stacks soportados

| Categoría | Tecnologías |
|---|---|
| **Lenguajes** | Go · TypeScript · JavaScript · Python · PHP · Ruby · Swift · Bash |
| **Frontend** | Vue.js · Nuxt.js · Node.js · Express.js |
| **IaC** | Terraform · OpenTofu · Pulumi |
| **Contenedores** | Docker · Kubernetes · Helm · Kustomize |
| **GitOps** | Argo CD · Argo Workflows |
| **Plataformas** | Nix · NixOS · Jenkins (Jenkinsfile) |
| **Cloud** | AWS · GCP · Heroku |
| **Bases de datos** | PostgreSQL · MySQL · MongoDB · Redis · Firebase |

Cada stack incluye formato, lint, tests, SAST y auditoría de dependencias adaptados; consulta [`skills/igor-builder/references/tech.md`](skills/igor-builder/references/tech.md) para las herramientas exactas por tecnología.

---

## Instalación

### Claude Code — desde el repositorio local

```sh
git clone <url-de-este-repo> igor-builder
claude --plugin-dir /ruta/absoluta/igor-builder
```

### Claude Code — desde un ZIP descargado

Descarga el ZIP de la última release, descomprímelo en cualquier carpeta y apunta `--plugin-dir` a esa carpeta:

```sh
unzip igor-builder-v<version>.zip -d igor-builder
claude --plugin-dir /ruta/absoluta/igor-builder
```

### Codex

En Codex instala el plugin vía la interfaz de plugins o añade la ruta del directorio/ZIP como fuente local. El manifiesto `.codex-plugin/plugin.json` se detecta automáticamente.

---

## Uso

### Claude Code

Una vez iniciado Claude Code con `--plugin-dir`, invoca el skill con cualquiera de estas formas:

```
/igor-builder:igor-builder
```

```
Usa igor-builder para crear un repositorio llamado my-api en Go, en GitHub, privado.
```

El skill pregunta los datos que falten (nombre, lenguaje, proveedor, propietario, visibilidad) y no vuelve a pedir lo que ya indicaste.

### Codex

```
Usa $igor-builder para crear un repositorio llamado my-api.
```

---

## Qué genera el skill

Para cada proyecto crea localmente y luego publica en el proveedor elegido:

- `README.md` con instalación, comandos de checks y flujo GitFlow
- `.editorconfig`, `.prettierrc.json`, `.prettierignore`, `.gitignore`
- `.pre-commit-config.yaml` con hooks de formato, lint, secretos y YAML
- Manifiesto y lockfile del ecosistema, fuente mínima y prueba de humo
- Pipeline activo (GitHub Actions o GitLab CI) que ejecuta todos los checks en cada push y en PR/MR
- Plantilla de release inactiva en `ci/templates/` (nunca conectada al pipeline inicial)
- Ramas `main` y `develop` publicadas en el remoto

No genera licencia, no habilita releases ni deploys, no añade protecciones de ramas.

---

## Desarrollo y validación

Requisitos: Python 3.13, Node.js 22, Git y Go compatible con Gitleaks.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
npm ci
pre-commit install
pre-commit run --all-files
npm audit --audit-level=low
pip-audit -r requirements-dev.txt
python scripts/check_plugin.py --package
```

`npm run format` corrige el formato; `npm run format:check` solo lo verifica. El ZIP de distribución se genera en `dist/` con los manifiestos en la raíz, el skill, sus referencias y documentación. No contiene dependencias de desarrollo.

---

## CI y releases

CI se ejecuta en cada push a cualquier rama y en pull requests, sin filtros. Verifica formato, YAML/JSON, workflows, coherencia de versiones, referencias, SAST, secretos y dependencias (incluyendo historial).

El workflow `release.yml` de **este plugin** está habilitado para tags `vX.Y.Z` y publica el ZIP en GitHub Releases. Consulta [`release.md`](release.md) para el proceso GitFlow y permisos. Las plantillas de release que el skill genera en otros repositorios permanecen deshabilitadas hasta que el usuario las activa.

Distribuido bajo la [licencia MIT](LICENSE). Las contribuciones se rigen por las guías en [CONTRIBUTING.md](CONTRIBUTING.md) y el [Código de Conducta](CODE_OF_CONDUCT.md).
