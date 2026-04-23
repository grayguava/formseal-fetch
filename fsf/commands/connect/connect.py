# Connect commands

import sys
from pathlib import Path

from fsf.ui import br, fail, ok, info, warn, G, W, D, C, Y, O, R, HEAD, OK, header
from fsf.commands.config.config import load_config, save_config
from fsf.security import tokens
from fsf.providers import get_providers


def _parse_args(args):
    if not args:
        fail("Usage: fsf connect <provider> [key:value ...]")
    
    provider = args[0].lower()
    parsed = {"provider": provider}
    
    for arg in args[1:]:
        if ":" not in arg:
            fail(f"Invalid format: {arg}\n           Use key:value (e.g., field:value)")
        key, value = arg.split(":", 1)
        parsed[key] = value
    
    return parsed


def run(args):
    if not args:
        fail("Usage: fsf connect <provider> [key:value ...]")

    parsed = _parse_args(args)

    cfg = load_config()
    if cfg.get("provider"):
        fail(f"Provider already set: {cfg['provider']}\nRun 'fsf disconnect' first.")

    provider = parsed["provider"].lower()
    providers = get_providers()
    if provider not in providers:
        fail(f"Unknown provider: {provider}\n           Run fsf providers to see available.")

    _setup_flow(provider, parsed, providers[provider])


def _setup_flow(provider, parsed, provider_obj):
    print()
    header("setup")
    print()

    cfg = load_config()
    cfg["provider"] = provider

    inputs = provider_obj.get_inputs()

    for field in inputs:
        key = field["name"]
        prompt = field.get("description", key)
        sensitive = field.get("sensitive", False)

        value = parsed.get(key)
        if not value:
            try:
                sys.stdout.write(f"  {prompt}: ")
                sys.stdout.flush()
                value = input().strip()
            except KeyboardInterrupt:
                br()
                info("Cancelled.")
                br()
                return

        if field.get("required") and not value:
            fail(f"{prompt} is required")

        if value:
            if sensitive:
                tokens.save_namespace(provider, value, key=key)
            else:
                cfg[key] = value

    token_label = provider_obj.get_token_label()
    if token_label:
        if "token" in parsed:
            token = parsed["token"]
        else:
            try:
                sys.stdout.write(f"  {token_label}: ")
                sys.stdout.flush()
                token = sys.stdin.readline().strip()
            except KeyboardInterrupt:
                br()
                info("Cancelled.")
                br()
                return
            if not token:
                fail(f"{token_label} is required")

        token = "".join(c for c in token if c.isprintable()).strip()
        if not token:
            fail(f"{token_label} is required")

        tokens.save_token(provider, token)

    if "output" in parsed:
        output_folder = parsed["output"]
    else:
        try:
            sys.stdout.write(f"  Output Folder [{D}data{R}]: ")
            sys.stdout.flush()
            output_folder = input().strip()
            if not output_folder:
                output_folder = "data"
        except KeyboardInterrupt:
            br()
            info("Cancelled.")
            br()
            return

    output_folder = Path(output_folder).resolve()
    try:
        output_folder.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        fail(f"Invalid output folder: {e}")

    cfg["output_folder"] = str(output_folder)
    print()

    save_config(cfg)

    print(f"{G}{OK}{R} Saved!")
    print()
    print(f"  Run {W}fsf fetch{R} to download ciphertexts")
    print()