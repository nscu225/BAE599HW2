# Streamlit Ag Data Visualizations

This small Streamlit app plots NASS data from the provided CSV files.

Files used (place in same folder as `app.py`):
- `Cropland Value copy.csv`
- `Crop Prices copy.csv`
- `E9E4CEB8-AB55-393F-A9F3-C9199B3BA051 copy.csv`

Install dependencies and run:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

The app shows three plots:
- Cropland value by state (KY, IN, OH, TN) from 1997–2025
- National crop prices for corn, soybeans, and wheat from 1975–2025
- National price received index (food commodities) from 1990–2025
