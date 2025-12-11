# WeatherML - Weather Prediction System Documentation

## 📋 Project Overview

**WeatherML** is an intelligent, production-ready weather forecasting application that uses machine learning to predict temperature and humidity for any global location and date. Built with Flask backend and modern responsive frontend, powered by RandomForest algorithms.

### ✨ Key Features
- 🌍 **Global Coverage**: Any location worldwide using lat/lon coordinates
- 🤖 **AI-Powered**: RandomForest ML models for accurate forecasts
- 📅 **Extended Range**: Predictions from 1980 to 2035 (55+ years)
- 🌓 **Dark Mode**: Full dark/light theme with persistent preference
- 📊 **Analytics**: Interactive dashboard with predicted vs actual data
- 🔍 **Smart Input**: Autocomplete city names with auto-detect coordinates
- ⚡ **Validated**: Real-time input validation with error handling
- 📱 **Responsive**: Optimized for desktop and tablet devices

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.1.2
- **Language**: Python 3.11.4
- **ML**: scikit-learn (RandomForest)
- **Data**: Pandas, NumPy
- **Serialization**: joblib
- **Geocoding**: geopy (Nominatim)

### Frontend
- **Layout**: HTML5 + Bootstrap 5.3
- **Styling**: CSS3 with theme variables
- **Scripting**: JavaScript ES6 (Fetch API)
- **Icons**: Font Awesome 6.4.0
- **Charts**: Plotly.js

### Data
- **Storage**: CSV format (2000 records)
- **Models**: joblib pickle files
- **Scaler**: StandardScaler for features

---

## 📦 Installation Guide

### Requirements
- Python 3.9+
- pip package manager
- Modern web browser

### Setup Steps

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Install dependencies
pip install flask==3.1.2
pip install scikit-learn>=1.3.0
pip install pandas>=2.0.0
pip install numpy>=1.24.0
pip install joblib>=1.3.0
pip install geopy>=2.3.0

# 3. Prepare data
# Place data/cleaned.csv with columns:
# latitude, longitude, date, temperature, humidity

# 4. Train models
python train.py
# Generates: temp_model.pkl, hum_model.pkl, scaler.pkl

# 5. Run application
python app.py
# Open http://127.0.0.1:5000
```

---

## 💻 User Guide

### Making a Prediction

**Step 1: Enter Location**
- Type city name (minimum 2 characters)
- Autocomplete fetches latitude/longitude
- Example: "New York", "London", "Tokyo", "Paris, France"

**Step 2: Select Date**
- Valid range: 1980-01-01 to 2035-12-31
- Use calendar picker or quick buttons
- Historical data: Use dates between 1980-2025
- Future predictions: Up to 2035

**Step 3: Get Forecast**
- Click "Get Forecast" button
- System validates all inputs
- Displays predictions with coordinates

**Output**
- Predicted Temperature (°C)
- Predicted Humidity (%)
- Location coordinates
- Selected date

### Analyzing Weather Data

**Analysis Dashboard**
1. Open "Analysis" page
2. Select Month (1-12)
3. Select Year (≤2025 for real data)
4. Click "Load Analysis"
5. View interactive charts

**Charts Available**
- Temperature: Predicted (blue line) vs Actual (red dots)
- Humidity: Predicted (green line) vs Actual (orange dots)
- Performance metrics: Averages for both

### Dark Mode Toggle
- Click moon/sun icon (top-right navbar)
- Theme saves to localStorage
- Applies to all pages automatically

---

## 📡 API Reference

### Endpoints

**GET `/`**
- Returns main prediction form page
- Status: 200 OK

**POST `/predict`**
- Generate weather prediction
- Parameters: location, lat, lon, date, elevation (optional)
- Returns: HTML with forecast results
- Status: 200 OK or 400 (validation error)

**GET `/analysis`**
- Returns analytics dashboard page
- Status: 200 OK

**POST `/api/analysis`**
- Fetch chart data for month/year
- Body: `{"month": 1-12, "year": 1980-2025}`
- Returns: JSON with predicted/actual weather
- Status: 200 OK or 400 (invalid month/year)

**GET `/health`**
- Health check endpoint
- Returns: `{"status": "ok"}`

---

## 🤖 ML Model Specifications

### Feature Set (6 inputs)

| Feature | Type | Range | Description |
|---------|------|-------|-------------|
| latitude | float | -90 to 90 | Geographic latitude |
| longitude | float | -180 to 180 | Geographic longitude |
| year | int | 1980-2035 | Year of prediction |
| month | int | 1-12 | Month number |
| day | int | 1-31 | Day of month |
| dayofweek | int | 0-6 | Day of week (Mon-Sun) |

### Output Variables

**Temperature Prediction**
- Type: Float (continuous)
- Physical range: -50°C to +50°C
- Auto-clamped: Values outside range adjusted
- Precision: 2 decimal places (e.g., 15.32°C)

**Humidity Prediction**
- Type: Float (continuous)
- Valid range: 0% to 100%
- Auto-clamped: Negative → 0%, >100% → 100%
- Precision: 1 decimal place (e.g., 65.2%)

### Model Type
- **Algorithm**: RandomForestRegressor
- **Trees**: 100
- **Max Depth**: 20
- **Samples Split**: 2
- **Samples Leaf**: 1

### Training Data
- **Records**: 2000 historical weather samples
- **Features**: 6 (as listed above)
- **Train-Test Split**: 80-20
- **Scaling**: StandardScaler applied

### Feature Importance (Approximate)
1. Latitude: 35% - Primary geographic factor
2. Longitude: 30% - Primary geographic factor
3. Month: 20% - Seasonal variation
4. Day: 8% - Temporal variation
5. Year: 5% - Long-term trends
6. DayOfWeek: 2% - Minor effect

---

## ✔️ Validation Rules

### Input Validation

**Location (String)**
- Required: Yes
- Min length: 1
- Max length: 100
- Validation: Nominatim geocoding
- Error: "Location not found"

**Latitude (Float)**
- Required: Yes (auto-fetched if not provided)
- Range: -90 to 90 degrees
- Precision: Up to 4 decimals
- Error: "Latitude must be between -90 and 90"

**Longitude (Float)**
- Required: Yes (auto-fetched if not provided)
- Range: -180 to 180 degrees
- Precision: Up to 4 decimals
- Error: "Longitude must be between -180 and 180"

**Date (String, YYYY-MM-DD)**
- Required: Yes
- Range: 1980-01-01 to 2035-12-31
- Format: ISO 8601
- Error messages:
  - "Date must be after 1980"
  - "Date must be before 2035"
  - "Invalid date format"

**Elevation (Float, Optional)**
- Range: 0 to 8848 meters
- Not used in current model
- For future enhancement

### Output Validation (Safety Checks)

**Temperature Clamping**
- Raw prediction: Any float
- Clamped range: -50°C to +50°C
- Logic: `max(-50, min(50, prediction))`
- Example: 55°C predicted → 50°C displayed

**Humidity Clamping**
- Raw prediction: Any float
- Valid range: 0% to 100%
- Logic: `max(0, min(100, prediction))`
- Example: 105% predicted → 100% displayed

**Wind Speed**
- Always non-negative
- Current model: Always 0 (not predicted)
- Future: Will add wind predictions

---

## 🐛 Troubleshooting

### Problem: "Models not found"
**Cause**: ML model files missing
**Solution**:
1. Check models/ directory exists
2. Run: `python train.py`
3. Verify .pkl files created
4. Restart Flask app

### Problem: "Location not found"
**Cause**: City not recognized by Nominatim
**Solution**:
- Use full city name: "Paris, France"
- Try English spelling
- Include country code
- Check internet connection

### Problem: "Date out of range"
**Cause**: Date before 1980 or after 2035
**Solution**:
- Use dates between 1980-2035
- Past dates: Use dates in training range
- Future dates: Up to ~2035 maximum

### Problem: "Invalid latitude/longitude"
**Cause**: Coordinates outside valid range
**Solution**:
- Use autocomplete feature
- Verify: Latitude -90 to 90
- Verify: Longitude -180 to 180
- Retry with different location

### Problem: Dark mode not saving
**Cause**: Browser localStorage disabled
**Solution**:
1. Clear browser cache
2. Check localStorage in DevTools (F12)
3. Enable JavaScript
4. Disable extensions blocking storage

### Problem: Analysis slow or errors
**Cause**: Large data processing, API timeout
**Solution**:
1. Try different month/year
2. Check internet connection
3. Refresh page (Ctrl+R)
4. Check browser console errors
5. Wait 10+ seconds

### Problem: Autocomplete not working
**Cause**: Network issue, API rate limit
**Solution**:
1. Type 2+ characters
2. Wait 1 second after typing
3. Use "City, Country" format
4. Check internet connection
5. Try different browser

---

## 📊 Performance Benchmarks

| Operation | Time | Status |
|-----------|------|--------|
| Home page load | < 500ms | ✅ Fast |
| Prediction generation | < 2000ms | ✅ Good |
| Location autocomplete | ~1000ms | ✅ Good |
| Analysis dashboard load | < 3000ms | ✅ Acceptable |
| Chart rendering | < 2000ms | ✅ Good |

### Browser Compatibility
- ✅ Chrome/Chromium 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers (responsive)

### Specifications
- Training data: 2000 records
- Feature dimensions: 6 inputs
- Model format: joblib pickle
- CSV file size: 500KB - 2MB

---

## 📁 Project Structure

```
weather-ml-app/
│
├── app.py                      # Flask application (356 lines)
├── train.py                    # Model training script
├── README.md                   # Quick start guide
├── DOCUMENTATION.md            # This file
├── requirements.txt            # Python dependencies
│
├── templates/                  # HTML templates
│   ├── index.html             # Prediction form (368 lines)
│   ├── result.html            # Results page (282 lines)
│   └── analysis.html          # Analytics dashboard (821 lines)
│
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css          # Global styling + themes (244 lines)
│   └── js/
│       └── main.js            # Client-side logic (200 lines)
│
├── data/                       # Data directory
│   └── cleaned.csv            # Training dataset (2000 rows)
│
├── models/                     # ML models (generated)
│   ├── temp_model.pkl        # Temperature predictor
│   ├── hum_model.pkl         # Humidity predictor
│   └── scaler.pkl            # Feature scaler
│
└── docs/                      # Documentation
    └── (Optional additional docs)
```

---

## 🚀 Quick Commands

### Setup & Run
```bash
# Windows
python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python train.py && python app.py

# Linux/Mac
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python train.py && python app.py
```

### Development
```bash
# Run with debug
python app.py

# Train models only
python train.py

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
```

### Production
```bash
# Set debug mode off in app.py: debug=False
# Use WSGI server: gunicorn app:app
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 🔮 Future Enhancements

**Phase 2 (Planned)**
- [ ] Real-time weather API integration
- [ ] LSTM/RNN neural networks
- [ ] Wind speed predictions
- [ ] Pressure predictions
- [ ] User authentication
- [ ] Prediction history

**Phase 3 (Roadmap)**
- [ ] Mobile app (React Native)
- [ ] Docker containers
- [ ] Cloud deployment (AWS/GCP)
- [ ] Advanced analytics
- [ ] Batch predictions
- [ ] Climate trends analysis

---

## ❓ FAQ

**Q: How accurate are the predictions?**
A: Typical RMSE ~2-3°C for temperature. Accuracy varies by location and season.

**Q: Can I use my own dataset?**
A: Yes! Place CSV in `data/cleaned.csv` with required columns and retrain.

**Q: Does it work offline?**
A: Location autocomplete needs internet. Predictions work offline once loaded.

**Q: How do I deploy to production?**
A: Set `debug=False` in app.py. Use Gunicorn + Nginx for production.

**Q: How do I modify the model?**
A: Edit `train.py` to add/remove features or change algorithms, then retrain.

**Q: Why are predictions sometimes outside expected range?**
A: ML models can extrapolate beyond training data. Output is auto-clamped to physical limits.

**Q: Can I add more weather variables?**
A: Yes! Modify training data, train.py, and prediction logic to include wind, pressure, etc.

---

## 📝 License & Credits

**Project**: WeatherML - Weather Prediction System
**Version**: 1.0.0
**Status**: Active Development
**Last Updated**: December 2025

### Technologies Used
- Flask (Web framework)
- scikit-learn (Machine learning)
- pandas/NumPy (Data processing)
- Bootstrap (UI framework)
- Plotly (Data visualization)

### Data Sources
- Historical weather data (CSV format)
- Nominatim OpenStreetMap (Geocoding)

---

## 📞 Support & Contact

**For issues:**
1. ✅ Check Troubleshooting section
2. ✅ Review this documentation
3. ✅ Check browser console (F12)
4. ✅ Verify input formats
5. ✅ Test internet connection

**Common Quick Fixes:**
- Models missing → Run `python train.py`
- Location not found → Use "City, Country" format
- Date error → Check 1980-2035 range
- Dark mode gone → Clear cache and localStorage
- Slow dashboard → Try different month/year

---

**Happy Weather Predicting! 🌤️**

*Built with ❤️ using Flask, Machine Learning, and Modern Web Technologies*
