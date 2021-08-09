terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.70.0"
    }
  }

  backend "gcs" {
    # set via -backend-config command line arg
    # bucket = "${var.project_id}-tfstate"
  }
}

provider "google" {
  project = var.project_id
  region  = var.google_compute_location
}
