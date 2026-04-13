# Architecture

FormSeal-Sync is a local CLI tool that pulls encrypted form submissions from your storage backend and saves them to your PC.

```
Browser → Storage (Cloudflare/Supabase) → FormSeal-Sync → Local ciphertexts.jsonl
```

---

## Components

| Component | Location | Description |
|---|---|---|
| CLI entry | `cli/fsync.py` | Main command handler |
| Node wrapper | `cli/shim.js` | Calls Python from npm |
| Daemon | `cli/daemon/worker.py` | Background sync process |
| Providers | `cli/providers/<name>/` | Storage backend adapters |
| Config | `~/.formsealdaemon/config.json` | User settings |

---

## Data flow

1. User runs `fsync sync start`
2. `cli/daemon/sync.py` spawns `worker.py` as detached process
3. Worker reads config from `~/.formsealdaemon/config.json`
4. Worker reads API token from environment variable
5. Worker calls provider's `fetch(config, output_path)`
6. Provider returns `(written, skipped)` counts
7. Ciphertexts appended to `ciphertexts.jsonl`
8. Worker sleeps for `sync_interval` minutes
9. Repeat from step 3

---

## Provider interface

Each provider implements:

```
cli/providers/<name>/
├── account.py      # validate credentials (optional)
└── storage/
    └── __init__.py # fetch(config, output_path) -> (written, skipped)
```