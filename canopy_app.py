
import streamlit as st

st.title("TRU-STEEL Canopy Cost Calculator")

st.sidebar.header("Inputs")
width = st.sidebar.number_input("Width (mm)", value=2000)
projection = st.sidebar.number_input("Projection (mm)", value=1500)
height = st.sidebar.number_input("Height (mm)", value=400)
num_panels = st.sidebar.number_input("Number of Panels", value=17)

# cost assumptions from your sheet
panel_cost_per_m = 26.401
z_beam_cost_per_m = 8.904
hat_section_cost_per_m = 34.21
support_cost_per_m = 7.422

# calculations
panel_length_m = width / 1000
panel_cost = panel_length_m * num_panels * panel_cost_per_m
z_beam_cost = 12 * z_beam_cost_per_m
hat_section_cost = 3 * hat_section_cost_per_m
support_cost = 6.3 * support_cost_per_m

subtotal = panel_cost + z_beam_cost + hat_section_cost + support_cost

discount_pct = st.sidebar.slider("Discount (%)", 0, 100, 30)
discount = discount_pct / 100

total = subtotal * (1 - discount)

st.header("Cost Breakdown")
st.write(f"Panel Cost: ${panel_cost:.2f}")
st.write(f"Z Beam Cost: ${z_beam_cost:.2f}")
st.write(f"Hat Section Cost: ${hat_section_cost:.2f}")
st.write(f"Support Cost: ${support_cost:.2f}")

st.subheader("Summary")
st.write(f"Subtotal: ${subtotal:.2f}")
st.write(f"Discount: {discount_pct}%")
st.write(f"Total (Excl Labour): ${total:.2f}")
