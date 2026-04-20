import streamlit as st
import pandas as pd
import plotly.express as px
import io

# --- STEP 1: CREATE THE DATASET (FOR EDA PURPOSES) ---
def create_dataset():
    # Real-world approximate data for India EV Market (2024-2025)
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
    df.to_csv("india_ev_data.csv", index=False)
    return df

df = create_dataset()

# --- STEP 2: DASHBOARD UI ---
st.set_page_config(page_title="EV EDA Dashboard", layout="wide")
st.title("📊 Exploratory Data Analysis: India's EV Landscape")
st.markdown("Analyzing the relationship between state-wise adoption and infrastructure.")

# Sidebar for EDA Controls
st.sidebar.header("EDA Settings")
st.sidebar.write("Dataset: `india_ev_data.csv`")
show_raw_data = st.sidebar.checkbox("Show Raw Dataset")

# --- STEP 3: KPI SUMMARY ---
total_sales = df['Total_EVs'].sum()
avg_stations = df['Charging_Stations'].mean()
top_state = df.loc[df['Total_EVs'].idxmax(), 'State']

col1, col2, col3 = st.columns(3)
col1.metric("Total EV Registrations", f"{total_sales:,}")
col2.metric("Avg Charging Stations/State", f"{int(avg_stations)}")
col3.metric("Market Leader", top_state)

st.divider()

# --- STEP 4: VISUAL ANALYSIS ---

# Row 1: Distribution & Rankings
row1_1, row1_2 = st.columns(2)

with row1_1:
    st.subheader("📍 State-wise Sales vs Stations")
    # Comparing two variables (Sales vs Infra)
    fig_scatter = px.scatter(df, x="Charging_Stations", y="Total_EVs", 
                             size="Total_EVs", color="State", hover_name="State",
                             title="Correlation: Infra vs Sales",
                             labels={"Charging_Stations": "Public Charging Points"})
    st.plotly_chart(fig_scatter, use_container_width=True)

with row1_2:
    st.subheader("🏆 Sales Leaderboard")
    fig_bar = px.bar(df.sort_values('Total_EVs', ascending=False), 
                     x='State', y='Total_EVs', color='Total_EVs',
                     title="Total EV Adoption by State")
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# Row 2: Composition Analysis
row2_1, row2_2 = st.columns(2)

with row2_1:
    st.subheader("🏍️ Vehicle Category Mix")
    # Melt data for stacked bar (Good for EDA)
    df_melted = df.melt(id_vars=['State'], value_vars=['Two_Wheelers', 'Three_Wheelers', 'Four_Wheelers'], 
                        var_name='Vehicle_Type', value_name='Count')
    fig_stack = px.bar(df_melted, x='State', y='Count', color='Vehicle_Type', 
                       title="Market Segment Distribution", barmode='stack')
    st.plotly_chart(fig_stack, use_container_width=True)

with row2_2:
    st.subheader("🥧 National Market Share")
    total_types = [df['Two_Wheelers'].sum(), df['Three_Wheelers'].sum(), df['Four_Wheelers'].sum()]
    labels = ['2-Wheelers', '3-Wheelers', '4-Wheelers']
    fig_pie = px.pie(values=total_types, names=labels, hole=0.5, 
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- STEP 5: RAW DATA VIEW ---
if show_raw_data:
    st.subheader("📄 Dataset Preview")
    st.dataframe(df)
    
    # Download button for the project report
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV for Project Report", data=csv, 
                       file_name="india_ev_eda_data.csv", mime="text/csv")
