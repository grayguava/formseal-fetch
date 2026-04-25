# Documentation

Welcome to the formseal-fetch documentation.

## Quick links

| Guide | Description |
|-------|-------------|
| [Getting Started](./getting-started.md) | Installation and first-time setup |
| [Security](./security.md) | How credentials are stored and protected |
| [Commands Reference](./reference/commands.md) | All available commands |
| [Configuration](./reference/configuration.md) | Config files and storage |
| [Cloudflare KV](./backends/cloudflare-kv.md) | Cloudflare KV backend |
| [Supabase](./backends/supabase.md) | Supabase backend |
| [Redis](./backends/redis.md) | Redis backend |
| [Troubleshooting](./troubleshooting.md) | Common issues and solutions |

## What is formseal-fetch?

formseal-fetch is a CLI tool that downloads encrypted form submissions from your storage backend. Use it together with [formseal-embed](https://github.com/grayguava/formseal-embed) — the client-side form encryption library.

## Supported backends

- Cloudflare KV
- Supabase
- Redis

## Workflow

```
Browser (formseal-embed)
       │
       ▼ (encrypted submissions)
  Storage backend
       │
       ▼ (fsf fetch)
  formseal.ct.jsonl ──► Your PC
```