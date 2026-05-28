import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit page config
st.set_page_config(page_title="Global Macroeconomic Intelligence Terminal", layout="wide")

# ==============================================================================
# 1. ADVANCED MACROECONOMIC DATASET ENGINE
# ==============================================================================
DATA_FILE = "macroeconomic_intelligence.csv"

if not os.path.exists(DATA_FILE):
    countries_meta = [
        {"name": "United States", "code": "USA", "base_gdp": 5963, "growth": 0.025, "pop_base": 250, "pop_growth": 0.006},
        {"name": "China", "code": "CHN", "base_gdp": 360, "growth": 0.075, "pop_base": 1135, "pop_growth": 0.004},
        {"name": "Japan", "code": "JPN", "base_gdp": 3132, "growth": 0.008, "pop_base": 123, "pop_growth": -0.002},
        {"name": "Germany", "code": "DEU", "base_gdp": 1772, "growth": 0.015, "pop_base": 79, "pop_growth": 0.001},
        {"name": "India", "code": "IND", "base_gdp": 321, "growth": 0.062, "pop_base": 870, "pop_growth": 0.012},
        {"name": "United Kingdom", "code": "GBR", "base_gdp": 1093, "growth": 0.018, "pop_base": 57, "pop_growth": 0.004},
        {"name": "France", "code": "FRA", "base_gdp": 1269, "growth": 0.016, "pop_base": 58, "pop_growth": 0.004},
        {"name": "Brazil", "code": "BRA", "base_gdp": 462, "growth": 0.022, "pop_base": 150, "pop_growth": 0.009},
        {"name": "Canada", "code": "CAN", "base_gdp": 590, "growth": 0.021, "pop_base": 27, "pop_growth": 0.010},
        {"name": "Australia", "code": "AUS", "base_gdp": 310, "growth": 0.026, "pop_base": 17, "pop_growth": 0.012},
        {"name": "South Korea", "code": "KOR", "base_gdp": 280, "growth": 0.045, "pop_base": 43, "pop_growth": 0.003},
        {"name": "South Africa", "code": "ZAF", "base_gdp": 115, "growth": 0.019, "pop_base": 38, "pop_growth": 0.014},
        {"name": "Mexico", "code": "MEX", "base_gdp": 290, "growth": 0.023, "pop_base": 85, "pop_growth": 0.013},
        {"name": "Saudi Arabia", "code": "SAU", "base_gdp": 117, "growth": 0.035, "pop_base": 16, "pop_growth": 0.021},
    ]

    years = list(range(1995, 2026))
    mock_data = []
    np.random.seed(42)

    for c in countries_meta:
        current_gdp = c["base_gdp"]
        current_pop = c["pop_base"]
        for year in years:
            annual_growth = c["growth"] + np.random.uniform(-0.02, 0.02)
            current_gdp *= (1 + annual_growth)
            current_pop *= (1 + c["pop_growth"] + np.random.uniform(-0.002, 0.002))

            gdp_raw = current_gdp * 1e9
            pop_raw = current_pop * 1e6
            gdp_per_capita = gdp_raw / pop_raw
            inflation = max(-1.0, (c["growth"] * 1.5) * 100 + np.random.uniform(-2.5, 5.0))

            mock_data.append({
                "Country Name": c["name"],
                "ISO Code": c["code"],
                "Year": year,
                "GDP (USD)": round(gdp_raw, 2),
                "GDP Growth Rate (%)": round(annual_growth * 100, 2),
                "Population": int(pop_raw),
                "GDP Per Capita (USD)": round(gdp_per_capita, 2),
                "Inflation Rate (%)": round(inflation, 2)
            })
    pd.DataFrame(mock_data).to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE)
all_countries = sorted(df["Country Name"].unique().tolist())
min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
default_selection = [c for c in ["United States", "China", "Germany", "India", "Japan"] if c in all_countries]

def format_currency(val):
    if val >= 1e12: return f"${val / 1e12:,.2f} T"
    if val >= 1e9: return f"${val / 1e9:,.2f} B"
    return f"${val:,.0f}"

# ==============================================================================
# 2. ENTERPRISE UI STRUCTURE (Streamlit Native Framework)
# ==============================================================================

# Header
st.markdown("""
<div style="background: linear-gradient(90deg, #1e293b, #0f172a); border-bottom: 2px solid #14b8a6; padding: 24px; border-radius: 8px; text-align: left; margin-bottom: 25px;">
    <span style="color: #14b8a6; font-weight: 700; letter-spacing: 2px; font-size: 12px; text-transform: uppercase;">Institutional Grade Analytics Terminal</span>
    <h1 style="margin: 4px 0 0 0; color: white; font-size: 28px; font-weight: 300;">Global Macroeconomic Intelligence Suite</h1>
</div>
""", unsafe_html=True)

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
            
            st.markdown(f"""
            <div style='background: #1e293b; padding: 15px; border-radius: 8px; border-left: 5px solid #0d9488; color: white; margin-bottom: 10px;'>
                <span style='font-size: 11px; opacity: 0.7; text-transform: uppercase;'>Global Sample Output Volume</span>
                <h3 style='margin: 5px 0 0 0; color: #2dd4bf;'>{format_currency(total_world_gdp)}</h3>
            </div>
            <div style='background: #1e293b; padding: 15px; border-radius: 8px; border-left: 5px solid #f43f5e; color: white;'>
                <span style='font-size: 11px; opacity: 0.7; text-transform: uppercase;'>Mean Inflation Rate</span>
                <h3 style='margin: 5px 0 0 0; color: #fb7185;'>{avg_inflation:.2f}%</h3>
            </div>
            """, unsafe_html=True)

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
                pie_df = pd.concat([top_6, pd.DataFrame([{"Country Name": "Other Nations", "GDP (USD)": others_gdp}])], ignore_index=True) if others_gdp > 0 else top_6
                
                fig_pie = px.pie(pie_df, values="GDP (USD)", names="Country Name", title="Global Economic Volume Dispersal", hole=0.5)
                st.plotly_chart(fig_pie, use_container_width=True)
                
            with sub_col2:
                bar_data = year_df.sort_values(by=target_metric, ascending=False).head(10)
                fig_bar = px.bar(
                    bar_data, x=target_metric, y="Country Name", orientation="h",
                    title=f"Top 10 Performing Nations ({target_metric})",
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
        metric_primary = st.selectbox("Primary Line Vector", choices=["GDP (USD)", "GDP Growth Rate (%)", "GDP Per Capita (USD)", "Inflation Rate (%)"], index=2)
        metric_secondary = st.selectbox("Risk Bubble Parameter", choices=["GDP (USD)", "GDP Growth Rate (%)", "GDP Per Capita (USD)", "Inflation Rate (%)"], index=3)
        
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
                    size_max=40, title=f"Risk Matrix Cluster Analysis: Output vs Inflation ({end_time_slider})"
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
        single_country_select = st.selectbox("Target Single Sovereign Profile", choices=all_countries, index=all_countries.index("United States") if "United States" in all_countries else 0)
        st.info("**Analytical Guide:** A correlation matrix reveals relationships between economic metrics over time. Values near `+1.00` indicate perfect alignment, while values near `-1.00` reveal an inverse structural link.")
        
    with col2:
        country_df = df[df["Country Name"] == single_country_select].copy()
        if not country_df.empty:
            numeric_cols = ["GDP (USD)", "GDP Growth Rate (%)", "Population", "GDP Per Capita (USD)", "Inflation Rate (%)"]
            corr_matrix = country_df[numeric_cols].corr()

            fig_corr = px.imshow(
                corr_matrix.values, text_auto=".2f",
                labels=dict(color="Correlation Coeff."),
                x=numeric_cols, y=numeric_cols,
                color_continuous_scale="RdBu", color_continuous_midpoint=0,
                title=f"Statistical Co-Variance Profile Matrix: {single_country_select}"
            )
            st.plotly_chart(fig_corr, use_container_width=True)