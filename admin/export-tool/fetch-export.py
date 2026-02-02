import os
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone


# -----------------------
# ASCII UI HELPERS
# -----------------------
BOX_WIDTH = 68


def hr(char="─"):
    return char * (BOX_WIDTH - 2)


def spacer():
    return f"│{' ' * (BOX_WIDTH - 2)}│"


def row(label, value=""):
    value = str(value)
    text = f"{label:<16}: {value}"

    # truncate safely if too long
    if len(text) > BOX_WIDTH - 4:
        text = text[: BOX_WIDTH - 7] + "..."

    padding = BOX_WIDTH - 3 - len(text)
    return f"│ {text}{' ' * padding}│"


def title(text):
    padding = BOX_WIDTH - 3 - len(text)
    return f"│ {text}{' ' * padding}│"


def box_start(name):
    print("\n┌" + hr() + "┐")
    print(title(name))
    print("├" + hr() + "┤")


def box_end():
    print("└" + hr() + "┘")


def fatal(msg):
    print("\n┌" + hr() + "┐")
    print(title("ERROR"))
    print("├" + hr() + "┤")
    print(spacer())
    print(row("reason", msg))
    print(spacer())
    print("└" + hr() + "┘")
    sys.exit(1)


# -----------------------
# LOAD CONFIG
# -----------------------
CONFIG_PATH = Path("config.json")

if not CONFIG_PATH.exists():
    fatal("config.json not found")

try:
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
except json.JSONDecodeError as e:
    fatal(f"invalid config.json: {e}")

REQUIRED_KEYS = [
    "base_url",
    "export_request_path",
    "exports_dir",
    "filename_prefix",
    "filename_extension",
]

for k in REQUIRED_KEYS:
    if k not in cfg:
        fatal(f"missing config key: {k}")

BASE_URL = cfg["base_url"].rstrip("/")
EXPORT_PATH = cfg["export_request_path"]
EXPORT_DIR = Path(cfg["exports_dir"])
PREFIX = cfg["filename_prefix"]
EXT = cfg["filename_extension"]

EXPORT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------
# LOAD SECRET
# -----------------------
ADMIN_TOKEN = os.environ.get("FORMSEAL_ADMIN_TOKEN")
if not ADMIN_TOKEN or len(ADMIN_TOKEN) < 32:
    fatal("FORMSEAL_ADMIN_TOKEN missing or invalid")

AUTH_HEADER = f"Bearer {ADMIN_TOKEN}"

USER_AGENT = "FormSeal-Admin-Exporter/1.0"

COMMON_HEADERS = {
    "Authorization": AUTH_HEADER,
    "Content-Type": "application/json",
    "User-Agent": USER_AGENT,
}

# -----------------------
# BUILD OUTPUT FILE
# -----------------------
timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
out_file = EXPORT_DIR / f"{PREFIX}_{timestamp}{EXT}"

# -----------------------
# REQUEST EXPORT
# -----------------------
box_start("EXPORT REQUEST")
print(spacer())
print(row("endpoint", BASE_URL + EXPORT_PATH))
print(row("output file", out_file.name))
print(spacer())
box_end()

req = urllib.request.Request(
    BASE_URL + EXPORT_PATH,
    method="POST",
    headers=COMMON_HEADERS,
    data=b"{}",
)

try:
    with urllib.request.urlopen(req, timeout=30) as res:
        raw = res.read()
except urllib.error.HTTPError as e:
    fatal(f"export request failed ({e.code})")
except Exception as e:
    fatal(f"export request failed: {e}")

try:
    payload = json.loads(raw)
except json.JSONDecodeError:
    fatal("server returned non-JSON response")

download_url = payload.get("download_url")
if not download_url:
    fatal("missing download_url in response")

# -----------------------
# DOWNLOAD FILE
# -----------------------
box_start("DOWNLOAD")
print(spacer())
print(row("url", download_url))
print(spacer())
box_end()

req2 = urllib.request.Request(
    BASE_URL + download_url,
    headers={
        "Authorization": AUTH_HEADER,
        "User-Agent": USER_AGENT,
    },
)

try:
    with urllib.request.urlopen(req2, timeout=300) as res:
        data = res.read()
except urllib.error.HTTPError as e:
    fatal(f"download failed ({e.code})")
except Exception as e:
    fatal(f"download failed: {e}")

out_file.write_bytes(data)

# -----------------------
# SUCCESS
# -----------------------
box_start("SUCCESS")
print(spacer())
print(row("saved to", out_file.resolve()))
print(row("size (bytes)", len(data)))
print(spacer())
box_end()
