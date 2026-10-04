# Base común

## Archivos y checks

EditorConfig: `root = true`, UTF-8, LF, newline final, eliminar espacios finales e indentación adaptada al lenguaje. Conserva tabs en Makefiles y espacios significativos cuando proceda. Excluye binarios y archivos generados del formato.

Fija Prettier como dependencia de desarrollo con lockfile y scripts de `format` y `format:check`. No ejecutes instalaciones que puedan modificar el lock en CI. Usa configuración explícita e ignores para dependencias, compilados y vendored code.

Pre-commit: fija las revisiones de hooks; incluye whitespace/newline, validación de YAML/JSON con soporte adecuado a tags del proveedor, secretos, formato y lint. Los hooks locales y CI deben compartir configuración y comandos. Instala hooks `pre-commit` y `pre-push` en el clon inicial, y documenta su instalación en futuros clones. Ejecuta en CI la revisión de todos los archivos y los checks completos; los hooks no sustituyen CI ni están activos automáticamente en otros clones.

Elige herramientas mantenidas adecuadas al lenguaje, verificando soporte oficial antes de generar archivos. Ejemplos de criterio: Ruff para Python, ESLint para JS/TS, gofmt/go vet para Go, rustfmt/Clippy para Rust. Prefiere el framework de tests nativo y evita herramientas duplicadas. Para lenguajes sin soporte de un scanner, selecciona otro compatible y explica límites reales.

Seguridad debe cubrir tres superficies: secretos (por ejemplo Gitleaks), código (SAST compatible) y dependencias (auditor del ecosistema). Fija versiones y configura códigos de salida que hagan fallar CI ante hallazgos; algunos scanners necesitan un flag explícito. Escanea el historial para secretos cuando la herramienta lo soporte y descarga el historial necesario. En un proyecto sin dependencias externas, comunica el alcance vacío del auditor, sin inventar hallazgos ni saltarse silenciosamente la fase.

Mantén los checks reproducibles mediante lockfiles, versiones de runtime y herramientas. No requieras productos de pago para los checks básicos. Usa credenciales de solo lectura para checks; no expongas secretos a código de forks. No agregues excepciones automáticas para hacer pasar scanners.

## GitFlow y release inactivo

Crea `main` y `develop`; documenta `feature/*` desde develop, `release/*` desde develop y `hotfix/*` desde main. Las features regresan a develop; releases/hotfixes se integran mediante PR/MR hacia main y de vuelta a develop. Usa tags SemVer `vX.Y.Z` en main para versiones terminadas. No hagas merges, tags ni releases durante el bootstrap.

La plantilla debe implementar validación de tag SemVer, comprobar que el commit está en main, volver a ejecutar checks, construir el artefacto apropiado al lenguaje y crear una release del proveedor con notas y artefactos. Comprueba idempotencia por tag: nunca sobrescribas una release existente. No publiques paquetes en registries ni despliegues por defecto.

Guárdala fuera de la configuración activa. No basta un job manual: no debe poder ejecutarse ni manual ni automáticamente antes de que el usuario la habilite. El README debe explicar cómo activarla, permisos/variables requeridos, configuración del artefacto, secuencia GitFlow y cómo verificarla antes del primer tag. No dejes comandos ficticios ni variables de artefactos sin resolver en la plantilla generada. Solo al activar el release deben añadirse credenciales con capacidad de escritura.
