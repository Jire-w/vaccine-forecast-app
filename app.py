import streamlit as st
import pandas as pd

# App title
st.title("Vaccine Forecasting and Supply Planning App")

# Sidebar inputs
st.sidebar.header("Planning Inputs")

# Planning year
planning_year = st.sidebar.number_input("Planning Year", min_value=2024, max_value=2100, value=2025)

# Vaccine selection
vaccine = st.sidebar.selectbox("Select Vaccine", ["HPV", "Measles", "Polio", "COVID-19"])

# Target population
population = st.sidebar.number_input("Target Population (number of eligible individuals)", min_value=0, value=100000)

doses_per_person = st.sidebar.number_input("Doses per Person", min_value=1, value=2)

coverage_target = st.sidebar.slider("Coverage Target (%)", min_value=50, max_value=100, value=90)

wastage_rate = st.sidebar.slider("Wastage Rate (%)", min_value=0, max_value=50, value=10)

buffer_stock = st.sidebar.slider("Buffer Stock (%)", min_value=0, max_value=50, value=25)

stock_on_hand = st.sidebar.number_input("Stock on Hand (doses)", min_value=0, value=5000)

incoming_deliveries = st.sidebar.number_input("Incoming Deliveries (doses)", min_value=0, value=10000)

# Calculate needs
programmatic_need = population * doses_per_person * (coverage_target / 100)
accounted_wastage = programmatic_need * (1 + (wastage_rate / 100))
total_requirement = accounted_wastage * (1 + (buffer_stock / 100))
procurement_need = total_requirement - stock_on_hand - incoming_deliveries

# Display results
st.header("Forecast Results")

st.metric("Programmatic Need (doses)", f"{programmatic_need:,.0f}")
st.metric("After Wastage (doses)", f"{accounted_wastage:,.0f}")
st.metric("With Buffer Stock (doses)", f"{total_requirement:,.0f}")

if procurement_need > 0:
    st.success(f"**Procurement Need:** {procurement_need:,.0f} doses")
else:
    st.info("No additional procurement needed; current stocks cover the requirement.")

# Summary table
data = {
    "Category": ["Programmatic Need", "After Wastage", "With Buffer Stock", "Stock on Hand", "Incoming Deliveries", "Procurement Need"],
    "Doses": [programmatic_need, accounted_wastage, total_requirement, stock_on_hand, incoming_deliveries, max(procurement_need, 0)]
}
df = pd.DataFrame(data)

st.subheader("Summary Table")
st.table(df)

# Export option
if st.button("Export Summary to CSV"):
    df.to_csv("forecast_summary.csv", index=False)
    st.success("Summary exported as 'forecast_summary.csv'")
