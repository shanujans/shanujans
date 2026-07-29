"""
write_readme.py

Generates README.md with:
- Hero: <picture> from main branch (dark/light mode)
- Inline SVGs for cards needing clickable links (projects, certifications, connect)
- <img> tags for other cards (preserves embedded fonts)
- Terminal-style: left-aligned, compact, consistent widths
"""

import json, html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = Path("/tmp/repo")
ASSETS = REPO / "assets"

with open(ROOT / "terminal_data.json", encoding="utf-8") as f:
    DATA = json.load(f)

INLINE_CARDS = set(DATA.get("inline_cards", ["hero", "projects", "certifications", "connect"]))
CARD_WIDTH = 720  # consistent width for all terminal cards

def read_svg(slug):
    path = ASSETS / f"terminal-{slug}.svg"
    return path.read_text(encoding="utf-8") if path.exists() else ""

def strip_font_styles(svg):
    """Remove @font-face defs so GitHub doesn't strip them; fallback to system monospace."""
    return re.sub(r'<defs>.*?</defs>', '', svg, flags=re.DOTALL)

def inline_card(slug, alt):
    svg = read_svg(slug)
    if not svg:
        return f'<!-- terminal-{slug}.svg not found -->'
    svg = svg.replace('<svg ', f'<svg width="{CARD_WIDTH}" ')
    return f'<p align="left">{svg}</p>'

def img_card(slug, alt):
    return f'<p align="left"><img src="assets/terminal-{slug}.svg" alt="{html.escape(alt)}" width="{CARD_WIDTH}"/></p>'

def img_bar(slug, alt):
    return f'<p align="left"><img src="assets/bar-{slug}.svg" alt="{html.escape(alt)}"/></p>'

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
            '<p align="left">'
            '<a href="https://github.com/shanujans"><img src="https://streak-stats.demolab.com?user=shanujans&hide_border=true&background=0d1117&border=0d1117&ring=ca7938&fire=5299d2&currStreakNum=ffffff&currStreakLabel=ca7938&sideNums=a0b3bc&sideLabels=a0b3bc&dates=5c6773" alt="Streak Stats"/></a>'
            '</p>'
        )
    if slug == "snake":
        return (
            '<p align="left">'
            '<a href="https://github.com/shanujans"><img src="https://github-readme-activity-graph.vercel.app/graph?username=shanujans&hide_border=true&bg_color=0d1117&color=a0b3bc&line=ca7938&point=5299d2&area=true&area_color=5299d2" alt="Activity Graph"/></a>'
            '</p>'
        )
    return img_card(slug, alt)

# Build README
parts = []

# Hero - from main branch with dark/light mode
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

# Sections: (bar_slug, card_slug, card_alt, use_inline)
sections = [
    ("projects",  "projects",  "Featured Projects",    True),   # inline: clickable titles
    ("opensource","opensource","Open Source Contributions", False), # img
    ("certifications","certifications","Certifications", True),   # inline: clickable verify links
    ("stats",     "stats",     "GitHub Stats",         False),  # external widget
    ("activity",  "activity",  "Contribution Activity", False), # external widget
    ("snake",     "snake",     "Contribution Snake",   False),  # external widget
    ("connect",   "connect",   "Contact",              True),   # inline: clickable links
]

for bar_slug, card_slug, alt, use_inline in sections:
    parts.append(img_bar(bar_slug, f"$ {bar_slug}"))
    if use_inline and card_slug in INLINE_CARDS:
        parts.append(inline_card(card_slug, alt))
    elif card_slug in ("stats", "activity", "snake"):
        parts.append(widget_card(card_slug, alt))
    else:
        parts.append(img_card(card_slug, alt))
    parts.append('<hr/>')

# Footer links
parts.append(
    '<p align="left">'
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
inline_count = sum(1 for _, _, _, inline in sections if inline)
print(f"Wrote {readme_path}  ({size_kb:.1f} KB)")
print(f"  inline SVG cards : {inline_count}")
print(f"  <img> cards      : {len(sections) - inline_count}")