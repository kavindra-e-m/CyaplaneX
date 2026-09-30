# CyaplaneX Target AWS Infrastructure - Main Configuration
# Project: CyaplaneX (Tata Technologies InnoVent 2026)
# Category: Edge AI for Predictive Maintenance & Aircraft Health Monitoring
#
# STATUS: TARGET ARCHITECTURE SPECIFICATION ONLY
# LIVE AWS DEPLOYMENT IS PENDING AND NOT DEPLOYED.
# Local verification and storage remain functional independently of cloud connectivity.

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "CyaplaneX"
      ManagedBy   = "Terraform"
      Environment = var.environment
      Competition = "Tata-Technologies-InnoVent-2026"
    }
  }
}

# ------------------------------------------------------------------------------
# 1. AWS Key Management Service (KMS) - Envelope Encryption
# ------------------------------------------------------------------------------

resource "aws_kms_key" "cyaplanex_key" {
  description             = "CyaplaneX CMK for S3 evidence bucket and Timestream encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "EnableRootPermissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "AllowIoTAndS3ServiceAccess"
        Effect = "Allow"
        Principal = {
          Service = [
            "s3.amazonaws.com",
            "timestream.amazonaws.com",
            "iot.amazonaws.com"
          ]
        }
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:DescribeKey"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_kms_alias" "cyaplanex_key_alias" {
  name          = "alias/${var.project_name}-cmk-${var.environment}"
  target_key_id = aws_kms_key.cyaplanex_key.key_id
}

# ------------------------------------------------------------------------------
# 2. Amazon S3 - Cryptographic Evidence & Passport Archive
# ------------------------------------------------------------------------------

resource "aws_s3_bucket" "evidence_store" {
  bucket_prefix = "${var.project_name}-evidence-${var.environment}-"
  force_destroy = false
}

resource "aws_s3_bucket_versioning" "evidence_store_versioning" {
  bucket = aws_s3_bucket.evidence_store.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "evidence_store_encryption" {
  bucket = aws_s3_bucket.evidence_store.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.cyaplanex_key.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "evidence_store_pab" {
  bucket = aws_s3_bucket.evidence_store.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "enforce_tls" {
  bucket = aws_s3_bucket.evidence_store.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "EnforceTLSRequestsOnly"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          aws_s3_bucket.evidence_store.arn,
          "${aws_s3_bucket.evidence_store.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })
}

# ------------------------------------------------------------------------------
# 3. Amazon Timestream - Time-Series Telemetry Ingestion
# ------------------------------------------------------------------------------

resource "aws_timestreamwrite_database" "telemetry_db" {
  database_name = "${var.project_name}_telemetry_${var.environment}"
  kms_key_id    = aws_kms_key.cyaplanex_key.arn
}

resource "aws_timestreamwrite_table" "telemetry_table" {
  database_name = aws_timestreamwrite_database.telemetry_db.database_name
  table_name    = "sensor_telemetry"

  retention_properties {
    magnetic_store_retention_period_in_days = var.retention_magnetic_store_days
    memory_store_retention_period_in_hours  = var.retention_memory_store_hours
  }

  magnetic_store_write_properties {
    enable_magnetic_store_writes = true
  }
}

# ------------------------------------------------------------------------------
# 4. AWS IoT Core - Device Registry & Least-Privilege Policy
# ------------------------------------------------------------------------------

resource "aws_iot_thing" "edge_device" {
  name = "${var.project_name}-edge-dev-01"

  attributes = {
    DeviceClass = "EdgeAI-PredictiveMaintenance"
    Platform    = "RaspberryPi-ESP32"
  }
}

resource "aws_iot_policy" "edge_device_policy" {
  name = "${var.project_name}-device-policy-${var.environment}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["iot:Connect"]
        Resource = "arn:aws:iot:${var.aws_region}:${data.aws_caller_identity.current.account_id}:client/$${iot:Connection.Thing.ThingName}"
      },
      {
        Effect   = "Allow"
        Action   = ["iot:Publish"]
        Resource = [
          "arn:aws:iot:${var.aws_region}:${data.aws_caller_identity.current.account_id}:topic/${var.project_name}/devices/$${iot:Connection.Thing.ThingName}/telemetry",
          "arn:aws:iot:${var.aws_region}:${data.aws_caller_identity.current.account_id}:topic/${var.project_name}/devices/$${iot:Connection.Thing.ThingName}/events"
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["iot:Subscribe"]
        Resource = [
          "arn:aws:iot:${var.aws_region}:${data.aws_caller_identity.current.account_id}:topicfilter/${var.project_name}/devices/$${iot:Connection.Thing.ThingName}/commands"
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["iot:Receive"]
        Resource = [
          "arn:aws:iot:${var.aws_region}:${data.aws_caller_identity.current.account_id}:topic/${var.project_name}/devices/$${iot:Connection.Thing.ThingName}/commands"
        ]
      }
    ]
  })
}

# ------------------------------------------------------------------------------
# 5. Caller Identity Data Source
# ------------------------------------------------------------------------------

data "aws_caller_identity" "current" {}
