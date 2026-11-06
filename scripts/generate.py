"""Builds the static SVGs in assets/: hero and timeline.

    python scripts/generate.py

Edit the data below and re-run.
"""

import random
from pathlib import Path

from theme import (BG, BORDER, GOLD, GOLD_DIM, MUTED, TEXT, card_bg,
                   esc, svg)

ASSETS = Path(__file__).resolve().parent.parent / "assets"

NAME = "Soumil Bhandari"
SUBTITLE = ("computer engineering @ purdue", "ai research @ perforated ai")
PHRASES = [
    "training diffusion LMs from scratch",
    "finding backdoors in neural nets",
    "routing boards for a race car",
    "building EEG caps for space",
    "checking if any of it actually works",
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
    LM samples, then a terminal line cycles through what I work on."""
    W, H = 1200, 400
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
.caret {{ fill: {GOLD}; }}
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

    # Typing line. Each character is its own <text> on a fixed monospace grid and
    # fades in on schedule; Safari ignores animations inside <clipPath>, so this
    # sticks to plain opacity and transforms.
    adv, ty, dt = 11.4, 322, 0.045
    slot, start = 4.6, done + 0.6
    cycle = slot * len(PHRASES)
    longest = max(len(p) for p in PHRASES)
    xs = (W - (longest + 2) * adv) / 2
    tx = xs + 2 * adv
    shown = 100 * (slot - 0.35) / cycle
    css += f"""
.tc {{ animation-duration: {cycle:.1f}s; animation-iteration-count: infinite;
  animation-fill-mode: both; animation-timing-function: linear; }}
@keyframes slot {{ 0% {{ opacity: 0; }} 0.01%, {shown:.2f}% {{ opacity: 1; }} {shown + 0.01:.2f}%, 100% {{ opacity: 0; }} }}
""" + "".join(f"@keyframes ch{k} {{ 0%, {100 * (k + 1) * dt / cycle:.3f}% {{ opacity: 0; }} "
              f"{100 * (k + 1) * dt / cycle + 0.01:.3f}%, 100% {{ opacity: 1; }} }}\n.c{k} {{ animation-name: ch{k}; }}\n"
              for k in range(longest))
    body.append(f'<text class="mono chev" x="{xs:.1f}" y="{ty}">\u203a</text>')
    for i, p in enumerate(PHRASES):
        n, delay = len(p), start + i * slot
        p1 = 100 * n * dt / cycle
        css += f"""
.g{i} {{ {"" if i == 0 else "opacity: 0;"} animation: slot {cycle:.1f}s linear {delay:.2f}s infinite both; }}
.g{i} .tc {{ animation-delay: {delay:.2f}s; }}
@keyframes caret{i} {{ 0% {{ transform: translateX(0); animation-timing-function: steps({n}, end); }}
  {p1:.2f}%, 100% {{ transform: translateX({n * adv:.1f}px); }} }}
.k{i} {{ animation: caret{i} {cycle:.1f}s {delay:.2f}s infinite both; }}
"""
        chars = "".join(f'<text class="mono typed tc c{k}" x="{tx + k * adv:.1f}" y="{ty}">{esc(ch)}</text>'
                        for k, ch in enumerate(p) if ch != " ")
        body.append(f'<g class="g{i}">{chars}<rect class="caret k{i}" x="{tx + 1:.1f}" y="{ty - 17}" '
                    f'width="10" height="21" rx="1.5"/></g>')

    body.append(f'<text class="mono foot" x="{W / 2}" y="{H - 30}" text-anchor="middle">'
                f'name \u00b7 masked diffusion, 16 denoising steps</text>')
    return svg(W, H, "\n".join(body), css, f"{NAME}: {SUBTITLE[0]}, {SUBTITLE[1]}")


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
    out = {"hero.svg": hero(), "timeline.svg": timeline()}
    for name, text in out.items():
        (ASSETS / name).write_text(text, encoding="utf-8")
        print(f"wrote assets/{name}")


if __name__ == "__main__":
    main()
