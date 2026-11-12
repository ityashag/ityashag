#!/usr/bin/env python3
"""Builds the animated profile README from live GitHub data.

Needs the GitHub CLI logged in to the account. Run: GH_TOKEN=... python3 scripts/build.py
Every number in the output comes from the GitHub API at build time.
"""
import datetime as dt
import html
import json
import re
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
PROJECT_NAMES = {"amd/gaia": "AMD Gaia", "minio/minio-js": "MinIO JS", "lingdojo/kana-dojo": "KanaDojo", "jenkinsci/jenkins": "Jenkins"}


def gql(query):
    out = subprocess.run(["gh", "api", "graphql", "-f", f"query={query}"], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)["data"]


user = gql('''{user(login:"%s"){createdAt
  repositories(first:100,ownerAffiliations:OWNER,privacy:PUBLIC,orderBy:{field:PUSHED_AT,direction:DESC}){nodes{
    name isFork url primaryLanguage{name}}}}}''' % LOGIN)["user"]
prs, cursor = [], None
while True:
    after = f',after:"{cursor}"' if cursor else ""
    page = gql('''{user(login:"%s"){pullRequests(first:50%s,orderBy:{field:CREATED_AT,direction:DESC}){
      pageInfo{hasNextPage endCursor}
      nodes{number title url state merged additions deletions body
        repository{nameWithOwner stargazerCount owner{login}}
        files(first:100){nodes{path additions deletions}}}}}}''' % (LOGIN, after))["user"]["pullRequests"]
    prs += page["nodes"]
    if not page["pageInfo"]["hasNextPage"]:
        break
    cursor = page["pageInfo"]["endCursor"]
now = dt.datetime.now(dt.timezone.utc)
repos = user["repositories"]["nodes"]
original = [r for r in repos if not r["isFork"]]
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
.draw{stroke-dasharray:var(--l);stroke-dashoffset:var(--l);animation:draw 1.1s ease-out forwards;animation-delay:var(--o)}
@keyframes draw{to{stroke-dashoffset:0}}
.rise{opacity:0;animation:rise .9s ease-out forwards;animation-delay:var(--o)}
@keyframes rise{to{opacity:1}}
.pulse{transform-box:fill-box;transform-origin:center;opacity:0;animation:pulse 3.6s ease-out infinite;animation-delay:var(--o)}
@keyframes pulse{0%{transform:scale(.7);opacity:.5}100%{transform:scale(2.8);opacity:0}}
.meteor{opacity:0;animation:meteor var(--d) linear infinite;animation-delay:var(--o)}
@keyframes meteor{0%{transform:translate(0,0);opacity:0}1.5%{opacity:.9}7%{transform:translate(-300px,150px);opacity:0}100%{transform:translate(-300px,150px);opacity:0}}
@media (prefers-reduced-motion:reduce){.tw,.sp,.bob,.pulse,.meteor{animation:none}.draw{animation:none;stroke-dashoffset:0}.rise{animation:none;opacity:1}}
</style>"""


# The conventional-commit type in a PR title, as a kind of work.
KINDS = {"fix": "Bug fixes", "docs": "Docs", "test": "Tests", "feat": "Features", "theme": "Features",
         "perf": "Performance", "chore": "Cleanup", "refactor": "Cleanup", "style": "Cleanup", "ci": "Build and CI"}
# Areas of each codebase by path prefix; the first match wins.
AREAS = {
    "amd/gaia": [("tui/", "Terminal app"), ("src/gaia/apps/webui/", "Agent UI"), ("src/gaia/ui/", "Agent UI backend"),
                 ("src/gaia/upload_names.py", "Agent UI backend"), ("src/gaia/code_index/", "Code search"),
                 ("src/gaia/rag/", "Document Q&A"), ("src/gaia/llm/", "Model client"),
                 ("src/gaia/agents/tools/", "Agent tools"), ("src/gaia/agents/", "Agents and installs"),
                 ("src/gaia/hub/", "Agents and installs"), ("src/gaia/cli.py", "Command line"),
                 ("website/", "Website"), ("docs/", "Docs")],
    "lingdojo/kana-dojo": [("community/", "Community themes")],
    "minio/minio-js": [("src/IamAwsProvider", "AWS credentials"), ("src/", "Client library")],
}
LANGS = {".py": "Python", ".ts": "TypeScript", ".tsx": "TypeScript", ".go": "Go", ".css": "CSS", ".js": "JavaScript",
         ".json": "JSON", ".md": "Markdown", ".mdx": "Markdown"}
CODE_EXT = (".py", ".ts", ".tsx", ".go", ".js", ".css")
TEST_PATH = re.compile(r"(^|/)(tests?|__tests__|visual)/|_test\.go$|\.test\.[jt]sx?$|(^|/)test_[^/]+\.py$")


def kind(p):
    m = re.match(r"(\w+)(\([^)]*\))?!?:", p["title"])
    return KINDS.get(m.group(1).lower(), "Other") if m else "Other"


def files(p):
    return (p.get("files") or {}).get("nodes") or []


def area_of(repo, path):
    for prefix, name in AREAS.get(repo, []):
        if path.startswith(prefix):
            return name
    return path.split("/")[0] if "/" in path else PROJECT_NAMES.get(repo, repo)


def main_area(p):
    """Where most of a PR's non-test lines went."""
    repo = p["repository"]["nameWithOwner"]
    changed = [f for f in files(p) if not TEST_PATH.search(f["path"])] or files(p)
    weight = {}
    for f in changed:
        a = area_of(repo, f["path"])
        weight[a] = weight.get(a, 0) + f["additions"] + f["deletions"]
    return max(weight, key=weight.get) if weight else PROJECT_NAMES.get(repo, repo)


def is_code_fix(p):
    return kind(p) == "Bug fixes" and any(
        f["path"].endswith(CODE_EXT) and not f["path"].startswith("docs/") for f in files(p))


def has_tests(p):
    return any(TEST_PATH.search(f["path"]) for f in files(p))


def language_share(items):
    """Each language's share of the lines changed, largest first."""
    lines = {}
    for p in items:
        for f in files(p):
            lang = LANGS.get(pathlib.PurePosixPath(f["path"]).suffix)
            if lang:
                lines[lang] = lines.get(lang, 0) + f["additions"] + f["deletions"]
    total = sum(lines.values()) or 1
    return [(lang, round(100 * n / total)) for lang, n in sorted(lines.items(), key=lambda kv: -kv[1])]


def area_rows():
    """One row per project area: its PRs newest first."""
    rows = {}
    for p in oss:
        key = (PROJECT_NAMES.get(p["repository"]["nameWithOwner"], p["repository"]["nameWithOwner"]), main_area(p))
        rows.setdefault(key, []).append(p)
    return sorted(rows.items(), key=lambda kv: (-len(kv[1]), kv[0]))


def summary():
    """Everything the receipt and README say about the work, from the PRs themselves."""
    by_project = {}
    kinds = {}
    for p in oss:
        by_project.setdefault(PROJECT_NAMES.get(p["repository"]["nameWithOwner"], p["repository"]["nameWithOwner"]), []).append(p)
        kinds[kind(p)] = kinds.get(kind(p), 0) + 1
    code_fixes = [p for p in oss if is_code_fix(p)]
    return {
        "projects": sorted(by_project.items(), key=lambda kv: -len(kv[1])),
        "kinds": sorted(kinds.items(), key=lambda kv: -kv[1]),
        "code_fixes": code_fixes,
        "tested": sum(has_tests(p) for p in code_fixes),
        "areas": area_rows(),
        "langs": language_share(oss),
    }


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
    return f'<g class="sp" fill="none" stroke-linecap="round" style="--d:170s;--c:{px}px {py}px">{"".join(arcs)}</g>'


def cover():
    w, h = 1280, 440
    px, py = 930, 200
    fade = ('<defs><linearGradient id="left"><stop offset="0" stop-color="#04050A" stop-opacity=".96"/>'
            '<stop offset=".44" stop-color="#04050A" stop-opacity=".74"/><stop offset=".72" stop-color="#04050A" stop-opacity="0"/></linearGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#left)"/>')
    text = (f'<text x="72" y="218" font-family="{SERIF}" font-size="80" fill="{STAR}">{NAME}</text>'
            f'<text x="75" y="264" font-family="{SERIF}" font-style="italic" font-size="27" fill="{SOFT}">contributing to open source, one small PR at a time</text>')
    projects = list(dict.fromkeys(PROJECT_NAMES.get(p["repository"]["nameWithOwner"], p["repository"]["nameWithOwner"]) for p in oss))
    text += (f'<text x="76" y="306" font-family="{MONO}" font-size="16" fill="{SOFT}">'
             f'{oss_merged} merged · {oss_open} open · {esc(", ".join(projects))}</text>')
    points = [(792, 96), (926, 58), (1032, 158), (884, 246), (1006, 338)]
    rows = oss[:5]
    pts = points[:len(rows)]
    lines = "".join(
        f'<path class="draw" style="--l:{math.dist(a, b):.0f};--o:{.6 + i * .7:.1f}s" d="M{a[0]},{a[1]} L{b[0]},{b[1]}" stroke="{STAR}" stroke-opacity=".5" stroke-width="1"/>'
        for i, (a, b) in enumerate(zip(pts, pts[1:])))
    stars = []
    for i, ((x, y), p) in enumerate(zip(pts, rows)):
        col = MERGED if p["merged"] else STAR
        repo = p["repository"]["nameWithOwner"].split("/")[1]
        ring = (f'<circle class="pulse" style="--o:{2 + i * .9:.1f}s" cx="{x}" cy="{y}" r="9" fill="none" stroke="{MERGED}" stroke-width="1.5"/>'
                if p["merged"] else "")
        stars.append(f'<g class="rise" style="--o:{.2 + i * .7:.1f}s">{ring}<circle cx="{x}" cy="{y}" r="11" fill="{col}" opacity=".16"/><circle class="tw" style="--d:{5 + (p["number"] % 4)}s;--o:-{p["number"] % 5}s" cx="{x}" cy="{y}" r="5.5" fill="{col}"/>'
                     f'<text x="{x + 17}" y="{y + 1}" font-family="{MONO}" font-size="16" fill="{STAR}">{esc(repo)} #{p["number"]}</text>'
                     f'<text x="{x + 17}" y="{y + 20}" font-family="{SERIF}" font-style="italic" font-size="15" fill="{col if p["merged"] else SOFT}">{"merged" if p["merged"] else "open"}</text></g>')
    meteors = "".join(
        f'<line class="meteor" style="--d:{d}s;--o:{o}s" x1="{x}" y1="{y}" x2="{x + 46}" y2="{y - 23}" stroke="{STAR}" stroke-width="1.3" stroke-linecap="round"/>'
        for x, y, d, o in ((640, 40, 11, 3), (520, 120, 17, 9)))
    label = f"{NAME}, over a slow star-trail sky. A constellation marks {len(rows)} real pull requests: {oss_open} open and {oss_merged} merged."
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
            f'{STYLE}<rect width="{w}" height="{h}" fill="{SPACE}"/>{star_trails(px, py, 41)}{fade}{meteors}{text}{lines}{"".join(stars)}</svg>')


def receipt():
    x0, rw, w = 70, 590, 1280
    top = 44
    t = []

    def line(y, left, right="", size=19, weight=400, lc=INK, rc=None):
        s = f'<text x="{x0 + 36}" y="{y}" font-family="{MONO}" font-size="{size}" font-weight="{weight}" fill="{lc}">{esc(left)}</text>'
        if right:
            s += f'<text x="{x0 + rw - 36}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="{size}" font-weight="{weight}" fill="{rc or lc}">{esc(right)}</text>'
        return s

    def rule(y):
        return f'<path d="M{x0 + 36},{y} L{x0 + rw - 36},{y}" stroke="{FAINT}" stroke-width="1.5" stroke-dasharray="2 6" stroke-linecap="round"/>'

    sm = summary()
    y = top + 56
    t.append(f'<text x="{x0 + rw / 2}" y="{y}" text-anchor="middle" font-family="{SERIF}" font-weight="700" font-size="33" fill="{INK}">Open Source Receipt</text>')
    y += 32
    t.append(f'<text x="{x0 + rw / 2}" y="{y}" text-anchor="middle" font-family="{MONO}" font-size="15" fill="{FAINT}">{esc(today.upper())}  ·  {LOGIN.upper()}</text>')

    def section(y, title, rows):
        y += 26
        t.append(rule(y))
        y += 34
        t.append(line(y, title, "", 14, 700, FAINT))
        for left, right, strong in rows:
            y += 28
            t.append(line(y, left, right, 17, 700 if strong else 400))
        return y

    shown = sm["projects"][:4]
    rows = [(name, f'{sum(p["merged"] for p in items)} merged · {sum(not p["merged"] for p in items)} open', False) for name, items in shown]
    if len(sm["projects"]) > len(shown):
        rows.append((f'+ {len(sm["projects"]) - len(shown)} more projects', "", False))
    y = section(y, "PROJECTS", rows)
    rows = [(k, str(n), False) for k, n in sm["kinds"]]
    rows.append(("CODE FIXES WITH TESTS", f'{sm["tested"]} / {len(sm["code_fixes"])}', True))
    y = section(y, "WORK", rows)
    y = section(y, "WHERE IN THE CODE", [(area, f'{len(items)} PR{"s" if len(items) > 1 else ""}', False) for (_, area), items in sm["areas"][:6]])
    y = section(y, "LANGUAGES", [(" · ".join(f"{lang} {pct}%" for lang, pct in sm["langs"][:3]), "", False)])
    y += 26
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
    paper_h = y + 84 - top
    h = max(paper_h + 110, 720)
    teeth = "".join(f"L{x0 + rw - i * 20 - 10},{top + paper_h + 10} L{x0 + rw - (i + 1) * 20},{top + paper_h} " for i in range(int(rw / 20)))
    t.insert(0, f'<path d="M{x0},{top} L{x0 + rw},{top} L{x0 + rw},{top + paper_h} {teeth}Z" fill="{PAPER}"/>')
    paper = f'<g class="bob"><g transform="rotate(-1.2 {x0 + rw / 2} {top + paper_h / 2})">{"".join(t)}</g></g>'

    # Orrery: one orbit per project, one moon per pull request.
    # The orbits share a fixed width, so more projects pack closer instead of
    # growing into the receipt, the stats or off the top of the image.
    outer = 172
    cx, cy = 950, outer + 44
    groups = {}
    for p in oss:
        groups.setdefault(p["repository"]["nameWithOwner"], []).append(p)
    # The busiest project gets the widest orbit, so its moons have room.
    rings = sorted(groups.items(), key=lambda kv: (len(kv[1]), kv[0]))
    step = min(46, (outer - 52) / max(1, len(rings) - 1))
    radii = [outer - (len(rings) - 1 - i) * step for i in range(len(rings))]
    # One moon size for every orbit, shrinking only when the widest one fills up.
    widest = max(len(items) for _, items in rings)
    moon = min(6.0, max(2.5, 2 * math.pi * radii[-1] / widest / 3.2))
    orbit = [f'<circle cx="{cx}" cy="{cy}" r="9" fill="#FFE2C2"/><circle cx="{cx}" cy="{cy}" r="20" fill="#FFE2C2" opacity=".12"/>']
    for i, ((repo, items), r) in enumerate(zip(rings, radii)):
        orbit.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{STAR}" stroke-opacity=".3"/>')
        moons = []
        for j, p in enumerate(items):
            a = math.radians(40 + i * 75 + j * 360 / len(items))
            col = MERGED if p["merged"] else STAR
            moons.append(f'<circle cx="{cx + r * math.cos(a):.1f}" cy="{cy + r * math.sin(a):.1f}" r="{moon:.1f}" fill="{col}" stroke="{SPACE}" stroke-width="2"/>')
        orbit.append(f'<g class="sp" style="--d:{70 + i * 45}s;--c:{cx}px {cy}px">{"".join(moons)}</g>')
        # Above the moons' path, so a passing moon never covers the name.
        orbit.append(f'<text x="{cx}" y="{cy - r - moon - 11:.0f}" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="15" fill="{SOFT}" stroke="{SPACE}" stroke-width="4" paint-order="stroke">{esc(PROJECT_NAMES.get(repo, repo))}</text>')
    kx, ky = cx + outer + 36, 40
    orbit.append(f'<circle cx="{kx}" cy="{ky - 5}" r="5" fill="{MERGED}"/><text x="{kx + 13}" y="{ky}" font-family="{SERIF}" font-style="italic" font-size="14" fill="{SOFT}">merged</text>'
                 f'<circle cx="{kx}" cy="{ky + 19}" r="5" fill="{STAR}"/><text x="{kx + 13}" y="{ky + 24}" font-family="{SERIF}" font-style="italic" font-size="14" fill="{SOFT}">open</text>')
    sx = 742

    def stat(y, big, small):
        return (f'<text x="{sx}" y="{y}" font-family="{SERIF}" font-size="52" fill="{STAR}">{esc(big)}</text>'
                f'<text x="{sx}" y="{y + 30}" font-family="{SERIF}" font-style="italic" font-size="19" fill="{SOFT}">{esc(small)}</text>')

    # Below the widest orbit's moons.
    sy = cy + outer + 66
    stats = (stat(sy, f"{len(oss)} pull requests", f"across {len(oss_projects)} projects, {oss_merged} merged so far")
             + stat(sy + 98, f"{stars_combined:,} stars", "on those projects (theirs, not mine)")
             + stat(sy + 196, f"{sm['tested']} of {len(sm['code_fixes'])} fixes", "came with tests of their own"))
    label = (f"A paper receipt floating in space summing up {len(oss)} open-source pull requests by project, kind of work, "
             f"area of the code and language: {oss_merged} merged, {oss_open} open. An orrery shows them orbiting {len(oss_projects)} projects.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
            f'{STYLE}{starfield(w, h, 23, 230)}{paper}{"".join(orbit)}{stats}</svg>')


# What a PR does, in plain words, where its Summary leads with code instead.
# Each line restates that PR's own description.
PLAIN = {
    "https://github.com/amd/gaia/pull/6926": "A chat meant to stay on your PC is no longer sent to a cloud model just to give it a title.",
    "https://github.com/amd/gaia/pull/6907": "A cloud model that one part of GAIA has discovered is now recognized as cloud everywhere, from any provider, instead of being treated as if it ran on your PC.",
    "https://github.com/amd/gaia/pull/6859": "Removes styling code the GAIA website no longer used, so the site ships less dead CSS.",
    "https://github.com/lingdojo/kana-dojo/pull/33693": "Brings back five community themes that two later merges had accidentally deleted.",
    "https://github.com/minio/minio-js/pull/1516": "Lets the MinIO JavaScript client sign in with AWS credentials on EC2 and in containers, which failed because it read the wrong field name.",
}


def impact(body):
    """The first sentence of a PR's Summary, in plain text: what it does for people."""
    text = body or ""
    m = re.search(r"^#+\s*Summary\s*$(.*?)(?=^#+\s|\Z)", text, re.M | re.S)
    if m:
        text = m.group(1)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    para = next((b.strip() for b in re.split(r"\n\s*\n", text) if b.strip() and not b.strip().startswith(("#", "|", "-", "*", ">", "!", "<", "```"))), "")
    para = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", para)
    para = re.sub(r"\*\*|__", "", para)
    para = " ".join(para.split())
    sentence = re.split(r"(?<=[.!?])\s+(?=[A-Z])", para, maxsplit=1)[0]
    return sentence if 20 <= len(sentence) <= 240 else ""


def why(p):
    return PLAIN.get(p["url"]) or impact(p.get("body"))


def pr_line(p, with_project=False):
    """One PR as a list item, with what it does for people underneath."""
    repo = p["repository"]["nameWithOwner"]
    title = p["title"].split(": ", 1)[-1]
    project = f"**{esc(PROJECT_NAMES.get(repo, repo))}** · " if with_project else ""
    line = f'- {project}[{esc(title)}]({p["url"]}) · <sub>{"merged" if p["merged"] else "open"}</sub>'
    value = why(p)
    return f"{line}<br>\n  {esc(value)}" if value else line


def cell(text):
    return esc(text).replace("|", "\\|")


def work_sections():
    """The README's summary, area table, latest merges and full list. Same size at 15 PRs or 150."""
    sm = summary()
    kinds = " · ".join(f"{k} {n}" for k, n in sm["kinds"])
    lead = (f"{len(oss)} pull requests to {len(sm['projects'])} projects ({kinds}). "
            f"{sm['tested']} of {len(sm['code_fixes'])} code fixes shipped with tests.")
    table = "\n".join(
        f"| {cell(project)} · **{cell(area)}** | {len(items)} ({sum(p['merged'] for p in items)} merged) "
        f"| {cell(', '.join(lang for lang, _ in language_share(items)[:3]))} "
        f"| [#{items[0]['number']}]({items[0]['url']}) {cell(why(items[0]))} |"
        for (project, area), items in sm["areas"])
    merged = [p for p in oss if p["merged"]][:5]
    grouped = "\n\n".join(f"**{esc(name)}** · {len(items)}\n\n" + "\n".join(pr_line(p) for p in items)
                          for name, items in sm["projects"])
    return f"""{lead}

### Where the work went

| Area | Pull requests | Languages | Latest change |
|---|---|---|---|
{table}

### Recently merged

{chr(10).join(pr_line(p, True) for p in merged)}

<details>
<summary>All {len(oss)} pull requests, each with what it does</summary>
<br>

{grouped}

</details>"""


def readme():
    team_rows = "\n".join(f'| {esc(p["repository"]["nameWithOwner"])} | [{esc(p["title"])}]({p["url"]}) | {"Merged" if p["merged"] else p["state"].title()} |' for p in team)
    merged_oss = next((p for p in reversed(oss) if p["merged"]), None)  # oss is newest first; this line is about the first merge
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

<sub>This page rebuilds itself from the GitHub API every day. [Make your own with orbit-profile](https://github.com/ityashag/orbit-profile).</sub>

{work_sections()}

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
(ROOT / "README.md").write_text(readme(), encoding="utf8")
print(json.dumps(dict(repos=len(repos), original=len(original), external=len(external), ext_merged=ext_merged,
                      oss=len(oss), oss_merged=oss_merged, oss_open=oss_open, added=added, removed=removed,
                      stars=stars_combined, team=len(team))))
