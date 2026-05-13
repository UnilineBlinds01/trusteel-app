
import streamlit as st
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="TRU-STEEL Quote Tool", layout="wide")

# -------------------------
# HEADER
# -------------------------
st.title("TRU-STEEL Canopy Quote Tool")
st.caption("Professional Quoting & Ordering System")

# -------------------------
# CUSTOMER DETAILS
# -------------------------
st.sidebar.header("Customer Details")
customer = st.sidebar.text_input("Customer Name")
address = st.sidebar.text_input("Job Address")
quote_date = st.sidebar.date_input("Quote Date", date.today())

# -------------------------
# INPUTS
# -------------------------
st.sidebar.header("Project Inputs")

width = st.sidebar.number_input("Width (mm)", value=2000)
projection = st.sidebar.number_input("Projection (mm)", value=1500)
height = st.sidebar.number_input("Height (mm)", value=400)

discount_pct = st.sidebar.slider("Discount (%)", 0, 50, 30)

# -------------------------
# RATES (FROM EXCEL)
# -------------------------
panel_rate = 26.401
z_beam_rate = 8.904
hat_rate = 34.21
support_rate = 7.422
weather_rate = 16.628
hinge_rate = 17.502
cover_rate = 5.155
c_channel_rate = 8.904
bracket_rate = 2.94
adjust_bracket_rate = 3.14

# -------------------------
# CALCULATIONS
# -------------------------
width_m = width / 1000
projection_m = projection / 1000

# Panels
panel_length = projection_m + 0.05
num_panels = max(1, int(width / 120))
panel_total = num_panels * panel_length * panel_rate

# Z Beams
beam_qty = max(1, int(width / 400))
beam_total = beam_qty * 5 * z_beam_rate

# Hat Sections
hat_qty = max(2, int(width / 1500))
hat_total = hat_qty * 5 * hat_rate

# Supports
support_qty = max(2, int(width / 1000))
support_total = support_qty * (height / 1000) * support_rate

# Extra materials (BOM extension)
weather_total = 2 * weather_rate
hinge_total = 2 * hinge_rate
cover_total = 3 * cover_rate
c_channel_total = 2 * c_channel_rate
bracket_total = support_qty * bracket_rate
adjust_bracket_total = support_qty * adjust_bracket_rate

# TOTALS
subtotal = (
    panel_total
    + beam_total
    + hat_total
    + support_total
    + weather_total
    + hinge_total
    + cover_total
    + c_channel_total
    + bracket_total
    + adjust_bracket_total
)

discount = subtotal * (discount_pct / 100)
final_total = subtotal - discount

# -------------------------
# DISPLAY
# -------------------------
st.header("Quote Summary")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer")
    st.write(f"**Name:** {customer}")
    st.write(f"**Address:** {address}")
    st.write(f"**Date:** {quote_date}")

with col2:
    st.subheader("Project")
    st.write(f"Width: {width} mm")
    st.write(f"Projection: {projection} mm")
    st.write(f"Height: {height} mm")

st.divider()

# -------------------------
# MATERIAL TABLE (WITH PART NUMBERS)
# -------------------------
st.subheader("Material Breakdown")

materials = [
    ("6.3032", "Skin Panels", num_panels, panel_total),
    ("6.344102", "Z Beam", beam_qty, beam_total),
    ("6.35002", "Hat Section", hat_qty, hat_total),
    ("6.35702", "Support Arm", support_qty, support_total),
    ("6.32302", "Weather Strip", 2, weather_total),
    ("6.33312", "Hinge Beam", 2, hinge_total),
    ("6.33502", "Cover Strip", 3, cover_total),
    ("6.342101", "C Channel", 2, c_channel_total),
    ("6.37302", "Support Bracket", support_qty, bracket_total),
    ("6.37502", "Adjustable Bracket", support_qty, adjust_bracket_total),
]

st.table({
    "Part No": [m[0] for m in materials],
    "Description": [m[1] for m in materials],
    "Qty": [m[2] for m in materials],
    "Cost ($)": [round(m[3], 2) for m in materials]
})

st.divider()

# -------------------------
# TOTALS
# -------------------------
st.subheader("Pricing")

st.write(f"Subtotal: ${subtotal:.2f}")
st.write(f"Discount: -${discount:.2f}")
st.success(f"FINAL PRICE: ${final_total:.2f}")

# -------------------------
# PDF GENERATOR
# -------------------------
def create_pdf():
    file_name = "quote.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)

    c.drawString(50, 800, "TRU-STEEL CANOPY QUOTE")
    c.drawString(50, 780, f"Customer: {customer}")
    c.drawString(50, 760, f"Address: {address}")
    c.drawString(50, 740, f"Date: {quote_date}")

    y = 700
    c.drawString(50, y, "Materials:")
    y -= 20

    for part, desc, qty, cost in materials:
        c.drawString(50, y, f"{part} - {desc} (x{qty}): ${cost:.2f}")
        y -= 18

    y -= 20
    c.drawString(50, y, f"Subtotal: ${subtotal:.2f}")
    y -= 20
    c.drawString(50, y, f"Discount: ${discount:.2f}")
    y -= 20
    c.drawString(50, y, f"TOTAL: ${final_total:.2f}")

    c.save()
    return file_name

# Download button
if st.button("Download PDF Quote"):
    pdf_file = create_pdf()
    with open(pdf_file, "rb") as f:
        st.download_button("Click to Download", f, file_name="Quote.pdf")
