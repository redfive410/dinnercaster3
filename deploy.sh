#!/bin/bash
# Deploy dinnercaster3 MCP server to Google Cloud Run

PROJECT_ID=${1:-"your-project-id"}
SERVICE_NAME="dinnercaster3-mcp"
REGION=${2:-"us-central1"}

echo "Deploying $SERVICE_NAME to Cloud Run..."
echo "Project: $PROJECT_ID"
echo "Region: $REGION"

# Build and deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --project $PROJECT_ID \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1

echo "Deployment complete!"
echo "Your MCP server will be available at:"
echo "https://$SERVICE_NAME-xxxxx-xx.a.run.app/mcp"
