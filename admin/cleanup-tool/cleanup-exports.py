import json
from pathlib import Path


# -----------------------
# HELPERS
# -----------------------
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


def extract_keys_from_export(path: Path) -> set[str]:
    keys = set()

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

            if obj.get("type") == "meta":
                continue

            if "key" in obj:
                keys.add(obj["key"])

    return keys


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
    cfg = json.loads(Path("config.json").read_text())

    export_dir = Path(cfg["export_dir"])
    data_dir = Path(cfg["data_dir"])
    dry_run = cfg.get("dry_run", True)

    message_meta = data_dir / "message-meta.jsonl"
    seen_keys = load_seen_keys(message_meta)

    deleted = 0
    kept = 0
    skipped = 0

    print("\n┌" + hr() + "┐")
    print(title("CLEANUP"))
    print("├" + hr() + "┤")
    print(row("export dir", export_dir))
    print(row("dry run", dry_run))
    print("└" + hr() + "┘")

    for export in sorted(export_dir.glob("*.jsonl")):
        export_keys = extract_keys_from_export(export)

        if not export_keys:
            skipped += 1
            continue

        if export_keys.issubset(seen_keys):
            if not dry_run:
                export.unlink()
            deleted += 1
        else:
            kept += 1

    print("\n┌" + hr() + "┐")
    print(title("RESULT"))
    print("├" + hr() + "┤")
    print(row("deleted", deleted))
    print(row("kept", kept))
    print(row("skipped", skipped))
    print("└" + hr() + "┘")

    print("\nCleanup finished")


if __name__ == "__main__":
    main()
