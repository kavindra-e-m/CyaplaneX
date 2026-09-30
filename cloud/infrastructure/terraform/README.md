# Target AWS Cloud Infrastructure (Terraform)

**Project:** CyaplaneX (Tata Technologies InnoVent 2026)  
**Status:** **TARGET ARCHITECTURE REVIEWED & SPECIFIED; LIVE DEPLOYMENT PENDING**  

---

## 1. Architectural Overview & Split

The CyaplaneX cloud tier is architecturally divided into two states:

1. **Implemented & Verified Locally (Zero Cloud Dependencies):**
   - Device-local evidence store ([`cloud/storage/evidence_store.py`](file:///d:/CyplaneX/cloud/storage/evidence_store.py))
   - Independent cryptographic verifier ([`cloud/verification/verifier.py`](file:///d:/CyplaneX/cloud/verification/verifier.py))
   - REST API gateway ([`cloud/api/app.py`](file:///d:/CyplaneX/cloud/api/app.py))
   - Store-and-forward sync coordinator ([`edge/connectivity/sync.py`](file:///d:/CyplaneX/edge/connectivity/sync.py))

2. **Target AWS Cloud Services (Deployment Pending Account Provisioning):**
   - **AWS IoT Core:** Secure MQTT broker with mutual TLS (X.509 client certificates) and strict topic-level least-privilege authorization.
   - **AWS IoT Greengrass v2:** Edge container runtime for edge-orchestrator deployment on industrial edge gateways.
   - **Amazon S3:** Append-only evidence repository for cryptographic manifests and digital passport lifecycle closures.
   - **Amazon Timestream:** Serverless time-series database optimized for high-throughput sensor telemetry.
   - **AWS KMS:** Customer-managed keys (CMK) providing envelope encryption for all at-rest evidence and telemetry records.

> **CRITICAL FACTUAL PRINCIPLE:**  
> Live AWS deployment has **NOT** been performed. No AWS resources are currently active.  
> The local demonstrator runs entirely offline without simulated or fabricated cloud screens.

---

## 2. Infrastructure Security Controls Review

The Terraform definitions in this directory satisfy the following security controls:

- **Least Privilege IoT Policies:** The IoT Core policy (`aws_iot_policy.edge_device_policy`) restricts publishing strictly to `cyaplanex/devices/${iot:Connection.Thing.ThingName}/*`. Cross-device topic poisoning is denied by default.
- **Envelope Encryption (KMS):** A dedicated Customer Managed Key (`aws_kms_key.cyaplanex_key`) with annual automatic key rotation encrypts both the S3 evidence bucket and Timestream database.
- **S3 Hardening:**
  - All four Public Access Block settings are enabled (`block_public_acls = true`, etc.).
  - S3 Bucket Versioning is enforced to prevent accidental or malicious record deletion.
  - Enforced TLS: A bucket policy explicitly denies non-HTTPS requests (`aws:SecureTransport = false`).
- **Zero Hardcoded Credentials:** No access keys, secret keys, or passwords are embedded in Terraform code. Authentication relies on AWS IAM AssumeRole or standard CLI credential chains.

---

## 3. Provisioning Instructions (When Credentials Are Provided)

When dedicated AWS account credentials and budget approval are provisioned:

```bash
# 1. Initialize Terraform provider plugins
terraform init

# 2. Review proposed changes
terraform plan -var="environment=staging"

# 3. Apply infrastructure provisioning
terraform apply -var="environment=staging"
```
