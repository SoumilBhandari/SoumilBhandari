"""Builds the live GitHub cards in assets/: stats, languages, contribution heatmap.

    GH_TOKEN=... python scripts/stats.py

Runs daily from .github/workflows/stats.yml. If the API call fails it exits
without touching the existing SVGs, so the profile never shows a broken card.
"""

import json
import os
import subprocess
import sys
import urllib.request
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

from theme import GOLD, MUTED, TEXT, card_bg, esc, svg

ASSETS = Path(__file__).resolve().parent.parent / "assets"
USER = os.environ.get("GH_USER", "SoumilBhandari")
SKIP_LANGS = {"TeX", "Makefile", "Jupyter Notebook", "Dockerfile", "Batchfile", "CMake", "Procfile"}
LEVELS = {"NONE": "#1b1b1f", "FIRST_QUARTILE": "#3d3628", "SECOND_QUARTILE": "#6e6146",
          "THIRD_QUARTILE": "#a3916d", "FOURTH_QUARTILE": GOLD}

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""


def token():
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if tok:
        return tok
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token()}", "User-Agent": "profile-readme"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]["user"]


def streaks(days):
    counts = [(date.fromisoformat(d["date"]), d["contributionCount"]) for d in days]
    longest = run = 0
    for _, c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    current = 0
    # Today doesn't break the streak until it's over.
    tail = counts[:-1] if counts and counts[-1][1] == 0 else counts
    for _, c in reversed(tail):
        if not c:
            break
        current += 1
    return longest, current


def stats_card(user, days):
    cc = user["contributionsCollection"]
    longest, current = streaks(days)
    stars = sum(r["stargazerCount"] for r in user["repositories"]["nodes"])
    metrics = [
        (f"{cc['contributionCalendar']['totalContributions']:,}", "contributions"),
        (f"{cc['totalCommitContributions']:,}", "commits"),
        (f"{longest}d", "longest streak"),
        (f"{current}d", "current streak"),
        (f"{user['repositories']['totalCount']}", "public repos"),
        (f"{stars}", "stars earned"),
    ]
    W, H = 600, 270
    css = f"""
.hd {{ font-size: 13px; letter-spacing: 2px; fill: {GOLD}; }}
.v {{ font-size: 34px; font-weight: 700; fill: {TEXT}; }}
.l {{ font-size: 15px; fill: {MUTED}; }}
.m {{ animation: up 0.6s ease-out both; }}
@keyframes up {{ from {{ opacity: 0; transform: translateY(8px); }} }}
"""
    body = [card_bg(W, H), f'<text class="mono hd" x="36" y="52">GITHUB · LAST 12 MONTHS</text>']
    for i, (v, label) in enumerate(metrics):
        x, y = 36 + (i % 3) * 184, 124 + (i // 3) * 92
        body.append(f'<g class="m" style="animation-delay: {0.1 + i * 0.08:.2f}s">'
                    f'<text class="sans v" x="{x}" y="{y}">{esc(v)}</text>'
                    f'<text class="sans l" x="{x}" y="{y + 26}">{esc(label)}</text></g>')
    alt = ", ".join(f"{v} {label}" for v, label in metrics)
    return svg(W, H, "\n".join(body), css, f"GitHub stats: {alt}")


def languages_card(user):
    sizes, colors = defaultdict(int), {}
    for repo in user["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            name = e["node"]["name"]
            if name not in SKIP_LANGS:
                sizes[name] += e["size"]
                colors[name] = e["node"]["color"] or MUTED
    top = sorted(sizes.items(), key=lambda kv: -kv[1])[:6]
    total = sum(s for _, s in top)
    W, H = 600, 270
    bx, bw = 36, W - 72
    css = f"""
.hd {{ font-size: 13px; letter-spacing: 2px; fill: {GOLD}; }}
.ln {{ font-size: 16px; fill: {TEXT}; }}
.pc {{ font-size: 14px; fill: {MUTED}; }}
.bar {{ transform-origin: {bx}px 0; animation: grow 1.1s cubic-bezier(.2,.7,.2,1) 0.2s both; }}
@keyframes grow {{ from {{ transform: scaleX(0); }} }}
"""
    body = [card_bg(W, H), f'<text class="mono hd" x="36" y="52">TOP LANGUAGES · BY BYTES</text>',
            f'<defs><clipPath id="pill"><rect x="{bx}" y="80" width="{bw}" height="12" rx="6"/></clipPath></defs>',
            '<g clip-path="url(#pill)"><g class="bar">']
    x = bx
    for name, s in top:
        w = bw * s / total
        body.append(f'<rect x="{x:.1f}" y="80" width="{w + 0.5:.1f}" height="12" fill="{colors[name]}"/>')
        x += w
    body.append("</g></g>")
    for i, (name, s) in enumerate(top):
        cx, cy = 36 + (i % 2) * 270, 142 + (i // 2) * 42
        body.append(f'<circle cx="{cx + 6}" cy="{cy - 5}" r="6" fill="{colors[name]}"/>'
                    f'<text class="sans ln" x="{cx + 22}" y="{cy}">{esc(name)}</text>'
                    f'<text class="mono pc" x="{cx + 236}" y="{cy}" text-anchor="end">{100 * s / total:.1f}%</text>')
    alt = ", ".join(f"{n} {100 * s / total:.1f}%" for n, s in top)
    return svg(W, H, "\n".join(body), css, f"Top languages: {alt}")


def heatmap(user):
    cal = user["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    W, pitch, cell = 1200, 20, 15
    x0, y0 = 96, 92
    H = y0 + 7 * pitch + 28
    css = f"""
.hd {{ font-size: 20px; fill: {TEXT}; }}
.ax {{ font-size: 13px; fill: {MUTED}; }}
.d {{ animation: pop 0.5s ease-out both; }}
@keyframes pop {{ from {{ opacity: 0; }} }}
""" + "".join(f".w{i} {{ animation-delay: {0.2 + i * 0.022:.3f}s; }}" for i in range(len(weeks)))
    body = [card_bg(W, H, 18),
            f'<text class="sans hd" x="{x0}" y="50"><tspan fill="{GOLD}" font-weight="700">'
            f'{cal["totalContributions"]:,}</tspan> contributions in the last year</text>']
    # Legend
    lx = W - 48 - 5 * pitch - 40
    body.append(f'<text class="sans ax" x="{lx - 10}" y="49" text-anchor="end">less</text>')
    for i, c in enumerate(LEVELS.values()):
        body.append(f'<rect x="{lx + i * pitch}" y="37" width="{cell}" height="{cell}" rx="3" fill="{c}"/>')
    body.append(f'<text class="sans ax" x="{lx + 5 * pitch + 6}" y="49">more</text>')
    for r, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        body.append(f'<text class="sans ax" x="{x0 - 12}" y="{y0 + r * pitch + 12}" text-anchor="end">{label}</text>')
    last_month = None
    for wi, week in enumerate(weeks):
        first = date.fromisoformat(week["contributionDays"][0]["date"])
        if first.month != last_month and wi < len(weeks) - 2:
            if last_month is not None or first.day <= 7:
                body.append(f'<text class="sans ax" x="{x0 + wi * pitch}" y="{y0 - 12}">{first.strftime("%b")}</text>')
            last_month = first.month
        for day in week["contributionDays"]:
            r = (date.fromisoformat(day["date"]).weekday() + 1) % 7  # Sunday on top
            body.append(f'<rect class="d w{wi}" x="{x0 + wi * pitch}" y="{y0 + r * pitch}" width="{cell}" '
                        f'height="{cell}" rx="3" fill="{LEVELS[day["contributionLevel"]]}"/>')
    return svg(W, H, "\n".join(body), css, f"{cal['totalContributions']:,} contributions in the last year")


def main():
    try:
        user = fetch()
    except Exception as e:  # keep yesterday's cards rather than publish a broken one
        print(f"stats: GitHub API failed, leaving cards as they are: {e}", file=sys.stderr)
        return
    days = [d for w in user["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    ASSETS.mkdir(exist_ok=True)
    for name, text in (("stats.svg", stats_card(user, days)), ("languages.svg", languages_card(user)),
                       ("heatmap.svg", heatmap(user))):
        (ASSETS / name).write_text(text, encoding="utf-8")
        print(f"wrote assets/{name}")


if __name__ == "__main__":
    main()
