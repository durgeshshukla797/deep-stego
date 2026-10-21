"""
Monochrome Vector Assets & SVG Icon Library for Deep-Stego.
Strictly black, white, and neutral grayscale (#000000, #FFFFFF, #111111, #333333, #666666, #999999).
Lightweight, scalable, zero emojis.
"""

def _clean(raw: str) -> str:
    """Strips leading and trailing spaces per line to prevent Markdown code block triggers."""
    return "".join(line.strip() for line in raw.strip().splitlines())

# ── Core SVG Icons ─────────────────────────────────────────────────────────────
ICONS = {
    "shield": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
</svg>""",
    
    "lock": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
<path d="M7 11V7a5 5 0 0 1 10 0v4"/>
</svg>""",
    
    "unlock": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
<path d="M7 11V7a5 5 0 0 1 9.9-1"/>
</svg>""",
    
    "key": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<path d="M21 2l-2 2m-1.5 1.5L16 7l-1.5-1.5L13 7l-2-2-4 4a5 5 0 1 0 7.07 7.07l4-4 1.5 1.5 1.5-1.5L20 11l2-2-1-7z"/>
<circle cx="7.5" cy="16.5" r="1.5"/>
</svg>""",
    
    "cpu": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<rect x="4" y="4" width="16" height="16" rx="2"/>
<rect x="9" y="9" width="6" height="6"/>
<path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/>
</svg>""",
    
    "neural": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<circle cx="6" cy="6" r="2.5"/>
<circle cx="6" cy="18" r="2.5"/>
<circle cx="18" cy="6" r="2.5"/>
<circle cx="18" cy="18" r="2.5"/>
<circle cx="12" cy="12" r="2.5"/>
<path d="M8.5 7.5l2 2.5m3 2l2 2.5m-7 0l2-2.5m3-2l2-2.5M6 8.5v7M18 8.5v7"/>
</svg>""",
    
    "mail": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
<polyline points="22,6 12,13 2,6"/>
</svg>""",
    
    "send": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<line x1="22" y1="2" x2="11" y2="13"/>
<polygon points="22 2 15 22 11 13 2 9 22 2"/>
</svg>""",
    
    "search": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<circle cx="11" cy="11" r="8"/>
<line x1="21" y1="21" x2="16.65" y2="16.65"/>
</svg>""",
    
    "refresh": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<polyline points="23 4 23 10 17 10"/>
<polyline points="1 20 1 14 7 14"/>
<path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
</svg>""",
    
    "check": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<polyline points="20 6 9 17 4 12"/>
</svg>""",
    
    "alert": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<circle cx="12" cy="12" r="10"/>
<line x1="12" y1="8" x2="12" y2="12"/>
<line x1="12" y1="16" x2="12.01" y2="16"/>
</svg>""",
    
    "upload": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
<polyline points="17 8 12 3 7 8"/>
<line x1="12" y1="3" x2="12" y2="15"/>
</svg>""",
    
    "download": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
<polyline points="7 10 12 15 17 10"/>
<line x1="12" y1="15" x2="12" y2="3"/>
</svg>""",
    
    "eye": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
<circle cx="12" cy="12" r="3"/>
</svg>""",
    
    "terminal": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<polyline points="4 17 10 11 4 5"/>
<line x1="12" y1="19" x2="20" y2="19"/>
</svg>""",
    
    "layers": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<polygon points="12 2 2 7 12 12 22 7 12 2"/>
<polyline points="2 17 12 22 22 17"/>
<polyline points="2 12 12 17 22 12"/>
</svg>""",
    
    "user": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
<circle cx="12" cy="7" r="4"/>
</svg>""",
    
    "activity": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
</svg>""",
    
    "database": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<ellipse cx="12" cy="5" rx="9" ry="3"/>
<path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
<path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
</svg>""",
    
    "chevron_right": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<polyline points="9 18 15 12 9 6"/>
</svg>""",
    
    "copy": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">
<rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
</svg>"""
}

def svg_icon(name: str, size: int = 16, color: str = "#FFFFFF", stroke_width: float = 1.75) -> str:
    """Returns clean inline SVG markup for the given icon name."""
    template = ICONS.get(name, ICONS["shield"])
    raw = template.format(size=size, color=color, stroke_width=stroke_width)
    return _clean(raw)

# ── Minimalist Geometric Empty State Illustrations ───────────────────────────
def svg_empty_inbox(width: int = 220, height: int = 140) -> str:
    """Geometric vector illustration for an empty transmission inbox."""
    raw = f"""<svg width="{width}" height="{height}" viewBox="0 0 220 140" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto">
<rect x="40" y="25" width="140" height="90" rx="6" stroke="#262626" stroke-width="1.5" stroke-dasharray="4 4"/>
<path d="M40 40L110 82L180 40" stroke="#404040" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="110" cy="70" r="28" stroke="#1F1F1F" stroke-width="1"/>
<circle cx="110" cy="70" r="18" stroke="#333333" stroke-width="1.25"/>
<path d="M104 70H116M110 64V76" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round"/>
<rect x="75" y="102" width="70" height="2" rx="1" fill="#1F1F1F"/>
</svg>"""
    return _clean(raw)

def svg_empty_sent(width: int = 220, height: int = 140) -> str:
    """Geometric vector illustration for empty outbound log."""
    raw = f"""<svg width="{width}" height="{height}" viewBox="0 0 220 140" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto">
<circle cx="110" cy="70" r="45" stroke="#1F1F1F" stroke-width="1" stroke-dasharray="3 3"/>
<circle cx="110" cy="70" r="30" stroke="#262626" stroke-width="1.25"/>
<circle cx="110" cy="70" r="15" stroke="#404040" stroke-width="1.5"/>
<circle cx="110" cy="70" r="3" fill="#FFFFFF"/>
<path d="M110 25V35M110 105V115M65 70H75M145 70H155" stroke="#333333" stroke-width="1.5" stroke-linecap="round"/>
<path d="M110 70L135 45" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round"/>
<polygon points="135,45 130,46 134,50" fill="#FFFFFF"/>
</svg>"""
    return _clean(raw)

def svg_empty_search(width: int = 180, height: int = 120) -> str:
    """Geometric vector viewfinder for search queries."""
    raw = f"""<svg width="{width}" height="{height}" viewBox="0 0 180 120" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto">
<circle cx="85" cy="55" r="28" stroke="#333333" stroke-width="1.5"/>
<line x1="105" y1="75" x2="135" y2="105" stroke="#666666" stroke-width="2" stroke-linecap="round"/>
<path d="M70 55H100M85 40V70" stroke="#1F1F1F" stroke-width="1.25" stroke-linecap="round"/>
<circle cx="85" cy="55" r="8" stroke="#555555" stroke-width="1" stroke-dasharray="2 2"/>
</svg>"""
    return _clean(raw)

def svg_architecture_diagram() -> str:
    """Detailed vector technical diagram of the Dual U-Net Steganography Pipeline."""
    raw = """<svg width="100%" height="220" viewBox="0 0 840 220" fill="none" xmlns="http://www.w3.org/2000/svg" style="max-width:840px;margin:1rem auto;display:block">
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1 L 8 5 L 0 9 z" fill="#FFFFFF"/>
</marker>
<marker id="arrow-dim" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1 L 8 5 L 0 9 z" fill="#666666"/>
</marker>
</defs>
<rect x="20" y="30" width="130" height="50" rx="6" fill="#0D0D0D" stroke="#262626" stroke-width="1.25"/>
<text x="85" y="52" fill="#FFFFFF" font-family="'JetBrains Mono',monospace" font-size="11" font-weight="600" text-anchor="middle">Cover Image</text>
<text x="85" y="68" fill="#666666" font-family="'Inter',sans-serif" font-size="9" text-anchor="middle">Carrier [3x128x128]</text>
<rect x="20" y="130" width="130" height="50" rx="6" fill="#0D0D0D" stroke="#262626" stroke-width="1.25"/>
<text x="85" y="152" fill="#FFFFFF" font-family="'JetBrains Mono',monospace" font-size="11" font-weight="600" text-anchor="middle">Secret Image</text>
<text x="85" y="168" fill="#666666" font-family="'Inter',sans-serif" font-size="9" text-anchor="middle">Payload [3x128x128]</text>
<path d="M150 55 L200 95" stroke="#666666" stroke-width="1.5" marker-end="url(#arrow-dim)"/>
<path d="M150 155 L200 115" stroke="#666666" stroke-width="1.5" marker-end="url(#arrow-dim)"/>
<rect x="205" y="85" width="80" height="40" rx="4" fill="#141414" stroke="#333333" stroke-width="1.25"/>
<text x="245" y="103" fill="#FFFFFF" font-family="'JetBrains Mono',monospace" font-size="10" font-weight="600" text-anchor="middle">Concat</text>
<text x="245" y="117" fill="#888888" font-family="'JetBrains Mono',monospace" font-size="8" text-anchor="middle">6 Channels</text>
<path d="M285 105 L335 105" stroke="#FFFFFF" stroke-width="1.5" marker-end="url(#arrow)"/>
<rect x="340" y="75" width="130" height="60" rx="6" fill="#0D0D0D" stroke="#FFFFFF" stroke-width="1.5"/>
<text x="405" y="100" fill="#FFFFFF" font-family="'JetBrains Mono',monospace" font-size="12" font-weight="700" text-anchor="middle">Hiding U-Net</text>
<text x="405" y="118" fill="#888888" font-family="'Inter',sans-serif" font-size="9" text-anchor="middle">5-Level Skip Conns</text>
<path d="M470 105 L520 105" stroke="#FFFFFF" stroke-width="1.5" marker-end="url(#arrow)"/>
<rect x="525" y="80" width="115" height="50" rx="6" fill="#141414" stroke="#404040" stroke-width="1.25"/>
<text x="582" y="102" fill="#FFFFFF" font-family="'JetBrains Mono',monospace" font-size="11" font-weight="600" text-anchor="middle">AES-256-GCM</text>
<text x="582" y="118" fill="#888888" font-family="'Inter',sans-serif" font-size="9" text-anchor="middle">PBKDF2 Authenticated</text>
<path d="M640 105 L685 105" stroke="#FFFFFF" stroke-width="1.5" marker-end="url(#arrow)"/>
<rect x="690" y="75" width="130" height="60" rx="6" fill="#0D0D0D" stroke="#FFFFFF" stroke-width="1.5"/>
<text x="755" y="100" fill="#FFFFFF" font-family="'JetBrains Mono',monospace" font-size="12" font-weight="700" text-anchor="middle">Reveal U-Net</text>
<text x="755" y="118" fill="#888888" font-family="'Inter',sans-serif" font-size="9" text-anchor="middle">Inverse Reconstruction</text>
<rect x="340" y="150" width="130" height="20" rx="3" fill="#080808" stroke="#1F1F1F"/>
<text x="405" y="163" fill="#666666" font-family="'JetBrains Mono',monospace" font-size="8" text-anchor="middle">PSNR &gt; 30 dB | SSIM &gt; 0.95</text>
<rect x="690" y="150" width="130" height="20" rx="3" fill="#080808" stroke="#1F1F1F"/>
<text x="755" y="163" fill="#666666" font-family="'JetBrains Mono',monospace" font-size="8" text-anchor="middle">Reconstructed Secret [3ch]</text>
</svg>"""
    return _clean(raw)
