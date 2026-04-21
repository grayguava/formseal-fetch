# Supabase storage

import json
import re
import urllib.request
import urllib.error

from cli.ui import fail

# Columns to always skip when auto-detecting ciphertext column
_SKIP_COLS = {"id", "created_at", "updated_at", "inserted_at"}

# Looks like formseal ciphertext: formseal.<base64url>
_FORMSEAL_RE = re.compile(r'^formseal\.[A-Za-z0-9+/=_\-]+$')


def _detect_ciphertext_col(row: dict) -> str | None:
    """Return the first column that looks like a ciphertext payload."""
    for key, val in row.items():
        if key in _SKIP_COLS:
            continue
        if isinstance(val, str) and _FORMSEAL_RE.match(val):
            return key
    return None


def _get(url, headers):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        fail(f"HTTP {e.code}: {e.read().decode()}")
    except Exception as e:
        fail(f"Fetch failed: {e}")


def fetch(ref, token, table):
    """Fetch all rows from a table. Returns dict[str, bytes]."""
    base_url = f"https://{ref}.supabase.co/rest/v1/{table}"

    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": token,
        "Content-Type": "application/json"
    }

    # --- Auto-detect ciphertext column ---
    probe = _get(f"{base_url}?limit=1&select=*", headers)
    if not probe:
        return {"ciphertexts": b""}

    col = _detect_ciphertext_col(probe[0])
    if not col:
        fail(f"Could not detect ciphertext column in table '{table}'. "
             f"Columns found: {list(probe[0].keys())}")

    # --- Paginated fetch ---
    result = {}
    offset = 0
    limit = 1000

    while True:
        url = f"{base_url}?offset={offset}&limit={limit}&select=id,{col}"
        data = _get(url, headers)

        if not data:
            break

        for row in data:
            row_id = row.get("id", f"row_{offset}")
            row_data = row.get(col, "")
            if row_data:
                result[row_id] = row_data.encode("utf-8")

        if len(data) < limit:
            break
        offset += limit

    if not result:
        return {"ciphertexts": b""}

    return result