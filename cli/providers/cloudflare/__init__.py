# Cloudflare provider

from cli.providers import Provider
from cli.providers.cloudflare.storage.kv import fetch as kv_fetch


class CloudflareProvider(Provider):

    name = "cloudflare"
    display_name = "☁️ Cloudflare"
    storage_type = "kv"

    @property
    def storage_label(self):
        return "Key-Value"

    @property
    def description(self):
        return f"{self.storage_label} storage"

    def get_config_schema(self):
        return {
            "namespace": {
                "required": True,
                "description": "KV Namespace ID",
                "sensitive": False
            }
        }

    def fetch(self, config):
        namespace = config.get("namespace")
        token = config.get("token")
        if not namespace or not token:
            raise ValueError("namespace and token are required")
        return kv_fetch(namespace=namespace, token=token)

    def get_status_extra(self, token, cfg):
        from cli.providers.cloudflare.storage.kv import _get_account_id
        account_id = _get_account_id(token)
        partial = account_id[:12] + "..." if len(account_id) > 12 else account_id
        return {"Account ID": partial}


Provider = CloudflareProvider