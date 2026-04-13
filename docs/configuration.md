# Configuration

---

## Config file

Location: `~/.formsealdaemon/config.json`

```json
{
  "provider": "cloudflare",
  "cloudflare.namespace": "abc123...",
  "cloudflare.storage": "kv",
  "output_folder": "D:/Documents/FormData",
  "sync_interval": 15,
  "last_sync": "2026-04-13T12:00:00.000000"
}
```

---

## Keys

| Key | Description |
|---|---|
| `provider` | Storage backend name |
| `<provider>.*` | Provider-specific settings (namespace, URL, etc.) |
| `output_folder` | Where to save ciphertexts |
| `sync_interval` | Minutes between sync cycles |
| `last_sync` | ISO timestamp of last successful sync |

---

## Environment variables

Sensitive credentials are read from environment variables — never stored in config.

| Variable | Used by | Description |
|---|---|---|
| `FSYNC_CF_TOKEN` | Cloudflare provider | API token |
| `FSYNC_SU_KEY` | Supabase provider | Service key |

See `fsync help --vars` for OS-specific setup instructions.

---

## Files

| File | Location | Description |
|---|---|---|
| Config | `~/.formsealdaemon/config.json` | All settings |
| PID | `~/.formsealdaemon/sync.pid` | Daemon process ID |
| Log | `~/.formsealdaemon/sync.log` | Daemon activity log |

---

## Editing

Edit config via CLI:

```bash
fsync set provider cloudflare
fsync set output_folder C:/data
fsync set sync_interval 5
```

Or edit the file directly (except tokens/keys — use env vars).