# Bitcoin All-Time High Distance Analyzer

A comprehensive web-based tool to analyze Bitcoin's distance from all-time high (ATH) and contextualize current price action within historical distributions. Features real-time price tracking, volatility analysis, and interactive visualizations to understand market cycle positioning.

## 🚀 Features

### 📊 Web Dashboard

- **Real-time Dashboard**: Live Bitcoin price updates with ATH distance tracking
- **Interactive Charts**: Time series with customizable ranges (7D, 1M, 3M, 6M, 1Y, 5Y, 10Y, ALL)
- **Distribution Analysis**: Histogram and cumulative distribution charts
- **Volatility Metrics**: Standard deviation, coefficient of variation, and statistical zones

### 📈 Advanced Analytics

- **Historical ATH Analysis**: Complete Bitcoin history from 2010 (3,900+ days)
- **Percentile Rankings**: Understand how rare current price levels are
- **Volatility Bands**: Visual ±1σ and ±2σ ranges for context
- **Statistical Classification**: Normal, Unusual, and Extreme range identification

### 🔄 Real-time Data

- **Live Price Updates**: Automatic refresh every 30 seconds
- **Multiple API Sources**: CoinGecko (primary), CoinMarketCap (backup), yfinance (fallback)
- **Smart Caching**: Incremental data updates for 5000x faster performance
- **Rate Limit Handling**: Graceful fallback between API sources

### 🎯 Professional Features

- **REST API**: Comprehensive endpoints for integration
- **Hot Reload Development**: Changes automatically refresh
- **Production Ready**: Gunicorn support for deployment
- **Responsive Design**: Modern UI with Bitcoin-themed styling

## 🌐 Web Interface

### Quick Start

1.  **Install UV Package Manager**

    ```bash
    # Install UV package manager
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Authenticate with Google Cloud**

    For local development, the application needs to authenticate with Google Cloud to access the GCS bucket. Run the following command and follow the prompts to log in with your GCP account. This step only needs to be done once.

    ```bash
    gcloud auth application-default login
    ```

3.  **Start the Web Application**
    ```bash
    # Start the web application
    uv run bitcoin-ath-web
    ```

Open your browser to [http://localhost:5000](http://localhost:5000) to see the dashboard!

### Dashboard Features

#### 📊 Real-time Metrics

- **Current Price**: Live Bitcoin price with 24h change
- **ATH Distance**: Percentage distance from all-time high
- **Percentile Rank**: How rare this proximity is (14th percentile = only 14% of days closer)
- **Dollar Difference**: Actual dollar amount from ATH

#### 📈 Interactive Charts

1. **Time Series Chart**

   - Toggle between different time ranges
   - Hover for detailed daily information
   - Visual ATH markers and trend analysis

2. **Distribution Histogram**

   - Shows frequency of different ATH distances
   - Mean/median lines for reference
   - Current position indicator
   - Volatility bands (±1σ, ±2σ)

3. **Cumulative Distribution**
   - Percentile finder curve
   - Current position with exact percentile
   - Legend positioned to avoid data overlap

#### 🔬 Volatility Analysis

- **Standard Deviation**: Typical spread of ATH distances (~22-25%)
- **Coefficient of Variation**: Normalized volatility measure
- **Current Position**: How many standard deviations from average
- **Zone Classification**:
  - 🟢 **Normal Range (±1σ)**: Typical Bitcoin behavior
  - 🟡 **Unusual Range (±2σ)**: Uncommon but not extreme
  - 🔴 **Extreme Range (>2σ)**: Historically rare positioning

## 🛠️ Installation & Setup

### Prerequisites

- **Python 3.8+** - Backend API and data processing
- **Node.js 18+** - Frontend build tools and React development
- **[UV Package Manager](https://github.com/astral-sh/uv)** - Python dependency management

### Install UV

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Alternative: pip install uv
```

### Project Setup

```bash
# Clone/navigate to project directory
cd bitcoin-data

# Install Python dependencies
uv sync --extra web

# Install Node.js dependencies (for React/TypeScript frontend)
npm install

# For development with both frontend and backend
uv sync --extra dev
```

#### Frontend Dependencies

The React/TypeScript frontend includes:

- **React 18** - Modern UI framework
- **TypeScript** - Type safety and enhanced developer experience
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **Plotly.js** - Interactive data visualizations
- **PostCSS & Autoprefixer** - CSS processing and browser compatibility

## 🚀 Usage

### Web Application

#### Development Mode (React + Flask)

For development, you'll run both the React/TypeScript frontend and Python backend:

```bash
# Terminal 1: Start Flask API server
uv run python web_deployment_example_react.py

# Terminal 2: Start Vite dev server (React/TypeScript)
npm run dev
```

The Vite dev server (http://localhost:5173) will proxy API requests to Flask (http://localhost:8080), providing:

- **Hot Reload**: Instant updates when you modify React components
- **TypeScript Checking**: Real-time type checking and error highlighting
- **Tailwind CSS**: Live CSS processing and optimization
- **API Integration**: Seamless communication between frontend and backend

#### Production Mode (Single Server)

For production-like testing locally:

```bash
# Build the React app first
npm run build

# Start Flask server (serves built React app)
uv run python web_deployment_example_react.py
```

#### Legacy Mode (Original HTML)

The original single-file HTML version is still available:

```bash
# Start original Flask server
uv run python web_deployment_example.py
```

### Command Line Analysis

```bash
# Run core analysis
uv run python bitcoin_ath_analyzer.py

# Generate static charts
uv run python bitcoin_ath_analyzer.py --plot
```

### Programmatic Usage

```python
from bitcoin_ath_analyzer import BitcoinATHAnalyzer
from api_integrations import get_current_bitcoin_analysis

# Initialize analyzer
analyzer = BitcoinATHAnalyzer()

# Load historical data (uses cache for speed)
analyzer.load_data()

# Get current analysis
current_analysis = get_current_bitcoin_analysis()
print(f"Current distance: {current_analysis['current_distance_from_ath']:.2f}%")
print(f"Percentile rank: {current_analysis['percentile_rank']:.1f}")

# Generate comprehensive report
report = analyzer.get_context_report()
print(report)
```

## 📡 API Endpoints

The web application provides several REST API endpoints:

### Core Analysis

- `GET /api/current-analysis` - Current Bitcoin price and ATH analysis
- `GET /api/historical-data?days=365` - Historical ATH distance data
- `GET /api/distribution-histogram` - Distribution statistics and volatility metrics

### Response Examples

```json
// /api/current-analysis
{
  "success": true,
  "data": {
    "current_price": 105234.56,
    "ath_price": 112345.67,
    "current_distance_from_ath": 6.32,
    "percentile_rank": 14.1,
    "last_updated": "2025-06-23T21:30:00Z"
  }
}

// /api/historical-data?days=365
{
  "success": true,
  "data": {
    "dates": ["2024-06-23", "2024-06-24", ...],
    "distances": [15.2, 14.8, ...],
    "days_requested": 365
  }
}
```

## 📊 Understanding the Metrics

### Core Metric

**Distance from ATH (%) = (ATH - Current Price) / ATH × 100**

### Percentile Interpretation

- **5th percentile**: Only 5% of days have been closer to ATH (extremely rare)
- **14th percentile**: Only 14% of days have been closer to ATH (rare)
- **50th percentile**: Median distance (typical positioning)
- **85th percentile**: 85% of days have been closer to ATH (far from ATH)

### Volatility Context

- **Standard Deviation**: ~22-25% for Bitcoin ATH distances
- **Coefficient of Variation**: ~60-70% (high volatility asset)
- **Current Position**: Measured in standard deviations from mean

### Historical Benchmarks

- **Average Distance**: ~36-38% from ATH
- **Median Distance**: ~35-40% from ATH
- **Days at ATH**: ~150-200 days out of 3,900+ total days (~4-5%)

## 🎯 Use Cases

### Trading & Investment

- **Market Timing**: Identify rare price proximity periods
- **Risk Assessment**: Understand potential correction magnitude
- **Entry/Exit Points**: Historical context for position sizing

### Research & Analysis

- **Cycle Analysis**: Identify market cycle positions
- **Academic Research**: Quantitative Bitcoin market analysis
- **Volatility Studies**: Statistical analysis of price behavior

### Educational

- **Market Education**: Understand Bitcoin's price history
- **Statistical Learning**: Real-world application of percentiles and distributions
- **Visualization**: Interactive charts for data exploration

## 🔧 Development

### Project Structure

```
bitcoin-data/
├── bitcoin_ath_analyzer.py      # Core analysis engine
├── api_integrations.py          # Real-time data & caching
├── web_deployment_example.py    # Flask web application
├── templates/dashboard.html     # Web dashboard UI
├── bitcoin_data_cache.csv       # Cached historical data
├── pyproject.toml              # UV configuration
└── README.md                   # This file
```

### Development Commands

```bash
# Start development server with hot reload
uv run bitcoin-ath-web

# Run analysis script
uv run python bitcoin_ath_analyzer.py

# Update cached data
uv run python api_integrations.py

# Add new dependencies
uv add requests pandas plotly

# Add development dependencies
uv add --dev pytest black ruff
```

### Environment Variables

```bash
# Optional: CoinMarketCap API key for backup data source
export COINMARKETCAP_API_KEY="your_api_key_here"
```

## 📈 Current Market Context

As of the latest update:

- **Bitcoin Price**: ~$105,000
- **Distance from ATH**: ~6.3%
- **Percentile Rank**: ~14th percentile
- **Interpretation**: Bitcoin is unusually close to ATH - this proximity only occurs ~14% of the time
- **Volatility Zone**: Likely "Extreme Range" (>2σ from average)

This represents a historically rare market condition where Bitcoin is trading very close to its all-time high.

## 🚀 Deployment

### Development

```bash
uv run bitcoin-ath-web
```

### Production

```bash
# Install production dependencies
uv sync --extra web

# Use Gunicorn for production
uv run gunicorn -w 4 -b 0.0.0.0:8000 web_deployment_example:app
```

### Docker (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync --extra web
EXPOSE 5000
CMD ["uv", "run", "python", "web_deployment_example.py"]
```

## ☁️ GCP Deployment Guide

This guide walks you through deploying the application to Google Cloud Platform using Cloud Run for the web service and Cloud Scheduler for daily data updates.

### 1. Prerequisites

- A Google Cloud Platform (GCP) project.
- The `gcloud` CLI installed and authenticated (`gcloud auth login`).
- Docker installed locally (for Cloud Build).
- [direnv](https://direnv.net/) (optional, but recommended for managing environment variables).

### 2. Initial Setup

First, set up your environment variables. Replace the placeholder values with your own.

#### Using direnv (Recommended)

1.  Create a file named `.envrc` in the root of the project. Because `.envrc` is listed in `.gitignore`, it will not be committed to your repository.

2.  Copy the following content into your new `.env` file and fill in the placeholder values with your specific GCP details:

    ```sh
    # GCP Configuration
    export PROJECT_ID="your-gcp-project-id"
    export REGION="us-central1"
    export GCS_BUCKET_NAME="your-unique-bucket-name"
    export WEB_SERVICE_NAME="bitcoin-ath-dashboard"
    export JOB_NAME="bitcoin-data-update-job"

    # Optional API Keys
    # export COINMARKETCAP_API_KEY="your_api_key_here"
    ```

3.  Run `direnv allow` in your terminal. `direnv` will now automatically load these environment variables whenever you are in this directory.

#### Manual Export

If you are not using `direnv`, you can manually export the variables in your shell session. Remember to do this for each new terminal session.

```bash
# Configure the gcloud CLI with the values from your .env file
gcloud config set project $PROJECT_ID
gcloud config set run/region $REGION
```

### 3. Enable GCP APIs

Enable the necessary APIs for your project.

```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  cloudscheduler.googleapis.com \
  iam.googleapis.com
```

### 4. Create GCS Bucket and Upload Initial Data

The application needs a GCS bucket to store the `bitcoin_data_cache.csv`.

```bash
# Create the GCS bucket
gcloud storage buckets create gs://$GCS_BUCKET_NAME --location=$REGION

# Run the analysis locally once to generate the initial cache file
uv run python bitcoin_ath_analyzer.py

# Upload the initial cache file to the bucket
gcloud storage cp bitcoin_data_cache.csv gs://$GCS_BUCKET_NAME/bitcoin_data_cache.csv
```

### 5. Build and Deploy the Web Application

The application uses a **React/TypeScript frontend** with a **Python Flask backend**. The deployment uses a multi-stage Docker build:

1. **Stage 1**: Build the React/TypeScript frontend with Node.js and Vite
2. **Stage 2**: Copy the built frontend and set up the Python backend

#### Option A: Using the Deploy Script (Recommended)

The easiest way to deploy is using the provided `deploy.sh` script:

```bash
# Test the build locally first (optional but recommended)
chmod +x test-deployment.sh
./test-deployment.sh

# Deploy to Cloud Run
chmod +x deploy.sh
./deploy.sh
```

The deployment script will automatically:

- Build the multi-stage Docker image (React + Python)
- Deploy to Cloud Run with proper environment variables
- Provide you with the service URL

The test script verifies:

- TypeScript compilation works
- React build completes successfully
- Docker multi-stage build works
- Container starts and responds to requests

#### Option B: Manual Deployment

If you prefer manual control, follow these steps:

First, create a repository in Google Artifact Registry to store your container images.

```bash
gcloud artifacts repositories create bitcoin-app \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker repository for bitcoin-ath-analyzer"
```

Build the container image using Cloud Build and deploy it to Cloud Run.

```bash
# Build the multi-stage container image (React/TypeScript + Python)
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/bitcoin-app/$WEB_SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $WEB_SERVICE_NAME \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/bitcoin-app/$WEB_SERVICE_NAME \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars="GCS_BUCKET_NAME=$GCS_BUCKET_NAME" \
  --max-instances "1"
```

#### Frontend Architecture

The React/TypeScript frontend provides:

- **Type Safety**: Full TypeScript integration with comprehensive type definitions
- **Modern UI**: Tailwind CSS with custom Bitcoin-themed design system
- **Interactive Charts**: Plotly.js visualizations with real-time data
- **Responsive Design**: Mobile-friendly interface with utility-first CSS
- **Component Architecture**: Reusable components with error boundaries
- **Hot Reload**: Development server with instant updates

#### Build Process

The Dockerfile handles the complete build process:

1. **Frontend Build**: `npm run build` compiles TypeScript and processes Tailwind CSS
2. **Asset Optimization**: Vite bundles and optimizes all frontend assets
3. **Backend Integration**: Flask serves the built React app from `static/dist/`
4. **Production Ready**: Gunicorn WSGI server for high-performance deployment

After deployment, `gcloud` will provide you with the public URL for your dashboard.

### 7. (Optional) Map a Custom Domain

To host the service at a custom URL like `bitcoin.bawolf.com`:

1.  **Verify Domain Ownership**: If this is the first time you are using this domain with your GCP project, you must verify you own it. Run the following command and follow the instructions in the browser tab that opens.

    ```bash
    gcloud domains verify your-base-domain.com
    ```

    (Replace `your-base-domain.com` with the domain you own, e.g., `bawolf.com`)

2.  **Create the Domain Mapping**: This tells Cloud Run to serve your application from the custom domain.

    ```bash
    gcloud beta run domain-mappings create --service $WEB_SERVICE_NAME --domain bitcoin.your-domain.com --region $REGION
    ```

3.  **Update DNS Records**: The previous command will output a DNS record (usually a CNAME). Add this record to your domain's DNS configuration at your domain registrar. It may take some time for the changes to propagate and for the SSL certificate to be provisioned.

### 6. Create and Deploy the Scheduled Job

This job will run daily to update the data in your GCS bucket.

#### Create a Service Account for the Job

It's a best practice to run the job with dedicated, minimal permissions.

```bash
# Create a service account
gcloud iam service-accounts create $JOB_NAME \
  --display-name "Bitcoin Data Update Job Service Account"

# Grant the service account permissions to access the GCS bucket
gcloud storage buckets add-iam-policy-binding gs://$GCS_BUCKET_NAME \
  --member="serviceAccount:$JOB_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"
```

#### Create the Cloud Run Job

This job will execute our `scheduled_job.py` script.

```bash
# We override the container's default 'gunicorn' command to run our script instead.
gcloud run jobs create $JOB_NAME \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/bitcoin-app/$WEB_SERVICE_NAME \
  --command "/app/.venv/bin/python3" \
  --args "scheduled_job.py" \
  --set-env-vars="GCS_BUCKET_NAME=$GCS_BUCKET_NAME" \
  --service-account "$JOB_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --task-timeout "10m" # Set a timeout for the job
```

#### Create the Cloud Scheduler Trigger

This will trigger the job to run automatically every day.

```bash
# Schedule the job to run every day at 1 AM UTC
gcloud scheduler jobs create http bitcoin-data-daily-update \
  --schedule "0 1 * * *" \
  --http-method POST \
  --uri "https://run.googleapis.com/v1/projects/$PROJECT_ID/locations/$REGION/jobs/$JOB_NAME:run" \
  --oauth-service-account-email "$JOB_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --time-zone "Etc/UTC" \
  --location "$REGION"
```

Your application is now fully deployed and configured to update automatically!

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes and test thoroughly
4. Ensure code quality (`uv run ruff check .`)
5. Update documentation if needed
6. Submit pull request with clear description

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Data Sources**: yfinance, CoinGecko, CoinMarketCap APIs
- **Technologies**: Flask, Plotly.js, UV Package Manager
- **Inspiration**: Bitcoin's incredible price history and the need for statistical context

## ⚠️ Disclaimer

**This tool is for educational and research purposes only.**

- Not financial advice
- Past performance doesn't predict future results
- Always do your own research
- Consult financial professionals before making investment decisions
- Cryptocurrency investments carry significant risk

---

**🔗 Quick Links:**

- [Web Dashboard](http://localhost:5000) (after running `uv run bitcoin-ath-web`)
- [UV Package Manager](https://github.com/astral-sh/uv)
- [Bitcoin Price Data](https://finance.yahoo.com/quote/BTC-USD/)

Built with ❤️ for the Bitcoin community
