import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Setup Page
st.set_page_config(page_title="EV Dashboard", layout="wide")

# 2. Create Data directly in the code (No CSV needed)
data = {
    'State': ['UP', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'Bihar', 'Delhi'],
    'Total_EVs': [369102, 241941, 179037, 131482, 112000, 95000],
    'Charging_Stations': [2137, 3746, 5880, 1524, 450, 1951],
    'Two_Wheelers': [210000, 140000, 120000, 95000, 85000, 50000]
}
df = pd.DataFrame(data)

# 3. UI Elements
st.title("⚡ India EV Adoption Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("State-wise Sales")
    fig1 = px.bar(df, x='State', y='Total_EVs', color='State')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Charging Infrastructure")
    fig2 = px.pie(df, values='Charging_Stations', names='State', hole=0.3)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Raw EDA Data")
st.dataframe(df)
