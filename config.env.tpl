# GCP project id being used for Cloud Tasks, etc.
PROJECT_ID=ff-app-dev

# this is the service account that Google Cloud Tasks uses to sign JWTs for requests to our API
GOOGLE_JWT_SERVICE_ACCOUNT=api-tasks@ff-app-dev.iam.gserviceaccount.com

# URL used to access the job board ingest API directly, externally
# (used by Cloud Tasks service for  "url" parameter for incoming tasks)
JOB_BOARD_INGEST_API_URL=https://your-dynamic-ngrok-url.ngrok.io

# Cloud Tasks queue name
JOB_BATCH_INGEST_QUEUE_NAME=job-batch-ingest-queue
