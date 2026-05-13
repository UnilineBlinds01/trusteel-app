import streamlit as st
from datetime import date

st.set_page_config(page_title="TRU-STEEL Quote Tool", layout="wide")

# -------------------------
# HEADER
# -------------------------
st.title("TRU-STEEL Canopy Quote Tool")

# -------------------------
# CUSTOMER DETAILS
# -------------------------
st.sidebar.header("Customer Details")
customer = st.sidebar.text_input("Customer Name")
address = st.sidebar.text_input("Job Address")
quote_date = st.sidebar.date_input("Date", date.today())

# -------------------------
# INPUTS (from your Excel)
# -------------------------
st.sidebar.header("Project Inputs")

width = st.sidebar.number_input("Width (mm)", value=2000)
projection = st.sidebar.number_input("Projection (mm)", value=1500)
height = st.sidebar.number_input("Height (mm)", value=400)

support_type = st.sidebar.selectbox("Support Location", ["Wall", "Ground"])
beam_type = st.sidebar.selectbox("Beam Type", ["Z Beam", "C Channel"])

discount_pct = st.sidebar.slider("Discount (%)", 0, 50, 30)

# -------------------------
# CONSTANTS (Excel values)
# -------------------------
panel_rate = 26.401
z_beam_rate = 8.904
hat_rate = 34.21
support_rate = 7.422

# -------------------------
# CALCULATIONS (matching your sheet logic)
# -------------------------
width_m = width / 1000
projection_m = projection / 1000

# Panels
panel_length = projection_m + 0.05
num_panels = max(1, int(width / 120))
panel_total = num_panels * panel_length * panel_rate

# Beams
beam_qty = max(1, int(width / 400))
beam_rate = z_beam_rate
beam_total = beam_qty * 5 * beam_rate

# Hat sections
hat_qty = max(2, int(width / 1500))
hat_total = hat_qty * 5 * hat_rate

# Supports
support_qty = max(2, int(width / 1000))
support_total = support_qty * (height / 1000) * support_rate

# Subtotal
subtotal = panel_total + beam_total + hat_total + support_total

# Discount
discount = subtotal * (discount_pct / 100)
final_total = subtotal - discount

# -------------------------
# OUTPUT
# -------------------------
st.header("Quote")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer")
    st.write(f"Name: {customer}")
    st.write(f"Address: {address}")
    st.write(f"Date: {quote_date}")

with col2:
    st.subheader("Project")
    st.write(f"Width: {width} mm")
    st.write(f"Projection: {projection} mm")
    st.write(f"Height: {height} mm")
    st.write(f"Beam: {beam_type}")

st.divider()

st.subheader("Material Breakdown")

st.write(f"Panels ({num_panels}): ${panel_total:.2f}")
st.write(f"Beams ({beam_qty}): ${beam_total:.2f}")
st.write(f"Hat Sections ({hat_qty}): ${hat_total:.2f}")
st.write(f"Supports ({support_qty}): ${support_total:.2f}")

st.divider()

st.subheader("Totals")

st.write(f"Subtotal: ${subtotal:.2f}")
st.write(f"Discount: -${discount:.2f}")

st.success(f"FINAL PRICE: ${final_total:.2f} (Excl Labour)")
