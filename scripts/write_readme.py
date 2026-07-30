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

def connect_terminal():
    c = DATA["contact"]
    return (
        '<div style="background:#0D1117;padding:26px 22px 22px;font-family:\'Courier New\',Consolas,monospace;font-size:16px;line-height:1.8;color:#E6EDF3">\n'
        '  <div><span style="font-weight:700;color:#E6EDF3">shanujans@github</span><span style="color:#A0B3BC;">~~~~~~~~~~~~~~~~~~~~~~~~</span></div>\n'
        '  <br/>\n'
        '  <div><span style="color:#A0B3BC;font-weight:700;">- Reach Me -</span><span style="color:#5C6773;">~~~~~~~~~~~~</span></div>\n'
        '  <br/>\n'
        f'  <div><span style="color:#CA7938;font-weight:700;">. Email:</span><span style="color:#5C6773;"> ....... </span><a href="{c["email"]["url"]}" style="color:#5299D2;text-decoration:none;">{c["email"]["display"]}</a></div>\n'
        f'  <div><span style="color:#CA7938;font-weight:700;">. Portfolio:</span><span style="color:#5C6773;"> ... </span><a href="{c["portfolio"]["url"]}" style="color:#5299D2;text-decoration:none;">{c["portfolio"]["display"]}</a></div>\n'
        f'  <div><span style="color:#CA7938;font-weight:700;">. GitHub:</span><span style="color:#5C6773;"> ..... </span><a href="{c["github"]["url"]}" style="color:#5299D2;text-decoration:none;">{c["github"]["display"]}</a></div>\n'
        f'  <div><span style="color:#CA7938;font-weight:700;">. LinkedIn:</span><span style="color:#5C6773;"> ... </span><a href="{c["linkedin"]["url"]}" style="color:#5299D2;text-decoration:none;">{c["linkedin"]["display"]}</a></div>\n'
        '  <br/>\n'
        '  <div style="color:#5C6773;font-style:italic;">// thanks for stopping by -- let\'s build something</div>\n'
        '  <div><span style="color:#CA7938;font-weight:700;">&gt;</span><span style="color:#A0B3BC;">_</span></div>\n'
        '</div>'
    )

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
parts.append(
    '<div style="background:#0D1117;padding:10px 22px;font-family:\'Courier New\',Consolas,monospace;font-size:16px;color:#E6EDF3">\n'
    '  <span style="color:#CA7938;font-weight:700;">$</span>\n'
    '  <span style="color:#5299D2;"> cat visitors.log</span>\n'
    '  <span style="color:#5C6773;"> ................... # Profile Views</span>\n'
    '</div>\n'
    '<p align="center">\n'
    '  <img src="https://komarev.com/ghpvc/?username=shanujans&style=flat-square&color=5299d2&label=PROFILE+VIEWS" alt="profile views"/>\n'
    '</p>'
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

parts.append(f'<div>\n{img_bar("connect", "$ connect")}\n{connect_terminal()}\n</div>')
parts.append('<hr/>')

readme_md = "\n".join(parts) + "\n"
readme_path = REPO / "README.md"
readme_path.write_text(readme_md, encoding="utf-8")

size_kb = readme_path.stat().st_size / 1024
img_count = readme_md.count('<img src="assets/')
print(f"Wrote {readme_path}  ({size_kb:.1f} KB)")
print(f"  asset <img> tags: {img_count}")
