"""Generates header.svg: the fire-themed profile banner.

Flames and embers are randomised from a fixed seed, so re-running
`python3 build_header.py` gives the same SVG unless you change SEED.
"""
import random

SEED = 7
W, H = 1200, 400
random.seed(SEED)


def flame(x, w, h, base):
    """A teardrop tongue of fire standing on y=base."""
    l, r, top = x - w / 2, x + w / 2, base - h
    return (
        f"M {l:.1f} {base} "
        f"C {l:.1f} {base - h * .45:.1f}, {x - w * .12:.1f} {base - h * .7:.1f}, {x:.1f} {top:.1f} "
        f"C {x + w * .12:.1f} {base - h * .7:.1f}, {r:.1f} {base - h * .45:.1f}, {r:.1f} {base} Z"
    )


def flame_layer(cls, color, step, w_range, h_center, h_edge, jitter):
    out = []
    x = -30
    while x < W + 30:
        edge = min(abs(x - W / 2) / (W / 2), 1) ** 1.6
        h = h_center + (h_edge - h_center) * edge + random.uniform(-jitter, jitter)
        w = random.uniform(*w_range)
        dur = random.uniform(1.1, 2.1)
        delay = -random.uniform(0, 2)
        out.append(
            f'<path class="tongue" d="{flame(x, w, h, H + 6)}" '
            f'style="animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s"/>'
        )
        x += step + random.uniform(-8, 8)
    return f'<g class="{cls}" fill="{color}">\n      ' + "\n      ".join(out) + "\n    </g>"


def embers(n):
    colors = ["#fde047", "#fbbf24", "#fb923c", "#f97316", "#fff7ed"]
    out = []
    for _ in range(n):
        cx = random.uniform(10, W - 10)
        cy = H - random.uniform(0, 30)
        r = random.uniform(1, 2.6)
        dx = random.uniform(-60, 60)
        dy = -random.uniform(170, 340)
        dur = random.uniform(4, 9)
        delay = -random.uniform(0, dur)
        out.append(
            f'<circle class="ember" cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.1f}" fill="{random.choice(colors)}" '
            f'style="--dx:{dx:.0f}px;--dy:{dy:.0f}px;animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s"/>'
        )
    return "\n      ".join(out)


back = flame_layer("flames back", "url(#fBack)", 46, (70, 110), 34, 150, 10)
mid = flame_layer("flames mid", "url(#fMid)", 40, (55, 90), 22, 105, 7)
front = flame_layer("flames front", "url(#fFront)", 38, (35, 60), 10, 55, 4)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Hesam Barzegar, aka Epicaler — Full-Stack Developer">
  <title>Hesam Barzegar, aka Epicaler — Full-Stack Developer</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0c0605"/>
      <stop offset="0.65" stop-color="#170905"/>
      <stop offset="1" stop-color="#2a0d04"/>
    </linearGradient>

    <linearGradient id="ink" x1="0" y1="0" x2="600" y2="0" gradientUnits="userSpaceOnUse" spreadMethod="reflect">
      <stop offset="0" stop-color="#fde047"/>
      <stop offset="0.45" stop-color="#fb923c"/>
      <stop offset="1" stop-color="#ef4444"/>
      <animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="1200 0" dur="6s" repeatCount="indefinite"/>
    </linearGradient>

    <radialGradient id="heat" cx="0.5" cy="1" r="0.75">
      <stop offset="0" stop-color="#f97316" stop-opacity="0.45"/>
      <stop offset="0.5" stop-color="#dc2626" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#dc2626" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="fBack" x1="0" y1="{H}" x2="0" y2="{H - 170}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#dc2626"/>
      <stop offset="0.6" stop-color="#991b1b" stop-opacity="0.8"/>
      <stop offset="1" stop-color="#7f1d1d" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="fMid" x1="0" y1="{H}" x2="0" y2="{H - 120}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#fb923c"/>
      <stop offset="0.55" stop-color="#ea580c" stop-opacity="0.85"/>
      <stop offset="1" stop-color="#c2410c" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="fFront" x1="0" y1="{H}" x2="0" y2="{H - 65}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#fef3c7"/>
      <stop offset="0.4" stop-color="#fde047" stop-opacity="0.9"/>
      <stop offset="1" stop-color="#fbbf24" stop-opacity="0"/>
    </linearGradient>

    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="#a8a29e" fill-opacity="0.14"/>
    </pattern>

    <radialGradient id="fade" cx="0.5" cy="0.4" r="0.6">
      <stop offset="0" stop-color="#fff"/>
      <stop offset="1" stop-color="#000"/>
    </radialGradient>
    <mask id="gridMask">
      <rect width="{W}" height="{H}" fill="url(#fade)"/>
    </mask>

    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="55"/>
    </filter>

    <!-- wobbles the flame tongues so they lick instead of sway -->
    <filter id="burn" x="0" y="160" width="{W}" height="{H - 160}" filterUnits="userSpaceOnUse">
      <feTurbulence type="fractalNoise" baseFrequency="0.012 0.045" numOctaves="2" seed="3" result="noise">
        <animate attributeName="baseFrequency" values="0.012 0.045; 0.016 0.06; 0.012 0.045" dur="3s" repeatCount="indefinite"/>
      </feTurbulence>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="26" xChannelSelector="R" yChannelSelector="G" result="licked"/>
      <feGaussianBlur in="licked" stdDeviation="1.6"/>
    </filter>
    <filter id="flameGlow" x="0" y="100" width="{W}" height="{H - 100}" filterUnits="userSpaceOnUse">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <filter id="neonWide" x="-40%" y="-150%" width="180%" height="400%">
      <feGaussianBlur stdDeviation="11"/>
    </filter>
    <filter id="neonNarrow" x="-20%" y="-80%" width="140%" height="260%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>

    <clipPath id="card">
      <rect width="{W}" height="{H}" rx="24"/>
    </clipPath>
  </defs>

  <style>
    .name {{
      font: 800 76px 'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif;
      letter-spacing: -1.5px;
    }}
    .stroke {{
      fill: none;
      stroke: url(#ink);
      stroke-width: 1.4;
      stroke-dasharray: 520;
      stroke-dashoffset: 520;
      animation: draw 2.4s cubic-bezier(.6,.1,.3,1) forwards;
    }}
    .fill {{
      fill: url(#ink);
      opacity: 0;
      animation: fadeIn 1s ease 1.6s forwards;
    }}
    .role {{
      font: 600 17px ui-monospace, 'SF Mono', 'Cascadia Code', Consolas, 'Liberation Mono', monospace;
      letter-spacing: 7px;
      fill: #e7d6cb;
      opacity: 0;
      animation: rise .9s ease 3.3s forwards;
    }}
    .neon {{
      font: italic 600 46px 'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif;
      letter-spacing: 4px;
    }}
    .neon-on {{ opacity: 0; animation: neonOn 1.6s linear 2.2s forwards; }}
    .neon-flicker {{ animation: flicker 7s linear 4.5s infinite; }}
    .glow {{ animation: breathe 2.4s ease-in-out 3.8s infinite; }}
    .bad {{ animation: badLetter 5s steps(1) 5s infinite; }}
    .tube {{
      stroke-dasharray: 70;
      stroke-dashoffset: 70;
      animation: draw .6s ease-out 2.9s forwards;
    }}
    .chip text {{
      font: 600 14px ui-monospace, 'SF Mono', 'Cascadia Code', Consolas, 'Liberation Mono', monospace;
      fill: #f5ede6;
    }}
    .chip rect {{ fill: #1a0b07; fill-opacity: .82; stroke: #fb923c; stroke-opacity: .28; }}
    .chip {{ opacity: 0; animation: rise .7s ease forwards; }}
    .c1 {{ animation-delay: 3.80s; }}
    .c2 {{ animation-delay: 3.95s; }}
    .c3 {{ animation-delay: 4.10s; }}
    .c4 {{ animation-delay: 4.25s; }}
    .dot {{ animation: pulse 2s ease-in-out infinite; }}
    .caret {{ animation: blink 1s steps(1) infinite; }}

    .ignite {{ transform-origin: 600px {H}px; animation: ignite 1.4s cubic-bezier(.2,.8,.3,1) both; }}
    .tongue {{
      transform-box: fill-box;
      transform-origin: 50% 100%;
      animation-name: lick;
      animation-timing-function: ease-in-out;
      animation-iteration-count: infinite;
      animation-direction: alternate;
    }}
    .back {{ opacity: .9; }}
    .mid {{ opacity: .85; }}
    .front {{ opacity: .75; }}
    .ember {{
      opacity: 0;
      animation-name: float;
      animation-timing-function: ease-out;
      animation-iteration-count: infinite;
    }}

    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes fadeIn {{ to {{ opacity: 1; }} }}
    @keyframes rise {{
      from {{ opacity: 0; transform: translateY(10px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes neonOn {{
      0% {{ opacity: 0; }} 8% {{ opacity: .9; }} 11% {{ opacity: .08; }} 19% {{ opacity: 1; }}
      22% {{ opacity: .15; }} 27% {{ opacity: .15; }} 33% {{ opacity: 1; }} 37% {{ opacity: .5; }}
      42%, 100% {{ opacity: 1; }}
    }}
    @keyframes flicker {{
      0%, 86%, 93%, 100% {{ opacity: 1; }}
      87% {{ opacity: .3; }} 88% {{ opacity: 1; }} 90% {{ opacity: .55; }} 91% {{ opacity: 1; }}
    }}
    @keyframes breathe {{ 0%, 100% {{ opacity: .6; }} 50% {{ opacity: 1; }} }}
    @keyframes badLetter {{
      0%, 100% {{ fill-opacity: 1; stroke-opacity: 1; }}
      62% {{ fill-opacity: .12; stroke-opacity: .12; }} 64% {{ fill-opacity: 1; stroke-opacity: 1; }}
      66% {{ fill-opacity: .2; stroke-opacity: .2; }} 70% {{ fill-opacity: 1; stroke-opacity: 1; }}
    }}
    @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .35; }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @keyframes ignite {{ from {{ transform: scaleY(0); opacity: 0; }} to {{ transform: scaleY(1); opacity: 1; }} }}
    @keyframes lick {{
      0% {{ transform: scale(1, .82) skewX(-3deg); }}
      50% {{ transform: scale(.94, 1.12) skewX(2deg); }}
      100% {{ transform: scale(1.04, .95) skewX(4deg); }}
    }}
    @keyframes float {{
      0% {{ opacity: 0; transform: translate(0, 0); }}
      12% {{ opacity: 1; }}
      55% {{ transform: translate(calc(var(--dx) * -.4), calc(var(--dy) * .55)); }}
      80% {{ opacity: .7; }}
      100% {{ opacity: 0; transform: translate(var(--dx), var(--dy)); }}
    }}
  </style>

  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>

    <!-- drifting heat -->
    <g filter="url(#blur)" opacity="0.5">
      <circle cx="230" cy="360" r="150" fill="#b91c1c">
        <animateTransform attributeName="transform" type="translate" values="0 0; 80 -30; 0 0" dur="11s" repeatCount="indefinite"/>
      </circle>
      <circle cx="970" cy="370" r="160" fill="#c2410c">
        <animateTransform attributeName="transform" type="translate" values="0 0; -100 -25; 0 0" dur="13s" repeatCount="indefinite"/>
      </circle>
      <circle cx="640" cy="60" r="90" fill="#f59e0b" opacity="0.35">
        <animateTransform attributeName="transform" type="translate" values="0 0; -60 30; 0 0" dur="9s" repeatCount="indefinite"/>
      </circle>
    </g>

    <rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#gridMask)"/>
    <rect width="{W}" height="{H}" fill="url(#heat)"/>

    <!-- the fire -->
    <g class="ignite">
      <g filter="url(#flameGlow)" opacity="0.7">
        <use href="#fireBack"/>
      </g>
      <g filter="url(#burn)">
        <g id="fireBack">
    {back}
        </g>
    {mid}
    {front}
      </g>
    </g>

    <!-- embers -->
    <g>
      {embers(30)}
    </g>

    <!-- status pill -->
    <g transform="translate(600 58)">
      <rect x="-118" y="-15" width="236" height="30" rx="15" fill="#f59e0b" fill-opacity="0.08" stroke="#f59e0b" stroke-opacity="0.4"/>
      <circle class="dot" cx="-96" cy="0" r="4.5" fill="#f59e0b"/>
      <text x="8" y="5" text-anchor="middle" font-family="ui-monospace, 'SF Mono', Consolas, 'Liberation Mono', monospace" font-size="13" font-weight="600" fill="#fcd34d">open to collaboration</text>
    </g>

    <!-- name: outline draws, then fire fills in -->
    <text class="name stroke" x="600" y="150" text-anchor="middle">Hesam Barzegar</text>
    <text class="name fill" x="600" y="150" text-anchor="middle">Hesam Barzegar</text>

    <!-- neon alias: flickers on, then burns -->
    <g class="neon-on"><g class="neon-flicker">
      <g class="glow" filter="url(#neonWide)" fill="#ff4d00" stroke="#ff4d00">
        <text class="neon" x="600" y="214" text-anchor="middle">Epi<tspan class="bad">c</tspan>aler</text>
        <path d="M 474 198 h -62 M 728 198 h 62" stroke-width="4" stroke-linecap="round"/>
      </g>
      <g filter="url(#neonNarrow)" fill="#ff8a1f" stroke="#ff8a1f">
        <text class="neon" x="600" y="214" text-anchor="middle" stroke="none">Epi<tspan class="bad">c</tspan>aler</text>
        <path class="tube" d="M 474 198 h -62 M 728 198 h 62" stroke-width="3" stroke-linecap="round"/>
      </g>
      <text class="neon" x="600" y="214" text-anchor="middle" fill="#fff4e0" stroke="#ffb35c" stroke-width="0.8">Epi<tspan class="bad">c</tspan>aler</text>
      <path class="tube" d="M 474 198 h -62 M 728 198 h 62" stroke="#fff4e0" stroke-width="1.6" stroke-linecap="round"/>
    </g></g>

    <text class="role" x="600" y="264" text-anchor="middle">FULL-STACK DEVELOPER<tspan class="caret" fill="#f97316">_</tspan></text>

    <!-- stack chips -->
    <g transform="translate(357 294)"><g class="chip c1">
      <rect width="110" height="34" rx="10"/>
      <circle cx="18" cy="17" r="4" fill="#ef4444"/>
      <text x="30" y="22">Laravel</text>
    </g></g>
    <g transform="translate(479 294)"><g class="chip c2">
      <rect width="120" height="34" rx="10"/>
      <circle cx="18" cy="17" r="4" fill="#f97316"/>
      <text x="30" y="22">Filament</text>
    </g></g>
    <g transform="translate(611 294)"><g class="chip c3">
      <rect width="120" height="34" rx="10"/>
      <circle cx="18" cy="17" r="4" fill="#fbbf24"/>
      <text x="30" y="22">WordPress</text>
    </g></g>
    <g transform="translate(743 294)"><g class="chip c4">
      <rect width="100" height="34" rx="10"/>
      <circle cx="18" cy="17" r="4" fill="#fde047"/>
      <text x="30" y="22">Go</text>
    </g></g>

    <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="23.5" fill="none" stroke="#fb923c" stroke-opacity="0.14"/>
  </g>
</svg>
"""

with open(__file__.replace("build_header.py", "header.svg"), "w") as f:
    f.write(svg)
print(f"header.svg written ({W}x{H}, {len(svg) // 1024} KB)")
