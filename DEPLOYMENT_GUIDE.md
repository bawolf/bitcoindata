# Deployment Guide - React/TypeScript + Flask

## Overview

The Bitcoin HODL Dashboard uses a **multi-stage Docker build** to deploy a React/TypeScript frontend with a Python Flask backend to Google Cloud Run.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Multi-Stage Build                 │
├─────────────────────────────────────────────────────────────┤
│ Stage 1: Frontend Build (Node.js 18 Alpine)               │
│ ├─ Install npm dependencies                                │
│ ├─ Compile TypeScript                                      │
│ ├─ Process Tailwind CSS                                    │
│ ├─ Bundle with Vite                                        │
│ └─ Output: static/dist/ (optimized assets)                 │
├─────────────────────────────────────────────────────────────┤
│ Stage 2: Backend Runtime (Python 3.11 Slim)              │
│ ├─ Copy built frontend from Stage 1                        │
│ ├─ Install Python dependencies with UV                     │
│ ├─ Configure Flask to serve React app                      │
│ └─ Run with Gunicorn WSGI server                          │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

### Local Development

- **Python 3.8+** with UV package manager
- **Node.js 18+** with npm
- **Docker** (for local testing)

### Cloud Deployment

- **Google Cloud Project** with billing enabled
- **gcloud CLI** configured and authenticated
- **Required APIs enabled**:
  - Cloud Run API
  - Cloud Build API
  - Artifact Registry API

## Quick Deployment

### 1. Environment Setup

Create `.envrc` file (not committed to git):

```bash
# GCP Configuration
export PROJECT_ID="your-gcp-project-id"
export REGION="us-central1"
export GCS_BUCKET_NAME="your-unique-bucket-name"
export WEB_SERVICE_NAME="bitcoin-ath-dashboard"
```

Then run:

```bash
direnv allow  # or manually export the variables
```

### 2. Test Build Locally

```bash
# Test the complete build process
chmod +x test-deployment.sh
./test-deployment.sh
```

This verifies:

- ✅ TypeScript compilation
- ✅ React/Vite build
- ✅ Docker multi-stage build
- ✅ Container startup

### 3. Deploy to Cloud Run

```bash
# Deploy using the automated script
chmod +x deploy.sh
./deploy.sh
```

## Build Process Details

### Frontend Build (Stage 1)

The frontend build process:

1. **Dependency Installation**

   ```dockerfile
   COPY package*.json tsconfig*.json tailwind.config.js postcss.config.js ./
   RUN npm ci --only=production
   ```

2. **Source Code Processing**

   ```dockerfile
   COPY src/ ./src/
   COPY index.html vite.config.js ./
   ```

3. **Build Execution**

   ```dockerfile
   RUN npm run build  # Runs: tsc && vite build
   ```

   This creates:

   - TypeScript compilation
   - Tailwind CSS processing
   - Vite bundling and optimization
   - Output in `static/dist/`

### Backend Runtime (Stage 2)

The backend setup:

1. **Copy Built Frontend**

   ```dockerfile
   COPY --from=frontend /app/static/dist ./static/dist
   ```

2. **Python Dependencies**

   ```dockerfile
   COPY pyproject.toml uv.lock ./
   RUN uv sync --extra web
   ```

3. **Application Files**

   ```dockerfile
   COPY *.py ./
   COPY templates/ ./templates/
   ```

4. **Runtime Configuration**
   ```dockerfile
   CMD .venv/bin/gunicorn --workers 2 --bind "0.0.0.0:$PORT" --preload web_deployment_example_react:app
   ```

## File Structure for Deployment

```
bitcoin-data/
├── Dockerfile                 # Multi-stage build configuration
├── .dockerignore             # Excludes unnecessary files from build
├── deploy.sh                 # Automated deployment script
├── test-deployment.sh        # Local build testing
├── package.json              # Node.js dependencies
├── tsconfig.json            # TypeScript configuration
├── tailwind.config.js       # Tailwind CSS configuration
├── vite.config.js           # Vite build configuration
├── src/                     # React/TypeScript source code
├── pyproject.toml           # Python dependencies
├── web_deployment_example_react.py  # Flask app with React integration
└── static/                  # Build output directory
    └── dist/               # Created during build
```

## Environment Variables

### Required for Deployment

- `PROJECT_ID` - Google Cloud Project ID
- `GCS_BUCKET_NAME` - Google Cloud Storage bucket for data caching

### Optional

- `WEB_SERVICE_NAME` - Cloud Run service name (default: "bitcoin-ath-dashboard")
- `REGION` - GCP region (default: "us-central1")

### Runtime Environment

- `PORT` - Set automatically by Cloud Run (default: 8080)

## Deployment Scripts

### `deploy.sh`

- Validates environment variables
- Builds multi-stage Docker image
- Deploys to Cloud Run
- Sets environment variables
- Provides service URL

### `test-deployment.sh`

- Tests TypeScript compilation
- Tests React build process
- Tests Docker build locally
- Tests container startup
- Verifies HTTP responses

## Build Optimization

### Docker Layer Caching

- Package files copied first for better caching
- Source code copied after dependencies
- Multi-stage build reduces final image size

### Frontend Optimization

- TypeScript compilation with strict checking
- Tailwind CSS purging removes unused styles
- Vite bundling with tree-shaking
- Asset optimization and compression

### Backend Optimization

- UV for fast Python dependency resolution
- Gunicorn with multiple workers
- Preload flag for faster startup
- Minimal Python base image

## Troubleshooting

### Build Failures

**TypeScript Errors:**

```bash
npm run type-check  # Check for type errors
```

**React Build Errors:**

```bash
npm run build  # Test build locally
```

**Docker Build Errors:**

```bash
docker build -t test .  # Test Docker build
```

### Deployment Failures

**Authentication Issues:**

```bash
gcloud auth login
gcloud config set project $PROJECT_ID
```

**API Not Enabled:**

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

**Insufficient Permissions:**

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:your-email@domain.com" \
  --role="roles/run.admin"
```

### Runtime Issues

**Container Won't Start:**

- Check Cloud Run logs in GCP Console
- Verify environment variables are set
- Ensure GCS bucket exists and is accessible

**Frontend Not Loading:**

- Verify React build completed successfully
- Check that Flask is serving from `static/dist/`
- Verify Vite build output exists

## Production Considerations

### Performance

- **CDN**: Consider adding Cloud CDN for static assets
- **Caching**: Implement Redis for API response caching
- **Monitoring**: Set up Cloud Monitoring and alerting

### Security

- **IAM**: Use least-privilege service accounts
- **Secrets**: Store API keys in Secret Manager
- **HTTPS**: Cloud Run provides automatic HTTPS

### Scaling

- **Concurrency**: Adjust Cloud Run concurrency settings
- **Instances**: Set min/max instance limits
- **Resources**: Configure CPU and memory limits

## Development vs Production

### Development Mode

```bash
# Terminal 1: Flask API
uv run python web_deployment_example_react.py

# Terminal 2: Vite dev server
npm run dev
```

### Production Mode

```bash
# Build and serve from single process
npm run build
uv run python web_deployment_example_react.py
```

### Cloud Deployment

- Multi-stage Docker build
- Gunicorn WSGI server
- Google Cloud Run hosting
- Automatic HTTPS and scaling

## Monitoring Deployment

After deployment, monitor:

- **Cloud Run Metrics**: Request latency, error rates
- **Cloud Build History**: Build success/failure rates
- **Application Logs**: Runtime errors and performance
- **GCS Usage**: Data cache access patterns

The deployment is designed for reliability, performance, and ease of maintenance while providing a modern development experience with TypeScript and React.
