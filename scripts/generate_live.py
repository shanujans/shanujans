"""
generate_live.py

Renders all 10 terminal-style SVG cards + 11 section bars for a GitHub profile README.

Live data:
  - GITHUB_TOKEN env var (optional but recommended)
  - Public repos count, account created_at -> uptime string, total commits -> live

Static data (edit terminal_data.json to change):
  - Bio, education, skills, tools, projects, certs, contact URLs, IDE list,
    language buckets, focus areas, last_known_loc fallback for lines-of-code

Run:
  GITHUB_TOKEN=$(gh auth token) python scripts/generate_live.py

Outputs to:
  /tmp/repo/assets/*.svg

Refreshed by:
  .github/workflows/refresh-terminal.yml (every 6 hours, manual dispatch also).
"""

import sys, os, json, datetime, pyfiglet, requests
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from terminal_card import build_card, GREEN, BLUE, ORANGE, GREY, DIM   # noqa: E402

ASSETS = Path("/tmp/repo/assets")
ASSETS.mkdir(exist_ok=True)

with open(ROOT / "terminal_data.json", encoding="utf-8") as f:
    DATA = json.load(f)

GITHUB_USER = DATA["github_target_user"]
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "shanujans-terminal-refresh"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


# ---------------------------------------------------------------- fetch ----
def fetch_user():
    try:
        r = requests.get(
            f"https://api.github.com/users/{GITHUB_USER}",
            headers=HEADERS, timeout=30,
        )
        if r.status_code != 200:
            print(f"  /users -> HTTP {r.status_code}; fallback to terminal_data.json")
            return None
        j = r.json()
        return {"created_at": j.get("created_at"), "public_repos": j.get("public_repos")}
    except requests.RequestException as e:
        print(f"  /users -> network error: {e}; fallback to terminal_data.json")
        return None


def fetch_total_commits():
    try:
        r = requests.get(
            f"https://api.github.com/search/commits?q=author:{GITHUB_USER}",
            headers={**HEADERS, "Accept": "application/vnd.github.cloak-preview+json"},
            timeout=30,
        )
        if r.status_code != 200:
            print(f"  /search/commits -> HTTP {r.status_code}; fallback")
            return None
        return r.json().get("total_count")
    except requests.RequestException as e:
        print(f"  /search/commits -> network error: {e}; fallback")
        return None


def fetch_repos_meta():
    """Pull owned repos (first 100) for repo-count consistency and any future LOC work."""
    try:
        r = requests.get(
            f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100&type=owner",
            headers=HEADERS, timeout=30,
        )
        if r.status_code != 200:
            print(f"  /repos -> HTTP {r.status_code}; fallback")
            return []
        return r.json()
    except requests.RequestException:
        return []


def fetch_contributed_to():
    """GraphQL: total unique repos user has contributed PRs/issues/etc to. Needs token."""
    if not GITHUB_TOKEN:
        return None
    q = (
        'query { user(login: "%s") { '
        'repositoriesContributedTo(first: 1, includeUserRepositories: false, '
        'contributionTypes: [PULL_REQUEST, PULL_REQUEST_REVIEW, ISSUE, REPOSITORY]) { '
        'totalCount } } }'
    ) % GITHUB_USER
    try:
        r = requests.post(
            "https://api.github.com/graphql",
            json={"query": q},
            headers=HEADERS, timeout=30,
        )
        if r.status_code != 200:
            print(f"  GraphQL -> HTTP {r.status_code}; fallback")
            return None
        payload = r.json().get("data", {}).get("user", {})
        if not payload:
            return None
        return payload["repositoriesContributedTo"]["totalCount"]
    except requests.RequestException as e:
        print(f"  GraphQL network error: {e}; fallback")
        return None


def uptime_str(created_at_iso, fallback_iso):
    for iso in (created_at_iso, fallback_iso):
        if not iso:
            continue
        try:
            created = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        except ValueError:
            continue
        now = datetime.datetime.now(datetime.timezone.utc)
        delta = now - created
        days = max(delta.days, 0)
        years, rem = divmod(days, 365)
        months, rdays = divmod(rem, 30)
        if years > 0:
            return f"{years}y {months}m {rdays}d on GitHub"
        if months > 0:
            return f"{months}m {rdays}d on GitHub"
        return f"{days}d on GitHub"
    return "—"


def now_utc_str():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


# Build live + computed values
user = fetch_user()
public_repos = (user or {}).get("public_repos")
created_at = (user or {}).get("created_at")
commits_total = fetch_total_commits()
repos_meta = fetch_repos_meta()
contributed_to = fetch_contributed_to()

LIVE = {
    "public_repos": public_repos if public_repos is not None else DATA.get("public_repos_fallback", 28),
    "contributed_to": contributed_to if contributed_to is not None else DATA.get("contributed_to_fallback", 32),
    "commits_total": commits_total if commits_total is not None else DATA.get("commits_total_fallback", 580),
    "created_at":    created_at or DATA.get("uptime_seed_iso"),
    "uptime":        uptime_str(created_at, DATA.get("uptime_seed_iso")),
    "last_synced":   now_utc_str(),
    "lines_loc":     DATA["last_known_loc"]["lines"],
    "additions_loc": DATA["last_known_loc"]["additions"],
    "deletions_loc": DATA["last_known_loc"]["deletions"],
}

print("\n== LIVE VALUES ==")
for k, v in LIVE.items():
    print(f"  {k}: {v}")
print()


# --------------------------------------------------------------- builders --

def card_hero():
    name_art = pyfiglet.figlet_format(DATA["display_name_figlet"], font="small")
    c = DATA["contact"]
    return [
        ("ascii", name_art, ORANGE),
        ("plain", DATA["tagline"], GREY),
        ("blank",),
        ("plain", "$ whoami", ORANGE, True),
        ("plain", DATA["whoami"], BLUE),
        ("blank",),
        ("section", "- Connect -"),
        ("linkfield", "Portfolio", c["portfolio"]["display"], c["portfolio"]["url"]),
        ("linkfield", "Email",    c["email"]["display"],     c["email"]["url"]),
        ("field",    "Status",    DATA["status"]),
        ("blank",),
        ("comment", f"// last synced {LIVE['last_synced']}"),
        ("prompt",),
    ]


def card_meta():
    return [
        ("field",     "OS",     DATA["os"]),
        ("field2",    "Uptime", LIVE["uptime"], GREEN),
        ("field",     "Host",   DATA["host"]),
        ("field",     "Kernel", DATA["kernel"]),
        ("field",     "Shell",  DATA["shell"]),
        ("field",     "IDE",    DATA["ide"]),
        ("blank",),
        ("comment",   f"// uptime live from GitHub `created_at` ({LIVE['created_at']})"),
        ("prompt",),
    ]


def card_languages():
    return [
        ("section",   "- Languages.Programming -"),
        ("plain",     DATA["languages_programming"], BLUE),
        ("blank",),
        ("section",   "- Languages.Markup -"),
        ("plain",     DATA["languages_markup"], BLUE),
        ("blank",),
        ("section",   "- Languages.Real -"),
        ("plain",     DATA["languages_real"], BLUE),
        ("blank",),
        ("comment",   "// three buckets you actually use"),
        ("prompt",),
    ]


def card_focus():
    return [
        ("field2", "Focus.AI",         DATA["focus_ai"],         GREEN),
        ("field2", "Focus.Automation", DATA["focus_automation"], GREEN),
        ("field2", "Focus.QA",         DATA["focus_qa"],         ORANGE),
        ("field2", "Focus.Cloud",      DATA["focus_cloud"],      ORANGE),
        ("blank",),
        ("comment", "// current focus stack -- numbers next to each are real, not aspirational"),
        ("prompt",),
    ]


def card_about():
    items = [
        ("field", "Name",       DATA["name"]),
        ("field", "Location",   "Sri Lanka"),
        ("field", "Role",       DATA["kernel"]),
        ("field", "Education",  DATA["shell"]),
        ("field", "Philosophy", '"Connecting dots others dont see."'),
        ("blank",),
        ("section", "- Skills.Confident -"),
    ]
    for label, value in DATA["skills_confident"]:
        items.append(("field", label, value))
    items.append(("blank",))
    items.append(("section", "- Skills.Learning -"))
    for label, value in DATA["skills_learning"]:
        items.append(("field", label, value))
    items += [
        ("blank",),
        ("comment", "// honest about skills -- no inflated claims, ever"),
        ("prompt",),
    ]
    return items


def card_tools():
    items = []
    for label, value in DATA["tools"]:
        items.append(("field", label, value))
    items += [
        ("blank",),
        ("comment", "// some projects below were AI-assisted -- I can explain & modify every line"),
        ("prompt",),
    ]
    return items


def card_projects():
    items = []
    for p in DATA["projects"]:
        items.append(("section", f"- {p['title']} -"))
        items.append(("linkplain", p["title"].split(". ", 1)[-1], p["url"]))
        items.append(("field",    "desc",   p["desc"]))
        items.append(("field",    "stack",  p["stack"]))
        if p.get("status"):
            color = GREEN if p.get("status_color") == "GREEN" else BLUE
            items.append(("field2",  "status", p["status"], color))
        items.append(("blank",))
    items += [
        ("comment", "// tap a title below to open the project"),
        ("prompt",),
    ]
    return items


def card_certifications():
    items = []
    for cert in DATA["certifications"]:
        items.append(("linkfield", cert["name"], cert["issuer"], cert["verify_url"]))
    items += [
        ("blank",),
        ("comment", "// 8 certifications -- 4 IBM, 3 Cisco, 1 Google Cloud"),
        ("prompt",),
    ]
    return items


def card_stats():
    repos_str    = f"{LIVE['public_repos']} {{Contributed: {LIVE['contributed_to']}}}"
    commits_str  = f"{LIVE['commits_total']}"
    loc_str      = f"{LIVE['lines_loc']:,} ( {LIVE['additions_loc']:,}++, {LIVE['deletions_loc']:,}-- )"
    return [
        ("field", "Repos",       repos_str),
        ("field", "Commits",     commits_str),
        ("field", "Lines of Code", loc_str),
        ("blank",),
        ("comment", f"// last synced {LIVE['last_synced']}"),
        ("prompt",),
    ]


def card_connect():
    c = DATA["contact"]
    return [
        ("linkplain2", "Open to:", "mailto:shanujansh@gmail.com?subject=IT%20Support%20opportunity", GREY, True),
        ("blank",),
        ("section", "- Reach Me -"),
        ("linkfield", "Email",     c["email"]["display"],     c["email"]["url"]),
        ("linkfield", "Portfolio", c["portfolio"]["display"], c["portfolio"]["url"]),
        ("linkfield", "GitHub",    c["github"]["display"],    c["github"]["url"]),
        ("linkfield", "LinkedIn",  c["linkedin"]["display"],  c["linkedin"]["url"]),
        ("blank",),
        ("comment", "// thanks for stopping by -- let's build something"),
        ("prompt",),
    ]


BARS = [
    ("about",          "whoami",                 "About Me"),
    ("meta",           "uname -a",               "System Meta"),
    ("languages",      "which -a --languages",   "Languages"),
    ("focus",          "focus --areas",          "Focus Areas"),
    ("tools",          "which -a --tools",       "Tools I Work With"),
    ("projects",       "ls ./projects --featured", "Featured Projects"),
    ("certifications", "cat certifications.log", "Certifications"),
    ("stats",          "gh stats --user shanujans", "GitHub Stats"),
    ("activity",       "gh activity --graph",    "Contribution Activity"),
    ("snake",          "./snake --eat contributions", "Contribution Snake"),
    ("connect",        "cat contact.md",          "Let's Connect"),
]


# ----------------------------------------------------------------- render --

CARDS = [
    ("hero",           card_hero,()),
    ("meta",           card_meta, ()),
    ("languages",      card_languages, ()),
    ("focus",          card_focus, ()),
    ("about",          card_about, ()),
    ("tools",          card_tools, ()),
    ("projects",       card_projects, ()),
    ("certifications", card_certifications, ()),
    ("stats",          card_stats, ()),
    ("connect",        card_connect, ()),
]

print("== RENDERING ==")
for slug, fn, _ in CARDS:
    out = ASSETS / f"terminal-{slug}.svg"
    build_card(DATA["username"], fn(), str(out))
    print(f"  wrote {out}")

for slug, cmd, label in BARS:
    out = ASSETS / f"bar-{slug}.svg"
    build_card(None, [("cmdheader", cmd, label)], str(out), with_header=False)
    print(f"  wrote {out}")

print(f"\nDone. {len(CARDS)} cards + {len(BARS)} bars regenerated.")
print(f"Last synced stamp on outputs: {LIVE['last_synced']}")

# ----------------------------------------------------------------- README --
print("\n== WRITING README.md (inlining clickable SVGs) ==")
import subprocess, sys
write_readme = ROOT / "write_readme.py"
if write_readme.exists():
    subprocess.run([sys.executable, str(write_readme), *([sys.argv[1]] if len(sys.argv) > 1 else [])], check=True)
else:
    print(f"  (write_readme.py not found at {write_readme}; skipping README rewrite)")
