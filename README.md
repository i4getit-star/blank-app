# ☀️ Solar Irradiance Forecaster

A Streamlit application that uses the **Solcast API** to provide accurate solar irradiance predictions for any location on Earth.

## Features

✅ **Real-time Solar Predictions** - Get accurate GHI, DNI, and DHI forecasts
✅ **Interactive Maps & Charts** - Visualize solar irradiance with Plotly graphs
✅ **Weather Data** - View temperature and wind speed forecasts
✅ **Customizable Parameters** - Choose forecast horizon and output parameters
✅ **Location-based Forecasts** - Enter any latitude/longitude coordinates

## Prerequisites

You need a **free Solcast API key** from [solcast.com](https://solcast.com)

## Installation

1. Clone this repository
2. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Create a `.env` file with your API key:

   ```bash
   SOLCAST_API_KEY=your_api_key_here
   ```

## Usage

Run the app:

```bash
streamlit run streamlit_app.py
```

Then:
1. Enter your Solcast API key (or use the sidebar to store it in `.env`)
2. Set your location by entering latitude and longitude
3. Adjust forecast hours and parameters as needed
4. Click "Get Solar Predictions" to fetch data

## API Parameters Explained

- **GHI** (Global Horizontal Irradiance): Total solar radiation on a horizontal surface (W/m²)
- **DNI** (Direct Normal Irradiance): Direct radiation perpendicular to the sun (W/m²)
- **DHI** (Diffuse Horizontal Irradiance): Scattered radiation from the sky (W/m²)
- **Air Temperature**: Ambient temperature (°C)
- **Wind Speed**: Wind velocity (m/s)

## Example Coordinates

- **Sydney, Australia**: -33.8688, 151.2093
- **New York, USA**: 40.7128, -74.0060
- **London, UK**: 51.5074, -0.1278
- **Tokyo, Japan**: 35.6762, 139.6503

## Documentation

For more details on the Solcast API, visit [docs.solcast.com.au](https://docs.solcast.com.au/)
