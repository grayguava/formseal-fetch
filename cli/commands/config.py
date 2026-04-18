# Config management

import json
import sys
from pathlib import Path

from cli.ui import br, fail, ok, info, warn, G, W, D, C, Y, R, HEAD, header
from cli.security import tokens
from cli.providers import get_provider, get_providers


def _load_version():
    p = Path(__file__).parent.parent.parent / "version.txt"
    if p.exists():
        return p.read_text().strip()
    return "dev"


VERSION = _load_version()


CONFIG_DIR = Path.home() / ".config" / "formseal-fetch"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {}


def save_config(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))


def get_token(provider: str):
    return tokens.load_token(provider)


def get_namespace(provider: str):
    return tokens.load_namespace(provider)


def run_set(args):
    if len(args) < 2:
        fail("Usage: fsf set <key> <value>")

    key = args[0]
    value = " ".join(args[1:])

    cfg = load_config()
    providers = get_providers()

    if key == "provider":
        if value not in providers:
            fail(f"Unknown provider: {value}\nValid: {', '.join(providers.keys())}")
        cfg["provider"] = value
        save_config(cfg)
        br()
        ok(f"Provider set to {value}")
        br()
        return

    if key == "output_folder":
        cfg[key] = value
        save_config(cfg)
        br()
        ok(f"Set {key} = {value}")
        br()
        return

    fail(f"Unknown key: {key}")


def run_status():
    cfg = load_config()

    br()
    header(VERSION)
    br()

    print(f"  {D}Configuration Status:{R}")
    br()

    provider_name = cfg.get("provider")
    if not provider_name:
        warn("No provider configured. Run: fsf connect provider:<name>")
        br()
        return

    provider = get_provider(provider_name)

    def row(label, value, color=W):
        print(f"  {D}{label:<26}{R}{color}{value}{R}")

    row("Provider:", provider.display_name if provider else provider_name)

    if provider:
        schema = provider.get_config_schema()
        for key, field_schema in schema.items():
            sensitive = field_schema.get("sensitive", True)
            if sensitive:
                value = tokens.load_namespace(provider_name, key=key)
            else:
                value = cfg.get(key)
            desc = field_schema.get("description", key)
            row(f"{desc}:", value or "(not set)", W if value else D)

        token = get_token(provider_name)
        if token:
            extra = {}
            if hasattr(provider, "get_status_extra"):
                try:
                    extra = provider.get_status_extra(token, cfg)
                except Exception:
                    pass
            for label, value in extra.items():
                row(f"{label}:", value)
            row("API Token:", "****")
            row("Token Location:", tokens.token_location(provider_name), G)
        else:
            row("API Token:", "(not set)", D)
            row("Token Location:", "Not set", D)

        br()
        storage_type = getattr(provider, 'storage_label', provider.storage_type)
        row("Storage Type:", storage_type)

    output_folder = cfg.get("output_folder")
    row("Output Folder:", output_folder or "(not set)", W if output_folder else D)

    br()


def run_config_show():
    cfg = load_config()

    br()
    header("config")
    br()

    provider = cfg.get("provider")

    if not cfg:
        info("No config. Run: fsf connect provider:<name>")
    else:
        for k, v in cfg.items():
            print(f"  {D}{k}:{R}  {W}{v}{R}")

    if provider:
        token = get_token(provider)
        print(f"  {D}token:{R}  {'****' if token else 'not set'}")

    br()


def run_disconnect(args=None):
    args = args or []
    wipe = "--wipe" in args

    if wipe:
        br()
        print(f"  {Y}THIS WILL DELETE EVERYTHING.{R}")
        print(f"  Config, credentials, AND ciphertexts will be deleted.")
    else:
        br()
        print(f"  {Y}This will delete all config and credentials.{R}")
        print(f"  Downloaded ciphertexts will NOT be affected.")
    br()
    sys.stdout.write(f"  Continue? [y/N]: ")
    sys.stdout.flush()
    confirm = input().strip().lower()

    if confirm != "y":
        br()
        info("Cancelled.")
        br()
        return

    cfg = load_config()
    provider = cfg.get("provider")

    if wipe:
        output_folder = cfg.get("output_folder")
        if output_folder:
            ciphertext_path = Path(output_folder) / "ciphertexts.jsonl"
            if ciphertext_path.exists():
                ciphertext_path.unlink()

    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()

    if provider:
        tokens.clear_all(provider)

    br()
    if wipe:
        ok("Disconnected. Everything wiped.")
    else:
        ok("Disconnected. All config and credentials cleared.")
    br()


run_logout = run_disconnect