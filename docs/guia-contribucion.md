---
title: "Guía de Contribución"
description: "Guía paso a paso para que el alumnado contribuya con nuevos términos al Glosario de Ciberseguridad."
---

# 🚀 Guía de Contribución al Glosario

¡Bienvenido a la guía de contribución del **Glosario Colaborativo de Ciberseguridad**!

Este proyecto utiliza la metodología **Docs-as-Code** (*Documentación como Código*). Todo el glosario se gestiona mediante control de versiones en Git y se publica automáticamente en GitHub Pages tras validar cada aportación mediante **Pull Requests (PR)**.

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de contar con:

- Una cuenta en [GitHub](https://github.com).
- [Git](https://git-scm.com) instalado y configurado en tu equipo.
- [Docker Desktop](https://www.docker.com) (o Python 3.10+) para probar el sitio en local.

---

## 🛠️ Flujo de Trabajo Paso a Paso

```mermaid
graph LR
    A[1. Fork del Repositorio] --> B[2. Crear Rama feat/termino]
    B --> C[3. Copiar Plantilla y Redactar]
    C --> D[4. Probar en Local con Docker]
    D --> E[5. Commit y Push]
    E --> F[6. Abrir Pull Request]
    F --> G[7. Validación CI y Aprobación]
```

### Paso 1: Hacer un Fork del Repositorio
1. Dirígete al repositorio principal en GitHub: `https://github.com/cibercelia/glosario`.
2. Haz clic en el botón **Fork** (arriba a la derecha) para crear una copia en tu cuenta personal.

---

### Paso 2: Clonar y Crear una Rama de Trabajo
Abre tu terminal y clona tu repositorio bifurcado (sustituye `TU-USUARIO` por tu usuario de GitHub):

```bash
git clone https://github.com/TU-USUARIO/glosario.git
cd glosario
git checkout -b feat/nombre-del-termino
```

!!! tip "Consejo para el nombre de la rama"
    Nombra la rama con el prefijo `feat/` seguido del nombre del concepto en minúsculas y separado por guiones (formato *kebab-case*), por ejemplo: `feat/cross-site-scripting` o `feat/ransomware`.

---

### Paso 3: Crear tu Término Usando la Plantilla
1. Copia el archivo de plantilla a la carpeta `docs/terms/` con el nombre de tu término en minúsculas:
   ```bash
   cp docs/plantillas/plantilla-termino.md docs/terms/nombre-del-termino.md
   ```
2. Abre `docs/terms/nombre-del-termino.md` en tu editor de código (VS Code, etc.).
3. Rellena los **metadatos YAML (Frontmatter)** obligatorios al inicio del archivo:
   ```yaml
   ---
   title: "Nombre del Término"
   category: "Vulnerabilidades Web" # Categoría del concepto
   author: "@tu-usuario-github" # Tu usuario para darte crédito
   tags:
     - ciberseguridad
     - web
     - owasp
   summary: "Resumen explicativo del término en 1 o 2 frases concisas."
   ---
   ```
4. Desarrolla las secciones requeridas siguiendo la [Plantilla de Términos](plantillas/plantilla-termino.md):
   - **📖 Definición**: Qué es y contexto técnico.
   - **⚙️ ¿Cómo funciona?**: Flujo, arquitectura o principios.
   - **🎯 Ejemplo Práctico**: Escenario vulnerable vs seguro con código si aplica.
   - **🛡️ Mitigación y Buenas Prácticas**: Recomendaciones oficiales (OWASP, NIST, CIS...).
   - **🔗 Referencias**: Enlaces a fuentes fiables.

---

### Paso 4: Probar la Web en Local con Docker

Para verificar que no hay enlaces rotos y que el índice de la página principal se genera correctamente:

```bash
docker compose up
```

Abre tu navegador en: **[http://localhost:8000](http://localhost:8000)**

!!! note "Recarga automática"
    Cada vez que guardes cambios en tu archivo `.md`, la página web se recargará automáticamente mostrando tus modificaciones.

*(Si prefieres usar Python nativo sin Docker: `pip install -r requirements.txt && mkdocs serve`)*.

---

### Paso 5: Confirmar Cambios y Subir la Rama
Una vez revisado el resultado en local:

```bash
git add docs/terms/nombre-del-termino.md
git commit -m "feat(terms): añadir definición de <nombre-del-termino>"
git push origin feat/nombre-del-termino
```

---

### Paso 6: Abrir el Pull Request (PR)
1. Ve a la página de tu fork en GitHub y pulsa en **"Compare & pull request"**.
2. Completa la plantilla de PR marcando las casillas del checklist.
3. El sistema de Integración Continua (GitHub Actions) ejecutará automáticamente las pruebas de validación:
   - Formato de nombre de archivo (*kebab-case*).
   - Metadatos YAML completos (`title`, `category`, `author`, `tags`, `summary`).
   - Compilación estricta de MkDocs sin enlaces rotos.
4. Cuando el profesorado o moderadores revisen y aprueben tu PR, se fusionará en la rama principal y aparecerá publicado en la web.

---

## ⚠️ Reglas de Calidad y Buenas Prácticas

- **Originalidad**: Redacta las explicaciones con tus propias palabras y cita siempre las fuentes consultadas.
- **Rigor Técnico**: Utiliza terminología precisa y estándares de la industria (OWASP, NIST, MITRE ATT&CK, RFCs).
- **Ejemplos Claros**: Los bloques de código deben estar formateados y comentados.
