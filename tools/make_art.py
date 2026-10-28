"""Generates the animated SVG artwork for the GitHub profile README.

Every SVG is a self-contained dark panel (no external fonts or images), so it renders
the same on GitHub's light and dark themes. Animation uses CSS keyframes and SMIL,
both of which GitHub renders for SVGs shown as images.

Run:  python3 tools/make_art.py   (writes into assets/)
"""
import math
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)

BG0, BG1 = "#0d1016", "#090b0f"
LINE = "#232a36"
INK = "#ecebe6"
MUTED = "#8b93a1"
FAINT = "#5b6371"
IND = "#969fff"
AMB = "#ffa852"
MINT = "#78dec4"
RED = "#ff7d90"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    a, b = hexrgb(a), hexrgb(b)
    return "#%02x%02x%02x" % tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def panel(w, h, body, extra_style="", glow=None):
    g = glow or (w * 0.72, h * 0.45)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<defs>
  <radialGradient id="bg" cx="{g[0] / w:.3f}" cy="{g[1] / h:.3f}" r="0.75">
    <stop offset="0" stop-color="#151a26"/><stop offset="0.55" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/>
  </radialGradient>
  <radialGradient id="glowMint"><stop offset="0" stop-color="{MINT}" stop-opacity=".55"/><stop offset="1" stop-color="{MINT}" stop-opacity="0"/></radialGradient>
  <radialGradient id="glowAmb"><stop offset="0" stop-color="{AMB}" stop-opacity=".55"/><stop offset="1" stop-color="{AMB}" stop-opacity="0"/></radialGradient>
</defs>
<style>
  .sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
  @keyframes tw{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
  @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
  @keyframes breathe{{0%,100%{{transform:scale(1);opacity:.9}}50%{{transform:scale(1.35);opacity:.35}}}}
  .t1{{animation:tw 3.1s ease-in-out infinite}} .t2{{animation:tw 4.3s ease-in-out infinite .7s}}
  .t3{{animation:tw 5.2s ease-in-out infinite 1.6s}} .t4{{animation:tw 3.7s ease-in-out infinite 2.4s}}
  .pulse{{animation:pulse 1.8s ease-in-out infinite}}
  @keyframes spin{{to{{transform:rotate(360deg)}}}}
  @keyframes grow{{0%,8%{{transform:scaleY(0)}}22%,88%{{transform:scaleY(1)}}100%{{transform:scaleY(0)}}}}
  .grow{{transform-box:fill-box;transform-origin:50% 100%;transform:scaleY(0);animation:grow 6s ease-out infinite}}
  .breathe{{transform-box:fill-box;transform-origin:center;animation:breathe 2.6s ease-in-out infinite}}
  {extra_style}
</style>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="url(#bg)" stroke="{LINE}"/>
{body}
</svg>
"""


def save(name, svg):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg)
    print(f"{name}: {len(svg) / 1024:.1f} KB")


# ---------------------------------------------------------------- header: a pixel network converging on a decision
def header():
    W, H, CY = 1200, 340, 172
    rnd = random.Random(7)
    spec = [  # x, count, half-height, half-width, pixel, grid, hot radius
        (778, 360, 128, 62, 3.2, 6, 15),
        (896, 140, 84, 40, 3.6, 7, 13),
        (992, 58, 52, 26, 4.0, 8, 11),
        (1068, 22, 28, 15, 4.4, 9, 10),
    ]
    OUTP = (1146, CY)
    anom_y = CY - 34
    layers = []
    for k, (cx, n, hy, hx, px, grid, r) in enumerate(spec):
        pts, used = [], set()
        focus_y = anom_y + (CY - anom_y) * k / (len(spec) - 1)
        fx = cx + 16 * (1 - k / (len(spec) - 1))
        guard = 0
        while len(pts) < n and guard < n * 40:
            guard += 1
            ang = rnd.random() * math.tau
            rad = abs(rnd.gauss(0, 1)) * 0.48 + rnd.random() * 0.08
            gy = math.sin(ang) * rad * hy * (1 + 0.18 * math.sin(ang * 3 + k))
            gx = math.cos(ang) * rad * hx * (1 + 0.22 * math.cos(ang * 2 - k))
            if abs(gy) > hy or abs(gx) > hx:
                continue
            x, y = round((cx + gx) / grid) * grid, round((CY + gy) / grid) * grid
            if (x, y) in used:
                continue
            used.add((x, y))
            hot = math.exp(-((math.hypot(x - fx, y - focus_y) / r) ** 2))
            pts.append(dict(x=x, y=y, hot=hot, a=0.12 + 0.36 * rnd.random(), dz=(x - cx) / hx))
        layers.append(dict(pts=pts, px=px, k=k))

    body = []
    # wiring
    wires = []
    for k in range(len(layers) - 1):
        A, B = layers[k]["pts"], layers[k + 1]["pts"]
        for i in range(0, len(A), 3):
            p, q = A[i], B[rnd.randrange(len(B))]
            wires.append(f'<line x1="{p["x"]}" y1="{p["y"]}" x2="{q["x"]}" y2="{q["y"]}"/>')
    body.append(f'<g stroke="{INK}" stroke-opacity=".03" stroke-width=".5">{"".join(wires)}</g>')
    # lit receptive path
    path_pts = []
    for k in range(len(layers) - 1):
        A = sorted(layers[k]["pts"], key=lambda p: -p["hot"])[: (8 if k == 0 else 6)]
        B = sorted(layers[k + 1]["pts"], key=lambda p: -p["hot"])[:2]
        col = mix(AMB, MINT, k / (len(layers) - 1))
        lines = "".join(f'<line x1="{p["x"]}" y1="{p["y"]}" x2="{B[i % 2]["x"]}" y2="{B[i % 2]["y"]}"/>' for i, p in enumerate(A))
        body.append(f'<g stroke="{col}" stroke-opacity=".34" stroke-width=".8">{lines}</g>')
        path_pts.append((A[0]["x"], A[0]["y"]))
    last = layers[-1]["pts"]
    lh = max(last, key=lambda p: p["hot"])
    path_pts += [(lh["x"], lh["y"]), OUTP]
    ow = "".join(f'<line x1="{p["x"]}" y1="{p["y"]}" x2="{OUTP[0]}" y2="{OUTP[1]}" stroke="{MINT if p["hot"] > .5 else INK}" stroke-opacity="{.42 if p["hot"] > .5 else .06}" stroke-width="{.8 if p["hot"] > .5 else .5}"/>' for p in last)
    body.append(f"<g>{ow}</g>")
    # pixels, twinkling in four phases
    groups = {1: [], 2: [], 3: [], 4: []}
    hot_px = []
    for L in layers:
        t = L["k"] / (len(layers) - 1)
        for p in sorted(L["pts"], key=lambda p: p["dz"]):
            depth = 0.55 + 0.45 * (p["dz"] * 0.5 + 0.5)
            s = L["px"] * (0.75 + 0.35 * depth)
            if p["hot"] > 0.42:
                c = mix(AMB, MINT, t)
                hot_px.append(f'<rect x="{p["x"] - s / 2:.1f}" y="{p["y"] - s / 2:.1f}" width="{s:.1f}" height="{s:.1f}" fill="{c}" fill-opacity="{.45 + .5 * p["hot"]:.2f}"/>')
            else:
                g = rnd.randint(1, 4)
                groups[g].append(f'<rect x="{p["x"] - s / 2:.1f}" y="{p["y"] - s / 2:.1f}" width="{s:.1f}" height="{s:.1f}" fill-opacity="{p["a"] * depth:.2f}"/>')
    for g, rects in groups.items():
        body.append(f'<g class="t{g}" fill="{mix(IND, INK, .1)}">{"".join(rects)}</g>')
    body.append(f'<g>{"".join(hot_px)}</g>')
    # a signal travelling the lit path into the output
    d = "M" + " L".join(f"{x},{y}" for x, y in path_pts)
    body.append(f'<path id="sig" d="{d}" fill="none" stroke="none"/>')
    for i, col in enumerate([AMB, MINT]):
        body.append(f'''<circle r="3" fill="{col}"><animateMotion dur="3.6s" begin="{i * 1.8}s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.8;1" calcMode="linear"><mpath href="#sig"/></animateMotion>
  <animate attributeName="fill" values="{AMB};{MINT};{MINT}" keyTimes="0;.8;1" dur="3.6s" begin="{i * 1.8}s" repeatCount="indefinite"/></circle>''')
    ox, oy = OUTP
    body.append(f'''<circle cx="{ox}" cy="{oy}" r="40" fill="url(#glowMint)" class="breathe"/>
<rect x="{ox - 4}" y="{oy - 4}" width="8" height="8" fill="{MINT}"/>
<rect x="{ox - 10.5}" y="{oy - 10.5}" width="21" height="21" fill="none" stroke="{MINT}" stroke-opacity=".5"/>
<rect x="{ox - 18.5}" y="{oy - 18.5}" width="37" height="37" fill="none" stroke="{MINT}" stroke-opacity=".16"/>''')

    # text
    chips = ["AI for SRE", "Platform engineering", "Infrastructure at scale", "Observability"]
    cx, cw = 56, []
    for c in chips:
        w = 18 + len(c) * 7.6
        cw.append(f'<rect x="{cx}" y="232" width="{w:.0f}" height="30" rx="15" fill="#ffffff" fill-opacity=".04" stroke="{LINE}"/><text x="{cx + w / 2:.0f}" y="252" text-anchor="middle" class="sans" font-size="13.5" font-weight="600" fill="{INK}">{c}</text>')
        cx += w + 8
    body.append(f'''
<g>
  <circle cx="62" cy="58" r="4.5" fill="{MINT}" class="pulse"/>
  <text x="76" y="63" class="mono" font-size="13" fill="{MUTED}">all systems operational</text>
  <text x="56" y="124" class="sans" font-size="54" font-weight="700" fill="{INK}" letter-spacing="-1.6">Gaurav G S</text>
  <text x="56" y="160" class="sans" font-size="21" font-weight="600" fill="{INK}">Senior Site Reliability Engineer</text>
  <text x="56" y="194" class="sans" font-size="17" fill="{MUTED}">Teaching infrastructure to heal itself.</text>
  {"".join(cw)}
  <text x="56" y="300" class="mono" font-size="13" fill="{IND}">gaurav-gs7.pages.dev  →</text>
</g>''')
    save("header.svg", panel(W, H, "\n".join(body), glow=(960, 170)))


# ---------------------------------------------------------------- pipeline: how an incident heals
def pipeline():
    W, H, Y = 1200, 210, 104
    stages = [("Notice", "Argus", "alerts → one incident"), ("Connect", "Argus", "walk the topology"),
              ("Suggest", "LLM", "advise, never decide"), ("Approve", "Judikt", "policy gates the fix"),
              ("Fix", "Helios", "durable remediation"), ("Confirm", "Attesta", "SLOs back in range")]
    x0, step = 110, 196
    xs = [x0 + i * step for i in range(len(stages))]
    cols = [IND, IND, AMB, MINT, AMB, MINT]
    T, run = 10, 0.82
    body = [f'<text x="40" y="38" class="mono" font-size="12.5" fill="{FAINT}">how an incident heals</text>',
            f'<text x="{W - 40}" y="38" text-anchor="end" class="mono" font-size="12.5" fill="{FAINT}">every step hash-chained into an audit trail</text>',
            f'<line x1="{xs[0]}" y1="{Y}" x2="{xs[-1]}" y2="{Y}" stroke="{LINE}" stroke-width="2"/>',
            f'<line x1="{xs[0]}" y1="{Y}" x2="{xs[-1]}" y2="{Y}" stroke="{MINT}" stroke-width="2" stroke-dasharray="{xs[-1] - xs[0]}" stroke-dashoffset="{xs[-1] - xs[0]}">'
            f'<animate attributeName="stroke-dashoffset" values="{xs[-1] - xs[0]};0;0;{xs[-1] - xs[0]}" keyTimes="0;{run};.96;1" dur="{T}s" repeatCount="indefinite"/></line>']
    for i, ((name, who, cap), x, c) in enumerate(zip(stages, xs, cols)):
        t = run * i / (len(stages) - 1)
        a, b2 = max(0, t - 0.02), min(.999, t + 0.1)
        body.append(f'''<g>
  <circle cx="{x}" cy="{Y}" r="22" fill="{c}" fill-opacity="0"><animate attributeName="fill-opacity" values="0;0;.22;.06;.06;0" keyTimes="0;{a:.3f};{t + .01:.3f};{b2:.3f};.96;1" dur="{T}s" repeatCount="indefinite"/></circle>
  <circle cx="{x}" cy="{Y}" r="13" fill="{BG0}" stroke="{FAINT}" stroke-width="1.5"><animate attributeName="stroke" values="{FAINT};{FAINT};{c};{c};{FAINT}" keyTimes="0;{a:.3f};{t + .01:.3f};.96;1" dur="{T}s" repeatCount="indefinite"/></circle>
  <circle cx="{x}" cy="{Y}" r="4" fill="{FAINT}"><animate attributeName="fill" values="{FAINT};{FAINT};{c};{c};{FAINT}" keyTimes="0;{a:.3f};{t + .01:.3f};.96;1" dur="{T}s" repeatCount="indefinite"/></circle>
  <text x="{x}" y="{Y - 34}" text-anchor="middle" class="mono" font-size="11.5" fill="{FAINT}">{cap}</text>
  <text x="{x}" y="{Y + 44}" text-anchor="middle" class="sans" font-size="16" font-weight="700" fill="{INK}">{name}</text>
  <text x="{x}" y="{Y + 64}" text-anchor="middle" class="mono" font-size="12" fill="{c}">{who}</text>
</g>''')
    body.append(f'''<circle r="5" fill="{RED}"><animateMotion path="M{xs[0]},{Y} L{xs[-1]},{Y}" keyPoints="0;1;1" keyTimes="0;{run};1" dur="{T}s" repeatCount="indefinite" calcMode="linear"/>
  <animate attributeName="fill" values="{RED};{AMB};{MINT};{MINT}" keyTimes="0;.35;{run};1" dur="{T}s" repeatCount="indefinite"/></circle>''')
    save("pipeline.svg", panel(W, H, "\n".join(body), glow=(600, 105)))


# ---------------------------------------------------------------- project cards
def card(name, file, tagline, stack, badge, badge_col, glyph):
    W, H = 590, 220
    lines = "".join(f'<text x="214" y="{98 + i * 22}" class="sans" font-size="14.5" fill="{MUTED}">{t}</text>' for i, t in enumerate(tagline))
    bw = 16 + len(badge) * 7.2
    body = f'''
<g>{glyph}</g>
<line x1="192" y1="28" x2="192" y2="{H - 28}" stroke="{LINE}"/>
<text x="214" y="64" class="sans" font-size="26" font-weight="700" fill="{INK}" letter-spacing="-.4">{name}</text>
<rect x="{W - 26 - bw:.0f}" y="40" width="{bw:.0f}" height="24" rx="12" fill="{badge_col}" fill-opacity=".12" stroke="{badge_col}" stroke-opacity=".45"/>
<text x="{W - 26 - bw / 2:.0f}" y="56.5" text-anchor="middle" class="mono" font-size="11.5" fill="{badge_col}">{badge}</text>
{lines}
<text x="214" y="{H - 30}" class="mono" font-size="12" fill="{FAINT}">{stack}</text>
<text x="{W - 26}" y="{H - 30}" text-anchor="end" class="mono" font-size="12" fill="{IND}">open repo →</text>'''
    save(file, panel(W, H, body, glow=(96, 110)))


def glyph_judikt():
    cx, cy = 96, 110
    out = [f'<line x1="{cx}" y1="40" x2="{cx}" y2="180" stroke="{MINT}" stroke-opacity=".7" stroke-width="1.6"/>',
           f'<path d="M{cx},28 l14,6 v10 c0,9 -6,15 -14,18 c-8,-3 -14,-9 -14,-18 v-10 z" fill="{MINT}" fill-opacity=".12" stroke="{MINT}" stroke-width="1.4"/>',
           f'<path d="M{cx - 5},45 l4,4 l7,-7" fill="none" stroke="{MINT}" stroke-width="1.6"/>']
    lanes = [74, 96, 118, 140, 162]
    for i, y in enumerate(lanes):
        denied = i == 2
        dur, beg = 2.6, i * 0.52
        if denied:
            out.append(f'<circle r="3.4" fill="{RED}"><animateMotion path="M24,{y} L{cx - 6},{y} L{cx - 26},{y}" keyPoints="0;.78;1" keyTimes="0;.6;1" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                       f'<animate attributeName="opacity" values="1;1;0" keyTimes="0;.6;1" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/></circle>')
        else:
            out.append(f'<circle r="3" fill="{IND}"><animateMotion path="M24,{y} L168,{y}" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                       f'<animate attributeName="fill" values="{IND};{IND};{MINT};{MINT}" keyTimes="0;.49;.51;1" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


def glyph_argus():
    cx, cy = 96, 110
    rnd = random.Random(3)
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{IND}" stroke-opacity="{o}"/>' for r, o in [(70, .14), (48, .18), (26, .22)]]
    out.append(f'<g style="transform-origin:{cx}px {cy}px;animation:spin 4s linear infinite"><path d="M{cx},{cy} L{cx},{cy - 70} A70,70 0 0,1 {cx + 49.5},{cy - 49.5} Z" fill="{IND}" fill-opacity=".14"/><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - 70}" stroke="{IND}" stroke-opacity=".7"/></g>')
    cluster = [(cx + 28, cy - 22), (cx + 40, cy - 6), (cx + 18, cy - 4)]
    out.append(f'<polyline points="{" ".join(f"{x},{y}" for x, y in cluster + [cluster[0]])}" fill="{AMB}" fill-opacity=".08" stroke="{AMB}" stroke-opacity=".6" stroke-dasharray="3 3"/>')
    for i, (x, y) in enumerate(cluster):
        out.append(f'<circle cx="{x}" cy="{y}" r="3.6" fill="{AMB}" class="pulse" style="animation-delay:{i * .3}s"/>')
    for _ in range(9):
        a, r = rnd.random() * math.tau, 20 + rnd.random() * 46
        out.append(f'<circle cx="{cx + math.cos(a) * r:.1f}" cy="{cy + math.sin(a) * r:.1f}" r="2.2" fill="{IND}" class="t{rnd.randint(1, 4)}"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{INK}"/>')
    return "".join(out)


def glyph_helios():
    N = {"a": (36, 110), "b": (82, 70), "c": (82, 150), "d": (128, 110), "e": (164, 110)}
    E = [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d"), ("d", "e")]
    out = [f'<line x1="{N[a][0]}" y1="{N[a][1]}" x2="{N[b][0]}" y2="{N[b][1]}" stroke="{FAINT}" stroke-width="1.4"/>' for a, b in E]
    T = 4
    order = {"a": 0, "b": .25, "c": .25, "d": .55, "e": .8}
    for k, (x, y) in N.items():
        t = order[k]
        out.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{BG0}" stroke="{FAINT}" stroke-width="1.5"><animate attributeName="stroke" values="{FAINT};{FAINT};{AMB};{MINT};{MINT};{FAINT}" keyTimes="0;{max(0, t - .01):.2f};{t:.2f};{min(.95, t + .12):.2f};.95;1" dur="{T}s" repeatCount="indefinite"/></circle>')
    for path, beg in [("M36,110 L82,70 L128,110 L164,110", 0), ("M36,110 L82,150 L128,110", 0)]:
        out.append(f'<circle r="3.4" fill="{AMB}"><animateMotion path="{path}" keyPoints="0;1;1" keyTimes="0;.8;1" dur="{T}s" begin="{beg}s" repeatCount="indefinite"/></circle>')
    out.append(f'<text x="100" y="188" text-anchor="middle" class="mono" font-size="10.5" fill="{FAINT}">lease · retry · resume</text>')
    return "".join(out)


def glyph_attesta():
    base, top = 160, 50
    out = [f'<line x1="28" y1="{base}" x2="168" y2="{base}" stroke="{FAINT}"/>',
           f'<line x1="28" y1="72" x2="168" y2="72" stroke="{RED}" stroke-opacity=".55" stroke-dasharray="4 4"/>',
           f'<text x="168" y="66" text-anchor="end" class="mono" font-size="10" fill="{RED}" fill-opacity=".8">SLO</text>']
    steps = [5, 25, 50, 100]
    for i, pct in enumerate(steps):
        x, h = 40 + i * 32, 52 * pct / 100 + 4
        out.append(f'<rect x="{x}" y="{base - h:.0f}" width="22" height="{h:.0f}" rx="3" fill="{MINT}" fill-opacity=".55" class="grow" style="animation-delay:{i * 1.0:.1f}s"/>'
                   f'<text x="{x + 11}" y="{base + 16}" text-anchor="middle" class="mono" font-size="10" fill="{FAINT}">{pct}%</text>')
    out.append(f'<polyline points="28,96 52,92 76,94 100,89 124,91 148,87 168,89" fill="none" stroke="{IND}" stroke-width="1.4" stroke-opacity=".8"/>'
               f'<text x="28" y="84" class="mono" font-size="10" fill="{IND}" fill-opacity=".8">p99</text>')
    return "".join(out)


def glyph_inferlab():
    out = []
    verdicts = [("PASS", MINT, 58), ("BLOCK", RED, 98), ("INCONCLUSIVE", AMB, 138)]
    T = 6
    for i, (v, c, y) in enumerate(verdicts):
        a, b = i / 3, (i + 1) / 3
        out.append(f'<rect x="30" y="{y - 15}" width="132" height="26" rx="13" fill="{c}" fill-opacity=".05" stroke="{c}" stroke-opacity=".25">'
                   f'<animate attributeName="fill-opacity" values=".05;.05;.2;.2;.05;.05" keyTimes="0;{a:.2f};{a + .02:.2f};{b - .02:.2f};{b:.2f};1" dur="{T}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="stroke-opacity" values=".25;.25;.9;.9;.25;.25" keyTimes="0;{a:.2f};{a + .02:.2f};{b - .02:.2f};{b:.2f};1" dur="{T}s" repeatCount="indefinite"/></rect>'
                   f'<text x="96" y="{y + 2.5}" text-anchor="middle" class="mono" font-size="11.5" font-weight="700" fill="{c}">{v}</text>')
    out.append(f'<text x="96" y="186" text-anchor="middle" class="mono" font-size="10.5" fill="{FAINT}">evidence first, then a verdict</text>')
    return "".join(out)


def cards():
    card("Judikt", "card-judikt.svg", ["Security gateway for AI agents using MCP.", "Policy, identity and approvals on every", "tool call, with a hash-chained audit trail."],
         "Python · MCP · OIDC · Redis · OTel", "v0.3.0 · PyPI", MINT, glyph_judikt())
    card("Argus", "card-argus.svg", ["Incident correlation and root-cause", "analysis. Deterministic scoring first;", "the LLM only explains."],
         "Go · PostgreSQL · NATS · OTel", "AIOps", IND, glyph_argus())
    card("Helios", "card-helios.svg", ["Durable DAG workflow engine that survives", "crashes mid-run: leases, heartbeats,", "retries and dead-worker recovery."],
         "Go · PostgreSQL · NATS", "learning project", FAINT, glyph_helios())
    card("Attesta", "card-attesta.svg", ["Kubernetes reliability control plane:", "readiness scoring, SLO-guarded rollouts", "and automatic rollback."],
         "Go · Kubernetes · Argo CD", "platform", IND, glyph_attesta())
    card("InferLab", "card-inferlab.svg", ["Release checks for LLM inference changes.", "Checks the evidence before it trusts", "the benchmark."],
         "Go · evidence contracts · Ed25519", "pre-alpha", AMB, glyph_inferlab())


# ---------------------------------------------------------------- career as a distributed trace
def career():
    W, H = 1200, 330
    t0, t1 = 2020.6, 2027.6               # axis range in years
    X0, X1 = 330, 1150
    xof = lambda t: X0 + (t - t0) / (t1 - t0) * (X1 - X0)
    NOW = 2026 + 9.9 / 12
    spans = [  # label, sub, start, end, colour, duration text, events
        ("google-cloud", "cloud apprenticeship", 2020 + 11 / 12, 2021 + 2 / 12, FAINT, "4 mos", []),
        ("phonepe", "sre intern · zookeeper, glusterfs", 2022 + 2 / 12, 2022 + 6 / 12, IND, "5 mos", []),
        ("phonepe", "sre-1 · UPI PSP infrastructure", 2022 + 7 / 12, 2025 + 3 / 12, IND, "2 yrs 9 mos",
         [(2022.95, "mesos → drove"), (2023.85, "dc migration"), (2024.75, "backups −33%")]),
        ("mastercard", "sre-2 · banking platform", 2025 + 3 / 12, NOW, MINT, "1 yr 6 mos · now", [(2025.75, "release automation")]),
        ("open-source", "ai-sre platform", 2026.0, NOW, AMB, "argus · judikt · helios", [(2026.72, "judikt v0.3.0")]),
    ]
    ROW0, RH = 96, 40
    body = [f'<text x="40" y="38" class="mono" font-size="12.5" fill="{FAINT}">trace</text>',
            f'<text x="86" y="38" class="mono" font-size="12.5" fill="{INK}">career.gaurav-gs7</text>',
            f'<text x="{W - 40}" y="38" text-anchor="end" class="mono" font-size="12.5" fill="{FAINT}">5 spans · status ok</text>']
    for y in range(2021, 2028):
        x = xof(y)
        body.append(f'<line x1="{x:.1f}" y1="56" x2="{x:.1f}" y2="{H - 30}" stroke="{LINE}" stroke-dasharray="2 4"/>'
                    f'<text x="{x:.1f}" y="72" text-anchor="middle" class="mono" font-size="11" fill="{FAINT}">{y}</text>')
    # root span
    body.append(f'<rect x="{xof(2020.9):.1f}" y="{ROW0 - 18}" width="{xof(NOW) - xof(2020.9):.1f}" height="4" rx="2" fill="{INK}" fill-opacity=".25"/>')
    for i, (svc, sub, s, e, c, dur, evs) in enumerate(spans):
        y = ROW0 + i * RH
        xs, xe = xof(s), xof(e)
        live = e >= NOW
        indent = 40 + (0 if i < 4 else 16)
        body.append(f'<text x="{indent}" y="{y + 6}" class="mono" font-size="13" fill="{c if c != FAINT else MUTED}">{svc}</text>'
                    f'<text x="{indent}" y="{y + 22}" class="sans" font-size="12" fill="{FAINT}">{sub}</text>')
        body.append(f'<rect x="{xs:.1f}" y="{y - 6}" width="{xe - xs:.1f}" height="16" rx="4" fill="{c}" fill-opacity="{.5 if c != FAINT else .35}"/>')
        if live:
            body.append(f'<rect x="{xe - 2:.1f}" y="{y - 9}" width="4" height="22" rx="2" fill="{c}" class="pulse"/>')
        for et, label in evs:
            ex = xof(et)
            body.append(f'<path d="M{ex:.1f},{y - 3} l5,5 l-5,5 l-5,-5 z" fill="{INK}" fill-opacity=".9"/>'
                        f'<text x="{ex:.1f}" y="{y - 12}" text-anchor="middle" class="mono" font-size="10" fill="{MUTED}">{label}</text>')
        tx = xe + 10 if not live else xe + 12
        body.append(f'<text x="{tx:.1f}" y="{y + 6}" class="mono" font-size="11" fill="{FAINT}">{dur}</text>' if xe < X1 - 140 else
                    f'<text x="{xs - 8:.1f}" y="{y + 6}" text-anchor="end" class="mono" font-size="11" fill="{FAINT}">{dur}</text>')
    # next: a dashed span beyond now
    yN = ROW0 + len(spans) * RH
    body.append(f'<text x="40" y="{yN + 6}" class="mono" font-size="13" fill="{MINT}">next</text>'
                f'<text x="40" y="{yN + 22}" class="sans" font-size="12" fill="{FAINT}">ai sre · platform · infrastructure</text>'
                f'<rect x="{xof(NOW):.1f}" y="{yN - 6}" width="{X1 - xof(NOW):.1f}" height="16" rx="4" fill="none" stroke="{MINT}" stroke-dasharray="4 4" stroke-opacity=".7">'
                f'<animate attributeName="stroke-dashoffset" values="0;-16" dur="1.2s" repeatCount="indefinite"/></rect>')
    xn = xof(NOW)
    body.append(f'<line x1="{xn:.1f}" y1="56" x2="{xn:.1f}" y2="{H - 30}" stroke="{MINT}" stroke-opacity=".5"/>'
                f'<text x="{xn:.1f}" y="{H - 14}" text-anchor="middle" class="mono" font-size="11" fill="{MINT}">now</text>')
    save("career.svg", panel(W, H + 40, "\n".join(body), glow=(800, 160)))


# ---------------------------------------------------------------- footer: a calm heartbeat
def footer():
    W, H = 1200, 110
    pts, y0 = [], 60
    for x in range(40, W - 40, 4):
        u = ((x - 40) / 260) % 1
        if .40 < u < .44: y = y0 + (u - .40) / .04 * 6
        elif .44 < u < .48: y = y0 + 6 - (u - .44) / .04 * 34
        elif .48 < u < .52: y = y0 - 28 + (u - .48) / .04 * 38
        elif .52 < u < .56: y = y0 + 10 - (u - .52) / .04 * 10
        else: y = y0
        pts.append(f"{x},{y:.1f}")
    L = 2600
    body = f'''<polyline points="{" ".join(pts)}" fill="none" stroke="{MINT}" stroke-opacity=".18" stroke-width="1.5"/>
<polyline points="{" ".join(pts)}" fill="none" stroke="{MINT}" stroke-width="1.8" stroke-dasharray="180 {L}">
  <animate attributeName="stroke-dashoffset" values="180;-{L}" dur="5s" repeatCount="indefinite"/></polyline>
<text x="{W / 2}" y="98" text-anchor="middle" class="mono" font-size="12" fill="{FAINT}">steady state · open to SRE, platform and AI-infrastructure roles · remote or Bengaluru</text>'''
    save("footer.svg", panel(W, H + 10, body, glow=(600, 60)))


if __name__ == "__main__":
    header(); pipeline(); cards(); career(); footer()
