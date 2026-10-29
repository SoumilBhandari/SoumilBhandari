"""Builds the static SVGs in assets/: hero, numbers, terminal, findings, timeline.

    python scripts/generate.py

Edit the data below and re-run; stats.py handles the live GitHub cards.
"""

import math
import random
from pathlib import Path

from theme import (BG, BORDER, GOLD, GOLD_DIM, MUTED, TEXT, card_bg,
                   esc, svg)

ASSETS = Path(__file__).resolve().parent.parent / "assets"

NAME = "Soumil Bhandari"
SUBTITLE = ("Computer Engineering @ Purdue", "AI Researcher @ Perforated AI")
PHRASES = [
    "training diffusion language models from scratch",
    "catching backdoors hidden in neural networks",
    "routing telemetry boards for Purdue Formula SAE",
    "building EEG caps for spaceflight",
    "measuring, honestly, whether it actually works",
]

NUMBERS = [
    ("3", "provisional US patents", "filed Dec 2025"),
    ("1st", "of 280+ teams", "HopHacks 2026"),
    ("Top 4%", "YC AI Startup School", "2,500 of 35,000+"),
    ("98%", "MEP classification", "Harvard Medical School"),
    ("$50K+", "personally realized", "from my deal engine"),
]

BUILDS = [
    ("nanoDLM", "masked-diffusion LM from scratch in ~1.1k lines of PyTorch", "ml"),
    ("deadbolt", "6 backdoor detectors vs a 102-model zoo, run blind", "security"),
    ("Bastion", "spend caps, rate limits + audit log for MCP tool calls", "agents"),
    ("SecuriVax", "vaccine cold-chain engine \u00b7 1st of 280+ @ HopHacks", "health"),
    ("Neurafy", "Alzheimer\u2019s progression model, AUC 0.95\u20130.97", "startup"),
    ("SpaceCap", "EEG + PPG cap that flags hypoxia in spaceflight", "space"),
    ("ATLAS", "closed-loop TMS thresholding @ Harvard Medical School", "neuro"),
    ("You2", "a voice assistant that remembers, fully on-device", "hardware"),
    ("Flipper", "real-estate deal engine \u00b7 $50K+ personally realized", "money"),
]

FINDINGS = [
    # (big number, what it measures, headline, plain explanation, source)
    ("0.254", "0.5 = guessing", "Chatbots are most confident when they\u2019re making things up.",
     "So confidence is worse than guessing at spotting lies. Reading its internals: 0.988.",
     "halluscope \u00b7 AUROC on HaluEval, 4,000 answers"),
    ("0 / 6", "detectors that worked", "None of the 6 published backdoor detectors I tested caught WaNet.",
     "A hidden-trigger attack that made every one of them do worse than a coin flip.",
     "deadbolt \u00b7 102 models, 540 blind scans"),
    ("2\u00d7", "too high, silently", "The model I forked was quietly training toward the wrong target.",
     "Its loss still went down, so nobody noticed. One wrong line made it aim 2\u00d7 too high.",
     "nanoDLM \u00b7 divided by mask.sum() instead of B\u00b7T"),
    ("1.00", "retrieval precision", "Memory that consolidates gets sharper with age, not noisier.",
     "Over a simulated year, You2 went from 0.50 to 1.00 and stale facts never resurfaced.",
     "you2 \u00b7 nightly summarize, version, and decay"),
]

TIMELINE = [
    ("2026 \u2013 now", "Perforated AI", "AI Researcher",
     "Researching dendritic model compression", True),
    ("2026 \u2013 now", "Purdue Formula SAE", "Electronics, 2nd in the world",
     "Routed the telemetry receiver PCB and wrote its firmware; brake-bias motor selection", True),
    ("2026", "Harvard Medical School", "Research Intern",
     "Automated TMS motor thresholding; real-time MEP classification at 98% accuracy", False),
    ("2025 \u2013 26", "Neurafy", "Founder",
     "Alzheimer\u2019s progression model, AUC 0.95\u20130.97 \u00b7 3 patents \u00b7 clinical pilot \u00b7 failed", False),
    ("2025 \u2013 26", "IIT Roorkee", "Research Intern",
     "Classifier gating a clinical RAG system at 92%+; LoRA fine-tuned LLaMA-2 and Flan-T5", False),
    ("2025", "McKesson", "Software Engineering Intern",
     "1M+ clinical records through GPT extraction for iKnowMed; 35% faster analytics", False),
    ("\u2192 2028", "Purdue University", "B.S. Computer Engineering",
     "Neural Space Cap (Purdue VIP): EEG + PPG monitoring for commercial spaceflight", False),
]


def dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def polyline(points):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    return d, sum(dist(a, b) for a, b in zip(points, points[1:]))


def dendrite_tree(soma, rng, squash=0.7):
    """Branches fanning left from the soma, three levels deep. Returns
    (edges as (depth, a, b), paths from each tip back to the soma)."""
    edges, paths = [], []

    def grow(node, angle, length, depth, trail):
        rad = math.radians(angle)
        tip = (node[0] + length * math.cos(rad), node[1] + squash * length * math.sin(rad))
        edges.append((depth, node, tip))
        if depth == 2:
            paths.append([tip] + trail[::-1])
            return
        for spread in (-1, 1):
            grow(tip, angle + spread * rng.uniform(16, 26), length * rng.uniform(0.68, 0.82),
                 depth + 1, trail + [tip])

    for angle in (156, 180, 204):
        grow(soma, angle + rng.uniform(-6, 6), rng.uniform(40, 50), 0, [soma])
    return edges, paths


def neurons(delay=0.0):
    """Three dendritic neurons in a chain. A spike runs in along each cell's
    dendrites, the soma lights up, and it fires down the myelinated axon into
    the next cell's dendrites."""
    rng = random.Random(7)
    somas = [(175, 392), (525, 397), (875, 389)]
    step, cycle = 2.3, 8.6
    width = {0: 2.6, 1: 1.8, 2: 1.2}
    css = [f"""
.den {{ fill: none; stroke: #4d4537; stroke-linecap: round; stroke-linejoin: round; }}
.axon {{ fill: none; stroke: #4d4537; stroke-width: 2; stroke-linejoin: round; }}
.myelin {{ fill: none; stroke: #2e2a21; stroke-width: 8; stroke-linecap: round; stroke-dasharray: 38 9; }}
.pulse {{ fill: none; stroke: {GOLD}; stroke-linecap: round; stroke-linejoin: round; opacity: 0; filter: url(#glow); }}
.soma {{ fill: #2a251c; stroke: {GOLD_DIM}; stroke-width: 2; }}
.fire {{ fill: {GOLD}; opacity: 0; filter: url(#glow); }}
.bulb {{ fill: {GOLD_DIM}; }}
"""]
    base = ['<defs><filter id="glow" x="-50%" y="-50%" width="200%" height="200%">'
            '<feGaussianBlur stdDeviation="2.5" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>']
    top, n = [], 0

    def pulse(points, start, dur, seg, w):
        nonlocal n
        d, L = polyline(points)
        a, b = 100 * start / cycle, 100 * (start + dur) / cycle
        css.append(f"@keyframes p{n} {{ 0%, {a:.2f}% {{ stroke-dashoffset: {seg}; opacity: 1; }} "
                   f"{b:.2f}% {{ stroke-dashoffset: {-L:.0f}; opacity: 1; }} "
                   f"{b + 0.01:.2f}%, 100% {{ stroke-dashoffset: {-L:.0f}; opacity: 0; }} }}\n"
                   f".p{n} {{ stroke-width: {w}; stroke-dasharray: {seg} {L + seg:.0f}; "
                   f"animation: p{n} {cycle}s linear {delay:.2f}s infinite; }}\n")
        top.append(f'<path class="pulse p{n}" d="{d}"/>')
        n += 1

    for k, (sx, sy) in enumerate(somas):
        t = k * step
        edges, paths = dendrite_tree((sx, sy), rng)
        for depth, a, b in edges:
            base.append(f'<line class="den" x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" '
                        f'y2="{b[1]:.1f}" stroke-width="{width[depth]}"/>')
        for m, path in enumerate(paths):
            pulse(path, t + 0.04 * m, 0.75, 16, 2)
        end = (sx + 205, sy + rng.uniform(-4, 4))
        axon = [(sx, sy), (sx + 60, sy - 5), (sx + 120, sy + 5), (sx + 175, sy - 3), end]
        d, _ = polyline(axon)
        base.append(f'<path class="axon" d="{d}"/><path class="myelin" d="{d}" stroke-dashoffset="-20"/>')
        pulse(axon, t + 1.0, 0.85, 46, 3)
        for dy in (-22, 0, 22):
            tip = (end[0] + 34, end[1] + dy)
            base.append(f'<line class="den" x1="{end[0]:.1f}" y1="{end[1]:.1f}" x2="{tip[0]:.1f}" '
                        f'y2="{tip[1]:.1f}" stroke-width="1.4"/><circle class="bulb" cx="{tip[0]:.1f}" cy="{tip[1]:.1f}" r="3.5"/>')
            pulse([end, tip], t + 1.85, 0.3, 14, 2)
        f0, f1, f2 = (100 * (t + v) / cycle for v in (0.75, 0.95, 1.6))
        css.append(f"@keyframes fire{k} {{ 0%, {f0:.2f}% {{ opacity: 0; }} {f1:.2f}% {{ opacity: 0.95; }} "
                   f"{f2:.2f}%, 100% {{ opacity: 0; }} }}\n"
                   f".fire{k} {{ animation: fire{k} {cycle}s ease-out {delay:.2f}s infinite; }}\n")
        top.append(f'<circle class="soma" cx="{sx}" cy="{sy}" r="13"/>'
                   f'<circle class="fire fire{k}" cx="{sx}" cy="{sy}" r="9"/>')
    return "".join(css), "\n".join(base + top)


def backdrop(W, H):
    return f"""<defs>
<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
  <circle cx="2" cy="2" r="1" fill="{BORDER}"/></pattern>
<radialGradient id="wash" cx="50%" cy="0%" r="75%">
  <stop offset="0%" stop-color="{GOLD}" stop-opacity="0.16"/>
  <stop offset="100%" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#dots)" opacity="0.7"/>
<rect width="{W}" height="{H}" fill="url(#wash)"/>
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{BORDER}"/>"""


def hero():
    """The name decodes from [MASK] tokens over 16 steps, the way a masked-diffusion
    LM samples, then a terminal line cycles through what I work on. Three dendritic
    neurons pass a spike along the bottom."""
    W, H = 1200, 480
    T0, DT, STEPS = 0.5, 0.16, 16
    t = lambda s: 0 if s == 0 else T0 + s * DT
    done = t(STEPS)

    cell, size, base_y = 46, 64, 200
    x0 = (W - len(NAME) * cell) / 2
    letters = [i for i, ch in enumerate(NAME) if ch != " "]
    order = letters[:]
    random.Random(16).shuffle(order)
    step_of = {idx: 1 + round(k * (STEPS - 1) / (len(order) - 1)) for k, idx in enumerate(order)}

    css = f"""
.prompt {{ font-size: 15px; fill: {MUTED}; }}
.step {{ font-size: 15px; fill: {GOLD}; }}
.mask {{ fill: {GOLD}; fill-opacity: 0.07; stroke: {GOLD_DIM}; stroke-width: 1.5; opacity: 0; }}
.ch {{ font-size: {size}px; font-weight: 600; fill: {TEXT}; text-anchor: middle; }}
.sub {{ font-size: 24px; fill: {TEXT}; text-anchor: middle; animation: up 0.8s ease-out {done + 0.15:.2f}s both; }}
.foot {{ font-size: 14px; fill: {GOLD_DIM}; animation: fade 1s ease-out {done + 0.4:.2f}s both; }}
.typed {{ font-size: 19px; fill: {TEXT}; }}
.caret {{ fill: {GOLD}; opacity: 0; }}
.chev {{ font-size: 19px; fill: {GOLD}; animation: fade 0.6s ease-out {done + 0.4:.2f}s both; }}
@keyframes show {{ from, to {{ opacity: 1; }} }}
@keyframes hide {{ from, to {{ opacity: 0; }} }}
@keyframes commit {{ 0% {{ opacity: 0; fill: {GOLD}; }} 25% {{ opacity: 1; fill: {GOLD}; }}
  100% {{ opacity: 1; fill: {TEXT}; }} }}
@keyframes up {{ from {{ opacity: 0; transform: translateY(10px); }} }}
@keyframes fade {{ from {{ opacity: 0; }} }}
"""
    body = [backdrop(W, H)]
    body.append(f'<text class="mono prompt" x="48" y="56">$ python sample.py --prompt "[MASK] × 14" --steps 16</text>')

    # Step counter: each value is visible only during its own step.
    for s in range(STEPS + 1):
        label = f"step {s:02d}/{STEPS}"
        if s < STEPS:
            anim = f"animation: show {t(s + 1) - t(s):.2f}s linear {t(s):.2f}s"
            body.append(f'<text class="mono step" x="{W - 48}" y="56" text-anchor="end" opacity="0" style="{anim}">{label}</text>')
        else:
            anim = f"animation: hide {done:.2f}s linear 0s"
            body.append(f'<text class="mono step" x="{W - 48}" y="56" text-anchor="end" style="{anim}">{label} ✓</text>')

    for i, ch in enumerate(NAME):
        if ch == " ":
            continue
        cx = x0 + cell / 2 + i * cell
        reveal = t(step_of[i])
        body.append(f'<rect class="mask" x="{cx - 18:.1f}" y="{base_y - 54}" width="36" height="66" rx="7" '
                    f'style="animation: show {reveal:.2f}s linear 0s"/>')
        body.append(f'<text class="mono ch" x="{cx:.1f}" y="{base_y}" '
                    f'style="animation: commit 0.7s ease-out {reveal:.2f}s both">{esc(ch)}</text>')

    a, b = SUBTITLE
    body.append(f'<text class="sans sub" x="{W / 2}" y="264">{esc(a)}'
                f'<tspan fill="{GOLD}" dx="14">·</tspan><tspan dx="14">{esc(b)}</tspan></text>')

    # Typing line. textLength pins every glyph to a fixed advance, so the clip
    # and caret line up on any monospace font.
    adv, ty = 11.4, 322
    slot, start = 4.6, done + 0.6
    cycle = slot * len(PHRASES)
    longest = max(len(p) for p in PHRASES)
    xs = (W - (longest + 2) * adv) / 2
    tx = xs + 2 * adv
    body.append(f'<text class="mono chev" x="{xs:.1f}" y="{ty}">›</text>')
    defs, kf = [], []
    for i, p in enumerate(PHRASES):
        n, w = len(p), len(p) * adv
        typing, erase = n * 0.045, 0.5
        hold = slot - typing - erase - 0.3
        p1, p2, p3 = (100 * v / cycle for v in (typing, typing + hold, typing + hold + erase))
        kf.append(f"""
@keyframes type{i} {{ 0% {{ transform: scaleX(0); animation-timing-function: steps({n}, end); }}
  {p1:.2f}% {{ transform: scaleX(1); animation-timing-function: linear; }}
  {p2:.2f}% {{ transform: scaleX(1); animation-timing-function: steps({n}, end); }}
  {p3:.2f}%, 100% {{ transform: scaleX(0); }} }}
@keyframes caret{i} {{ 0% {{ opacity: 0; transform: translateX(0); animation-timing-function: step-end; }}
  0.05% {{ opacity: 1; transform: translateX(0); animation-timing-function: steps({n}, end); }}
  {p1:.2f}% {{ opacity: 1; transform: translateX({w:.1f}px); animation-timing-function: linear; }}
  {p2:.2f}% {{ opacity: 1; transform: translateX({w:.1f}px); animation-timing-function: steps({n}, end); }}
  {p3:.2f}% {{ opacity: 1; transform: translateX(0); }}
  {p3 + 0.01:.2f}%, 100% {{ opacity: 0; transform: translateX(0); }} }}
.r{i} {{ transform-origin: {tx:.1f}px 0; {"" if i == 0 else "transform: scaleX(0);"}
  animation: type{i} {cycle:.1f}s {start + i * slot:.2f}s infinite both; }}
.k{i} {{ animation: caret{i} {cycle:.1f}s {start + i * slot:.2f}s infinite both; }}
""")
        defs.append(f'<clipPath id="c{i}"><rect class="r{i}" x="{tx:.1f}" y="{ty - 20}" width="{w + 1:.1f}" height="28"/></clipPath>')
        body.append(f'<text class="mono typed" x="{tx:.1f}" y="{ty}" textLength="{w:.1f}" lengthAdjust="spacing" '
                    f'clip-path="url(#c{i})">{esc(p)}</text>')
        body.append(f'<rect class="caret k{i}" x="{tx + 1:.1f}" y="{ty - 17}" width="10" height="21" rx="1.5"/>')
    css += "".join(kf)
    body.insert(1, f"<defs>{''.join(defs)}</defs>")

    ncss, nbody = neurons(delay=done)
    css += ncss
    body.append(nbody)
    body.append(f'<text class="mono foot" x="48" y="462">name \u00b7 masked diffusion, 16 denoising steps</text>')
    body.append(f'<text class="mono foot" x="{W - 48}" y="462" text-anchor="end">neurons \u00b7 dendrites in, spike out</text>')
    return svg(W, H, "\n".join(body), css, f"{NAME}: {SUBTITLE[0]}, {SUBTITLE[1]}")


def numbers():
    W, H = 1200, 170
    col = W / len(NUMBERS)
    css = f"""
.big {{ font-size: 44px; font-weight: 700; fill: {GOLD}; text-anchor: middle; }}
.lbl {{ font-size: 17px; fill: {MUTED}; text-anchor: middle; }}
.lbl.hi {{ fill: {TEXT}; }}
.n {{ animation: up 0.7s ease-out both; }}
@keyframes up {{ from {{ opacity: 0; transform: translateY(10px); }} }}
"""
    body = [card_bg(W, H, 18)]
    for i, (big, l1, l2) in enumerate(NUMBERS):
        cx = col * i + col / 2
        if i:
            body.append(f'<line x1="{col * i:.0f}" y1="32" x2="{col * i:.0f}" y2="{H - 32}" stroke="{BORDER}"/>')
        body.append(f'<g class="n" style="animation-delay: {0.15 + i * 0.12:.2f}s">'
                    f'<text class="sans big" x="{cx:.0f}" y="80">{esc(big)}</text>'
                    f'<text class="sans lbl hi" x="{cx:.0f}" y="114">{esc(l1)}</text>'
                    f'<text class="sans lbl" x="{cx:.0f}" y="137">{esc(l2)}</text></g>')
    alt = "; ".join(f"{b} {l1} {l2}" for b, l1, l2 in NUMBERS)
    return svg(W, H, "\n".join(body), css, alt)


def terminal():
    """`ls ~/builds` in a terminal window: the command types out, then the listing prints."""
    W, adv, pitch = 1200, 11.4, 36
    top = 104
    H = top + pitch * (len(BUILDS) + 1) + 34
    cmd = "ls ~/builds --sort=impact"
    cx = 40 + 2 * adv
    type_t, t0 = len(cmd) * 0.05, 0.5
    listed = t0 + type_t + 0.25
    css = f"""
.bar {{ font-size: 14px; fill: {MUTED}; text-anchor: middle; }}
.t {{ font-size: 19px; fill: {TEXT}; }}
.p {{ font-size: 19px; fill: {GOLD}; }}
.nm {{ font-size: 19px; font-weight: 700; fill: {GOLD}; }}
.ds {{ font-size: 19px; fill: {MUTED}; }}
.tg {{ font-size: 15px; fill: {GOLD_DIM}; text-anchor: end; }}
.cmd {{ transform-origin: {cx:.1f}px 0; animation: type {type_t:.2f}s steps({len(cmd)}, end) {t0}s both; }}
.ln {{ animation: on 0.2s ease-out both; }}
.cur {{ fill: {GOLD}; animation: on 0.2s {listed + len(BUILDS) * 0.09:.2f}s both, blink 1.1s steps(1) {listed + len(BUILDS) * 0.09:.2f}s infinite; }}
@keyframes type {{ from {{ transform: scaleX(0); }} }}
@keyframes on {{ from {{ opacity: 0; }} }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
"""
    w = len(cmd) * adv
    body = [card_bg(W, H),
            f'<line x1="0" y1="48" x2="{W}" y2="48" stroke="{BORDER}"/>',
            f'<circle cx="30" cy="24" r="6" fill="{GOLD_DIM}"/>',
            f'<circle cx="52" cy="24" r="6" fill="#3a3630"/><circle cx="74" cy="24" r="6" fill="#3a3630"/>',
            f'<text class="mono bar" x="{W / 2}" y="29">soumil@purdue: ~/builds</text>',
            f'<defs><clipPath id="cc"><rect class="cmd" x="{cx:.1f}" y="{top - 22}" width="{w + 1:.1f}" height="30"/></clipPath></defs>',
            f'<text class="mono p" x="40" y="{top}">$</text>',
            f'<text class="mono t" x="{cx:.1f}" y="{top}" textLength="{w:.1f}" lengthAdjust="spacing" clip-path="url(#cc)">{esc(cmd)}</text>']
    for k, (name, desc, tag) in enumerate(BUILDS):
        y = top + pitch * (k + 1) + 8
        body.append(f'<g class="ln" style="animation-delay: {listed + k * 0.09:.2f}s">'
                    f'<text class="mono nm" x="40" y="{y}">{esc(name)}</text>'
                    f'<text class="mono ds" x="190" y="{y}">{esc(desc)}</text>'
                    f'<text class="mono tg" x="{W - 40}" y="{y}">{esc(tag)}</text></g>')
    y = top + pitch * (len(BUILDS) + 1) + 16
    body.append(f'<g class="ln" style="animation-delay: {listed + len(BUILDS) * 0.09:.2f}s">'
                f'<text class="mono p" x="40" y="{y}">$</text></g>'
                f'<rect class="cur" x="{cx:.1f}" y="{y - 17}" width="10" height="21" rx="1.5"/>')
    alt = "; ".join(f"{n}: {d}" for n, d, _ in BUILDS)
    return svg(W, H, "\n".join(body), css, f"Builds: {alt}")


def findings():
    W, top, pitch = 1200, 76, 132
    H = top + pitch * len(FINDINGS) + 4
    css = f"""
.hd {{ font-size: 13px; letter-spacing: 2px; fill: {GOLD}; }}
.big {{ font-size: 46px; font-weight: 700; fill: {GOLD}; }}
.cap {{ font-size: 13px; fill: {MUTED}; }}
.hl {{ font-size: 22px; font-weight: 700; fill: {TEXT}; }}
.ex {{ font-size: 18px; fill: {MUTED}; }}
.src {{ font-size: 13px; fill: {GOLD_DIM}; }}
.row {{ animation: up 0.6s ease-out both; }}
@keyframes up {{ from {{ opacity: 0; transform: translateY(8px); }} }}
"""
    body = [card_bg(W, H, 18),
            f'<text class="mono hd" x="40" y="50">LAB NOTEBOOK \u00b7 RESULTS I DIDN\u2019T EXPECT</text>']
    for i, (num, cap, headline, explain, src) in enumerate(FINDINGS):
        r = top + i * pitch
        if i:
            body.append(f'<line x1="40" y1="{r}" x2="{W - 40}" y2="{r}" stroke="{BORDER}"/>')
        body.append(
            f'<g class="row" style="animation-delay: {0.15 + i * 0.12:.2f}s">'
            f'<text class="mono big" x="40" y="{r + 70}">{esc(num)}</text>'
            f'<text class="mono cap" x="42" y="{r + 98}">{esc(cap)}</text>'
            f'<text class="sans hl" x="270" y="{r + 46}">{esc(headline)}</text>'
            f'<text class="sans ex" x="270" y="{r + 76}">{esc(explain)}</text>'
            f'<text class="mono src" x="270" y="{r + 106}">{esc(src)}</text></g>')
    alt = " ".join(f"{h} {e} ({n}, {c}; {s})." for n, c, h, e, s in FINDINGS)
    return svg(W, H, "\n".join(body), css, alt)


def timeline():
    W, row, top = 1200, 96, 56
    H = top + row * len(TIMELINE) - 10
    lx = 196
    css = f"""
.yr {{ font-size: 17px; fill: {GOLD}; text-anchor: end; }}
.org {{ font-size: 25px; font-weight: 700; fill: {TEXT}; }}
.role {{ font-size: 21px; font-weight: 400; fill: {MUTED}; }}
.det {{ font-size: 19px; fill: {MUTED}; }}
.ring {{ fill: none; stroke: {GOLD}; stroke-width: 2; opacity: 0; transform-box: fill-box; transform-origin: center;
  animation: ping 2.2s ease-out 0.8s infinite; }}
.row {{ animation: in 0.6s ease-out both; }}
@keyframes ping {{ 0% {{ opacity: 0.8; transform: scale(1); }} 100% {{ opacity: 0; transform: scale(2.6); }} }}
@keyframes in {{ from {{ opacity: 0; transform: translateX(-8px); }} }}
"""
    body = [card_bg(W, H, 18),
            f'<line x1="{lx}" y1="{top - 6}" x2="{lx}" y2="{H - 46}" stroke="{BORDER}" stroke-width="2"/>']
    for i, (yr, org, role, det, now) in enumerate(TIMELINE):
        y = top + i * row
        dot = (f'<circle cx="{lx}" cy="{y - 8}" r="7" fill="{GOLD}"/>'
               f'<circle class="ring" cx="{lx}" cy="{y - 8}" r="7"/>' if now else
               f'<circle cx="{lx}" cy="{y - 8}" r="6" fill="{BG}" stroke="{GOLD_DIM}" stroke-width="2"/>')
        body.append(
            f'<g class="row" style="animation-delay: {0.1 + i * 0.1:.1f}s">'
            f'<text class="mono yr" x="{lx - 32}" y="{y}">{esc(yr)}</text>{dot}'
            f'<text class="sans org" x="{lx + 32}" y="{y}">{esc(org)}<tspan class="role" dx="14">{esc(role)}</tspan></text>'
            f'<text class="sans det" x="{lx + 32}" y="{y + 31}">{esc(det)}</text></g>')
    alt = "; ".join(f"{yr}: {org}, {role}. {det}" for yr, org, role, det, _ in TIMELINE)
    return svg(W, H, "\n".join(body), css, alt)


def main():
    ASSETS.mkdir(exist_ok=True)
    out = {"hero.svg": hero(), "numbers.svg": numbers(), "terminal.svg": terminal(),
           "findings.svg": findings(), "timeline.svg": timeline()}
    for name, text in out.items():
        (ASSETS / name).write_text(text, encoding="utf-8")
        print(f"wrote assets/{name}")


if __name__ == "__main__":
    main()
