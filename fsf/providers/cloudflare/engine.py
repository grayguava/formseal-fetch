# fsf/providers/cloudflare/engine.py
# Cloudflare KV engine

from fsf.providers.cloudflare.account import get_account_id
from fsf.providers.cloudflare.storage.kv import fetch as kv_fetch


def run(config):
    namespace = config.get("namespace")
    token = config.get("token")
    if not namespace or not token:
        raise ValueError("namespace and token are required")
    return kv_fetch(namespace=namespace, token=token)


def get_account(config):
    token = config.get("token")
    return get_account_id(token)