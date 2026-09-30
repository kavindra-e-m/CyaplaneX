# CyaplaneX Target AWS Infrastructure - Outputs
# Project: CyaplaneX (Tata Technologies InnoVent 2026)
# Status: Target Infrastructure Specification (Live Deployment Pending)

output "kms_key_arn" {
  description = "ARN of the Customer Managed Key (CMK) for CyaplaneX envelope encryption"
  value       = aws_kms_key.cyaplanex_key.arn
}

output "s3_evidence_bucket_name" {
  description = "Name of the secure S3 evidence bucket"
  value       = aws_s3_bucket.evidence_store.id
}

output "s3_evidence_bucket_arn" {
  description = "ARN of the secure S3 evidence bucket"
  value       = aws_s3_bucket.evidence_store.arn
}

output "timestream_database_name" {
  description = "Name of the Timestream telemetry database"
  value       = aws_timestreamwrite_database.telemetry_db.database_name
}

output "timestream_table_name" {
  description = "Name of the Timestream telemetry table"
  value       = aws_timestreamwrite_table.telemetry_table.table_name
}

output "iot_thing_name" {
  description = "Name of the registered IoT Core thing"
  value       = aws_iot_thing.edge_device.name
}

output "deployment_status" {
  description = "Current deployment verification status"
  value       = "TARGET_ARCHITECTURE_DEFINED_DEPLOYMENT_PENDING"
}
