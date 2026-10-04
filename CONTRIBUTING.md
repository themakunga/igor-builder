# Contribuir a igor-builder

¡Gracias por tu interés! Este documento explica cómo reportar problemas, proponer cambios y enviar pull requests.

## Código de conducta

Este proyecto se rige por el [Código de Conducta](CODE_OF_CONDUCT.md). Al participar, aceptas cumplirlo.

## Cómo reportar un bug

Abre un issue describiendo:

1. Qué hiciste (comando o prompt exacto).
2. Qué esperabas que pasara.
3. Qué pasó en su lugar (salida de error, CI fallido, etc.).
4. Versión del plugin y del cliente (Claude Code / Codex).

No incluyas credenciales, tokens ni claves en el issue.

## Cómo proponer una mejora

Abre un issue con el prefijo `[RFC]` antes de escribir código. Describe el problema que resuelves y la solución propuesta. Así evitamos trabajo duplicado.

## Flujo de trabajo

```
main        ← tags vX.Y.Z, producción
develop     ← integración continua
feature/*   ← trabajo nuevo (parte desde develop)
hotfix/*    ← correcciones urgentes (parte desde main)
```

1. Forkea el repositorio y crea tu rama desde `develop`:
   ```sh
   git checkout -b feature/mi-mejora develop
   ```
2. Instala las dependencias de desarrollo:
   ```sh
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements-dev.txt
   npm ci
   pre-commit install
   ```
3. Realiza tus cambios y asegúrate de que todos los checks pasan:
   ```sh
   pre-commit run --all-files
   npm run format:check
   python scripts/check_plugin.py --package
   ```
4. Haz commit siguiendo [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat: descripción` — nueva funcionalidad
   - `fix: descripción` — corrección de bug
   - `docs: descripción` — sólo documentación
   - `refactor: descripción` — sin cambio de comportamiento
5. Abre un pull request hacia `develop` con una descripción clara del cambio y el issue relacionado.

## Qué se acepta

- Nuevos stacks/tecnologías en `references/tech.md` con herramientas verificadas y versionadas.
- Mejoras a `references/base.md`, `github.md` o `gitlab.md` que corrijan comportamiento o añadan claridad.
- Correcciones de bugs en `SKILL.md` o los scripts de validación.
- Mejoras de documentación.

## Qué no se acepta

- Credenciales, tokens o valores reales de cualquier tipo.
- Herramientas sin versión fija o marcadas como `latest`.
- Cambios que rompan los checks existentes sin justificación.
- Dependencias de desarrollo nuevas sin discusión previa.

## Licencia

Al contribuir aceptas que tu aporte se distribuya bajo la [licencia MIT](LICENSE) de este proyecto.
