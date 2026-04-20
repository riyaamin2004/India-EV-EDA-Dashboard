import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. PAGE SETTINGS ---
st.set_page_config(page_title="India EV Analysis", layout="wide")

st.title("📊 India Electric Vehicle (EV) EDA Dashboard")
st.markdown("Using real-world market data to analyze adoption trends across states and categories.")

# --- 2. DATA LOADING ---
@st.cache_data
def load_data():
    try:
        # This looks for the CSV file in your GitHub folder
        df = pd.read_csv("india_ev_data.csv")
        return df
    except FileNotFoundError:
        st.error("❌ **Dataset Not Found!** Please upload 'india_ev_data.csv' to your GitHub repository.")
        return None

df = load_data()

# --- 3. DASHBOARD LOGIC ---
if df is not None:
    # Sidebar Filters
    st.sidebar.header("Filter Analytics")
    
    # Selecting State (Automatically finds the 'State' column)
    state_col = [c for c in df.columns if 'State' in c or 'UT' in c][0]
    all_states = sorted(df[state_col].unique())
    selected_states = st.sidebar.multiselect("Select States", options=all_states, default=all_states[:5])

    # Filter Data based on Selection
    filtered_df = df[df[state_col].isin(selected_states)]

    # --- 4. KPI SUMMARY ---
    # We identify numeric columns for sales/counts
    num_cols = filtered_df.select_dtypes(include=['number']).columns
    total_sales = filtered_df[num_cols[0]].sum() if len(num_cols) > 0 else 0

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total EVs in Selection", f"{total_sales:,}")
    kpi2.metric("States Analyzed", len(selected_states))
    kpi3.metric("Data Source", "Kaggle / Vahan")

    st.divider()

    # --- 5. VISUALIZATIONS ---
    row1_left, row1_right = st.columns(2)

    with row1_left:
        st.subheader("🏁 State-wise Comparison")
        # Creating a bar chart of the first numeric column vs State
        fig_bar = px.bar(filtered_df, x=state_col, y=num_cols[0], 
                         color=num_cols[0], color_continuous_scale='Turbo')
        st.plotly_chart(fig_bar, use_container_width=True)

    with row1_right:
        st.subheader("🥧 Market Distribution")
        # Pie chart showing the spread across selected states
        fig_pie = px.pie(filtered_df, names=state_col, values=num_cols[0], hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

    # --- 6. ADVANCED EDA: RELATIONSHIPS ---
    st.subheader("🧐 Deep Dive: Data Distribution")
    
    if len(num_cols) >= 2:
        # Scatter plot to show correlation between two metrics if available
        fig_scatter = px.scatter(filtered_df, x=num_cols[0], y=num_cols[1], 
                                 color=state_col, size=num_cols[0], 
                                 hover_name=state_col, template="plotly_dark")
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Add more columns to the CSV to see correlation analysis.")

    # Show raw data at the bottom
    with st.expander("📄 View Filtered Raw Data"):
        st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("Waiting for dataset upload...")
