"""Builds assets/hero.svg: the name as a heat signature in a thermal drone feed.

    python scripts/generate.py

The feed boots in static, targeting brackets close in on the name and lock,
then the camera drifts while the HUD keeps running. Every animation's
un-animated state is the final frame, so reduced-motion viewers see the
locked-on feed.
"""

import random
from pathlib import Path

from theme import BG, BORDER, GOLD, GOLD_DIM, esc, svg

ASSETS = Path(__file__).resolve().parent.parent / "assets"

NAME = "Soumil Bhandari"
COORDS = "40.4237N  86.9212W"
HEADING = 274
# Heat signatures the system checks and rejects before it finds the name:
# (x, y, match score, which side the verdict prints on)
DECOYS = [(104, 118, 12, "r"), (1090, 204, 31, "l"), (326, 250, 8, "r"), (1074, 96, 47, "l")]
SCAN_START, SCAN_STEP, SCAN_HOLD = 0.8, 0.62, 0.7

HOT = "#fff3dc"
WARM = "#d98b32"
EMBER = "#6b3410"


def grid_text(s, x, y, cls, adv=8.4):
    """Monospace text with every character pinned to a fixed grid, so the HUD
    lines up the same whatever mono font the viewer has."""
    return "".join(f'<text class="{cls}" x="{x + k * adv:.1f}" y="{y}">{esc(ch)}</text>'
                   for k, ch in enumerate(s) if ch != " ")


def grain(rng, size=160, n=260):
    dots = "".join(f'<rect x="{rng.uniform(0, size):.1f}" y="{rng.uniform(0, size):.1f}" '
                   f'width="{rng.choice((1, 1, 2))}" height="1" opacity="{rng.uniform(0.15, 0.6):.2f}"/>'
                   for _ in range(n))
    return f'<pattern id="grain" width="{size}" height="{size}" patternUnits="userSpaceOnUse"><g fill="#fff">{dots}</g></pattern>'


def hero():
    W, H = 1200, 300
    cx, base = W / 2, 182
    box = (180, 94, 1020, 210)
    lock = SCAN_START + SCAN_STEP * len(DECOYS) + 0.6
    rng = random.Random(4)
    adv = 8.4

    css = f"""
.hud {{ font-size: 14px; fill: {GOLD}; }}
.dim {{ font-size: 14px; fill: {GOLD_DIM}; }}
.tiny {{ font-size: 12px; fill: {GOLD_DIM}; text-anchor: middle; }}
.line {{ stroke: {GOLD}; stroke-width: 1.5; fill: none; }}
.thin {{ stroke: {GOLD_DIM}; stroke-width: 1; fill: none; }}
.nm {{ font-size: 92px; font-weight: 800; letter-spacing: -1px; text-anchor: middle; }}
.ember {{ fill: {EMBER}; filter: url(#b18); animation: breathe 3.2s ease-in-out {lock:.1f}s infinite; }}
.warm {{ fill: {WARM}; opacity: 0.85; filter: url(#b6); }}
.core {{ fill: {HOT}; filter: url(#b05); }}
.hud-in {{ animation: fade 0.5s ease-out 0.2s both; }}
.heat {{ animation: bloom 1.4s cubic-bezier(.2, .7, .2, 1) 0.5s both; transform-origin: {cx}px {base - 30}px; }}
.static {{ opacity: 0.09; animation: settle 1.4s ease-out both; }}
.noise {{ animation: jitter 0.4s steps(1) infinite; }}
.world {{ animation: drift 11s ease-in-out {lock:.1f}s infinite; }}
.brk {{ animation: close 0.8s cubic-bezier(.5, 0, .2, 1) {lock - 0.8:.2f}s both, track 2.6s ease-in-out {lock:.1f}s infinite;
  transform-origin: {cx}px {(box[1] + box[3]) / 2}px; }}
.acq {{ opacity: 0; animation: acq {lock:.2f}s steps(1) both; }}
.trk {{ animation: arm {lock:.2f}s linear both; }}
.rec {{ fill: #e5483b; animation: blink 1.2s steps(1) infinite; }}
.tape {{ animation: pan 9s ease-in-out infinite alternate; }}
.ones {{ animation: roll10 10s steps(10) infinite; }}
.tens {{ animation: roll6 60s steps(6) infinite; }}
.tear {{ opacity: 0; animation: tear 6.5s linear {lock + 1.5:.1f}s infinite; }}
@keyframes fade {{ from {{ opacity: 0; }} }}
@keyframes arm {{ 0%, 99% {{ opacity: 0; }} }}
@keyframes bloom {{ from {{ opacity: 0; transform: scale(1.06); }} 40% {{ opacity: 0.6; }} }}
@keyframes settle {{ from {{ opacity: 0.7; }} 30% {{ opacity: 0.5; }} }}
@keyframes jitter {{ 0% {{ transform: translate(0, 0); }} 25% {{ transform: translate(-53px, 17px); }}
  50% {{ transform: translate(-21px, -71px); }} 75% {{ transform: translate(-88px, -34px); }} }}
@keyframes breathe {{ 50% {{ opacity: 0.7; }} }}
@keyframes drift {{ 25% {{ transform: translate(6px, -3px); }} 50% {{ transform: translate(-4px, 3px); }}
  75% {{ transform: translate(3px, 4px); }} }}
@keyframes close {{ from {{ opacity: 0; transform: scale(1.35); }} 15% {{ opacity: 1; }} 70% {{ transform: scale(0.97); }} }}
@keyframes track {{ 30% {{ transform: translate(2px, -1px); }} 60% {{ transform: translate(-2px, 1px); }} }}
@keyframes blink {{ 50% {{ opacity: 0.15; }} }}
@keyframes pan {{ from {{ transform: translateX(-40px); }} to {{ transform: translateX(40px); }} }}
@keyframes roll10 {{ to {{ transform: translateY(-180px); }} }}
@keyframes roll6 {{ to {{ transform: translateY(-108px); }} }}
@keyframes tear {{ 0%, 93% {{ opacity: 0; transform: translateX(0); }} 94% {{ opacity: 1; transform: translateX(16px); }}
  96% {{ opacity: 1; transform: translateX(-11px); }} 98% {{ opacity: 1; transform: translateX(5px); }} 99%, 100% {{ opacity: 0; }} }}
"""

    # SCANNING blinks from the end of the boot until the lock.
    on = [100 * (0.6 + 0.5 * k) / lock for k in range(int((lock - 0.6) / 0.5))]
    css += ("@keyframes acq { 0% { opacity: 0; } "
            + " ".join(f"{a:.1f}% {{ opacity: {1 if k % 2 == 0 else 0}; }}" for k, a in enumerate(on))
            + " 100% { opacity: 0; } }\n")

    # Each decoy gets boxed, scored, and dropped, one after another.
    decoys = []
    for k, (dx_, dy_, score, side) in enumerate(DECOYS):
        t = SCAN_START + k * SCAN_STEP
        a, b, v = (100 * x / lock for x in (t, t + SCAN_HOLD, t + 0.22))
        css += (f"@keyframes dec{k} {{ 0%, {a:.2f}% {{ opacity: 0; }} {a + 0.1:.2f}%, {b:.2f}% {{ opacity: 1; }} "
                f"{b + 0.1:.2f}%, 100% {{ opacity: 0; }} }}\n"
                f"@keyframes ver{k} {{ 0%, {v:.2f}% {{ opacity: 0; }} {v + 0.1:.2f}%, 100% {{ opacity: 1; }} }}\n"
                f".dec{k} {{ opacity: 0; animation: dec{k} {lock:.2f}s linear both; }}\n"
                f".ver{k} {{ animation: ver{k} {lock:.2f}s linear both; }}\n"
                f".snap{k} {{ animation: snap 0.25s ease-out {t:.2f}s both; transform-origin: {dx_}px {dy_}px; }}\n")
        w, h, arm_ = 22, 26, 8
        corners_ = "".join(f'<path class="line" d="M{x} {y + sy * arm_} V{y} H{x + sx * arm_}"/>'
                           for x, y, sx, sy in ((dx_ - w, dy_ - h, 1, 1), (dx_ + w, dy_ - h, -1, 1),
                                                (dx_ - w, dy_ + h, 1, -1), (dx_ + w, dy_ + h, -1, -1)))
        verdict = f"NO MATCH {score}%"
        vx = dx_ + w + 10 if side == "r" else dx_ - w - 10 - len(verdict) * 7.2
        decoys.append(f'<g class="dec{k}"><g class="snap{k}">{corners_}</g>'
                      f'<g class="ver{k}">{grid_text(verdict, vx, dy_ + 4, "mono tag", 7.2)}</g></g>')
    css += f"""
.tag {{ font-size: 12px; fill: {GOLD}; }}
@keyframes snap {{ from {{ transform: scale(1.8); }} }}
"""
    bodies = "".join(
        f'<ellipse cx="{x}" cy="{y}" rx="11" ry="16" fill="{WARM}" opacity="0.55" filter="url(#b6)"/>'
        f'<ellipse cx="{x}" cy="{y - 2}" rx="4" ry="8" fill="{HOT}" opacity="0.8" filter="url(#b2)"/>'
        for x, y, _, _ in DECOYS)

    defs = f"""<defs>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="16"/></clipPath>
<clipPath id="band"><rect x="0" y="{base - 40}" width="{W}" height="13"/></clipPath>
<linearGradient id="tapefade"><stop offset="0" stop-color="#000"/><stop offset="0.25" stop-color="#fff"/><stop offset="0.75" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
<mask id="tapewin"><rect x="430" y="236" width="340" height="50" fill="url(#tapefade)"/></mask>
<clipPath id="digits"><rect x="0" y="0" width="{W}" height="18"/></clipPath>
<filter id="b18" x="-20%" y="-80%" width="140%" height="260%"><feGaussianBlur stdDeviation="18"/></filter>
<filter id="b6" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="b05"><feGaussianBlur stdDeviation="0.6"/></filter>
<filter id="b2" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="b40" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="40"/></filter>
<pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity="0.45"/></pattern>
{grain(rng)}
<radialGradient id="vig" cx="50%" cy="50%" r="70%">
  <stop offset="55%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity="0.75"/></radialGradient>
</defs>"""

    # The world: everything the camera sees, drifting together.
    blobs = "".join(f'<ellipse cx="{rng.uniform(0, W):.0f}" cy="{rng.uniform(0, H):.0f}" '
                    f'rx="{rng.uniform(60, 160):.0f}" ry="{rng.uniform(30, 80):.0f}" fill="#2a1a0e" '
                    f'opacity="{rng.uniform(0.3, 0.7):.2f}" filter="url(#b40)"/>' for _ in range(7))
    name = esc(NAME)
    x0, y0, x1, y1 = box
    arm = 26
    brackets = "".join(
        f'<path class="line" d="M{x} {y + dy * arm} V{y} H{x + dx * arm}"/>'
        for x, y, dx, dy in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)))
    world = f"""<g class="world">
{blobs}
{bodies}
<g class="heat">
<text class="sans nm ember" x="{cx}" y="{base}">{name}</text>
<text class="sans nm warm" x="{cx}" y="{base}">{name}</text>
<text class="sans nm core" x="{cx}" y="{base}">{name}</text>
</g>
<g clip-path="url(#band)"><text class="sans nm core tear" x="{cx}" y="{base}">{name}</text></g>
<g class="brk">{brackets}
<g class="trk">{grid_text("MATCH 99.7% · TGT 01", x0, y0 - 12, "mono hud")}</g>
</g>
<g class="acq">{grid_text("SCANNING", x0, y0 - 12, "mono hud")}</g>
{"".join(decoys)}
</g>"""

    # HUD: fixed to the screen.
    mid = (y0 + y1) / 2
    reticle = (f'<path class="thin" d="M24 {mid} H{x0 - 40} M{x1 + 40} {mid} H{W - 24}"/>'
               f'<path class="thin" d="M{x0 - 40} {mid - 6} V{mid + 6} M{x1 + 40} {mid - 6} V{mid + 6}"/>')
    corners = "".join(f'<path class="thin" d="M{x} {y + dy * 18} V{y} H{x + dx * 18}"/>'
                      for x, y, dx, dy in ((14, 14, 1, 1), (W - 14, 14, -1, 1), (14, H - 14, 1, -1), (W - 14, H - 14, -1, -1)))

    # Running timecode: the last two digits roll on strips behind a fixed window.
    tc_x, tc_y = 64, 40
    stamp = "T+00:"
    dx = tc_x + len(stamp) * adv
    tens = "".join(f'<text class="mono hud" x="{dx:.1f}" y="{tc_y + 18 * k}">{k}</text>' for k in range(6))
    ones = "".join(f'<text class="mono hud" x="{dx + adv:.1f}" y="{tc_y + 18 * k}">{k}</text>' for k in range(10))
    clock = (grid_text(stamp, tc_x, tc_y, "mono hud") +
             f'<g transform="translate(0 {tc_y - 14})"><g clip-path="url(#digits)"><g transform="translate(0 {14 - tc_y})">'
             f'<g class="tens">{tens}</g><g class="ones">{ones}</g></g></g></g>')

    ticks = []
    for h in range(HEADING - 26, HEADING + 27):
        x = cx + (h - HEADING) * 10
        tall = h % 5 == 0
        ticks.append(f'<line class="thin" x1="{x}" y1="{262 - (10 if tall else 5)}" x2="{x}" y2="262"/>')
        if h % 10 == 0:
            ticks.append(f'<text class="mono tiny" x="{x}" y="281">{h % 360:03d}</text>')
    tape = (f'<g mask="url(#tapewin)"><g class="tape">{"".join(ticks)}</g></g>'
            f'<path d="M{cx - 6} 240 L{cx + 6} 240 L{cx} 248 Z" fill="{GOLD}"/>')

    hud = f"""<g class="hud-in">
{corners}{reticle}
<circle class="rec" cx="44" cy="35" r="5"/>
{clock}
{grid_text("FLIR · WHT HOT", cx - 7 * adv, 40, "mono dim")}
{grid_text("ZOOM 4.0x", W - 44 - 9 * adv, 40, "mono hud")}
{grid_text(COORDS, 44, 272, "mono hud")}
{grid_text("ALT 0412 FT", W - 44 - 11 * adv, 272, "mono hud")}
{tape}
</g>"""

    body = f"""{defs}
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="{BG}"/>
{world}
<g class="static"><rect class="noise" x="0" y="0" width="{W + 160}" height="{H + 160}" fill="url(#grain)"/></g>
<rect width="{W}" height="{H}" fill="url(#scan)"/>
<rect width="{W}" height="{H}" fill="url(#vig)"/>
{hud}
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{BORDER}"/>"""
    return svg(W, H, body, css, f"{NAME}, as a heat signature on a thermal drone feed")


def main():
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "hero.svg").write_text(hero(), encoding="utf-8")
    print("wrote assets/hero.svg")


if __name__ == "__main__":
    main()
