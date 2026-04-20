import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import plotly.graph_objects as go
from utils.lookup_data import (
    get_state_data,
    get_all_states,
    CROP_EMOJI,
    CROP_PRICE_PER_QUINTAL,
    SEASON_MAP
)

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌾 Crop Intelligence System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg,#f0f7f0,#e8f5e9); }
.metric-card { background:white; padding:1rem; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center; }
.section-title { font-size:1.3rem; font-weight:700; color:#1b5e20; margin-bottom:1rem; }
.footer { text-align:center; color:#777; font-size:0.8rem; margin-top:2rem; }
</style>
""", unsafe_allow_html=True)

# ─── Load Models ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    crop_model   = joblib.load("models/crop_model.pkl")
    yield_model  = joblib.load("models/yield_model.pkl")
    le_rec       = joblib.load("models/label_encoder.pkl")
    scaler       = joblib.load("models/scaler.pkl")
    le_state     = joblib.load("models/le_state.pkl")
    le_crop_yld  = joblib.load("models/le_crop_yield.pkl")
    le_season    = joblib.load("models/le_season.pkl")
    feat_cols    = joblib.load("models/feature_columns.pkl")
    with open("models/metadata.json") as f:
        meta = json.load(f)
    return crop_model, yield_model, le_rec, scaler, le_state, le_crop_yld, le_season, feat_cols, meta

(
    crop_model,
    yield_model,
    le_rec,
    scaler,
    le_state,
    le_crop_yld,
    le_season,
    feat_cols,
    meta
) = load_models()

# ─── Sidebar Inputs ────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🌾 Crop Intelligence")
    selected_state = st.selectbox("State", get_all_states())
    season_display = st.selectbox("Season", list(SEASON_MAP.keys()))
    area_ha = st.number_input("Farm Area (hectares)", 0.5, 10000.0, 5.0, 0.5)
    crop_year = st.slider("Crop Year", 2000, 2026, 2024)
    top_n = st.slider("Top Recommendations", 1, 5, 3)
    show_profit = st.checkbox("Show Revenue", True)
    predict_btn = st.button("🔍 Analyze & Recommend")

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="metric-card">
<h1>🌾 Crop Intelligence System</h1>
<p>ML-powered crop & yield prediction for Indian agriculture</p>
</div>
""", unsafe_allow_html=True)

if not predict_btn:
    st.info("👈 Select inputs from sidebar and click **Analyze & Recommend**")
    st.stop()

# ─── Environment Data ──────────────────────────────────────────────────────────
env = get_state_data(selected_state)
season_raw = SEASON_MAP.get(season_display, season_display)

# ─── Crop Recommendation ───────────────────────────────────────────────────────
rec_input = pd.DataFrame([[ 
    env["N"], env["P"], env["K"],
    env["temperature"], env["humidity"],
    env["ph"], env["rainfall"]
]], columns=feat_cols)

rec_scaled = scaler.transform(rec_input)
probs = crop_model.predict_proba(rec_scaled)[0]
top_idx = np.argsort(probs)[::-1][:top_n]
top_crops = le_rec.inverse_transform(top_idx)
top_probs = probs[top_idx]

# ─── FIXED Yield Prediction Function ───────────────────────────────────────────
def predict_yield(crop_name, state, season, year, area):
    try:
        # Crop matching
        crop_clean = crop_name.lower().strip()
        matched_crop = next(
            (c for c in le_crop_yld.classes_ if c.lower().strip() == crop_clean),
            None
        )
        if matched_crop is None:
            return None

        # State check
        if state not in le_state.classes_:
            return None

        # Season matching
        season_clean = season.lower()
        matched_season = min(
            le_season.classes_,
            key=lambda s: abs(len(s.lower()) - len(season_clean))
        )

        inp = pd.DataFrame([[
            le_state.transform([state])[0],
            le_crop_yld.transform([matched_crop])[0],
            year,
            le_season.transform([matched_season])[0],
            area
        ]], columns=["State_Name","Crop","Crop_Year","Season","Area"])

        return max(0, yield_model.predict(inp)[0])

    except:
        return None

# ─── Results Computation ───────────────────────────────────────────────────────
results = []
for crop, prob in zip(top_crops, top_probs):
    yld = predict_yield(crop, selected_state, season_raw, crop_year, area_ha)
    total_prod = yld * area_ha if yld else None
    price = CROP_PRICE_PER_QUINTAL.get(crop.lower())
    revenue = total_prod * 10 * price if (total_prod and price) else None

    results.append({
        "crop": crop,
        "prob": prob,
        "yield": yld,
        "total": total_prod,
        "revenue": revenue,
        "emoji": CROP_EMOJI.get(crop.lower(), "🌿")
    })

# ─── Results Display ───────────────────────────────────────────────────────────
st.markdown(f"## 📍 Results for **{selected_state}** ({season_display} {crop_year})")

for i, r in enumerate(results):
    cols = st.columns(5)
    cols[0].markdown(f"### {r['emoji']} {r['crop']}")
    cols[1].metric("Suitability", f"{r['prob']*100:.1f}%")
    cols[2].metric("Yield / ha", f"{r['yield']:.2f} t" if r["yield"] else "N/A")
    cols[3].metric("Total Prod.", f"{r['total']:.1f} t" if r["total"] else "N/A")
    if show_profit:
        cols[4].metric("Revenue", f"₹{r['revenue']:,.0f}" if r["revenue"] else "Unavailable")

st.markdown("---")

# ─── Charts ────────────────────────────────────────────────────────────────────
fig = go.Figure(go.Bar(
    x=[r["crop"] for r in results],
    y=[r["prob"]*100 for r in results],
    text=[f"{r['prob']*100:.1f}%" for r in results],
    textposition="outside"
))
fig.update_layout(
    title="Crop Suitability (%)",
    yaxis_title="Suitability",
    height=350
)
st.plotly_chart(fig, use_container_width=True)

# ─── Summary Table ─────────────────────────────────────────────────────────────
df = pd.DataFrame([{
    "Crop": r["crop"],
    "Suitability (%)": round(r["prob"]*100,1),
    "Yield (t/ha)": round(r["yield"],2) if r["yield"] else None,
    "Total (t)": round(r["total"],2) if r["total"] else None,
    "Revenue (₹)": round(r["revenue"],0) if r["revenue"] else None
} for r in results])

st.dataframe(df, use_container_width=True)

st.download_button(
    "⬇️ Download CSV",
    df.to_csv(index=False),
    "crop_results.csv",
    "text/csv"
)

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
🌾 Crop Intelligence System • Streamlit + ML
</div>
""", unsafe_allow_html=True)