locals {
  service_account_email = "${var.cron_svc_account}@${var.project_id}.iam.gserviceaccount.com"
}

data "google_cloud_run_service" "job_board_ingest_api" {
  name     = var.job_board_ingest_api_service
  location = var.google_compute_location
}

resource "google_cloud_run_service" "career_site_scraper_alpha" {
  name                       = var.service_name
  location                   = var.google_compute_location
  autogenerate_revision_name = true
  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/${var.service_name}:${var.docker_image_tag}"
        env {
          name  = "PROJECT_ID"
          value = var.project_id
        }
        env {
          name  = "GOOGLE_JWT_SERVICE_ACCOUNT"
          value = "api-tasks@${var.project_id}.iam.gserviceaccount.com"
        }
        env {
          name  = "JOB_BOARD_INGEST_API_URL"
          value = data.google_cloud_run_service.job_board_ingest_api.status[0].url
        }
        env {
          name  = "JOB_BATCH_INGEST_QUEUE_NAME"
          value = var.job_batch_ingest_queue_name
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "iam_cron_career_site_scraper_alpha" {
  service  = google_cloud_run_service.career_site_scraper_alpha.name
  location = var.google_compute_location
  role     = "roles/run.invoker"
  member   = "serviceAccount:${local.service_account_email}"
}

resource "google_cloud_scheduler_job" "trigger_career_site_scraper_alpha" {
  # uncomment to only deploy this cron job to prod
  # count            = var.project_id == "ff-app-prod" ? 1 : 0

  lifecycle {
    # Create but do not update this recource.
    # If we don't ignore, pausing the job would cause deployment to fail
    # because paused jobs can't be updated.
    ignore_changes = all
  }

  name             = "trigger-${var.service_name}"
  description      = "Trigger career site scraper alpha"
  schedule         = "0 9 * * *"
  time_zone        = "America/Chicago"
  attempt_deadline = "1799s"
  http_target {
    uri         = google_cloud_run_service.career_site_scraper_alpha.status[0].url
    http_method = "PUT"
    headers = {
      "Content-Type" : "application/json,charset=utf-8"
    }
    oidc_token {
      service_account_email = local.service_account_email
      audience              = google_cloud_run_service.career_site_scraper_alpha.status[0].url
    }
  }
}