# fsf/providers/redis/__init__.py
# Redis provider

from fsf.providers import BaseProvider
from fsf.providers.redis.engine import run


class RedisProvider(BaseProvider):

    name = "redis"

    def fetch(self, config):
        return run(config)


Provider = RedisProvider