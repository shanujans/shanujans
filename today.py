#!/usr/bin/env python3
"""
today.py

Calculates live GitHub statistics (repos, contributions, commits, stars,
followers, and total lines of code added/removed) and renders them into
two terminal-styled SVG cards (light_mode.svg / dark_mode.svg) that can be
embedded in a profile README using a <picture> tag so they switch with the
viewer's GitHub theme.

Requires an environment variable ACCESS_TOKEN with a GitHub Personal Access
Token (needs at least `read:user` and `repo` scopes to read private repo
stats; use `public_repo` only if you don't want private repos counted).

Usage (locally):
    ACCESS_TOKEN=ghp_xxx GH_USERNAME=yourname python today.py
"""

import os
import sys
import time
import datetime
from pathlib import Path

import requests

GITHUB_USERNAME = os.environ.get("GH_USERNAME", "shanujans")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
DISPLAY_NAME = os.environ.get("DISPLAY_NAME", "Shanujan Suresh")
ROLE = os.environ.get("DISPLAY_ROLE", "IT Support Professional")

API_URL = "https://api.github.com/graphql"
REST_ROOT = "https://api.github.com"

HEADERS = {
    "Authorization": f"bearer {ACCESS_TOKEN}",
    "Accept": "application/vnd.github+json",
}

ROOT = Path(__file__).parent
TEMPLATES = ROOT / "templates"


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def graphql(query: str, variables: dict | None = None) -> dict:
    resp = requests.post(
        API_URL,
        json={"query": query, "variables": variables or {}},
        headers=HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        fail(f"GraphQL error: {data['errors']}")
    return data["data"]


def get_user_overview() -> dict:
    query = """
    query($login: String!) {
      user(login: $login) {
        createdAt
        followers { totalCount }
        repositories(first: 100, ownerAffiliations: [OWNER], isFork: false, privacy: PUBLIC) {
          totalCount
          nodes { nameWithOwner stargazerCount }
        }
        contributionsCollection {
          totalCommitContributions
          totalRepositoriesWithContributedCommits
          restrictedContributionsCount
        }
      }
    }
    """
    data = graphql(query, {"login": GITHUB_USERNAME})
    return data["user"]


def get_lines_of_code(repo_names: list[str]) -> tuple[int, int]:
    """Sum additions/deletions attributed to GITHUB_USERNAME across repos
    using the /stats/contributors endpoint. GitHub computes this stat
    asynchronously; a 202 means "still generating", so we retry briefly."""
    total_add, total_del = 0, 0
    for full_name in repo_names:
        url = f"{REST_ROOT}/repos/{full_name}/stats/contributors"
        for attempt in range(3):
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 202:
                time.sleep(2)
                continue
            if r.status_code != 200:
                break
            for contributor in r.json() or []:
                author = contributor.get("author") or {}
                if author.get("login", "").lower() == GITHUB_USERNAME.lower():
                    for week in contributor.get("weeks", []):
                        total_add += week.get("a", 0)
                        total_del += week.get("d", 0)
            break
    return total_add, total_del


def human_age(created_at_iso: str) -> str:
    created = datetime.datetime.fromisoformat(created_at_iso.replace("Z", "+00:00"))
    now = datetime.datetime.now(datetime.timezone.utc)
    delta = now - created
    years = delta.days // 365
    days = delta.days % 365
    return f"{years}y {days}d on GitHub"


def fmt(n: int) -> str:
    return f"{n:,}"


def render(template_path: Path, output_path: Path, values: dict) -> None:
    svg = template_path.read_text(encoding="utf-8")
    for key, val in values.items():
        svg = svg.replace("{{" + key + "}}", str(val))
    output_path.write_text(svg, encoding="utf-8")
    print(f"Wrote {output_path}")


def main() -> None:
    if not ACCESS_TOKEN:
        fail("ACCESS_TOKEN environment variable is not set.")

    user = get_user_overview()

    repos = user["repositories"]["nodes"]
    repo_count = user["repositories"]["totalCount"]
    stars = sum(r["stargazerCount"] for r in repos)
    followers = user["followers"]["totalCount"]

    contrib = user["contributionsCollection"]
    commits = (
        contrib["totalCommitContributions"]
        + contrib["restrictedContributionsCount"]
    )
    contributed_to = contrib["totalRepositoriesWithContributedCommits"]

    repo_full_names = [r["nameWithOwner"] for r in repos]
    loc_add, loc_del = get_lines_of_code(repo_full_names)

    values = {
        "USERNAME": GITHUB_USERNAME,
        "NAME": DISPLAY_NAME,
        "ROLE": ROLE,
        "AGE": human_age(user["createdAt"]),
        "REPOS": fmt(repo_count),
        "CONTRIBUTED": fmt(contributed_to),
        "COMMITS": fmt(commits),
        "STARS": fmt(stars),
        "FOLLOWERS": fmt(followers),
        "LOC_ADD": fmt(loc_add),
        "LOC_DEL": fmt(loc_del),
        "GEN_DATE": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }

    render(TEMPLATES / "dark_mode.svg.template", ROOT / "dark_mode.svg", values)
    render(TEMPLATES / "light_mode.svg.template", ROOT / "light_mode.svg", values)


if __name__ == "__main__":
    main()
