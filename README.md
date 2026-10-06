# 🛡️ Glosario Colaborativo de Ciberseguridad

Repositorio colaborativo para crear, organizar y mantener una enciclopedia y glosario técnico de ciberseguridad utilizando la metodología **Docs-as-Code** con **Material for MkDocs**, desplegado automáticamente en **GitHub Pages**.

El glosario está diseñado para que el **alumnado y la comunidad** contribuyan añadiendo o mejorando términos mediante el flujo de trabajo estándar de Git (**Fork & Pull Request**).

---

## 📂 Estructura del Proyecto

```text
glosario-ciberseguridad/
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md       # Plantilla de verificación para PRs de alumnos
│   └── workflows/
│       ├── deploy.yml                 # Despliegue automático a GitHub Pages (main)
│       └── validate-pr.yml            # Validación CI de metadatos y enlaces en cada PR
├── docs/
│   ├── index.md                       # Página principal con índice interactivo dinámico
│   ├── guia-contribucion.md           # Guía completa de contribución para el alumnado
│   ├── stylesheets/
│   │   └── extra.css                  # Estilos personalizados (tarjetas, badges, dark mode)
│   ├── plantillas/
│   │   └── plantilla-termino.md       # Plantilla oficial para redactar un nuevo término
│   └── terms/
│       ├── sql-injection.md           # Término de ejemplo: Inyección SQL
│       └── zero-trust.md              # Término de ejemplo: Zero Trust
├── hooks/
│   └── generate_glossary_index.py     # Hook de MkDocs: Genera el índice A-Z automáticamente
├── .gitignore
├── compose.yaml                       # Configuración de Docker Compose para entorno local
├── Dockerfile                         # Imagen Docker con MkDocs y dependencias
├── mkdocs.yml                         # Configuración principal de MkDocs y Material Theme
├── README.md                          # Guía del proyecto y de contribución
└── requirements.txt                   # Dependencias de Python
```

---

## 🚀 Guía Rápida para Alumnos: Cómo Contribuir

Sigue estos pasos para investigar y proponer un nuevo término al glosario:

### 1. Haz un Fork del Repositorio
Haz clic en el botón **Fork** (arriba a la derecha en GitHub) para crear una copia del repositorio en tu cuenta personal.

### 2. Clona tu Fork y Crea una Rama
Abre tu terminal y ejecuta:

```bash
git clone https://github.com/TU-USUARIO/glosario.git
cd glosario
git checkout -b feat/nombre-del-termino
```

> 💡 *Usa nombres en minúsculas separados por guiones para la rama, por ejemplo: `feat/cross-site-scripting` o `feat/ransomware`.*

### 3. Redacta tu Término Usando la Plantilla
1. Copia el archivo de plantilla a la carpeta `docs/terms/` con el nombre de tu término en formato **kebab-case**:
   ```bash
   cp docs/plantillas/plantilla-termino.md docs/terms/mi-termino.md
   ```
2. Abre `docs/terms/mi-termino.md` en tu editor de código.
3. Rellena el bloque inicial de **metadatos YAML (Frontmatter)**:
   ```yaml
   ---
   title: "Nombre del Término"
   category: "Vulnerabilidades Web"
   author: "@tu-usuario-github"
   tags:
     - ciberseguridad
     - web
   summary: "Resumen conciso del término en 1 o 2 líneas explicativas."
   ---
   ```
4. Desarrolla las secciones del término: **Definición**, **¿Cómo funciona?**, **Ejemplo práctico (seguro vs inseguro)**, **Medidas de mitigación** y **Referencias bibliográficas**.

---

## 🐳 Probar la Web en Local con Docker

Puedes levantar el servidor de documentación y ver tus cambios en tiempo real con recarga automática (*hot-reload*).

### Opción con Docker Compose (Recomendado)

```bash
docker compose up
```

Abre tu navegador en: **[http://localhost:8000](http://localhost:8000)**

Cada vez que edites y guardes un archivo en `docs/`, el navegador actualizará automáticamente el contenido y el índice alfabético.

### Opción con Docker directo

```bash
# Construir la imagen
docker build -t glosario-ciberseguridad .

# Ejecutar el contenedor montando los archivos locales
docker run --rm -it -p 8000:8000 -v $(pwd):/docs glosario-ciberseguridad
```

---

## 💻 Alternativa: Probar en Local con Python (sin Docker)

Si prefieres usar un entorno virtual de Python en tu equipo:

```bash
# Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor de desarrollo
mkdocs serve
```

---

## 🔍 ¿Cómo Funciona el Índice Dinámico en la Página Principal?

Para que los alumnos solo tengan que preocuparse de crear su archivo en `docs/terms/`, el proyecto incluye un **Hook de MkDocs** en [`hooks/generate_glossary_index.py`](hooks/generate_glossary_index.py):

1. Durante la compilación o el servidor de desarrollo, el hook escanea todos los archivos Markdown en `docs/terms/`.
2. Lee los metadatos YAML de cada término (`title`, `category`, `author`, `tags`, `summary`).
3. Agrupa los términos alfabéticamente (A-Z) y genera automáticamente:
   - Tarjetas de estadísticas (total de términos, categorías y colaboradores).
   - Barra de salto alfabético interactivo.
   - Tarjetas estilizadas con enlaces directos, insignias de categoría y etiquetas.
4. Inyecta este contenido en el marcador `<!-- GLOSSARY_INDEX -->` de [`docs/index.md`](docs/index.md).

---

## 📬 Enviar tu Contribución (Pull Request)

1. Añade los cambios y haz commit:
   ```bash
   git add docs/terms/mi-termino.md
   git commit -m "feat(terms): añadir término <nombre-del-termino>"
   ```
2. Sube la rama a tu fork en GitHub:
   ```bash
   git push origin feat/nombre-del-termino
   ```
3. Dirígete a GitHub y haz clic en **"Compare & pull request"**.
4. Completa la plantilla de PR verificando que cumples todos los puntos del checklist.
5. El flujo automatizado de GitHub Actions (**`validate-pr.yml`**) validará que el formato YAML y la compilación de MkDocs sean correctos.
6. Una vez revisado y aprobado por el profesorado, el término se integrará en `main` y se desplegará automáticamente en GitHub Pages.

---

## ⚙️ Configuración de GitHub Pages en el Repositorio

Para activar el despliegue automático en GitHub:

1. Ve a **Settings** > **Pages** en el repositorio de GitHub.
2. En la sección **Build and deployment** > **Source**, selecciona **GitHub Actions**.
3. Cada push a `main` ejecutará el workflow [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) y publicará el sitio web.