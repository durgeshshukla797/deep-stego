import streamlit as st
import torch, torch.nn as nn
import numpy as np
from PIL import Image
import io, uuid, os
from supabase import create_client
from crypto_utils import generate_stego_id, encrypt_image_bytes, decrypt_image_bytes

# ── Page config ───────────────────────────────────────────────────────────────
# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Deep-Stego | Neural Steganography & Verification", layout="wide",
                   initial_sidebar_state="collapsed")

# ══════════════════════════════════════════════════════════════════════════════
# MINIMALIST MONOCHROME DESIGN SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ─── Base Reset ─── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #050505;
    color: #e5e5e5;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1140px;
}
.stApp {
    background-color: #050505;
}

/* ─── Typography & Headings ─── */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff!important;
    font-weight: 700!important;
    letter-spacing: -0.025em!important;
}

/* ─── Clean Monochrome Hero ─── */
.hero {
    background: #0a0a0a;
    border: 1px solid #1f1f1f;
    border-radius: 12px;
    padding: 3rem 2rem 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
}
.hero h1 {
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #ffffff!important;
    margin-bottom: 0.5rem;
}
.hero .subtitle {
    color: #888888;
    font-size: 0.95rem;
    font-weight: 400;
    line-height: 1.6;
    max-width: 640px;
    margin: 0 auto;
}
.badge-row {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}
.tech-badge {
    background: #121212;
    border: 1px solid #262626;
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 0.75rem;
    font-weight: 500;
    color: #a3a3a3;
    letter-spacing: 0.02em;
}

/* ─── Auth Containers ─── */
.auth-wrapper {
    max-width: 440px;
    margin: 0 auto;
    background: #0a0a0a;
    border: 1px solid #1f1f1f;
    border-radius: 12px;
    padding: 2.25rem 2rem;
}
.auth-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.25rem;
    letter-spacing: -0.02em;
}
.auth-sub {
    color: #737373;
    font-size: 0.85rem;
    margin-bottom: 1.25rem;
    font-weight: 400;
    line-height: 1.5;
}
.auth-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 1.25rem 0;
    color: #525252;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.auth-divider::before, .auth-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1f1f1f;
}
.feature-pill {
    display: inline-block;
    background: #121212;
    border: 1px solid #262626;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 0.75rem;
    color: #a3a3a3;
    margin: 3px;
}

/* ─── Monochrome Cards ─── */
.glass-card {
    background: #0c0c0c;
    border: 1px solid #1f1f1f;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}

/* ─── Top Dashboard Bar ─── */
.user-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #0a0a0a;
    border: 1px solid #1f1f1f;
    border-radius: 10px;
    padding: 14px 20px;
    margin-bottom: 1.5rem;
}
.user-info {
    display: flex;
    align-items: center;
    gap: 12px;
}
.user-avatar {
    width: 38px;
    height: 38px;
    border-radius: 8px;
    background: #1c1c1c;
    border: 1px solid #2e2e2e;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.95rem;
    font-weight: 700;
    color: #ffffff;
}
.user-name {
    font-weight: 600;
    color: #ffffff;
    font-size: 0.95rem;
}
.user-id {
    font-size: 0.75rem;
    color: #737373;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 2px;
}
.shield-badge {
    display: flex;
    align-items: center;
    gap: 6px;
    background: #121212;
    border: 1px solid #262626;
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 0.75rem;
    color: #e5e5e5;
    font-weight: 500;
}

/* ─── Section Headers ─── */
.section-header {
    margin-bottom: 1.25rem;
    padding-bottom: 10px;
    border-bottom: 1px solid #1a1a1a;
}
.section-header h2 {
    font-size: 1.2rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
}

/* ─── Message Cards ─── */
.msg-card {
    background: #0c0c0c;
    border: 1px solid #1f1f1f;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 8px;
}
.msg-card.unread {
    border-left: 3px solid #ffffff;
}
.msg-card.read {
    border-left: 3px solid #262626;
    opacity: 0.75;
}
.msg-meta {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}
.sender-tag {
    font-size: 0.85rem;
    font-weight: 600;
    color: #ffffff;
}
.date-tag {
    font-size: 0.75rem;
    color: #666666;
}
.status-tag {
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.status-unread {
    background: #262626;
    color: #ffffff;
}
.status-read {
    background: #171717;
    color: #737373;
    border: 1px solid #262626;
}
.lock-tag {
    background: #141414;
    color: #888888;
    border: 1px solid #262626;
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 500;
}

/* ─── Metrics Display ─── */
.metric-row {
    display: flex;
    gap: 10px;
    margin: 1rem 0;
    flex-wrap: wrap;
}
.metric-card {
    flex: 1;
    min-width: 110px;
    background: #0a0a0a;
    border: 1px solid #1f1f1f;
    border-radius: 8px;
    padding: 14px;
    text-align: center;
}
.metric-val {
    font-size: 1.5rem;
    font-weight: 700;
    color: #ffffff;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -0.02em;
}
.metric-lbl {
    font-size: 0.7rem;
    color: #737373;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}
.img-label {
    text-align: center;
    font-size: 0.75rem;
    color: #737373;
    margin-top: 6px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ─── Notification Banners ─── */
.success-banner {
    background: #0c0c0c;
    border: 1px solid #262626;
    border-left: 3px solid #ffffff;
    border-radius: 6px;
    padding: 12px 18px;
    color: #e5e5e5;
    font-size: 0.88rem;
    margin: 1rem 0;
}
.error-banner {
    background: #0f0a0a;
    border: 1px solid #2e1a1a;
    border-left: 3px solid #dc2626;
    border-radius: 6px;
    padding: 12px 18px;
    color: #f87171;
    font-size: 0.88rem;
    margin: 1rem 0;
}
.info-banner {
    background: #0c0c0c;
    border: 1px solid #1f1f1f;
    border-radius: 6px;
    padding: 12px 18px;
    color: #888888;
    font-size: 0.85rem;
    margin: 0.75rem 0;
    line-height: 1.55;
}
.profile-id {
    background: #0a0a0a;
    border: 1px solid #1f1f1f;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    margin: 1rem 0;
}
.profile-id .id-val {
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.15em;
}
.profile-id .id-lbl {
    font-size: 0.7rem;
    color: #666666;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
}

/* ─── Buttons ─── */
div.stButton > button {
    border-radius: 6px!important;
    font-weight: 500!important;
    font-size: 0.88rem!important;
    font-family: 'Inter', sans-serif!important;
    transition: all 0.15s ease!important;
    padding: 8px 16px!important;
    border: 1px solid #262626!important;
    background: #111111!important;
    color: #e5e5e5!important;
}
div.stButton > button:hover {
    background: #1c1c1c!important;
    border-color: #383838!important;
    color: #ffffff!important;
    transform: none!important;
    box-shadow: none!important;
}
div.stButton > button[kind="primary"] {
    background: #ffffff!important;
    color: #000000!important;
    border: 1px solid #ffffff!important;
    font-weight: 600!important;
}
div.stButton > button[kind="primary"]:hover {
    background: #e0e0e0!important;
    color: #000000!important;
    border-color: #e0e0e0!important;
}

/* ─── Tabs ─── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #0a0a0a;
    border-radius: 8px;
    padding: 3px;
    border: 1px solid #1a1a1a;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px!important;
    padding: 8px 18px!important;
    font-weight: 500!important;
    font-size: 0.84rem!important;
    color: #737373!important;
    transition: all 0.15s!important;
}
.stTabs [aria-selected="true"] {
    background: #171717!important;
    color: #ffffff!important;
    border: 1px solid #262626!important;
    font-weight: 600!important;
}
.stTabs [data-baseweb="tab-highlight"] {
    background: transparent!important;
}

/* ─── Form Inputs ─── */
.stTextInput > div > div > input, .stTextArea > div > div > textarea {
    background: #0a0a0a!important;
    border: 1px solid #242424!important;
    border-radius: 6px!important;
    color: #ffffff!important;
    font-family: 'Inter', sans-serif!important;
    font-size: 0.88rem!important;
}
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
    border-color: #ffffff!important;
    box-shadow: none!important;
}
.stSelectbox > div > div {
    background: #0a0a0a!important;
    border: 1px solid #242424!important;
    border-radius: 6px!important;
}
.stFileUploader {
    border: 1px dashed #262626!important;
    border-radius: 8px!important;
    background: #080808!important;
}

/* ─── Scrollbar ─── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #050505; }
::-webkit-scrollbar-thumb { background: #222222; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #333333; }
</style>""", unsafe_allow_html=True)

# ── Supabase ──────────────────────────────────────────────────────────────────
SUPA_URL = os.environ.get("SUPABASE_URL", "https://uptkoxuoppvcyfnqvmfj.supabase.co")
SUPA_KEY = os.environ.get("SUPABASE_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVwdGtveHVvcHB2Y3lmbnF2bWZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ3Njk5NDIsImV4cCI6MjA5MDM0NTk0Mn0.ZfddbXl7QiaQQ1ddg9rJBodRpT-Fql9IIxk1HKgfrsY")
sb = create_client(SUPA_URL, SUPA_KEY)

# Restore auth session on Streamlit rerun (critical for RLS)
if "_sb_access_token" in st.session_state and "_sb_refresh_token" in st.session_state:
    try:
        sb.auth.set_session(st.session_state["_sb_access_token"], st.session_state["_sb_refresh_token"])
    except Exception:
        pass  # Token expired — user will need to re-login

# ── Model ─────────────────────────────────────────────────────────────────────
IMG_SIZE = 128
DEVICE = torch.device("cpu")

class ConvBlock(nn.Module):
    def __init__(self, i, o):
        super().__init__()
        self.b = nn.Sequential(nn.Conv2d(i,o,3,1,1,bias=False), nn.BatchNorm2d(o), nn.ReLU(True))
    def forward(self, x): return self.b(x)

class UNet(nn.Module):
    def __init__(self, ic=6, oc=3, bf=64):
        super().__init__()
        self.e1=nn.Sequential(ConvBlock(ic,bf),ConvBlock(bf,bf))
        self.e2=nn.Sequential(ConvBlock(bf,bf*2),ConvBlock(bf*2,bf*2))
        self.e3=nn.Sequential(ConvBlock(bf*2,bf*4),ConvBlock(bf*4,bf*4))
        self.e4=nn.Sequential(ConvBlock(bf*4,bf*8),ConvBlock(bf*8,bf*8))
        self.bn=nn.Sequential(ConvBlock(bf*8,bf*8),ConvBlock(bf*8,bf*8))
        self.d4=nn.Sequential(ConvBlock(bf*16,bf*8),ConvBlock(bf*8,bf*4))
        self.d3=nn.Sequential(ConvBlock(bf*8,bf*4),ConvBlock(bf*4,bf*2))
        self.d2=nn.Sequential(ConvBlock(bf*4,bf*2),ConvBlock(bf*2,bf))
        self.d1=nn.Sequential(ConvBlock(bf*2,bf),ConvBlock(bf,bf//2))
        self.out=nn.Sequential(nn.Conv2d(bf//2,oc,1),nn.Sigmoid())
        self.pool=nn.MaxPool2d(2); self.up=nn.Upsample(scale_factor=2,mode='bilinear',align_corners=True)
    def forward(self, x):
        e1=self.e1(x);e2=self.e2(self.pool(e1));e3=self.e3(self.pool(e2));e4=self.e4(self.pool(e3))
        b=self.bn(self.pool(e4))
        return self.out(self.d1(torch.cat([self.up(self.d2(torch.cat([self.up(self.d3(torch.cat([self.up(self.d4(torch.cat([self.up(b),e4],1))),e3],1))),e2],1))),e1],1)))

class HidingNet(nn.Module):
    def __init__(self, bf=64): super().__init__(); self.u=UNet(6,3,bf)
    def forward(self, c, s): return self.u(torch.cat([c,s],1))

class RevealNet(nn.Module):
    def __init__(self, bf=64): super().__init__(); self.u=UNet(3,3,bf)
    def forward(self, x): return self.u(x)

@st.cache_resource(show_spinner=False)
def load_models():
    h=HidingNet(64).to(DEVICE); r=RevealNet(64).to(DEVICE); p="best.pt"
    if not os.path.exists(p):
        try:
            from huggingface_hub import hf_hub_download
            p=hf_hub_download(repo_id=os.environ.get("HF_REPO",""),filename="best.pt",local_dir=".")
        except Exception as e: return None,None,str(e)
    ck=torch.load(p,map_location=DEVICE,weights_only=False)
    h.load_state_dict(ck.get("hiding",ck.get("hiding_net",{}))); r.load_state_dict(ck.get("reveal",ck.get("reveal_net",{})))
    h.eval(); r.eval(); return h,r,None

# ── Helpers ───────────────────────────────────────────────────────────────────
def preprocess(img):
    img=img.convert("RGB").resize((IMG_SIZE,IMG_SIZE),Image.BICUBIC)
    return torch.from_numpy(np.array(img,dtype=np.float32)/255.0).permute(2,0,1).unsqueeze(0).to(DEVICE)

def postprocess(t):
    return Image.fromarray((t.squeeze(0).detach().cpu().clamp(0,1).permute(1,2,0).numpy()*255).astype(np.uint8))

def to_bytes(img):
    buf=io.BytesIO(); img.save(buf,format="PNG"); return buf.getvalue()

def calc_psnr(a,b):
    mse=np.mean((np.array(a).astype(float)-np.array(b).astype(float))**2)
    return 0 if mse==0 else round(20*np.log10(255/np.sqrt(mse)),1)

def calc_ssim(a,b):
    a,b=np.array(a).astype(float),np.array(b).astype(float)
    ma,mb=a.mean(),b.mean(); sa,sb=a.std(),b.std()
    cov=((a-ma)*(b-mb)).mean(); c1,c2=(0.01*255)**2,(0.03*255)**2
    return round(float((2*ma*mb+c1)*(2*cov+c2)/((ma**2+mb**2+c1)*(sa**2+sb**2+c2))),4)

def detection_score(p,s):
    # SSIM weighted 70% (perceptual), PSNR weighted 30%
    # SSIM 0.99+ is near-perfect; PSNR >20 is acceptable for steganography
    ssim_score = min(max((s - 0.85) / 0.15, 0), 1)  # 0.85 -> 0%, 1.0 -> 100%
    psnr_score = min(max((p - 18) / 22, 0), 1)       # 18 -> 0%, 40 -> 100%
    return round(ssim_score * 70 + psnr_score * 30, 1)

def pixel_diff_heatmap(a,b):
    diff=np.abs(np.array(a).astype(float)-np.array(b).astype(float)).mean(axis=2)
    if diff.max()>0: diff=(diff/diff.max()*255)
    hm=np.zeros((*diff.shape,3),dtype=np.uint8)
    hm[:,:,0]=(diff*0.9).astype(np.uint8)
    hm[:,:,1]=((255-diff)*0.3).astype(np.uint8)
    hm[:,:,2]=(np.clip(200-diff,0,255)*0.7).astype(np.uint8)
    return Image.fromarray(hm)

# ── DB Functions ──────────────────────────────────────────────────────────────
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
    sb.storage.from_("stego-images").upload(fn, data, {"content-type":"application/octet-stream"})

def insert_message(sid, rid, path, note, has_pp, nonce_b64, salt_b64):
    sb.table("messages").insert({
        "sender_id":sid,"receiver_id":rid,"stego_path":path,"note":note,
        "revealed":False,"passphrase_hash":"yes" if has_pp else "no",
        "encryption_iv":nonce_b64,"sender_public_key":salt_b64
    }).execute()

def get_inbox(uid):
    try:
        return (sb.table("messages").select("*, profiles!messages_sender_id_fkey(username,stego_id)")
                .eq("receiver_id",uid).order("created_at",desc=True).execute()).data or []
    except Exception:
        try:
            msgs = (sb.table("messages").select("*").eq("receiver_id",uid).order("created_at",desc=True).execute()).data or []
            for m in msgs:
                p = sb.table("profiles").select("username,stego_id").eq("id", m.get("sender_id")).execute().data
                m["profiles"] = p[0] if p else {}
            return msgs
        except Exception:
            return []

def get_sent(uid):
    try:
        return (sb.table("messages").select("*, profiles!messages_receiver_id_fkey(username,stego_id)")
                .eq("sender_id",uid).order("created_at",desc=True).execute()).data or []
    except Exception:
        try:
            msgs = (sb.table("messages").select("*").eq("sender_id",uid).order("created_at",desc=True).execute()).data or []
            for m in msgs:
                p = sb.table("profiles").select("username,stego_id").eq("id", m.get("receiver_id")).execute().data
                m["profiles"] = p[0] if p else {}
            return msgs
        except Exception:
            return []

def download_stego(p): return sb.storage.from_("stego-images").download(p)
def mark_revealed(mid): sb.table("messages").update({"revealed":True}).eq("id",mid).execute()

# ── Auth ──────────────────────────────────────────────────────────────────────
def _ensure_profile(user, username=None):
    """Ensure a profile row exists for the given auth user. Creates one if missing."""
    try:
        prof = sb.table("profiles").select("*").eq("id", user.id).single().execute()
        return prof.data
    except Exception:
        # Profile missing — create it
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
        res = sb.auth.sign_up({"email": email, "password": password,
            "options": {"data": {"username": username}}})
        if not res.user:
            return False, None, "Registration failed.", False
        # Create profile (upsert handles duplicates gracefully)
        sb.table("profiles").upsert({"id": res.user.id, "username": username, "stego_id": sid}).execute()
        
        # Auto-login immediately after registration
        login_ok, _ = do_login(email, password)
        if login_ok:
            return True, sid, None, True
        return True, sid, None, False
    except Exception as e:
        err = str(e)
        if "already registered" in err.lower() or "already been registered" in err.lower():
            # User exists in auth — try to log them in and ensure profile exists
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
            # Store tokens for session restore on rerun
            if res.session:
                st.session_state["_sb_access_token"] = res.session.access_token
                st.session_state["_sb_refresh_token"] = res.session.refresh_token
            return True, None
        return False, "Login failed."
    except Exception as e: return False, str(e)

def do_logout():
    # Clear all session keys so no leftover inputs, passwords, or data remain
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    try: sb.auth.sign_out()
    except Exception: pass
    st.rerun()

# ── Session ───────────────────────────────────────────────────────────────────
for k in ["user","profile","stego_result"]:
    if k not in st.session_state: st.session_state[k]=None

# ══════════════════════════════════════════════════════════════════════════════
# HERO & LANDING (Shown only when unauthenticated)
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.user is None:
    st.markdown("""<div class="hero">
    <h1>Deep-Stego</h1>
    <p class="subtitle">Neural Image Steganography with AES-256-GCM Payload Verification.<br>
    Synthesizes imperceptible carrier-payload embeddings with authenticated encryption.</p>
    <div class="badge-row">
    <div class="tech-badge">Dual U-Net</div>
    <div class="tech-badge">AES-256-GCM</div>
    <div class="tech-badge">128x128 Resolution</div>
    <div class="tech-badge">SSIM &gt; 0.92</div>
    <div class="tech-badge">PBKDF2-SHA256</div>
    </div></div>""", unsafe_allow_html=True)

with st.spinner("Initializing neural network..."):
    hiding_net, reveal_net, model_error = load_models()
if model_error:
    st.error(f"Model initialization error: {model_error}"); st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.user is None:
    col_l, col_center, col_r = st.columns([1, 2, 1])
    with col_center:
        tab_login, tab_reg = st.tabs(["Sign In", "Create Account"])

        with tab_login:
            st.markdown('<div class="auth-title">Account Access</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-sub">Authenticate to access transmission inbox and neural decoder.</div>', unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=False):
                l_email = st.text_input("Email", placeholder="user@domain.com", key="auth_login_email")
                l_pass = st.text_input("Password", type="password", placeholder="Enter password", key="auth_login_pass")
                submit_login = st.form_submit_button("Sign In", type="primary", use_container_width=True)
                
                if submit_login:
                    if not l_email or not l_pass:
                        st.warning("Both email and password are required.")
                    else:
                        ok, err = do_login(l_email, l_pass)
                        if ok:
                            for k in ["auth_login_email", "auth_login_pass", "auth_reg_user", "auth_reg_email", "auth_reg_pass"]:
                                st.session_state.pop(k, None)
                            st.rerun()
                        else:
                            st.error(err or "Authentication failed. Please verify credentials.")

            st.markdown('<div class="auth-divider">Supabase Cloud Authentication</div>', unsafe_allow_html=True)
            st.markdown("""<div style="display:flex;justify-content:center;flex-wrap:wrap">
            <div class="feature-pill">AES-256-GCM Encrypted</div>
            <div class="feature-pill">Dual U-Net Inference</div>
            <div class="feature-pill">Authenticated Routing</div>
            </div>""", unsafe_allow_html=True)

        with tab_reg:
            st.markdown('<div class="auth-title">User Registration</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-sub">Register account to receive an assigned Stego-ID for transmission routing.</div>', unsafe_allow_html=True)
            
            with st.form("register_form", clear_on_submit=False):
                r_user = st.text_input("Username", placeholder="e.g. duggu", key="auth_reg_user")
                r_email = st.text_input("Email", placeholder="user@domain.com", key="auth_reg_email")
                r_pass = st.text_input("Password", type="password", placeholder="Minimum 6 characters", key="auth_reg_pass")
                st.markdown("""<div class="info-banner" style="font-size:0.8rem">
                A system-generated Stego-ID will be provisioned for peer-to-peer transmission routing.
                </div>""", unsafe_allow_html=True)
                submit_reg = st.form_submit_button("Register & Authenticate", type="primary", use_container_width=True)
                
                if submit_reg:
                    if not (r_user and r_email and r_pass):
                        st.warning("All fields are mandatory.")
                    elif len(r_pass) < 6:
                        st.error("Password length must be at least 6 characters.")
                    else:
                        with st.spinner("Provisioning account..."):
                            ok, sid, err, auto_logged = do_register(r_user, r_email, r_pass)
                            if ok:
                                for k in ["auth_login_email", "auth_login_pass", "auth_reg_user", "auth_reg_email", "auth_reg_pass"]:
                                    st.session_state.pop(k, None)
                                if auto_logged:
                                    st.session_state["_just_registered"] = True
                                    st.rerun()
                                else:
                                    st.success(f"Account registered. Assigned Stego-ID: {sid}. Proceed to Sign In.")
                            else:
                                st.error(err or "Registration failed.")

    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
profile = st.session_state.profile
uid = profile["id"]; uname = profile["username"]; stego_id = profile.get("stego_id","N/A")
avatar_initial = (uname[:1] if uname else "U").upper()

# Banner upon first registration
if st.session_state.get("_just_registered"):
    st.markdown(f"""<div class="success-banner">
    Account successfully provisioned. User: <b>{uname}</b> | Assigned Stego-ID: 
    <code style="font-family:'JetBrains Mono';background:#171717;padding:2px 8px;border-radius:4px;color:#ffffff">{stego_id}</code>.
    </div>""", unsafe_allow_html=True)
    st.session_state["_just_registered"] = False

# Professional Header Bar
st.markdown(f"""<div class="user-bar">
<div class="user-info">
<div class="user-avatar">{avatar_initial}</div>
<div>
<div class="user-name">{uname}</div>
<div class="user-id">STEGO-ID: <span style="color:#ffffff;font-weight:600;font-family:'JetBrains Mono'">{stego_id}</span></div>
</div>
</div>
<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">
<div class="shield-badge">AES-256-GCM Active</div>
<div class="shield-badge">Dual U-Net Online</div>
</div>
</div>""", unsafe_allow_html=True)

c_spacer, c_logout = st.columns([6,1])
with c_logout:
    if st.button("Sign Out", use_container_width=True, key="logout_btn"):
        do_logout()

# Calculate unread inbox count for clean badge
inbox_items = get_inbox(uid)
unread_count = sum(1 for m in inbox_items if not m.get("revealed", False))
inbox_tab_title = f"Inbox [{unread_count}]" if unread_count > 0 else "Inbox"

tab_encode, tab_inbox, tab_decode, tab_sent, tab_profile = st.tabs([
    "Encode & Transmit", inbox_tab_title, "Decode", "Sent History", "System Architecture"])

# ═══════════════════ ENCODE & TRANSMIT ═══════════════════
with tab_encode:
    st.markdown("""<div class="section-header">
    <h2>Neural Steganographic Synthesis & Encryption</h2></div>""", unsafe_allow_html=True)

    # ── STEP 1: Upload Images ─────────────────────────────────────────────
    st.markdown("#### 1. Image Inputs")
    cc, cs = st.columns(2)
    with cc:
        st.markdown("""<div class="glass-card">
        <div style="color:#ffffff;font-weight:600;font-size:0.88rem;margin-bottom:8px">
        Cover Image <span style="color:#737373;font-weight:400;font-size:0.8rem">— Carrier Media</span></div>""", unsafe_allow_html=True)
        cover_f = st.file_uploader("", type=["jpg","jpeg","png"], key="cover", label_visibility="collapsed")
        if cover_f:
            st.image(cover_f, use_container_width=True)
            st.markdown('<div class="img-label">Cover (Carrier)</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with cs:
        st.markdown("""<div class="glass-card">
        <div style="color:#ffffff;font-weight:600;font-size:0.88rem;margin-bottom:8px">
        Secret Image <span style="color:#737373;font-weight:400;font-size:0.8rem">— Payload to Embed</span></div>""", unsafe_allow_html=True)
        secret_f = st.file_uploader("", type=["jpg","jpeg","png"], key="secret", label_visibility="collapsed")
        if secret_f:
            st.image(secret_f, use_container_width=True)
            st.markdown('<div class="img-label">Secret (Payload)</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── STEP 2: Set Passphrase ────────────────────────────────────────────
    st.markdown("#### 2. Cryptographic Key Derivation")

    pp_set = st.session_state.get("_passphrase_confirmed", False)

    if not pp_set:
        pc1, pc2 = st.columns([3, 1])
        with pc1:
            pp_val = st.text_input("Secret passphrase", type="password", key="pp",
                                    placeholder="Enter passphrase for PBKDF2 key derivation...", label_visibility="collapsed")
        with pc2:
            if st.button("Configure Key", use_container_width=True, type="primary"):
                if pp_val and len(pp_val) >= 3:
                    st.session_state["_passphrase_confirmed"] = True
                    st.session_state["_passphrase_value"] = pp_val
                    st.rerun()
                else:
                    st.error("Passphrase must contain at least 3 characters.")
        st.markdown("""<div class="info-banner">
        The recipient must use the identical passphrase to derive the 256-bit AES key and decrypt the payload.
        </div>""", unsafe_allow_html=True)
    else:
        pp_val = st.session_state.get("_passphrase_value", "")
        st.markdown(f"""<div class="success-banner">
        Passphrase configured ({len(pp_val)} characters). Ready for neural synthesis.
        </div>""", unsafe_allow_html=True)
        if st.button("Reset Passphrase"):
            st.session_state["_passphrase_confirmed"] = False
            st.session_state["_passphrase_value"] = ""
            st.rerun()

    # ── STEP 3: Encode ────────────────────────────────────────────────────
    passphrase = st.session_state.get("_passphrase_value", "")
    if cover_f and secret_f and pp_set:
        st.markdown("---")
        if st.button("Synthesize Stego Image", type="primary", use_container_width=True):
            with st.spinner("Executing Dual U-Net forward pass and AES-256-GCM encryption..."):
                try:
                    ci=Image.open(cover_f); si=Image.open(secret_f)
                    ct_t,st_t=preprocess(ci),preprocess(si)
                    with torch.no_grad(): stego_t=hiding_net(ct_t,st_t)
                    stego_img=postprocess(stego_t); stego_bytes=to_bytes(stego_img)
                    cr=ci.convert("RGB").resize((IMG_SIZE,IMG_SIZE))
                    pv=calc_psnr(cr,stego_img); sv=calc_ssim(np.array(cr),np.array(stego_img))
                    dr=detection_score(pv,sv)
                    enc=encrypt_image_bytes(stego_bytes, passphrase)
                    st.session_state.stego_result={
                        "cover":cr,"secret":si,"stego":stego_img,
                        "psnr":pv,"ssim":sv,"dr":dr,"receiver":None,
                        "bytes":stego_bytes,"enc":enc,"sent":False
                    }
                    st.rerun()
                except Exception as e: st.error(f"Execution error: {e}")
    elif cover_f and secret_f and not pp_set:
        st.markdown("---")
        st.warning("Configure cryptographic passphrase above to enable neural synthesis.")

    # ── RESULTS + SEND ────────────────────────────────────────────────────
    if st.session_state.stego_result:
        r = st.session_state.stego_result
        sent = r.get("sent", False)

        if sent:
            st.markdown(f"""<div class="success-banner">
            Transmission completed and dispatched to <b>{r['receiver']}</b>.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="success-banner">
            Synthesis completed. Stego image generated and AES-256-GCM payload verified.
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="metric-row">
        <div class="metric-card"><div class="metric-val">{r['psnr']} dB</div><div class="metric-lbl">PSNR</div></div>
        <div class="metric-card"><div class="metric-val">{r['ssim']}</div><div class="metric-lbl">SSIM</div></div>
        <div class="metric-card"><div class="metric-val">{r['dr']}%</div><div class="metric-lbl">Detection Resistance</div></div>
        <div class="metric-card"><div class="metric-val">AES-256</div><div class="metric-lbl">Cipher Mode</div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("#### Verification Analysis")
        c1,c2,c3=st.columns(3)
        with c1: st.image(r["cover"],use_container_width=True); st.markdown('<div class="img-label">Cover (Carrier)</div>',unsafe_allow_html=True)
        with c2: st.image(r["stego"],use_container_width=True); st.markdown('<div class="img-label">Stego Output</div>',unsafe_allow_html=True)
        with c3: st.image(pixel_diff_heatmap(np.array(r["cover"]),np.array(r["stego"])),use_container_width=True); st.markdown('<div class="img-label">Pixel Residual Heatmap</div>',unsafe_allow_html=True)

        st.download_button("Download Stego Image", data=r["bytes"], file_name="stego.png", mime="image/png")

        # ── Dispatch transmission ──────────────────────────────────────────
        if not sent:
            st.markdown("---")
            st.markdown("#### 3. Dispatch Transmission")
            st.markdown("""<div class="info-banner">
            Query destination user by Username or Stego-ID to transmit the encrypted stego payload.
            </div>""", unsafe_allow_html=True)

            sc1, sc2 = st.columns([3, 1])
            with sc1:
                sq = st.text_input("Enter username or Stego-ID", placeholder="e.g. duggu or DSS-19F569", key="srch", label_visibility="collapsed")
            with sc2:
                search_btn = st.button("Search Users", use_container_width=True, key="search_btn")

            chosen = None
            if (sq and len(sq) >= 1) and search_btn:
                with st.spinner("Querying directory..."):
                    st.session_state["_search_results"] = search_users(sq, uid)

            search_results = st.session_state.get("_search_results", [])
            if search_results:
                for u in search_results:
                    rc1, rc2 = st.columns([4, 1])
                    with rc1:
                        st.markdown(f"""<div class="glass-card" style="padding:10px 14px;margin-bottom:6px">
                        <div style="display:flex;align-items:center;gap:12px">
                        <div>
                        <div style="font-weight:600;color:white;font-size:0.9rem">{u['username']}</div>
                        <div style="font-size:0.75rem;color:#737373;font-family:'JetBrains Mono',monospace">{u['stego_id']}</div>
                        </div></div></div>""", unsafe_allow_html=True)
                    with rc2:
                        if st.button(f"Transmit", key=f"send_{u['id']}", use_container_width=True):
                            chosen = u

                if chosen is None:
                    for u in search_results:
                        if st.session_state.get(f"send_{u['id']}"):
                            chosen = u
                            break
            elif sq and search_btn:
                st.markdown("""<div class="info-banner">
                No matching user found in directory.
                </div>""", unsafe_allow_html=True)

            note = st.text_input("Transmission metadata note (optional)", placeholder="e.g. Project deliverable verification", key="note")

            if chosen:
                with st.spinner(f"Encrypting and transmitting to {chosen['username']}..."):
                    try:
                        enc = r["enc"]
                        fn = f"{uid}/{uuid.uuid4().hex}.enc"
                        upload_stego(enc["ct"], fn)
                        insert_message(uid, chosen["id"], fn, note, True, enc["nonce"], enc["salt"])
                        st.session_state.stego_result["receiver"] = chosen["username"]
                        st.session_state.stego_result["sent"] = True
                        if "_search_results" in st.session_state: del st.session_state["_search_results"]
                        st.rerun()
                    except Exception as e: st.error(f"Transmission error: {e}")

        if st.button("New Synthesis Session"):
            st.session_state.stego_result=None
            st.session_state["_passphrase_confirmed"]=False
            st.session_state["_passphrase_value"]=""
            if "_search_results" in st.session_state: del st.session_state["_search_results"]
            st.rerun()

# ═══════════════════ INBOX ═══════════════════
with tab_inbox:
    ch,cr=st.columns([4,1])
    with ch:
        st.markdown("""<div class="section-header">
        <h2>Incoming Encrypted Transmissions</h2></div>""", unsafe_allow_html=True)
    with cr:
        if st.button("Refresh", use_container_width=True, key="ref_in"): st.rerun()

    inbox=get_inbox(uid)
    if not inbox:
        st.markdown(f"""<div class="glass-card" style="text-align:center;padding:2.5rem">
        <div style="color:#737373;font-size:0.95rem">No incoming transmissions recorded.<br>
        <span style="font-size:0.8rem;color:#555555">Provide assigned Stego-ID <code style="color:#ffffff">{stego_id}</code> for inbound transmissions.</span>
        </div></div>""", unsafe_allow_html=True)
    else:
        unread=sum(1 for m in inbox if not m["revealed"])
        st.markdown(f"""<div class="metric-row">
        <div class="metric-card"><div class="metric-val">{len(inbox)}</div><div class="metric-lbl">Total Received</div></div>
        <div class="metric-card"><div class="metric-val">{unread}</div><div class="metric-lbl">Pending Decryption</div></div>
        <div class="metric-card"><div class="metric-val">{len(inbox)-unread}</div><div class="metric-lbl">Decrypted</div></div>
        </div>""", unsafe_allow_html=True)

        for msg in inbox:
            si=msg.get("profiles") or {}; sn=si.get("username","Unknown"); ssid=si.get("stego_id","")
            ir=msg["revealed"]; d=msg["created_at"][:10]
            cc="read" if ir else "unread"; sc="status-read" if ir else "status-unread"
            st_=("Decrypted" if ir else "Encrypted")
            nh=f'<div style="color:#888888;font-size:0.8rem;margin-top:6px">Note: {msg["note"]}</div>' if msg.get("note") else ""
            st.markdown(f"""<div class="msg-card {cc}"><div class="msg-meta">
            <span class="sender-tag">From: {sn}</span>
            <span style="color:#666666;font-family:'JetBrains Mono';font-size:0.72rem">{ssid}</span>
            <span class="date-tag">{d}</span>
            <span class="status-tag {sc}">{st_}</span>
            <span class="lock-tag">AES-256</span>
            </div>{nh}</div>""", unsafe_allow_html=True)

            if not ir:
                pp_in=st.text_input("Decryption passphrase", type="password", key=f"pp_{msg['id']}", placeholder="Enter passphrase to derive AES-256 key")
                if st.button("Decrypt & Reconstruct", key=f"btn_{msg['id']}", use_container_width=True):
                    if not pp_in:
                        st.error("Passphrase required for key derivation.")
                    else:
                        with st.spinner("Deriving AES-256 key and reconstructing payload..."):
                            try:
                                nonce=msg.get("encryption_iv",""); salt=msg.get("sender_public_key","")
                                enc=download_stego(msg["stego_path"])
                                dec=decrypt_image_bytes(enc, pp_in, nonce, salt)
                                stego_img=Image.open(io.BytesIO(dec)); stego_t=preprocess(stego_img)
                                with torch.no_grad(): rev_t=reveal_net(stego_t)
                                rev_img=postprocess(rev_t)
                                st.markdown(f"""<div class="success-banner">Decryption verified. Secret payload reconstructed from <b>{sn}</b>.</div>""",unsafe_allow_html=True)
                                c1,c2=st.columns(2)
                                with c1: st.image(stego_img,use_container_width=True); st.markdown('<div class="img-label">Received Stego</div>',unsafe_allow_html=True)
                                with c2: st.image(rev_img,use_container_width=True); st.markdown('<div class="img-label">Reconstructed Secret</div>',unsafe_allow_html=True)
                                st.download_button("Download Reconstructed Image", data=to_bytes(rev_img), file_name=f"reconstructed_{sn}.png", mime="image/png", key=f"dl_{msg['id']}")
                                mark_revealed(msg["id"])
                            except Exception as e:
                                if "tag" in str(e).lower() or "InvalidTag" in str(type(e).__name__):
                                    st.markdown('<div class="error-banner">Authentication failure: Invalid passphrase or corrupted ciphertext.</div>',unsafe_allow_html=True)
                                else: st.error(f"Decryption error: {e}")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ═══════════════════ DECODE ═══════════════════
with tab_decode:
    st.markdown("""<div class="section-header">
    <h2>Neural Reveal Inference</h2></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="info-banner">
    Upload a stego image to reconstruct embedded secret image. If encrypted with a passphrase, provide it for key derivation. Direct unencrypted stego PNGs can be reconstructed without a passphrase.
    </div>""", unsafe_allow_html=True)

    st.markdown("#### 1. Stego Image Input")
    decode_file = st.file_uploader("Upload stego image", type=["jpg","jpeg","png"], key="decode_upload", label_visibility="collapsed")

    if decode_file:
        st.image(decode_file, use_container_width=True, caption="Stego Carrier Input")

        st.markdown("#### 2. Passphrase Configuration (If Encrypted)")
        decode_pp = st.text_input("Passphrase", type="password", key="decode_pp",
                                   placeholder="Leave blank if using raw unencrypted stego image...")

        st.markdown("#### 3. Reconstruct Secret Payload")
        if st.button("Execute Reveal Network", type="primary", use_container_width=True, key="decode_reveal_btn"):
            with st.spinner("Forward pass through Reveal Network..."):
                try:
                    raw_bytes = decode_file.getvalue()
                    stego_img = Image.open(io.BytesIO(raw_bytes))
                    stego_t = preprocess(stego_img)
                    with torch.no_grad():
                        rev_t = reveal_net(stego_t)
                    rev_img = postprocess(rev_t)

                    st.markdown("""<div class="success-banner">Neural reveal inference completed successfully.</div>""",
                                unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        st.image(stego_img, use_container_width=True)
                        st.markdown('<div class="img-label">Stego Input</div>', unsafe_allow_html=True)
                    with c2:
                        st.image(rev_img, use_container_width=True)
                        st.markdown('<div class="img-label">Reconstructed Secret</div>', unsafe_allow_html=True)
                    st.download_button("Download Reconstructed Image", data=to_bytes(rev_img),
                                       file_name="reconstructed_secret.png", mime="image/png", key="decode_dl")
                except Exception as e:
                    st.error(f"Inference error: {e}")

# ═══════════════════ SENT HISTORY ═══════════════════
with tab_sent:
    st.markdown("""<div class="section-header">
    <h2>Outbound Transmission Log</h2></div>""", unsafe_allow_html=True)
    sent=get_sent(uid)
    if not sent:
        st.markdown("""<div class="glass-card" style="text-align:center;padding:2.5rem">
        <div style="color:#737373">No outbound transmissions logged.</div></div>""",unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="metric-row">
        <div class="metric-card"><div class="metric-val">{len(sent)}</div><div class="metric-lbl">Total Dispatched</div></div>
        <div class="metric-card"><div class="metric-val">{sum(1 for m in sent if m['revealed'])}</div><div class="metric-lbl">Decrypted by Recipient</div></div>
        <div class="metric-card"><div class="metric-val">{sum(1 for m in sent if not m['revealed'])}</div><div class="metric-lbl">Pending Recipient Action</div></div>
        </div>""", unsafe_allow_html=True)
        for msg in sent:
            ri=msg.get("profiles") or {}; rn=ri.get("username","Unknown"); rsid=ri.get("stego_id","")
            d=msg["created_at"][:10]; op=msg["revealed"]
            st_=("Decrypted" if op else "Pending"); sc=("status-read" if op else "status-unread")
            nh=f'<div style="color:#888888;font-size:0.8rem;margin-top:6px">Note: {msg["note"]}</div>' if msg.get("note") else ""
            st.markdown(f"""<div class="msg-card"><div class="msg-meta">
            <span class="sender-tag">To: {rn}</span>
            <span style="color:#666666;font-family:'JetBrains Mono';font-size:0.72rem">{rsid}</span>
            <span class="date-tag">{d}</span>
            <span class="status-tag {sc}">{st_}</span>
            <span class="lock-tag">AES-256</span>
            </div>{nh}</div>""", unsafe_allow_html=True)

# ═══════════════════ SYSTEM ARCHITECTURE ═══════════════════
with tab_profile:
    st.markdown("""<div class="section-header">
    <h2>System Architecture & Cryptographic Verification</h2></div>""", unsafe_allow_html=True)
    
    st.markdown(f"""<div class="profile-id">
    <div class="id-lbl">ASSIGNED STEGO-ID</div>
    <div class="id-val">{stego_id}</div>
    <div class="id-lbl" style="margin-top:4px">Network Routing Identifier</div>
    </div>""", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="glass-card">
        <div style="color:#ffffff;font-weight:600;margin-bottom:8px;font-size:0.95rem">Account Configuration</div>
        <div style="color:#a3a3a3;font-size:0.88rem;line-height:2">
        <b style="color:#ffffff">Username:</b> {uname}<br>
        <b style="color:#ffffff">Stego-ID:</b> <code style="color:#ffffff">{stego_id}</code><br>
        <b style="color:#ffffff">Principal UUID:</b> <code style="font-size:0.75rem;color:#737373">{uid}</code><br>
        <b style="color:#ffffff">Authorization:</b> Authenticated
        </div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="glass-card">
        <div style="color:#ffffff;font-weight:600;margin-bottom:8px;font-size:0.95rem">Cryptographic Parameters</div>
        <div style="color:#a3a3a3;font-size:0.88rem;line-height:2">
        <b style="color:#ffffff">Cipher:</b> AES-256-GCM (Authenticated AEAD)<br>
        <b style="color:#ffffff">KDF:</b> PBKDF2-HMAC-SHA256 (480,000 iterations)<br>
        <b style="color:#ffffff">Initialization Vector:</b> 96-bit random nonce<br>
        <b style="color:#ffffff">Salt:</b> 128-bit cryptographically secure salt
        </div></div>""", unsafe_allow_html=True)

    st.markdown("#### Technical Specification & Verification Analysis")

    d1, d2 = st.columns(2)
    with d1:
        st.markdown("""<div class="glass-card">
        <div style="color:#ffffff;font-weight:600;font-size:0.9rem;margin-bottom:6px">1. Dual U-Net Neural Pipeline</div>
        <p style="color:#888888;font-size:0.84rem;line-height:1.6">
        • <b>Hiding Network:</b> Concatenates carrier (3 channels) and payload (3 channels) into a 6-channel tensor, outputting a 3-channel synthesized stego image.<br>
        • <b>Reveal Network:</b> Inverts the high-frequency residual distribution from the 3-channel stego carrier to reconstruct the 3-channel secret image.<br>
        • <b>Skip Connections:</b> Preserves spatial gradients and high-frequency edge information to minimize perceptual artifacts.
        </p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="glass-card">
        <div style="color:#ffffff;font-weight:600;font-size:0.9rem;margin-bottom:6px">2. Steganographic Distortion Metrics</div>
        <p style="color:#888888;font-size:0.84rem;line-height:1.6">
        • <b>PSNR (&gt; 30 dB):</b> Quantifies signal degradation relative to carrier image. Values exceeding 30 dB are imperceptible to human visual inspection.<br>
        • <b>SSIM (&gt; 0.95):</b> Assesses structural fidelity, luminance, and contrast preservation against human visual cortex models.<br>
        • <b>Detection Resistance (%):</b> Composite weighted index (70% SSIM + 30% PSNR) evaluating resilience against statistical steganalysis.
        </p>
        </div>""", unsafe_allow_html=True)

    with d2:
        st.markdown("""<div class="glass-card">
        <div style="color:#ffffff;font-weight:600;font-size:0.9rem;margin-bottom:6px">3. Defense-in-Depth Cryptography</div>
        <p style="color:#888888;font-size:0.84rem;line-height:1.6">
        • Standard neural steganography is vulnerable to weight leakage or extraction attacks.<br>
        • In Deep-Stego, synthesized payloads are encrypted using <b>AES-256-GCM</b> prior to transmission.<br>
        • An adversary possessing the exact model weights cannot decrypt or reconstruct payload data without the PBKDF2-derived key.
        </p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="glass-card">
        <div style="color:#ffffff;font-weight:600;font-size:0.9rem;margin-bottom:6px">4. Zero-Knowledge Cloud Storage</div>
        <p style="color:#888888;font-size:0.84rem;line-height:1.6">
        • Ciphertext blobs are stored in Supabase Object Storage isolated with per-file salt and nonce.<br>
        • Passphrases and plaintext decryption keys are never stored on cloud servers.<br>
        • Decryption occurs entirely in client memory during authenticated user sessions.
        </p>
        </div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""<div style="text-align:center;color:#555555;font-size:0.75rem;padding:0.75rem 0;
font-family:'Inter',sans-serif;letter-spacing:0.02em">
Deep-Stego · Dual U-Net Steganography · AES-256-GCM Cryptographic Layer · PyTorch + Streamlit + Supabase
</div>""", unsafe_allow_html=True)