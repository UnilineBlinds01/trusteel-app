import streamlit as st

st.set_page_config(layout="wide")

# -------------------------
# DARK UI STYLE
# -------------------------
st.markdown("""
<style>
body {
    background-color: #0b0b0b;
    color: white;
}
.block-container {
    padding-top: 1rem;
}

/* Sections */
.section {
    background: linear-gradient(145deg, #1a1a1a, #111);
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 25px;
}

/* Cards */
.card {
    background: #222;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    border: 1px solid #333;
}

/* Buttons */
.stButton button {
    background: #ff6a00;
    color: white;
    border-radius: 10px;
    height: 55px;
    font-size: 18px;
}

.orange {
    color: #ff6a00;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.markdown("""
<span style='color:#888;'>TRU-STEEL</span>
<h1>Canopy Awning Costing</h1>
""", unsafe_allow_html=True)

# -------------------------
# DIMENSIONS
# -------------------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("Dimensions")

col1, col2 = st.columns(2)

with col1:
    width = st.number_input("Width (mm)", value=2000)

with col2:
    projection = st.number_input("Projection (mm)", value=1500)

height = st.number_input("Height / Rise (mm)", value=400)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# CONFIGURATION
# -------------------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("Configuration")

col1, col2 = st.columns(2)

with col1:
    support = st.radio("Support Type", ["Wall", "Ground"])

with col2:
    beam = st.radio("Beam Type", ["Z Beam", "Small C"])

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# PRICING
# -------------------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("Pricing")

discount_pct = st.number_input("Trade Discount (%)", value=30)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# CALCULATIONS
# -------------------------
width_m = width / 1000
projection_m = projection / 1000

panels = int(width / 120)
panel_length = int((projection_m + 0.05) * 1000)

beams = int(width / 400)
hats = max(2, int(width / 1500))
supports = max(2, int(width / 1000))

# COSTS
subtotal = (
    panels * 26.401 +
    beams * 8.904 * 5 +
    hats * 34.21 * 5 +
    supports * (height / 1000) * 7.422 +
    2 * 16.628 +
    2 * 17.502 +
    3 * 5.155 +
    supports * 2.94
)

discount = subtotal * (discount_pct / 100)
total = subtotal - discount

# -------------------------
# AUTO CALCULATED
# -------------------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("Auto-Calculated")

c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)

c1.markdown(f"<div class='card'>Panels<br><b>{panels}</b></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='card'>Panel Length<br><b>{panel_length} mm</b></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='card'>Z/C Beams<br><b>{beams}</b></div>", unsafe_allow_html=True)

c4.markdown(f"<div class='card'>Hat Sections<br><b>{hats}</b></div>", unsafe_allow_html=True)
c5.markdown(f"<div class='card'>Supports<br><b>{supports}</b></div>", unsafe_allow_html=True)
c6.markdown(f"<div class='card'>Est Total<br><b>${total:.2f}</b></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# MATERIAL LIST
