import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Ag Data Visualizations", layout="wide")
st.title("Agricultural Prices & Cropland Value (NASS data)")

# File paths (assume files are in the same folder as this app)
CROPLAND_FILE = "Cropland Value copy.csv"
CROP_PRICES_FILE = "Crop Prices copy.csv"
NASS_FILE = "E9E4CEB8-AB55-393F-A9F3-C9199B3BA051 copy.csv"

@st.cache_data
def load_csv(path):
    df = pd.read_csv(path)
    # Remove leading/trailing spaces in column names
    df.columns = [c.strip() for c in df.columns]
    return df

# Load data
cropland = load_csv(CROPLAND_FILE)
crop_prices = load_csv(CROP_PRICES_FILE)
price_index = load_csv(NASS_FILE)

st.markdown("Data loaded from provided CSV files. Below are three plots as requested.")

### Plot 1: Cropland value by state (1997-2025)
st.header("Cropland Value: $ / acre by state (1997-2025)")

# Interactive controls for Plot 1
col1, col2 = st.columns(2)
with col1:
    year_range_1 = st.slider("Select Year Range", 1997, 2025, (1997, 2025), key="plot1_years")
with col2:
    available_states = ["KENTUCKY", "INDIANA", "OHIO", "TENNESSEE"]
    selected_states = st.multiselect("Select States", available_states, default=available_states, key="plot1_states")

# Filter cropland for desired states and data item
cp = cropland.copy()
# Ensure Year is numeric
cp['Year'] = pd.to_numeric(cp['Year'], errors='coerce')
cp['Value'] = cp['Value'].replace({',':''}, regex=True)
cp['Value'] = pd.to_numeric(cp['Value'], errors='coerce')
cp = cp[cp['State'].isin(selected_states)]
cp = cp[(cp['Year'] >= year_range_1[0]) & (cp['Year'] <= year_range_1[1])]
# Prepare for plotting
cp_plot = cp[['Year','State','Value']].dropna()

chart1 = alt.Chart(cp_plot).mark_line(point=True).encode(
    x=alt.X('Year:O', title='Year'),
    y=alt.Y('Value:Q', title='Cropland value ($ / acre)'),
    color=alt.Color('State:N', title='State'),
    tooltip=['State','Year','Value']
).properties(width=900, height=350).interactive()

st.altair_chart(chart1, use_container_width=True)

### Plot 2: Crop prices national (1975-2025)
st.header("Crop Prices: $ / bu (national, 1975-2025)")

# Interactive controls for Plot 2
col1, col2 = st.columns(2)
with col1:
    year_range_2 = st.slider("Select Year Range", 1975, 2025, (1975, 2025), key="plot2_years")
with col2:
    available_crops = ["CORN", "SOYBEANS", "WHEAT"]
    selected_crops = st.multiselect("Select Crops", available_crops, default=available_crops, key="plot2_crops")

cp2 = crop_prices.copy()
cp2['Year'] = pd.to_numeric(cp2['Year'], errors='coerce')
cp2['Value'] = pd.to_numeric(cp2['Value'], errors='coerce')
# Filter for national level and crops
cp2 = cp2[cp2['Geo Level'].str.upper().str.contains('NATIONAL') | (cp2['Geo Level'].str.upper()== 'NATIONAL')]
cp2 = cp2[cp2['Commodity'].isin(selected_crops)]
cp2 = cp2[(cp2['Year'] >= year_range_2[0]) & (cp2['Year'] <= year_range_2[1])]
cp2_plot = cp2[['Year','Commodity','Value']].dropna()

chart2 = alt.Chart(cp2_plot).mark_line(point=True).encode(
    x=alt.X('Year:O', title='Year'),
    y=alt.Y('Value:Q', title='Price ($ / bu)'),
    color=alt.Color('Commodity:N', title='Crop'),
    tooltip=['Commodity','Year','Value']
).properties(width=900, height=350).interactive()

st.altair_chart(chart2, use_container_width=True)

### Plot 3: Price received index (1990-2025)
st.header("Price Received Index (2011=100) — National (1990-2025)")

# Interactive controls for Plot 3
year_range_3 = st.slider("Select Year Range", 1990, 2025, (1990, 2025), key="plot3_years")

pi = price_index.copy()
pi['Year'] = pd.to_numeric(pi['Year'], errors='coerce')
pi['Value'] = pd.to_numeric(pi['Value'], errors='coerce')
# Filter national and the FOOD COMMODITIES index rows
pi = pi[pi['Geo Level'].str.upper().str.contains('NATIONAL') | (pi['Geo Level'].str.upper()=='NATIONAL')]
# The Data Item seems to contain the text; filter for 'PRICE RECEIVED' or index
pi = pi[pi['Commodity'].str.upper().str.contains('FOOD COMMODITIES')]
pi = pi[(pi['Year'] >= year_range_3[0]) & (pi['Year'] <= year_range_3[1])]
pi_plot = pi[['Year','Value']].dropna()

chart3 = alt.Chart(pi_plot).mark_line(point=True, color='steelblue').encode(
    x=alt.X('Year:O', title='Year'),
    y=alt.Y('Value:Q', title='Price Received Index (2011=100)'),
    tooltip=['Year','Value']
).properties(width=900, height=300).interactive()

st.altair_chart(chart3, use_container_width=True)

st.markdown("---")
st.write("Files used:")
st.write(f"- {CROPLAND_FILE}")
st.write(f"- {CROP_PRICES_FILE}")
st.write(f"- {NASS_FILE}")
