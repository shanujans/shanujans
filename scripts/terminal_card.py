import base64, html, os

BG      = "#0D1117"
ORANGE  = "#CA7938"
BLUE    = "#5299D2"
GREY    = "#A0B3BC"
DIM     = "#5C6773"
GREEN   = "#3FB950"
WHITE   = "#E6EDF3"

FONT_SIZE = 15
LINE_H    = 21
PAD_X     = 22
PAD_TOP   = 26
PAD_BOTTOM = 22
CHAR_W    = FONT_SIZE * 1200 / 1950.0

_FONT_DIR = os.environ.get(
    "TERMINAL_FONT_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts"),
)

with open(os.path.join(_FONT_DIR, "FiraCode-Regular.subset.woff2"), "rb") as f:
    REG_B64 = base64.b64encode(f.read()).decode("ascii")
with open(os.path.join(_FONT_DIR, "FiraCode-Bold.subset.woff2"), "rb") as f:
    BOLD_B64 = base64.b64encode(f.read()).decode("ascii")


def esc(s):
    return html.escape(s, quote=False)


SVG_OPEN = '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <style>
      @font-face {{
        font-family: 'FiraCodeSubset';
        src: url(data:font/woff2;base64,{REG}) format('woff2');
        font-weight: 400;
      }}
      @font-face {{
        font-family: 'FiraCodeSubset';
        src: url(data:font/woff2;base64,{BOLD}) format('woff2');
        font-weight: 700;
      }}
      text {{
        font-family: 'FiraCodeSubset', 'Fira Code', 'Cascadia Code', Consolas, monospace;
        font-size: {FS}px;
        font-variant-ligatures: none;
        font-feature-settings: "liga" 0, "calt" 0;
      }}
      a {{ text-decoration: none; cursor: pointer; }}
      a:hover text {{ fill: {ORANGE}; }}
    </style>
  </defs>
  <rect x="0" y="0" width="{w}" height="{h}" fill="{BG}"/>'''

SVG_CLOSE = '</svg>'


def build_card(username_title, items, out_path, min_width_chars=0, with_header=True):
    pre = [("header", username_title + " -")] if with_header else []
    raw_items = pre + items

    all_items = []
    for it in raw_items:
        if it[0] == "ascii":
            _, text, color = it
            lines = text.rstrip("\n").split("\n")
            for ln in lines:
                if ln.strip() == "":
                    continue
                all_items.append(("asciiline", ln, color))
        else:
            all_items.append(it)

    field_prefixes = []
    for it in all_items:
        if it[0] in ("field", "field2", "linkfield", "linkfield2"):
            field_prefixes.append(f". {it[1]}:")
    target_col = (max(len(p) for p in field_prefixes) + 3) if field_prefixes else 0

    def line_len(it):
        if it[0] in ("header", "section"):
            return len(it[1])
        if it[0] in ("field", "field2", "linkfield", "linkfield2"):
            return target_col + 1 + len(it[2])
        if it[0] == "comment":
            return len(it[1])
        if it[0] in ("plain", "linkplain", "linkplain2"):
            return len(it[1])
        if it[0] == "asciiline":
            return len(it[1])
        if it[0] in ("cmdheader", "linkcmdheader"):
            cmd, label = it[1], it[2]
            return len(f"$ {cmd}") + 3 + len(f"# {label}")
        return 1

    max_chars = max(line_len(it) for it in all_items) + 2
    max_chars = max(max_chars, min_width_chars)

    canvas_w = int(PAD_X * 2 + max_chars * CHAR_W)
    canvas_h = int(PAD_TOP + PAD_BOTTOM + LINE_H * len(all_items))

    svg_header = SVG_OPEN.format(
        w=canvas_w, h=canvas_h,
        REG=REG_B64, BOLD=BOLD_B64,
        FS=FONT_SIZE, ORANGE=ORANGE, BG=BG,
    )

    svg_lines = []
    y = PAD_TOP
    for it in all_items:
        kind = it[0]
        if kind == "header":
            text = it[1]
            tildes = "~" * max(0, max_chars - len(text))
            svg_lines.append(
                f'<text x="{PAD_X}" y="{y}" xml:space="preserve">'
                f'<tspan font-weight="700" fill="{WHITE}">{esc(text)}</tspan>'
                f'<tspan fill="{GREY}">{esc(tildes)}</tspan></text>'
            )
        elif kind == "section":
            text = it[1]
            tildes = "~" * max(0, max_chars - len(text))
            svg_lines.append(
                f'<text x="{PAD_X}" y="{y}" xml:space="preserve">'
                f'<tspan font-weight="700" fill="{GREY}">{esc(text)}</tspan>'
                f'<tspan fill="{DIM}">{esc(tildes)}</tspan></text>'
            )
        elif kind in ("field", "field2"):
            label, value = it[1], it[2]
            vcolor = it[3] if kind == "field2" else BLUE
            prefix = f". {label}:"
            dots_n = max(3, target_col - len(prefix))
            dots = "." * dots_n
            svg_lines.append(
                f'<text x="{PAD_X}" y="{y}" xml:space="preserve">'
                f'<tspan font-weight="700" fill="{ORANGE}">{esc(prefix)}</tspan>'
                f'<tspan fill="{DIM}"> {esc(dots)} </tspan>'
                f'<tspan fill="{vcolor}">{esc(value)}</tspan></text>'
            )
        elif kind in ("linkfield", "linkfield2"):
            label, value, url = it[1], it[2], it[3]
            vcolor = it[4] if kind == "linkfield2" else BLUE
            prefix = f". {label}:"
            dots_n = max(3, target_col - len(prefix))
            dots = "." * dots_n
            svg_lines.append(
                f'<text x="{PAD_X}" y="{y}" xml:space="preserve">'
                f'<tspan font-weight="700" fill="{ORANGE}">{esc(prefix)}</tspan>'
                f'<tspan fill="{DIM}"> {esc(dots)} </tspan>'
                f'<tspan fill="{vcolor}">'
                f'<tspan><a xlink:href="{esc(url)}" target="_blank">{esc(value)}</a></tspan>'
                f'</tspan></text>'
            )
        elif kind == "comment":
            svg_lines.append(
                f'<text x="{PAD_X}" y="{y}" font-style="italic" fill="{DIM}" xml:space="preserve">{esc(it[1])}</text>'
            )
        elif kind == "prompt":
            svg_lines.append(
                f'<text x="{PAD_X}" y="{y}" font-weight="700" fill="{ORANGE}">&gt;<tspan fill="{GREY}">_</tspan></text>'
            )
        elif kind == "plain":
            text = it[1]
            color = it[2] if len(it) > 2 else BLUE
            bold = "700" if (len(it) > 3 and it[3]) else "400"
            svg_lines.append(
                f'<text x="{PAD_X}" y="{y}" font-weight="{bold}" fill="{color}" xml:space="preserve">{esc(text)}</text>'
            )
        elif kind == "linkplain":
            text, url = it[1], it[2]
            svg_lines.append(
                f'<text x="{PAD_X}" y="{y}" xml:space="preserve">'
                f'<tspan><a xlink:href="{esc(url)}" target="_blank">'
                f'<tspan fill="{BLUE}">{esc(text)}</tspan></a></tspan></text>'
            )
        elif kind == "linkplain2":
            text, url, color = it[1], it[2], it[3]
            bold = "700" if (len(it) > 4 and it[4]) else "400"
            svg_lines.append(
                f'<text x="{PAD_X}" y="{y}" font-weight="{bold}" xml:space="preserve">'
                f'<tspan><a xlink:href="{esc(url)}" target="_blank">'
                f'<tspan fill="{color}">{esc(text)}</tspan></a></tspan></text>'
            )
        elif kind == "asciiline":
            text, color = it[1], it[2]
            svg_lines.append(
                f'<text x="{PAD_X}" y="{y}" font-weight="700" fill="{color}" xml:space="preserve">{esc(text)}</text>'
            )
        elif kind == "cmdheader":
            cmd, label = it[1], it[2]
            prefix = f"$ {cmd}"
            dots_n = max(2, max_chars - len(prefix) - len(f"# {label}") - 2)
            dots = " " * dots_n
            svg_lines.append(
                f'<text x="{PAD_X}" y="{y}" xml:space="preserve">'
                f'<tspan font-weight="700" fill="{ORANGE}">$</tspan>'
                f'<tspan fill="{BLUE}"> {esc(cmd)}</tspan>'
                f'<tspan fill="{DIM}">{esc(dots)}# {esc(label)}</tspan></text>'
            )
        elif kind == "linkcmdheader":
            cmd, label, url = it[1], it[2], it[3]
            prefix = f"$ {cmd}"
            dots_n = max(2, max_chars - len(prefix) - len(f"# {label}") - 2)
            dots = " " * dots_n
            svg_lines.append(
                f'<text x="{PAD_X}" y="{y}" xml:space="preserve">'
                f'<tspan><a xlink:href="{esc(url)}" target="_blank">'
                f'<tspan font-weight="700" fill="{ORANGE}">$</tspan>'
                f'<tspan fill="{BLUE}"> {esc(cmd)}</tspan>'
                f'</a></tspan>'
                f'<tspan fill="{DIM}">{esc(dots)}# {esc(label)}</tspan></text>'
            )
        y += LINE_H

    body = "\n  ".join(svg_lines)
    svg = svg_header + "\n  " + body + "\n" + SVG_CLOSE
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    return canvas_w, canvas_h
