"""
write_readme.py

Reads the freshly-generated SVGs from /tmp/repo/assets and emits README.md
with ALL cards as <img src="assets/...svg"> references.

Note: GitHub strips <style> from inline SVGs in READMEs, causing font CSS
to dump as raw text. Using <img> tags ensures SVGs render correctly.
"""

import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = Path("/tmp/repo")
ASSETS = REPO / "assets"

with open(ROOT / "terminal_data.json", encoding="utf-8") as f:
    DATA = json.load(f)


def img_card(slug, alt, width=None):
    width_attr = f' width="{width}"' if width else ""
    return f'<img src="assets/terminal-{slug}.svg" alt="{html.escape(alt)}"{width_attr}/>'


def img_bar(slug, alt):
    return f'<img src="assets/bar-{slug}.svg" alt="{html.escape(alt)}"/>'


def centered_img(img_tag):
    return f'<p align="center">{img_tag}</p>'


# Build README
parts = []

# Hero - use neofetch card from main branch
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

# Projects
parts.append(img_bar("projects", "$ ls ./projects --featured"))
parts.append(centered_img(img_card("projects", "Featured Projects", 625)))

parts.append('<hr/>')

# Open Source Contributions
parts.append(img_bar("opensource", "$ git contrib --oss"))
parts.append(centered_img(img_card("opensource", "Open Source Contributions", 625)))

parts.append('<hr/>')

# Certifications
parts.append(img_bar("certifications", "$ cat certifications.log"))
parts.append(centered_img(img_card("certifications", "Certifications", 588)))

parts.append('<hr/>')

# External widgets - stats
parts.append(
    '<p align="center">'
    '<a href="https://github.com/shanujans"><img src="https://github-readme-stats.vercel.app/api?username=shanujans&show_icons=true&hide_border=true&bg_color=0d1117&title_color=ca7938&icon_color=5299d2&text_color=a0b3bc"></a>'
    '<a href="https://github.com/shanujans"><img src="https://github-readme-stats.vercel.app/api/top-langs/?username=shanujans&layout=compact&hide_border=true&bg_color=0d1117&title_color=ca7938&text_color=a0b3bc"></a>'
    '</p>'
)
parts.append(
    '<p align="center">'
    '<a href="https://github.com/shanujans"><img src="https://streak-stats.demolab.com?user=shanujans&hide_border=true&background=0d1117&border=0d1117&ring=ca7938&fire=5299d2&currStreakNum=ffffff&currStreakLabel=ca7938&sideNums=a0b3bc&sideLabels=a0b3bc&dates=5c6773"></a>'
    '</p>'
)

parts.append('<hr/>')

# Activity
parts.append(img_bar("activity", "$ gh activity --graph"))
parts.append(
    '<p align="center">'
    '<a href="https://github.com/shanujans"><img src="https://github-readme-activity-graph.vercel.app/graph?username=shanujans&hide_border=true&bg_color=0d1117&color=a0b3bc&line=ca7938&point=5299d2&area=true&area_color=5299d2"></a>'
    '</p>'
)

parts.append('<hr/>')

# Snake
parts.append(img_bar("snake", "$ ./snake --eat contributions"))
parts.append(
    '<p align="center">'
    '<img src="https://raw.githubusercontent.com/shanujans/shanujans/output/github-contribution-grid-snake.svg" alt="snake"/>'
    '</p>'
)

parts.append('<hr/>')

# Connect
parts.append(img_bar("connect", "$ cat contact.md"))
parts.append(centered_img(img_card("connect", "Contact", 524)))

parts.append(
    '<p align="center">'
    '<a href="mailto:shanujansh@gmail.com">Email</a> &middot; '
    '<a href="https://shanujan.is-a.dev">Portfolio</a> &middot; '
    '<a href="https://github.com/shanujans">GitHub</a> &middot; '
    '<a href="https://www.linkedin.com/in/shanujansuresh/">LinkedIn</a>'
    '</p>'
)


readme_md = "\n\n".join(parts) + "\n"

readme_path = REPO / "README.md"
readme_path.write_text(readme_md, encoding="utf-8")

size_kb = readme_path.stat().st_size / 1024
img_count = readme_md.count('<img src="assets/')

print(f"Wrote {readme_path}  ({size_kb:.1f} KB)")
print(f"  asset <img> tags   : {img_count}")