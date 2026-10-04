# GitLab

Usa el conector GitLab autenticado o `glab`. Respeta el host y namespace exactos. Comprueba CI y runners disponibles; crear YAML no implica que exista un runner.

Genera `.gitlab-ci.yml` con reglas que admitan todo pipeline `push` sobre ramas y `merge_request_event`. No añadas `only: main`, filtros `changes` ni una regla que suprima los pipelines de push cuando haya un MR abierto: el usuario pide comprobar cada push. Un pipeline adicional de MR es aceptable. Las reglas de cada job deben preservar calidad, lint y seguridad para todas las ramas.

Fija imágenes/versiones y usa instalación reproducible desde locks. Todos los checks deben bloquear ante fallo: sin `allow_failure`. Los controles básicos deben funcionar sin depender de plantillas de seguridad de planes de pago. No expongas variables protegidas a forks. Usa el CI Lint del proveedor cuando el acceso lo permita y revisa el primer pipeline tras publicar ambas ramas.

Guarda release en `ci/templates/gitlab-release.yml`; no lo incluyas desde `.gitlab-ci.yml` al crear el proyecto. Prepara un fragmento includible con jobs y reglas de tags SemVer, verificación de main, checks/build y publicación de GitLab Release con artefactos. Documenta los cambios de `workflow: rules` necesarios para admitir tags al habilitarlo y las etapas que deben añadirse. Verifica que el include futuro forme una configuración válida. No basta `when: manual`: la plantilla debe quedar desconectada.

Adapta publicación/autenticación a capacidades verificadas del host y su versión. No presupongas que `CI_JOB_TOKEN` tiene permisos para cualquier operación. La plantilla debe describir el mecanismo mínimo permitido y la configuración que el usuario deberá habilitar; nunca guarda tokens en archivos versionados.
