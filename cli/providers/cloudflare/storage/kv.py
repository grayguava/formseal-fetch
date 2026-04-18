# Cloudflare KV storage

import json
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

from cli.ui import fail


def _get(url, token):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        fail(f"HTTP {e.code}: {e.read().decode()}")


def _get_raw(url, token):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8").strip()
    except urllib.error.HTTPError as e:
        fail(f"HTTP {e.code}: {e.read().decode()}")


def _load_seen(output_path) -> set:
    p = Path(output_path)
    if not p.exists():
        return set()
    return {line.strip() for line in p.read_text(encoding="utf-8").splitlines() if line.strip()}


def fetch(namespace, token):
    """Fetch all values from a KV namespace. Returns dict[str, bytes] with single key 'ciphertexts'."""
    account_id = _get_account_id(token)
    base = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace}"

    all_keys = []
    cursor = None

    while True:
        url = f"{base}/keys" + (f"?cursor={cursor}" if cursor else "")
        data = _get(url, token)
        if not data.get("success"):
            fail(f"API error: {data.get('errors')}")
        all_keys.extend(k["name"] for k in data.get("result", []))
        cursor = data.get("result_info", {}).get("cursor")
        if not cursor:
            break

    if not all_keys:
        return {"ciphertexts": b""}

    result = {}
    for key in all_keys:
        value = _get_raw(f"{base}/values/{urllib.parse.quote(key, safe='')}", token)
        if value:
            result[key] = value.encode("utf-8")

    return result


def _get_account_id(token):
    url = "https://api.cloudflare.com/client/v4/accounts"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())

    if not data.get("success"):
        fail(f"Auth failed: {data.get('errors')}")

    accounts = data.get("result", [])
    if not accounts:
        fail("No accounts found. Token needs 'Account Settings: Read' scope.")

    return accounts[0]["id"]