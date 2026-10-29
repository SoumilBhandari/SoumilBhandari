"""Shared palette and SVG helpers. Black and Purdue gold, matching soumilbhandari.com."""

from html import escape

BG = "#0b0b0d"
SURFACE = "#141417"
SURFACE_HI = "#1b1b1f"
BORDER = "#26262b"
TEXT = "#f3f1ed"
MUTED = "#9d9993"
GOLD = "#cfb991"
GOLD_DIM = "#8d7f5f"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

BASE_CSS = f"""
.sans {{ font-family: {SANS}; }}
.mono {{ font-family: {MONO}; }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
"""


def esc(s):
    return escape(str(s), quote=True)


def svg(width, height, body, css="", title=""):
    """Wrap body in a standalone SVG. Every animation is written so that the
    un-animated state is the final state, so reduced-motion viewers lose nothing."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">\n'
        f"<title>{esc(title)}</title>\n"
        f"<style>{BASE_CSS}{css}</style>\n{body}\n</svg>\n"
    )


def card_bg(width, height, rx=16):
    return (
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="{rx}" '
        f'fill="{SURFACE}" stroke="{BORDER}"/>'
    )


def wrap(text, limit):
    lines, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > limit:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        lines.append(line)
    return lines
