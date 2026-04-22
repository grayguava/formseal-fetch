# fsf/providers/cloudflare/__init__.py
# Cloudflare provider

from fsf.providers import BaseProvider
from fsf.providers.cloudflare.engine import run


class CloudflareProvider(BaseProvider):

    name = "cloudflare"

    def fetch(self, config):
        return run(config)


Provider = CloudflareProvider