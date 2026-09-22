# Low-Level Design

Modules are split by ownership and communicate through shared JSON contracts. Edge modules should remain independently testable and must not import cloud SDKs directly. Cloud adapters should validate contracts before persistence or verification. Dashboard code consumes API-shaped records and should not implement signing or trust decisions.

The current executable reference includes range/stuck checks, deterministic canonical hashing, a health value object, replay sequence checking, and a framework-neutral verification API smoke function. Other files are typed placeholders.
