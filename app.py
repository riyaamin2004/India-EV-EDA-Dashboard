import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. DATASET GENERATION (Embedded for Easy EDA) ---
def load_data():
    # This represents real-world trends for India EV Market 2024-25
    data = {
        'State': ['Uttar Pradesh', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'Bihar', 
                  'Rajasthan', 'Gujarat', 'Delhi', 'Kerala', 'Madhya Pradesh'],
        'EV_Sales_2024': [369102, 241941, 179037, 131482, 112000, 109393, 100000, 95000, 88000, 82000],
        'Charging_Stations': [2137, 3746, 5880, 1524, 450, 1250, 1008, 1951, 1288, 1054],
        'Two_Wheelers': [210000, 140000, 120000, 95000, 85000, 70000, 65000, 50000, 60000, 55000],
        'Four_Wheelers': [15000, 65000, 40000, 25000, 2000, 15000, 20000, 35000, 18000, 12000],
        'Three_Wheelers': [144102, 36941, 19037, 11482, 25000, 24393, 15000, 10000, 10000, 15000]
    }
    df = pd.DataFrame(data)
    df['Total_EVs'] = df['Two_Wheelers'] + df['Four_Wheelers'] + df['Three_Wheelers']
    return df

df = load_data()

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(page_title="India EV EDA Dashboard", layout="wide", page_icon="⚡")

# Custom CSS for styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_with_html=True)

st.title("⚡ India Electric Vehicle (EV) Adoption EDA")
st.markdown("An Exploratory Data Analysis of state-wise growth and infrastructure distribution.")

# --- 3. SIDEBAR CONTROLS ---
st.sidebar.header("Filter Options")
selected_state = st.sidebar.multiselect("Select States to Compare", options=df['State'].unique(), default=df['State'].unique())
filtered_df = df[df['State'].isin(selected_state)]

st.sidebar.divider()
st.sidebar.info("This dashboard uses approximate 2024-25 market data for academic EDA purposes.")

# --- 4. KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total EV Registrations", f"{filtered_df['Total_EVs'].sum():,}")
col2.metric("Top State", filtered_df.loc[filtered_df['Total_EVs'].idxmax(), 'State'])
col3.metric("Total Charging Points", f"{filtered_df['Charging_Stations'].sum():,}")
col4.metric("Avg. EVs per State", f"{int(filtered_df['Total_EVs'].mean()):,}")

st.divider()

# --- 5. CHARTS SECTION ---

# Row 1: Sales vs Infrastructure
c1, c2 = st.columns(2)

with c1:
    st.subheader("🏆 Total EV Adoption by State")
    fig1 = px.bar(filtered_df.sort_values('Total_EVs', ascending=False), 
                  x='State', y='Total_EVs', color='Total_EVs',
                  color_continuous_scale='GnBu', template='plotly_white')
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("🔌 Charging Station Distribution")
    fig2 = px.bar(filtered_df.sort_values('Charging_Stations', ascending=False), 
                  x='State', y='Charging_Stations', 
                  color_discrete_sequence=['#ff7f0e'], template='plotly_white')
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Row 2: Deep Dive Analysis
c3, c4 = st.columns(2)

with c3:
    st.subheader("📉 Infrastructure vs. Sales Correlation")
    fig3 = px.scatter(filtered_df, x="Charging_Stations", y="Total_EVs", 
                      size="Total_EVs", color="State", hover_name="State",
                      trendline="ols", # Adds a linear regression trend line for EDA
                      template='plotly_white')
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.subheader("🏍️ Market Segment Breakdown")
    # We aggregate the totals for the pie chart
    segment_totals = {
        '2-Wheelers': filtered_df['Two_Wheelers'].sum(),
        '3-Wheelers': filtered_df['Three_Wheelers'].sum(),
        '4-Wheelers': filtered_df['Four_Wheelers'].sum()
    }
    fig4 = px.pie(names=list(segment_totals.keys()), values=list(segment_totals.values()),
                  hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig4, use_container_width=True)

# --- 6. RAW DATA TABLE ---
with st.expander("Explore Raw Data"):
    st.dataframe(filtered_df.sort_values('Total_EVs', ascending=False), use_container_width=True)
