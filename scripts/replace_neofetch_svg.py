import html
import inspect


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


if __name__ == "__main__":
    src = inspect.getsource(build_neofetch_svg)
    path = "scripts/terminal_card.py"
    content = open(path, encoding="utf-8").read()
    idx = content.index("def build_neofetch_svg(")
    new_content = content[:idx].rstrip() + "\n\n\n" + src
    open(path, "w", encoding="utf-8").write(new_content)
    print("Replaced build_neofetch_svg in scripts/terminal_card.py")
