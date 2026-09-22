# Contributing

## Branching
```text
main
  ^
develop
  ^
feature/<member>/<module>
```

Examples: `feature/kavindra/provenance`, `feature/dhakshatha/sensors`, `feature/monhit/fault-classifier`, `feature/hari/iot-ingestion`, `feature/ashwarya/dashboard`.

## Rules
- No direct push to `main`.
- Normal work goes through a pull request.
- Pull the latest `develop` before starting.
- Rebase the feature branch before opening a pull request.
- Keep commits small and meaningful.
- Include tests and validation notes in every pull request.
- Security or interface changes require architecture review.

Keep ownership boundaries modular and avoid inventing production behavior in scaffold modules.
