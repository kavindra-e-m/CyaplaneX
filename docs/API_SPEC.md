# API Specification

## Health
`GET /health` returns `{ "status": "ok", "service": "aerotrust-verification-api" }` in the current scaffold.

## Future endpoints
- `POST /verification/events`: submit a signed maintenance event.
- `GET /verification/{report_id}`: return signature, replay, model, and chain status.
- `GET /maintenance/{asset_id}`: list maintenance history.
- `GET /passport/{component_id}`: return the component maintenance digital passport.

TODO: Select a web framework, authentication model, error envelope, pagination, and versioning policy.
