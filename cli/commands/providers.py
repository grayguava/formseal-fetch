# List providers

from pathlib import Path

from cli.ui import br, C, G, Y, W, D, R, HEAD, header
from cli.commands import VERSION
from cli.providers import get_providers


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
        print(f"    {W}>  {provider.display_name}:{R}   {provider.description}")

    br()