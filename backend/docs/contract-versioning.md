# Contract versioning

The initial package version and `contract_version` are `1.0.0`. Requests reject unknown fields (`extra="forbid"`). Every service-to-service model carries the contract version, correlation ID, request ID and timestamp through `ContractMetadata`.

Regenerate checked-in schemas after an agreed contract change:

```powershell
$env:PYTHONPATH="backend/contracts/civicflow_contracts"
python -m civicflow_contracts.schemas.export
```

Additive optional fields may remain compatible within a minor version. Removing/renaming fields, changing meaning, tightening accepted values, or changing requiredness needs an explicit major version. Update consumers and compatibility fixtures together. Members 2 and 3 treat contracts as read-only after freeze; submit proposals to Member 1.
