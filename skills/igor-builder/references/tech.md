# Toolchains por tecnología

Lee esta referencia junto con `base.md`. Para cada tecnología elige la herramienta señalada; verifica soporte oficial antes de generar archivos. No instales ni menciones herramientas que no cubran el stack declarado.

---

## Lenguajes

### Go
- **Formato/lint:** `gofmt -w` y `go vet ./...`; usa `golangci-lint run` fijando versión en `.golangci.yml`. No uses `golint` (deprecado).
- **Tests:** `go test ./... -race -coverprofile=coverage.out`.
- **Seguridad:** `govulncheck ./...` para código; `go mod tidy && git diff --exit-code` para módulos limpios. No hay auditor de dependencias nativo adicional; aplica trivy en el artefacto final si se produce imagen Docker.
- **Build:** `go build -o bin/<nombre> ./cmd/...`. Fija versión de Go en `go.mod` y en la imagen base.
- **CI image:** `golang:<version>-alpine` o equivalente; no uses `latest`.

### TypeScript / JavaScript / Node.js
- **Formato:** Prettier (ya cubierto en `base.md`).
- **Lint:** ESLint con config TypeScript (`@typescript-eslint`); sin reglas redundantes con Prettier.
- **Tests:** Jest o Vitest; Mocha cuando ya esté en el proyecto. Puppeteer sólo para tests E2E explícitamente pedidos.
- **Tipos:** `tsc --noEmit` como check independiente.
- **Seguridad:** `npm audit --audit-level=high`; `node_modules/` en `.gitignore`.
- **Build:** `tsc` o bundler existente (Vite, Webpack, Rollup). No añadas bundler si no hay uno.
- **Frameworks Vue/Nuxt:** usa la toolchain Node estándar; para Nuxt agrega `nuxt typecheck`. No sustituyas ESLint por lint de Vetur/Volar a menos que el proyecto ya lo use.

### Python
- **Formato/lint:** Ruff (`ruff check`, `ruff format`). No añadas Flake8/Black/isort; Ruff los cubre.
- **Types:** mypy o pyright si el proyecto ya los usa; no los impones por defecto.
- **Tests:** pytest con `--tb=short`.
- **Seguridad:** Bandit (SAST); `pip-audit` para dependencias.
- **Lockfile:** `uv lock` / `requirements.txt` pinned. Indica claramente cuál se usa.

### PHP
- **Formato/lint:** PHP-CS-Fixer con `--dry-run --diff` en CI; PHP_CodeSniffer como alternativa si el proyecto lo declara.
- **Análisis estático:** PHPStan (nivel mínimo 5) o Psalm.
- **Tests:** PHPUnit.
- **Seguridad:** `local-php-security-checker` para dependencias; Semgrep para SAST.

### Ruby
- **Formato/lint:** RuboCop con `rubocop --parallel`.
- **Tests:** RSpec o Minitest según el proyecto.
- **Seguridad:** `bundle-audit check --update` para dependencias; Brakeman para SAST (sólo si hay Rails o Rack).

### Swift
- **Formato/lint:** SwiftLint (`.swiftlint.yml` explícito). SwiftFormat si el proyecto ya lo usa.
- **Tests:** `swift test`.
- **Seguridad:** no hay auditor de paquetes oficial; aplica trivy sobre el artefacto si se produce binario.

### Bash / Shell
- **Lint:** ShellCheck (`shellcheck -S warning`).
- **Formato:** shfmt (`shfmt -w`).
- **No hay SAST ni auditor** de dependencias aplicable; documenta la omisión.

---

## Infraestructura como código

### Terraform / OpenTofu
- Usa `tofu` si el proyecto declara OpenTofu; usa `terraform` si declara Terraform. No mezcles binarios.
- **Formato:** `tofu fmt -check -recursive` / `terraform fmt -check -recursive`.
- **Validación:** `tofu validate` / `terraform validate` — requiere `init -backend=false`.
- **Lint:** tflint con plugins del proveedor correspondiente.
- **Seguridad SAST:** Trivy (`trivy config .`) o tfsec. Elige uno; no ambos.
- **Lockfile:** `.terraform.lock.hcl` versionado; `tofu providers lock` en el setup de CI.
- **No ejecutes `plan` ni `apply`** durante el bootstrap. Documenta variables requeridas sin valores reales.

### Pulumi
- **Lint/typecheck:** el del lenguaje host (TypeScript → tsc, Python → mypy/ruff, Go → golangci-lint).
- **CI check:** `pulumi preview --non-interactive` sólo si hay stack de preview disponible; en su ausencia documenta la limitación.
- **Seguridad:** trivy sobre artefactos IaC cuando sea aplicable.

---

## Contenedores y orquestación

### Docker
- **Lint:** Hadolint (`hadolint Dockerfile` / `hadolint --failure-threshold warning`).
- **Seguridad:** Trivy image scan (`trivy image --exit-code 1 --severity HIGH,CRITICAL <imagen>`). Escanea la imagen construida, no sólo el Dockerfile.
- **Build check:** `docker build --no-cache -t <imagen>:ci .` en CI para confirmar que la imagen compila.
- **Prácticas:** imagen base fijada con digest o tag inmutable, usuario no-root, multi-stage cuando aplique.
- **docker-compose:** valida con `docker compose config` antes del push.

### Kubernetes (manifests puros)
- **Lint/validación de esquema:** kubeconform (`kubeconform -strict -ignore-missing-schemas`) fijando versión de Kubernetes.
- **Policies:** kube-linter (`kube-linter lint .`) para buenas prácticas de seguridad.
- **Secretos:** nunca versiones valores reales; usa referencias a Secret Store o placeholders documentados.
- **Kustomize:** valida con `kubectl kustomize --dry-run=client` si el proyecto lo usa.
- **Helm:** `helm lint` + `helm template | kubeconform` en CI.

### Argo CD
- **Lint de manifests de Application/AppProject:** yamllint con reglas estrictas + kubeconform contra el CRD de Argo CD.
- **Argo CD CLI:** `argocd app lint` si la CLI está disponible en el runner; documenta si no lo está.
- **No sincronices** durante el bootstrap; el CI sólo valida YAML y estructura.
- **Secrets:** ApplicationSets con generators externos no deben contener credenciales en texto plano.
- **Versión de CRD:** fija la versión del CRD de Argo CD usada para la validación de esquema.

### Argo Workflows
- **Lint:** yamllint + kubeconform contra el CRD de Argo Workflows; fija versión.
- **Argo CLI:** `argo lint <archivo>` si la CLI está disponible; si no, kubeconform cubre el esquema.
- **Templates:** valida `WorkflowTemplate` y `ClusterWorkflowTemplate` por separado.
- **No ejecutes workflows** durante el bootstrap; CI valida estructura y sintaxis.
- **Secretos e inputs:** usa `valueFrom.secretKeyRef` o parámetros; sin valores reales versionados.

---

## Plataformas y runtime

### Nix / NixOS
- **Lint:** statix (`statix check`) y deadnix (`deadnix`) para código Nix.
- **Formato:** nixfmt o alejandra; elige uno y fíjalo en `.pre-commit-config.yaml`.
- **Flakes:** si el proyecto usa flakes, incluye `nix flake check --no-build` en CI.
- **Build check:** `nix build .#default` o el atributo declarado; documenta si el runner no tiene Nix.

### Jenkins (Jenkinsfile en el repo)
- **Lint:** Jenkinsfile-linter vía la CLI de Jenkins o el API de validación del servidor si está disponible.
- **No generes un pipeline de Jenkins** como sustituto del CI del proveedor (GitHub Actions / GitLab CI). Jenkinsfile es artefacto del repo; el CI de calidad sigue siendo el del proveedor.

---

## Bases de datos y servicios (checks de CI)

**PostgreSQL / MySQL / MongoDB / Redis / Firebase:** no hay lint de esquema universal. Si el repo incluye migraciones, valídalas en CI con la herramienta del ORM/migrador declarado (Flyway, Liquibase, golang-migrate, Alembic, etc.). No instales un motor de base de datos en CI sólo para el bootstrap; usa service containers del proveedor si las pruebas los requieren y el usuario los pide explícitamente.

---

## Selección y prioridad

1. Usa sólo las herramientas del stack declarado. Si el usuario no menciona Docker, no generes Dockerfile ni Hadolint.
2. Nunca instales dos herramientas que hagan lo mismo (p. ej. tfsec + trivy para IaC — elige uno).
3. Si una herramienta requiere un runner específico (Argo CLI, argocd CLI, Nix), documenta el requisito y proporciona una alternativa basada en kubeconform/yamllint como fallback.
4. Versiones: fija siempre; nunca uses `latest` ni rangos amplios.
