# commands/help.py
# Help command - shows all available commands

from fsf.ui import br, header, cmd_line, rule
from fsf.ui.styles import C, G, R, W, GRAY


def _get_help_groups():
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


def _show_help():
    groups = _get_help_groups()
    br()
    header()
    br()

    for group, cmds in groups.items():
        print(f"  {GRAY}>> {group}{R}")
        print(G + " " + "\u2500" * 44 + R)
        for cmd, desc in cmds:
            if desc:
                print(f"  {W}{cmd:<27}{R} {G}{desc}{R}")
            else:
                print(f"  {C}{cmd}{R}")
        br()


def run():
    _show_help()


def run_aliases():
    br()
    header("shorthand aliases")
    br()

    print(f" {W}Short{R}  {G}Canonical{R}")
    print(G + " " + "\u2500" * 44 + R)
    print(f" {W}-s{R}     {G}status{R}")
    print(f" {W}-c{R}     {G}connect{R}")
    print(f" {W}-o{R}     {G}fetch --output <path>{R}")
    print(f" {W}-pl{R}    {G}providers{R}")
    br()