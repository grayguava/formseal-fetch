# FormSeal Admin Workflow

This directory contains all tools required to administer FormSeal submissions.

---

## Recommended workflow

1. Run the export tool to fetch encrypted submissions
2. Run the decrypt tool to process and inspect data locally
3. Run the cleanup tool to remove processed exports

---

## Trust boundaries

- Backend: encrypted storage only
- Admin machine: decryption and inspection
- Private keys never leave the admin environment

---

## Entry point

For full automation, use the top-level `sync.py` orchestrator.
