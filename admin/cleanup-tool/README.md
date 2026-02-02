
---
# Cleanup tool

This tool removes encrypted export files that have already been successfully
processed by the decrypt tool.

It exists purely for **operational hygiene**.

---

## What this tool does

- Scans encrypted export files
- Compares them against processed message metadata
- Deletes exports that contain no new messages

---

## Safety model

By default, this tool runs in **dry-run mode**.

In dry-run mode:
- No files are deleted
- The tool only reports what *would* be removed

This prevents accidental data loss.

---

## Configuration

Edit `config.json` carefully:

- `export_dir` must point to encrypted exports
- `data_dir` must contain message metadata
- `dry_run` must be explicitly set to `false` to enable deletion

---

## Usage

From this directory:

```python
py cleanup-exports.py
```
or
```python
python cleanup-exports.py
```

Always run in **dry-run mode at least once** before enabling deletion.

---

## Important notes

- This tool does not contact the backend
- This tool does not decrypt data
- This tool assumes the decrypt tool has already run successfully

Deletion is permanent. Use responsibly.