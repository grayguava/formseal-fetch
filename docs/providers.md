# Providers

FormSeal-Sync fetches ciphertexts from storage backends via HTTP APIs.

---

## Supported providers

| Provider | Storage type | Description |
|---|---|---|
| Cloudflare | KV | Cloudflare Workers KV |
| Supabase | DB | Supabase PostgreSQL |

---

## Cloudflare KV

Fetches from Cloudflare Workers KV namespace.

**Required:**
- API token with KV read scope (`FSYNC_CF_TOKEN`)
- Namespace ID

**Configuration:**
```bash
fsync set provider cloudflare
fsync set namespace <namespace-id>
```

---

## Supabase DB

Fetches from Supabase PostgreSQL table.

**Required:**
- Service key with table read access (`FSYNC_SU_KEY`)
- Project URL
- Table name (default: `ciphertexts`)

**Configuration:**
```bash
fsync set provider supabase
fsync set url <project-url>
fsync set table <table-name>
```

---

## Adding new providers

The provider system is modular. Each provider lives in `cli/providers/<name>/`.

To add a new backend, create:

```
cli/providers/<name>/
├── account.py      # optional: validate credentials
└── storage/
    ├── __init__.py # fetch(config, output_path) -> (written, skipped)
    └── ...
```

The CLI auto-detects available providers. Run `fsync providers` to see what's installed.