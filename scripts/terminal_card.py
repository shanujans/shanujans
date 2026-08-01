import base64, html, os

BG      = "#0D1117"
ORANGE  = "#CA7938"
BLUE    = "#5299D2"
GREY    = "#A0B3BC"
DIM     = "#5C6773"
GREEN   = "#3FB950"
WHITE   = "#E6EDF3"

FONT_SIZE = 16
LINE_H    = 23
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


def build_line_svg(text, color=BLUE, bold=False, italic=False, width_chars=100, pad=2, pad_top=4, pad_bottom=4, link=None, out_path=None):
    canvas_w = int(PAD_X * 2 + width_chars * CHAR_W)
    canvas_h = int(pad_top + pad_bottom + LINE_H)

    svg_header = SVG_OPEN.format(
        w=canvas_w, h=canvas_h,
        REG=REG_B64, BOLD=BOLD_B64,
        FS=FONT_SIZE, ORANGE=ORANGE, BG=BG,
    )

    weight = "700" if bold else "400"
    style = 'font-style="italic"' if italic else ""
    y_pos = pad_top + LINE_H - 4
    if link:
        svg_line = (
            f'<text x="{PAD_X}" y="{y_pos}" {style} font-weight="{weight}" fill="{color}" xml:space="preserve">'
            f'<tspan><a xlink:href="{esc(link)}" target="_blank">{esc(text)}</a></tspan></text>'
        )
    else:
        svg_line = (
            f'<text x="{PAD_X}" y="{y_pos}" {style} font-weight="{weight}" fill="{color}" xml:space="preserve">{esc(text)}</text>'
        )

    svg = svg_header + "\n  " + svg_line + "\n" + SVG_CLOSE
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg)
    return svg


def build_field_line_svg(label, value, url, width_chars=100, pad=2, pad_top=4, pad_bottom=4, out_path=None):
    """Build a field line with: orange bold label, dim dots, blue linked value."""
    canvas_w = int(PAD_X * 2 + width_chars * CHAR_W)
    canvas_h = int(pad_top + pad_bottom + LINE_H)

    svg_header = SVG_OPEN.format(
        w=canvas_w, h=canvas_h,
        REG=REG_B64, BOLD=BOLD_B64,
        FS=FONT_SIZE, ORANGE=ORANGE, BG=BG,
    )

    # Compute dots for alignment
    prefix = f". {label}:"
    target_col = width_chars - len(value) - 3
    dots_n = max(3, target_col - len(prefix))
    dots = "." * dots_n

    y_pos = pad_top + LINE_H - 4
    svg_line = (
        f'<text x="{PAD_X}" y="{y_pos}" xml:space="preserve">'
        f'<tspan font-weight="700" fill="{ORANGE}">{esc(prefix)}</tspan>'
        f'<tspan fill="{DIM}"> {esc(dots)} </tspan>'
        f'<tspan fill="{BLUE}">'
        f'<tspan><a xlink:href="{esc(url)}" target="_blank">{esc(value)}</a></tspan>'
        f'</tspan></text>'
    )

    svg = svg_header + "\n  " + svg_line + "\n" + SVG_CLOSE
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg)
    return svg


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


def build_neofetch_card(username, items, out_path, min_width_chars=80):
    """Build a neofetch-style card with ascii art on left, fields on right."""
    # Separate ascii art from fields
    ascii_lines = []
    fields = []
    for it in items:
        if it[0] == "ascii":
            ascii_lines = it[1].rstrip("\n").split("\n")
        else:
            fields.append(it)

    # Build field lines
    field_items = []
    for it in fields:
        kind = it[0]
        if kind == "header":
            field_items.append(("header", it[1]))
        elif kind == "section":
            field_items.append(("section", it[1]))
        elif kind in ("field", "field2"):
            label, value = it[1], it[2]
            vcolor = it[3] if kind == "field2" else BLUE
            field_items.append(("field", label, value, vcolor))
        elif kind in ("linkfield", "linkfield2"):
            label, value, url = it[1], it[2], it[3]
            vcolor = it[4] if kind == "linkfield2" else BLUE
            field_items.append(("linkfield", label, value, url, vcolor))
        elif kind == "comment":
            field_items.append(("comment", it[1]))
        elif kind == "blank":
            field_items.append(("blank",))
        elif kind == "prompt":
            field_items.append(("prompt",))

    # ASCII column width (fixed for neofetch-style)
    ascii_col_w = 50
    # Total width = ascii_col_w + field_col_w + gap
    field_col_w = max(min_width_chars, 60)
    total_chars = ascii_col_w + field_col_w + 4

    total_lines = max(len(ascii_lines), len(field_items))
    canvas_w = int(PAD_X * 2 + total_chars * CHAR_W)
    canvas_h = int(PAD_TOP + PAD_BOTTOM + LINE_H * total_lines)

    svg_header = SVG_OPEN.format(
        w=canvas_w, h=canvas_h,
        REG=REG_B64, BOLD=BOLD_B64,
        FS=FONT_SIZE, ORANGE=ORANGE, BG=BG,
    )

    x_ascii = PAD_X
    x_fields = PAD_X + int((ascii_col_w + 2) * CHAR_W)

    svg_lines = []
    y = PAD_TOP + LINE_H - 4

    for i in range(total_lines):
        # Left side: ascii art (only for lines that have ascii)
        left_text = ""
        left_color = ORANGE
        if i < len(ascii_lines):
            left_text = ascii_lines[i]

        # Right side: fields
        right_svg = ""
        if i < len(field_items):
            f = field_items[i]
            kind = f[0]
            if kind == "header":
                text = f[1]
                tildes = "~" * max(0, field_col_w - len(text))
                right_svg = (
                    f'<tspan font-weight="700" fill="{WHITE}">{esc(text)}</tspan>'
                    f'<tspan fill="{GREY}">{esc(tildes)}</tspan>'
                )
            elif kind == "section":
                text = f[1]
                tildes = "~" * max(0, field_col_w - len(text))
                right_svg = (
                    f'<tspan font-weight="700" fill="{GREY}">{esc(text)}</tspan>'
                    f'<tspan fill="{DIM}">{esc(tildes)}</tspan>'
                )
            elif kind == "field":
                label, value, vcolor = f[1], f[2], f[3]
                prefix = f". {label}:"
                dots_n = max(3, field_col_w - len(prefix) - len(value) - 3)
                dots = "." * dots_n
                right_svg = (
                    f'<tspan font-weight="700" fill="{ORANGE}">{esc(prefix)}</tspan>'
                    f'<tspan fill="{DIM}"> {esc(dots)} </tspan>'
                    f'<tspan fill="{vcolor}">{esc(value)}</tspan>'
                )
            elif kind == "linkfield":
                label, value, url, vcolor = f[1], f[2], f[3], f[4]
                prefix = f". {label}:"
                dots_n = max(3, field_col_w - len(prefix) - len(value) - 3)
                dots = "." * dots_n
                right_svg = (
                    f'<tspan font-weight="700" fill="{ORANGE}">{esc(prefix)}</tspan>'
                    f'<tspan fill="{DIM}"> {esc(dots)} </tspan>'
                    f'<tspan fill="{vcolor}">'
                    f'<tspan><a xlink:href="{esc(url)}" target="_blank">{esc(value)}</a></tspan>'
                    f'</tspan>'
                )
            elif kind == "comment":
                right_svg = f'<tspan font-style="italic" fill="{DIM}">{esc(f[1])}</tspan>'
            elif kind == "blank":
                right_svg = ""
            elif kind == "prompt":
                right_svg = f'<tspan font-weight="700" fill="{ORANGE}">></tspan><tspan fill="{GREY}">_</tspan>'

        # Combine left and right in single text element per line
        if left_text or right_svg:
            parts = []
            if left_text:
                parts.append(f'<tspan fill="{left_color}">{esc(left_text)}</tspan>')
            if right_svg:
                # Add spacing between ascii and fields
                parts.append(f'<tspan x="{x_fields}" xml:space="preserve">{right_svg}</tspan>')
            svg_lines.append(
                f'<text x="{x_ascii}" y="{y}" xml:space="preserve">{"".join(parts)}</text>'
            )
        y += LINE_H

    body = "\n  ".join(svg_lines)
    svg = svg_header + "\n  " + body + "\n" + SVG_CLOSE
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    return canvas_w, canvas_h


def build_neofetch_svg(username, items, out_path, is_dark=True, data=None, live=None):
    """Exact neofetch-card hero matching the neofetch-card branch (height fixed to 800)."""
    if data is None:
        data = {}
    if live is None:
        live = {}

    ascii_art = [
        "********########################%%%#%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:.+@@@@@",
        "********#######################%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*.-%@@@@",
        "********#####################%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*.=@@@@@",
        "********###################%%%%%%%%###+***#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@*.=@@@@@",
        "********###################%%#*              +*%@@@@@@@@@@@@@@@@@@@@@@@@:++@@@@@",
        "********################%#%+.                   -#@@@@@@@@@@@@@@@@@@@@@@*:+@@@@@",
        "********################%+.                       =@@@@@@@@@@@@@@@@@@@@#:++@@@@@",
        "********################%%.                         +@@@@@@@@@@@@@@@@@@@::+@@@@@",
        "********##################.        ......:::.        *@@@@@@@@@@@@@@@@@@*:+@@@@@",
        "********##################     .:=+*##*######+--     *@@@@@@@@@@@@@@@@@@*:+@@@@@",
        "********#################%:   .=+**########****+-   =@@@@@@@@@@@@@@@@@@@*:+@@@@@",
        "********#################%*   :=+*#%%%%%%%%%#*+++.  #@@@@@@@@@@@@@@@@@@@*:+@@@@@",
        "********#################%%. -:.::::-*%@%#-..:-::= :@@@@@@@@@@@@@@@@@@@@*:+@@@@@",
        "********#################%%= =-:::.:.-#@#=.-.-::-+:*@@@@@@@@@@@@@@@@@@@@*:+@@@@@",
        "********###################*:+++=+-++=*%#+++-===++=**=%@@@@@@@@@@@@@@@@@*:*@@@@@",
        "********####################=+#%%%%%#**%**#%%%%%#+=*#=%@@@@@@@@@@@@@@@@@*:*@@@@@",
        "********################%%%+==#%@@%%**%@%*#%@@@%#==+#%@@@@@@@@@@@@@@@@@@*:*@@@@@",
        "********################%%%*+:=*%%##+-+**=*##%%#+-+*%@@@@@@@@@@@@@@@@@@@*:*@@@@@",
        "********################%%%#*--=+*++++++++==++*+-+#@@@@@@@@@@@@@@@@@@@@@*:*@@@@@",
        "********################%%%*##-===-:-=++*=-:-====%@@@@@@@@@@@@@@@@@@@@@@*:*@@@@@",
        "********################%%%##%+:--=+==-:--=+=-=-*@@@@@@@@@@@@@@@@@@@@@@@*:*@@@@@",
        "********################%%%##%*-..-=+*++++++-:.-#@@@@@@@@@@@@@@@@@@@@@@@*:*@@@@@",
        "********################%%%##%*=-. .:.::..:...-+*%@@@@@@@@@@@@@@@@@@@@@@*:*@@@@@",
        "********#################%%##+#+++=:       .-+**#+%@@@@@@@@@@@@@@@@@@@@@*:*@@@@@",
        "********#################%%*::@##**+===+==+*###%@-.*%@@@@@@@@@@@@@@@@@@@*.*@@@@@",
        "********#################*=  .%@@%###**+*###%%@@@-  .=*#%@@@@@@@@@@@@@@@+.*@@@@@",
        "********###############:       *@@@@%%%###%%%@@@@%        :-+*#%@@@@@@@@+.*@@@@@",
        "********###########:.        :%@@@@@#===*%@@@@@*             .:-+*#%@@@@+.*@@@@@",
        "********########.             :%@@@%:     .+%@@@%.                  .:@@+.*@@@@@",
        "********###:.                .%@@@%*=.  .+*%@@@#                        .-*@@@@@",
        "******:.                       *@@@@@@+  +@@@@@@-                        .:@@@@@",
        "**.:::                         .%@@@@#    #@@@@#                           .@@@@",
        "**.::.                          =@@@@-    =@@@%:                           :@@@@",
        "**.::.                           *@@%.    -@@@+                             :@@@",
        "**.::                            .%@%.    :@@#                              .:@@",
        "**.:.                             -%%.    :@%.                              .:@@",
        "**.:                               =%     :%-                                .:@",
        "**..                                :     .:                                 .:@",
        "**.                                                                           :@",
        "*.                                                                            .@  ",
    ]

    dots = {
        "OS": " ...................... ",
        "Uptime": " ........... ",
        "Host": " ............. ",
        "Kernel": " ....... ",
        "Shell": " ........... ",
        "IDE": " ............. ",
        "Languages.Programming": "   ",
        "Languages.Markup": " ........... ",
        "Languages.Real": " .............. ",
        "Focus.AI": " .............. ",
        "Focus.Automation": " ...... ",
        "Focus.QA": " .............. ",
        "Focus.Cloud": " ............ ",
        "Repos": " .......... ",
        "Commits": " ........ ",
        "Lines of Code": "   ",
        "Email": " .............. ",
        "Portfolio": " .......... ",
        "LinkedIn": " ............ ",
    }

    hdr_tildes = " -~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~-"
    contact_tildes = " -~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~-"
    stats_tildes = " -~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~-"

    if is_dark:
        bg = "#0d1117"
        header_color = "#c9d1d9"
        key_color = "#f0883e"
        value_color = "#58a6ff"
        cc_color = "#8b949e"
        ascii_color = "#6e7681"
        section_color = "#d2a8ff"
        add_color = "#3fb950"
        del_color = "#f85149"
        hover_color = "#79c0ff"
    else:
        bg = "#f6f8fa"
        header_color = "#24292f"
        key_color = "#953800"
        value_color = "#0969da"
        cc_color = "#57606a"
        ascii_color = "#8c959f"
        section_color = "#8250df"
        add_color = "#1a7f37"
        del_color = "#cf222e"
        hover_color = "#218bff"

    def esc(s):
        return html.escape(s, quote=False)

    os_val = data.get("os", "Windows, Android, Linux (basic)")
    uptime_val = live.get("uptime", "1y 3m 17d on GitHub")
    host_val = data.get("host", "Sri Lanka")
    kernel_val = data.get("kernel", "IT Support Professional (4+ yrs)")
    shell_val = data.get("shell", "BSc CS @ Univ. of the People")
    ide_val = data.get("ide", "VS Code, AI Studio, Git, OpenCode")
    lang_prog = data.get("languages_programming", "Python, TypeScript")
    lang_mark = data.get("languages_markup", "HTML, CSS, JSON, YAML")
    lang_real = data.get("languages_real", "English, Tamil")
    focus_ai = data.get("focus_ai", "Gemini API, AI Studio")
    focus_auto = data.get("focus_automation", "Cloudflare Workers, GitHub Actions")
    focus_qa = data.get("focus_qa", "Manual Testing (learning)")
    focus_cloud = data.get("focus_cloud", "AWS (basic), OCI (basic)")

    c = data.get("contact", {}) or {}
    email_url = (c.get("email") or {}).get("url", "mailto:shanujansh@gmail.com")
    email_disp = (c.get("email") or {}).get("display", "shanujansh@gmail.com")
    portfolio_url = (c.get("portfolio") or {}).get("url", "https://shanujan.is-a.dev")
    portfolio_disp = (c.get("portfolio") or {}).get("display", "shanujan.is-a.dev")
    linkedin_url = (c.get("linkedin") or {}).get("url", "https://www.linkedin.com/in/shanujansuresh/")
    linkedin_disp = "shanujansuresh"

    repos = str(live.get("public_repos", 58))
    contributed = str(live.get("contributed_to", 32))
    commits = str(live.get("commits_total", 536))
    loc = f"{int(live.get('lines_loc', 338640)):,}"
    add = f"{int(live.get('additions_loc', 4184343)):,}++"
    dele = f"{int(live.get('deletions_loc', 3845703)):,}--"
    last_synced = live.get("last_synced", "")

    def key_span(label):
        if "." in label:
            a, b = label.split(".", 1)
            return f'<tspan class="key">{esc(a)}</tspan>.<tspan class="key">{esc(b)}</tspan>'
        return f'<tspan class="key">{esc(label)}</tspan>'

    def field_html(label, value, underline=False):
        val_attr = ' text-decoration="underline"' if underline else ""
        return (
            key_span(label)
            + ":"
            + f'<tspan class="cc">{esc(dots.get(label, " ............ "))}</tspan>'
            + f'<tspan class="value"{val_attr}>{esc(value)}</tspan>'
        )

    def link_html(y, url, target, label, value):
        tgt = ' target="_blank"' if target else ""
        return (
            f'<a href="{esc(url)}"{tgt}><text x="783" y="{y}" font-size="16px">'
            '<tspan class="cc">. </tspan>'
            + field_html(label, value, underline=True)
            + "</text></a>"
        )

    header_tspan = f'<tspan x="783" y="30">{esc(username)}</tspan>{hdr_tildes}'

    def field_ts(y, label, value):
        return f'<tspan x="783" y="{y}" class="cc">. </tspan>' + field_html(label, value)

    right_tspans = [
        header_tspan,
        field_ts(55, "OS", os_val),
        field_ts(80, "Uptime", uptime_val),
        field_ts(105, "Host", host_val),
        field_ts(130, "Kernel", kernel_val),
        field_ts(155, "Shell", shell_val),
        field_ts(180, "IDE", ide_val),
        '<tspan x="783" y="205" class="cc">. </tspan>',
        field_ts(230, "Languages.Programming", lang_prog),
        field_ts(255, "Languages.Markup", lang_mark),
        field_ts(280, "Languages.Real", lang_real),
        '<tspan x="783" y="305" class="cc">. </tspan>',
        field_ts(330, "Focus.AI", focus_ai),
        field_ts(355, "Focus.Automation", focus_auto),
        field_ts(380, "Focus.QA", focus_qa),
        field_ts(405, "Focus.Cloud", focus_cloud),
        f'<tspan x="783" y="430" class="section">- Contact</tspan>{contact_tildes}',
    ]

    links = [
        link_html(455, email_url, False, "Email", email_disp),
        link_html(480, portfolio_url, True, "Portfolio", portfolio_disp),
        link_html(505, linkedin_url, True, "LinkedIn", linkedin_disp),
    ]

    stats_tspans = [
        f'<tspan x="783" y="535" class="section">- GitHub Stats</tspan>{stats_tildes}',
        f'<tspan x="783" y="560" class="cc">. </tspan><tspan class="key">Repos</tspan>:<tspan class="cc">{dots["Repos"]}</tspan><tspan class="value">{repos}</tspan> {{<tspan class="key">Contributed</tspan>: <tspan class="value">{contributed}</tspan>}}',
        f'<tspan x="783" y="585" class="cc">. </tspan><tspan class="key">Commits</tspan>:<tspan class="cc">{dots["Commits"]}</tspan><tspan class="value">{commits}</tspan>',
        f'<tspan x="783" y="610" class="cc">. </tspan><tspan class="key">Lines of Code</tspan>:<tspan class="cc">{dots["Lines of Code"]}</tspan><tspan class="value">{loc}</tspan> ( <tspan class="addColor">{add}</tspan>, <tspan class="delColor">{dele}</tspan> )',
        f'<tspan x="783" y="640" class="cc">// last synced {esc(last_synced)}</tspan>',
        '<tspan x="783" y="665" class="key">&#10095;</tspan> <tspan class="cursor cc">&#9615;</tspan>',
    ]

    svg = (
        f'<svg width="1480" height="800" font-family="ConsolasFallback,Consolas,monospace" font-size="16px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
        f"<style>\n"
        f"@font-face {{\n"
        f"  src: local('Consolas'), local('Consolas Bold');\n"
        f"  font-family: 'ConsolasFallback';\n"
        f"  font-display: swap;\n"
        f"  -webkit-size-adjust: 109%;\n"
        f"  size-adjust: 109%;\n"
        f"}}\n"
        f".key {{fill: {key_color};}}\n"
        f".value {{fill: {value_color};}}\n"
        f".addColor {{fill: {add_color};}}\n"
        f".delColor {{fill: {del_color};}}\n"
        f".cc {{fill: {cc_color};}}\n"
        f".ascii {{fill: {ascii_color};}}\n"
        f".section {{fill: {section_color};}}\n"
        f"text, tspan {{white-space: pre;}}\n"
        f"a text {{cursor: pointer;}}\n"
        f"a:hover .value {{fill: {hover_color};}}\n"
        f".cursor {{animation: blink 1s step-end infinite;}}\n"
        f"@keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}\n"
        f"</style>\n"
        f'<rect width="1480" height="800" fill="{bg}" rx="15"/>\n'
        f'<text x="15" y="30" class="ascii" font-size="12px">'
    )
    for i, line in enumerate(ascii_art):
        svg += f'\n<tspan x="15" y="{30 + i * 16}">{esc(line)}</tspan>'
    svg += '\n</text>'
    svg += f'\n<text x="783" y="30" fill="{header_color}">'
    for ts in right_tspans:
        svg += "\n" + ts
    svg += "\n</text>"
    for lk in links:
        svg += "\n" + lk
    svg += f'\n<text x="783" y="535" fill="{header_color}">'
    for ts in stats_tspans:
        svg += "\n" + ts
    svg += "\n</text>"
    svg += "\n</svg>\n"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    return 1480, 800
