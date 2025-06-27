# How Hard Is It to HODL?

A web application that tracks Bitcoin's price relative to its all-time high over time. Shows historical patterns and provides context for current price levels.

🌐 **Live Demo**: [bitcoin.bawolf.com](https://bitcoin.bawolf.com) | 📊 **GitHub**: [github.com/bawolf/bitcoindata](https://github.com/bawolf/bitcoindata)

## What It Does

The app tracks Bitcoin's distance from all-time high and shows:

- Historical charts of Bitcoin's price relative to ATH since 2010
- Statistical analysis of how often Bitcoin trades at different levels
- A table of the "hardest days" to hold Bitcoin (furthest from ATH)
- Current analysis of where Bitcoin stands today

The main metric is "Percent of Previous ATH" (PoPATH) - what percentage of the all-time high Bitcoin was trading at on any given day.

## Technology

- React TypeScript frontend with Plotly.js charts
- Python Flask backend using pandas for data analysis
- Bitcoin price data from CoinGecko and yfinance APIs

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- [UV Package Manager](https://github.com/astral-sh/uv)

### Installation

```bash
# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --extra web
npm install
```

### Development Mode

Run both frontend and backend for development:

```bash
# Terminal 1: Start Flask API server (port 8080)
uv run python app.py

# Terminal 2: Start Vite dev server (port 5173)
npm run dev
```

The Vite dev server proxies API requests to Flask, providing hot reload for React components.

### Production Mode

```bash
# Build React frontend
npm run build

# Start Flask server (serves built React app)
uv run python app.py
```

Open [http://localhost:5000](http://localhost:5000) to view the dashboard.

## The Core Metric

**PoPATH (Percent of Previous ATH)** measures Bitcoin's price as a percentage of its all-time high on that date:

```
PoPATH = (Day's High Price / ATH on That Date) × 100
```

Higher percentages mean Bitcoin is closer to its ATH. Lower percentages indicate it's further away, which historically correlates with more difficult periods for holders.

## API Endpoints

- `GET /api/current-analysis` - Live Bitcoin price and ATH analysis
- `GET /api/historical-data?days=365` - Historical ATH distance data
- `GET /api/distribution-histogram` - Statistical distribution data
- `GET /api/hardest-days` - The most difficult days to hold Bitcoin

### Example Response

```json
{
  "success": true,
  "data": {
    "current_price": 95432.56,
    "ath_price": 108135.67,
    "current_percent_of_ath": 88.25,
    "percentile_rank": 73.4,
    "sentiment": "moderate",
    "last_updated": "2024-01-15T21:30:00Z"
  }
}
```

## Project Structure

```
bitcoin-data/
├── src/                          # React TypeScript frontend
│   ├── components/
│   │   ├── common/              # 5 reusable UI components
│   │   ├── CurrentStats.tsx     # Real-time Bitcoin metrics
│   │   ├── HistoricalChart.tsx  # Time series visualization
│   │   ├── DistributionChart.tsx # Statistical distribution
│   │   ├── CumulativeChart.tsx  # Percentile curve
│   │   └── HardestDaysTable.tsx # Historical difficulty ranking
│   ├── hooks/
│   │   └── useApiData.ts        # Generic typed API hook
│   ├── types/                   # TypeScript definitions
│   ├── utils/                   # Helper functions and chart configs
│   └── App.tsx                  # Main application component
├── app.py                       # Flask web server & API
├── bitcoin_ath_analyzer.py      # Core analysis engine
├── api_integrations.py          # Data fetching & caching
├── scheduled_job.py             # Background update job
├── static/dist/                 # Built React app (production)
├── package.json                 # Node.js dependencies
├── pyproject.toml              # Python dependencies (UV)
└── README.md                   # This file
```

## Deployment

### Prerequisites

- Google Cloud Project with billing enabled
- `gcloud` CLI authenticated
- Docker for Cloud Build

### Environment Setup

Create `.envrc` file:

```bash
export PROJECT_ID="your-gcp-project-id"
export REGION="us-central1"
export GCS_BUCKET_NAME="your-unique-bucket-name"
export WEB_SERVICE_NAME="bitcoin-hodl-dashboard"
export JOB_NAME="bitcoin-data-update-job"
```

### Deployment Steps

```bash
# 1. Enable required APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com cloudscheduler.googleapis.com

# 2. Create GCS bucket for data persistence
gcloud storage buckets create gs://$GCS_BUCKET_NAME --location=$REGION

# 3. Generate initial data and upload
uv run python bitcoin_ath_analyzer.py
gcloud storage cp bitcoin_data_cache.csv gs://$GCS_BUCKET_NAME/

# 4. Deploy using provided script
chmod +x deploy.sh
./deploy.sh
```

The deployment script handles:

- Multi-stage Docker build (React TypeScript + Python Flask)
- Cloud Run deployment with auto-scaling
- Scheduled job setup for daily data updates
- Environment variable configuration

### Custom Domain (Optional)

```bash
# Verify domain ownership
gcloud domains verify your-domain.com

# Create domain mapping
gcloud beta run domain-mappings create \
  --service $WEB_SERVICE_NAME \
  --domain bitcoin.your-domain.com \
  --region $REGION
```

## 📈 Historical Data Sources

The application uses comprehensive Bitcoin price data:

- **2010-2022**: Historical data from multiple exchanges (Mt. Gox, Bitstamp, Coinbase)
- **2022-Present**: Real-time data via CoinGecko and yfinance APIs
- **Total Coverage**: 5,400+ days of Bitcoin price history

### Data Rebuild

If historical data needs refreshing:

```bash
python rebuild_comprehensive_data.py
```

This automatically downloads and merges historical data from trusted sources.

## 🧪 Development Commands

```bash
# Frontend development
npm run dev              # Start Vite dev server
npm run build           # Build React app for production
npm run type-check      # TypeScript validation

# Backend development
uv run python app.py    # Start Flask development server
uv run python bitcoin_ath_analyzer.py --plot  # Generate analysis with charts

# Testing
./test-deployment.sh    # Test Docker build locally
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes with proper TypeScript types
4. Test both frontend and backend changes
5. Ensure code quality (`npm run type-check`, `uv run ruff check .`)
6. Submit pull request with clear description

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**This tool is for educational and research purposes only.**

- Not financial advice
- Past performance doesn't predict future results
- Always do your own research
- Cryptocurrency investments carry significant risk

## 🙏 Acknowledgments

- **Data Sources**: yfinance, CoinGecko APIs, historical Bitcoin exchanges
- **Technologies**: React, TypeScript, Flask, Plotly.js, Tailwind CSS, UV Package Manager
- **Inspiration**: The emotional rollercoaster of Bitcoin hodling

---

Built with ❤️ for understanding Bitcoin's emotional journey through statistical analysis.
