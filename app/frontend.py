import streamlit as st
import requests
from PIL import Image
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tea Leaf Disease Classifier",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg:         #0d1a12;
    --surface:    #122018;
    --surface-2:  #1a2e20;
    --border:     #2a4232;
    --green-mid:  #3d7a52;
    --green-hi:   #5db87a;
    --green-glow: rgba(93,184,122,0.15);
    --cream:      #e8e0cc;
    --cream-dim:  #a09880;
    --white:      #f5f2ec;
    --danger:     #c0614a;
    --warn:       #c09a4a;
}

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--cream);
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }

/* ── Main wrapper padding ── */
[data-testid="stAppViewContainer"] > .main > div { padding-top: 2rem !important; }
.block-container { padding: 0 3rem 3rem 3rem !important; max-width: 1200px; margin: auto; }

/* ── Hero header ── */
.hero-wrap {
    display: flex;
    align-items: flex-start;
    gap: 1.2rem;
    margin-bottom: 0.2rem;
}
.hero-icon {
    font-size: 2.8rem;
    line-height: 1;
    margin-top: 4px;
    filter: drop-shadow(0 0 12px rgba(93,184,122,0.5));
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    color: var(--white);
    line-height: 1.1;
    margin: 0;
    letter-spacing: -0.5px;
}
.hero-title em {
    font-style: italic;
    color: var(--green-hi);
}
.hero-sub {
    font-size: 0.85rem;
    color: var(--cream-dim);
    margin-top: 0.35rem;
    font-weight: 300;
    letter-spacing: 0.02em;
}
.badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 2px 8px;
    border: 1px solid var(--green-mid);
    border-radius: 2px;
    color: var(--green-hi);
    margin-top: 0.5rem;
}

/* ── Divider ── */
.styled-divider {
    height: 1px;
    background: linear-gradient(to right, var(--border), var(--green-mid) 40%, var(--border));
    margin: 1.5rem 0 2rem 0;
    border: none;
}

/* ── Section labels ── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--green-hi);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Card panels ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.5rem;
    height: 100%;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(to right, transparent, var(--green-mid), transparent);
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 1px dashed var(--border) !important;
    border-radius: 4px !important;
    background: var(--surface-2) !important;
    padding: 0.75rem !important;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover { border-color: var(--green-mid) !important; }

[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] small {
    color: var(--cream-dim) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
}
[data-testid="stFileUploaderDropzone"] { background: transparent !important; }

/* ── Image display ── */
[data-testid="stImage"] img {
    border-radius: 3px;
    border: 1px solid var(--border);
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    background: transparent !important;
    border: 1px solid var(--green-mid) !important;
    color: var(--green-hi) !important;
    border-radius: 3px !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: var(--green-glow) !important;
    border-color: var(--green-hi) !important;
    box-shadow: 0 0 16px var(--green-glow) !important;
}
.stButton > button[kind="primary"] {
    background: var(--green-mid) !important;
    color: var(--bg) !important;
    border-color: var(--green-hi) !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--green-hi) !important;
    box-shadow: 0 0 20px var(--green-glow) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--green-hi) !important; }

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 3px !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: var(--cream-dim) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.6rem !important;
    color: var(--white) !important;
}

/* ── Progress bar ── */
[data-testid="stProgress"] > div > div {
    background: var(--surface-2) !important;
    border-radius: 2px !important;
    height: 6px !important;
    border: 1px solid var(--border) !important;
}
[data-testid="stProgress"] > div > div > div {
    background: linear-gradient(to right, var(--green-mid), var(--green-hi)) !important;
    border-radius: 2px !important;
    box-shadow: 0 0 8px var(--green-glow) !important;
}
[data-testid="stProgress"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.1em !important;
    color: var(--cream-dim) !important;
}

/* ── Alert / info boxes ── */
[data-testid="stAlert"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-left: 3px solid var(--green-mid) !important;
    border-radius: 3px !important;
    color: var(--cream-dim) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
}
.stAlert[data-baseweb="notification"] { padding: 0.8rem 1rem !important; }

/* ── Success / error specifics ── */
div[data-testid="stAlert"][kind="success"],
div.stSuccess { border-left-color: var(--green-hi) !important; }
div[data-testid="stAlert"][kind="error"],
div.stError   { border-left-color: var(--danger) !important; }

/* ── Columns gap ── */
[data-testid="column"] { padding: 0 0.75rem !important; }
[data-testid="column"]:first-child { padding-left: 0 !important; }
[data-testid="column"]:last-child  { padding-right: 0 !important; }

/* ── Bottom rule ── */
.footer-rule {
    height: 1px;
    background: var(--border);
    margin: 3rem 0 1rem 0;
}
.footer-text {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #3a5242;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ── Hero header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-icon">🍃</div>
  <div>
    <h1 class="hero-title">Tea Leaf <em>Disease</em> Classifier</h1>
    <p class="hero-sub">Automated pathogen detection via deep convolutional feature analysis</p>
    <span class="badge">ResNet50 · Fine-tuned · Transfer Learning</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

# ── Two-column layout ─────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-label">01 — Input Sample</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drop a tea leaf image here, or click to browse",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption=f"↑  {uploaded_file.name}", use_container_width=True)
    else:
        st.markdown("""
        <div style="
            border: 1px dashed #2a4232;
            border-radius: 4px;
            padding: 3.5rem 1rem;
            text-align: center;
            color: #3a5242;
            font-family: 'DM Mono', monospace;
            font-size: 0.72rem;
            letter-spacing: 0.1em;
        ">
            NO SAMPLE LOADED
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-label">02 — Model Analysis</div>', unsafe_allow_html=True)

    if uploaded_file is None:
        st.info("Upload a leaf sample on the left to begin spectral analysis.")
    else:
        st.markdown(
            '<p style="font-size:0.82rem; color:#a09880; margin-bottom:1rem;">'
            'Sample received. Invoke the classification model when ready.</p>',
            unsafe_allow_html=True,
        )

        if st.button("▶  Run Disease Prediction", type="primary", use_container_width=True):
            with st.spinner("Extracting convolutional features…"):
                try:
                    uploaded_file.seek(0)
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000/predict")
                    response = requests.post(backend_url, files=files)

                    if response.status_code == 200:
                        result = response.json()
                        confidence_pct = result["confidence"] * 100

                        st.success("Analysis complete — results below")
                        st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

                        metric_col1, metric_col2 = st.columns(2)
                        metric_col1.metric(label="Classification", value=result["class"])
                        metric_col2.metric(label="Confidence", value=f"{confidence_pct:.2f}%")

                        st.markdown("<br>", unsafe_allow_html=True)
                        st.progress(result["confidence"], text="Model certainty")

                    else:
                        st.error(f"API error {response.status_code} — {response.text}")

                except requests.exceptions.ConnectionError:
                    st.error("Cannot reach backend. Ensure the inference server is running.")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-rule"></div>
<p class="footer-text">Tea Leaf Disease Classifier · ResNet50 · University of Peradeniya</p>
""", unsafe_allow_html=True)