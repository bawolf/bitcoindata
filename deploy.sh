#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration Check ---
# This script uses environment variables for configuration.
# Please ensure you have an .envrc file with the following variables set,
# then run 'direnv allow' before executing this script.

# Check for required environment variables
if [ -z "$PROJECT_ID" ]; then
    echo "❌ ERROR: PROJECT_ID environment variable is not set."
    echo "Please define it in your .envrc file."
    exit 1
fi

if [ -z "$WEB_SERVICE_NAME" ]; then
    echo "ℹ️  WEB_SERVICE_NAME environment variable is not set."
    echo "Using default value 'bitcoin-ath-dashboard'."
    SERVICE_NAME="bitcoin-ath-dashboard"
else
    SERVICE_NAME="$WEB_SERVICE_NAME"
fi

if [ -z "$REGION" ]; then
    echo "ℹ️  REGION environment variable is not set."
    echo "Using default value 'us-central1'."
    REGION="us-central1"
fi

if [ -z "$GCS_BUCKET_NAME" ]; then
    echo "❌ ERROR: GCS_BUCKET_NAME environment variable is not set."
    echo "Please define it in your .envrc file."
    exit 1
fi

# --- Deployment Steps ---

echo "🚀 Starting deployment to Google Cloud Run..."
echo "----------------------------------------"
echo "Project: $PROJECT_ID"
echo "Service: $SERVICE_NAME"
echo "Region:  $REGION"
echo "Bucket:  $GCS_BUCKET_NAME"
echo "----------------------------------------"

# 1. Build the container image using Google Cloud Build.
# This command builds the image from the Dockerfile in the current directory
# and tags it in the Google Container Registry (gcr.io).
# The multi-stage build will:
# - Stage 1: Build React/TypeScript frontend with Node.js
# - Stage 2: Copy built frontend and set up Python backend
echo "📦 Building container image (React/TypeScript + Python)..."
gcloud builds submit --tag "gcr.io/$PROJECT_ID/$SERVICE_NAME" --quiet

# 2. Deploy the new container image to Cloud Run.
# This command updates the service with the new image.
# --platform managed: Specifies the fully managed Cloud Run platform.
# --allow-unauthenticated: Allows public access to the service (important for a web dashboard).
# --set-env-vars: Sets the GCS_BUCKET_NAME environment variable that the app needs.
echo "🚢 Deploying to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
  --image "gcr.io/$PROJECT_ID/$SERVICE_NAME" \
  --platform managed \
  --region "$REGION" \
  --allow-unauthenticated \
  --set-env-vars="GCS_BUCKET_NAME=$GCS_BUCKET_NAME" \
  --quiet

echo "----------------------------------------"
echo "✅ Deployment complete!"
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --platform managed --region "$REGION" --format="value(status.url)")
echo "Your service is available at: $SERVICE_URL"
echo "----------------------------------------" 