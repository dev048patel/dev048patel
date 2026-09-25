"""Generates the animated SVG cards for the dev048patel profile README."""
from pathlib import Path

import live

D = live.gather()

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

FONT = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
BG, PANEL, LINE = "#0b0c0e", "#101215", "#23272e"
TXT, DIM, FAINT = "#e8e8e8", "#7a818c", "#3a3f47"
AMBER, GREEN, CYAN, RED, VIOLET, TEAL = "#f5a524", "#4ade80", "#38bdf8", "#ef4444", "#a78bfa", "#2dd4bf"

BASE_CSS = """
text{font-family:%s}
.cap{font-size:9px;letter-spacing:1.4px;font-weight:700}
.dim{fill:%s}
.blink{animation:blink 1.1s steps(1) infinite}
@keyframes blink{50%%{opacity:0}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
""" % (FONT, DIM)

DEFS = """
<defs>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="6"/>
  </filter>
  <linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffffff" stop-opacity=".035"/>
    <stop offset=".35" stop-color="#ffffff" stop-opacity="0"/>
  </linearGradient>
</defs>"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(name, w, h, body, css="", title=""):
    doc = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<style>{BASE_CSS}{css}</style>
{DEFS}
<rect width="{w}" height="{h}" rx="12" fill="{BG}"/>
{body}
</svg>"""
    (OUT / f"{name}.svg").write_text(doc)


def panel(w, h, accent, mark=""):
    s = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="11" fill="{PANEL}" stroke="{LINE}"/>'
    s += f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="11" fill="url(#sheen)"/>'
    s += f'<rect x="1" y="24" width="2" height="{h-48}" fill="{accent}" opacity=".55"/>'
    if mark:
        s += f'<text x="{w-14}" y="{h-10}" text-anchor="end" font-size="64" font-weight="800" fill="#fff" opacity=".035">{mark}</text>'
    return s


def chip(x, y, text, color, size=8.5, fill=True):
    w = len(text) * (size * 0.61 + 0.3) + 13
    bg = f'fill="{color}" fill-opacity=".12"' if fill else 'fill="none"'
    return (f'<rect x="{x}" y="{y-10}" width="{w:.1f}" height="14" rx="3" {bg} stroke="{color}" stroke-opacity=".8"/>'
            f'<text x="{x+6}" y="{y}" font-size="{size}" font-weight="700" fill="{color}" letter-spacing=".3">{esc(text)}</text>'), w


def card_head(w, tag, color, kicker, badge, title, sub, title_size=14):
    c, cw = chip(18, 28, tag, color, 7.5)
    s = c
    s += f'<text x="{18+cw+8}" y="28" class="cap dim" font-size="7.5">{esc(kicker)}</text>'
    bw = len(badge) * 8.5 * 0.6 + 16
    s += (f'<rect x="{w-18-bw:.1f}" y="15" width="{bw:.1f}" height="18" rx="4" fill="{color}" fill-opacity=".1" stroke="{color}"/>'
          f'<text x="{w-18-bw/2:.1f}" y="28" text-anchor="middle" font-size="8.5" font-weight="700" fill="{color}">{esc(badge)}</text>')
    s += f'<text x="18" y="56" font-size="{title_size}" font-weight="700" fill="{TXT}">{esc(title)}</text>'
    c, _ = chip(18, 76, sub, color, 7.5, fill=False)
    return s + c


def footer_caption(w, h, text):
    return f'<text x="{w/2}" y="{h-14}" text-anchor="middle" font-size="8.5" class="dim" opacity=".8">{esc(text)}</text>'


# --------------------------------------------------------------------------- header
def header():
    w, h = 840, 218
    b = panel(w, h, AMBER)
    b += f'<text x="26" y="30" class="cap dim">FULL-STACK · CS STUDENT · REGINA, SK · UPDATED {D["updated"]}</text>'
    b += (f'<text x="26" y="66" font-size="24" font-weight="800" fill="{TXT}">Dev Patel <tspan fill="{DIM}">—</tspan> '
          f'<tspan fill="{AMBER}" filter="url(#glow)">full-stack apps that real people use</tspan></text>')
    lines = [
        ("cs student in regina, sk. react on the front, node + fastapi in the middle, postgres underneath.", ""),
        ("i like clean ui, smooth motion, and breaking things to see how they work. ", "school is a course list."),
        ("", "shipping is the part that compounds."),
    ]
    for i, (d, strong) in enumerate(lines):
        b += (f'<text x="26" y="{94+i*16}" font-size="11" class="dim">{esc(d)}'
              f'<tspan fill="{TXT}" font-weight="700">{esc(strong)}</tspan></text>')
    x = 26
    site = "▸ gotransitregina.ca is live" if D["site_live"] else "▸ gotransitregina.ca is down right now"
    for t, col in [(site, "#9aa1ab" if D["site_live"] else RED), ("▸ bus positions every 1.5s", "#9aa1ab"),
                   (f"▸ {D['gotransit_commits']} commits and counting", "#9aa1ab")]:
        c, cw = chip(x, 162, t, col, 9.5)
        b += c
        x += cw + 8
    for i, n in enumerate(["1", "2", "3", "4"]):
        on = n == "3"
        col = AMBER if on else FAINT
        b += (f'<rect x="{26+i*22}" y="180" width="16" height="16" rx="3" fill="{col}" fill-opacity="{.15 if on else 0}" stroke="{col}"/>'
              f'<text x="{34+i*22}" y="191.5" text-anchor="middle" font-size="8.5" font-weight="700" fill="{AMBER if on else DIM}">{n}</text>')
    tail = f"last commit {live.ago(D['last_push_days'])} · the product is a line that grows with every user"
    b += f'<text x="124" y="192" font-size="9.5" class="dim">{esc(tail)}</text>'
    b += f'<rect class="blink" x="{124 + len(tail) * 5.72 + 6:.0f}" y="183" width="6" height="11" fill="{AMBER}"/>'
    svg("header", w, h, b, title="Dev Patel — full-stack apps that real people use")


# --------------------------------------------------------------------------- pixel bus
def pixel_bus(cx, cy, px=4.6):
    cols, rows = 24, 13
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    for r in range(11):
        for c in range(cols):
            grid[r][c] = "A"
    for r, c in [(0, 0), (0, 1), (1, 0), (0, 22), (0, 23), (1, 23), (10, 0), (10, 23)]:
        grid[r][c] = "."
    for c0 in (2, 6, 10, 14):
        for r in range(2, 5):
            for c in range(c0, c0 + 3):
                grid[r][c] = "W"
    for r in range(2, 10):
        for c in (19, 20):
            grid[r][c] = "W"
    for r in range(2, 5):
        grid[r][22] = "W"
    for c in range(0, 18):
        grid[7][c] = "S"
    grid[8][23] = "L"
    grid[8][0] = "T"
    for c0 in (3, 15):
        for r in range(10, 13):
            for c in range(c0, c0 + 4):
                grid[r][c] = "K"
        grid[11][c0 + 1] = grid[11][c0 + 2] = "H"
    colors = {"A": AMBER, "W": "#1a1206", "S": "#c2760a", "L": "#fff3b0", "T": RED, "K": "#15171a", "H": "#8a8f98"}
    x0, y0 = cx - cols * px / 2, cy - rows * px / 2
    body, extra = [], []
    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            if ch == ".":
                continue
            rect = f'<rect x="{x0+c*px:.1f}" y="{y0+r*px:.1f}" width="{px+.3:.1f}" height="{px+.3:.1f}" fill="{colors[ch]}"/>'
            (extra if ch in "LH" else body).append(rect)
    # window "eyes" blink (a light pixel inside two windows)
    eyes = "".join(
        f'<rect class="eye" x="{x0+c*px:.1f}" y="{y0+3*px:.1f}" width="{px:.1f}" height="{px:.1f}" fill="{AMBER}" opacity=".9"/>'
        for c in (15, 22))
    beam = (f'<path d="M{x0+24*px:.1f} {y0+8.5*px:.1f} l34 -9 v18 z" fill="#fff3b0" opacity=".12" class="beam"/>')
    return (f'<g class="bob"><g filter="url(#glow)">{"".join(body)}</g>{"".join(extra)}{eyes}{beam}</g>')


ORBIT_CSS = """
.spin{animation:spin 18s linear infinite}
.spin2{animation:spin 7s linear infinite reverse}
@keyframes spin{to{transform:rotate(360deg)}}
.bob{animation:bob 1.6s steps(2) infinite}
@keyframes bob{50%{transform:translateY(-2px)}}
.eye{animation:eye 4s steps(1) infinite}
@keyframes eye{0%,92%{opacity:.9}93%,97%{opacity:0}}
.beam{animation:beam 2.4s ease-in-out infinite}
@keyframes beam{50%{opacity:.28}}
.seal{animation:seal 1.2s steps(1) infinite}
@keyframes seal{50%{opacity:.35}}
.rise{transform-box:fill-box;transform-origin:bottom;animation:rise 2.6s cubic-bezier(.3,.7,.2,1) infinite}
@keyframes rise{0%{transform:scaleY(.15)}45%,85%{transform:scaleY(1)}100%{transform:scaleY(.15)}}
.lens{animation:lens 3.6s ease-in-out infinite alternate}
@keyframes lens{from{transform:translate(0,0)}to{transform:translate(34px,14px)}}
.now{animation:now 1.4s ease-in-out infinite}
@keyframes now{50%{opacity:.3}}
"""


def orbit(cx, cy, accent, labels, center, s=1.0):
    """Spinning tick ring + orbiting comet + labelled dots around a pixel icon.
    labels: [(text, degrees, color, extra_class)]"""
    import math
    o = f'transform-origin:{cx}px {cy}px'
    b = f'<circle cx="{cx}" cy="{cy}" r="{118*s:.1f}" fill="{accent}" opacity=".05" filter="url(#soft)"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{72*s:.1f}" fill="none" stroke="{FAINT}" stroke-width=".6"/>'
    ticks = ""
    for i in range(60):
        a = math.radians(i * 6)
        r1, r2 = ((90, 96) if i % 5 == 0 else (92, 95))
        ticks += (f'<line x1="{cx+r1*s*math.cos(a):.1f}" y1="{cy+r1*s*math.sin(a):.1f}" '
                  f'x2="{cx+r2*s*math.cos(a):.1f}" y2="{cy+r2*s*math.sin(a):.1f}" stroke="{FAINT}" stroke-width="1"/>')
    b += (f'<g class="spin" style="{o}">{ticks}<circle cx="{cx}" cy="{cy}" r="{104*s:.1f}" fill="none" '
          f'stroke="{accent}" stroke-opacity=".25" stroke-dasharray="2 7"/></g>')
    b += f'<g class="spin2" style="{o}"><circle cx="{cx+104*s:.1f}" cy="{cy}" r="2.5" fill="{accent}" filter="url(#glow)"/></g>'
    for text, deg, col, cls in labels:
        a = math.radians(deg)
        c, n = math.cos(a), math.sin(a)
        anchor = "middle" if abs(c) < .3 else ("start" if c > 0 else "end")
        ly = cy + 121 * s * n + (-4 if n < -.95 else 7 if n > .95 else 0)
        k = f' class="{cls}"' if cls else ""
        b += f'<g{k}><line x1="{cx+104*s*c:.1f}" y1="{cy+104*s*n:.1f}" x2="{cx+116*s*c:.1f}" y2="{cy+116*s*n:.1f}" stroke="{col}" stroke-opacity=".6"/>'
        b += f'<circle cx="{cx+104*s*c:.1f}" cy="{cy+104*s*n:.1f}" r="3" fill="{col}" filter="url(#glow)"/>'
        b += f'<text x="{cx+121*s*c:.1f}" y="{ly+3:.1f}" text-anchor="{anchor}" class="cap" font-size="8" fill="{col}">{esc(text)}</text></g>'
    return b + center


def _px(ox, oy, px, cells):
    """cells: (col, row, w, h, color[, class]) in pixel units -> rects."""
    out = ""
    for c in cells:
        col, row, w, h, fill = c[:5]
        k = f' class="{c[5]}"' if len(c) > 5 else ""
        out += f'<rect{k} x="{ox+col*px:.1f}" y="{oy+row*px:.1f}" width="{w*px+.3:.1f}" height="{h*px+.3:.1f}" fill="{fill}"/>'
    return out


def pixel_envelope(cx, cy, px=3.4):
    W, H = 22, 14
    ox, oy = cx - W * px / 2, cy - H * px / 2
    cells = [(0, 0, W, H, CYAN)]
    for i in range(8):  # the flap "V"
        cells += [(i, i, 1, 1, "#0b2a3a"), (W - 1 - i, i, 1, 1, "#0b2a3a")]
    cells += [(0, H - 1, W, 1, "#1d7fae")]
    seal = [(9, 7, 4, 1), (8, 8, 6, 1), (8, 9, 6, 1), (9, 10, 4, 1)]
    body = _px(ox, oy, px, cells)
    s = _px(ox, oy, px, [(c, r, w, h, RED) for c, r, w, h in seal] + [(10, 8, 2, 1, "#fff3b0"), (10, 9, 2, 1, "#fff3b0")])
    return f'<g class="bob"><g filter="url(#glow)">{body}</g><g class="seal">{s}</g></g>'


def pixel_chart(cx, cy, px=3.4):
    W, H = 22, 16
    ox, oy = cx - W * px / 2, cy - H * px / 2
    axes = _px(ox, oy, px, [(0, 0, 1, H, "#2f6b45"), (0, H - 1, W, 1, "#2f6b45")])
    bars = ""
    for i, (h, d) in enumerate([(5, 0), (8, .2), (6, .4), (11, .6), (13, .8)]):
        bars += (f'<rect class="rise" style="animation-delay:{d}s" x="{ox+(2+i*4)*px:.1f}" y="{oy+(H-1-h)*px:.1f}" '
                 f'width="{3*px:.1f}" height="{h*px:.1f}" fill="{GREEN}"/>')
    coin = _px(ox, oy, px, [(17, -4, 4, 1, AMBER), (16, -3, 6, 3, AMBER), (17, 0, 4, 1, AMBER), (18, -3, 2, 3, "#b7791f")])
    return f'<g class="bob">{axes}<g filter="url(#glow)">{bars}</g>{coin}</g>'


def pixel_code(cx, cy, px=3.4):
    W, H = 22, 16
    ox, oy = cx - W * px / 2, cy - H * px / 2
    cells = [(0, 0, W, H, "#1a1530"), (0, 0, W, 2, VIOLET), (1, .5, 1, 1, RED), (3, .5, 1, 1, AMBER), (5, .5, 1, 1, GREEN)]
    for r, (ind, ln, col) in enumerate([(1, 9, VIOLET), (3, 12, CYAN), (3, 7, "#8a8f98"), (1, 4, VIOLET), (3, 14, CYAN)]):
        cells.append((ind, 3.5 + r * 2.4, ln, 1.2, col))
    win = _px(ox, oy, px, cells)
    bug = _px(ox, oy, px, [(2.4, 8.1, 16, 1.6, RED, "seal")])
    lens = (f'<g class="lens"><circle cx="{ox+6*px:.1f}" cy="{oy+6*px:.1f}" r="{3.2*px:.1f}" fill="#fff" fill-opacity=".08" '
            f'stroke="{TXT}" stroke-width="{px*.8:.1f}"/><line x1="{ox+8.3*px:.1f}" y1="{oy+8.3*px:.1f}" '
            f'x2="{ox+11*px:.1f}" y2="{oy+11*px:.1f}" stroke="{TXT}" stroke-width="{px*1.1:.1f}" stroke-linecap="square"/></g>')
    return f'<g class="bob"><g filter="url(#glow)">{win}</g>{bug}{lens}</g>'


# --------------------------------------------------------------------------- stack (big card)
def stack():
    w, h = 840, 424
    css = ORBIT_CSS + """
.hop{animation:hop 3.2s cubic-bezier(.6,0,.4,1) infinite}
@keyframes hop{0%{transform:translateX(0);opacity:0}6%{opacity:1}94%{opacity:1}100%{transform:translateX(452px);opacity:0}}
.bar{transform-box:fill-box;transform-origin:left;animation:grow 1.6s cubic-bezier(.2,.8,.2,1) both}
@keyframes grow{from{transform:scaleX(0)}}
.pulse{animation:pulse 2s ease-in-out infinite}
@keyframes pulse{50%{opacity:.35}}
"""
    b = panel(w, h, AMBER, "01")
    b += card_head(w, "THE STACK", AMBER, "THE DEGREE IS A LIST · THE PRODUCT IS NOT", "4 hops / tap",
                   "Once a rider taps the map, every layer they touch is one i wrote",
                   "left: five hats, one developer", 15)
    b += f'<text x="190" y="76" font-size="7.5" class="dim">right: what one tap on gotransit actually does</text>'

    # ---- left: orbit + bus
    cx, cy = 178, 232
    hats = [("FRONTEND", -90, CYAN, ""), ("DESIGN", -18, RED, ""), ("DATABASE", 54, VIOLET, ""),
            ("DEPLOY", 126, GREEN, ""), ("BACKEND", 198, AMBER, "")]
    b += orbit(cx, cy, AMBER, hats, pixel_bus(cx, cy))
    b += f'<text x="{cx}" y="374" text-anchor="middle" class="cap" font-size="10" fill="{AMBER}">THE DEVELOPER</text>'
    b += f'<text x="{cx}" y="388" text-anchor="middle" font-size="8" class="dim">five hats · one keyboard</text>'

    # ---- right: request route
    X = 340
    b += f'<text x="{X}" y="116" class="cap" fill="{AMBER}">ONE TAP · FOUR HOPS</text>'
    nodes = [("a rider taps", None, 84, False), ("React 19", "view · ui", 100, True),
             ("Express 5", "api · node", 100, True), ("Supabase", "postgres · auth", 100, True),
             ("the map", None, 60, False)]
    b += f'<circle class="hop" cx="{X+4}" cy="146" r="3" fill="{GREEN}" filter="url(#glow)"/>'
    x = X
    centers = []
    for label, sub, nw, boxed in nodes:
        if boxed:
            b += f'<rect x="{x}" y="128" width="{nw}" height="36" rx="5" fill="{PANEL}"/>'
            b += f'<rect x="{x}" y="128" width="{nw}" height="36" rx="5" fill="{TEAL}" fill-opacity=".06" stroke="{TEAL}" stroke-opacity=".6"/>'
            b += f'<text x="{x+nw/2}" y="143" text-anchor="middle" font-size="9.5" font-weight="700" fill="{TXT}">{label}</text>'
            b += f'<text x="{x+nw/2}" y="156" text-anchor="middle" font-size="7.5" class="dim">{sub}</text>'
        else:
            b += f'<rect x="{x}" y="134" width="{nw}" height="24" rx="4" fill="{PANEL}" stroke="{FAINT}" stroke-dasharray="2 2"/>'
            b += f'<text x="{x+nw/2}" y="149" text-anchor="middle" font-size="8.5" class="dim">{label}</text>'
        centers.append((x, nw))
        x += nw + 8
    for (x1, w1), (x2, _) in zip(centers, centers[1:]):
        b += f'<line x1="{x1+w1}" y1="146" x2="{x2}" y2="146" stroke="{TEAL}" stroke-opacity=".5"/>'
    b += f'<text x="{X}" y="184" font-size="8" class="dim">every tap runs this route · the map redraws the result</text>'
    b += f'<text x="{w-22}" y="185" text-anchor="end" font-size="12" font-weight="800" fill="{GREEN}">1.5s a poll</text>'

    # ---- right: bars
    b += f'<text x="{X}" y="220" class="cap" fill="{AMBER}">WHERE THE HOURS GO · AGAINST A FULL WEEK</text>'
    BX, BW = 556, 186
    b += f'<text x="{BX+BW}" y="220" text-anchor="end" font-size="7.5" class="dim">full week</text>'
    b += f'<line x1="{BX+BW}" y1="226" x2="{BX+BW}" y2="352" stroke="{DIM}" stroke-opacity=".5" stroke-dasharray="2 3"/>'
    rows = [("typescript · react", "the front", .9, GREEN, "daily"),
            ("node · express", "the api", .74, CYAN, "daily"),
            ("python · fastapi", "scripts, apis", .52, AMBER, "weekly"),
            ("postgres · supabase", "the data", .44, VIOLET, "weekly"),
            ("java · c++", "coursework", .26, "#f87171", "for class")]
    for i, (lab, sub, frac, col, val) in enumerate(rows):
        y = 242 + i * 24
        b += f'<text x="{X}" y="{y+4}" font-size="9.5" font-weight="700" fill="{col}">{lab}</text>'
        b += f'<text x="470" y="{y+4}" font-size="7.5" class="dim">{sub}</text>'
        b += f'<rect x="{BX}" y="{y-5}" width="{BW}" height="11" rx="2" fill="#1a1d22"/>'
        b += (f'<rect class="bar" style="animation-delay:{.2+i*.15:.2f}s" x="{BX}" y="{y-5}" width="{BW*frac:.1f}" height="11" rx="2" '
              f'fill="{col}" fill-opacity=".85" filter="url(#glow)"/>')
        b += f'<text x="{w-22}" y="{y+4}" text-anchor="end" font-size="9" font-weight="700" fill="{col}">{val}</text>'
    b += f'<line x1="{X}" y1="368" x2="{w-22}" y2="368" stroke="{LINE}"/>'
    b += f'<text x="{X}" y="386" font-size="9.5" font-weight="700" fill="{TXT}">gotransit = react + express + supabase</text>'
    b += f'<text x="{w-22}" y="386" text-anchor="end" font-size="9" fill="{CYAN if D["site_live"] else RED}">{"live" if D["site_live"] else "down"}: gotransitregina.ca</text>'
    b += footer_caption(w, h, "not a skill rating · just where the hours go · every layer i can touch is a layer i can fix")
    svg("stack", w, h, b, css, "The stack: one tap on GoTransit runs through React, Express and Supabase")


# --------------------------------------------------------------------------- belt
def loop():
    w, h = 420, 310
    css = """
.belt{animation:belt 1s linear infinite}
@keyframes belt{to{stroke-dashoffset:-12}}
.pk{animation:pk 6s linear infinite}
@keyframes pk{
 0%{transform:translateX(0);fill:#4b5563;opacity:0}
 4%{opacity:1}
 16.9%{fill:#4b5563}17%{fill:#e5e7eb}
 49.9%{fill:#e5e7eb}50%{fill:#38bdf8}
 82.9%{fill:#38bdf8}83%{fill:#4ade80}
 96%{opacity:1}
 100%{transform:translateX(360px);fill:#4ade80;opacity:0}}
.st{animation:st 2s ease-in-out infinite}
@keyframes st{50%{stroke-opacity:.35}}
"""
    b = panel(w, h, CYAN, "02")
    b += card_head(w, "THE LOOP", CYAN, "THREE STATIONS TOUCH EVERY BUS", "1.5s each",
                   "Every bus rides the same loop, all day", "watch the boxes turn green as the map draws them")
    b += f'<text x="{w/2}" y="104" text-anchor="middle" class="cap" fill="{CYAN}" font-size="9.5">EVERY BUS RIDES THE SAME LOOP</text>'
    stations = [("POLL", "/buses", GREEN), ("CACHE", "merge · diff", CYAN), ("RENDER", "markers", GREEN)]
    for i, (a, s, col) in enumerate(stations):
        x = 40 + i * 122
        b += f'<rect class="st" style="animation-delay:{i*.5}s" x="{x}" y="116" width="96" height="42" rx="6" fill="{col}" fill-opacity=".04" stroke="{col}" stroke-opacity=".7"/>'
        b += f'<text x="{x+48}" y="134" text-anchor="middle" font-size="11" font-weight="700" fill="{TXT}">{a}</text>'
        b += f'<text x="{x+48}" y="148" text-anchor="middle" font-size="8" class="dim">{s}</text>'
        b += f'<rect x="{x+40}" y="158" width="16" height="10" fill="{col}" fill-opacity=".5"/>'
    b += f'<line x1="22" y1="190" x2="{w-22}" y2="190" stroke="{FAINT}" stroke-width="6" stroke-linecap="round"/>'
    b += f'<line class="belt" x1="22" y1="190" x2="{w-22}" y2="190" stroke="#2a2f36" stroke-width="2" stroke-dasharray="6 6"/>'
    for i in range(5):
        b += f'<rect class="pk" style="animation-delay:{-i*1.2:.1f}s" x="24" y="176" width="14" height="10" rx="2" fill="#4b5563"/>'
    # stats box
    b += f'<rect x="18" y="212" width="{w-36}" height="54" rx="6" fill="#0d0f12" stroke="{LINE}"/>'
    stats = [("poll every", "1.5s", GREEN, 32, "start"), ("polls an hour", "2,400", TXT, w / 2, "middle"),
             ("stale buses", "dropped", CYAN, w - 32, "end")]
    for lab, val, col, x, anc in stats:
        b += f'<text x="{x}" y="232" text-anchor="{anc}" font-size="8.5" class="dim">{lab}</text>'
        b += f'<text x="{x}" y="254" text-anchor="{anc}" font-size="16" font-weight="800" fill="{col}">{val}</text>'
    b += footer_caption(w, h, "2,400 polls an hour · the loop never stops while the buses run")
    svg("loop", w, h, b, css, "GoTransit live-tracking loop: poll, cache, render every 1.5 seconds")


# --------------------------------------------------------------------------- cells
def cells():
    w, h = 420, 310
    n_ok = 31
    css = """
.c{animation:lit 12s ease-out infinite both}
@keyframes lit{0%{fill:#1b1e23}2%,86%{fill:var(--c)}94%,100%{fill:#1b1e23}}
"""
    b = panel(w, h, GREEN, "03")
    b += card_head(w, "THE CELLS", GREEN, "ONE CELL IS ONE PERCENT OF DOMAINS", "31 / 69",
                   "A hundred domains, lit one at a time", "green is protected · red is anyone-can-spoof-you")
    b += f'<text x="31" y="104" class="cap" fill="{GREEN}" font-size="9.5">100 DOMAINS · ONE CELL IS 1%</text>'
    b += f'<text x="{w-31}" y="104" text-anchor="end" font-size="10" font-weight="800" fill="{TXT}">31 / 69</text>'
    s, g = 15, 3
    for i in range(100):
        r, c = divmod(i, 20)
        col = GREEN if i < n_ok else RED
        op = "" if i < n_ok else ' fill-opacity=".85"'
        b += (f'<rect class="c" style="--c:{col};animation-delay:{i*.07:.2f}s" x="{31+c*(s+g)}" y="{114+r*(s+g)}" '
              f'width="{s}" height="{s}" rx="2.5" fill="#1b1e23"{op}/>')
    y = 222
    b += f'<rect x="31" y="{y-8}" width="8" height="8" rx="1.5" fill="{GREEN}"/><text x="44" y="{y}" font-size="9" fill="{GREEN}">protected 31</text>'
    b += f'<rect x="140" y="{y-8}" width="8" height="8" rx="1.5" fill="{RED}"/><text x="153" y="{y}" font-size="9" fill="{RED}">no real dmarc 69</text>'
    b += f'<rect x="276" y="{y-8}" width="8" height="8" rx="1.5" fill="{AMBER}"/><text x="289" y="{y}" font-size="9" fill="{AMBER}">yours? run it</text>'
    b += f'<text x="31" y="252" font-size="10.5" fill="{TXT}">dmarc-translate tells you which cell you are</text>'
    b += f'<text x="31" y="268" font-size="8.5" class="dim">— in plain english, and when it is safe to block the fakes</text>'
    b += footer_caption(w, h, "~69% of domains have no real dmarc · the tooling gap is the blocker")
    svg("cells", w, h, b, css, "dmarc-translate: roughly 69 of 100 domains have no real DMARC protection")


# --------------------------------------------------------------------------- meters
def meters():
    w, h = 420, 310
    css = """
.prog{transform-box:fill-box;transform-origin:left;animation:prog 5s cubic-bezier(.3,.7,.2,1) infinite}
@keyframes prog{0%{transform:scaleX(0)}70%,100%{transform:scaleX(1)}}
.dot{animation:pulse 1.4s ease-in-out infinite}
@keyframes pulse{50%{opacity:.25}}
.full{transform-box:fill-box;transform-origin:left;animation:full 1.4s cubic-bezier(.2,.8,.2,1) both}
@keyframes full{from{transform:scaleX(0)}}
"""
    b = panel(w, h, AMBER, "04")
    b += card_head(w, "THE METERS", AMBER, "ONE SHIPS, ONE CLIMBS", "1 live · 1 wip",
                   "One is live · one is still climbing", f"the right bar climbs one phase at a time, {D['phase_total']} total")
    b += f'<text x="20" y="104" class="cap" fill="{AMBER}" font-size="9.5">TWO METERS · ONE LIVE, ONE CLIMBING</text>'
    # left meter
    b += f'<rect x="20" y="116" width="182" height="104" rx="8" fill="{AMBER}" fill-opacity=".06" stroke="{AMBER}" stroke-opacity=".55"/>'
    b += f'<text x="32" y="136" class="cap" fill="{AMBER}" font-size="9">GOTRANSIT</text>'
    b += f'<text x="190" y="136" text-anchor="end" font-size="8.5" font-weight="700" fill="{AMBER if D["site_live"] else RED}">{"live" if D["site_live"] else "down"}</text>'
    b += f'<text x="32" y="150" font-size="8" class="dim">react · express · supabase</text>'
    b += f'<text x="32" y="192" font-size="30" font-weight="800" fill="{AMBER}" filter="url(#glow)">{D["gotransit_commits"]}</text>'
    b += f'<text x="{36 + len(str(D["gotransit_commits"])) * 18.5:.0f}" y="192" font-size="9" class="dim">commits</text>'
    b += f'<rect x="32" y="204" width="158" height="4" rx="2" fill="#2a2418"/>'
    b += f'<rect class="full" x="32" y="204" width="158" height="4" rx="2" fill="{AMBER}"/>'
    # right meter
    b += f'<rect x="216" y="116" width="184" height="104" rx="8" fill="{CYAN}" fill-opacity=".07" stroke="{CYAN}" stroke-opacity=".6"/>'
    b += f'<text x="228" y="136" class="cap" fill="{CYAN}" font-size="9">DMARC-TRANSLATE</text>'
    b += f'<circle class="dot" cx="386" cy="132" r="3.5" fill="{CYAN}"/>'
    b += f'<text x="228" y="150" font-size="8" class="dim">python · parsedmarc · sqlite</text>'
    b += f'<text x="228" y="192" font-size="26" font-weight="800" fill="{CYAN}" filter="url(#glow)">phase {D["phase_current"]}</text>'
    b += f'<text x="352" y="192" font-size="9" class="dim">of {D["phase_total"]}</text>'
    n = max(D["phase_total"], 1)
    seg = 158 / n
    for k in range(n):
        x = 228 + k * seg
        if k < D["phase_current"] - 1 or D.get("phase_finished"):
            b += f'<rect x="{x:.1f}" y="204" width="{seg-3:.1f}" height="4" rx="2" fill="{CYAN}"/>'
        elif k == D["phase_current"] - 1:
            b += f'<rect x="{x:.1f}" y="204" width="{seg-3:.1f}" height="4" rx="2" fill="#132530"/>'
            b += f'<rect class="prog" x="{x:.1f}" y="204" width="{seg-3:.1f}" height="4" rx="2" fill="{CYAN}" fill-opacity=".6"/>'
        else:
            b += f'<rect x="{x:.1f}" y="204" width="{seg-3:.1f}" height="4" rx="2" fill="#132530"/>'
    b += f'<text x="20" y="246" font-size="10" fill="{TXT}">the left one is {"live" if D["site_live"] else "down right now"} at gotransitregina.ca</text>'
    b += f'<text x="20" y="262" font-size="10" fill="{CYAN}">{esc(("now building: " + D["phase_name"])[:46])}</text>'
    b += footer_caption(w, h, f"and when phase {D['phase_current']} lands, the bar starts climbing again")
    svg("meters", w, h, b, css, f"GoTransit has {D['gotransit_commits']} commits; dmarc-translate is in phase {D['phase_current']} of {D['phase_total']}")


# --------------------------------------------------------------------------- dots
def dots():
    w, h = 420, 310
    css = """
.scan{animation:scan 5s linear infinite}
@keyframes scan{from{transform:translateX(0)}to{transform:translateX(360px)}}
.red{transform-box:fill-box;transform-origin:center;animation:red 1.6s ease-in-out infinite}
@keyframes red{50%{transform:scale(1.35);opacity:.8}}
.ring{transform-box:fill-box;transform-origin:center;animation:ring 1.6s ease-out infinite}
@keyframes ring{from{transform:scale(1);opacity:.7}to{transform:scale(3);opacity:0}}
"""
    kinds = list(reversed(D["commits"]))  # oldest first, reads left-to-right
    real = bool(kinds)
    if not real:  # offline fallback: illustrative pattern
        kinds = ["ok"] * 200
        for i in (7, 23, 41, 58, 86, 112, 139, 150, 171, 196):
            kinds[i] = "fix"
        kinds[118] = "break"
    n = len(kinds)
    n_ok, n_fix, n_brk = kinds.count("ok"), kinds.count("fix"), kinds.count("break")
    hi = max((i for i, k in enumerate(kinds) if k == "break"), default=None)
    if hi is None:
        hi = max((i for i, k in enumerate(kinds) if k == "fix"), default=None)
    hi_col = RED if hi is not None and kinds[hi] == "break" else AMBER

    b = panel(w, h, RED, "05")
    kicker = f"{n} COMMITS, {n_brk} RED DOT{'' if n_brk == 1 else 'S'}"
    b += card_head(w, "THE HONEST PART", RED, kicker, "read this one",
                   f"My last {n} commits: {n_fix} fixes, {n_brk} undos",
                   "the scanner passes over the red ones every cycle", 13)
    b += f'<text x="30" y="104" class="cap" fill="{RED}" font-size="9.5">ONE DOT PER COMMIT · OLDEST FIRST, NEWEST LAST</text>'
    cols, sx, sy, x0, y0 = 25, 14.8, 12, 32, 118
    b += (f'<defs><linearGradient id="scan" x1="0" x2="1"><stop offset="0" stop-color="{RED}" stop-opacity="0"/>'
          f'<stop offset="1" stop-color="{RED}" stop-opacity=".22"/></linearGradient></defs>')
    b += f'<g class="scan"><rect x="{x0-30}" y="{y0-8}" width="30" height="{8*sy+4}" fill="url(#scan)"/><line x1="{x0}" y1="{y0-8}" x2="{x0}" y2="{y0+8*sy-4}" stroke="{RED}" stroke-opacity=".5"/></g>'
    style = {"ok": (GREEN, .75), "fix": (AMBER, 1), "break": (RED, 1)}
    for i in range(200):
        r, c = divmod(i, cols)
        x, y = x0 + c * sx, y0 + r * sy
        if i == hi:
            continue
        if i < n:
            col, op = style[kinds[i]]
            b += f'<circle cx="{x:.1f}" cy="{y}" r="{3 if kinds[i] == "break" else 2.6}" fill="{col}" opacity="{op}"/>'
        else:
            b += f'<circle cx="{x:.1f}" cy="{y}" r="2" fill="none" stroke="{FAINT}"/>'
    if hi is not None:
        r, c = divmod(hi, cols)
        x, y = x0 + c * sx, y0 + r * sy
        b += f'<circle class="ring" cx="{x:.1f}" cy="{y}" r="5" fill="none" stroke="{hi_col}"/>'
        b += f'<circle class="red" cx="{x:.1f}" cy="{y}" r="5.5" fill="{hi_col}" filter="url(#glow)"/>'
        b += f'<line x1="{x:.1f}" y1="{y+8}" x2="{x:.1f}" y2="{y0+8*sy+2}" stroke="{hi_col}" stroke-opacity=".5" stroke-dasharray="2 2"/>'
    ly, lx = 228, 34
    for count, label, col, bold in [(n_ok, "shipped", GREEN, False), (n_fix, "fixes", AMBER, False),
                                    (n_brk, "reverts · hotfixes", RED, True)]:
        t = f"{count} · {label}"
        wt = ' font-weight="700"' if bold else ""
        b += (f'<circle cx="{lx}" cy="{ly-3}" r="3.5" fill="{col}"/><text x="{lx+8}" y="{ly}" font-size="9" '
              f'fill="{RED if bold else TXT}"{wt}>{t}</text>')
        lx += len(t) * 5.6 + 30
    msg = ("every red dot is something i broke, then un-broke" if n_brk
           else "zero reverts so far · the scanner keeps looking")
    b += f'<text x="30" y="254" font-size="10" fill="#f87171">{msg}</text>'
    note = ("live from my commit messages · refreshed every 15 min" if real
            else "illustrative until the next refresh")
    b += f'<text x="30" y="269" font-size="8" class="dim">{note}</text>'
    b += footer_caption(w, h, "building one line at a time, breaking it twice as fast")
    svg("dots", w, h, b, css, f"My last {n} commits: {n_fix} fixes and {n_brk} reverts or hotfixes")

# --------------------------------------------------------------------------- footer
def strip(name, white, amber):
    w, h = 840, 46
    b = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="11" fill="{PANEL}" stroke="{LINE}"/>'
    b += (f'<text x="{w/2}" y="28" text-anchor="middle" font-size="11.5" font-weight="700" fill="{TXT}">'
          f'{esc(white)} <tspan fill="{DIM}">—</tspan> <tspan fill="{AMBER}">{esc(amber)}</tspan></text>')
    end = w / 2 + (len(white) + len(amber) + 3) * 7.0 / 2
    b += f'<rect class="blink" x="{end + 6:.0f}" y="18" width="6" height="12" fill="{AMBER}"/>'
    svg(name, w, h, b, title=f"{white} — {amber}")


def footer():
    strip("footer", "the degree takes four years", "the product gets better every time someone uses it")


def projects_title():
    strip("projects", "the projects", "four things i build, one still in the oven")


# --------------------------------------------------------------------------- project cards
def project(slug, n, accent, tag_kicker, badge, title, sub, hops, stats, caption, icon, ring, building=False):
    w, h = 420, 450
    css = """
.hop{animation:hop 3.4s cubic-bezier(.6,0,.4,1) infinite}
@keyframes hop{0%%{transform:translateX(0);opacity:0}6%%{opacity:1}94%%{opacity:1}100%%{transform:translateX(%dpx);opacity:0}}
.pulse{animation:pulse 1.4s ease-in-out infinite}
@keyframes pulse{50%%{opacity:.2}}
""" % (w - 44) + ORBIT_CSS
    b = panel(w, h, accent, f"{n:02d}")
    b += card_head(w, f"PROJECT {n:02d}", accent, tag_kicker, badge, title, sub)
    if building:
        bw = len(badge) * 8.5 * 0.6 + 16
        b += f'<circle class="pulse" cx="{w-18-bw-10:.1f}" cy="24" r="3.5" fill="{accent}"/>'
    b += orbit(210, 192, accent, ring, icon(210, 192), .72)
    b += '<g transform="translate(0,208)">'
    b += f'<text x="18" y="104" class="cap" fill="{accent}" font-size="9">HOW IT FLOWS</text>'
    nw, gap, x = (w - 36 - 3 * 8) / 4, 8, 18
    b += f'<circle class="hop" cx="22" cy="131" r="3" fill="{accent}" filter="url(#glow)"/>'
    for i, (lab, sub_) in enumerate(hops):
        boxed = 0 < i < 3
        if boxed:
            b += f'<rect x="{x:.1f}" y="114" width="{nw:.1f}" height="34" rx="5" fill="{PANEL}"/>'
            b += f'<rect x="{x:.1f}" y="114" width="{nw:.1f}" height="34" rx="5" fill="{accent}" fill-opacity=".06" stroke="{accent}" stroke-opacity=".6"/>'
            b += f'<text x="{x+nw/2:.1f}" y="128" text-anchor="middle" font-size="9" font-weight="700" fill="{TXT}">{esc(lab)}</text>'
            b += f'<text x="{x+nw/2:.1f}" y="141" text-anchor="middle" font-size="7.5" class="dim">{esc(sub_)}</text>'
        else:
            b += f'<rect x="{x:.1f}" y="119" width="{nw:.1f}" height="24" rx="4" fill="{PANEL}" stroke="{FAINT}" stroke-dasharray="2 2"/>'
            b += f'<text x="{x+nw/2:.1f}" y="134" text-anchor="middle" font-size="8.5" class="dim">{esc(lab)}</text>'
        if i < 3:
            b += f'<line x1="{x+nw:.1f}" y1="131" x2="{x+nw+gap:.1f}" y2="131" stroke="{accent}" stroke-opacity=".5"/>'
        x += nw + gap
    b += f'<rect x="18" y="162" width="{w-36}" height="50" rx="6" fill="#0d0f12" stroke="{LINE}"/>'
    for (lab, val, col), (x, anc) in zip(stats, [(32, "start"), (w / 2, "middle"), (w - 32, "end")]):
        b += f'<text x="{x}" y="180" text-anchor="{anc}" font-size="8.5" class="dim">{esc(lab)}</text>'
        b += f'<text x="{x}" y="200" text-anchor="{anc}" font-size="14" font-weight="800" fill="{col}">{esc(val)}</text>'
    b += '</g>'
    b += footer_caption(w, h, caption)
    svg(f"proj-{slug}", w, h, b, css, title)


def phase_ring(cur):
    names = ["DNS SETUP", "INGEST", "SCORING", "ENGLISH", "DASHBOARD"]
    out = []
    for i, (name, deg) in enumerate(zip(names, (-90, -18, 54, 126, 198))):
        col, cls = (GREEN, "") if i + 1 < cur else (CYAN, "now") if i + 1 == cur else (DIM, "")
        out.append((name, deg, col, cls))
    return out


def projects():
    R = D["repos"]

    def commits(name):
        c = R[name]["commits"]
        return "—" if c is None else f"{c:,}"

    def pushed(name):
        return "not pushed" if not R[name]["public"] else live.ago(R[name]["days"])

    up = D["site_live"]
    project("gotransit", 1, AMBER, "REAL-TIME TRANSIT · REGINA", "live" if up else "down",
            "GoTransit — live buses for Regina, SK", "react 19 · express 5 · supabase · google maps",
            [("a rider taps", ""), ("React 19", "map ui"), ("Express 5", "transit api"), ("the bus", "")],
            [("commits", commits("GoTransit"), AMBER), ("last push", pushed("GoTransit"), TXT),
             ("status", "live" if up else "down", GREEN if up else RED)],
            "live tracking every 1.5s · trip planning · admin analytics",
            lambda x, y: pixel_bus(x, y, 3.4),
            [("LIVE MAP", -90, CYAN, ""), ("TRIP PLAN", -18, GREEN, ""), ("ADMIN", 54, RED, ""),
             ("AUTH", 126, VIOLET, ""), ("GPS", 198, AMBER, "")])
    cur, tot = D["phase_current"], D["phase_total"]
    project("dmarc", 2, CYAN, "EMAIL SECURITY · 2-PERSON BUILD", f"phase {cur} / {tot}",
            "dmarc-translate — who's faking your email", "python · parsedmarc · sqlite · fastapi",
            [("dmarc xml", ""), ("parsedmarc", "xml → rows"), ("SQLite", "scored"), ("plain english", "")],
            [("commits", commits("dmarc-translate"), CYAN), ("last push", pushed("dmarc-translate"), TXT),
             ("phase", f"{cur} of {tot}", CYAN)],
            "turns raw dmarc reports into 'is it safe to block them yet?'",
            pixel_envelope, phase_ring(cur))
    project("ai-finance", 3, GREEN, "PERSONAL FINANCE · AI INSIGHTS", "built",
            "AI-Finance — your spending, explained", "next.js · prisma · supabase · gemini · clerk",
            [("a transaction", ""), ("Prisma", "postgres"), ("Gemini", "summarize"), ("an insight", "")],
            [("commits", commits("AI-Finance"), GREEN), ("last push", pushed("AI-Finance"), TXT),
             ("ai", "gemini", GREEN)],
            "real-time spending dashboards with ai-written summaries",
            pixel_chart,
            [("AI INSIGHTS", -90, GREEN, ""), ("ANALYTICS", -18, CYAN, ""), ("SUPABASE", 54, VIOLET, ""),
             ("AUTH", 126, AMBER, ""), ("TRANSACTIONS", 198, TXT, "")])
    rv = R["AI-generate-code-reviewer"]
    project("code-reviewer", 4, VIOLET, "DEVTOOLS · AI CODE REVIEW", "building",
            "AI code reviewer — building now",
            f"{rv['commits']} commits pushed so far" if rv["public"] else "not pushed yet · this card goes live when it is",
            [("your diff", ""), ("AI model", "reads it"), ("review", "flags issues"), ("feedback", "")],
            [("commits pushed", commits("AI-generate-code-reviewer") if rv["public"] else "0", VIOLET),
             ("repo", "public" if rv["public"] else "local only", TXT), ("status", "building", VIOLET)],
            "ai-generate-code-reviewer · updates itself once it's on github",
            pixel_code,
            [("READ DIFF", -90, VIOLET, ""), ("FIND BUGS", -18, RED, "now"), ("EXPLAIN", 54, CYAN, ""),
             ("SUGGEST FIX", 126, GREEN, ""), ("SECURITY", 198, AMBER, "")], building=True)


for f in (header, stack, loop, cells, meters, dots, projects_title, projects, footer):
    f()
print("built:", sorted(p.name for p in OUT.iterdir()))
