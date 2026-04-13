# Daemon

The background sync daemon runs continuously, periodically fetching new ciphertexts from your storage backend.

---

## Start

```bash
fsync sync start
```

Spawns a detached process. Returns immediately — you can close the terminal.

The daemon:
- Runs in the background
- Survives terminal closing
- Reads config from `~/.formsealdaemon/config.json`
- Logs to `~/.formsealdaemon/sync.log`

---

## Stop

```bash
fsync sync stop
```

Kills the daemon process by PID stored in `~/.formsealdaemon/sync.pid`.

---

## Status

```bash
fsync sync status
```

Shows:
- Running state and PID
- Current sync interval
- Last sync timestamp
- Recent log entries (last 5 lines)

---

## Manual run

```bash
fsync sync run
```

Runs one sync cycle in the foreground. Output shown directly.

Useful for:
- Testing configuration
- One-time fetches
- Debugging issues

---

## Interval

The daemon reads `sync_interval` from config on each cycle. Change it without restarting:

```bash
fsync setup sync
```

Or set directly:

```bash
fsync set sync_interval 5
```

---

## Troubleshooting

**Daemon won't start**
```
Sync already running (PID: 12345). Run: fsync sync stop first.
```

**No new submissions**
```bash
# Check credentials
fsync status

# Check logs
type %USERPROFILE%\.formsealdaemon\sync.log

# Run manually to see errors
fsync sync run
```

**Duplicate syncs**
If you see entries twice per interval, a previous daemon may still be running:
```bash
fsync sync stop
fsync sync start
```