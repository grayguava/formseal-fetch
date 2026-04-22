# Main entry point

import sys
import os
from pathlib import Path

script_dir = Path(__file__).absolute()
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

from cli.ui import br, fail, info, warn, C, G, W, Y, R, D, GRAY, HEAD, header
from cli.commands import about as cmd_about
from cli.commands import version as cmd_version
from cli.commands import help as cmd_help
from cli.commands.config import run_status, run_set, run_disconnect
from cli.commands.setup import run as run_connect
from cli.commands.fetch import run as run_fetch
from cli.commands.providers import run as run_providers
from cli.providers import get_providers


COMMANDS = {
    "connect": ("Connect to a provider", lambda a: run_connect(a)),
    "fetch": ("Fetch ciphertexts", lambda a: run_fetch(a)),
    "status": ("Show connection status", lambda a: run_status()),
    "set": ("Set a config value", run_set),
    "disconnect": ("Clear all credentials", lambda a: run_disconnect(a)),
    "providers": ("List available providers", lambda a: run_providers(a)),
}


def _get_help_groups():
    providers = get_providers()
    provider_list = ", ".join(p.display_name for p in providers.values())
    return {
        "Connect": [
            ("fsf connect provider:<name>", "connect to a storage provider"),
            ("fsf disconnect", "clear configuration"),
            ("fsf disconnect --wipe", "clear everything including ciphertexts"),
        ],
        "Fetch": [
            ("fsf fetch", "download ciphertexts"),
            ("fsf fetch --output <file>", "custom output path"),
        ],
        "Config": [
            ("fsf status", "show configuration"),
            ("fsf set <key> <value>", "set config value"),
        ],
        "Info": [
            ("fsf providers", "list available providers"),
            ("fsf --version", "show version"),
            ("fsf --aliases", "list shorthand flags"),
        ],
        "Docs": [
            ("https://github.com/grayguava/formseal-fetch", None),
        ],
    }


HELP_GROUPS = _get_help_groups()


def _show_help():
    br()
    header()
    br()

    for group, cmds in HELP_GROUPS.items():
        print(f"  {GRAY}>> {group}{R}")
        print(G + " " + "\u2500" * 44 + R)
        for cmd, desc in cmds:
            if desc:
                print(f"  {W}{cmd:<27}{R} {G}{desc}{R}")
            else:
                print(f"  {C}{cmd}{R}")
        br()


def main():
    if len(sys.argv) < 2:
        cmd_about.run()
        return

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]

    if cmd == "--help":
        _show_help()
        return

    if cmd == "--about":
        cmd_about.run()
        return

    if cmd == "version" or cmd == "--version":
        cmd_version.run()
        return

    if cmd == "--aliases":
        cmd_help.run_aliases()
        return

    if cmd == "-s":
        cmd = "status"
    elif cmd == "-pl":
        cmd = "providers"
    elif cmd == "-c":
        cmd = "connect"
    elif cmd == "-o":
        cmd = "fetch"
        args = ["--output"] + args

    if cmd not in COMMANDS:
        br()
        fail(f"Unknown command: {cmd}\nRun 'fsf --help' for available commands")

    _, handler = COMMANDS[cmd]

    if handler is None:
        br()
        fail(f"Command not implemented: {cmd}")

    try:
        handler(args)
    except KeyboardInterrupt:
        br()
        info("Interrupted.")
        br()
        sys.exit(130)
    except Exception as e:
        fail(str(e))


if __name__ == "__main__":
    main()