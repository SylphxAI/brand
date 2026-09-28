#!/usr/bin/env python3
"""Render the three directions onto real pages and compose review boards.

  python3 directions/build.py            # all directions
  python3 directions/build.py a-signal   # one

Pages: home, product (Database), docs, console home, console resource page.
Each at desktop 1440 px and mobile 390 px, in the direction's default theme,
plus the console in the other theme. Screenshots come from headless Chromium;
boards are composed with Pillow into directions/out/.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from directions import DIRECTIONS, icon_svg, mark_svg

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
HTML = OUT / "html"
SHOTS = OUT / "shots"
FONTS = HERE / "fonts"

FONT_FILES = {
    "Geist Sans": "geist-sans-latin-{w}-normal",
    "Geist Mono": "geist-mono-latin-{w}-normal",
    "Instrument Sans": "instrument-sans-latin-{w}-normal",
    "Instrument Serif": "instrument-serif-latin-{w}-normal",
    "IBM Plex Sans": "ibm-plex-sans-latin-{w}-normal",
    "IBM Plex Mono": "ibm-plex-mono-latin-{w}-normal",
    "JetBrains Mono": "jetbrains-mono-latin-{w}-normal",
}


def font_faces() -> str:
    css = []
    for family, pattern in FONT_FILES.items():
        for w in (400, 500, 600, 700):
            f = FONTS / (pattern.format(w=w) + ".woff2")
            if f.exists():
                css.append(
                    f"@font-face{{font-family:'{family}';font-weight:{w};src:url('{f.as_uri()}') format('woff2')}}"
                )
    return "".join(css)


# ── CSS ────────────────────────────────────────────────────────────────────


def css(d: dict, t: dict) -> str:
    v = "".join(f"--{k.replace('_', '-')}:{val};" for k, val in t.items())
    dense = {"compact": (13, 32, 36), "airy": (14, 38, 44), "dense": (13, 30, 34)}[d["density"]]
    fs, ctl, row = dense
    grad = (
        f"radial-gradient(1200px 520px at 50% -120px, color-mix(in srgb, {t['accent']} 38%, transparent), transparent 70%),"
        f"radial-gradient(700px 400px at 85% 10%, color-mix(in srgb, {t.get('accent2', t['accent'])} 26%, transparent), transparent 70%)"
        if d["hero"] == "centered"
        else "none"
    )
    grid_bg = (
        f"linear-gradient({t['border']} 1px, transparent 1px) 0 0/48px 48px,"
        f"linear-gradient(90deg, {t['border']} 1px, transparent 1px) 0 0/48px 48px"
        if d["hero"] == "grid"
        else "none"
    )
    return f"""
{font_faces()}
:root{{{v}--r:{d['radius']};--rl:{d['radius_lg']};--fs:{fs}px;--ctl:{ctl}px;--row:{row}px;
--sans:'{d['font_sans']}',system-ui,sans-serif;--display:'{d['font_display']}',system-ui,sans-serif;--mono:'{d['font_mono']}',ui-monospace,monospace}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font:var(--fs)/1.5 var(--sans);-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none}}
.mono{{font-family:var(--mono)}}
.t2{{color:var(--text2)}}.t3{{color:var(--text3)}}
.btn{{display:inline-flex;align-items:center;gap:8px;height:var(--ctl);padding:0 14px;border-radius:var(--r);font-weight:500;font-size:var(--fs);border:1px solid var(--border2);background:var(--surface);color:var(--text);white-space:nowrap}}
.btn.primary{{background:var(--accent);border-color:var(--accent);color:var(--on-accent)}}
.btn.lg{{height:calc(var(--ctl) + 10px);padding:0 20px;font-size:15px}}
.badge{{display:inline-flex;align-items:center;gap:6px;height:20px;padding:0 8px;border-radius:999px;font-size:11px;font-weight:500;background:var(--surface2);color:var(--text2);border:1px solid var(--border)}}
.badge.accent{{background:var(--accent-soft);color:var(--accent-text);border-color:transparent}}
.dot{{width:7px;height:7px;border-radius:50%;display:inline-block;background:var(--ok)}}
.dot.warn{{background:var(--warn)}}.dot.err{{background:var(--err)}}
.card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--rl)}}
.label{{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--text3);font-family:{'var(--mono)' if d['hero'] == 'grid' else 'var(--sans)'};font-weight:500}}
.kbd{{font-family:var(--mono);font-size:11px;border:1px solid var(--border2);border-bottom-width:2px;border-radius:4px;padding:0 5px;color:var(--text2)}}
/* site */
.nav{{display:flex;align-items:center;gap:28px;height:64px;padding:0 40px;border-bottom:1px solid var(--border);background:color-mix(in srgb,var(--bg) 80%,transparent)}}
.logo{{display:flex;align-items:center;gap:10px;font-family:var(--sans);font-weight:600;font-size:17px;letter-spacing:-.02em}}
.nav .links{{display:flex;gap:24px;color:var(--text2);font-size:14px}}
.nav .right{{margin-left:auto;display:flex;gap:10px;align-items:center}}
.hero{{padding:96px 40px 72px;background:{grad};position:relative}}
.hero.gridbg{{background:{grid_bg}}}
.h1{{font-family:var(--display);font-weight:{d['display_weight']};letter-spacing:{d['display_tracking']};font-size:68px;line-height:1.02}}
.h2{{font-family:var(--display);font-weight:{d['display_weight']};letter-spacing:{d['display_tracking']};font-size:40px;line-height:1.08}}
.lede{{font-size:19px;color:var(--text2);max-width:560px;line-height:1.5;margin-top:22px}}
.wrap{{max-width:1200px;margin:0 auto}}
.term{{background:var(--code-bg);color:#EDEAE4;border-radius:var(--rl);border:1px solid var(--border);font:13px/1.7 var(--mono);padding:18px 20px;overflow:hidden}}
.term .c{{color:#8A847D}}.term .k{{color:{t['accent_text'] if t['code_bg'] == t['bg'] else '#F5B454' if d['name'] == 'Signal' else '#9DB0FF'}}}.term .s{{color:#9BE3B0}}
.section{{padding:72px 40px;border-top:1px solid var(--border)}}
.engines{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:34px}}
.prod{{padding:18px;display:flex;flex-direction:column;gap:8px;min-height:128px}}
.prod .ptop{{display:flex;align-items:center;gap:10px;font-weight:600;font-size:15px}}
.ico{{width:34px;height:34px;display:grid;place-items:center;border-radius:var(--r);background:var(--accent-soft);color:var(--accent-text)}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);margin-top:40px;border:1px solid var(--border);border-radius:var(--rl);overflow:hidden}}
.stats>div{{padding:22px;border-right:1px solid var(--border)}}.stats>div:last-child{{border:0}}
.num{{font-family:var(--display);font-size:34px;font-weight:{d['display_weight']};letter-spacing:{d['display_tracking']}}}
/* docs */
.docs{{display:grid;grid-template-columns:260px 1fr 220px;min-height:calc(100vh - 64px)}}
.side{{border-right:1px solid var(--border);padding:24px 18px;font-size:13.5px;color:var(--text2)}}
.side h6{{margin:18px 0 6px;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--text3);font-weight:600}}
.side a{{display:block;padding:5px 10px;border-radius:var(--r)}}.side a.on{{background:var(--accent-soft);color:var(--accent-text);font-weight:500}}
.article{{padding:40px 56px;max-width:820px}}
.article h1{{font-family:var(--display);font-weight:{d['display_weight']};letter-spacing:{d['display_tracking']};font-size:40px;margin:10px 0 14px}}
.article h2{{font-size:21px;margin:34px 0 10px;font-weight:600}}
.article p{{color:var(--text2);font-size:15.5px;line-height:1.7;margin:10px 0}}
.tabs{{display:flex;gap:2px;border-bottom:1px solid #2F2C29;padding:0 10px;background:#161412}}
.tabs span{{padding:9px 12px;font:12px var(--mono);color:#8A847D}}.tabs span.on{{color:#F2EEE6;box-shadow:inset 0 -2px 0 {t['accent']}}}
.callout{{border:1px solid var(--border);border-left:3px solid var(--accent);background:var(--accent-soft);padding:12px 16px;border-radius:var(--r);font-size:14px;color:var(--text2);margin:18px 0}}
.toc{{padding:40px 20px;font-size:13px;color:var(--text3);border-left:1px solid var(--border)}}
.toc a{{display:block;padding:4px 0}}
/* console */
.app{{display:grid;grid-template-columns:{'232px' if d['console'] != 'rail' else '64px 212px'} 1fr;min-height:100vh}}
.sb{{border-right:1px solid var(--border);padding:12px 10px;display:flex;flex-direction:column;gap:2px;background:{'var(--surface)' if d['console'] == 'sidebar' else 'var(--bg)'}}}
.floating .sb{{margin:10px;border:1px solid var(--border);border-radius:var(--rl);background:var(--surface)}}
.rail{{border-right:1px solid var(--border);display:flex;flex-direction:column;align-items:center;gap:10px;padding:14px 0;background:var(--surface)}}
.rail .ri{{width:36px;height:36px;display:grid;place-items:center;border-radius:var(--r);color:var(--text2)}}.rail .ri.on{{background:var(--accent-soft);color:var(--accent-text)}}
.sb .grp{{margin:14px 8px 4px;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--text3);font-weight:500}}
.sb a{{display:flex;align-items:center;gap:10px;height:30px;padding:0 10px;border-radius:var(--r);color:var(--text2);font-size:13px}}
.sb a.on{{background:var(--surface2);color:var(--text);font-weight:500;{'box-shadow:inset 2px 0 0 var(--accent);' if d['console'] == 'rail' else ''}}}
.appbar{{height:52px;display:flex;align-items:center;gap:10px;padding:0 20px;border-bottom:1px solid var(--border);font-size:13px}}
.crumb{{display:flex;align-items:center;gap:8px;color:var(--text2)}}.crumb b{{color:var(--text);font-weight:500}}
.env{{display:inline-flex;align-items:center;gap:6px;height:24px;padding:0 9px;border-radius:999px;background:var(--accent-soft);color:var(--accent-text);font-size:12px;font-weight:500}}
.search{{margin-left:auto;display:flex;align-items:center;gap:10px;height:32px;width:280px;padding:0 10px;border:1px solid var(--border);border-radius:var(--r);color:var(--text3);background:var(--surface)}}
.main{{padding:28px 32px}}
.ph{{display:flex;align-items:flex-end;gap:16px;margin-bottom:22px}}
.ph h1{{font-size:24px;font-weight:600;letter-spacing:-.02em}}
.grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.env-card{{padding:16px}}
.kv{{display:flex;justify-content:space-between;font-size:12.5px;color:var(--text2);padding:4px 0}}
.table{{width:100%;border-collapse:collapse;font-size:13px}}
.table th{{text-align:left;font-weight:500;color:var(--text3);font-size:12px;padding:0 14px;height:34px;border-bottom:1px solid var(--border)}}
.table td{{padding:0 14px;height:var(--row);border-bottom:1px solid var(--border)}}
.spark{{display:flex;align-items:flex-end;gap:3px;height:56px}}.spark i{{flex:1;background:var(--accent);opacity:.75;border-radius:2px 2px 0 0}}
.check li{{list-style:none;display:flex;align-items:center;gap:10px;padding:9px 0;border-bottom:1px solid var(--border);font-size:13.5px}}
.box{{width:18px;height:18px;border-radius:{'50%' if d['console'] == 'floating' else '4px'};border:1.5px solid var(--border2);display:grid;place-items:center;font-size:11px}}
.box.done{{background:var(--accent);border-color:var(--accent);color:var(--on-accent)}}
.feed div{{display:flex;gap:10px;padding:9px 0;border-bottom:1px solid var(--border);font-size:13px;color:var(--text2)}}
.tabsline{{display:flex;gap:22px;border-bottom:1px solid var(--border);margin-bottom:20px;font-size:13.5px;color:var(--text2)}}
.tabsline span{{padding:10px 0}}.tabsline span.on{{color:var(--text);box-shadow:inset 0 -2px 0 var(--accent);font-weight:500}}
.bar{{height:180px;display:flex;align-items:flex-end;gap:4px;padding:10px 0}}.bar i{{flex:1;background:linear-gradient(var(--accent),color-mix(in srgb,var(--accent) 40%,transparent));border-radius:2px 2px 0 0}}
.mobile-only{{display:none}}
@media (max-width:600px){{
 .nav{{padding:0 16px;gap:12px}}.nav .links,.nav .right .btn:not(.primary){{display:none}}
 .hero{{padding:48px 16px 40px}}.h1{{font-size:40px}}.h2{{font-size:28px}}.lede{{font-size:16px}}
 .split{{grid-template-columns:1fr!important}}.section{{padding:44px 16px}}
 .engines{{grid-template-columns:1fr 1fr;gap:10px}}.stats{{grid-template-columns:1fr 1fr}}.stats>div:nth-child(2){{border-right:0}}
 .docs{{grid-template-columns:1fr}}.side,.toc{{display:none}}.article{{padding:24px 16px}}.article h1{{font-size:30px}}
 .app{{grid-template-columns:1fr}}.sb,.rail{{display:none}}.search{{display:none}}.main{{padding:18px 16px 90px}}
 .grid3{{grid-template-columns:1fr}}.appbar{{padding:0 14px}}.hide-m{{display:none}}.mobile-only{{display:flex}}
 .tabbar{{position:fixed;bottom:0;left:0;right:0;height:64px;border-top:1px solid var(--border);background:var(--surface);display:flex;justify-content:space-around;align-items:center;font-size:10.5px;color:var(--text3)}}
 .tabbar div{{display:flex;flex-direction:column;align-items:center;gap:4px}}.tabbar .on{{color:var(--accent-text)}}
}}
"""


# ── Page fragments ─────────────────────────────────────────────────────────


def logo(d: dict, t: dict) -> str:
    return f'<a class="logo" href="#">{mark_svg(d, t, 26)}<span>Sylphx</span></a>'


def site_nav(d: dict, t: dict) -> str:
    return (
        f'<header class="nav">{logo(d, t)}<nav class="links"><a>Products</a><a>Docs</a><a>Pricing</a><a>Changelog</a><a>Customers</a></nav>'
        '<div class="right"><a class="btn">Sign in</a><a class="btn primary">Start building</a></div></header>'
    )


def i(d: dict, t: dict, name: str, size: int = 18) -> str:
    return icon_svg(d, name, size, "currentColor", t["accent"])


PRODUCTS = [
    ("deploy", "Hosting", "Deploy from Git, a preview per pull request."),
    ("database", "Database", "Serverless Postgres with branching."),
    ("users", "Auth", "Sign-in, passkeys and organizations."),
    ("workflow", "Workflows", "Durable steps that survive restarts."),
    ("bolt", "Functions", "Containers that scale to zero."),
    ("logs", "Monitoring", "Logs, traces and errors in one place."),
    ("key", "AI", "One API for every frontier model."),
    ("search", "Search", "Full-text and vector indexes."),
]


def home(d: dict, t: dict) -> str:
    code = (
        '<span class="c"># one call: a project with hosting, a database and auth</span>\n'
        '<span class="k">$</span> npx sylphx init --agent\n'
        '<span class="s">✓</span> project <b>acme/shop</b> created\n'
        '<span class="s">✓</span> database <b>main</b> ready  <span class="c">18 ms</span>\n'
        '<span class="s">✓</span> deployed https://shop.sylphx.app\n\n'
        '<span class="k">import</span> {{ Sylphx }} <span class="k">from</span> <span class="s">"@sylphx/sdk"</span>\n'
        'const sx = new Sylphx()\n'
        'await sx.data.databases.<span class="k">query</span>(<span class="s">"select 1"</span>)'
    ).replace("{{", "{").replace("}}", "}")
    centered = d["hero"] == "centered"
    hero_text = (
        '<span class="badge accent">New · Agents and MCP hosting</span>'
        '<h1 class="h1" style="margin-top:20px">The backend<br>your agents can run.</h1>'
        '<p class="lede">Hosting, data, auth and workflows on one API, one key and one bill. Provisioned by a person or an agent in one call.</p>'
        '<div style="display:flex;gap:10px;margin-top:30px;flex-wrap:wrap' + (";justify-content:center" if centered else "") + '"><a class="btn primary lg">Start building</a><a class="btn lg">Read the docs</a></div>'
    )
    if centered:
        hero = f'<section class="hero"><div class="wrap" style="text-align:center;display:flex;flex-direction:column;align-items:center">{hero_text.replace("class=\"lede\"", "class=\"lede\" style=\"margin-left:auto;margin-right:auto\"")}<div class="term" style="margin-top:48px;width:min(760px,100%);text-align:left"><pre>{code}</pre></div></div></section>'
    else:
        cls = "hero gridbg" if d["hero"] == "grid" else "hero"
        hero = f'<section class="{cls}"><div class="wrap split" style="display:grid;grid-template-columns:1.1fr 1fr;gap:48px;align-items:center"><div>{hero_text}</div><div class="term"><pre>{code}</pre></div></div></section>'
    cards = "".join(
        f'<div class="card prod"><div class="ptop"><span class="ico">{i(d, t, ic)}</span>{n}</div><div class="t2" style="font-size:13.5px">{s}</div>'
        f'<div style="margin-top:auto"><span class="badge">{"Preview" if k % 3 else "Available"}</span></div></div>'
        for k, (ic, n, s) in enumerate(PRODUCTS)
    )
    stats = "".join(
        f'<div><div class="num">{a}</div><div class="t2" style="font-size:13px">{b}</div></div>'
        for a, b in (("1 call", "to a working backend"), ("47", "products on six engines"), ("< 1 s", "to first byte, worldwide"), ("$0", "to start, one bill after"))
    )
    return (
        site_nav(d, t)
        + hero
        + f'<section class="section"><div class="wrap"><div class="label">Products</div><h2 class="h2" style="margin-top:10px">Everything a product needs, on one platform.</h2>'
        f'<div class="engines">{cards}</div><div class="stats">{stats}</div></div></section>'
    )


def product(d: dict, t: dict) -> str:
    rows = "".join(
        f'<tr><td class="mono">{a}</td><td class="t2">{b}</td><td class="mono" style="text-align:right">{c}</td></tr>'
        for a, b, c in (("Storage", "per GB-month", "$0.35"), ("Compute", "per active CPU-hour", "$0.16"), ("Branches", "per branch-hour", "$0.002"), ("Egress", "per GB", "$0.05"))
    )
    feats = "".join(
        f'<div class="card" style="padding:20px"><span class="ico">{i(d, t, ic)}</span><div style="font-weight:600;margin-top:14px">{a}</div><div class="t2" style="font-size:13.5px;margin-top:6px">{b}</div></div>'
        for ic, a, b in (
            ("workflow", "Branch per pull request", "Every preview gets its own copy of the data, created in under a second."),
            ("bolt", "Scales to zero", "Idle databases cost nothing and wake on the first query."),
            ("key", "Row-level security", "Your users' tokens work directly, checked in the database."),
        )
    )
    return (
        site_nav(d, t)
        + f'<section class="hero {"gridbg" if d["hero"] == "grid" else ""}"><div class="wrap split" style="display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center">'
        f'<div><div style="display:flex;gap:8px;align-items:center"><span class="ico">{i(d, t, "database")}</span><span class="label">Store · Database</span><span class="badge">Preview</span></div>'
        '<h1 class="h1" style="margin-top:18px;font-size:56px">Postgres that<br>branches with your code.</h1>'
        '<p class="lede">Serverless Postgres with pgvector, instant branches, backups and point-in-time restore.</p>'
        '<div style="display:flex;gap:10px;margin-top:26px"><a class="btn primary lg">Create a database</a><a class="btn lg">Quickstart</a></div></div>'
        '<div class="term"><pre><span class="c"># create, branch, connect</span>\n<span class="k">$</span> sylphx data databases create main\n<span class="k">$</span> sylphx data databases branch main pr-42\n<span class="k">$</span> psql $(sylphx data databases connect main)\n\n<span class="s">main</span>=&gt; select count(*) from orders;\n  count\n -------\n  48210</pre></div></div></section>'
        f'<section class="section"><div class="wrap"><div class="grid3" style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px">{feats}</div>'
        f'<div style="margin-top:48px"><div class="label">Pricing</div><h2 class="h2" style="margin:10px 0 18px;font-size:30px">Free to start. Pay for what runs.</h2>'
        f'<div class="card" style="overflow:hidden"><table class="table"><thead><tr><th>Meter</th><th>Unit</th><th style="text-align:right">Price</th></tr></thead><tbody>{rows}</tbody></table></div></div></div></section>'
    )


def docs(d: dict, t: dict) -> str:
    side = (
        "<h6>Get started</h6><a>Overview</a><a>Quickstart</a><a>Agents and MCP</a>"
        '<h6>Database</h6><a>Overview</a><a class="on">Branching</a><a>Connect</a><a>Backups and restore</a><a>Row-level security</a>'
        "<h6>Reference</h6><a>API · databases</a><a>CLI · data</a><a>Errors</a>"
    )
    return (
        site_nav(d, t)
        + f'<div class="docs"><aside class="side">{side}</aside><article class="article">'
        '<div class="t3" style="font-size:13px">Docs / Database / Branching</div>'
        '<div style="display:flex;gap:8px;margin-top:14px"><span class="badge">How-to</span><span class="badge accent">Preview</span></div>'
        "<h1>Branch a database for every pull request</h1>"
        "<p>A branch is a copy of your database that shares storage with its parent, so it is created in under a second and costs only what changes. Hosting creates one for every preview automatically.</p>"
        '<div class="callout">Branches inherit the parent\'s row-level security policies. Test policy changes on a branch before they reach production.</div>'
        "<h2>Create a branch</h2><p>Name the parent and the branch. The branch appears in the same environment as the parent.</p>"
        '<div style="border-radius:var(--rl);overflow:hidden;border:1px solid var(--border)"><div class="tabs"><span class="on">CLI</span><span>TypeScript</span><span>cURL</span><span>MCP</span></div>'
        '<div class="term" style="border:0;border-radius:0"><pre><span class="k">$</span> sylphx data databases branch main pr-42 --env preview\n<span class="s">✓</span> branch pr-42 ready in 640 ms</pre></div></div>'
        "<h2>Delete a branch</h2><p>A branch is deleted with its preview. Deleted branches can be restored for 30 days.</p>"
        '</article><nav class="toc"><div class="label" style="margin-bottom:10px">On this page</div><a style="color:var(--text)">Create a branch</a><a>Connect</a><a>Delete a branch</a><a>Limits</a>'
        '<div style="margin-top:24px" class="label">Copy page</div><a>As Markdown</a><a>Open in assistant</a></nav></div>'
    )


def console_shell(d: dict, t: dict, active: str, body: str) -> str:
    groups = [
        (None, [("overview", "Overview"), ("logs", "Activity"), ("search", "Logs")]),
        ("Run", [("deploy", "Services"), ("bolt", "Functions")]),
        ("Store", [("database", "Databases"), ("search", "Search indexes")]),
        ("Identity", [("users", "Users")]),
        ("Platform", [("key", "API keys"), ("settings", "Settings")]),
    ]
    links = ""
    for g, items in groups:
        if g:
            links += f'<div class="grp">{g}</div>'
        for ic, n in items:
            links += f'<a class="{"on" if n == active else ""}">{i(d, t, ic, 16)}{n}</a>'
    sb = f'<aside class="sb">{links}</aside>'
    if d["console"] == "rail":
        rail = f'<nav class="rail"><div style="margin-bottom:8px">{mark_svg(d, t, 26)}</div>' + "".join(
            f'<div class="ri {"on" if k == 1 else ""}">{i(d, t, ic, 18)}</div>' for k, ic in enumerate(("overview", "deploy", "database", "users", "settings"))
        ) + "</nav>"
        nav = rail + sb
    else:
        nav = sb
    top = (
        f'<header class="appbar">{"" if d["console"] == "rail" else mark_svg(d, t, 22)}'
        '<div class="crumb"><b>acme</b><span class="t3">/</span><b>shop</b><span class="t3">/</span><span class="env"><span class="dot"></span>production</span></div>'
        f'<div class="search">{i(d, t, "search", 15)}<span>Search or jump to…</span><span style="margin-left:auto" class="kbd">⌘K</span></div>'
        '<div style="width:28px;height:28px;border-radius:50%;background:var(--surface2);border:1px solid var(--border)" class="hide-m"></div></header>'
    )
    tabbar = (
        '<nav class="tabbar mobile-only">'
        + "".join(
            f'<div class="{"on" if k == 0 else ""}">{i(d, t, ic, 20)}{n}</div>'
            for k, (ic, n) in enumerate((("overview", "Overview"), ("database", "Resources"), ("search", "Search"), ("logs", "Activity"), ("settings", "More")))
        )
        + "</nav>"
    )
    return f'<div class="app {"floating" if d["console"] == "floating" else ""}">{nav}<div>{top}<main class="main">{body}</main></div></div>{tabbar}'


def console_home(d: dict, t: dict) -> str:
    envs = "".join(
        f'<div class="card env-card"><div style="display:flex;align-items:center;gap:8px;font-weight:600"><span class="dot {s}"></span>{n}</div>'
        f'<div class="spark" style="margin:14px 0 10px">{"".join(f"<i style=height:{h}%></i>" for h in hs)}</div>'
        f'<div class="kv"><span>Last deploy</span><span class="mono">{dep}</span></div><div class="kv"><span>Error rate</span><span class="mono">{er}</span></div></div>'
        for n, s, hs, dep, er in (
            ("production", "", (40, 52, 48, 60, 72, 66, 80, 76, 90, 84, 70, 78), "4 min ago", "0.02%"),
            ("preview", "", (20, 26, 18, 30, 24, 36, 28, 40, 34, 22, 30, 26), "12 min ago", "0.00%"),
            ("development", "warn", (8, 12, 10, 6, 14, 9, 16, 12, 7, 11, 13, 10), "2 h ago", "1.40%"),
        )
    )
    checklist = "".join(
        f'<li><span class="box {"done" if k < 2 else ""}">{"✓" if k < 2 else ""}</span><span style="{"color:var(--text3);text-decoration:line-through" if k < 2 else ""}">{x}</span></li>'
        for k, x in enumerate(("Make your first API call", "Deploy from GitHub", "Add a custom domain", "Invite a teammate", "Set a spend cap"))
    )
    feed = "".join(
        f'<div><span class="dot {c}" style="margin-top:6px"></span><div><span style="color:var(--text)">{a}</span> {b}<div class="t3" style="font-size:12px">{w}</div></div></div>'
        for a, b, w, c in (
            ("web", "deployed to production · #184", "4 min ago · kai@acme.dev", ""),
            ("main", "branched as pr-42", "12 min ago · agent claude-ci", ""),
            ("API key", "prod-server rolled", "1 h ago · kai@acme.dev", "warn"),
            ("checkout", "workflow failed 3 runs", "2 h ago", "err"),
        )
    )
    body = (
        '<div class="ph"><div><div class="label">Project</div><h1>shop</h1></div><div style="margin-left:auto;display:flex;gap:8px" class="hide-m"><a class="btn">Settings</a><a class="btn primary">Deploy</a></div></div>'
        f'<div class="grid3">{envs}</div>'
        '<div style="display:grid;grid-template-columns:1.2fr 1fr;gap:14px;margin-top:14px" class="split">'
        f'<div class="card" style="padding:18px"><div style="display:flex;align-items:center"><b>Recent activity</b><a class="t3" style="margin-left:auto;font-size:12.5px">View all</a></div><div class="feed" style="margin-top:8px">{feed}</div></div>'
        f'<div class="card" style="padding:18px"><b>Finish setting up</b><span class="t3" style="font-size:12.5px"> · 2 of 5</span><ul class="check" style="margin-top:8px">{checklist}</ul></div></div>'
    )
    return console_shell(d, t, "Overview", body)


def console_resource(d: dict, t: dict) -> str:
    bars = "".join(f"<i style=height:{h}%></i>" for h in (22, 30, 28, 44, 38, 52, 60, 48, 66, 72, 58, 80, 74, 62, 70, 88, 76, 64, 58, 70, 82, 90, 78, 68))
    rows = "".join(
        f'<tr><td class="mono">{a}</td><td><span class="dot {s}"></span> <span class="t2">{st}</span></td><td class="mono t2">{b}</td><td class="mono t2 hide-m">{c}</td></tr>'
        for a, s, st, b, c in (
            ("main", "", "Ready", "2.4 GB", "3 min ago"),
            ("pr-42", "", "Ready", "18 MB", "12 min ago"),
            ("pr-39", "warn", "Sleeping", "11 MB", "2 d ago"),
        )
    )
    body = (
        '<div class="t3" style="font-size:12.5px;margin-bottom:10px"><span class="mono">orgs/acme/projects/shop/envs/production/databases/main</span></div>'
        f'<div class="ph"><span class="ico" style="width:40px;height:40px">{i(d, t, "database", 20)}</span><div><h1>main</h1><div class="t2" style="font-size:13px"><span class="dot"></span> Ready · Postgres 17 · hk-1</div></div>'
        '<div style="margin-left:auto;display:flex;gap:8px" class="hide-m"><a class="btn">Copy as <span class="kbd">CLI</span></a><a class="btn">Connect</a><a class="btn primary">Branch</a></div></div>'
        '<div class="tabsline"><span class="on">Overview</span><span>Branches</span><span>Metrics</span><span>Logs</span><span class="hide-m">Activity</span><span class="hide-m">Settings</span></div>'
        '<div style="display:grid;grid-template-columns:2fr 1fr;gap:14px" class="split">'
        f'<div class="card" style="padding:18px"><div style="display:flex;align-items:baseline;gap:10px"><b>Queries per second</b><span class="t3" style="font-size:12px">last 24 h</span><span class="mono" style="margin-left:auto;font-size:22px">1,284</span></div><div class="bar">{bars}</div></div>'
        '<div class="card" style="padding:18px"><b>Details</b><div style="margin-top:10px">'
        + "".join(f'<div class="kv"><span>{a}</span><span class="mono" style="color:var(--text)">{b}</span></div>' for a, b in (("Size", "2.4 GB"), ("Connections", "38 / 400"), ("Backups", "every 5 min"), ("Restore window", "7 days"), ("Region", "hk-1")))
        + "</div></div></div>"
        f'<div class="card" style="margin-top:14px;overflow:hidden"><div style="padding:14px 14px 6px;display:flex"><b>Branches</b><a class="t3" style="margin-left:auto;font-size:12.5px">New branch</a></div><table class="table"><thead><tr><th>Name</th><th>Status</th><th>Size</th><th class="hide-m">Updated</th></tr></thead><tbody>{rows}</tbody></table></div>'
    )
    return console_shell(d, t, "Databases", body)


PAGES = {"home": (home, 1420), "product": (product, 1450), "docs": (docs, 1100), "console": (console_home, 900), "resource": (console_resource, 960)}
MOBILE_H = {"home": 1900, "product": 1700, "docs": 1300, "console": 1500, "resource": 1500}


def page_html(d: dict, t: dict, fn) -> str:
    return f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><style>{css(d, t)}</style></head><body>{fn(d, t)}</body></html>'


def shoot(html: Path, png: Path, w: int, h: int, scale: int = 1) -> None:
    subprocess.run(
        ["/usr/bin/chromium", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
         f"--force-device-scale-factor={scale}", f"--window-size={w},{h}", f"--screenshot={png}", html.as_uri()],
        check=True, capture_output=True, timeout=120,
    )


# ── Boards ─────────────────────────────────────────────────────────────────


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    f = FONTS / ("instrument-sans-latin-600-normal.woff2" if bold else "instrument-sans-latin-400-normal.woff2")
    try:
        return ImageFont.truetype(str(f), size)
    except OSError:
        return ImageFont.load_default()


def identity_html(d: dict) -> str:
    dk, lt = d["dark"], d["light"]
    import io

    def swatches(t: dict) -> str:
        keys = ("bg", "surface", "surface2", "border", "text2", "text", "accent", "accent_text", "ok", "warn", "err", "info")
        return "".join(
            f'<div style="text-align:center;font:10px var(--mono);color:var(--text3)"><div style="width:58px;height:44px;border-radius:6px;background:{t[k]};border:1px solid var(--border)"></div>{k.replace("_", "-")}<br>{t[k]}</div>'
            for k in keys
        )

    icons = "".join(f'<div style="color:var(--text)">{icon_svg(d, n, 26, "currentColor", lt["accent"])}</div>' for n in ("overview", "deploy", "database", "key", "logs", "workflow", "users", "settings", "search", "bolt"))
    lockup = lambda t, fg: f'<div style="display:flex;align-items:center;gap:14px;font:600 44px/1 var(--sans);letter-spacing:-.03em;color:{fg}">{mark_svg(d, t, 56)}Sylphx</div>'
    app = f'<div style="width:132px;height:132px;border-radius:30px;background:{lt["field"]};display:grid;place-items:center">{mark_svg(d, dk, 100, True)}</div>'
    motion = "".join(f"<li style='margin:4px 0'>{m}</li>" for m in d["motion"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css(d, lt)}</style></head><body style="padding:48px;width:1600px">
<div style="display:flex;align-items:baseline;gap:16px"><div class="h2" style="font-size:52px">{d['name']}</div><div class="t2" style="font-size:18px">{d['tagline']}</div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:30px">
 <div class="card" style="padding:32px;display:flex;gap:40px;align-items:center">{mark_svg(d, lt, 160)}<div style="display:flex;flex-direction:column;gap:20px">{lockup(lt, lt['text'])}{app}</div></div>
 <div style="background:{dk['bg']};border-radius:var(--rl);padding:32px;display:flex;gap:40px;align-items:center;border:1px solid {dk['border']}">{mark_svg(d, dk, 160)}<div style="display:flex;flex-direction:column;gap:20px">{lockup(dk, dk['text'])}<div class="mono" style="color:{dk['text2']};font-size:13px">favicon 16 · 32 · app icon on the right board</div></div></div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px">
 <div class="card" style="padding:22px"><div class="label">Light</div><div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px">{swatches(lt)}</div></div>
 <div style="background:{dk['bg']};border-radius:var(--rl);padding:22px;border:1px solid {dk['border']};--text3:{dk['text3']};--border:{dk['border']}"><div class="label">Dark</div><div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px">{swatches(dk)}</div></div>
</div>
<div style="display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:20px;margin-top:20px">
 <div class="card" style="padding:22px"><div class="label">Type</div><div style="font:{d['display_weight']} 56px/1 var(--display);letter-spacing:{d['display_tracking']};margin-top:12px">Ship the backend.</div>
 <div style="font:16px/1.5 var(--sans);margin-top:12px" class="t2">{d['font_sans']} for text and interface · {d['font_display']} for display · {d['font_mono']} for code and numbers.</div>
 <div class="mono" style="margin-top:10px;font-size:14px">orgs/acme/projects/shop · 1,284 qps · $0.35</div></div>
 <div class="card" style="padding:22px"><div class="label">Icons</div><div style="display:flex;gap:18px;flex-wrap:wrap;margin-top:16px">{icons}</div>
 <div class="t3" style="font-size:12px;margin-top:14px">{d['icon']['width']} px stroke · {d['icon']['cap']} caps{' · duotone' if d['icon']['duotone'] else ''}</div></div>
 <div class="card" style="padding:22px"><div class="label">Motion</div><ul style="margin-top:10px;padding-left:18px;font-size:14px" class="t2">{motion}</ul></div>
</div>
<div class="card" style="padding:18px 22px;margin-top:20px;font-size:14px"><b>Takes</b> <span class="t2">{d['takes']}</span>&nbsp;&nbsp; <b>Rejects</b> <span class="t2">{d['rejects']}</span></div>
</body></html>"""


def favicon_strip(d: dict, key: str) -> Image.Image:
    """Pixel-snapped 16 and 32 px icons, at 1x and enlarged."""
    import io
    import resvg_py

    dk = d["dark"]
    tile = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" rx="96" fill="{d["light"]["field"]}"/><g transform="translate(40 40) scale(0.84375)">' + d["mark"]().replace("{c}", dk[d["mark_colours"][0]]).replace("{c2}", "#F2EEE6" if d["mark_colours"][1] == "text" else dk.get(d["mark_colours"][1], dk["accent"])) + "</g></svg>"
    strip = Image.new("RGBA", (560, 300), d["light"]["bg"])
    x = 20
    for px in (16, 32):
        big = Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=tile, width=px * 8)))).convert("RGBA")
        small = big.resize((px, px), Image.BOX)
        strip.alpha_composite(small, (x, 20))
        strip.alpha_composite(small.resize((px * 8, px * 8), Image.NEAREST), (x, 50))
        x += px * 8 + 30
    app = Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=tile, width=200)))).convert("RGBA")
    strip.alpha_composite(app.resize((150, 150), Image.LANCZOS), (x, 50))
    return strip


def compose(key: str, d: dict) -> None:
    sh = SHOTS / key
    W = 3200
    pad = 60
    title_h = 120
    ident = Image.open(sh / "identity.png").convert("RGB")
    fav = favicon_strip(d, key).convert("RGB")
    # Board 1: identity + favicons
    b1 = Image.new("RGB", (ident.width + 40 + fav.width, max(ident.height, fav.height)), d["light"]["bg"])
    b1.paste(ident, (0, 0))
    b1.paste(fav, (ident.width + 20, 60))
    b1.save(OUT / f"{key}-1-identity.png", optimize=True)

    # Board 2: desktop pages (default theme) + console in the other theme
    default = "dark" if key != "c-engineered" else "light"
    other = "light" if default == "dark" else "dark"
    tiles = [(f"{p} · desktop · {default}", sh / f"{p}-desktop-{default}.png") for p in PAGES] + [
        (f"console · desktop · {other}", sh / f"console-desktop-{other}.png")
    ]
    colw = (W - pad * 3) // 2
    ims = []
    for label, f in tiles:
        im = Image.open(f).convert("RGB")
        im = im.resize((colw, int(im.height * colw / im.width)), Image.LANCZOS)
        ims.append((label, im))
    heights = [0, 0]
    placed = []
    for label, im in ims:
        col = 0 if heights[0] <= heights[1] else 1
        placed.append((label, im, pad + col * (colw + pad), title_h + heights[col]))
        heights[col] += im.height + 70
    board = Image.new("RGB", (W, title_h + max(heights) + pad), "#E9E7E3")
    dr = ImageDraw.Draw(board)
    dr.text((pad, 34), f"{d['name']} — pages, desktop 1440 px", fill="#1C1917", font=font(48, True))
    for label, im, x, y in placed:
        dr.text((x, y - 44), label, fill="#57534E", font=font(28))
        board.paste(im, (x, y))
    board.save(OUT / f"{key}-2-desktop.png", optimize=True)

    # Board 3: mobile pages
    mobs = [Image.open(sh / f"{p}-mobile-{default}.png").convert("RGB") for p in PAGES] + [Image.open(sh / f"console-mobile-{other}.png").convert("RGB")]
    mw = 460
    mobs = [m.resize((mw, int(m.height * mw / m.width)), Image.LANCZOS) for m in mobs]
    mh = max(m.height for m in mobs)
    board = Image.new("RGB", (pad + len(mobs) * (mw + pad), title_h + mh + pad + 50), "#E9E7E3")
    dr = ImageDraw.Draw(board)
    dr.text((pad, 34), f"{d['name']} — pages, mobile 390 px", fill="#1C1917", font=font(48, True))
    names = list(PAGES) + [f"console {other}"]
    for k, m in enumerate(mobs):
        x = pad + k * (mw + pad)
        dr.text((x, title_h), names[k], fill="#57534E", font=font(26))
        board.paste(m, (x, title_h + 44))
    board.save(OUT / f"{key}-3-mobile.png", optimize=True)


def build(key: str) -> None:
    d = DIRECTIONS[key]
    (HTML / key).mkdir(parents=True, exist_ok=True)
    (SHOTS / key).mkdir(parents=True, exist_ok=True)
    for theme in ("dark", "light"):
        t = d[theme]
        for name, (fn, h) in PAGES.items():
            f = HTML / key / f"{name}-{theme}.html"
            f.write_text(page_html(d, t, fn))
            shoot(f, SHOTS / key / f"{name}-desktop-{theme}.png", 1440, h)
            shoot(f, SHOTS / key / f"{name}-mobile-{theme}.png", 390, MOBILE_H[name], 2)
    f = HTML / key / "identity.html"
    f.write_text(identity_html(d))
    shoot(f, SHOTS / key / "identity.png", 1696, 1400)
    compose(key, d)


if __name__ == "__main__":
    for k in sys.argv[1:] or list(DIRECTIONS):
        build(k)
        print("built", k)
