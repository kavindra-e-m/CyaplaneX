# CyaplaneX AWS Cloud Deployment Runbook

**Project:** CyaplaneX (Tata Technologies InnoVent 2026)  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring  
**Document Classification:** Cloud Architecture & Deployment Runbook  
**LIVE AWS DEPLOYMENT = PENDING** (Target Cloud Architecture Specified & Review Complete; Live Deployment Pending AWS Credentials and Budget Provisioning)

---

## 1. Architectural Scope & Operating Paradigm

CyaplaneX is architected with a strict separation between **Edge Intelligence** and **Cloud Governance**:

$$\begin{aligned}
\text{Edge Host (Orchestrator, Trust, ML, HMAC Signer)} &\longrightarrow \text{Store-and-Forward Offline Queue} \\
&\longrightarrow \text{AWS IoT Core (MQTT over mTLS)} \\
&\longrightarrow \begin{cases}
\textbf{Amazon Timestream} & \text{(High-frequency time-series telemetry)} \\
\textbf{Amazon S3 + KMS} & \text{(Cryptographic manifests \& audit archive)} \\
\textbf{Amazon DynamoDB} & \text{(Asset digital passport \& component lifecycle)} \\
\textbf{CloudWatch Logs} & \text{(Tamper alarms \& verification audit)}
\end{cases}
\end{aligned}$$

> [!IMPORTANT]
> **LOCAL INDEPENDENCE & ZERO CLOUD DEPENDENCIES:**
> All 68 automated tests, the production ML model, cryptographic provenance, tamper detection, offline buffering, and the interactive MRO dashboard execute **entirely offline on the local host**.
> Live AWS deployment has **NOT** been executed. No active AWS resources exist. No cloud metrics or costs are fabricated.

---

## 2. Target AWS Services Architecture

| Service | Architectural Role | Security & Governance Control |
| :--- | :--- | :--- |
| **AWS IoT Core** | Managed MQTT Broker connecting Edge Gateways to AWS cloud | Mutual TLS (X.509 client certificate), strict per-thing topic authorization (`cyaplanex/devices/${iot:Connection.Thing.ThingName}/*`) |
| **AWS IoT Greengrass v2** | Edge container runtime on industrial edge gateways | Orchestrates edge container lifecycle, local IPC, and automatic OTA deployment of signed ML model updates |
| **Amazon S3** | Append-only repository for diagnostic manifests and closure records | Bucket versioning enabled, Public Access Block enforced (all 4 flags), Customer-Managed KMS envelope encryption, forced TLS (`aws:SecureTransport = false`) |
| **Amazon Timestream** | Serverless time-series database for telemetry streams | Encrypted at rest via KMS CMK, configurable retention (e.g., 24h memory store, 365 days magnetic store) |
| **Amazon DynamoDB** | Fast single-digit millisecond key-value store for Digital Passport records | Partition key: `component_id`, Sort key: `event_timestamp`, point-in-time recovery (PITR) enabled, KMS encrypted |
| **AWS KMS** | Centralized cryptographic key management | Dedicated Customer-Managed Key (CMK) with automatic 365-day rotation and strict least-privilege key policy |
| **AWS IAM** | Identity and Access Management | Role-based access control (RBAC), zero hardcoded credentials, least-privilege service roles for IoT Core rules |
| **Amazon CloudWatch** | Centralized logging, metric alarms, and audit alerts | Real-time alarms on `PROVENANCE_VIOLATION` and `REPLAY_ATTACK` events routed to Amazon SNS |

---

## 3. Deployment Prerequisites

Before deploying the Terraform infrastructure:

1. **AWS CLI v2:** Installed and configured with administrator permissions:
   ```bash
   aws sts get-caller-identity
   ```
2. **Terraform CLI:** Version `1.5.0` or later:
   ```bash
   terraform version
   ```
3. **Dedicated AWS Account / Isolation:** Deployment target should be an isolated sandbox or staging account (e.g., `cyaplanex-staging-account`).
4. **Environment Variables:** Set AWS region (default: `ap-south-1` or `us-east-1`):
   ```bash
   export AWS_DEFAULT_REGION="ap-south-1"
   ```

---

## 4. Step-by-Step Provisioning via Terraform

The Terraform infrastructure definitions reside in [`cloud/infrastructure/terraform/`](file:///d:/CyplaneX/cloud/infrastructure/terraform/).

### Step 4.1: Initialize Provider Plugins
```bash
cd cloud/infrastructure/terraform
terraform init
```

### Step 4.2: Infrastructure Validation & Dry-Run Planning
```bash
terraform plan -var="environment=staging" -out=tfplan.binary
```
Review the execution plan:
- 1 KMS Key + Alias
- 1 S3 Bucket + Versioning + Encryption + Public Access Block + TLS Policy
- 1 Timestream Database + Table
- 1 IoT Thing + IoT Policy

### Step 4.3: Apply Infrastructure Provisioning
```bash
terraform apply tfplan.binary
```

### Step 4.4: Record Provisioned Outputs
```bash
terraform output
```
Key outputs to document:
- `kms_key_arn`
- `s3_evidence_bucket_name`
- `timestream_database_name`
- `timestream_table_name`
- `iot_device_policy_name`

---

## 5. AWS IoT Core Device Provisioning

Each physical edge device (Raspberry Pi / industrial PC) must be enrolled with its own X.509 certificate:

```bash
# 1. Create Thing Certificate and Keypair
aws iot create-keys-and-certificate \
    --set-as-active \
    --certificate-pem-outfile "certs/device.cert.pem" \
    --public-key-outfile "certs/device.public.key" \
    --private-key-outfile "certs/device.private.key" \
    --output json > certs_meta.json

CERT_ARN=$(jq -r '.certificateArn' certs_meta.json)

# 2. Attach Least-Privilege IoT Policy
aws iot attach-policy \
    --policy-name "cyaplanex-device-policy-staging" \
    --target "$CERT_ARN"

# 3. Attach Certificate to IoT Thing
aws iot attach-thing-principal \
    --thing-name "cyaplanex-edge-dev-01" \
    --principal "$CERT_ARN"

# 4. Fetch AWS IoT Endpoint
aws iot describe-endpoint --endpoint-type iot:Data-ATS
```

---

## 6. AWS IoT Greengrass v2 Edge Deployment

To deploy CyaplaneX as an edge container runtime on a physical Raspberry Pi:

1. **Install Greengrass Core Software:**
   ```bash
   sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE \
     -jar ./GreengrassInstaller/lib/Greengrass.jar \
     --aws-region ap-south-1 \
     --thing-name cyaplanex-edge-dev-01 \
     --thing-group-name cyaplanex-edge-gateways \
     --component-default-user ggc_user:ggc_group \
     --provision true \
     --setup-system-service true
   ```
2. **Deploy CyaplaneX Edge Recipe (`cyaplanex.edge.orchestrator`):**
   - Package `edge/` and ML artifacts into an immutable zip archive.
   - Publish recipe to AWS IoT Greengrass Component Repository.
   - Greengrass automatically starts [`edge/main.py`](file:///d:/CyplaneX/edge/main.py) as an isolated systemd daemon.

---

## 7. Amazon S3 & DynamoDB Evidence Architecture

### S3 Evidence Storage Structure
Cryptographic manifests and signed closure records are stored immutably with prefix paths:
```text
s3://cyaplanex-evidence-staging-<account_id>/
  └── assets/
      └── airc-cf34-01/
          ├── manifests/
          │   ├── 2026/10/02/manifest_evt-diag-101.json
          │   └── 2026/10/02/manifest_evt-diag-102.json
          └── closures/
              └── 2026/10/02/closure_rec-mro-001.json
```

### DynamoDB Digital Passport Table Specification (Target)
```bash
aws dynamodb create-table \
    --table-name cyaplanex_digital_passport_staging \
    --attribute-definitions \
        AttributeName=component_id,AttributeType=S \
        AttributeName=record_timestamp,AttributeType=S \
    --key-schema \
        AttributeName=component_id,KeyType=HASH \
        AttributeName=record_timestamp,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --sse-specification Enabled=true,SSEType=KMS,KMSMasterKeyId=alias/cyaplanex-cmk-staging
```

---

## 8. Logging, Monitoring & Security Alarms

### CloudWatch Log Group
Configure IoT Topic Rules to route verification events to CloudWatch Logs:
- `/aws/iot/cyaplanex/verification_events`
- Filter pattern for security violations:
  ```text
  { $.verification_status = "PROVENANCE_VIOLATION" || $.verification_status = "REPLAY_REJECTED" }
  ```

### Real-Time SNS Alarm
When the metric filter detects $\ge 1$ violation within 1 minute:
- CloudWatch triggers an alarm state.
- Amazon SNS notifies the Flight Line Safety Office & MRO Chief Engineer via SMS/email.

---

## 9. Tear-Down & Cost Control Procedure

When cloud verification testing is concluded, deprovision all cloud infrastructure to prevent ongoing AWS charges:

```bash
cd cloud/infrastructure/terraform

# 1. Empty S3 Bucket (versioning must be suspended or all versions deleted)
python -c "
import boto3
s3 = boto3.resource('s3')
bucket = s3.Bucket('cyaplanex-evidence-staging-<account_id>')
bucket.object_versions.delete()
"

# 2. Destroy all provisioned Terraform resources
terraform destroy -var="environment=staging" -auto-approve
```

---

## 10. Status Summary

- **Local Demonstrator Status:** FULLY OPERATIONAL & VERIFIED (Zero Cloud Costs)
- **Terraform Configuration Status:** REVIEWED, SECURITY-HARDENED, & READY
- **Live AWS Cloud Status:** **PENDING** (Zero active billable resources)
