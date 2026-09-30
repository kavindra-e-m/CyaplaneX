# Low-Level Design (LLD) — CyaplaneX

Modules are partitioned strictly by ownership and communicate through versioned Draft 2020-12 JSON Schema contracts. 

- **Edge Runtime (`edge/`):** Independently testable; performs sensor acquisition, multi-sensor trust checks (range, freshness, stuck, drift, consensus), statistical preprocessing, ML adapter boundary inference, maintenance reasoning, canonical SHA-256 provenance manifest building, device-local HMAC-SHA256 signing, and bounded FIFO offline store-and-forward buffering.
- **Cloud Runtime (`cloud/`):** Validates contracts, verifies cryptographic HMAC signatures, enforces strictly monotonic sequence replay checks, exposes the WSGI REST API (`/health`, `/verification/*`, `/maintenance/*`, `/passport/*`), and persists evidence in the thread-safe store.
- **Dashboard (`dashboard/`):** Client-side operator interface presenting 10 system states and 8 operational action flows without duplicating edge trust or signing decisions.

