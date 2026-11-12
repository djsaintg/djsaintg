#!/usr/bin/env python3
"""Generate the profile's GitHub stats cards as static SVGs.

Replaces the public github-readme-stats service, which can go down or get
rate-limited. Runs in GitHub Actions with the built-in GITHUB_TOKEN and only
the Python standard library. Output: stats/overview.svg and stats/languages.svg
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path

USER = os.environ.get("STATS_USER", "djsaintg")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
OUT = Path(__file__).resolve().parents[2] / "stats"

# Tokyo Night, matching sponsor.svg
BG, BORDER, TITLE, TEXT, MUTED = "#0D1117", "#233041", "#7DCFFF", "#C0CAF5", "#565F89"
ACCENTS = ["#7DCFFF", "#BB9AF7", "#9ECE6A", "#E0AF68", "#F7768E", "#2AC3DE"]
FONT = "ui-monospace, 'SF Mono', 'Fira Code', Menlo, monospace"

QUERY = """
query($login: String!, $after: String) {
  user(login: $login) {
    contributionsCollection { totalCommitContributions restrictedContributionsCount }
    pullRequests { totalCount }
    issues { totalCount }
    repositoriesContributedTo(contributionTypes: [COMMIT, PULL_REQUEST, ISSUE]) { totalCount }
    releases: repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC) {
      nodes { releases { totalCount } }
    }
    repositories(first: 100, after: $after, ownerAffiliations: OWNER, privacy: PUBLIC) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        isFork
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""


def gql(variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        sys.exit(f"GraphQL error: {data['errors']}")
    return data["data"]["user"]


def collect():
    after, repos, user = None, [], None
    while True:
        user = gql({"login": USER, "after": after})
        page = user["repositories"]
        repos += page["nodes"]
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]
    own = [r for r in repos if not r["isFork"]]
    langs = {}
    for r in own:
        for e in r["languages"]["edges"]:
            name = e["node"]["name"]
            size, color = langs.get(name, (0, e["node"]["color"]))
            langs[name] = (size + e["size"], color or "#888")
    cc = user["contributionsCollection"]
    return {
        "stars": sum(r["stargazerCount"] for r in own),
        "commits": cc["totalCommitContributions"],
        "prs": user["pullRequests"]["totalCount"],
        "issues": user["issues"]["totalCount"],
        "repos": len(own),
        "contributed": user["repositoriesContributedTo"]["totalCount"],
        "releases": sum(r["releases"]["totalCount"] for r in user["releases"]["nodes"]),
        "langs": sorted(langs.items(), key=lambda kv: -kv[1][0]),
    }


def frame(w, h, title, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
        f"<title>{escape(title)}</title>"
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>'
        f'<circle cx="22" cy="24" r="5" fill="#F7768E"/><circle cx="40" cy="24" r="5" fill="#E0AF68"/>'
        f'<circle cx="58" cy="24" r="5" fill="#9ECE6A"/>'
        f'<text x="76" y="29" font-family="{FONT}" font-size="14" font-weight="600" fill="{TITLE}">{escape(title)}</text>'
        f"{body}</svg>"
    )


def overview(s):
    rows = [
        (f"Commits ({datetime.now(timezone.utc).year} so far)", s["commits"]),
        ("Public repos", s["repos"]),
        ("Releases shipped", s["releases"]),
        ("Total stars", s["stars"]),
        ("Pull requests", s["prs"]),
        ("Issues opened", s["issues"]),
        ("Contributed to", s["contributed"]),
    ]
    # Keep the first four always; only show the rest once they're non-zero
    rows = rows[:4] + [r for r in rows[4:] if r[1]]
    body = ""
    for i, (label, val) in enumerate(rows):
        y = 64 + i * 26
        body += (
            f'<text x="24" y="{y}" font-family="{FONT}" font-size="13"><tspan fill="{ACCENTS[i % len(ACCENTS)]}">$</tspan>'
            f'<tspan dx="9" fill="{TEXT}">{escape(label)}</tspan></text>'
            f'<text x="336" y="{y}" text-anchor="end" font-family="{FONT}" font-size="13" font-weight="700" fill="{TEXT}">{val:,}</text>'
        )
    return frame(360, 64 + len(rows) * 26, f"{USER} --stats", body)


def languages(s, top=6):
    langs = s["langs"][:top]
    total = sum(v[0] for _, v in langs) or 1
    body, x = "", 24
    bar_w = 312
    body += f'<clipPath id="bar"><rect x="24" y="48" width="{bar_w}" height="10" rx="5"/></clipPath><g clip-path="url(#bar)">'
    for name, (size, color) in langs:
        w = bar_w * size / total
        body += f'<rect x="{x:.1f}" y="48" width="{w + 0.5:.1f}" height="10" fill="{color}"/>'
        x += w
    body += "</g>"
    for i, (name, (size, color)) in enumerate(langs):
        col, row = i % 2, i // 2
        cx, cy = 30 + col * 160, 84 + row * 24
        body += (
            f'<circle cx="{cx}" cy="{cy - 4}" r="5" fill="{color}"/>'
            f'<text x="{cx + 12}" y="{cy}" font-family="{FONT}" font-size="12" fill="{TEXT}">{escape(name)} '
            f'<tspan fill="{MUTED}">{100 * size / total:.1f}%</tspan></text>'
        )
    rows = (len(langs) + 1) // 2
    return frame(360, 84 + rows * 24, f"{USER} --langs", body)


def main():
    if not TOKEN:
        sys.exit("Set GITHUB_TOKEN or GH_TOKEN")
    s = collect()
    OUT.mkdir(exist_ok=True)
    (OUT / "overview.svg").write_text(overview(s), encoding="utf-8")
    (OUT / "languages.svg").write_text(languages(s), encoding="utf-8")
    print(json.dumps({k: v for k, v in s.items() if k != "langs"}), [n for n, _ in s["langs"][:6]])


if __name__ == "__main__":
    main()
