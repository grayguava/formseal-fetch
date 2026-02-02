# Export Tool

This tool is used to export **encrypted FormSeal submissions** from a deployed
FormSeal backend.

It performs **no decryption** and handles **encrypted blobs only**.

---

## What this tool does

- Authenticates to the FormSeal export API
- Requests a one-time export token
- Downloads encrypted submissions as `.jsonl` files
- Writes export files to a local directory

The backend remains blind to message contents.

---

## Requirements

- A deployed FormSeal instance with export APIs enabled
- A valid administrator export token
- Python 3.10+ recommended

---

This tool assumes the following FormSeal endpoints exist:

- POST /api/export-request
- GET  /api/export/{token}

These endpoints are implemented and documented in the FormSeal repository.

---

## Authentication

This tool requires an environment variable:

 - **FORMSEAL_ADMIN_TOKEN**
 
This token must be a **high-entropy secret** configured on the FormSeal backend.

### Examples

**Windows (PowerShell):**
```powershell
setx FORMSEAL_ADMIN_TOKEN "your-secret-here"
```

**Linux/macOS:**
```
export FORMSEAL_ADMIN_TOKEN="your-secret-here"
```

---
## Configuration

Edit `config.json` before running:

- `base_url` must point to your FormSeal deployment
- Other fields should not be changed unless you know what you are doing

---

## Usage

From this directory:

```python
python fetch-export.py
```
or
```python
py fetch-export.py
```

Successful runs will write encrypted export files to the configured `exports/`  
directory.

---

## Important notes

- Exported files contain **encrypted data only**
- These files are intended as input to the decrypt tool
- Do not edit exported files manually