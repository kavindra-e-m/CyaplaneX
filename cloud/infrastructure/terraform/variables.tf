# CyaplaneX Target AWS Infrastructure - Variables
# Project: CyaplaneX (Tata Technologies InnoVent 2026)
# Status: Target Infrastructure Specification (Live Deployment Pending)

variable "aws_region" {
  description = "Target AWS region for CyaplaneX cloud deployment"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Target deployment environment (e.g. dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Canonical project identifier"
  type        = string
  default     = "cyaplanex"
}

variable "retention_memory_store_hours" {
  description = "Retention period for Timestream in-memory store in hours"
  type        = number
  default     = 24
}

variable "retention_magnetic_store_days" {
  description = "Retention period for Timestream magnetic store in days"
  type        = number
  default     = 365
}
