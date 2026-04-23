# fsf/providers/redis/engine.py
# Redis engine

import redis as redis_client
from fsf.ui import fail


def run(config):
    from fsf.security import tokens
    from fsf.commands.config.config import load_config

    cfg = load_config()
    provider = cfg.get("provider")
    url = tokens.load_token(provider)
    key_prefix = config.get("key_prefix", "submissions")

    try:
        r = redis_client.from_url(url)
        values = r.lrange(key_prefix, 0, -1)
        r.close()
    except Exception as e:
        fail(f"Redis connection failed: {e}")

    result = {}
    for i, v in enumerate(values):
        decoded = v.decode() if isinstance(v, bytes) else v
        result[f"redis_{i}"] = decoded.encode("utf-8")

    return result