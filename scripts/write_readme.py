"""
write_readme.py

Generates README.md with ALL cards as <img> tags.
GitHub Markdown only renders SVGs via <img src="..."> - raw <svg> elements are shown as text.
Note: Internal SVG links (xlink:href) don't work on GitHub; only the hero wraps in <a>.
"""

import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = Path("/tmp/repo")
ASSETS = REPO / "assets"

with open(ROOT / "terminal_data.json", encoding="utf-8") as f:
    DATA = json.load(f)

CARD_WIDTH = "100%"

def img_card(slug, alt):
    return f'<img src="assets/terminal-{slug}.svg" alt="{html.escape(alt)}" width="{CARD_WIDTH}" style="display:block"/>'

def img_bar(slug, alt):
    return f'<img src="assets/bar-{slug}.svg" alt="{html.escape(alt)}" width="{CARD_WIDTH}" style="display:block"/>'

def widget_card(slug, alt):
    if slug == "stats":
        return (
            '<p align="left">'
            '<a href="https://github.com/shanujans"><img src="https://github-readme-stats.vercel.app/api?username=shanujans&show_icons=true&hide_border=true&bg_color=0d1117&title_color=ca7938&icon_color=5299d2&text_color=a0b3bc" alt="GitHub Stats"/></a>'
            '<a href="https://github.com/shanujans"><img src="https://github-readme-stats.vercel.app/api/top-langs/?username=shanujans&layout=compact&hide_border=true&bg_color=0d1117&title_color=ca7938&text_color=a0b3bc" alt="Top Languages"/></a>'
            '</p>'
        )
    if slug == "activity":
        return (
            '<a href="https://github.com/shanujans">\n'
            '  <img src="https://github-readme-activity-graph.vercel.app/graph?username=shanujans&theme=react-dark&bg_color=0d1117&color=ca7938&line=5299d2&point=ffffff" alt="Shanujan\'s Contribution Graph" width="100%"/>\n'
            '</a>\n'
            '<a href="https://github.com/shanujans">\n'
            '  <img src="https://streak-stats.demolab.com?user=shanujans&hide_border=true&background=0d1117&border=0d1117&ring=ca7938&fire=5299d2&currStreakNum=ffffff&currStreakLabel=ca7938&sideNums=a0b3bc&sideLabels=a0b3bc&dates=5c6773" alt="Streak Stats"/>\n'
            '</a>'
        )
    if slug == "snake":
        return (
            '<a href="https://github.com/shanujans">'
            '<img src="https://raw.githubusercontent.com/shanujans/shanujans/output/github-contribution-grid-snake.svg" alt="snake"/>'
            '</a>'
        )
    return img_card(slug, alt)

parts = []

# Hero - neofetch from main branch
parts.append(
    '<p align="center">\n'
    '  <a href="https://github.com/shanujans">\n'
    '    <picture>\n'
    '      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/shanujans/shanujans/main/dark_mode.svg">\n'
    '      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/shanujans/shanujans/main/light_mode.svg">\n'
    '      <img alt="Shanujan\'s GitHub neofetch card" src="https://raw.githubusercontent.com/shanujans/shanujans/main/light_mode.svg">\n'
    '    </picture>\n'
    '  </a>\n'
    '</p>'
)
parts.append(
    '<p align="center">'
    '<img src="https://komarev.com/ghpvc/?username=shanujans&style=flat-square&color=5299d2&label=PROFILE+VIEWS" alt="profile views"/>'
    '</p>'
)
parts.append('<hr/>')

sections = [
    ("projects",      "projects",      "Featured Projects",      "img"),
    ("opensource",    "opensource",    "Open Source Contributions", "img"),
    ("certifications","certifications","Certifications",         "img"),
    ("stats",         "stats",         "GitHub Stats",           "img"),
    ("activity",      "activity",      "Contribution Activity",  "widget"),
    ("snake",         "snake",         "Contribution Snake",     "widget"),
    ("connect",       "connect",       "Contact",                "img"),
]

for bar_slug, card_slug, alt, kind in sections:
    if kind == "widget":
        parts.append(f'<div>\n{img_bar(bar_slug, f"$ {bar_slug}")}\n{widget_card(card_slug, alt)}\n</div>')
    else:
        parts.append(f'<div>\n{img_bar(bar_slug, f"$ {bar_slug}")}\n{img_card(card_slug, alt)}\n</div>')
    parts.append('<hr/>')

# Footer
parts.append(
    '<p align="left">'
    '<a href="mailto:shanujansh@gmail.com">Email</a> &middot; '
    '<a href="https://shanujan.is-a.dev">Portfolio</a> &middot; '
    '<a href="https://github.com/shanujans">GitHub</a> &middot; '
    '<a href="https://www.linkedin.com/in/shanujansuresh/">LinkedIn</a>'
    '</p>'
)

readme_md = "\n".join(parts) + "\n"
readme_path = REPO / "README.md"
readme_path.write_text(readme_md, encoding="utf-8")

size_kb = readme_path.stat().st_size / 1024
img_count = readme_md.count('<img src="assets/')
print(f"Wrote {readme_path}  ({size_kb:.1f} KB)")
print(f"  asset <img> tags: {img_count}")