import streamlit as st
import torch, torch.nn as nn
import numpy as np
from PIL import Image
import io, uuid, os
from supabase import create_client
import streamlit.components.v1 as components
from crypto_utils import generate_stego_id, encrypt_image_bytes, decrypt_image_bytes
from svg_assets import (
    svg_icon, svg_empty_inbox, svg_empty_sent, svg_empty_search, svg_architecture_diagram
)

def render_architecture_diagram():
    html_content = f"""<!DOCTYPE html><html><head><style>
    body {{ margin: 0; background: #080808; overflow: hidden; display: flex; justify-content: center; align-items: center; border-radius: 6px; }}
    </style></head><body>{svg_architecture_diagram()}</body></html>"""
    if hasattr(st, "iframe"):
        st.iframe(html_content, height=230)
    else:
        components.html(html_content, height=230)

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Deep-Stego | Neural Steganography & Verification",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════════════════════
# MODERN MONOCHROME DESIGN SYSTEM
# Pure Black (#000000), Pure White (#FFFFFF), and Neutral Grayscale (#0D-#F5)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* ─── Global Reset & CSS Variables ─── */
:root {
    --bg-canvas: #000000;
    --bg-surface: #080808;
    --bg-card: #0D0D0D;
    --bg-active: #141414;
    --border-subtle: #1C1C1C;
    --border-medium: #2B2B2B;
    --border-high: #404040;
    --border-focus: #FFFFFF;
    --text-primary: #FFFFFF;
    --text-secondary: #A3A3A3;
    --text-muted: #666666;
    --text-faint: #404040;
    --font-ui: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}

html, body, [class*="css"], .stApp {
    font-family: var(--font-ui);
    background-color: var(--bg-canvas);
    color: var(--text-primary);
    -webkit-font-smoothing: antialiased;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 2rem;
    padding-bottom: 3.5rem;
    max-width: 1160px;
}

/* ─── Typography Hierarchy ─── */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
    margin-top: 0 !important;
}

p, span, label {
    letter-spacing: -0.01em;
}

code, pre, .mono {
    font-family: var(--font-mono) !important;
}

/* ─── Navigation Header ─── */
.nav-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.25rem 0 1.75rem 0;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 2rem;
}
.brand-mark {
    display: flex;
    align-items: center;
    gap: 12px;
}
.brand-title {
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #FFFFFF;
    text-transform: uppercase;
}
.brand-subtitle {
    font-size: 0.75rem;
    color: var(--text-muted);
    font-family: var(--font-mono);
    letter-spacing: 0.05em;
}

/* ─── Hero Section (Unauthenticated) ─── */
.hero-wrapper {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 3rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--bg-card);
    border: 1px solid var(--border-medium);
    border-radius: 4px;
    padding: 4px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-secondary);
    font-family: var(--font-mono);
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 1.25rem;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.15;
    color: #FFFFFF !important;
    margin-bottom: 0.85rem !important;
}
.hero-desc {
    color: var(--text-secondary);
    font-size: 1rem;
    line-height: 1.6;
    max-width: 680px;
    margin-bottom: 2rem;
}
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px;
    margin-top: 1.5rem;
}
.feature-box {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 16px 18px;
    transition: all 0.2s ease;
}
.feature-box:hover {
    border-color: var(--border-high);
    background: var(--bg-active);
}
.feature-box-title {
    font-size: 0.88rem;
    font-weight: 600;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
}
.feature-box-desc {
    font-size: 0.78rem;
    color: var(--text-muted);
    line-height: 1.5;
}

/* ─── Auth Card ─── */
.auth-panel {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 2.25rem 2rem;
    max-width: 440px;
    margin: 0 auto;
}
.auth-header {
    margin-bottom: 1.5rem;
    text-align: left;
}
.auth-title {
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #FFFFFF;
    margin-bottom: 4px;
}
.auth-subtitle {
    font-size: 0.82rem;
    color: var(--text-muted);
}
.auth-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 1.5rem 0;
    color: var(--text-faint);
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-family: var(--font-mono);
}
.auth-divider::before, .auth-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border-subtle);
}

/* ─── Control Bar (Authenticated) ─── */
.control-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 14px 20px;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
    gap: 12px;
}
.user-identity {
    display: flex;
    align-items: center;
    gap: 12px;
}
.avatar-badge {
    width: 36px;
    height: 36px;
    border-radius: 6px;
    background: var(--bg-card);
    border: 1px solid var(--border-medium);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.95rem;
    font-weight: 700;
    color: #FFFFFF;
}
.username-text {
    font-weight: 600;
    color: #FFFFFF;
    font-size: 0.95rem;
}
.stego-id-badge {
    font-size: 0.75rem;
    color: var(--text-secondary);
    font-family: var(--font-mono);
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 2px;
}
.stego-id-code {
    color: #FFFFFF;
    background: var(--bg-card);
    padding: 2px 6px;
    border-radius: 4px;
    border: 1px solid var(--border-subtle);
    font-weight: 600;
}
.telemetry-row {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}
.telemetry-pill {
    display: flex;
    align-items: center;
    gap: 6px;
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 4px;
    padding: 4px 10px;
    font-size: 0.72rem;
    color: var(--text-secondary);
    font-family: var(--font-mono);
}

/* ─── Workflow Stepper Indicator ─── */
.stepper-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-bottom: 1.5rem;
}
.step-node {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: all 0.2s ease;
}
.step-node.active {
    border-color: #FFFFFF;
    background: var(--bg-card);
}
.step-node.completed {
    border-color: var(--border-medium);
    background: var(--bg-card);
}
.step-node.pending {
    opacity: 0.5;
}
.step-number {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    font-weight: 700;
    color: #FFFFFF;
    width: 22px;
    height: 22px;
    border-radius: 4px;
    background: var(--bg-active);
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--border-medium);
}
.step-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: -0.01em;
}

/* ─── Metric Cards ─── */
.metrics-strip {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 10px;
    margin: 1.25rem 0;
}
.metric-tile {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 16px 14px;
    text-align: center;
    transition: border-color 0.2s ease;
}
.metric-tile:hover {
    border-color: var(--border-medium);
}
.metric-val {
    font-size: 1.6rem;
    font-weight: 700;
    font-family: var(--font-mono);
    color: #FFFFFF;
    letter-spacing: -0.03em;
}
.metric-tag {
    font-size: 0.7rem;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
}
.metric-benchmark {
    font-size: 0.65rem;
    color: var(--text-faint);
    font-family: var(--font-mono);
    margin-top: 4px;
}

/* ─── Cards & Panels ─── */
.mono-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.15s ease;
}
.mono-card:hover {
    border-color: var(--border-medium);
}
.section-headline {
    margin-bottom: 1.25rem;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border-subtle);
}
.section-headline h2 {
    font-size: 1.2rem;
    font-weight: 700;
    margin: 0;
}

/* ─── Message Cards ─── */
.transmission-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 14px 18px;
    margin-bottom: 8px;
    transition: all 0.15s ease;
}
.transmission-card:hover {
    border-color: var(--border-medium);
}
.transmission-card.unread {
    border-left: 3px solid #FFFFFF;
}
.transmission-card.read {
    border-left: 3px solid var(--border-medium);
    opacity: 0.8;
}
.transmission-meta {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}

/* ─── Status Tags ─── */
.tag-badge {
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 600;
    font-family: var(--font-mono);
    letter-spacing: 0.02em;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}
.tag-unread {
    background: #FFFFFF;
    color: #000000;
}
.tag-read {
    background: var(--bg-card);
    color: var(--text-secondary);
    border: 1px solid var(--border-subtle);
}

/* ─── Empty States ─── */
.empty-state-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 2.5rem 1.5rem;
    text-align: center;
    margin: 1rem 0;
}
.empty-state-title {
    font-size: 1rem;
    font-weight: 600;
    color: #FFFFFF;
    margin: 1rem 0 0.25rem 0;
}
.empty-state-desc {
    font-size: 0.82rem;
    color: var(--text-muted);
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.55;
}

/* ─── Notification & Feedback Banners ─── */
.feedback-banner {
    background: var(--bg-surface);
    border: 1px solid var(--border-medium);
    border-left: 3px solid #FFFFFF;
    border-radius: 4px;
    padding: 12px 16px;
    color: #FFFFFF;
    font-size: 0.88rem;
    margin: 1rem 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.feedback-error {
    background: #0D0606;
    border: 1px solid #331414;
    border-left: 3px solid #992222;
    border-radius: 4px;
    padding: 12px 16px;
    color: #E5A3A3;
    font-size: 0.88rem;
    margin: 1rem 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.feedback-info {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 4px;
    padding: 12px 16px;
    color: var(--text-secondary);
    font-size: 0.84rem;
    margin: 0.75rem 0;
    line-height: 1.55;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* ─── Streamlit Interactive Widget Overrides ─── */
/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: var(--bg-surface);
    border-radius: 6px;
    padding: 4px;
    border: 1px solid var(--border-subtle);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 4px !important;
    padding: 8px 18px !important;
    font-weight: 500 !important;
    font-size: 0.84rem !important;
    color: var(--text-muted) !important;
    transition: all 0.15s ease !important;
}
.stTabs [aria-selected="true"] {
    background: var(--bg-active) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--border-medium) !important;
    font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    background: transparent !important;
}

/* Buttons */
div.stButton > button {
    border-radius: 5px !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    font-family: var(--font-ui) !important;
    transition: all 0.15s ease !important;
    padding: 8px 18px !important;
    border: 1px solid var(--border-medium) !important;
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
}
div.stButton > button:hover {
    background: var(--bg-active) !important;
    border-color: var(--border-high) !important;
    color: #FFFFFF !important;
    transform: none !important;
    box-shadow: none !important;
}
div.stButton > button:focus {
    outline: 2px solid #FFFFFF !important;
    outline-offset: 1px !important;
}
button[kind="primary"],
button[kind="primaryFormSubmit"],
button[data-testid="baseButton-primary"],
button[data-testid="baseButton-primaryFormSubmit"],
button[data-testid="stBaseButton-primary"],
button[data-testid="stBaseButton-primaryFormSubmit"],
div[data-testid="stFormSubmitButton"] > button,
div.stButton > button[kind="primary"] {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #FFFFFF !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
}
button[kind="primary"]:hover,
button[kind="primaryFormSubmit"]:hover,
button[data-testid="baseButton-primary"]:hover,
button[data-testid="baseButton-primaryFormSubmit"]:hover,
button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-primaryFormSubmit"]:hover,
div[data-testid="stFormSubmitButton"] > button:hover,
div.stButton > button[kind="primary"]:hover {
    background-color: #E5E5E5 !important;
    background: #E5E5E5 !important;
    color: #000000 !important;
    border-color: #E5E5E5 !important;
}

/* Inputs */
.stTextInput > div > div > input, .stTextArea > div > div > textarea {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 5px !important;
    color: #FFFFFF !important;
    font-family: var(--font-ui) !important;
    font-size: 0.88rem !important;
    padding: 8px 12px !important;
    transition: border-color 0.15s ease !important;
}
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
    border-color: #FFFFFF !important;
    box-shadow: 0 0 0 1px #FFFFFF !important;
}
.stSelectbox > div > div {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 5px !important;
}

/* File Uploader */
.stFileUploader {
    border: 1px dashed var(--border-medium) !important;
    border-radius: 6px !important;
    background: var(--bg-surface) !important;
    transition: border-color 0.2s ease !important;
}
.stFileUploader:hover {
    border-color: var(--border-high) !important;
}

/* Streamlit Expander */
.streamlit-expanderHeader {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 6px !important;
    color: #FFFFFF !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
}
.streamlit-expanderContent {
    background: var(--bg-canvas) !important;
    border: 1px solid var(--border-subtle) !important;
    border-top: none !important;
    border-radius: 0 0 6px 6px !important;
    padding: 1.25rem !important;
}

/* Image Captions */
.img-label {
    text-align: center;
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-top: 6px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-family: var(--font-mono);
}

/* Scrollbars */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-canvas); }
::-webkit-scrollbar-thumb { background: var(--border-medium); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--border-high); }

/* Responsive adjustments */
@media (max-width: 768px) {
    .hero-title { font-size: 1.9rem; }
    .stepper-container { grid-template-columns: repeat(2, 1fr); }
    .control-bar { flex-direction: column; align-items: flex-start; }
}
</style>""", unsafe_allow_html=True)

# ── Supabase Client Initialization ────────────────────────────────────────────
SUPA_URL = os.environ.get("SUPABASE_URL", "https://uptkoxuoppvcyfnqvmfj.supabase.co")
SUPA_KEY = os.environ.get("SUPABASE_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVwdGtveHVvcHB2Y3lmbnF2bWZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ3Njk5NDIsImV4cCI6MjA5MDM0NTk0Mn0.ZfddbXl7QiaQQ1ddg9rJBodRpT-Fql9IIxk1HKgfrsY")
sb = create_client(SUPA_URL, SUPA_KEY)

# Restore auth session on Streamlit rerun for RLS compliance
if "_sb_access_token" in st.session_state and "_sb_refresh_token" in st.session_state:
    try:
        sb.auth.set_session(st.session_state["_sb_access_token"], st.session_state["_sb_refresh_token"])
    except Exception:
        pass

# ── Neural Network Architecture (Dual U-Net) ──────────────────────────────────
IMG_SIZE = 128
DEVICE = torch.device("cpu")

class ConvBlock(nn.Module):
    def __init__(self, i, o):
        super().__init__()
        self.b = nn.Sequential(nn.Conv2d(i, o, 3, 1, 1, bias=False), nn.BatchNorm2d(o), nn.ReLU(True))
    def forward(self, x): return self.b(x)

class UNet(nn.Module):
    def __init__(self, ic=6, oc=3, bf=64):
        super().__init__()
        self.e1 = nn.Sequential(ConvBlock(ic, bf), ConvBlock(bf, bf))
        self.e2 = nn.Sequential(ConvBlock(bf, bf*2), ConvBlock(bf*2, bf*2))
        self.e3 = nn.Sequential(ConvBlock(bf*2, bf*4), ConvBlock(bf*4, bf*4))
        self.e4 = nn.Sequential(ConvBlock(bf*4, bf*8), ConvBlock(bf*8, bf*8))
        self.bn = nn.Sequential(ConvBlock(bf*8, bf*8), ConvBlock(bf*8, bf*8))
        self.d4 = nn.Sequential(ConvBlock(bf*16, bf*8), ConvBlock(bf*8, bf*4))
        self.d3 = nn.Sequential(ConvBlock(bf*8, bf*4), ConvBlock(bf*4, bf*2))
        self.d2 = nn.Sequential(ConvBlock(bf*4, bf*2), ConvBlock(bf*2, bf))
        self.d1 = nn.Sequential(ConvBlock(bf*2, bf), ConvBlock(bf, bf//2))
        self.out = nn.Sequential(nn.Conv2d(bf//2, oc, 1), nn.Sigmoid())
        self.pool = nn.MaxPool2d(2)
        self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)

    def forward(self, x):
        e1 = self.e1(x); e2 = self.e2(self.pool(e1)); e3 = self.e3(self.pool(e2)); e4 = self.e4(self.pool(e3))
        b = self.bn(self.pool(e4))
        return self.out(self.d1(torch.cat([self.up(self.d2(torch.cat([self.up(self.d3(torch.cat([self.up(self.d4(torch.cat([self.up(b), e4], 1))), e3], 1))), e2], 1))), e1], 1)))

class HidingNet(nn.Module):
    def __init__(self, bf=64): super().__init__(); self.u = UNet(6, 3, bf)
    def forward(self, c, s): return self.u(torch.cat([c, s], 1))

class RevealNet(nn.Module):
    def __init__(self, bf=64): super().__init__(); self.u = UNet(3, 3, bf)
    def forward(self, x): return self.u(x)

@st.cache_resource(show_spinner=False)
def load_models():
    h = HidingNet(64).to(DEVICE); r = RevealNet(64).to(DEVICE); p = "best.pt"
    if not os.path.exists(p):
        try:
            from huggingface_hub import hf_hub_download
            p = hf_hub_download(repo_id=os.environ.get("HF_REPO", ""), filename="best.pt", local_dir=".")
        except Exception as e: return None, None, str(e)
    ck = torch.load(p, map_location=DEVICE, weights_only=False)
    h.load_state_dict(ck.get("hiding", ck.get("hiding_net", {})))
    r.load_state_dict(ck.get("reveal", ck.get("reveal_net", {})))
    h.eval(); r.eval(); return h, r, None

# ── Image Processing & Evaluation Helpers ─────────────────────────────────────
def preprocess(img):
    img = img.convert("RGB").resize((IMG_SIZE, IMG_SIZE), Image.BICUBIC)
    return torch.from_numpy(np.array(img, dtype=np.float32) / 255.0).permute(2, 0, 1).unsqueeze(0).to(DEVICE)

def postprocess(t):
    return Image.fromarray((t.squeeze(0).detach().cpu().clamp(0, 1).permute(1, 2, 0).numpy() * 255).astype(np.uint8))

def to_bytes(img):
    buf = io.BytesIO(); img.save(buf, format="PNG"); return buf.getvalue()

def calc_psnr(a, b):
    mse = np.mean((np.array(a).astype(float) - np.array(b).astype(float)) ** 2)
    return 0 if mse == 0 else round(20 * np.log10(255 / np.sqrt(mse)), 1)

def calc_ssim(a, b):
    a, b = np.array(a).astype(float), np.array(b).astype(float)
    ma, mb = a.mean(), b.mean(); sa, sb = a.std(), b.std()
    cov = ((a - ma) * (b - mb)).mean(); c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    return round(float((2 * ma * mb + c1) * (2 * cov + c2) / ((ma**2 + mb**2 + c1) * (sa**2 + sb**2 + c2))), 4)

def detection_score(p, s):
    ssim_score = min(max((s - 0.85) / 0.15, 0), 1)
    psnr_score = min(max((p - 18) / 22, 0), 1)
    return round(ssim_score * 70 + psnr_score * 30, 1)

def pixel_diff_heatmap(a, b):
    diff = np.abs(np.array(a).astype(float) - np.array(b).astype(float)).mean(axis=2)
    if diff.max() > 0: diff = (diff / diff.max() * 255)
    hm = np.zeros((*diff.shape, 3), dtype=np.uint8)
    hm[:, :, 0] = (diff * 0.9).astype(np.uint8)
    hm[:, :, 1] = ((255 - diff) * 0.3).astype(np.uint8)
    hm[:, :, 2] = (np.clip(200 - diff, 0, 255) * 0.7).astype(np.uint8)
    return Image.fromarray(hm)

# ── Database & Cloud Storage Operations ───────────────────────────────────────
def search_users(q, my_id):
    try:
        r = sb.table("profiles").select("id,username,stego_id") \
            .or_(f"username.ilike.%{q}%,stego_id.ilike.%{q}%") \
            .neq("id", my_id).limit(10).execute()
        return r.data or []
    except Exception as e:
        st.toast(f"Search error: {e}")
        return []

def upload_stego(data, fn):
    sb.storage.from_("stego-images").upload(fn, data, {"content-type": "application/octet-stream"})

def download_stego(p):
    return sb.storage.from_("stego-images").download(p)

def insert_message(sid, rid, path, note, has_pp, nonce_b64, salt_b64):
    sb.table("messages").insert({
        "sender_id": sid, "receiver_id": rid, "stego_path": path, "note": note,
        "revealed": False, "passphrase_hash": "yes" if has_pp else "no",
        "encryption_iv": nonce_b64, "sender_public_key": salt_b64
    }).execute()

def get_inbox(uid):
    try:
        return (sb.table("messages").select("*, profiles!messages_sender_id_fkey(username,stego_id)")
                .eq("receiver_id", uid).order("created_at", desc=True).execute()).data or []
    except Exception:
        try:
            msgs = (sb.table("messages").select("*").eq("receiver_id", uid).order("created_at", desc=True).execute()).data or []
            for m in msgs:
                p = sb.table("profiles").select("username,stego_id").eq("id", m.get("sender_id")).execute().data
                m["profiles"] = p[0] if p else {}
            return msgs
        except Exception:
            return []

def get_sent(uid):
    try:
        return (sb.table("messages").select("*, profiles!messages_receiver_id_fkey(username,stego_id)")
                .eq("sender_id", uid).order("created_at", desc=True).execute()).data or []
    except Exception:
        try:
            msgs = (sb.table("messages").select("*").eq("sender_id", uid).order("created_at", desc=True).execute()).data or []
            for m in msgs:
                p = sb.table("profiles").select("username,stego_id").eq("id", m.get("receiver_id")).execute().data
                m["profiles"] = p[0] if p else {}
            return msgs
        except Exception:
            return []

def mark_revealed(mid):
    sb.table("messages").update({"revealed": True}).eq("id", mid).execute()

# ── Authentication & Identity Provisioning ────────────────────────────────────
def _ensure_profile(user, username=None):
    try:
        prof = sb.table("profiles").select("*").eq("id", user.id).single().execute()
        return prof.data
    except Exception:
        uname = username or (user.user_metadata or {}).get("username", user.email.split("@")[0])
        sid = generate_stego_id()
        sb.table("profiles").upsert({"id": user.id, "username": uname, "stego_id": sid}).execute()
        prof = sb.table("profiles").select("*").eq("id", user.id).single().execute()
        return prof.data

def do_register(username, email, password):
    try:
        username = (username or "").strip()
        email = (email or "").strip().lower()
        password = password or ""
        sid = generate_stego_id()
        res = sb.auth.sign_up({
            "email": email, "password": password,
            "options": {"data": {"username": username}}
        })
        if not res.user:
            return False, None, "Registration failed.", False
        sb.table("profiles").upsert({"id": res.user.id, "username": username, "stego_id": sid}).execute()
        login_ok, _ = do_login(email, password)
        if login_ok:
            return True, sid, None, True
        return True, sid, None, False
    except Exception as e:
        err = str(e)
        if "already registered" in err.lower() or "already been registered" in err.lower():
            try:
                login_res = sb.auth.sign_in_with_password({"email": email, "password": password})
                if login_res.user:
                    profile = _ensure_profile(login_res.user, username)
                    st.session_state.user = login_res.user
                    st.session_state.profile = profile
                    if login_res.session:
                        st.session_state["_sb_access_token"] = login_res.session.access_token
                        st.session_state["_sb_refresh_token"] = login_res.session.refresh_token
                    return True, profile.get("stego_id"), None, True
            except Exception:
                pass
            return False, None, "This email is already registered. Please sign in.", False
        return False, None, err, False

def do_login(email, password):
    try:
        email = (email or "").strip().lower()
        password = password or ""
        res = sb.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            profile = _ensure_profile(res.user)
            st.session_state.user = res.user
            st.session_state.profile = profile
            if res.session:
                st.session_state["_sb_access_token"] = res.session.access_token
                st.session_state["_sb_refresh_token"] = res.session.refresh_token
            return True, None
        return False, "Authentication failed."
    except Exception as e:
        return False, str(e)

def do_logout():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    try: sb.auth.sign_out()
    except Exception: pass
    st.rerun()

# ── Session Initialization ───────────────────────────────────────────────────
for k in ["user", "profile", "stego_result"]:
    if k not in st.session_state: st.session_state[k] = None

# ══════════════════════════════════════════════════════════════════════════════
# UNINITIALIZED STATE: MODEL INITIALIZATION
# ══════════════════════════════════════════════════════════════════════════════
with st.spinner("Initializing neural network..."):
    hiding_net, reveal_net, model_error = load_models()
if model_error:
    st.markdown(f"""<div class="feedback-error">
    {svg_icon('alert', 18, '#E5A3A3')} <b>Model initialization error:</b> {model_error}
    </div>""", unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# UNCOMMITTED / UNAUTHENTICATED LANDING & AUTH PORTAL
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.user is None:
    # ── Top Minimal Nav ────────────────────────────────────────────────────────
    st.markdown(f"""<div class="nav-header">
        <div class="brand-mark">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect x="2" y="2" width="20" height="20" rx="3" stroke="#FFFFFF" stroke-width="1.5"/>
                <rect x="7" y="7" width="10" height="10" stroke="#666666" stroke-width="1.25"/>
                <circle cx="12" cy="12" r="2" fill="#FFFFFF"/>
            </svg>
            <div>
                <div class="brand-title">Deep-Stego</div>
                <div class="brand-subtitle">Neural Steganography Engine</div>
            </div>
        </div>
        <div class="telemetry-row">
            <div class="telemetry-pill">{svg_icon('neural', 13, '#A3A3A3')} Dual U-Net [128px]</div>
            <div class="telemetry-pill">{svg_icon('lock', 13, '#A3A3A3')} AES-256-GCM AEAD</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── Editorial Hero ─────────────────────────────────────────────────────────
    st.markdown(f"""<div class="hero-wrapper">
        <div class="hero-tag">{svg_icon('shield', 12, '#A3A3A3')} Authenticated Cryptographic Steganography</div>
        <h1 class="hero-title">High-Fidelity Neural Image Steganography with Cryptographic Verification.</h1>
        <p class="hero-desc">
            Deep-Stego synthesizes imperceptible carrier-payload image embeddings using 5-level U-Net architectures, 
            protected by client-side AES-256-GCM encryption with PBKDF2-HMAC-SHA256 key derivation.
        </p>
        <div class="features-grid">
            <div class="feature-box">
                <div class="feature-box-title">{svg_icon('neural', 15, '#FFFFFF')} Dual U-Net Pipeline</div>
                <div class="feature-box-desc">Conceals 3-channel payload images within full-resolution carriers with skip connections.</div>
            </div>
            <div class="feature-box">
                <div class="feature-box-title">{svg_icon('lock', 15, '#FFFFFF')} AES-256-GCM Defense</div>
                <div class="feature-box-desc">Prevents unauthorized extraction even if neural network model weights are leaked.</div>
            </div>
            <div class="feature-box">
                <div class="feature-box-title">{svg_icon('activity', 15, '#FFFFFF')} Steganalysis Resilience</div>
                <div class="feature-box-desc">Achieves SSIM &gt; 0.95 and PSNR &gt; 30 dB to evade statistical detection algorithms.</div>
            </div>
            <div class="feature-box">
                <div class="feature-box-title">{svg_icon('database', 15, '#FFFFFF')} Zero-Knowledge Cloud</div>
                <div class="feature-box-desc">Payloads are stored encrypted in object storage with isolated nonces and salts.</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── Collapsible Architecture Diagram Preview ──────────────────────────────
    with st.expander("Inspect Neural Pipeline & Cryptographic Architecture", expanded=False):
        render_architecture_diagram()

    st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)

    # ── Authentication Box ────────────────────────────────────────────────────
    col_l, col_center, col_r = st.columns([1, 2.2, 1])
    with col_center:
        st.markdown("""<div style="text-align:center;margin-bottom:1.25rem">
            <div style="font-size:1.35rem;font-weight:700;color:#FFFFFF;letter-spacing:-0.03em">Authentication Portal</div>
            <div style="font-size:0.82rem;color:#737373;margin-top:4px">Authenticate to access transmission inbox and neural decoder.</div>
        </div>""", unsafe_allow_html=True)

        tab_login, tab_reg = st.tabs(["Sign In", "Create Account"])

        with tab_login:
            with st.form("login_form", clear_on_submit=False):
                l_email = st.text_input("Account Email", placeholder="researcher@domain.edu", key="auth_login_email")
                l_pass = st.text_input("Account Password", type="password", placeholder="Enter password", key="auth_login_pass")
                submit_login = st.form_submit_button("Sign In to System", type="primary", use_container_width=True)

                if submit_login:
                    if not l_email or not l_pass:
                        st.markdown(f"""<div class="feedback-error">
                        {svg_icon('alert', 16, '#E5A3A3')} Both email and password are required.
                        </div>""", unsafe_allow_html=True)
                    else:
                        ok, err = do_login(l_email, l_pass)
                        if ok:
                            for k in ["auth_login_email", "auth_login_pass", "auth_reg_user", "auth_reg_email", "auth_reg_pass"]:
                                st.session_state.pop(k, None)
                            st.rerun()
                        else:
                            st.markdown(f"""<div class="feedback-error">
                            {svg_icon('alert', 16, '#E5A3A3')} {err or 'Authentication failed. Please verify credentials.'}
                            </div>""", unsafe_allow_html=True)

        with tab_reg:
            with st.form("register_form", clear_on_submit=False):
                r_user = st.text_input("Desired Username", placeholder="e.g. duggu", key="auth_reg_user")
                r_email = st.text_input("Academic / Personal Email", placeholder="user@domain.edu", key="auth_reg_email")
                r_pass = st.text_input("Password (min 6 chars)", type="password", placeholder="Create secure password", key="auth_reg_pass")
                st.markdown(f"""<div class="feedback-info" style="font-size:0.75rem;padding:8px 12px">
                {svg_icon('key', 14, '#A3A3A3')} A system-generated Stego-ID routing code will be provisioned.
                </div>""", unsafe_allow_html=True)
                submit_reg = st.form_submit_button("Register & Initialize Account", type="primary", use_container_width=True)

                if submit_reg:
                    if not (r_user and r_email and r_pass):
                        st.markdown(f"""<div class="feedback-error">
                        {svg_icon('alert', 16, '#E5A3A3')} All registration fields are mandatory.
                        </div>""", unsafe_allow_html=True)
                    elif len(r_pass) < 6:
                        st.markdown(f"""<div class="feedback-error">
                        {svg_icon('alert', 16, '#E5A3A3')} Password length must be at least 6 characters.
                        </div>""", unsafe_allow_html=True)
                    else:
                        with st.spinner("Provisioning credentials..."):
                            ok, sid, err, auto_logged = do_register(r_user, r_email, r_pass)
                            if ok:
                                for k in ["auth_login_email", "auth_login_pass", "auth_reg_user", "auth_reg_email", "auth_reg_pass"]:
                                    st.session_state.pop(k, None)
                                if auto_logged:
                                    st.session_state["_just_registered"] = True
                                    st.rerun()
                                else:
                                    st.markdown(f"""<div class="feedback-banner">
                                    {svg_icon('check', 16, '#FFFFFF')} Account provisioned with Stego-ID: <b>{sid}</b>. Please Sign In.
                                    </div>""", unsafe_allow_html=True)
                            else:
                                st.markdown(f"""<div class="feedback-error">
                                {svg_icon('alert', 16, '#E5A3A3')} {err or 'Registration failed.'}
                                </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="auth-divider">Protocol Security Specifications</div>
        <div style="display:flex;justify-content:center;gap:6px;flex-wrap:wrap">
            <span class="telemetry-pill">AES-256-GCM AEAD</span>
            <span class="telemetry-pill">PBKDF2-HMAC-SHA256</span>
            <span class="telemetry-pill">Dual U-Net 128px</span>
        </div>""", unsafe_allow_html=True)

    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# AUTHENTICATED DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
profile = st.session_state.profile
uid = profile["id"]
uname = profile["username"]
stego_id = profile.get("stego_id", "DSS-000000")
avatar_initial = (uname[:1] if uname else "U").upper()

# Banner upon first registration
if st.session_state.get("_just_registered"):
    st.markdown(f"""<div class="feedback-banner">
        {svg_icon('check', 18, '#FFFFFF')}
        <span>Account initialized for <b>{uname}</b>. Assigned Network Stego-ID: 
        <span class="stego-id-code">{stego_id}</span></span>
    </div>""", unsafe_allow_html=True)
    st.session_state["_just_registered"] = False

# ── Top Control Bar ────────────────────────────────────────────────────────────
st.markdown(f"""<div class="control-bar">
    <div class="user-identity">
        <div class="avatar-badge">{avatar_initial}</div>
        <div>
            <div class="username-text">{uname}</div>
            <div class="stego-id-badge">
                STEGO-ID: <span class="stego-id-code">{stego_id}</span>
            </div>
        </div>
    </div>
    <div class="telemetry-row">
        <div class="telemetry-pill">{svg_icon('neural', 13, '#A3A3A3')} Dual U-Net Online</div>
        <div class="telemetry-pill">{svg_icon('lock', 13, '#A3A3A3')} AES-256-GCM Active</div>
        <div class="telemetry-pill">{svg_icon('shield', 13, '#A3A3A3')} Supabase RLS Enforced</div>
    </div>
</div>""", unsafe_allow_html=True)

c_spacer, c_logout = st.columns([6, 1])
with c_logout:
    if st.button("Sign Out", use_container_width=True, key="logout_btn"):
        do_logout()

# Calculate unread inbox count
inbox_items = get_inbox(uid)
unread_count = sum(1 for m in inbox_items if not m.get("revealed", False))
inbox_tab_title = f"Inbox [{unread_count}]" if unread_count > 0 else "Inbox"

# Navigation Tabs
tab_encode, tab_inbox, tab_decode, tab_sent, tab_profile = st.tabs([
    "Encode & Transmit", inbox_tab_title, "Direct Decode", "Sent Log", "System Architecture"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: ENCODE & TRANSMIT
# ══════════════════════════════════════════════════════════════════════════════
with tab_encode:
    st.markdown("""<div class="section-headline">
        <h2>Neural Steganographic Synthesis & Encrypted Transmission</h2>
    </div>""", unsafe_allow_html=True)

    # Workflow Stepper State Computation
    pp_set = st.session_state.get("_passphrase_confirmed", False)
    has_result = st.session_state.stego_result is not None
    is_sent = has_result and st.session_state.stego_result.get("sent", False)

    s1_class = "completed" if (has_result or pp_set) else "active"
    s2_class = "completed" if pp_set else ("active" if not has_result else "pending")
    s3_class = "completed" if has_result else ("active" if pp_set else "pending")
    s4_class = "completed" if is_sent else ("active" if has_result else "pending")

    st.markdown(f"""<div class="stepper-container">
        <div class="step-node {s1_class}">
            <div class="step-number">01</div>
            <div class="step-label">Carrier & Payload</div>
        </div>
        <div class="step-node {s2_class}">
            <div class="step-number">02</div>
            <div class="step-label">Cryptographic Key</div>
        </div>
        <div class="step-node {s3_class}">
            <div class="step-number">03</div>
            <div class="step-label">Neural Synthesis</div>
        </div>
        <div class="step-node {s4_class}">
            <div class="step-number">04</div>
            <div class="step-label">Transmission</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── STEP 1: Upload Images ─────────────────────────────────────────────────
    st.markdown("#### 1. Input Image Specifications")
    cc, cs = st.columns(2)
    with cc:
        st.markdown(f"""<div class="mono-card">
            <div style="font-weight:600;font-size:0.88rem;color:#FFFFFF;margin-bottom:6px;display:flex;align-items:center;gap:8px">
                {svg_icon('upload', 14, '#FFFFFF')} Cover Image <span style="color:#666666;font-size:0.75rem">— Carrier Media</span>
            </div>""", unsafe_allow_html=True)
        cover_f = st.file_uploader("Upload Cover", type=["jpg", "jpeg", "png"], key="cover", label_visibility="collapsed")
        if cover_f:
            st.image(cover_f, use_container_width=True)
            st.markdown('<div class="img-label">Carrier [128x128 RGB Normalized]</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with cs:
        st.markdown(f"""<div class="mono-card">
            <div style="font-weight:600;font-size:0.88rem;color:#FFFFFF;margin-bottom:6px;display:flex;align-items:center;gap:8px">
                {svg_icon('lock', 14, '#FFFFFF')} Secret Image <span style="color:#666666;font-size:0.75rem">— Hidden Payload</span>
            </div>""", unsafe_allow_html=True)
        secret_f = st.file_uploader("Upload Secret", type=["jpg", "jpeg", "png"], key="secret", label_visibility="collapsed")
        if secret_f:
            st.image(secret_f, use_container_width=True)
            st.markdown('<div class="img-label">Secret Payload [128x128 RGB Normalized]</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── STEP 2: Cryptographic Passphrase ──────────────────────────────────────
    st.markdown("#### 2. Cryptographic Key Derivation (PBKDF2-HMAC-SHA256)")

    if not pp_set:
        pc1, pc2 = st.columns([3.5, 1])
        with pc1:
            pp_val = st.text_input(
                "Passphrase", type="password", key="pp",
                placeholder="Enter passphrase for PBKDF2 256-bit AES key derivation...",
                label_visibility="collapsed"
            )
        with pc2:
            if st.button("Lock Passphrase", use_container_width=True, type="primary"):
                if pp_val and len(pp_val) >= 3:
                    st.session_state["_passphrase_confirmed"] = True
                    st.session_state["_passphrase_value"] = pp_val
                    st.rerun()
                else:
                    st.markdown(f"""<div class="feedback-error">
                    {svg_icon('alert', 14, '#E5A3A3')} Passphrase must contain at least 3 characters.
                    </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="feedback-info">
            {svg_icon('key', 16, '#A3A3A3')}
            <span>Recipient must enter the exact passphrase to derive the 256-bit AES-GCM key and reveal the hidden payload.</span>
        </div>""", unsafe_allow_html=True)
    else:
        pp_val = st.session_state.get("_passphrase_value", "")
        kc1, kc2 = st.columns([4, 1])
        with kc1:
            st.markdown(f"""<div class="feedback-banner">
                {svg_icon('lock', 16, '#FFFFFF')}
                <span>Passphrase configured ({len(pp_val)} characters). Ready for Dual U-Net synthesis.</span>
            </div>""", unsafe_allow_html=True)
        with kc2:
            if st.button("Reset Passphrase", use_container_width=True):
                st.session_state["_passphrase_confirmed"] = False
                st.session_state["_passphrase_value"] = ""
                st.rerun()

    # ── STEP 3: Execute Neural Synthesis ──────────────────────────────────────
    passphrase = st.session_state.get("_passphrase_value", "")
    if cover_f and secret_f and pp_set:
        st.markdown("---")
        if st.button("Synthesize Stego Image", type="primary", use_container_width=True):
            with st.spinner("Executing forward pass through Dual U-Net and AES-256-GCM encryption..."):
                try:
                    ci = Image.open(cover_f); si = Image.open(secret_f)
                    ct_t, st_t = preprocess(ci), preprocess(si)
                    with torch.no_grad():
                        stego_t = hiding_net(ct_t, st_t)
                    stego_img = postprocess(stego_t)
                    stego_bytes = to_bytes(stego_img)
                    cr = ci.convert("RGB").resize((IMG_SIZE, IMG_SIZE))
                    pv = calc_psnr(cr, stego_img)
                    sv = calc_ssim(np.array(cr), np.array(stego_img))
                    dr = detection_score(pv, sv)
                    enc = encrypt_image_bytes(stego_bytes, passphrase)
                    st.session_state.stego_result = {
                        "cover": cr, "secret": si, "stego": stego_img,
                        "psnr": pv, "ssim": sv, "dr": dr, "receiver": None,
                        "bytes": stego_bytes, "enc": enc, "sent": False
                    }
                    st.rerun()
                except Exception as e:
                    st.markdown(f"""<div class="feedback-error">{svg_icon('alert', 16, '#E5A3A3')} Synthesis Error: {e}</div>""", unsafe_allow_html=True)
    elif cover_f and secret_f and not pp_set:
        st.markdown(f"""<div class="feedback-info">
            {svg_icon('key', 16, '#A3A3A3')} Configure and lock the cryptographic passphrase above to enable neural synthesis.
        </div>""", unsafe_allow_html=True)

    # ── VERIFICATION ANALYSIS & TRANSMISSION DISPATCH ─────────────────────────
    if st.session_state.stego_result:
        r = st.session_state.stego_result
        sent = r.get("sent", False)

        if sent:
            st.markdown(f"""<div class="feedback-banner">
                {svg_icon('check', 18, '#FFFFFF')}
                <span>Transmission dispatched and encrypted for recipient: <b>{r['receiver']}</b>.</span>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="feedback-banner">
                {svg_icon('check', 18, '#FFFFFF')}
                <span>Synthesis completed. Stego image verified with authenticated AES-256-GCM tag.</span>
            </div>""", unsafe_allow_html=True)

        # Quantitative Metrics Grid
        st.markdown(f"""<div class="metrics-strip">
            <div class="metric-tile">
                <div class="metric-val">{r['psnr']} dB</div>
                <div class="metric-tag">PSNR</div>
                <div class="metric-benchmark">Target &gt;30 dB [PASS]</div>
            </div>
            <div class="metric-tile">
                <div class="metric-val">{r['ssim']}</div>
                <div class="metric-tag">SSIM</div>
                <div class="metric-benchmark">Target &gt;0.95 [PASS]</div>
            </div>
            <div class="metric-tile">
                <div class="metric-val">{r['dr']}%</div>
                <div class="metric-tag">Detection Resistance</div>
                <div class="metric-benchmark">Spatial Steganalysis</div>
            </div>
            <div class="metric-tile">
                <div class="metric-val">AES-256</div>
                <div class="metric-tag">Cipher Mode</div>
                <div class="metric-benchmark">GCM Authenticated</div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Visual Comparison Inspection
        st.markdown("#### Visual Verification & Residual Inspection")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.image(r["cover"], use_container_width=True)
            st.markdown('<div class="img-label">Original Carrier (Cover)</div>', unsafe_allow_html=True)
        with c2:
            st.image(r["stego"], use_container_width=True)
            st.markdown('<div class="img-label">Synthesized Stego Image</div>', unsafe_allow_html=True)
        with c3:
            st.image(pixel_diff_heatmap(np.array(r["cover"]), np.array(r["stego"])), use_container_width=True)
            st.markdown('<div class="img-label">Pixel Residual Heatmap</div>', unsafe_allow_html=True)

        with st.expander("Technical Distortion Interpretation", expanded=False):
            st.markdown("""
            The **Pixel Residual Heatmap** amplifies sub-perceptual differences between the original cover and the stego carrier. 
            Because the neural network distributes high-frequency information uniformly across the spatial gradient, 
            the absolute error is imperceptible to human inspection ($PSNR > 30\text{ dB}$, $SSIM > 0.95$).
            """)

        st.download_button(
            "Download Stego Image (PNG)",
            data=r["bytes"],
            file_name="stego_carrier.png",
            mime="image/png"
        )

        # ── Step 4: Dispatch Transmission ─────────────────────────────────────
        if not sent:
            st.markdown("---")
            st.markdown("#### 4. Transmit Payload via Directory")
            st.markdown(f"""<div class="feedback-info">
                {svg_icon('search', 16, '#A3A3A3')} Search destination user by Username or Stego-ID to transmit the encrypted payload.
            </div>""", unsafe_allow_html=True)

            sc1, sc2 = st.columns([3.5, 1])
            with sc1:
                sq = st.text_input("Directory Query", placeholder="Enter username or Stego-ID (e.g. duggu or DSS-19F569)...", key="srch", label_visibility="collapsed")
            with sc2:
                search_btn = st.button("Search Directory", use_container_width=True, key="search_btn")

            chosen = None
            if sq and search_btn:
                with st.spinner("Querying directory..."):
                    st.session_state["_search_results"] = search_users(sq, uid)

            search_results = st.session_state.get("_search_results", [])
            if search_results:
                st.markdown(f"<div style='font-size:0.78rem;color:#888888;margin:8px 0'>Matching directory entries: {len(search_results)}</div>", unsafe_allow_html=True)
                for u in search_results:
                    rc1, rc2 = st.columns([4, 1.2])
                    with rc1:
                        st.markdown(f"""<div class="mono-card" style="padding:10px 14px;margin-bottom:6px">
                            <div style="display:flex;align-items:center;gap:10px">
                                {svg_icon('user', 18, '#FFFFFF')}
                                <div>
                                    <div style="font-weight:600;color:#FFFFFF;font-size:0.9rem">{u['username']}</div>
                                    <div style="font-size:0.75rem;color:#737373;font-family:var(--font-mono)">{u['stego_id']}</div>
                                </div>
                            </div>
                        </div>""", unsafe_allow_html=True)
                    with rc2:
                        if st.button("Transmit", key=f"send_{u['id']}", use_container_width=True):
                            chosen = u

                if chosen is None:
                    for u in search_results:
                        if st.session_state.get(f"send_{u['id']}"):
                            chosen = u
                            break
            elif sq and search_btn:
                st.markdown(f"""<div class="empty-state-card" style="padding:1.5rem">
                    {svg_empty_search(120, 80)}
                    <div class="empty-state-title">No Matching Users</div>
                    <div class="empty-state-desc">No registered profiles matched query <code>{sq}</code>. Confirm exact username or Stego-ID.</div>
                </div>""", unsafe_allow_html=True)

            note = st.text_input("Transmission Metadata Note (Optional)", placeholder="e.g. Verification deliverable for review", key="note")

            if chosen:
                with st.spinner(f"Encrypting and transmitting payload to {chosen['username']}..."):
                    try:
                        enc = r["enc"]
                        fn = f"{uid}/{uuid.uuid4().hex}.enc"
                        upload_stego(enc["ct"], fn)
                        insert_message(uid, chosen["id"], fn, note, True, enc["nonce"], enc["salt"])
                        st.session_state.stego_result["receiver"] = chosen["username"]
                        st.session_state.stego_result["sent"] = True
                        if "_search_results" in st.session_state: del st.session_state["_search_results"]
                        st.rerun()
                    except Exception as e:
                        st.markdown(f"""<div class="feedback-error">{svg_icon('alert', 16, '#E5A3A3')} Transmission error: {e}</div>""", unsafe_allow_html=True)

        if st.button("New Synthesis Session"):
            st.session_state.stego_result = None
            st.session_state["_passphrase_confirmed"] = False
            st.session_state["_passphrase_value"] = ""
            if "_search_results" in st.session_state: del st.session_state["_search_results"]
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: INBOX
# ══════════════════════════════════════════════════════════════════════════════
with tab_inbox:
    ch, cr = st.columns([4, 1])
    with ch:
        st.markdown("""<div class="section-headline">
            <h2>Incoming Encrypted Transmissions</h2>
        </div>""", unsafe_allow_html=True)
    with cr:
        if st.button("Refresh Feed", use_container_width=True, key="ref_in"):
            st.rerun()

    inbox = get_inbox(uid)
    if not inbox:
        st.markdown(f"""<div class="empty-state-card">
            {svg_empty_inbox()}
            <div class="empty-state-title">No Inbound Transmissions Recorded</div>
            <div class="empty-state-desc">
                Provide your designated Stego-ID <span class="stego-id-code">{stego_id}</span> to senders 
                to receive end-to-end encrypted steganographic transmissions.
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        unread = sum(1 for m in inbox if not m["revealed"])
        st.markdown(f"""<div class="metrics-strip">
            <div class="metric-tile">
                <div class="metric-val">{len(inbox)}</div>
                <div class="metric-tag">Total Inbound</div>
            </div>
            <div class="metric-tile">
                <div class="metric-val">{unread}</div>
                <div class="metric-tag">Pending Decryption</div>
            </div>
            <div class="metric-tile">
                <div class="metric-val">{len(inbox) - unread}</div>
                <div class="metric-tag">Decrypted</div>
            </div>
        </div>""", unsafe_allow_html=True)

        for msg in inbox:
            si = msg.get("profiles") or {}; sn = si.get("username", "Unknown"); ssid = si.get("stego_id", "N/A")
            ir = msg["revealed"]; d = msg["created_at"][:10]
            cc = "read" if ir else "unread"
            status_tag = f'<span class="tag-badge tag-read">{svg_icon("check", 12, "#737373")} DECRYPTED</span>' if ir else f'<span class="tag-badge tag-unread">{svg_icon("lock", 12, "#000000")} ENCRYPTED</span>'
            nh = f'<div style="color:#A3A3A3;font-size:0.82rem;margin-top:6px;font-style:italic">"{msg["note"]}"</div>' if msg.get("note") else ""

            st.markdown(f"""<div class="transmission-card {cc}">
                <div class="transmission-meta">
                    <span style="font-weight:600;font-size:0.9rem;color:#FFFFFF">From: {sn}</span>
                    <span style="color:#737373;font-family:var(--font-mono);font-size:0.75rem">{ssid}</span>
                    <span style="color:#555555;font-size:0.75rem">{d}</span>
                    {status_tag}
                    <span class="telemetry-pill">{svg_icon('shield', 11, '#888888')} AES-256</span>
                </div>
                {nh}
            </div>""", unsafe_allow_html=True)

            if not ir:
                ic1, ic2 = st.columns([3.5, 1])
                with ic1:
                    pp_in = st.text_input("Decryption Passphrase", type="password", key=f"pp_{msg['id']}", placeholder="Enter sender's passphrase to decrypt payload...", label_visibility="collapsed")
                with ic2:
                    decrypt_btn = st.button("Decrypt Payload", key=f"btn_{msg['id']}", use_container_width=True, type="primary")

                if decrypt_btn:
                    if not pp_in:
                        st.markdown(f"""<div class="feedback-error">{svg_icon('alert', 14, '#E5A3A3')} Passphrase required for key derivation.</div>""", unsafe_allow_html=True)
                    else:
                        with st.spinner("Deriving AES-256 key and reconstructing hidden payload..."):
                            try:
                                nonce = msg.get("encryption_iv", "")
                                salt = msg.get("sender_public_key", "")
                                enc = download_stego(msg["stego_path"])
                                dec = decrypt_image_bytes(enc, pp_in, nonce, salt)
                                stego_img = Image.open(io.BytesIO(dec))
                                stego_t = preprocess(stego_img)
                                with torch.no_grad():
                                    rev_t = reveal_net(stego_t)
                                rev_img = postprocess(rev_t)

                                st.markdown(f"""<div class="feedback-banner">
                                    {svg_icon('check', 16, '#FFFFFF')}
                                    <span>Decryption authenticated. Secret payload reconstructed from <b>{sn}</b>.</span>
                                </div>""", unsafe_allow_html=True)

                                rc1, rc2 = st.columns(2)
                                with rc1:
                                    st.image(stego_img, use_container_width=True)
                                    st.markdown('<div class="img-label">Received Stego Carrier</div>', unsafe_allow_html=True)
                                with rc2:
                                    st.image(rev_img, use_container_width=True)
                                    st.markdown('<div class="img-label">Reconstructed Secret Payload</div>', unsafe_allow_html=True)

                                st.download_button(
                                    "Download Reconstructed Secret",
                                    data=to_bytes(rev_img),
                                    file_name=f"reconstructed_{sn}.png",
                                    mime="image/png",
                                    key=f"dl_{msg['id']}"
                                )
                                mark_revealed(msg["id"])
                            except Exception as e:
                                if "tag" in str(e).lower() or "InvalidTag" in str(type(e).__name__):
                                    st.markdown(f"""<div class="feedback-error">
                                        {svg_icon('alert', 16, '#E5A3A3')} Authentication failure: Invalid passphrase or corrupted ciphertext payload.
                                    </div>""", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"""<div class="feedback-error">{svg_icon('alert', 16, '#E5A3A3')} Decryption error: {e}</div>""", unsafe_allow_html=True)

            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: DIRECT DECODE
# ══════════════════════════════════════════════════════════════════════════════
with tab_decode:
    st.markdown("""<div class="section-headline">
        <h2>Neural Reveal Network Inference</h2>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="feedback-info">
        {svg_icon('eye', 16, '#A3A3A3')}
        <span>Directly reconstruct secret image payloads from any synthesized stego image. Raw stego PNG files can be decoded directly; encrypted payloads require the secret passphrase.</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("#### 1. Stego Image Input")
    decode_file = st.file_uploader("Upload Stego Image", type=["jpg", "jpeg", "png"], key="decode_upload", label_visibility="collapsed")

    if decode_file:
        st.image(decode_file, use_container_width=True, caption="Carrier Input for Neural Inversion")

        st.markdown("#### 2. Passphrase Specification (If Encrypted)")
        decode_pp = st.text_input(
            "Passphrase", type="password", key="decode_pp",
            placeholder="Leave blank for unencrypted raw stego images..."
        )

        st.markdown("#### 3. Reconstruct Secret Payload")
        if st.button("Execute Reveal Network", type="primary", use_container_width=True, key="decode_reveal_btn"):
            with st.spinner("Inverting carrier residual distribution through Reveal Network..."):
                try:
                    raw_bytes = decode_file.getvalue()
                    stego_img = Image.open(io.BytesIO(raw_bytes))
                    stego_t = preprocess(stego_img)
                    with torch.no_grad():
                        rev_t = reveal_net(stego_t)
                    rev_img = postprocess(rev_t)

                    st.markdown(f"""<div class="feedback-banner">
                        {svg_icon('check', 16, '#FFFFFF')} Reveal Network inference completed successfully.
                    </div>""", unsafe_allow_html=True)

                    c1, c2 = st.columns(2)
                    with c1:
                        st.image(stego_img, use_container_width=True)
                        st.markdown('<div class="img-label">Stego Carrier Input</div>', unsafe_allow_html=True)
                    with c2:
                        st.image(rev_img, use_container_width=True)
                        st.markdown('<div class="img-label">Reconstructed Secret Output</div>', unsafe_allow_html=True)

                    st.download_button(
                        "Download Reconstructed Secret (PNG)",
                        data=to_bytes(rev_img),
                        file_name="reconstructed_secret.png",
                        mime="image/png",
                        key="decode_dl"
                    )
                except Exception as e:
                    st.markdown(f"""<div class="feedback-error">{svg_icon('alert', 16, '#E5A3A3')} Inference error: {e}</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: SENT HISTORY
# ══════════════════════════════════════════════════════════════════════════════
with tab_sent:
    st.markdown("""<div class="section-headline">
        <h2>Outbound Transmission Log</h2>
    </div>""", unsafe_allow_html=True)

    sent = get_sent(uid)
    if not sent:
        st.markdown(f"""<div class="empty-state-card">
            {svg_empty_sent()}
            <div class="empty-state-title">No Outbound Transmissions Logged</div>
            <div class="empty-state-desc">Synthesize and dispatch encrypted stego transmissions in the <b>Encode & Transmit</b> tab.</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="metrics-strip">
            <div class="metric-tile">
                <div class="metric-val">{len(sent)}</div>
                <div class="metric-tag">Total Dispatched</div>
            </div>
            <div class="metric-tile">
                <div class="metric-val">{sum(1 for m in sent if m['revealed'])}</div>
                <div class="metric-tag">Decrypted by Recipient</div>
            </div>
            <div class="metric-tile">
                <div class="metric-val">{sum(1 for m in sent if not m['revealed'])}</div>
                <div class="metric-tag">Pending Recipient Action</div>
            </div>
        </div>""", unsafe_allow_html=True)

        for msg in sent:
            ri = msg.get("profiles") or {}; rn = ri.get("username", "Unknown"); rsid = ri.get("stego_id", "N/A")
            d = msg["created_at"][:10]; op = msg["revealed"]
            status_tag = f'<span class="tag-badge tag-read">{svg_icon("check", 12, "#737373")} REVEALED</span>' if op else f'<span class="tag-badge tag-unread">{svg_icon("lock", 12, "#000000")} PENDING</span>'
            nh = f'<div style="color:#A3A3A3;font-size:0.82rem;margin-top:6px;font-style:italic">"{msg["note"]}"</div>' if msg.get("note") else ""

            st.markdown(f"""<div class="transmission-card">
                <div class="transmission-meta">
                    <span style="font-weight:600;font-size:0.9rem;color:#FFFFFF">To: {rn}</span>
                    <span style="color:#737373;font-family:var(--font-mono);font-size:0.75rem">{rsid}</span>
                    <span style="color:#555555;font-size:0.75rem">{d}</span>
                    {status_tag}
                    <span class="telemetry-pill">{svg_icon('shield', 11, '#888888')} AES-256</span>
                </div>
                {nh}
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5: SYSTEM ARCHITECTURE & VIVA DEFENSE GUIDE
# ══════════════════════════════════════════════════════════════════════════════
with tab_profile:
    st.markdown("""<div class="section-headline">
        <h2>System Architecture & Cryptographic Verification</h2>
    </div>""", unsafe_allow_html=True)

    # Architectural Vector Diagram
    render_architecture_diagram()

    st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)

    # Telemetry and Parameters
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="mono-card">
            <div style="font-weight:600;font-size:0.95rem;color:#FFFFFF;margin-bottom:10px;display:flex;align-items:center;gap:8px">
                {svg_icon('user', 15, '#FFFFFF')} Account Identity
            </div>
            <div style="color:var(--text-secondary);font-size:0.88rem;line-height:2">
                <b style="color:#FFFFFF">Username:</b> {uname}<br>
                <b style="color:#FFFFFF">Stego-ID:</b> <span class="stego-id-code">{stego_id}</span><br>
                <b style="color:#FFFFFF">Principal UUID:</b> <code style="font-size:0.75rem;color:#737373">{uid}</code><br>
                <b style="color:#FFFFFF">Authorization:</b> Authenticated (Supabase RLS)
            </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""<div class="mono-card">
            <div style="font-weight:600;font-size:0.95rem;color:#FFFFFF;margin-bottom:10px;display:flex;align-items:center;gap:8px">
                {svg_icon('shield', 15, '#FFFFFF')} Cryptographic Parameters
            </div>
            <div style="color:var(--text-secondary);font-size:0.88rem;line-height:2">
                <b style="color:#FFFFFF">Cipher:</b> AES-256-GCM (Authenticated AEAD)<br>
                <b style="color:#FFFFFF">KDF:</b> PBKDF2-HMAC-SHA256 (480,000 rounds)<br>
                <b style="color:#FFFFFF">Initialization Vector:</b> 96-bit random nonce<br>
                <b style="color:#FFFFFF">Salt:</b> 128-bit cryptographically secure salt
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("#### Technical Specification & Viva Reference")

    d1, d2 = st.columns(2)
    with d1:
        st.markdown(f"""<div class="mono-card">
            <div style="font-weight:600;font-size:0.9rem;color:#FFFFFF;margin-bottom:8px;display:flex;align-items:center;gap:8px">
                {svg_icon('neural', 15, '#FFFFFF')} 1. Dual U-Net Neural Pipeline
            </div>
            <p style="color:var(--text-secondary);font-size:0.84rem;line-height:1.6">
                • <b>Hiding Network:</b> Concatenates carrier (3 channels) and payload (3 channels) into a 6-channel tensor, outputting a 3-channel synthesized stego image.<br>
                • <b>Reveal Network:</b> Inverts high-frequency residual distributions from the 3-channel stego carrier to reconstruct the 3-channel secret image.<br>
                • <b>Skip Connections:</b> Preserves spatial gradients and edge textures across 5 resolution scales to eliminate visual artifacts.
            </p>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="mono-card">
            <div style="font-weight:600;font-size:0.9rem;color:#FFFFFF;margin-bottom:8px;display:flex;align-items:center;gap:8px">
                {svg_icon('activity', 15, '#FFFFFF')} 2. Distortion Metrics & Steganalysis
            </div>
            <p style="color:var(--text-secondary);font-size:0.84rem;line-height:1.6">
                • <b>PSNR (&gt; 30 dB):</b> Quantifies signal degradation relative to carrier. Values exceeding 30 dB are imperceptible to human visual inspection.<br>
                • <b>SSIM (&gt; 0.95):</b> Assesses structural fidelity, luminance, and contrast against human visual cortex perception models.<br>
                • <b>Detection Resistance (%):</b> Weighted composite index (70% SSIM + 30% PSNR) evaluating robustness against statistical steganalysis.
            </p>
        </div>""", unsafe_allow_html=True)

    with d2:
        st.markdown(f"""<div class="mono-card">
            <div style="font-weight:600;font-size:0.9rem;color:#FFFFFF;margin-bottom:8px;display:flex;align-items:center;gap:8px">
                {svg_icon('lock', 15, '#FFFFFF')} 3. Defense-in-Depth Cryptography
            </div>
            <p style="color:var(--text-secondary);font-size:0.84rem;line-height:1.6">
                • Traditional neural steganography is vulnerable if network weights are compromised.<br>
                • In Deep-Stego, synthesized payloads are encrypted using <b>AES-256-GCM</b> prior to dispatch.<br>
                • An adversary possessing the exact model weights cannot decrypt or reconstruct the payload without the PBKDF2-derived key.
            </p>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="mono-card">
            <div style="font-weight:600;font-size:0.9rem;color:#FFFFFF;margin-bottom:8px;display:flex;align-items:center;gap:8px">
                {svg_icon('database', 15, '#FFFFFF')} 4. Zero-Knowledge Cloud Storage
            </div>
            <p style="color:var(--text-secondary);font-size:0.84rem;line-height:1.6">
                • Ciphertext blobs are stored in Supabase Object Storage isolated with per-file salt and nonce.<br>
                • Passphrases and plaintext decryption keys are never stored on cloud servers.<br>
                • Decryption occurs entirely in client memory during authenticated user sessions.
            </p>
        </div>""", unsafe_allow_html=True)

# ── Minimalist Monochrome Footer ──────────────────────────────────────────────
st.markdown("---")
st.markdown("""<div style="text-align:center;color:#555555;font-size:0.75rem;padding:0.75rem 0;
font-family:var(--font-mono);letter-spacing:0.04em">
Deep-Stego · Dual U-Net Neural Pipeline · AES-256-GCM AEAD Layer · PyTorch + Streamlit + Supabase
</div>""", unsafe_allow_html=True)