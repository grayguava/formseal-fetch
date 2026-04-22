# fsf/cmd.py
# Command registry

from fsf.commands.config.config import run_status, run_set, run_disconnect
from fsf.commands.connect.connect import run as run_connect
from fsf.commands.fetch.fetch import run as run_fetch
from fsf.commands.general.providers import run as run_providers


COMMANDS = {
    "connect": ("Connect to a provider", lambda a: run_connect(a)),
    "fetch": ("Fetch ciphertexts", lambda a: run_fetch(a)),
    "status": ("Show connection status", lambda a: run_status()),
    "set": ("Set a config value", run_set),
    "disconnect": ("Clear all credentials", lambda a: run_disconnect(a)),
    "providers": ("List available providers", lambda a: run_providers(a)),
}