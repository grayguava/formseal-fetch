# List providers

from pathlib import Path

from fsf.ui import br, C, G, Y, W, D, R, HEAD, header
from fsf.commands.general.version import VERSION
from fsf.providers import get_providers


def run(args):
    _list_providers()


def _list_providers():
    providers = get_providers()

    br()
    header()
    br()

    print(f"  {G}Available providers:{R}")
    br()

    for name, provider in providers.items():
        name_part = f"    {W}>  {provider.display_name}:{R}"
        visible = f"    >  {provider.display_name}:"
        print(name_part + " " * (25 - len(visible)) + f"{provider.storage_type}")

    br()