"""Builds assets/hero.svg: the name, nothing else.

    python scripts/generate.py

The outline draws itself in, gold floods the letters, then a light sweep
runs across them on a loop.
"""

from pathlib import Path

from theme import GOLD, esc, svg

ASSETS = Path(__file__).resolve().parent.parent / "assets"

NAME = "Soumil Bhandari"
SHINE = "#fff4d8"


def hero():
    W, H = 1200, 170
    draw, flood = 2.2, 0.8
    sweep, rest = 1.6, 3.4
    cycle = sweep + rest
    css = f"""
.name {{ font-size: 112px; font-weight: 800; letter-spacing: -2px; text-anchor: middle;
  fill: url(#shine); stroke: {GOLD}; stroke-width: 1.4; stroke-opacity: 0;
  animation: draw {draw + flood:.1f}s cubic-bezier(.6, 0, .3, 1) both; }}
.glow {{ font-size: 112px; font-weight: 800; letter-spacing: -2px; text-anchor: middle;
  fill: {GOLD}; opacity: 0.22; filter: url(#blur); animation: glow {draw + flood:.1f}s ease-out both; }}
@keyframes draw {{
  0% {{ stroke-dasharray: 420; stroke-dashoffset: 420; stroke-opacity: 1; fill-opacity: 0; }}
  {100 * draw / (draw + flood):.0f}% {{ stroke-dasharray: 420; stroke-dashoffset: 0; stroke-opacity: 1; fill-opacity: 0; }}
  100% {{ stroke-dasharray: 420; stroke-dashoffset: 0; stroke-opacity: 0; fill-opacity: 1; }} }}
@keyframes glow {{ 0%, {100 * draw / (draw + flood):.0f}% {{ opacity: 0; }} }}
"""
    x, y = W / 2, 122
    start = draw + flood
    body = f"""<defs>
<linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0" gradientTransform="translate(-900 0)">
  <stop offset="0" stop-color="{GOLD}"/>
  <stop offset="0.42" stop-color="{GOLD}"/>
  <stop offset="0.5" stop-color="{SHINE}"/>
  <stop offset="0.58" stop-color="{GOLD}"/>
  <stop offset="1" stop-color="{GOLD}"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-900 0;900 0;900 0"
    keyTimes="0;{sweep / cycle:.3f};1" dur="{cycle}s" begin="{start - 0.3:.1f}s" repeatCount="indefinite"/>
</linearGradient>
<filter id="blur" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
</defs>
<text class="sans glow" x="{x}" y="{y}">{esc(NAME)}</text>
<text class="sans name" x="{x}" y="{y}">{esc(NAME)}</text>"""
    return svg(W, H, body, css, NAME)


def main():
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "hero.svg").write_text(hero(), encoding="utf-8")
    print("wrote assets/hero.svg")


if __name__ == "__main__":
    main()
