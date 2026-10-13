"""Generates dark.svg / light.svg (terminal-style banner). Re-run after editing ROWS."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, os

W, H = 1180, 610
ROWS = [
    ("Subject", "Sudipto Biswas"), ("Role", "Back-End Developer"),
    ("Status", "Building + Learning + Shipping"), None,
    ("Core.Lang", "Go · PHP · JavaScript"), ("Core.Backend", "gRPC · REST · Web3.js"),
    ("Core.Database", "PostgreSQL"), ("Core.Infra", "Linux · Git"), None,
    ("Grid.Portfolio", "sudipto.xyz"), ("Grid.LinkedIn", "in/developer-sudipto"),
    ("Grid.GitHub", "dipto0079"), ("Grid.Facebook", "developer.sudipto"),
]
THEMES = {
    "dark":  dict(bg="#0D1117", panel="#0A101F", chrome="#22D3EE", portrait="#A78BFA", accent="#10B981", label="#94A3B8", value="#F8FAFC", leader="#334155"),
    "light": dict(bg="#FFFFFF", panel="#F1F5F9", chrome="#0891B2", portrait="#7C3AED", accent="#059669", label="#475569", value="#0F172A", leader="#CBD5E1"),
}

def monogram(text="SB", gw=150, gh=170):
    img = Image.new("L", (gw, gh), 0)
    font = None
    for f in ("arialbd.ttf", "DejaVuSans-Bold.ttf", "arial.ttf"):
        try: font = ImageFont.truetype(f, 125); break
        except OSError: pass
    d = ImageDraw.Draw(img)
    bb = d.textbbox((0, 0), text, font=font)
    d.text(((gw - (bb[2]-bb[0]))/2 - bb[0], (gh - (bb[3]-bb[1]))/2 - bb[1]), text, fill=255, font=font)
    a = np.asarray(img, float) / 255
    yy, xx = np.mgrid[0:gh, 0:gw]
    # dither-like density: solid core, sparse halo
    from scipy.ndimage import gaussian_filter
    dens = np.clip(a * 0.95 + gaussian_filter(a, 4) * 0.35, 0, 1)
    rng = np.random.default_rng(7)
    return (rng.random(dens.shape) < dens)

def dots_path(mask, x0, y0, cell):
    parts = []
    for y, row in enumerate(mask):
        x = 0
        while x < len(row):
            if row[x]:
                s = x
                while x < len(row) and row[x]: x += 1
                parts.append(f"M{x0+s*cell:.1f} {y0+y*cell:.1f}h{(x-s)*cell:.1f}v{cell*1.05:.1f}h-{(x-s)*cell:.1f}z")
            else: x += 1
    return "".join(parts)

def build(name, t):
    px, py, pw, ph = 40, 90, 430, 480
    mask = monogram()
    cell = 2.6
    mx = px + (pw - mask.shape[1]*cell)/2
    my = py + 30
    path = dots_path(mask, mx, my, cell)
    rx, rw = 510, 630
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Consolas,Menlo,\'DejaVu Sans Mono\',monospace">',
        f'<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}"/>',
        f'<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="10" fill="{t["panel"]}" stroke="{t["chrome"]}" stroke-opacity=".5"/>',
        '<circle cx="36" cy="38" r="6" fill="#EF4444"/><circle cx="58" cy="38" r="6" fill="#F59E0B"/><circle cx="80" cy="38" r="6" fill="#10B981"/>',
        f'<text x="{W/2}" y="43" text-anchor="middle" font-size="14" fill="{t["label"]}">profile.sh --live</text>',
        f'<line x1="10" y1="62" x2="{W-10}" y2="62" stroke="{t["chrome"]}" stroke-opacity=".3"/>',
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="none" stroke="{t["chrome"]}" stroke-opacity=".6"/>',
        f'<text x="{px+14}" y="{py-10}" font-size="13" fill="{t["chrome"]}">VISUAL.MAP</text>',
        f'<g fill="{t["portrait"]}" shape-rendering="crispEdges"><path d="{path}">'
        '<animate attributeName="opacity" values="0;1;1" keyTimes="0;0.2;1" dur="3.2s" fill="freeze"/></path></g>',
        f'<text x="{px+pw/2}" y="{py+ph-24}" text-anchor="middle" font-size="16" fill="{t["portrait"]}">&lt;/&gt; dipto0079</text>',
        f'<text x="{rx}" y="{py-10}" font-size="13" fill="{t["chrome"]}">SYSTEM.INFO</text>',
        f'<rect x="{rx+rw-210}" y="{py-26}" width="64" height="22" rx="4" fill="#EF4444"/>',
        f'<text x="{rx+rw-178}" y="{py-10}" text-anchor="middle" font-size="12" fill="#fff">● LIVE<animate attributeName="opacity" values="1;.35;1" dur="1.6s" repeatCount="indefinite"/></text>',
        f'<rect x="{rx+rw-136}" y="{py-28}" width="136" height="26" rx="13" fill="{t["chrome"]}"/>',
        f'<text x="{rx+rw-68}" y="{py-10}" text-anchor="middle" font-size="14" fill="{t["bg"]}">@dipto0079</text>']
    y = py + 24
    cw = 8.4  # approx mono char width at 14px
    for r in ROWS:
        if r is None: y += 12; continue
        k, v = r
        vw = len(v)*cw; kw = len(k)*cw
        out.append(f'<text x="{rx}" y="{y}" font-size="14" fill="{t["label"]}" textLength="{kw:.0f}" lengthAdjust="spacingAndGlyphs">{k}</text>')
        n = int((rw - kw - vw - 16) / cw)
        out.append(f'<text x="{rx+kw+8:.0f}" y="{y}" font-size="14" fill="{t["leader"]}">{"·"*max(n,3)}</text>')
        out.append(f'<text x="{rx+rw-vw:.0f}" y="{y}" font-size="14" fill="{t["value"]}" textLength="{vw:.0f}" lengthAdjust="spacingAndGlyphs">{v.replace("&","&amp;")}</text>')
        y += 23
    out.append('</svg>')
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, f"{name}.svg"), "w", encoding="utf-8") as f: f.write("\n".join(out))

for n, t in THEMES.items(): build(n, t)
print("ok")
