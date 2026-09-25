"""Generates about.svg: an editor window that types out a small PHP class.

Run `python3 build_about.py` after editing LINES to regenerate the SVG.
"""
from html import escape

C = {
    "kw": "#c084fc",
    "type": "#fbbf24",
    "str": "#86efac",
    "var": "#f472b6",
    "fn": "#60a5fa",
    "p": "#94a3b8",
    "cm": "#64748b",
    "t": "#e2e8f0",
}

# Each line is a list of (color-key, text) tokens.
LINES = [
    [("kw", "<?php")],
    [],
    [("kw", "namespace "), ("t", "App\\Developers"), ("p", ";")],
    [],
    [("cm", "/** Building for the web, from idea to production. */")],
    [("kw", "final class "), ("type", "Hesam "), ("kw", "extends "), ("type", "Developer")],
    [("p", "{")],
    [("kw", "    public string "), ("var", "$role  "), ("p", "= "), ("str", "'Full-Stack Developer'"), ("p", ";")],
    [("kw", "    public array  "), ("var", "$stack "), ("p", "= ["), ("str", "'PHP'"), ("p", ", "), ("str", "'Laravel'"), ("p", ", "), ("str", "'Filament'"), ("p", ", "), ("str", "'Go'"), ("p", ", "), ("str", "'TS'"), ("p", "];")],
    [("kw", "    public array  "), ("var", "$ships "), ("p", "= ["), ("str", "'CRMs'"), ("p", ", "), ("str", "'E-commerce'"), ("p", ", "), ("str", "'Streaming'"), ("p", ", "), ("str", "'AI'"), ("p", "];")],
    [],
    [("kw", "    public function "), ("fn", "motto"), ("p", "(): "), ("kw", "string")],
    [("p", "    {")],
    [("kw", "        return "), ("str", "'Clean code first. Fast code second. Shipped always.'"), ("p", ";")],
    [("p", "    }")],
    [("p", "}")],
]

W = 900
LINE_H = 24
TOP = 86          # baseline of the first code line
GUTTER_X = 52     # right edge of line numbers
CODE_X = 72
CHAR_W = 9.2      # generous width of a 15px monospace glyph
PER_CHAR = 0.018  # seconds per typed character
GAP = 0.12        # pause between lines
START = 0.6
ITALIC = ' font-style="italic"'

H = TOP + LINE_H * (len(LINES) - 1) + 40

out = []
defs = []
t = START

for i, tokens in enumerate(LINES):
    y = TOP + i * LINE_H
    text = "".join(s for _, s in tokens)
    out.append(
        f'<text class="ln" x="{GUTTER_X}" y="{y}" text-anchor="end" style="animation-delay:{t:.2f}s">{i + 1}</text>'
    )
    if not tokens:
        t += GAP
        continue
    dur = max(len(text) * PER_CHAR, 0.08)
    width = len(text) * CHAR_W + 24
    defs.append(
        f'<clipPath id="l{i}"><rect x="{CODE_X - 2}" y="{y - 18}" width="0" height="{LINE_H}">'
        f'<animate attributeName="width" from="0" to="{width:.0f}" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/>'
        f"</rect></clipPath>"
    )
    spans = "".join(
        f'<tspan fill="{C[k]}"{ITALIC if k == "cm" else ""}>{escape(s).replace(" ", "&#160;")}</tspan>'
        for k, s in tokens
    )
    out.append(f'<text class="code" x="{CODE_X}" y="{y}" clip-path="url(#l{i})">{spans}</text>')
    t += dur + GAP

cursor_x, cursor_y = CODE_X + 12, TOP + (len(LINES) - 1) * LINE_H

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Hesam.php — a PHP class describing Hesam's role, stack and motto">
  <title>Hesam.php</title>
  <defs>
    <linearGradient id="win" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#111827"/>
      <stop offset="1" stop-color="#0b0f1a"/>
    </linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#a78bfa"/>
      <stop offset="0.5" stop-color="#22d3ee"/>
      <stop offset="1" stop-color="#f472b6"/>
    </linearGradient>
    {"".join(defs)}
  </defs>
  <style>
    .code {{ font: 15px ui-monospace, 'SF Mono', 'Cascadia Code', Consolas, 'Liberation Mono', monospace; white-space: pre; }}
    .ln {{ font: 13px ui-monospace, 'SF Mono', Consolas, 'Liberation Mono', monospace; fill: #475569; opacity: 0; animation: show .2s ease forwards; }}
    .tab {{ font: 600 13px ui-monospace, 'SF Mono', Consolas, 'Liberation Mono', monospace; fill: #e2e8f0; }}
    .hint {{ font: 12px ui-monospace, 'SF Mono', Consolas, 'Liberation Mono', monospace; fill: #64748b; }}
    .cursor {{ opacity: 0; animation: show 0s linear {t:.2f}s forwards, blink 1s steps(1) {t:.2f}s infinite; }}
    @keyframes show {{ to {{ opacity: 1; }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
  </style>

  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="url(#win)" stroke="#ffffff" stroke-opacity="0.08"/>
  <rect x="24" y="0" width="{W - 48}" height="2" rx="1" fill="url(#edge)" opacity="0.8"/>

  <circle cx="26" cy="26" r="6.5" fill="#ff5f57"/>
  <circle cx="48" cy="26" r="6.5" fill="#febc2e"/>
  <circle cx="70" cy="26" r="6.5" fill="#28c840"/>

  <rect x="98" y="12" width="128" height="30" rx="8" fill="#ffffff" fill-opacity="0.05"/>
  <circle cx="114" cy="27" r="4" fill="#818cf8"/>
  <text class="tab" x="126" y="32">Hesam.php</text>
  <text class="hint" x="{W - 24}" y="32" text-anchor="end">PHP 8.3 · UTF-8</text>

  <line x1="0" y1="52" x2="{W}" y2="52" stroke="#ffffff" stroke-opacity="0.06"/>

  {chr(10).join("  " + o for o in out).strip()}

  <rect class="cursor" x="{cursor_x}" y="{cursor_y - 15}" width="9" height="19" rx="1.5" fill="#22d3ee"/>
</svg>
"""

with open(__file__.replace("build_about.py", "about.svg"), "w") as f:
    f.write(svg)
print(f"about.svg written ({W}x{H}, typing ends at {t:.1f}s)")
