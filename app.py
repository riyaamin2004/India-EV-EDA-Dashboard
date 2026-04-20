import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="India EV Market EDA", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    div.stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e1e4e8; }
    </style>
    """, unsafe_with_html=True)

# --- 2. LOAD DATA ---
@st.cache_data
def load_data():
    try:
        # Tries to load your Kaggle file
        df = pd.read_csv("india_ev_data.csv")
        # Standardizing column names for consistency
        df.columns = [c.replace(' ', '_').strip() for c in df.columns]
        return df
    except:
        st.error("⚠️ Dataset not found. Please upload 'india_ev_data.csv' to your GitHub.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- 3. SIDEBAR FILTERS ---
    st.sidebar.header("🔍 EDA Filters")
    
    # Dynamically find columns for filtering
    state_col = [c for c in df.columns if 'State' in c or 'UT' in c][0]
    year_col = [c for c in df.columns if 'Year' in c][0]
    sales_col = [c for c in df.columns if 'Sales' in c or 'Quantity' in c][0]
    cat_col = [c for c in df.columns if 'Category' in c or 'Type' in c][0]

    states = st.sidebar.multiselect("Select States", options=sorted(df[state_col].unique()), default=df[state_col].unique()[:5])
    years = st.sidebar.slider("Select Year Range", int(df[year_col].min()), int(df[year_col].max()), (2020, 2024))

    # Apply Filters
    mask = (df[state_col].isin(states)) & (df[year_col].between(years[0], years[1]))
    filtered_df = df[mask]

    # --- 4. DASHBOARD HEADER ---
    st.title("📊 India EV Market - Exploratory Data Analysis")
    st.markdown(f"Performing analysis from **{years[0]}** to **{years[1]}** across **{len(states)}** states.")

    # KPI Metrics
    m1, m2, m3 = st.columns(3)
    total_sales = filtered_df[sales_col].sum()
    m1.metric("Total EV Sales", f"{total_sales:,}")
    m2.metric("Leading Category", filtered_df.groupby(cat_col)[sales_col].sum().idxmax())
    m3.metric("Top Growth State", filtered_df.groupby(state_col)[sales_col].sum().idxmax())

    st.divider()

    # --- 5. VISUALIZATIONS (The EDA Core) ---
    row1_left, row1_right = st.columns(2)

    with row1_left:
        st.subheader("📈 Sales Growth Over Time")
        # Line chart showing trends
        trend_df = filtered_df.groupby(year_col)[sales_col].sum().reset_index()
        fig_line = px.line(trend_df, x=year_col, y=sales_col, markers=True, 
                           template="plotly_white", line_shape="spline")
        st.plotly_chart(fig_line, use_container_width=True)

    with row1_right:
        st.subheader("🏁 State-wise Competition")
        # Bar chart for state comparison
        state_comp = filtered_df.groupby(state_col)[sales_col].sum().reset_index().sort_values(sales_col)
        fig_bar = px.bar(state_comp, x=sales_col, y=state_col, orientation='h', color=sales_col)
        st.plotly_chart(fig_bar, use_container_width=True)

    row2_left, row2_right = st.columns(2)

    with row2_left:
        st.subheader("🏍️ Vehicle Category Share")
        # Pie chart for segments
        cat_share = filtered_df.groupby(cat_col)[sales_col].sum().reset_index()
        fig_pie = px.pie(cat_share, names=cat_col, values=sales_col, hole=0.5)
        st.plotly_chart(fig_pie, use_container_width=True)

    with row2_right:
        st.subheader("🧐 Yearly Distribution of Segments")
        # Stacked bar for deeper EDA
        stack_df = filtered_df.groupby([year_col, cat_col])[sales_col].sum().reset_index()
        fig_stack = px.bar(stack_df, x=year_col, y=sales_col, color=cat_col, barmode="group")
        st.plotly_chart(fig_stack, use_container_width=True)

    # --- 6. DATA TABLE ---
    with st.expander("📂 View Filtered Dataset"):
        st.dataframe(filtered_df, use_container_width=True)
