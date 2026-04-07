import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SOLCAST_API_BASE = "https://api.solcast.com.au/world_radiation/forecasts"
SOLCAST_HISTORIC_BASE = "https://api.solcast.com.au/world_radiation/historic"

# Page configuration
st.set_page_config(
    page_title="☀️ Solar Irradiance Forecaster",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("☀️ Solar Irradiance Forecaster")
st.write("Get accurate solar irradiance predictions using the Solcast API")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.write("Enter your Solcast API key here, or set `SOLCAST_API_KEY` in a `.env` file.")
    
    # API Key
    api_key = st.text_input(
        "Solcast API Key",
        value=os.getenv("SOLCAST_API_KEY", ""),
        type="password",
        help="Get your free API key from https://solcast.com"
    )
    st.caption("If the sidebar is hidden, enter your API key below on the main page.")

if not api_key:
    st.warning("⚠️ Please enter your Solcast API key in the sidebar or below.")
    st.info("Get a free API key at [solcast.com](https://solcast.com)")
    api_key = st.text_input(
        "Solcast API Key",
        value="",
        type="password",
        help="Enter your Solcast API key here if the sidebar is not visible."
    )

# Location input
col1, col2 = st.columns(2)
with col1:
    latitude = st.number_input(
        "📍 Latitude",
        value=-33.8688,
        min_value=-90.0,
        max_value=90.0,
        step=0.0001,
        help="Enter latitude in decimal degrees (e.g., -33.8688 for Sydney)"
    )

with col2:
    longitude = st.number_input(
        "📍 Longitude",
        value=151.2093,
        min_value=-180.0,
        max_value=180.0,
        step=0.0001,
        help="Enter longitude in decimal degrees (e.g., 151.2093 for Sydney)"
    )

# Additional parameters
with st.expander("🔧 Advanced Options"):
    col1, col2 = st.columns(2)
    with col1:
        horizon = st.slider(
            "Horizon (hours)",
            min_value=1,
            max_value=168,
            value=24,
            help="Number of hours to forecast"
        )
    
    with col2:
        output_parameters = st.multiselect(
            "Output Parameters",
            options=["ghi", "dni", "dhi", "air_temp", "wind_speed"],
            default=["ghi", "dni", "dhi"],
            help="Select which solar parameters to retrieve"
        )

# Get predictions button
if st.button("🔍 Get Solar Predictions", use_container_width=True):
    if not api_key:
        st.error("❌ Please enter your Solcast API key")
    else:
        with st.spinner("📊 Fetching solar predictions..."):
            try:
                api_key = api_key.strip()
                allowed_parameters = ["ghi", "dni", "dhi", "air_temp", "wind_speed"]
                selected_output_parameters = [p for p in output_parameters if p in allowed_parameters]

                if not selected_output_parameters:
                    st.error("❌ Please select at least one valid output parameter.")
                    raise ValueError("No valid output parameters selected.")

                # Prepare parameters
                params = {
                    "latitude": latitude,
                    "longitude": longitude,
                    "hours": horizon,
                    "api_key": api_key,
                    "output_parameters": ",".join(selected_output_parameters)
                }
                
                with col3:
                        st.metric("📅 Forecast Period", f"{horizon} hours")
                    
                    st.divider()
                    
                    # Display data table
                    st.subheader("📋 Forecast Data")
                    display_cols = ["period_end"] + [col for col in df.columns if col != "period_end"]
                    st.dataframe(df[display_cols], use_container_width=True)
                    
                    st.divider()
                    
                    # Create visualizations
                    st.subheader("📊 Solar Irradiance Charts")
                    
                    # GHI Chart (if available)
                    if "ghi" in df.columns:
                        fig_ghi = go.Figure()
                        fig_ghi.add_trace(go.Scatter(
                            x=df["period_end"],
                            y=df["ghi"],
                            mode="lines+markers",
                            name="GHI (W/m²)",
                            line=dict(color="orange", width=2),
                            fill="tozeroy"
                        ))
                        fig_ghi.update_layout(
                            title="Global Horizontal Irradiance (GHI)",
                            xaxis_title="Date/Time",
                            yaxis_title="Irradiance (W/m²)",
                            hovermode="x unified",
                            height=400
                        )
                        st.plotly_chart(fig_ghi, use_container_width=True)
                    
                    # DNI and DHI Chart (if available)
                    if "dni" in df.columns or "dhi" in df.columns:
                        fig_components = go.Figure()
                        
                        if "dni" in df.columns:
                            fig_components.add_trace(go.Scatter(
                                x=df["period_end"],
                                y=df["dni"],
                                mode="lines+markers",
                                name="DNI (W/m²)",
                                line=dict(color="red", width=2)
                            ))
                        
                        if "dhi" in df.columns:
                            fig_components.add_trace(go.Scatter(
                                x=df["period_end"],
                                y=df["dhi"],
                                mode="lines+markers",
                                name="DHI (W/m²)",
                                line=dict(color="blue", width=2)
                            ))
                        
                        fig_components.update_layout(
                            title="Solar Irradiance Components",
                            xaxis_title="Date/Time",
                            yaxis_title="Irradiance (W/m²)",
                            hovermode="x unified",
                            height=400
                        )
                        st.plotly_chart(fig_components, use_container_width=True)
                    
                    # Weather data (if available)
                    if "air_temp" in df.columns or "wind_speed" in df.columns:
                        st.subheader("🌡️ Weather Conditions")
                        col1, col2 = st.columns(2)
                        
                        if "air_temp" in df.columns:
                            with col1:
                                fig_temp = go.Figure()
                                fig_temp.add_trace(go.Scatter(
                                    x=df["period_end"],
                                    y=df["air_temp"],
                                    mode="lines+markers",
                                    name="Temperature (°C)",
                                    line=dict(color="red", width=2)
                                ))
                                fig_temp.update_layout(
                                    title="Air Temperature",
                                    xaxis_title="Date/Time",
                                    yaxis_title="Temperature (°C)",
                                    hovermode="x unified",
                                    height=300
                                )
                                st.plotly_chart(fig_temp, use_container_width=True)
                        
                        if "wind_speed" in df.columns:
                            with col2:
                                fig_wind = go.Figure()
                                fig_wind.add_trace(go.Scatter(
                                    x=df["period_end"],
                                    y=df["wind_speed"],
                                    mode="lines+markers",
                                    name="Wind Speed (m/s)",
                                    line=dict(color="blue", width=2)
                                ))
                                fig_wind.update_layout(
                                    title="Wind Speed",
                                    xaxis_title="Date/Time",
                                    yaxis_title="Wind Speed (m/s)",
                                    hovermode="x unified",
                                    height=300
                                )
                                st.plotly_chart(fig_wind, use_container_width=True)
                    
                    # Summary statistics
                    st.divider()
                    st.subheader("📈 Summary Statistics")
                    
                    stats_col = st.columns(len(output_parameters))
                    for idx, param in enumerate(output_parameters):
                        if param in df.columns:
                            with stats_col[idx]:
                                st.metric(
                                    f"{param.upper()} Max",
                                    f"{df[param].max():.2f}",
                                    delta=f"Avg: {df[param].mean():.2f}"
                                )
            
            except requests.exceptions.HTTPError as e:
                status = e.response.status_code if e.response is not None else "unknown"
                detail = e.response.text if e.response is not None else str(e)
                st.error(f"❌ API Error {status}: {detail}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ API Error: {str(e)}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer with documentation
st.divider()
with st.expander("ℹ️ About Solcast API Parameters"):
    st.markdown("""
    - **GHI (Global Horizontal Irradiance)**: Total solar radiation received on a horizontal surface
    - **DNI (Direct Normal Irradiance)**: Direct solar radiation perpendicular to the sun's rays
    - **DHI (Diffuse Horizontal Irradiance)**: Scattered solar radiation from the sky
    - **Air Temperature**: Ambient temperature at the location
    - **Wind Speed**: Wind velocity at the location
    
    For more information, visit [Solcast Documentation](https://docs.solcast.com.au/)
    """)
