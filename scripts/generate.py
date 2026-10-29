"""Builds the static SVGs in assets/: hero, numbers, project cards, timeline, footer.

    python scripts/generate.py

Edit the data below and re-run; stats.py handles the live GitHub cards.
"""

import random
from pathlib import Path

from theme import (BG, BORDER, GOLD, GOLD_DIM, MUTED, SURFACE_HI, TEXT, card_bg,
                   esc, svg, wrap)

ASSETS = Path(__file__).resolve().parent.parent / "assets"

NAME = "Soumil Bhandari"
SUBTITLE = ("Computer Engineering @ Purdue", "AI Researcher @ Perforated AI")
PHRASES = [
    "training diffusion language models from scratch",
    "catching backdoors hidden in neural networks",
    "building wearables for neurodegenerative disease",
    "putting guardrails on AI agents",
    "measuring, honestly, whether it actually works",
]

NUMBERS = [
    ("3", "provisional US patents", "neurodegenerative modeling"),
    ("1M+", "clinical records through", "my pipelines at McKesson"),
    ("Top 4%", "YC Startup School", "of 35,000+ applicants"),
    ("1st", "Best Overall Hack", "HopHacks 2026"),
    ("1,000+", "students on Notes360.ai", "across five schools"),
]

PROJECTS = [
    ("nanoDLM", "ML RESEARCH",
     "The nanoGPT of masked-diffusion language models: ~1,100 lines of plain PyTorch, "
     "with an honest head-to-head against a matched autoregressive baseline.",
     "char-level · RoPE · self-conditioning", "Python"),
    ("deadbolt", "AI SECURITY",
     "A benchmark for catching backdoors in neural networks, and for finding out "
     "which published detectors actually work.",
     "6 attacks · 6 detectors · 540 blind scans", "Python"),
    ("Bastion", "AGENT INFRASTRUCTURE",
     "A local-first control plane for AI agent tools. Caps spend, rate-limits, "
     "and audits every MCP tool call in a tamper-evident log.",
     "pip install bastion-mcp", "Python"),
    ("HalluScope", "LLM EVALUATION",
     "Three ways to catch an LLM lying, and an honest AUROC evaluation of which one "
     "actually works. Highlights fabricated spans live.",
     "HaluEval · TruthfulQA · Gradio", "Python"),
    ("SecuriVax", "HEALTH HARDWARE",
     "Is this vial still good? A last-mile cold-chain monitor that makes vaccine "
     "integrity visible, measurable, and actionable.",
     "Best Overall · HopHacks 2026", "Python"),
    ("NeuraBand", "NEUROTECH",
     "A pill-sized wearable that passively tracks ten neurological biomarkers and "
     "streams them over BLE to a clinical dashboard.",
     "10 biomarkers · Web Bluetooth · Expo", "JavaScript"),
    ("ATLAS", "NEUROTECH · HARVARD",
     "Closed-loop TMS motor-threshold estimation: calibrated MEP detection plus "
     "Bayesian, entropy-minimizing adaptive search.",
     "built at Harvard Medical School", "Python"),
    ("You2", "PHYSICAL AI",
     "A local-only desk assistant that remembers. It consolidates every conversation "
     "into a second brain, and none of it leaves the box.",
     "on-device · “Hey Friday” · no cloud", "Python"),
]

LANG_COLORS = {"Python": "#3572A5", "JavaScript": "#f1e05a", "TypeScript": "#3178c6"}

TIMELINE = [
    ("2026 – now", "Perforated AI", "AI Researcher",
     "Researching dendritic model compression", True),
    ("2026 – now", "Purdue University", "B.S. Computer Engineering",
     "VIP / AAMED: Neural Space Cap, an EEG cap for astronaut EVA helmets", False),
    ("2026", "Harvard Medical School", "Research Intern, TMS Lab",
     "Closed-loop motor-threshold estimation (ATLAS) with Dr. Aapo Nummenmaa", False),
    ("2025", "Neurafy", "Founder",
     "Alzheimer’s progression modeling · three provisional US patents", False),
    ("2025", "McKesson", "Software Engineering Intern",
     "GPT pipelines over 1M+ clinical records", False),
    ("2025", "IIT Roorkee", "Research Intern",
     "XGBoost at 92%+ accuracy; LLaMA-2 and Flan-T5 fine-tuned with LoRA", False),
    ("2023", "Tekizma", "Software Engineering Intern",
     "spaCy + Hugging Face NLP · Distinguished Intern Award, multiple years", False),
]


def ecg_path(x0, x1, base, beats):
    """A heartbeat trace. Returns (path d, approximate length)."""
    shape = [(0, 0), (10, -6), (20, 0), (28, 0), (32, 6), (38, -46), (44, 14),
             (50, 0), (64, 0), (76, -10), (90, 0)]
    pts = [(x0, base)]
    for bx in beats:
        pts += [(bx + dx, base + dy) for dx, dy in shape]
    pts.append((x1, base))
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
    length = sum(((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5 for a, b in zip(pts, pts[1:]))
    return d, int(length) + 1


def trace(x0, x1, base, beats, draw_delay=0.3, pulse_delay=2.8):
    d, L = ecg_path(x0, x1, base, beats)
    css = f"""
.trace {{ fill: none; stroke: #3a3630; stroke-width: 2; stroke-linejoin: round;
  stroke-dasharray: {L}; animation: draw 2.4s ease-out {draw_delay}s both; }}
.pulse {{ fill: none; stroke: {GOLD}; stroke-width: 2.5; stroke-linejoin: round; opacity: 0;
  stroke-dasharray: 140 {L}; filter: url(#glow);
  animation: travel 4.5s linear {pulse_delay}s infinite; }}
@keyframes draw {{ from {{ stroke-dashoffset: {L}; }} to {{ stroke-dashoffset: 0; }} }}
@keyframes travel {{ 0% {{ stroke-dashoffset: 140; opacity: 1; }}
  100% {{ stroke-dashoffset: {-L}; opacity: 1; }} }}
"""
    body = (
        '<defs><filter id="glow" x="-10%" y="-50%" width="120%" height="200%">'
        '<feGaussianBlur stdDeviation="3" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
        "</filter></defs>"
        f'<path class="trace" d="{d}"/><path class="pulse" d="{d}"/>'
    )
    return css, body


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
    W, H = 1200, 450
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

    tcss, tbody = trace(40, W - 40, 398, [130, 410, 690, 970], pulse_delay=done)
    css += tcss
    body.append(tbody)
    body.append(f'<text class="mono foot" x="48" y="432">masked diffusion · 16 denoising steps</text>')
    body.append(f'<text class="mono foot" x="{W - 48}" y="432" text-anchor="end">soumilbhandari.com</text>')
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


def project_card(idx, name, cat, desc, stat, lang):
    W, H = 600, 270
    css = f"""
.cat {{ font-size: 13px; letter-spacing: 2px; fill: {GOLD}; }}
.idx {{ font-size: 46px; font-weight: 700; fill: {SURFACE_HI}; text-anchor: end; }}
.name {{ font-size: 30px; font-weight: 700; fill: {TEXT}; }}
.desc {{ font-size: 17px; fill: {MUTED}; }}
.stat {{ font-size: 14px; fill: {GOLD}; }}
.lang {{ font-size: 14px; fill: {MUTED}; text-anchor: end; }}
"""
    lines = wrap(desc, 56)[:3]
    body = [card_bg(W, H),
            f'<rect x="36" y="0" width="56" height="3" rx="1.5" fill="{GOLD}"/>',
            f'<text class="mono idx" x="{W - 32}" y="68">{idx:02d}</text>',
            f'<text class="mono cat" x="36" y="52">{esc(cat)}</text>',
            f'<text class="sans name" x="36" y="98">{esc(name)}</text>']
    for k, line in enumerate(lines):
        body.append(f'<text class="sans desc" x="36" y="{138 + k * 25}">{esc(line)}</text>')
    lang_w = len(lang) * 8
    body += [f'<line x1="36" y1="{H - 54}" x2="{W - 36}" y2="{H - 54}" stroke="{BORDER}"/>',
             f'<text class="mono stat" x="36" y="{H - 24}">{esc(stat)}</text>',
             f'<circle cx="{W - 36 - lang_w - 12}" cy="{H - 29}" r="6" fill="{LANG_COLORS.get(lang, MUTED)}"/>',
             f'<text class="sans lang" x="{W - 36}" y="{H - 24}">{esc(lang)}</text>']
    return svg(W, H, "\n".join(body), css, f"{name}: {desc}")


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


def footer():
    W, H = 1200, 120
    css = f".bye {{ font-size: 15px; fill: {MUTED}; text-anchor: middle; }}"
    tcss, tbody = trace(40, W - 40, 92, [250, 560, 870], pulse_delay=1.5)
    body = [tbody, f'<text class="mono bye" x="{W / 2}" y="34">thanks for scrolling · still building</text>']
    return svg(W, H, "\n".join(body), css + tcss, "Thanks for scrolling")


def main():
    (ASSETS / "projects").mkdir(parents=True, exist_ok=True)
    out = {"hero.svg": hero(), "numbers.svg": numbers(), "timeline.svg": timeline(), "footer.svg": footer()}
    for i, p in enumerate(PROJECTS, 1):
        out[f"projects/{p[0].lower()}.svg"] = project_card(i, *p)
    for name, text in out.items():
        (ASSETS / name).write_text(text, encoding="utf-8")
        print(f"wrote assets/{name}")


if __name__ == "__main__":
    main()
