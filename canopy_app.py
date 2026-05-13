import streamlit as st
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="TRU-STEEL Quote Tool", layout="wide")

# -------------------------
# HEADER / BRANDING
# -------------------------
st.title("TRU-STEEL Canopy Quote Tool")
st.caption("Professional Quoting System")

# -------------------------
# CUSTOMER DETAILS
# -------------------------
st.sidebar.header("Customer Details")
customer = st.sidebar.text_input("Customer Name")
address = st.sidebar.text_input("Job Address")
quote_date = st.sidebar.date_input("Date", date.today())

# -------------------------
# INPUTS
# -------------------------
st.sidebar.header("Project Inputs")
width = st.sidebar.number_input("Width (mm)", value=2000)
projection = st.sidebar.number_input("Projection (mm)", value=1500)
height = st.sidebar.number_input("Height (mm)", value=400)

discount_pct = st.sidebar.slider("Discount (%)", 0, 50, 30)

# -------------------------
# RATES (from Excel)
# -------------------------
panel_rate = 26.401
z_beam_rate = 8.904
hat_rate = 34.21
support_rate = 7.422
weather_strip_rate = 16.628
hinge_rate = 17.502
cover_rate = 5.155
bracket_rate = 2.94

# -------------------------
# CALCULATIONS
# -------------------------
width_m = width / 1000
projection_m = projection / 1000

# Panels
panel_length = projection_m + 0.05
num_panels = max(1, int(width / 120))
panel_total = num_panels * panel_length * panel_rate

# Beams
beam_qty = max(1, int(width / 400))
beam_total = beam_qty * 5 * z_beam_rate

# Hat sections
hat_qty = max(2, int(width / 1500))
hat_total = hat_qty * 5 * hat_rate

# Supports
support_qty = max(2, int(width / 1000))
support_total = support_qty * (height / 1000) * support_rate

# EXTRA ITEMS (from Excel BOM style)
weather_total = 2 * weather_strip_rate
hinge_total = 2 * hinge_rate
cover_total = 3 * cover_rate
bracket_total = support_qty * bracket_rate

# Subtotal
subtotal = (
    panel_total
    + beam_total
    + hat_total
    + support_total
    + weather_total
    + hinge_total
    + cover_total
    + bracket_total
)

discount = subtotal * (discount_pct / 100)
final_total = subtotal - discount

# -------------------------
# DISPLAY (PREMIUM UI)
# -------------------------
st.header("Quote Summary")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer Info")
    st.write(f"**Name:** {customer}")
    st.write(f"**Address:** {address}")
    st.write(f"**Date:** {quote_date}")

with col2:
    st.subheader("Project Specs")
    st.write(f"Width: {width} mm")
    st.write(f"Projection: {projection} mm")
    st.write(f"Height: {height} mm")

st.divider()

st.subheader("Materials")

st.table({
    "Item": [
        "Panels",
        "Z Beams",
        "Hat Sections",
        "Supports",
        "Weather Strip",
        "Hinge Beam",
        "Cover Strip",
        "Brackets"
    ],
    "Qty": [
        num_panels,
        beam_qty,
        hat_qty,
        support_qty,
        2,
        2,
        3,
        support_qty
    ],
    "Cost ($)": [
        panel_total,
        beam_total,
        hat_total,
        support_total,
        weather_total,
        hinge_total,
        cover_total,
        bracket_total
    ]
})

st.divider()

st.subheader("Total")

st.write(f"Subtotal: ${subtotal:.2f}")
st.write(f"Discount: -${discount:.2f}")

st.success(f"FINAL PRICE: ${final_total:.2f}")

# -------------------------
# PDF GENERATOR
# -------------------------
def create_pdf():
    file_name = "quote.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)

    c.drawString(50, 800, "TRU-STEEL QUOTE")
    c.drawString(50, 780, f"Customer: {customer}")
    c.drawString(50, 760, f"Address: {address}")
    c.drawString(50, 740, f"Date: {quote_date}")

    y = 700
    c.drawString(50, y, "Materials:")
    y -= 20

    items = [
        ("Panels", panel_total),
        ("Z Beams", beam_total),
        ("Hat Sections", hat_total),
        ("Supports", support_total),
        ("Weather Strip", weather_total),
        ("Hinge Beam", hinge_total),
        ("Cover Strip", cover_total),
        ("Brackets", bracket_total),
    ]

    for item, cost in items:
        c.drawString(50, y, f"{item}: ${cost:.2f}")
        y -= 20

    y -= 20
    c.drawString(50, y, f"Subtotal: ${subtotal:.2f}")
    y -= 20
    c.drawString(50, y, f"Discount: ${discount:.2f}")
    y -= 20
    c.drawString(50, y, f"TOTAL: ${final_total:.2f}")

    c.save()
    return file_name

if st.button("Download PDF Quote"):
    pdf_file = create_pdf()
    with open(pdf_file, "rb") as f:
        st.download_button("Click to Download", f, file_name="Quote.pdf")
