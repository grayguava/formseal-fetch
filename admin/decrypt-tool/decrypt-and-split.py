import json
import base64
from pathlib import Path
from datetime import datetime, timezone

from nacl.public import PrivateKey, SealedBox


# -----------------------
# HELPERS
# -----------------------
def b64url_to_bytes(s: str) -> bytes:
    s = s.replace("-", "+").replace("_", "/")
    s += "=" * (-len(s) % 4)
    return base64.b64decode(s)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_seen_keys(path: Path) -> set[str]:
    keys = set()
    if not path.exists():
        return keys

    with path.open("r", encoding="utf-8") as f:
        buffer = ""
        for raw_line in f:
            buffer += raw_line.rstrip()
            try:
                obj = json.loads(buffer)
                buffer = ""
            except json.JSONDecodeError:
                buffer += "\n"
                continue

            if "key" in obj:
                keys.add(obj["key"])

    return keys


def load_seen_export_ids(path: Path) -> set[str]:
    ids = set()
    if not path.exists():
        return ids

    with path.open("r", encoding="utf-8") as f:
        buffer = ""
        for raw_line in f:
            buffer += raw_line.rstrip()
            try:
                obj = json.loads(buffer)
                buffer = ""
            except json.JSONDecodeError:
                buffer += "\n"
                continue

            if "export_id" in obj:
                ids.add(obj["export_id"])

    return ids


def count_jsonl_entries(path: Path) -> int:
    if not path.exists():
        return 0

    count = 0
    with path.open("r", encoding="utf-8") as f:
        buffer = ""
        for raw_line in f:
            buffer += raw_line.rstrip()
            try:
                json.loads(buffer)
                count += 1
                buffer = ""
            except json.JSONDecodeError:
                buffer += "\n"

    return count


# -----------------------
# ASCII UI HELPERS
# -----------------------
BOX_WIDTH = 60


def hr(char="─"):
    return char * (BOX_WIDTH - 2)


def row(label, value=""):
    text = f"{label:<16}: {value}"
    padding = BOX_WIDTH - 3 - len(text)
    return f"│ {text}{' ' * max(0, padding)}│"


def title(text):
    padding = BOX_WIDTH - 3 - len(text)
    return f"│ {text}{' ' * max(0, padding)}│"


# -----------------------
# MAIN
# -----------------------
def main():
    cfg = load_json(Path("config.json"))
    keys = load_json(Path("keys.json"))

    input_dir = Path(cfg["input_dir"])
    data_dir = Path(cfg["data_dir"])
    data_dir.mkdir(parents=True, exist_ok=True)

    export_meta_path = data_dir / "export-meta.jsonl"
    message_meta_path = data_dir / "message-meta.jsonl"
    inbox_path = data_dir / "inbox.jsonl"

    seen_keys = load_seen_keys(message_meta_path)
    seen_exports = load_seen_export_ids(export_meta_path)

    priv_raw = b64url_to_bytes(keys["x25519_private"])
    priv_bytes = priv_raw[:32] if len(priv_raw) == 64 else priv_raw
    box = SealedBox(PrivateKey(priv_bytes))

    exports = sorted(input_dir.glob("*.jsonl"))
    if not exports:
        raise RuntimeError("No encrypted exports found")

    for export_file in exports:
        export_id = export_file.stem
        new_keys = 0
        skipped_keys = 0

        with export_file.open("r", encoding="utf-8") as f:
            buffer = ""
            for raw_line in f:
                buffer += raw_line.rstrip()
                try:
                    obj = json.loads(buffer)
                    buffer = ""
                except json.JSONDecodeError:
                    buffer += "\n"
                    continue

                # ---- META HEADER ----
                if obj.get("type") == "meta":
                    if export_id not in seen_exports:
                        export_meta = {
                            "export_id": export_id,
                            "export_time_utc": obj.get("export_time_utc"),
                            "kv_namespace": obj.get("kv_namespace"),
                            "source": obj.get("source"),
                        }
                        with export_meta_path.open("a", encoding="utf-8") as out:
                            out.write(json.dumps(export_meta) + "\n")
                        seen_exports.add(export_id)
                    continue

                # ---- MESSAGE ENTRY ----
                if "key" not in obj or "value" not in obj:
                    continue

                key = obj["key"]
                if key in seen_keys:
                    skipped_keys += 1
                    continue

                ciphertext = b64url_to_bytes(obj["value"])
                plaintext = box.decrypt(ciphertext)
                payload = json.loads(plaintext.decode("utf-8"))

                fs = payload.get("_fs", {})
                data = payload.get("data", {})

                msg_meta = {
                    "key": key,
                    "export_id": export_id,
                    "schema": fs,
                    "ingested_at_utc": datetime.now(timezone.utc).isoformat(),
                }

                inbox_entry = {
                    "key": key,
                    "export_id": export_id,
                    "fullname": data.get("fullname"),
                    "email": data.get("email"),
                    "message": data.get("message"),
                    "client_time": data.get("client_time"),
                    "client_tz": data.get("client_tz"),
                }

                with message_meta_path.open("a", encoding="utf-8") as out:
                    out.write(json.dumps(msg_meta) + "\n")

                with inbox_path.open("a", encoding="utf-8") as out:
                    out.write(json.dumps(inbox_entry) + "\n")

                seen_keys.add(key)
                new_keys += 1

        # ---- UI OUTPUT ----
        total_messages = count_jsonl_entries(message_meta_path)
        status = "replay (no new messages)" if new_keys == 0 else "ingested"

        print("\n┌" + hr() + "┐")
        print(title("EXPORT"))
        print("├" + hr() + "┤")
        print(row("file", export_file.name))
        print(row("status", status))
        print("├" + hr() + "┤")
        print(title("Messages"))
        print(row("new this export", new_keys))
        print(row("duplicates", skipped_keys))
        print(row("total stored", total_messages))
        print("└" + hr() + "┘")

    print("\nDecrypt + split complete")


if __name__ == "__main__":
    main()
