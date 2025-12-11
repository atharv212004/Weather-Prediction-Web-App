# WeatherML - AI-Powered Weather Prediction System

## 📋 Project Overview

**WeatherML** is an intelligent, web-based weather forecasting application that leverages machine learning to predict temperature and humidity for any global location and date. Built with Flask backend and modern responsive frontend, it provides accurate predictions using RandomForest algorithms trained on historical weather data.

### ✨ Key Features
- 🌍 **Global Coverage**: Support for any worldwide location using latitude/longitude coordinates
- 🤖 **AI-Powered Predictions**: RandomForest machine learning models for accurate forecasts
- 📅 **Extended Forecast Range**: Predictions from 1980 to 2035 (55+ years range)
- 🌓 **Dark Mode Support**: Full dark/light theme with persistent user preference
- 📊 **Advanced Analytics**: Interactive dashboard comparing predicted vs. actual weather data
- 🔍 **Smart Location Input**: Autocomplete city names with automatic coordinate detection
- ⚡ **Comprehensive Validation**: Real-time input validation with intelligent error messages
- 📱 **Responsive Design**: Optimized for desktop and tablet devices
- ⚙️ **Production-Ready**: Robust error handling and performance optimization

This project is an intelligent Flask web app that uses trained ML models to predict temperature and humidity for any location and date.

Features:
- Enter a location or use browser geolocation (permission required)
- Date picker to select the desired date
- Dark / Light theme toggle
- Output page shows temperature, humidity, and wind with icons
- Analysis page shows feature importances

Quick start
1. Create a virtual environment and install requirements:

```powershell
python -m venv .venv; .\.venv\Scripts\activate; pip install -r requirements.txt
```

2. Place your dataset CSV (or use the attached file) and train the model:

```powershell
python train_model.py --csv "C:\Users\91932\Downloads\Global_Weather_5Years_2000Rows.csv"
```

This saves `model.joblib` in the project folder.

3. Run the Flask app:

```powershell
python app.py
```

Open http://127.0.0.1:5000 in your browser.

Notes and customization
- The training script attempts to auto-detect common column names. If it fails, open `train_model.py` and adjust the column name lists.
- The ML model used is a MultiOutput RandomForestRegressor (robust and suitable for tabular data). You can change it to XGBoost or LightGBM for higher accuracy.
- The front-end uses Nominatim (OpenStreetMap) for reverse geocoding. For production use, consider a proper geocoding API with rate limits and API key.

New workflow for full required pipeline
1. Clean the raw CSV into standardized `data/cleaned.csv`:

```powershell
python -m src.data.cleaning "C:\Users\91932\Downloads\Global_Weather_5Years_2000Rows.csv"
```

2. Train per-target models and scaler (saves artifacts under `models/`):

```powershell
python -m src.models.train "data/cleaned.csv"
```

3. Start the app (ensures `models/` and `data/cleaned.csv` exist):

```powershell
python app.py
```

Open http://127.0.0.1:5000 and use the input form (or `input.html`).
