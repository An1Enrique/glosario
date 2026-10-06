#!/usr/bin/env python3
"""
Hook de MkDocs para generar automáticamente el índice del glosario de ciberseguridad.
Escanea el directorio docs/terms/, extrae los metadatos YAML de cada término
y construye un índice alfabético y visual interactivo en docs/index.md.
"""

import os
import re
import unicodedata
import yaml
from pathlib import Path

def normalize_letter(char):
    """Normaliza un caracter para agrupación alfabética eliminando tildes."""
    if not char:
        return "#"
    char = char.strip()[0].upper()
    nfkd = unicodedata.normalize('NFKD', char)
    base_char = "".join([c for c in nfkd if not unicodedata.combining(c)])
    if base_char.isalpha():
        return base_char
    return "#"

def parse_term_file(filepath):
    """Extrae el frontmatter YAML y el resumen de un archivo de término markdown."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    frontmatter = {}
    body = content

    # Comprobar si tiene frontmatter YAML (--- ... ---)
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1)) or {}
        except Exception as e:
            print(f"[Hook Glosario] Error al parsear YAML en {filepath}: {e}")
        body = match.group(2)

    filename = os.path.basename(filepath)
    slug = filename[:-3] if filename.endswith(".md") else filename

    title = frontmatter.get("title")
    if not title:
        # Intentar extraer del primer encabezado # Titulo
        h1_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        if h1_match:
            title = h1_match.group(1).strip()
        else:
            title = slug.replace("-", " ").title()

    summary = frontmatter.get("summary")
    if not summary:
        # Extraer el primer párrafo no vacío
        paragraphs = [p.strip() for p in body.split("\n\n") if p.strip() and not p.strip().startswith("#")]
        summary = paragraphs[0] if paragraphs else "Sin descripción disponible."
        if len(summary) > 200:
            summary = summary[:197] + "..."

    return {
        "slug": slug,
        "title": title,
        "category": frontmatter.get("category", "General"),
        "tags": frontmatter.get("tags", []),
        "author": frontmatter.get("author", "Comunidad"),
        "author_url": frontmatter.get("author_url", ""),
        "summary": summary,
        "rel_path": f"terms/{slug}/",
    }

def generate_index_markdown(docs_dir):
    """Genera el bloque Markdown del índice a partir de los archivos en terms/."""
    terms_dir = Path(docs_dir) / "terms"
    if not terms_dir.exists():
        return "\n*No se encontró el directorio de términos.*\n"

    term_files = [
        terms_dir / f for f in os.listdir(terms_dir)
        if f.endswith(".md") and not f.startswith(("_", ".")) and f != "index.md"
    ]

    terms = []
    authors = set()
    categories = set()

    for tf in term_files:
        term_data = parse_term_file(tf)
        terms.append(term_data)
        if term_data["author"]:
            authors.add(term_data["author"])
        if term_data["category"]:
            categories.add(term_data["category"])

    # Ordenar alfabéticamente por título
    terms.sort(key=lambda t: unicodedata.normalize('NFKD', t["title"].lower()))

    # Agrupar por letra
    grouped = {}
    for term in terms:
        letter = normalize_letter(term["title"])
        grouped.setdefault(letter, []).append(term)

    sorted_letters = sorted([k for k in grouped.keys() if k != "#"])
    if "#" in grouped:
        sorted_letters.append("#")

    lines = []

    # 1. Tarjetas de Estadísticas
    lines.append('<div class="glossary-stats-grid">')
    lines.append(f'  <div class="stat-card"><span class="stat-number">{len(terms)}</span><span class="stat-label">Términos Definidos</span></div>')
    lines.append(f'  <div class="stat-card"><span class="stat-number">{len(categories)}</span><span class="stat-label">Categorías</span></div>')
    lines.append(f'  <div class="stat-card"><span class="stat-number">{len(authors)}</span><span class="stat-label">Colaboradores</span></div>')
    lines.append('</div>\n')

    # 2. Barra de Navegación Alfabética Rápida
    lines.append('<nav class="alphabet-nav" aria-label="Navegación alfabética">')
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if letter in grouped:
            lines.append(f'<a href="#{letter.lower()}" class="alpha-link active">{letter}</a>')
        else:
            lines.append(f'<span class="alpha-link disabled">{letter}</span>')
    if "#" in grouped:
        lines.append('<a href="#otros" class="alpha-link active">#</a>')
    lines.append('</nav>\n')

    # 3. Secciones por letra con tarjetas
    for letter in sorted_letters:
        anchor_id = "otros" if letter == "#" else letter.lower()
        display_letter = letter if letter != "#" else "# (Símbolos / Números)"
        lines.append(f'<div class="letter-group-header" id="{anchor_id}">')
        lines.append(f'  <h2 class="letter-title">{display_letter}</h2>')
        lines.append(f'  <a href="#top" class="back-to-top" title="Volver arriba">↑ Arriba</a>')
        lines.append('</div>\n')

        lines.append('<div class="terms-card-grid">')
        for term in grouped[letter]:
            cat_badge = f'<span class="term-badge badge-category">{term["category"]}</span>' if term["category"] else ''
            
            author_html = ""
            if term["author"]:
                author_val = term["author"]
                if author_val.startswith("@"):
                    gh_user = author_val.lstrip("@")
                    author_html = f'<a href="https://github.com/{gh_user}" target="_blank" class="author-tag">👤 {author_val}</a>'
                else:
                    author_html = f'<span class="author-tag">👤 {author_val}</span>'

            tag_html = ""
            if term["tags"]:
                tags_formatted = [f'<span class="tag-pill">#{t}</span>' for t in term["tags"]]
                tag_html = f'<div class="term-tags">{" ".join(tags_formatted)}</div>'

            lines.append('  <div class="term-card">')
            lines.append('    <div class="term-card-header">')
            lines.append(f'      <h3 class="term-card-title"><a href="{term["rel_path"]}">{term["title"]}</a></h3>')
            if cat_badge:
                lines.append(f'      <div class="term-badges">{cat_badge}</div>')
            lines.append('    </div>')
            lines.append(f'    <p class="term-card-summary">{term["summary"]}</p>')
            lines.append('    <div class="term-card-footer">')
            lines.append(f'      {author_html}')
            lines.append(f'      {tag_html}')
            lines.append('    </div>')
            lines.append('  </div>')

        lines.append('</div>\n')

    return "\n".join(lines)

def on_page_markdown(markdown, page, config, files):
    """Hook que intercepta el contenido markdown antes de renderizar la página."""
    if page.file.src_path == "index.md":
        docs_dir = config["docs_dir"]
        index_html = generate_index_markdown(docs_dir)
        if "<!-- GLOSSARY_INDEX -->" in markdown:
            return markdown.replace("<!-- GLOSSARY_INDEX -->", index_html)
        else:
            return markdown + "\n\n## 📚 Explorador de Términos\n\n" + index_html
    return markdown

if __name__ == "__main__":
    import sys
    base_dir = Path(__file__).resolve().parent.parent
    docs_path = base_dir / "docs"
    print("--- Test de Generación del Índice del Glosario ---")
    print(generate_index_markdown(docs_path))
