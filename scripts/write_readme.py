import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = Path("/tmp/repo")
ASSETS = REPO / "assets"

with open(ROOT / "terminal_data.json", encoding="utf-8") as f:
    DATA = json.load(f)

CARD_W = 1028
BG = "#0D1117"
ORANGE = "#CA7938"
BLUE = "#5299D2"
GREY = "#A0B3BC"
DIM = "#5C6773"
GREEN = "#3FB950"
WHITE = "#E6EDF3"
FONT = "'Fira Code','Cascadia Code',Consolas,monospace"
FONT_SZ = 16
LINE_H = 23
PAD_X = 22
PAD_TOP = 26

def esc(s):
    return html.escape(s, quote=False)

def line_y(idx):
    return PAD_TOP + idx * LINE_H

def img_card(slug, alt):
    return f'<img src="assets/terminal-{slug}.svg" alt="{html.escape(alt)}" width="100%" style="display:block"/>'

def img_bar(slug, alt):
    return f'<img src="assets/bar-{slug}.svg" alt="{html.escape(alt)}" width="100%" style="display:block"/>'

def make_svg(lines, h):
    text_block = "\n".join(lines)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CARD_W} {h}" width="100%" style="display:block">\n'
        f'<rect width="100%" height="100%" fill="{BG}"/>\n'
        f'{text_block}\n'
        f'</svg>'
    )

def profile_views_svg():
    lines = [
        f'<text x="{PAD_X}" y="{line_y(0)}" font-family="{FONT}" font-size="{FONT_SZ}" font-style="italic" fill="{DIM}">// profile views</text>',
        f'<text x="{PAD_X}" y="{line_y(1)}" font-family="{FONT}" font-size="{FONT_SZ}" fill="{ORANGE}" font-weight="700">&gt;</text>',
        f'<text x="{PAD_X + 14}" y="{line_y(1)}" font-family="{FONT}" font-size="{FONT_SZ}" fill="{BLUE}"> cat visitors.log</text>',
        f'<text x="260" y="{line_y(1)}" font-family="{FONT}" font-size="{FONT_SZ}" fill="{DIM}">.................... # Views</text>',
    ]
    h = PAD_TOP + LINE_H * 3 + 16
    svg = make_svg(lines, h)
    badge = '<img src="https://komarev.com/ghpvc/?username=shanujans&style=flat-square&color=5299d2&label=PROFILE+VIEWS" alt="profile views" style="display:block;margin-top:4px"/>'
    return f'<div style="background:{BG};padding:0;line-height:0">{svg}{badge}</div>'

def connect_svg():
    c = DATA["contact"]
    entries = [
        ("Email",    c["email"]["url"],    c["email"]["display"]),
        ("Portfolio",c["portfolio"]["url"],c["portfolio"]["display"]),
        ("GitHub",   c["github"]["url"],   c["github"]["display"]),
        ("LinkedIn", c["linkedin"]["url"], c["linkedin"]["display"]),
    ]
    max_label = max(len(f". {e[0]}:") for e in entries)
    target_col = max_label + 3

    lines = [
        f'<text x="{PAD_X}" y="{line_y(0)}" font-family="{FONT}" font-size="{FONT_SZ}" fill="{WHITE}" font-weight="700">shanujans@github<tspan fill="{GREY}">~~~~~~~~~~~~~~~~~~~~~~~~</tspan></text>',
        f'<text x="{PAD_X}" y="{line_y(2)}" font-family="{FONT}" font-size="{FONT_SZ}" fill="{GREY}" font-weight="700">- Reach Me -<tspan fill="{DIM}">~~~~~~~~~~~~</tspan></text>',
    ]
    for i, (label, url, display) in enumerate(entries):
        idx = 4 + i
        prefix = f". {label}:"
        dots_n = max(3, target_col - len(prefix))
        dots = "." * dots_n
        lines.append(
            f'<text x="{PAD_X}" y="{line_y(idx)}" font-family="{FONT}" font-size="{FONT_SZ}" xml:space="preserve">'
            f'<tspan fill="{ORANGE}" font-weight="700">{esc(prefix)}</tspan>'
            f'<tspan fill="{DIM}"> {esc(dots)} </tspan>'
            f'<a href="{esc(url)}" target="_blank"><tspan fill="{BLUE}">{esc(display)}</tspan></a>'
            f'</text>'
        )
    comment_idx = 4 + len(entries)
    lines.append(
        f'<text x="{PAD_X}" y="{line_y(comment_idx)}" font-family="{FONT}" font-size="{FONT_SZ}" font-style="italic" fill="{DIM}">// thanks for stopping by -- let\'s build something</text>'
    )
    prompt_idx = comment_idx + 1
    lines.append(
        f'<text x="{PAD_X}" y="{line_y(prompt_idx)}" font-family="{FONT}" font-size="{FONT_SZ}" fill="{ORANGE}" font-weight="700">&gt;<tspan fill="{GREY}">_</tspan></text>'
    )
    h = PAD_TOP + (prompt_idx + 1) * LINE_H
    return make_svg(lines, h)

def widget_card(slug, alt):
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
parts.append(profile_views_svg())
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

parts.append(f'<div>\n{img_bar("connect", "$ connect")}\n{connect_svg()}\n</div>')
parts.append('<hr/>')

readme_md = "\n".join(parts) + "\n"
readme_path = REPO / "README.md"
readme_path.write_text(readme_md, encoding="utf-8")

size_kb = readme_path.stat().st_size / 1024
img_count = readme_md.count('<img src="assets/')
print(f"Wrote {readme_path}  ({size_kb:.1f} KB)")
print(f"  asset <img> tags: {img_count}")
