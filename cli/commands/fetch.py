# Fetch ciphertexts

import argparse
from pathlib import Path

from cli.ui import br, fail, ok, info, G, W, D, C, R, Y, HEAD, header
from cli.commands import VERSION
from cli.commands.config import load_config
from cli.security import tokens
from cli.providers import get_provider


def run(args):
    parser = argparse.ArgumentParser(prog="fsf fetch")
    parser.add_argument("--output", default=None)
    parsed = parser.parse_args(args)

    cfg = load_config()
    provider_name = cfg.get("provider")
    output_folder = cfg.get("output_folder", "data")

    if not provider_name:
        fail("No provider set. Run: fsf connect provider:<name>")

    provider = get_provider(provider_name)
    if not provider:
        fail(f"Unknown provider: {provider_name}")

    provider_config = _build_provider_config(provider, provider_name)

    br()
    header()
    br()

    def row(label, value, color=W):
        print(f"  {D}{label:<26}{R}{color}{value}{R}")

    schema = provider.get_config_schema()
    for key in schema:
        value = provider_config.get(key)
        if value:
            sensitive = schema[key].get("sensitive", True)
            if sensitive:
                trunc = value[:8] + "***" if len(str(value)) > 8 else str(value)
            else:
                trunc = str(value)
            row(f"{key.capitalize()}:", trunc)

    br()

    try:
        files = provider.fetch(provider_config)
    except Exception as e:
        fail(f"Fetch failed: {e}")

    if not files:
        info("No data to fetch.")
        br()
        return

    output_path = parsed.output or f"{output_folder}/ciphertexts.jsonl"

    written, skipped = _write_files(files, output_path)

    total = 0
    if Path(output_path).exists():
        with open(output_path, "r", encoding="utf-8") as f:
            total = sum(1 for line in f if line.strip())

    br()
    row("New entries:", written, G if written > 0 else D)
    row("Duplicate/Skipped:", skipped, D if skipped > 0 else D)
    row("Current total:", total, G)
    row("Output File Path:", output_path, W)

    br()


def _build_provider_config(provider, provider_name):
    schema = provider.get_config_schema()
    config = {}
    cfg = load_config()

    for key in schema:
        sensitive = schema[key].get("sensitive", True)
        if sensitive:
            value = tokens.load_namespace(provider_name, key=key)
        else:
            value = cfg.get(key)
        if value:
            config[key] = value

    config["token"] = tokens.load_token(provider_name)

    return config


def _write_files(files: dict[str, bytes], output_path: str) -> tuple[int, int]:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    existing = set()
    if Path(output_path).exists():
        with open(output_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    existing.add(line.strip())

    written = 0
    skipped = 0
    for name, data in files.items():
        content = data.decode("utf-8") if isinstance(data, bytes) else data

        if content in existing:
            skipped += 1
            continue

        with open(output_path, "a", encoding="utf-8") as f:
            f.write(content + "\n")
        existing.add(content)
        written += 1

    return written, skipped