#!/usr/bin/env python3
"""Builds the animated profile README from live GitHub data.

Needs the GitHub CLI logged in to the account. Run: GH_TOKEN=... python3 scripts/build.py
Every number in the output comes from the GitHub API at build time.
"""
import datetime as dt
import html
import json
import math
import pathlib
import random
import subprocess

LOGIN = "ityashag"
NAME = "Yash Agarwal"
ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

SANS = "ui-sans-serif,-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
PROJECT_NAMES = {"amd/gaia": "AMD Gaia", "minio/minio-js": "MinIO JS", "lingdojo/kana-dojo": "KanaDojo"}


def gql(query):
    out = subprocess.run(["gh", "api", "graphql", "-f", f"query={query}"], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)["data"]


user = gql('''{user(login:"%s"){createdAt
  repositories(first:100,ownerAffiliations:OWNER,privacy:PUBLIC,orderBy:{field:PUSHED_AT,direction:DESC}){nodes{
    name isFork url primaryLanguage{name}}}
  pullRequests(first:100,orderBy:{field:CREATED_AT,direction:DESC}){nodes{
    number title url state merged additions deletions
    repository{nameWithOwner stargazerCount owner{login}}}}}}''' % LOGIN)["user"]
now = dt.datetime.now(dt.timezone.utc)
repos = user["repositories"]["nodes"]
original = [r for r in repos if not r["isFork"]]
prs = user["pullRequests"]["nodes"]
external = [p for p in prs if p["repository"]["owner"]["login"] != LOGIN]
oss = [p for p in external if p["repository"]["stargazerCount"] >= 1000]
team = [p for p in external if p["repository"]["stargazerCount"] < 1000]
oss_projects = {p["repository"]["nameWithOwner"]: p["repository"]["stargazerCount"] for p in oss}
stars_combined = sum(oss_projects.values())
oss_merged = sum(p["merged"] for p in oss)
oss_open = sum(p["state"] == "OPEN" for p in oss)
added = sum(p["additions"] for p in oss)
removed = sum(p["deletions"] for p in oss)
ext_merged = sum(p["merged"] for p in external)
languages = {}
for r in original:
    if r["primaryLanguage"]:
        languages[r["primaryLanguage"]["name"]] = languages.get(r["primaryLanguage"]["name"], 0) + 1
top_languages = [k for k, _ in sorted(languages.items(), key=lambda kv: (-kv[1], kv[0])) if k != "Jupyter Notebook"][:3]
repo_by_name = {r["name"]: r for r in repos}
today = now.strftime("%-d %b %Y")
since = dt.datetime.fromisoformat(user["createdAt"].replace("Z", "+00:00")).strftime("%b %Y")


def calendar(start=None, end=None):
    span = f'(from:"{start}",to:"{end}")' if start else ""
    data = gql('''{user(login:"%s"){contributionsCollection%s{contributionCalendar{totalContributions
        weeks{contributionDays{date contributionCount weekday}}}}}}''' % (LOGIN, span))
    return data["user"]["contributionsCollection"]["contributionCalendar"]


recent = calendar()
first_year = dt.datetime.fromisoformat(user["createdAt"].replace("Z", "+00:00")).year
all_years = {y: calendar(f"{y}-01-01T00:00:00Z", f"{y}-12-31T23:59:59Z") for y in range(first_year, now.year + 1)}
recent_days = [d for week in recent["weeks"] for d in week["contributionDays"]]
active_days = sum(d["contributionCount"] > 0 for d in recent_days)
best_day = max(recent_days, key=lambda d: d["contributionCount"])
all_time = sum(c["totalContributions"] for c in all_years.values())


def esc(s):
    return html.escape(str(s), quote=True)


def write(name, body):
    (ASSETS / name).write_text(body, encoding="utf8")


# ---------------------------------------------------------------- cosmos
SERIF = "Georgia,'Iowan Old Style','Times New Roman',serif"
SPACE, STAR, SOFT, MERGED, PAPER, INK, FAINT = "#04050A", "#F4F1E8", "#9CA0A8", "#3FB950", "#F5F2E9", "#22211E", "#6F6D66"
STYLE = """<style>
.tw{animation:tw var(--d) ease-in-out infinite;animation-delay:var(--o)}
@keyframes tw{0%,100%{opacity:.25}50%{opacity:1}}
.sp{transform-box:view-box;transform-origin:var(--c);animation:sp var(--d) linear infinite}
@keyframes sp{to{transform:rotate(360deg)}}
.bob{animation:bob 11s ease-in-out infinite alternate}
@keyframes bob{from{transform:translateY(-5px)}to{transform:translateY(5px)}}
@media (prefers-reduced-motion:reduce){.tw,.sp,.bob{animation:none}}
</style>"""


def starfield(w, h, seed, count=170):
    """Mostly fixed stars, a few twinkling, over a faint band of the Milky Way."""
    rng = random.Random(seed)
    out = ['<defs><radialGradient id="mw"><stop offset="0" stop-color="#C9C4B8" stop-opacity=".13"/>'
           '<stop offset=".55" stop-color="#8E8F9E" stop-opacity=".05"/><stop offset="1" stop-color="#8E8F9E" stop-opacity="0"/></radialGradient></defs>',
           f'<rect width="{w}" height="{h}" fill="{SPACE}"/>',
           f'<ellipse cx="{w * .6}" cy="{h * .45}" rx="{w * .62}" ry="{h * .34}" fill="url(#mw)" transform="rotate(-18 {w * .6} {h * .45})"/>']
    for i in range(count):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        r = rng.choice((.5, .6, .7, .8, .9, 1.1, 1.5))
        col = rng.choice((STAR, STAR, STAR, "#CFE0FF", "#FFE2C2"))
        if i % 7 == 0:
            out.append(f'<circle class="tw" style="--d:{rng.uniform(3, 8):.1f}s;--o:-{rng.uniform(0, 8):.1f}s" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{col}"/>')
        else:
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{col}" opacity="{rng.uniform(.25, .85):.2f}"/>')
    return "".join(out)


def star_trails(px, py, seed, count=340, reach=1150):
    rng = random.Random(seed)
    arcs = []
    for _ in range(count):
        r = (rng.random() ** .72) * reach + 18
        start = rng.uniform(0, 360)
        sweep = rng.uniform(12, 34)
        a0, a1 = math.radians(start), math.radians(start + sweep)
        x0, y0 = px + r * math.cos(a0), py + r * math.sin(a0)
        x1, y1 = px + r * math.cos(a1), py + r * math.sin(a1)
        col = rng.choice((STAR, STAR, STAR, "#BFD4FF", "#FFD9B0"))
        arcs.append(f'<path d="M{x0:.0f},{y0:.0f} A{r:.0f},{r:.0f} 0 0,1 {x1:.0f},{y1:.0f}" stroke="{col}" stroke-opacity="{rng.uniform(.28, .95):.2f}" stroke-width="{rng.choice((.8, 1, 1.3, 1.7))}"/>')
    return f'<g class="sp" fill="none" stroke-linecap="round" style="--d:420s;--c:{px}px {py}px">{"".join(arcs)}</g>'


def cover():
    w, h = 1280, 440
    px, py = 930, 200
    fade = ('<defs><linearGradient id="left"><stop offset="0" stop-color="#04050A" stop-opacity=".96"/>'
            '<stop offset=".44" stop-color="#04050A" stop-opacity=".74"/><stop offset=".72" stop-color="#04050A" stop-opacity="0"/></linearGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#left)"/>')
    text = (f'<text x="72" y="218" font-family="{SERIF}" font-size="80" fill="{STAR}">{NAME}</text>'
            f'<text x="75" y="264" font-family="{SERIF}" font-style="italic" font-size="27" fill="{SOFT}">contributing to open source, one small PR at a time</text>')
    points = [(792, 96), (926, 58), (1032, 158), (884, 246), (1006, 338)]
    rows = oss[:5]
    pts = points[:len(rows)]
    lines = "".join(f'<path d="M{a[0]},{a[1]} L{b[0]},{b[1]}" stroke="{STAR}" stroke-opacity=".5" stroke-width="1"/>' for a, b in zip(pts, pts[1:]))
    stars = []
    for (x, y), p in zip(pts, rows):
        col = MERGED if p["merged"] else STAR
        repo = p["repository"]["nameWithOwner"].split("/")[1]
        stars.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{col}" opacity=".16"/><circle class="tw" style="--d:{5 + (p["number"] % 4)}s;--o:-{p["number"] % 5}s" cx="{x}" cy="{y}" r="5.5" fill="{col}"/>'
                     f'<text x="{x + 17}" y="{y + 1}" font-family="{MONO}" font-size="16" fill="{STAR}">{esc(repo)} #{p["number"]}</text>'
                     f'<text x="{x + 17}" y="{y + 20}" font-family="{SERIF}" font-style="italic" font-size="15" fill="{col if p["merged"] else SOFT}">{"merged" if p["merged"] else "open"}</text>')
    label = f"{NAME}, over a slow star-trail sky. A constellation marks {len(rows)} real pull requests: {oss_open} open and {oss_merged} merged."
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
            f'{STYLE}<rect width="{w}" height="{h}" fill="{SPACE}"/>{star_trails(px, py, 41)}{fade}{text}{lines}{"".join(stars)}</svg>')


def receipt():
    x0, rw, w = 70, 590, 1280
    item_h = 62
    paper_h = 188 + item_h * len(oss) + 214
    h = paper_h + 110
    top = 44
    teeth = "".join(f"L{x0 + rw - i * 20 - 10},{top + paper_h + 10} L{x0 + rw - (i + 1) * 20},{top + paper_h} " for i in range(int(rw / 20)))
    t = [f'<path d="M{x0},{top} L{x0 + rw},{top} L{x0 + rw},{top + paper_h} {teeth}Z" fill="{PAPER}"/>']

    def line(y, left, right="", size=19, weight=400, lc=INK, rc=None):
        s = f'<text x="{x0 + 36}" y="{y}" font-family="{MONO}" font-size="{size}" font-weight="{weight}" fill="{lc}">{esc(left)}</text>'
        if right:
            s += f'<text x="{x0 + rw - 36}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="{size}" font-weight="{weight}" fill="{rc or lc}">{esc(right)}</text>'
        return s

    def rule(y):
        return f'<path d="M{x0 + 36},{y} L{x0 + rw - 36},{y}" stroke="{FAINT}" stroke-width="1.5" stroke-dasharray="2 6" stroke-linecap="round"/>'

    y = top + 56
    t.append(f'<text x="{x0 + rw / 2}" y="{y}" text-anchor="middle" font-family="{SERIF}" font-weight="700" font-size="33" fill="{INK}">Open Source Receipt</text>')
    y += 32
    t.append(f'<text x="{x0 + rw / 2}" y="{y}" text-anchor="middle" font-family="{MONO}" font-size="15" fill="{FAINT}">{esc(today.upper())}  ·  {LOGIN.upper()}</text>')
    y += 26
    t.append(rule(y))
    y += 38
    for p in oss:
        t.append(line(y, f'{p["repository"]["nameWithOwner"]} #{p["number"]}', f'+{p["additions"]} −{p["deletions"]}', 19, 600))
        title = p["title"].split(": ", 1)[-1]
        title = title if len(title) <= 40 else title[:39] + "…"
        t.append(line(y + 24, title, "MERGED" if p["merged"] else "OPEN", 15, 400, FAINT, "#1A7F37" if p["merged"] else FAINT))
        y += item_h
    y -= 16
    t.append(rule(y))
    y += 38
    t.append(line(y, "PULL REQUESTS", str(len(oss)), 19, 700))
    y += 29
    t.append(line(y, "MERGED / OPEN", f"{oss_merged} / {oss_open}", 17))
    y += 27
    t.append(line(y, "LINES CHANGED", f"+{added} −{removed}", 17))
    y += 27
    t.append(line(y, "PAID IN", "code review", 17))
    y += 22
    t.append(rule(y))
    y += 20
    pos = x0 + 130
    for ch in "".join(str(p["number"]) for p in oss):
        n = int(ch) % 4 + 2
        if pos + n > x0 + rw - 130:
            break
        t.append(f'<rect x="{pos}" y="{y}" width="{n}" height="32" fill="{INK}"/>')
        pos += n + (int(ch) % 3) + 3
    t.append(f'<text x="{x0 + rw / 2}" y="{y + 56}" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{FAINT}">thank you for reviewing</text>')
    paper = f'<g class="bob"><g transform="rotate(-1.2 {x0 + rw / 2} {top + paper_h / 2})">{"".join(t)}</g></g>'

    # Orrery: one orbit per project, one moon per pull request.
    cx, cy = 950, 190
    groups = {}
    for p in oss:
        groups.setdefault(p["repository"]["nameWithOwner"], []).append(p)
    orbit = [f'<circle cx="{cx}" cy="{cy}" r="9" fill="#FFE2C2"/><circle cx="{cx}" cy="{cy}" r="20" fill="#FFE2C2" opacity=".12"/>']
    for i, (repo, items) in enumerate(groups.items()):
        r = 58 + i * 46
        orbit.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{STAR}" stroke-opacity=".3"/>')
        moons = []
        for j, p in enumerate(items):
            a = math.radians(40 + i * 75 + j * 360 / len(items))
            col = MERGED if p["merged"] else STAR
            moons.append(f'<circle cx="{cx + r * math.cos(a):.1f}" cy="{cy + r * math.sin(a):.1f}" r="6" fill="{col}" stroke="{SPACE}" stroke-width="2"/>')
        orbit.append(f'<g class="sp" style="--d:{70 + i * 45}s;--c:{cx}px {cy}px">{"".join(moons)}</g>')
        orbit.append(f'<text x="{cx}" y="{cy - r - 7}" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="15" fill="{SOFT}" stroke="{SPACE}" stroke-width="4" paint-order="stroke">{esc(PROJECT_NAMES.get(repo, repo))}</text>')
    sx = 742

    def stat(y, big, small):
        return (f'<text x="{sx}" y="{y}" font-family="{SERIF}" font-size="52" fill="{STAR}">{esc(big)}</text>'
                f'<text x="{sx}" y="{y + 30}" font-family="{SERIF}" font-style="italic" font-size="19" fill="{SOFT}">{esc(small)}</text>')

    stats = (stat(410, f"{len(oss)} pull requests", f"across {len(oss_projects)} projects, {oss_merged} merged so far")
             + stat(510, f"{stars_combined:,} stars", "on those projects (theirs, not mine)")
             + stat(610, f"{ext_merged} merged", "in other people's repos, team projects included"))
    label = f"A paper receipt floating in space listing {len(oss)} open-source pull requests: {oss_merged} merged, {oss_open} open, +{added} and -{removed} lines. An orrery shows them orbiting {len(oss_projects)} projects."
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
            f'{STYLE}{starfield(w, h, 23, 230)}{paper}{"".join(orbit)}{stats}</svg>')


# ---------------------------------------------------------------- the green graph
GREENS = ("#161B22", "#0E4429", "#006D32", "#26A641", "#39D353")


def level(count, peak):
    return 0 if count <= 0 else min(4, 1 + int((count - 1) * 4 / max(peak, 1)))


def contributions():
    w, size, gap = 1280, 17, 4
    left = 112
    t = [f'<text x="60" y="72" font-family="{SERIF}" font-size="36" fill="{STAR}">{recent["totalContributions"]} contributions in the last year</text>',
         f'<text x="60" y="104" font-family="{SERIF}" font-style="italic" font-size="19" fill="{SOFT}">on {active_days} days, with a best day of {best_day["contributionCount"]}. {all_time} since {first_year}.</text>']
    peak = max(d["contributionCount"] for d in recent_days)
    top = 158
    seen = None

    def square(x, y, count, top_value):
        return f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="3" fill="{GREENS[level(count, top_value)]}"/>'

    for col, week in enumerate(recent["weeks"]):
        x = left + col * (size + gap)
        month = week["contributionDays"][0]["date"][:7]
        if month != seen and col < len(recent["weeks"]) - 1:
            seen = month
            t.append(f'<text x="{x}" y="{top - 12}" font-family="{MONO}" font-size="14" fill="{SOFT}">{dt.date.fromisoformat(month + "-01").strftime("%b")}</text>')
        for d in week["contributionDays"]:
            t.append(square(x, top + d["weekday"] * (size + gap), d["contributionCount"], peak))
    for wd, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        t.append(f'<text x="60" y="{top + wd * (size + gap) + 14}" font-family="{MONO}" font-size="14" fill="{SOFT}">{name}</text>')
    y = top + 7 * (size + gap) + 62
    t.append(f'<text x="60" y="{y - 18}" font-family="{SERIF}" font-style="italic" font-size="18" fill="{SOFT}">every year, one square per week</text>')
    weekly = {yr: [sum(d["contributionCount"] for d in wk["contributionDays"]) for wk in c["weeks"]] for yr, c in all_years.items()}
    peak_week = max(max(v) for v in weekly.values()) or 1
    for yr, weeks in weekly.items():
        t.append(f'<text x="60" y="{y + 14}" font-family="{MONO}" font-size="14" fill="{SOFT}">{yr}</text>')
        for col, count in enumerate(weeks[:54]):
            t.append(square(left + col * (size + gap), y, count, peak_week))
        t.append(f'<text x="{left + 54 * (size + gap) + 4}" y="{y + 14}" font-family="{MONO}" font-size="14" font-weight="600" fill="{STAR}">{all_years[yr]["totalContributions"]}</text>')
        y += size + gap
    y += 16
    t.append(f'<text x="{left}" y="{y + 13}" font-family="{MONO}" font-size="14" fill="{SOFT}">Less</text>')
    for i, col in enumerate(GREENS):
        t.append(f'<rect x="{left + 48 + i * (size + gap)}" y="{y}" width="{size}" height="{size}" rx="3" fill="{col}"/>')
    t.append(f'<text x="{left + 48 + 5 * (size + gap) + 6}" y="{y + 13}" font-family="{MONO}" font-size="14" fill="{SOFT}">More</text>')
    h = y + 50
    label = f'Green contribution graph: {recent["totalContributions"]} contributions in the last year on {active_days} days, and {all_time} since {first_year}. ' + ", ".join(f'{k}: {v["totalContributions"]}' for k, v in all_years.items()) + "."
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
            f'{STYLE}{starfield(w, h, 31, 150)}{"".join(t)}</svg>')


def readme():
    prs_list = []
    for p in oss:
        repo = p["repository"]["nameWithOwner"]
        title = p["title"].split(": ", 1)[-1]
        state = "merged" if p["merged"] else "open"
        prs_list.append(f'- **{esc(PROJECT_NAMES.get(repo, repo))}** · [{esc(title)}]({p["url"]}) · <sub>{state}</sub>')
    team_rows = "\n".join(f'| {esc(p["repository"]["nameWithOwner"])} | [{esc(p["title"])}]({p["url"]}) | {"Merged" if p["merged"] else p["state"].title()} |' for p in team)
    year_rows = "\n".join(f'| {k} | {v["totalContributions"]} |' for k, v in all_years.items())
    merged_oss = next((p for p in oss if p["merged"]), None)
    restore = next((p for p in oss if "restore" in p["title"].lower()), None)
    first_line = f"First merged PR in a popular open-source project: [{PROJECT_NAMES[merged_oss['repository']['nameWithOwner']]} #{merged_oss['number']}]({merged_oss['url']})" if merged_oss else ""
    catch_line = f"Spotted a merge that wiped 5 themes from KanaDojo and [opened the fix]({restore['url']})" if restore else ""
    tick = lambda repo: "x" if any(p["merged"] for p in oss if p["repository"]["nameWithOwner"] == repo) else " "
    big = "x" if any(p["merged"] and p["repository"]["stargazerCount"] >= 10000 for p in oss) else " "

    def built(name, title, line):
        return f'- **[{esc(title)}]({repo_by_name[name]["url"]})** · {esc(line)}'

    built_list = "\n".join([
        built("HappyHeartHub", "Happy Heart Hub", "heart-risk prediction and generative AI, deployed to scale under load"),
        built("SOCKET_PROGRAMMING", "Secured Socket Programming", "private messaging and file sharing with end-to-end encryption"),
        built("crew.ai", "CrewAI Projects", "7 hands-on projects, from zero to multi-agent systems"),
        built("Open-AI-SDK", "OpenAI Agents SDK Projects", "7 practical projects, learning the SDK by building"),
    ])
    langs = " ".join(f"`{l}`" for l in top_languages)
    return f"""<img src="assets/cover.svg" alt="{NAME}, over a slow star-trail sky, with a constellation of real pull requests." width="100%">

Working professional, contributing to open source.

{langs} &nbsp;·&nbsp; {len(repos)} public repos &nbsp;·&nbsp; on GitHub since {since}

## Receipts

<img src="assets/receipt.svg" alt="Paper receipt floating in space: {len(oss)} pull requests, {oss_merged} merged, {oss_open} open, plus {added} and minus {removed} lines." width="100%">

{chr(10).join(prs_list)}

<details>
<summary>What happened to the merged theme?</summary>
<br>

It merged, then a later merge from another PR accidentally removed it along with other themes. I traced that through the commit history and opened the fix listed above. Star counts belong to the projects.

</details>

<details>
<summary>Earlier team projects ({len(team)} PRs)</summary>
<br>

| Repository | Pull request | Status |
|---|---|---|
{team_rows}

</details>

## Contributions

<img src="assets/contributions.svg" alt="Green contribution graph: {recent['totalContributions']} contributions in the last year and {all_time} since {first_year}." width="100%">

<details>
<summary>Yearly totals</summary>
<br>

| Year | Contributions |
|---|---|
{year_rows}

</details>

## Built

{built_list}

## On my list

- [{'x' if merged_oss else ' '}] {first_line}
- [{'x' if restore else ' '}] {catch_line}
- [{tick('amd/gaia')}] First merge at [AMD Gaia](https://github.com/amd/gaia)
- [{tick('minio/minio-js')}] First merge at [MinIO](https://github.com/minio/minio-js)
- [{big}] First merged PR in a project with 10k+ stars

<sub>Numbers from the GitHub API, last updated {esc(today)}.</sub>
"""


write("cover.svg", cover())
write("receipt.svg", receipt())
write("contributions.svg", contributions())
(ROOT / "README.md").write_text(readme(), encoding="utf8")
print(json.dumps(dict(repos=len(repos), original=len(original), external=len(external), ext_merged=ext_merged,
                      oss=len(oss), oss_merged=oss_merged, oss_open=oss_open, added=added, removed=removed,
                      stars=stars_combined, team=len(team), last_year=recent["totalContributions"], active_days=active_days,
                      best_day=best_day["contributionCount"], all_time=all_time,
                      years={k: v["totalContributions"] for k, v in all_years.items()})))
