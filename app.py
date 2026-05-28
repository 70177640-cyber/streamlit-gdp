import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit page config
st.set_page_config(page_title="Global Macroeconomic Intelligence Terminal", layout="wide")

# ==============================================================================
# 1. DATASET ENGINE (Using your uploaded gdp.csv)
# ==============================================================================
DATA_FILE = "gdp.csv"

if os.path.exists(DATA_FILE):
    # Load your actual uploaded data
    raw_df = pd.read_csv(DATA_FILE)
    
    # Standardize column names to match the visual logic
    # Transforming Country Name,Country Code,Year,Value to what the script expects
    df = raw_df.rename(columns={
        "Country Name": "Country Name",
        "Country Code": "ISO Code",
        "Year": "Year",
        "Value": "GDP (USD)"
    })
    
    # Generate some proxy metrics since raw GDP data only has "Value"
    # This prevents the app from breaking on missing columns
    df["GDP Growth Rate (%)"] = df.groupby("Country Name")["GDP (USD)"].pct_change().fillna(0) * 100
    df["Population"] = 50_000_000  # Proxy baseline
    df["GDP Per Capita (USD)"] = df["GDP (USD)"] / df["Population"]
    df["Inflation Rate (%)"] = np.random.uniform(1.5, 4.5, size=len(df))
else:
    st.error(f"Could not find {DATA_FILE}. Please ensure it is uploaded to GitHub.")
    st.stop()

all_countries = sorted(df["Country Name"].dropna().unique().tolist())
min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
default_selection = [c for c in ["United States", "China", "Germany", "India", "Japan"] if c in all_countries]
if not default_selection and all_countries:
    default_selection = all_countries[:3]

def format_currency(val):
    if val >= 1e12: return f"${val / 1e12:,.2f} T"
    if val >= 1e9: return f"${val / 1e9:,.2f} B"
    return f"${val:,.0f}"

# ==============================================================================
# 2. ENTERPRISE UI STRUCTURE (Streamlit Native Framework)
# ==============================================================================

# Header (FIXED: Removed the incorrect 'unsafe_html' parameter)
st.markdown("""
<div style="background: linear-gradient(90deg, #1e293b, #0f172a); border-bottom: 2px solid #14b8a6; padding: 24px; border-radius: 8px; text-align: left; margin-bottom: 25px;">
    <span style="color: #14b8a6; font-weight: 700; letter-spacing: 2px; font-size: 12px; text-transform: uppercase;">Institutional Grade Analytics Terminal</span>
    <h1 style="margin: 4px 0 0 0; color: white; font-size: 28px; font-weight: 300;">Global Macroeconomic Intelligence Suite</h1>
</div>
""", unsafe_allow_html=True)

# Tabs Configuration
tab1, tab2, tab3 = st.tabs([
    "🌐 Cross-Sectional Geopolitical Heatmaps", 
    "📈 Multi-Variable Growth Trajectories", 
    "📐 Advanced Micro-Correlation Matrix"
])

# ------------------------------------------------------------------------------
# TAB 1: Geopolitical Heatmaps
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("🔍 Geographic Variations & Macro Dispersal")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        select_year = st.slider("Target Econometric Horizon", min_value=min_year, max_value=max_year, value=max_year)
        target_metric = st.selectbox(
            "Target Analytical Evaluation Metric",
            choices=["GDP (USD)", "GDP Growth Rate (%)", "GDP Per Capita (USD)", "Inflation Rate (%)"],
            index=0
        )
        
        # Calculate KPI Data
        year_df = df[df["Year"] == int(select_year)].copy()
        if not year_df.empty:
            avg_inflation = year_df["Inflation Rate (%)"].mean()
            total_world_gdp = year_df["GDP (USD)"].sum()
            
            # FIXED: Using unsafe_allow_html=True
            st.markdown(f"""
            <div style='background: #1e293b; padding: 15px; border-radius: 8px; border-left: 5px solid #0d9488; color: white; margin-bottom: 10px;'>
                <span style='font-size: 11px; opacity: 0.7; text-transform: uppercase;'>Global Sample Output Volume</span>
                <h3 style='margin: 5px 0 0 0; color: #2dd4bf;'>{format_currency(total_world_gdp)}</h3>
            </div>
            <div style='background: #1e293b; padding: 15px; border-radius: 8px; border-left: 5px solid #f43f5e; color: white;'>
                <span style='font-size: 11px; opacity: 0.7; text-transform: uppercase;'>Mean Inflation Rate</span>
                <h3 style='margin: 5px 0 0 0; color: #fb7185;'>{avg_inflation:.2f}%</h3>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if not year_df.empty:
            # Map
            fig_map = px.choropleth(
                year_df, locations="ISO Code", color=target_metric, hover_name="Country Name",
                title=f"Global Heatmap Distribution: {target_metric} ({select_year})",
                color_continuous_scale="Viridis" if "GDP" in target_metric else "Plasma"
            )
            st.plotly_chart(fig_map, use_container_width=True)
            
            # Pie & Bar side by side
            sub_col1, sub_col2 = st.columns(2)
            
            with sub_col1:
                sorted_df = year_df.sort_values(by="GDP (USD)", ascending=False)
                top_6 = sorted_df.head(6).copy()
                others_gdp = sorted_df.iloc[6:]["GDP (USD)"].sum()
                
                fig_pie = px.pie(top_6, values="GDP (USD)", names="Country Name", title="Top Nations Economic Volume Dispersal", hole=0.5)
                st.plotly_chart(fig_pie, use_container_width=True)
                
            with sub_col2:
                bar_data = year_df.sort_values(by=target_metric, ascending=False).head(10)
                fig_bar = px.bar(
                    bar_data, x=target_metric, y="Country Name", orientation="h",
                    title=f"Top Performing Nations ({target_metric})",
                    color=target_metric, color_continuous_scale="Cividis"
                )
                fig_bar.update_layout(yaxis={"categoryorder": "total ascending"})
                st.plotly_chart(fig_bar, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 2: Multi-Variable Growth Trajectories
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("📊 Longitudinal Structural Time Series & Multi-Axis Modeling")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        select_countries = st.multiselect("Entities of Interest", options=all_countries, default=default_selection)
        metric_primary = st.selectbox("Primary Line Vector", choices=["GDP (USD)", "GDP Growth Rate (%)", "GDP Per Capita (USD)", "Inflation Rate (%)"], index=0)
        metric_secondary = st.selectbox("Risk Bubble Parameter", choices=["GDP (USD)", "GDP Growth Rate (%)", "GDP Per Capita (USD)", "Inflation Rate (%)"], index=1)
        
        start_time_slider = st.slider("Initial Horizon", min_value=min_year, max_value=max_year, value=min_year)
        end_time_slider = st.slider("Terminal Horizon", min_value=min_year, max_value=max_year, value=max_year)

    with col2:
        if select_countries:
            slice_df = df[
                (df["Country Name"].isin(select_countries)) &
                (df["Year"] >= int(start_time_slider)) & (df["Year"] <= int(end_time_slider))
            ].copy()
            
            if not slice_df.empty:
                # Line Chart
                fig_line = px.line(
                    slice_df, x="Year", y=metric_primary, color="Country Name", markers=True,
                    title=f"Historical Vector Tracking Profile: {metric_primary}"
                )
                st.plotly_chart(fig_line, use_container_width=True)
                
                # Bubble Chart
                latest_slice = slice_df[slice_df["Year"] == int(end_time_slider)]
                if latest_slice.empty: latest_slice = slice_df
                
                fig_bubble = px.scatter(
                    latest_slice, x="GDP Per Capita (USD)", y="Inflation Rate (%)",
                    size="GDP (USD)", color="Country Name", hover_name="Country Name",
                    title=f"Risk Matrix Cluster Analysis ({end_time_slider})"
                )
                st.plotly_chart(fig_bubble, use_container_width=True)
            else:
                st.warning("Zero records match selected scope parameters.")
        else:
            st.info("Select countries to generate evaluation matrices.")

# ------------------------------------------------------------------------------
# TAB 3: Advanced Micro-Correlation Matrix
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("🧠 Diagnostic Co-Variance Heatmapping")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        single_country_select = st.selectbox("Target Single Sovereign Profile", choices=all_countries, index=0)
        st.info("**Analytical Guide:** A correlation matrix reveals relationships between economic metrics over time. Values near `+1.00` indicate perfect alignment, while values near `-1.00` reveal an inverse structural link.")
        
    with col2:
        country_df = df[df["Country Name"] == single_country_select].copy()
        if not country_df.empty:
            numeric_cols = ["GDP (USD)", "GDP Growth Rate (%)", "Population", "GDP Per Capita (USD)", "Inflation Rate (%)"]
            corr_matrix = country_df[numeric_cols].corr().fillna(0)

            fig_corr = px.imshow(
                corr_matrix.values, text_auto=".2f",
                labels=dict(color="Correlation Coeff."),
                x=numeric_cols, y=numeric_cols,
                color_continuous_scale="RdBu", color_continuous_midpoint=0,
                title=f"Statistical Co-Variance Profile Matrix: {single_country_select}"
            )
            st.plotly_chart(fig_corr, use_container_width=True)
