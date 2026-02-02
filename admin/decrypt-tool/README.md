
---
# Decrypt Tool

This tool decrypts encrypted FormSeal exports **locally** and splits them into
structured data files for inspection.

All cryptographic operations occur **offline** on the administrator’s machine.

---

## What this tool does

- Reads encrypted `.jsonl` export files
- Decrypts each submission using an X25519 private key
- Splits data into:
  - inbox entries
  - message metadata
  - export metadata
- Deduplicates previously processed messages

---

## Requirements

- Python 3.10+ recommended
- `PyNaCl` installed
- Encrypted export files from the export tool
- Administrator X25519 private key

---

## Key material

This tool requires a `keys.json` file containing the administrator’s keypair.

⚠️ **This file must never be committed or shared.**

Example structure:

```json
{
  "x25519_public": "BASE64URL_PUBLIC_KEY",
  "x25519_private": "BASE64URL_PRIVATE_KEY"
}
```

The private key must match the public key configured in FormSeal.

---
## Configuration

Edit `config.json` to point to:

- the directory containing encrypted exports
- the directory where decrypted data should be written

---

## Usage

From this directory:

`python decrypt-and-split.py`

The tool is idempotent:

- previously processed messages are skipped
- safe to re-run after new exports

---

## Output files

Decrypted data is written as newline-delimited JSON:

- `inbox.jsonl` — human-facing message content
- `message-meta.jsonl` — internal metadata
- `export-meta.jsonl` — export-level records

These files are plaintext. Protect them accordingly.