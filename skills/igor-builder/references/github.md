# GitHub

Usa el conector GitHub autenticado o `gh`. Revisa cuenta, host y disponibilidad de Actions. No deduzcas que la sesión del navegador da acceso al CLI.

Genera `.github/workflows/ci.yml` con eventos `push` sin filtros de branches/paths y `pull_request`. No uses `pull_request_target` para ejecutar código del contribuidor. Calidad, lint y seguridad deben ejecutarse en todas las ramas, incluidas main, develop, feature, release y hotfix. No agregues condiciones por rama ni skips automáticos. Configura permisos mínimos `contents: read`, versiones de runtime explícitas, instalación desde locks y acciones fijadas a SHAs verificados con comentario de versión.

Todos los checks deben contribuir al resultado del workflow. Evita que cancelar runs por concurrencia impida comprobar cada push. Valida sintaxis con actionlint si está disponible, y comprueba la ejecución real después del push. Los pushes usando el GITHUB_TOKEN de Actions pueden no disparar otros workflows: si bootstrap ocurre dentro de Actions, usa una credencial autorizada apropiada o informa esa limitación antes de elegir el mecanismo de push.

Guarda release en `ci/templates/github-release.yml`, nunca en `.github/workflows/` inicialmente. Una vez copiada allí por autorización expresa, debe reaccionar a tags SemVer, verificar main, ejecutar checks/build y crear la GitHub Release con artefactos. Restringe `contents: write` al job de publicación. Documenta la activación y permisos; no crees secretos durante el bootstrap.

Si un conector no permite publicar archivos de workflows o crear ramas, usa CLI/API autenticado disponible. Si los permisos no alcanzan, conserva los archivos y describe la operación pendiente; no omitas el CI para conseguir que el push pase.
