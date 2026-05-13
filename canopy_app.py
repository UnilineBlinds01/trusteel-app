import streamlit as st
from datetime import date

st.set_page_config(page_title="TRU-STEEL Costing", layout="wide")

# -------------------------
# CUSTOM STYLING (DARK UI)
# -------------------------
st.markdown("""
<style>
body {
    background-color: #0e0e0e;
    color: white;
}
.block-container {
    padding-top: 2rem;
}
.section {
    background-color: #1a1a1a;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}
.card {
    background-color: #2a2a2a;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
.orange {
    color: #ff6a00;
}
.stButton>button {
    background-color: #ff6a00;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.markdown("""
## TRU-STEEL  
# Canopy Awning Costing
""")

# -------------------------
# DIMENSIONS
# -------------------------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("📏 Dimensions")

col1, col2 = st.columns(2)

with col1:
    width = st.number_input("Width (mm)", value=2000)

with col2:
    projection = st.number_input("Projection (mm)", value=1500)

height = st.number_input("Height / Rise (mm)", value=400)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# CONFIGURATION
# -------------------------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("⚙️ Configuration")

col1, col2 = st.columns(2)

with col1:
    support = st.radio("Support Type", ["Wall", "Ground"])

with col2:
    beam = st.radio("Beam Type", ["Z Beam", "Small C"])

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# PRICING
# -------------------------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("💰 Pricing")

discount_pct = st.number_input("Trade Discount (%)", value=30)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# CALCULATIONS (FROM EXCEL)
# -------------------------
panel_rate = 26.401
z_beam_rate = 8.904
hat_rate = 34.21
support_rate = 7.422
weather_rate = 16.628
hinge_rate = 17.502
cover_rate = 5.155
bracket_rate = 2.94

width_m = width / 1000
projection_m = projection / 1000

num_panels = int(width / 120)
panel_length = projection_m + 0.05
panel_total = num_panels * panel_length * panel_rate

beam_qty = int(width / 400)
beam_total = beam_qty * 5 * z_beam_rate

hat_qty = max(2, int(width / 1500))
hat_total = hat_qty * 5 * hat_rate

support_qty = max(2, int(width / 1000))
support_total = support_qty * (height / 1000) * support_rate

weather_total = 2 * weather_rate
hinge_total = 2 * hinge_rate
cover_total = 3 * cover_rate
bracket_total = support_qty * bracket_rate

subtotal = (
    panel_total + beam_total + hat_total +
    support_total + weather_total +
    hinge_total + cover_total + bracket_total
)

discount = subtotal * (discount_pct / 100)
final_total = subtotal - discount

# -------------------------
# AUTO CALCULATED SECTION
# -------------------------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("📊 Auto-Calculated")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'<div class="card">Panels<br><b>{num_panels}</b></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="card">Panel Length<br><b>{int(panel_length*1000)} mm</b></div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="card">Beams<br><b>{beam_qty}</b></div>', unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown(f'<div class="card">Hat Sections<br><b>{hat_qty}</b></div>', unsafe_allow_html=True)

with col5:
    st.markdown(f'<div class="card">Supports<br><b>{support_qty}</b></div>', unsafe_allow_html=True)

with col6:
    st.markdown(f'<div class="card">Est Total<br><b>${final_total:.2f}</b></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# MATERIAL LIST (LIKE YOUR SECOND SCREEN)
# -------------------------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("📦 Materials")

materials = [
    ("6.3032", "Skin Panels", num_panels, panel_total),
    ("6.344102", "Z Beam", beam_qty, beam_total),
    ("6.35002", "Hat Section", hat_qty, hat_total),
    ("6.35702", "Support Arm", support_qty, support_total),
    ("6.32302", "Weather Strip", 2, weather_total),
    ("6.33312", "Hinge Beam", 2, hinge_total),
    ("6.33502", "Cover Strip", 3, cover_total),
    ("6.37302", "Support Bracket", support_qty, bracket_total),
]

for part, desc, qty, cost in materials:
    st.markdown(f"""
    **{part} — {desc}**  
    Qty: {qty}  
    Cost: ${cost:.2f}
    """)
    st.divider()

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# TOTAL
# -------------------------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("🏷 Price Summary")

st.write(f"Subtotal: ${subtotal:.2f}")
st.write(f"Trade Discount ({discount_pct}%): -${discount:.2f}")

st.markdown(f"## <span class='orange'>TOTAL: ${final_total:.2f}</span>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# CTA BUTTON
# -------------------------
st.button("View Full Quote ➜")
