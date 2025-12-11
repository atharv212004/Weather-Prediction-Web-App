from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import joblib
import pandas as pd
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_secret')

MODELS_DIR = 'models'


def load_models():
    out = {}
    base = Path(MODELS_DIR)
    try:
        if (base / 'temp_model.pkl').exists():
            out['temp'] = joblib.load(str(base / 'temp_model.pkl'))
        if (base / 'hum_model.pkl').exists():
            out['hum'] = joblib.load(str(base / 'hum_model.pkl'))
        if (base / 'scaler.pkl').exists():
            out['scaler'] = joblib.load(str(base / 'scaler.pkl'))
    except Exception as e:
        print(f"Error loading models: {e}")
        out = {}
    return out


def date_to_features(date_str):
    """Convert date string to features for prediction.
    
    Handles both past and future dates correctly.
    """
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return {
        'dayofyear': dt.timetuple().tm_yday,
        'month': dt.month,
        'year': dt.year,
        'day': dt.day,
        'dayofweek': dt.weekday(),
    }


def clamp_predictions(preds):
    """Clamp prediction values to reasonable physical ranges"""
    # Temperature: typical range -50°C to 50°C  
    preds['temp'] = float(preds.get('temp', 0))
    if preds['temp'] < -50 or preds['temp'] > 50:
        preds['temp'] = max(-50, min(50, preds['temp']))
    
    # Humidity: must be 0-100%
    preds['humidity'] = float(preds.get('humidity', 0))
    preds['humidity'] = max(0, min(100, preds['humidity']))
    
    # Wind speed: must be non-negative
    preds['wind'] = max(0, float(preds.get('wind', 0)))
    
    return preds


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    models = load_models()
    if not models:
        flash('❌ Model artifacts not found. Please train models first.', 'danger')
        return render_template('index.html')

    location = request.form.get('location', '').strip()
    lat = request.form.get('lat', '').strip()
    lon = request.form.get('lon', '').strip()
    date = request.form.get('date', '').strip()

    # Basic validation
    if not date:
        flash('❌ Please select a date.', 'warning')
        return render_template('index.html')

    if not location and (not lat or not lon):
        flash('❌ Please enter a location or use the location button.', 'warning')
        return render_template('index.html')
    
    # Validate date format and range
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        # Check if date is within reasonable range (1980 to 2035)
        if date_obj.year < 1980:
            flash('❌ Date must be after 1980.', 'warning')
            return render_template('index.html')
        if date_obj.year > 2035:
            flash('❌ Date must be before 2035.', 'warning')
            return render_template('index.html')
    except ValueError:
        flash('❌ Invalid date format. Use YYYY-MM-DD.', 'warning')
        return render_template('index.html')

    try:
        feats = date_to_features(date)
    except Exception:
        flash('❌ Invalid date format. Use YYYY-MM-DD.', 'warning')
        return render_template('index.html')

    try:
        lat_f = float(lat) if lat else None
        lon_f = float(lon) if lon else None
    except ValueError:
        flash('❌ Invalid latitude/longitude values.', 'warning')
        return render_template('index.html')
    
    # Validate latitude and longitude ranges
    if lat_f is not None:
        if lat_f < -90 or lat_f > 90:
            flash('❌ Latitude must be between -90 and 90 degrees.', 'warning')
            return render_template('index.html')
    
    if lon_f is not None:
        if lon_f < -180 or lon_f > 180:
            flash('❌ Longitude must be between -180 and 180 degrees.', 'warning')
            return render_template('index.html')

    # If lat/lon missing, try to geocode server-side using geopy (best-effort)
    if (lat_f is None or lon_f is None) and location:
        try:
            from geopy.geocoders import Nominatim
            geolocator = Nominatim(user_agent='weather-app')
            geo = geolocator.geocode(location, timeout=10)
            if geo:
                lat_f = geo.latitude
                lon_f = geo.longitude
        except Exception:
            pass

    if lat_f is None or lon_f is None:
        flash('❌ Could not determine coordinates. Try typing a specific city name.', 'warning')
        return render_template('index.html')

    # Build feature vector: latitude, longitude, year, month, day, dayofweek
    row = {
        'latitude': lat_f,
        'longitude': lon_f,
        'year': feats['year'],
        'month': feats['month'],
        'day': datetime.strptime(date, '%Y-%m-%d').day,
        'dayofweek': datetime.strptime(date, '%Y-%m-%d').weekday(),
    }

    X_df = pd.DataFrame([row])

    scaler = models.get('scaler')
    if scaler is not None:
        try:
            X_scaled = scaler.transform(X_df)
        except Exception as e:
            print(f"Scaler error: {e}")
            X_scaled = X_df.values
    else:
        X_scaled = X_df.values

    pred_out = {}
    try:
        if 'temp' in models:
            pred_out['temp'] = round(float(models['temp'].predict(X_scaled)[0]), 2)
        if 'hum' in models:
            pred_out['humidity'] = round(float(models['hum'].predict(X_scaled)[0]), 1)
        # clamp safety
        pred_out = clamp_predictions({'temp': pred_out.get('temp', 0), 'humidity': pred_out.get('humidity', 0), 'wind': 0})
    except Exception as e:
        print(f"Prediction error: {e}")
        flash(f'❌ Prediction error: {e}', 'danger')
        return render_template('index.html')

    # Prepare result with lat/lon display
    location_display = f"{lat_f:.4f}, {lon_f:.4f}" if (lat or lon) else location
    
    return render_template('result.html', 
                         location=location_display, 
                         lat=round(lat_f, 4),
                         lon=round(lon_f, 4),
                         date=date, 
                         preds=pred_out)


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/deep')
def deep_info():
    # Accept lat, lon, date as query params and return deep_info.html
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    date = request.args.get('date')
    if not (lat and lon and date):
        flash('Missing parameters for deep info (lat, lon, date).', 'warning')
        return redirect(url_for('index'))

    try:
        lat_f = float(lat)
        lon_f = float(lon)
    except Exception:
        flash('Invalid coordinates for deep info.', 'warning')
        return redirect(url_for('index'))

    models = load_models()
    if not models:
        flash('Models are not available.', 'danger')
        return redirect(url_for('index'))

    try:
        feats = date_to_features(date)
    except Exception:
        flash('Invalid date format for deep info.', 'warning')
        return redirect(url_for('index'))

    row = {
        'latitude': lat_f,
        'longitude': lon_f,
        'year': feats['year'],
        'month': feats['month'],
        'day': datetime.strptime(date, '%Y-%m-%d').day,
        'dayofweek': datetime.strptime(date, '%Y-%m-%d').weekday(),
    }
    X_df = pd.DataFrame([row])
    scaler = models.get('scaler')
    if scaler is not None:
        try:
            X_scaled = scaler.transform(X_df)
        except Exception:
            X_scaled = X_df.values
    else:
        X_scaled = X_df.values

    preds = {}
    if 'temp' in models:
        preds['temp'] = round(float(models['temp'].predict(X_scaled)[0]), 2)
    if 'hum' in models:
        preds['humidity'] = round(float(models['hum'].predict(X_scaled)[0]), 1)
    if 'wind' in models:
        preds['wind'] = round(float(models['wind'].predict(X_scaled)[0]), 2)

    # historical series
    try:
        from src.data.history import load_cleaned, nearest_series
        cleaned_path = Path('data/cleaned.csv')
        if cleaned_path.exists():
            df_clean = load_cleaned(cleaned_path)
            series = nearest_series(df_clean, lat_f, lon_f, max_days=365)
        else:
            series = {'dates': [], 'temperature': [], 'humidity': [], 'wind_speed': []}
    except Exception:
        series = {'dates': [], 'temperature': [], 'humidity': [], 'wind_speed': []}

    # feature importances from temp model if available
    importances = []
    try:
        temp_model = models.get('temp')
        if hasattr(temp_model, 'feature_importances_'):
            importances = list(getattr(temp_model, 'feature_importances_', []))
    except Exception:
        importances = []

    return render_template('deep_info.html', preds=preds, series=series, importances=importances)


@app.route('/analysis')
def analysis():
    """Show model analysis page with plots for different attributes"""
    models = load_models()
    if not models:
        flash('❌ Models not loaded. Please train models first.', 'danger')
        return redirect(url_for('index'))
    
    # Get data for analysis
    try:
        df = pd.read_csv('data/cleaned.csv')
        df['date'] = pd.to_datetime(df['date'])
    except Exception as e:
        flash(f'❌ Error loading data: {e}', 'danger')
        return redirect(url_for('index'))
    
    # Get unique values for filtering - only include years up to 2025 (for real vs predicted comparison)
    months = sorted(df['date'].dt.month.unique().tolist())
    years = sorted(df['date'].dt.year.unique().tolist())
    
    # Limit years to 2025 (only show real data years for comparison)
    all_years = [year for year in years if year <= 2025]
    if 2025 not in all_years:
        all_years.append(2025)
    all_years = sorted(all_years)
    
    return render_template('analysis.html', months=months, years=all_years)


@app.route('/api/analysis', methods=['POST'])
def api_analysis():
    """API endpoint to get analysis data"""
    models = load_models()
    if not models or 'temp' not in models:
        return jsonify({'error': 'Models not loaded'}), 400
    
    data = request.json
    selected_month = int(data.get('month', 1))
    selected_year = int(data.get('year', 2020))
    
    try:
        df = pd.read_csv('data/cleaned.csv')
        df['date'] = pd.to_datetime(df['date'])
        
        # Filter by month and year
        df_filtered = df[(df['date'].dt.month == selected_month) & (df['date'].dt.year == selected_year)]
        
        if df_filtered.empty:
            return jsonify({'error': 'No data for selected date'}), 400
        
        # Get sample records and make predictions
        sample_size = min(30, len(df_filtered))
        df_sample = df_filtered.head(sample_size)
        
        # Prepare features for prediction
        features = ['latitude', 'longitude', 'year', 'month', 'day', 'dayofweek']
        X = df_sample[features].copy()
        
        scaler = models.get('scaler')
        if scaler:
            X_scaled = scaler.transform(X)
        else:
            X_scaled = X.values
        
        # Make predictions
        temp_preds = models['temp'].predict(X_scaled) if 'temp' in models else []
        hum_preds = models['hum'].predict(X_scaled) if 'hum' in models else []
        
        # Prepare response
        dates = df_sample['date'].dt.strftime('%Y-%m-%d').tolist()
        actual_temp = df_sample['temperature_avg'].tolist() if 'temperature_avg' in df_sample.columns else []
        actual_hum = df_sample['humidity'].tolist() if 'humidity' in df_sample.columns else []
        
        return jsonify({
            'dates': dates,
            'predicted_temp': [float(x) for x in temp_preds],
            'actual_temp': [float(x) if not pd.isna(x) else None for x in actual_temp],
            'predicted_hum': [float(x) for x in hum_preds],
            'actual_hum': [float(x) if not pd.isna(x) else None for x in actual_hum],
        })
    except Exception as e:
        print(f"Error in api_analysis: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
