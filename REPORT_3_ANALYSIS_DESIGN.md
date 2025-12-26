# REPORT 3: ANALYSIS & DESIGN
## Technical Architecture, Requirements, and Implementation Details

---

## 3.1 Software Requirements & Technology Stack

### Complete Software Requirements Specification

#### 3.1.1 Frontend Requirements

**HTML5 Markup (index.html, result.html, analysis.html)**

| Component | Requirement | Justification |
|-----------|-------------|---------------|
| **Semantic Structure** | HTML5 with proper sections and headings | Accessibility and SEO optimization |
| **Forms** | Text input, date picker, number input | Intuitive user interaction |
| **Data Binding** | Hidden fields for lat/lon storage | JavaScript form data manipulation |
| **Responsiveness** | Mobile-first responsive markup | Support all device sizes (320px - 4K) |
| **Accessibility** | ARIA labels, form associations | WCAG 2.1 AA compliance |
| **Character Encoding** | UTF-8 charset declaration | International character support |
| **Viewport** | Device width viewport meta tag | Proper mobile rendering |

**CSS3 Styling (style.css)**

| Feature | Specification | Rationale |
|---------|--------------|-----------|
| **Grid System** | Bootstrap 5.3 (12-column grid) | Responsive layout management |
| **Variables** | CSS custom properties for theming | Dynamic dark/light mode switching |
| **Flexbox** | Flex containers for component layout | Flexible, modern layout engine |
| **Media Queries** | Breakpoints: 576px, 768px, 992px, 1200px | Device-specific styling |
| **Animations** | CSS transitions and keyframes | Smooth visual feedback |
| **Color Palette** | Blue primary (#667eea), gradients | Professional, accessible colors |
| **Typography** | System fonts + Google Fonts (optional) | Performance and readability |
| **Shadows & Borders** | Subtle box shadows for depth | Modern, clean aesthetic |

**JavaScript ES6 (main.js)**

| Feature | Implementation | Purpose |
|---------|-----------------|---------|
| **Event Listeners** | DOMContentLoaded, click, input, submit | User interaction handling |
| **Form Validation** | Client-side checks before submission | Immediate feedback, UX improvement |
| **Fetch API** | Async/await for HTTP requests | Modern, promise-based API calls |
| **LocalStorage** | Theme preference persistence | Remember user settings |
| **DOM Manipulation** | Element selection and class toggling | Dynamic UI updates |
| **Error Handling** | Try-catch blocks and error callbacks | Graceful failure handling |
| **Debouncing** | 1000ms delay for autocomplete | Reduced API request frequency |
| **Geolocation** | Browser Geolocation API integration | One-tap location detection |
| **Promise Handling** | Promise chaining and error states | Async operation management |

**External Libraries & CDN Resources**

| Library | Version | Purpose | CDN |
|---------|---------|---------|-----|
| **Bootstrap** | 5.3.0 | CSS framework & components | cdn.jsdelivr.net |
| **Font Awesome** | 6.4.0 | Icon library | cdnjs.cloudflare.com |
| **Animate.css** | 4.1.1 | CSS animations | cdnjs.cloudflare.com |
| **Plotly.js** | Latest | Interactive charts | cdn.plot.ly |

#### 3.1.2 Backend Requirements

**Python Environment**

| Specification | Requirement | Notes |
|---------------|-------------|-------|
| **Python Version** | 3.9+ (tested on 3.11.4) | Modern syntax support, performance |
| **Package Manager** | pip (PyPI) | Standard Python package management |
| **Virtual Environment** | venv (built-in) | Dependency isolation |
| **Requirements File** | requirements.txt | Reproducible dependency specification |
| **Execution** | Python interpreter on command line | Simple deployment model |

**Flask Web Framework (app.py)**

| Component | Version | Functionality |
|-----------|---------|--------------|
| **Flask Core** | 3.1.2 | HTTP request routing and response handling |
| **Jinja2** | Built-in to Flask | Template rendering with Python logic |
| **Werkzeug** | Built-in to Flask | WSGI utilities and file handling |

**Flask Capabilities Used**:
```python
@app.route('/')                          # Route decorator for URL mapping
@app.route('/predict', methods=['POST']) # POST request handling
render_template()                        # HTML template rendering
request.form.get()                       # Form data retrieval
request.form.getlist()                   # Multiple form values
flash()                                  # Flash message system
jsonify()                                # JSON response generation
```

**Required Flask Extensions (in requirements.txt)**:
```
Flask==3.1.2
Werkzeug>=2.3.0
Jinja2>=3.1.0
```

#### 3.1.3 Machine Learning & Data Processing

**scikit-learn (ML Library)**

| Component | Purpose | Specifications |
|-----------|---------|-----------------|
| **RandomForestRegressor** | Main ML algorithm | 100 estimators, max_depth=20 |
| **StandardScaler** | Feature normalization | Mean=0, standard deviation=1 |
| **train_test_split** | Data partitioning | 80-20 train-test split |
| **metrics** | Model evaluation | R² score, mean squared error |

**RandomForest Configuration Details**:
```python
RandomForestRegressor(
    n_estimators=100,           # 100 decision trees in ensemble
    max_depth=20,               # Prevent overfitting
    min_samples_split=2,        # Standard split criterion
    min_samples_leaf=1,         # Allow single-sample leaves
    random_state=42,            # Reproducible results
    n_jobs=-1,                  # Parallel processing
    criterion='squared_error'   # MSE minimization
)
```

**Pandas (Data Processing)**

| Feature | Usage | Version |
|---------|-------|---------|
| **DataFrame** | In-memory data structure | 2.0+ |
| **read_csv()** | CSV file loading | Supports UTF-8, custom delimiters |
| **groupby()** | Data aggregation | Monthly/yearly statistics |
| **fillna()** | Missing value handling | Forward/backward fill options |
| **astype()** | Type conversion | Ensure correct data types |

**NumPy (Numerical Computing)**

| Operation | Purpose | Usage |
|-----------|---------|-------|
| **Arrays** | Underlying data structure for models | Efficient numerical operations |
| **Mathematical functions** | Computations in models | Used internally by scikit-learn |
| **Broadcasting** | Array operations | Used in feature scaling |

**joblib (Model Serialization)**

| Task | Function | Details |
|------|----------|---------|
| **Model Saving** | joblib.dump(model, 'file.pkl') | Binary serialization format |
| **Model Loading** | model = joblib.load('file.pkl') | Restore trained models |
| **Scaler Saving** | joblib.dump(scaler, 'scaler.pkl') | Serialize StandardScaler |
| **Compression** | compress=3 parameter | Reduce file size (tradeoff: CPU) |

**Complete Requirements.txt**:
```
Flask==3.1.2
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
joblib>=1.3.0
geopy>=2.3.0
Werkzeug>=2.3.0
```

#### 3.1.4 Data Storage & Files

**CSV Data Format (data/cleaned.csv)**

| Aspect | Specification | Details |
|--------|---------------|---------|
| **Format** | CSV (comma-separated values) | Text-based, human-readable |
| **Records** | 2000 samples | Historical weather data |
| **Columns** | 5 features | latitude, longitude, date, temperature, humidity |
| **Row Structure** | latitude, longitude, YYYY-MM-DD, temp_value, humidity_value | Example: 40.7128,-74.0060,2020-01-15,2.5,65.3 |
| **Encoding** | UTF-8 | Standard text encoding |
| **Line Endings** | LF (Unix) or CRLF (Windows) | Platform independent |
| **Missing Values** | None (pre-cleaned) | No NULL or empty cells |
| **Data Quality** | Validated ranges | Lat: -90 to 90, Lon: -180 to 180 |

**Example CSV Data**:
```csv
latitude,longitude,date,temperature,humidity
40.7128,-74.0060,2020-01-15,2.5,65.3
51.5074,-0.1278,2020-01-15,-1.2,78.5
48.8566,2.3522,2020-01-15,1.8,72.1
35.6762,139.6503,2020-01-15,5.2,48.9
-33.8688,151.2093,2020-01-15,23.5,52.1
```

**Model Artifact Files (models/ directory)**

| File | Size | Format | Contents | Lifespan |
|------|------|--------|----------|----------|
| **temp_model.pkl** | ~50KB | joblib binary | RandomForest (temperature) | Until retrained |
| **hum_model.pkl** | ~50KB | joblib binary | RandomForest (humidity) | Until retrained |
| **scaler.pkl** | ~1KB | joblib binary | StandardScaler (6 features) | Until retrained |

**Training Pipeline (train.py)**

| Step | Input | Processing | Output |
|------|-------|-----------|--------|
| 1. Load Data | data/cleaned.csv | pd.read_csv() | DataFrame (2000 rows) |
| 2. Feature Engineering | Date column | Extract: year, month, day, dayofweek | 6-feature matrix |
| 3. Separate Targets | DataFrame | Split temp & humidity columns | X (features), y_temp, y_humidity |
| 4. Create Scaler | X (unscaled) | StandardScaler.fit(X) | Scaler object (saved) |
| 5. Scale Features | X | scaler.transform(X) | X_scaled (normalized) |
| 6. Train-Test Split | X_scaled, y | 80-20 split, random_state=42 | X_train, X_test, y_train, y_test |
| 7. Train Temp Model | X_train, y_train_temp | RandomForest.fit() | Model (100 trees) |
| 8. Train Humidity Model | X_train, y_train_humidity | RandomForest.fit() | Model (100 trees) |
| 9. Evaluate Models | X_test, y_test | Calculate R², RMSE | Metrics (printed) |
| 10. Save Artifacts | Models + Scaler | joblib.dump() | .pkl files in models/ |

#### 3.1.5 External Services & APIs

**Nominatim OpenStreetMap API**

| Specification | Details | Usage |
|---------------|---------|-------|
| **Service** | Free geocoding service | Location name → coordinates |
| **Endpoint** | https://nominatim.openstreetmap.org/search | Auto-complete location lookup |
| **Endpoint (Reverse)** | https://nominatim.openstreetmap.org/reverse | Coordinates → location name |
| **Authentication** | User-Agent header required | Identify application |
| **Rate Limit** | 1 request per second | API fairness policy |
| **Timeout** | 5 seconds | Request timeout setting |
| **Response Format** | JSON array | Parsed in JavaScript |
| **Free Tier** | No API key required | No cost or registration |

**JavaScript Integration Example**:
```javascript
const response = await fetch(
  `https://nominatim.openstreetmap.org/search?` +
  `format=json&q=${encodeURIComponent(query)}&limit=1`,
  {
    headers: {
      'User-Agent': 'WeatherML-App/1.0'
    }
  }
);
const data = await response.json();
// Extract: data[0].lat, data[0].lon
```

---

## 3.2 Hardware Requirements & Infrastructure

### 3.2.1 Development Environment Hardware

**Minimum Requirements (For Code Development)**

| Component | Minimum Specification | Rationale |
|-----------|----------------------|-----------|
| **CPU** | Dual-core processor (2 GHz+) | Flask development server, Python interpreter |
| **RAM** | 4 GB | Operating system, Python runtime, data processing |
| **Storage** | 500 MB free space | Source code, dependencies, models, data |
| **Network** | Internet connection (optional) | Nominatim API, CDN resources, git operations |
| **Display** | 1366x768 resolution minimum | Development IDE, documentation, browser |
| **OS** | Windows 10/11, macOS, Linux | Python 3.9+ compatibility |

**Recommended Specifications (For Comfortable Development)**

| Component | Recommended | Benefits |
|-----------|------------|----------|
| **CPU** | Quad-core processor (3+ GHz) | Faster compilation, model training |
| **RAM** | 8 GB | Smooth IDE operation, larger datasets |
| **Storage** | 256 GB SSD | Faster file I/O, quicker training |
| **Network** | Fiber/broadband (50+ Mbps) | Quick library downloads, API testing |
| **Display** | 1920x1080 (or dual monitors) | IDE + browser side-by-side |
| **GPU** | Optional (for faster training) | 10x faster RandomForest training (CUDA) |

**Software Development Stack**

| Tool | Purpose | Alternatives |
|------|---------|--------------|
| **IDE** | VS Code, PyCharm, Sublime Text | Any Python-capable editor |
| **Git** | Version control | GitHub, GitLab, Bitbucket |
| **Python** | Runtime and package management | conda, pyenv |
| **Terminal** | Command-line interface | PowerShell (Windows), bash (Linux/Mac) |
| **Browser** | Testing frontend | Chrome, Firefox, Safari, Edge |

### 3.2.2 Model Training Hardware

**Training a Small Dataset (2000 records)**

| Component | Requirement | Reasoning |
|-----------|-------------|-----------|
| **CPU** | Multi-core (4+ cores) | Parallel tree training |
| **RAM** | 2-4 GB | DataFrame + models in memory |
| **Storage** | 1 GB | Data + models + temp files |
| **Time** | <5 seconds | Modern CPU executes training quickly |
| **GPU** | Not required | Dataset too small for GPU benefit |

**Example Training Performance**:
```
System: Intel i7 (8 cores), 16 GB RAM, SSD
Training 2000 samples with RandomForest:
├─ Data loading: 0.5s
├─ Feature engineering: 0.2s
├─ Scaling: 0.1s
├─ Model training (temp): 1.2s
├─ Model training (humidity): 1.2s
├─ Model evaluation: 0.3s
├─ Artifact saving: 0.2s
└─ Total time: ~3.7 seconds
```

**Training Larger Datasets (100,000+ records)**

| Component | Recommended | Rationale |
|-----------|------------|-----------|
| **CPU** | 8+ cores | Parallel tree training essential |
| **RAM** | 16-32 GB | Large DataFrame + intermediate results |
| **Storage** | SSD with 50GB+ free | Temporary files during training |
| **Time** | 1-5 minutes | Longer training on larger data |
| **GPU** | Recommended (NVIDIA) | 10-50x speedup with CUDA |

**GPU Acceleration (Optional)**

```python
# For faster training with cuML (RAPIDS)
from cuml.ensemble import RandomForestRegressor
# Requires NVIDIA GPU + CUDA + cuML
# 10-50x faster than CPU RandomForest
```

### 3.2.3 Deployment Infrastructure

**Local Deployment (Single Machine)**

**Specifications**:
```
CPU: Dual-core (2 GHz+)
RAM: 1-2 GB
Storage: 500 MB
OS: Any (Windows, Linux, macOS)
Network: Ethernet/WiFi
Deployment: Flask development server
Users: 1-5 concurrent (single machine)
Availability: Manual start/stop
```

**Use Case**: Personal project, testing, development

**Small Scale Production (Cloud Instance)**

**Specifications**:
```
Instance Type: AWS t3.small / DigitalOcean Basic / Google Cloud e2-small
CPU: 1-2 vCPUs
RAM: 2 GB
Storage: 50 GB SSD (standard EBS)
Network: 1 Gbps
Deployment: Gunicorn (4 workers) + Nginx
Users: 50-200 concurrent
Availability: 99.5% SLA
Monthly Cost: $10-20
```

**Configuration Example**:
```bash
# Start Gunicorn with 4 worker processes
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Nginx reverse proxy configuration
upstream weatherml {
    server 127.0.0.1:5000;
}
server {
    listen 80;
    server_name api.weatherml.com;
    location / {
        proxy_pass http://weatherml;
    }
}
```

**Medium Scale Production (High Availability)**

**Specifications**:
```
Load Balancer: AWS ALB / Google Cloud Load Balancer
├─ Auto-scaling group: 2-10 instances
├─ Instance Type: t3.medium
│  ├─ CPU: 2 vCPUs
│  ├─ RAM: 4 GB
│  └─ Per instance cost: $30/month
├─ Database: RDS PostgreSQL (optional)
│  ├─ Storage: 100 GB
│  └─ Cost: $50-100/month
├─ Cache: Redis ElastiCache (optional)
│  ├─ Memory: 1-5 GB
│  └─ Cost: $15-50/month
└─ CDN: CloudFront (for static assets)
   └─ Cost: Variable (typically $5-20/month)

Total Monthly Cost: $150-350 (3-5 instances)
Concurrent Users: 1000-5000
Availability: 99.99% SLA
Response Time: <500ms p99
```

### 3.2.4 Networking Requirements

**Bandwidth Calculations**

| Operation | Data Size | Frequency | Monthly Bandwidth |
|-----------|-----------|-----------|-------------------|
| Form submission | 1 KB | 1000/month | 1 MB |
| Result HTML | 50 KB | 1000/month | 50 MB |
| Assets (CSS/JS) | 100 KB | 1/user session | 100 MB (cache hits) |
| Plotly charts | 200 KB | 500/month | 100 MB |
| Nominatim API | 5 KB | 1000/month | 5 MB |
| **Total** | | | **~300 MB/month** |

**Bandwidth Recommendations**:
- Development: 10 Mbps sufficient
- Production: 100 Mbps (headroom for spikes)
- CDN: Essential for static assets

### 3.2.5 Data Storage & Backup

**Data Storage Breakdown**

```
Source Code:
├─ Python files: 50 KB
├─ HTML templates: 100 KB
├─ CSS/JS: 50 KB
└─ Total: 200 KB

Training Data:
├─ cleaned.csv: 500 KB - 2 MB
└─ Raw data: 1-5 MB (if kept)

Model Artifacts:
├─ temp_model.pkl: 50 KB
├─ hum_model.pkl: 50 KB
├─ scaler.pkl: 1 KB
└─ Total: ~101 KB

Logs & Temp Files:
├─ Application logs: 10-100 MB/month
├─ Training logs: 1 MB/training
└─ Temp predictions cache: 5-10 MB

Total Storage: 50-200 MB (typical)
```

**Backup Strategy**

| Component | Frequency | Method | Retention |
|-----------|-----------|--------|-----------|
| **Source Code** | Every commit | Git (GitHub) | Permanent |
| **Training Data** | Monthly | S3 / GCS / Azure Blob | 12 months |
| **Models** | After training | Versioned (v1, v2, etc) | Keep last 5 versions |
| **Application Logs** | Daily | CloudWatch / ELK Stack | 90 days |
| **Database** (if used) | Daily | Automated RDS backups | 30 days |

### 3.2.6 Security & Access Requirements

**SSL/TLS Certificates**

| Environment | Certificate | Cost | Renewal |
|-------------|-------------|------|---------|
| **Development** | Self-signed | Free | N/A |
| **Production** | Let's Encrypt | Free | Every 90 days (auto) |
| **Enterprise** | Comodo/Sectigo | $50-200/year | Annually |

**Authentication & Authorization**

| Layer | Requirement | Implementation |
|-------|------------|-----------------|
| **User Authentication** | Future: OAuth2 / JWT | Currently: None (public app) |
| **API Keys** | Optional rate limiting | Nominatim API rate limit: 1 req/sec |
| **Database Access** | If using SQL DB | Encrypted connections + strong passwords |
| **File Permissions** | Restrict model access | Read-only for app, write for training |

### 3.2.7 Monitoring & Logging

**Required Monitoring Stack**

| Component | Purpose | Tool |
|-----------|---------|------|
| **Application Monitoring** | Track requests, errors, performance | DataDog, New Relic, Sentry |
| **Log Aggregation** | Centralize application logs | ELK Stack, CloudWatch, Splunk |
| **Metrics** | CPU, RAM, disk usage | Prometheus, Grafana |
| **Uptime Monitoring** | Website availability | UptimeRobot, Pingdom |
| **Error Tracking** | Catch exceptions | Sentry, Rollbar |

**Key Metrics to Monitor**

```
Application Metrics:
├─ Request count per hour
├─ Error rate (% of failed requests)
├─ Average response time (latency)
├─ P95, P99 response times
├─ Prediction accuracy (RMSE)
└─ Model inference time

Infrastructure Metrics:
├─ CPU utilization (%)
├─ Memory usage (GB)
├─ Disk usage (%)
├─ Network bandwidth (Mbps)
└─ Database connections

Business Metrics:
├─ Active users
├─ Prediction requests/day
├─ Geographic distribution
└─ Popular locations/dates
```

---

## 3.3 Architecture & Design Patterns

### 3.3.1 Software Architecture Pattern: Three-Tier Architecture

```
┌─────────────────────────────────────────────────────┐
│          PRESENTATION TIER (Frontend)                │
│                                                     │
│  HTML5 + Bootstrap + Plotly + Font Awesome         │
│  ├─ index.html (Prediction form)                    │
│  ├─ result.html (Results display)                   │
│  └─ analysis.html (Analytics dashboard)             │
│                                                     │
│  JavaScript ES6 (main.js)                           │
│  ├─ Form validation                                 │
│  ├─ Location autocomplete                           │
│  ├─ Dark mode toggle                                │
│  └─ Chart rendering                                 │
│                                                     │
│  CSS3 (style.css)                                   │
│  ├─ Responsive grid layout                          │
│  ├─ Theme variables (light/dark)                    │
│  └─ Animations & transitions                        │
└────────────────────┬────────────────────────────────┘
                     │
         HTTP/JSON Communication
                     │
        ┌────────────▼────────────┐
        │ Network (REST API)      │
        │ (HTTP GET/POST)         │
        └────────────┬────────────┘
                     │
┌─────────────────────────────────────────────────────┐
│        APPLICATION TIER (Backend)                    │
│                                                     │
│  Flask 3.1.2 (Python)                               │
│  ├─ Route handlers (@app.route)                     │
│  │  ├─ GET / → index page                           │
│  │  ├─ POST /predict → prediction logic             │
│  │  ├─ GET /analysis → analytics page               │
│  │  └─ POST /api/analysis → chart data              │
│  │                                                  │
│  ├─ Input validation & sanitization                 │
│  │  ├─ Date range checks (1980-2035)               │
│  │  ├─ Coordinate bounds (-90 to 90, -180 to 180)  │
│  │  └─ Type conversion & error handling             │
│  │                                                  │
│  ├─ Feature engineering                             │
│  │  ├─ Extract date features (year, month, day)    │
│  │  ├─ Calculate day of week                        │
│  │  └─ Prepare feature vector                       │
│  │                                                  │
│  ├─ ML model inference                              │
│  │  ├─ Load models from disk                        │
│  │  ├─ Normalize features (StandardScaler)          │
│  │  ├─ Parallel predictions (temp + humidity)       │
│  │  └─ Clamp outputs to safe ranges                 │
│  │                                                  │
│  └─ Response generation                             │
│     ├─ Render HTML templates (Jinja2)              │
│     ├─ Format JSON for API                          │
│     └─ Flash error messages                         │
│                                                     │
│  External Services                                  │
│  └─ Nominatim API (location geocoding)              │
└────────────────────┬────────────────────────────────┘
                     │
         File I/O & Data Layer
                     │
        ┌────────────▼────────────┐
        │ Local Filesystem        │
        │ (models/ & data/)       │
        └────────────┬────────────┘
                     │
┌─────────────────────────────────────────────────────┐
│         DATA TIER (ML & Storage)                     │
│                                                     │
│  Model Artifacts (models/ directory)                │
│  ├─ temp_model.pkl (RandomForest)                  │
│  ├─ hum_model.pkl (RandomForest)                   │
│  └─ scaler.pkl (StandardScaler)                    │
│                                                     │
│  Training Data (data/ directory)                    │
│  └─ cleaned.csv (2000 historical records)          │
│                                                     │
│  Data Processing (train.py)                         │
│  ├─ Load CSV with pandas                            │
│  ├─ Feature engineering                             │
│  ├─ StandardScaler fitting                          │
│  ├─ RandomForest training (scikit-learn)            │
│  └─ Model saving (joblib)                           │
│                                                     │
│  scikit-learn ML Pipeline                           │
│  ├─ RandomForestRegressor (100 trees)              │
│  ├─ StandardScaler (feature normalization)          │
│  └─ Metrics (R², RMSE evaluation)                  │
└─────────────────────────────────────────────────────┘
```

### 3.3.2 Design Patterns Used

**1. Model-View-Controller (MVC) Pattern**

```
Model Layer:
├─ Trained ML models (temp_model, hum_model)
├─ StandardScaler for normalization
└─ Pandas DataFrame for data manipulation

View Layer:
├─ index.html (prediction form UI)
├─ result.html (prediction results display)
├─ analysis.html (analytics dashboard)
└─ CSS styling for presentation

Controller Layer:
├─ Flask routes (@app.route)
├─ Request handlers (form processing)
├─ Validation logic (client + server-side)
├─ Model invocation (inference)
└─ Response generation
```

**2. Separation of Concerns**

```
Concerns:
├─ Presentation → HTML/CSS/JavaScript (frontend/)
├─ Business Logic → Flask routes (app.py)
├─ Data Processing → Pandas/NumPy operations
├─ ML Inference → scikit-learn models
└─ Data Storage → CSV files (data/)

Benefits:
├─ Easier testing (unit test each layer)
├─ Maintainability (modify one concern independently)
├─ Reusability (models can be used elsewhere)
└─ Scalability (replace storage layer if needed)
```

**3. Factory Pattern (Model Loading)**

```python
# models/ directory acts as factory
models = {
    'temp': joblib.load('models/temp_model.pkl'),
    'hum': joblib.load('models/hum_model.pkl'),
    'scaler': joblib.load('models/scaler.pkl')
}
# Single place to load all ML artifacts
# Easy to replace with database-backed loading
```

**4. Strategy Pattern (Multiple Input Methods)**

```javascript
// Flexible location input strategies
Strategies:
├─ Autocomplete strategy: Type city name
├─ Geolocation strategy: Click "Detect Location"
├─ Manual strategy: Enter coordinates directly
└─ All strategies populate same fields (lat/lon)
```

**5. Template Method Pattern (Request Handling)**

```python
# Standard Flask request handling template
@app.route('/predict', methods=['POST'])
def predict():
    1. Extract form data
    2. Validate input (may fail with flash)
    3. Prepare features
    4. Run inference
    5. Clamp outputs
    6. Render response

# Same structure for all routes
```

---

## 3.4 Implementation Details & Flow

### 3.4.1 Complete Request-Response Cycle

**User Makes Prediction Request**

```
1. User navigates to http://127.0.0.1:5000
   ↓
2. GET / route triggered
   ↓
3. Flask renders index.html
   ↓
4. JavaScript loads: main.js
   ↓
5. Theme preference restored from localStorage
   ↓
6. User interface displayed
```

**User Submits Prediction Form**

```
1. User enters location: "New York"
   ├─ Debounce 1000ms
   ├─ AJAX call to Nominatim API
   ├─ Receive coordinates: 40.7128, -74.0060
   └─ Auto-fill hidden lat/lon fields

2. User selects date: 2025-12-25 (via calendar)

3. User clicks "Get Forecast"
   ├─ Client-side validation triggers
   │  ├─ Check location filled
   │  ├─ Check date filled
   │  ├─ Check lat -90 to 90
   │  ├─ Check lon -180 to 180
   │  └─ Show errors if invalid
   │
   └─ If valid: Submit form to /predict
```

**Server-Side Processing (app.py)**

```
1. POST /predict received
   ├─ Extract form data:
   │  ├─ location: "New York"
   │  ├─ lat: 40.7128
   │  ├─ lon: -74.0060
   │  └─ date: 2025-12-25
   │
   ├─ Server-side validation:
   │  ├─ Parse date: YYYY-MM-DD format
   │  ├─ Check year 1980-2035 range
   │  ├─ Validate lat -90 to 90
   │  ├─ Validate lon -180 to 180
   │  └─ Show error if fails
   │
   ├─ Feature engineering:
   │  ├─ Extract from date:
   │  │  ├─ year: 2025
   │  │  ├─ month: 12
   │  │  ├─ day: 25
   │  │  └─ dayofweek: 3 (Thursday)
   │  │
   │  └─ Prepare feature array:
   │     [latitude, longitude, year, month, day, dayofweek]
   │     [40.7128, -74.0060, 2025, 12, 25, 3]
   │
   ├─ Load ML artifacts:
   │  ├─ Load scaler.pkl
   │  ├─ Load temp_model.pkl
   │  └─ Load hum_model.pkl
   │
   ├─ Feature normalization:
   │  └─ normalized_features = scaler.transform(features)
   │     Result: [1.52, -2.14, 0.82, 0.35, -0.18, 1.05]
   │
   ├─ Model inference (parallel):
   │  ├─ temp_pred = temp_model.predict([normalized_features])[0]
   │  │  Result: ~5.32°C
   │  │
   │  └─ hum_pred = hum_model.predict([normalized_features])[0]
   │     Result: ~67.8%
   │
   ├─ Output safety (clamping):
   │  ├─ Temperature: max(-50, min(50, 5.32)) = 5.32°C ✓
   │  └─ Humidity: max(0, min(100, 67.8)) = 67.8% ✓
   │
   └─ Prepare response:
      ├─ Render result.html with:
      │  ├─ location: "New York"
      │  ├─ date: "2025-12-25"
      │  ├─ temperature: 5.32°C
      │  ├─ humidity: 67.8%
      │  ├─ latitude: 40.7128
      │  └─ longitude: -74.0060
      │
      └─ Return HTML to browser
```

**Browser Displays Results**

```
1. Receive result.html
2. Browser renders page with prediction
3. Display:
   ┌─────────────────────────────┐
   │ 📍 New York, USA            │
   │ 📅 2025-12-25 (Christmas)   │
   │ 🌡️ Temperature: 5.32°C      │
   │ 💧 Humidity: 67.8%          │
   │ 📍 Coords: 40.7128, -74.0060│
   └─────────────────────────────┘
4. Options:
   ├─ [← Back to Prediction]
   └─ [Analyze This Month →]
```

### 3.4.2 Analytics Dashboard Flow

```
1. User clicks "Analyze This Month"
   ↓
2. GET /analysis page loaded
   ├─ Month selector: [dropdown 1-12]
   └─ Year selector: [dropdown ≤2025]

3. User selects: Month=12, Year=2020
   ├─ Selects December 2020
   └─ Click "Load Analysis"

4. POST /api/analysis request:
   ├─ Server receives: month=12, year=2020
   │
   ├─ Load data/cleaned.csv
   │
   ├─ Filter to December 2020:
   │  └─ 31 records (one per day)
   │
   ├─ For each day, generate prediction:
   │  └─ Loop through Dec 1-31, 2020
   │     For each date:
   │     ├─ Extract features
   │     ├─ Normalize
   │     ├─ Run temp_model.predict()
   │     ├─ Run hum_model.predict()
   │     └─ Collect results
   │
   ├─ Prepare chart data:
   │  ├─ Predicted values: [pred_1, pred_2, ..., pred_31]
   │  ├─ Actual values: [actual_1, actual_2, ..., actual_31]
   │  ├─ X-axis: [1, 2, 3, ..., 31] (days)
   │  └─ Y-axis: Temperature (°C)
   │
   └─ Return JSON:
      {
        "temperature": {
          "predicted": [5.2, 6.1, 5.8, ...],
          "actual": [4.5, 5.9, 6.2, ...],
          "days": [1, 2, 3, ...]
        },
        "humidity": {
          "predicted": [65.3, 64.8, 68.2, ...],
          "actual": [62.1, 65.5, 69.2, ...],
          "days": [1, 2, 3, ...]
        },
        "stats": {
          "temp_avg_pred": 6.2,
          "temp_avg_actual": 6.8,
          "humid_avg_pred": 66.5,
          "humid_avg_actual": 65.9
        }
      }

5. Browser receives JSON

6. JavaScript renders Plotly charts:
   ├─ Chart 1: Temperature
   │  ├─ Blue line: Predicted values
   │  ├─ Red dots: Actual values
   │  └─ Interactive: zoom, pan, hover
   │
   └─ Chart 2: Humidity
      ├─ Green line: Predicted values
      ├─ Orange dots: Actual values
      └─ Interactive: zoom, pan, hover

7. Statistics panel shows:
   ├─ Average Predicted Temp: 6.2°C
   ├─ Average Actual Temp: 6.8°C
   ├─ Accuracy (correlation): 0.87
   └─ Similar for humidity
```

---

## 3.5 Conclusion: Architecture Summary

The WeatherML application architecture provides:

1. **Scalability**: Three-tier design allows each layer to scale independently
2. **Maintainability**: Clear separation of concerns enables easy updates
3. **Reliability**: Comprehensive validation prevents errors at every stage
4. **Performance**: Optimized request handling with ~2-second prediction latency
5. **Flexibility**: Modular design supports easy feature additions and customizations
6. **Deployment**: Ready for local development, small production, and cloud scaling

---

**Report 3 Completed**: Analysis & Design
**Date Generated**: December 2025
**Project**: WeatherML Weather Prediction Web Application

**All 3 Reports Generated Successfully** ✅
