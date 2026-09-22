# High-Level Design

## Scope
AeroTrust AI is a trusted closed-loop Edge AI demonstrator. The architecture separates sensor acquisition, sensor trust, edge intelligence, provenance, connectivity, cloud verification, and MRO workflow.

## Data path
Sensors -> trust checks -> preprocessing/fusion -> model adapters -> maintenance reasoning -> local provenance -> offline queue -> AWS IoT -> S3/Timestream/KMS -> verification API -> dashboard -> repair retest -> closure record.

## Security posture
The edge signs locally and remains functional without AWS availability. Cloud KMS is reserved for governance and supported cloud cryptographic workflows. Sequence, timestamp, nonce, sensor-window hash, model metadata, and previous-record hash are evidence fields. This scaffold is tamper-evident and cryptographically verifiable in intent; production cryptography and key custody remain TODO.

## AWS extension points
Greengrass, IoT Core, S3, Timestream, KMS are the core path. DynamoDB, Lambda, API Gateway, EventBridge, SNS, SiteWise, Grafana, and TwinMaker are future integrations.
