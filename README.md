# FormSeal Sync

**FormSeal Sync** provides **local, operator-run administrative tooling** for
exporting, decrypting, and inspecting submissions collected by a FormSeal
deployment.

This repository is **not part of the public submission pipeline**.
It exists solely to support **trusted operators** managing FormSeal data
after ingestion.

---

## What this repository is

- Local administrative tooling
- Operator-controlled and scriptable
- Offline-first for decryption and inspection
- Designed to work with an existing FormSeal deployment

FormSeal Sync assumes you already run or understand FormSeal.

---

## What this repository is NOT

- ❌ A backend service
- ❌ A browser-based admin interface
- ❌ A dashboard or hosted tool
- ❌ Part of the ingestion or encryption path
- ❌ Suitable for untrusted users

No plaintext ever touches the FormSeal backend.
All decryption happens locally.

---

## High-level workflow

The intended operator workflow is:

1. **Export** encrypted submissions from FormSeal using authenticated APIs  
2. **Decrypt and split** submissions locally using administrator-held keys  
3. **Inspect or process** plaintext data offline  
4. **Clean up** processed export files as needed  

Each step is handled by a dedicated tool.

## Backend API dependency

FormSeal Sync relies on the export APIs provided by a deployed
FormSeal instance.

API definitions, authentication logic, and deployment configuration
live exclusively in the FormSeal repository:

https://github.com/grayguava/formseal

---

## Repository structure

```
admin/  
├── sync.py # Orchestrator (recommended entrypoint)  
│  
├── export-tool/ # Fetch encrypted exports from FormSeal  
├── decrypt-tool/ # Offline decryption and inbox splitting  
└── cleanup-tool/ # Optional cleanup of processed exports
```


This script `sync.py` orchestrates the full export → decrypt → cleanup workflow.

Individual tools can also be run manually if finer control is required.

---

## Security model (important)

- The FormSeal backend stores **encrypted data only**
- Export APIs stream encrypted blobs without decryption
- Private keys exist **only on the operator’s local machine**
- Secrets are supplied via environment variables
- No secrets are committed to this repository

Operators are responsible for:
- key custody
- local system security
- protecting decrypted data at rest

---

## Relationship to FormSeal

- **FormSeal (core)**  
  Handles browser-side encryption, ingestion, and blind storage  

- **FormSeal Sync (this repository)**  
  Handles export, decryption, and administrative inspection  

FormSeal core repository:  
https://github.com/grayguava/formseal

---

## Requirements

- Python 3.10+ recommended
- A deployed FormSeal instance with export APIs enabled
- Administrator credentials and private keys

---

## Status

This repository is **actively used** as the reference implementation for
FormSeal administrative workflows.

The internal structure is intentionally conservative to preserve
auditability and trust boundaries.

---

## License

MIT License.
