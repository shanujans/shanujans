import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = Path("/tmp/repo")
ASSETS = REPO / "assets"

with open(ROOT / "terminal_data.json", encoding="utf-8") as f:
    DATA = json.load(f)

WHITE = "#E6EDF3"
GREY = "#A0B3BC"
BLUE = "#5299D2"
DIM = "#5C6773"
ORANGE = "#CA7938"

CARD_WIDTH = "100%"

def img_card(slug, alt):
    return f'<img src="assets/terminal-{slug}.svg" alt="{html.escape(alt)}" width="{CARD_WIDTH}" style="display:block"/>'

def img_bar(slug, alt):
    return f'<img src="assets/bar-{slug}.svg" alt="{html.escape(alt)}" width="{CARD_WIDTH}" style="display:block"/>'

def widget_card(slug, alt):
    if slug == "activity":
        return (
            '<a href="https://github.com/shanujans">\n'
            '  <img src="https://github-readme-activity-graph.vercel.app/graph?username=shanujans&theme=react-dark&bg_color=0d1117&color=ca7938&line=5299d2&point=ffffff" alt="Shanujan\'s Contribution Graph" width="100%"/>\n'
            '</a>'
        )
    if slug == "snake":
        return (
            '<a href="https://github.com/shanujans">'
            '<img src="https://raw.githubusercontent.com/shanujans/shanujans/output/github-contribution-grid-snake.svg" alt="snake"/>'
            '</a>'
        )
    return img_card(slug, alt)

def connect_html():
    c = DATA["contact"]
    lines = [
        ('shanujans@github', WHITE, True, None, 'header'),
        ('- Reach Me -', GREY, True, None, 'section'),
        ('. Email: ....... shanujansh@gmail.com', BLUE, False, c["email"]["url"], 'field'),
        ('. Portfolio: ... shanujan.is-a.dev', BLUE, False, c["portfolio"]["url"], 'field'),
        ('. GitHub: ...... github.com/shanujans', BLUE, False, c["github"]["url"], 'field'),
        ('. LinkedIn: .... linkedin.com/in/shanujansuresh', BLUE, False, c["linkedin"]["url"], 'field'),
        ('// thanks for stopping by -- let\'s build something', DIM, True, None, 'comment'),
        ('>_', ORANGE, True, None, 'prompt'),
    ]
    html_lines = []
    for i, line in enumerate(lines):
        text, color, bold, link, suffix = line
        filename = f"assets/connect-lines/line-{i:02d}-{suffix}.svg"
        if text == '':
            html_lines.append(f'<img src="{filename}" alt="" width="100%" style="display:block"/>')
        else:
            if link:
                html_lines.append(
                    f'<a href="{html.escape(link)}" target="_blank" style="text-decoration:none;display:block">'
                    f'<img src="{filename}" alt="{html.escape(text)}" width="100%" style="display:block"/>'
                    f'</a>'
                )
            else:
                html_lines.append(
                    f'<img src="{filename}" alt="{html.escape(text)}" width="100%" style="display:block"/>'
                )
    return "\n".join(html_lines)

parts = []

# Hero - neofetch card from main branch (dark_mode.svg / light_mode.svg)
# Fixed width to prevent GitHub from over-scaling the 1480px-wide SVG
NEOFETCH_WIDTH = "800"
parts.append(
    '<p align="center">\n'
    '  <a href="https://github.com/shanujans">\n'
    '    <picture>\n'
    f'      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/shanujans/shanujans/main/dark_mode.svg">\n'
    f'      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/shanujans/shanujans/main/light_mode.svg">\n'
    f'      <img alt="Shanujan\'s GitHub neofetch card" src="https://raw.githubusercontent.com/shanujans/shanujans/main/light_mode.svg" width="{NEOFETCH_WIDTH}">\n'
    '    </picture>\n'
    '  </a>\n'
    '</p>'
)
parts.append('<hr/>')

# Profile views - terminal style bar + live counter line
parts.append(
    f'<div>\n{img_bar("views", "$ views")}\n'
    f'<a href="https://github.com/shanujans" target="_blank" style="text-decoration:none;display:block">'
    f'<img src="assets/views-line.svg" alt=". Views: ....... 967" width="{CARD_WIDTH}" style="display:block"/>'
    f'</a>\n</div>'
)
parts.append('<hr/>')

sections = [
    ("projects",      "projects",      "Featured Projects",           "img"),
    ("opensource",    "opensource",    "Open Source Contributions",   "img"),
    ("certifications","certifications","Certifications",              "img"),
    ("stats",         "stats",         "GitHub Stats",                "img"),
    ("activity",      "activity",      "Contribution Activity",       "widget"),
    ("snake",         "snake",         "Contribution Snake",          "widget"),
]

for bar_slug, card_slug, alt, kind in sections:
    if kind == "widget":
        parts.append(f'<div>\n{img_bar(bar_slug, f"$ {bar_slug}")}\n{widget_card(card_slug, alt)}\n</div>')
    else:
        parts.append(f'<div>\n{img_bar(bar_slug, f"$ {bar_slug}")}\n{img_card(card_slug, alt)}\n</div>')
    parts.append('<hr/>')

parts.append(f'<div>\n{img_bar("connect", "$ connect")}\n{connect_html()}\n</div>')
parts.append('<hr/>')

readme_md = "\n".join(parts) + "\n"
readme_path = REPO / "README.md"
readme_path.write_text(readme_md, encoding="utf-8")

size_kb = readme_path.stat().st_size / 1024
img_count = readme_md.count('<img src="assets/')
print(f"Wrote {readme_path}  ({size_kb:.1f} KB)")
print(f"  asset <img> tags: {img_count}")
