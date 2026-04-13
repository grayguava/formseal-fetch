# Commands

---

## Setup

### fsync setup quick

Interactive wizard to configure the storage backend.

```bash
fsync setup quick
```

Prompts for:
- Provider (storage backend)
- Storage type
- Provider-specific settings (namespace ID, URL, etc.)
- Output folder

### fsync setup sync

Set the sync interval in minutes.

```bash
fsync setup sync
```

Default: 15 minutes.

### fsync setup reset

Clear all configuration.

```bash
fsync setup reset
```

---

## Sync

### fsync sync start

Start the background sync daemon. Returns immediately — runs detached.

```bash
fsync sync start
```

### fsync sync stop

Stop the background sync daemon.

```bash
fsync sync stop
```

### fsync sync status

Show daemon status, PID, interval, last sync time, and recent logs.

```bash
fsync sync status
```

### fsync sync run

Run sync once in the foreground. Useful for testing or one-time fetches.

```bash
fsync sync run
```

---

## Fetch

### fsync fetch

Download ciphertexts from the configured backend.

```bash
fsync fetch                    # Uses config's output_folder
fsync fetch --output custom.j  # Custom output path
```

---

## Config

### fsync status

Show current configuration.

```bash
fsync status
```

Shows provider, storage settings, output folder, and credential status.

### fsync set

Set a config value directly.

```bash
fsync set provider cloudflare
fsync set output_folder C:/data
fsync set sync_interval 5
```

### fsync logout

Clear all stored configuration.

```bash
fsync logout
```

---

## Other

### fsync --help

Show all available commands.

```bash
fsync --help
```

### fsync help --vars

Show environment variable setup instructions for your OS.

```bash
fsync help --vars             # Auto-detect OS
fsync help --vars-windows     # Windows
fsync help --vars-macos       # macOS
fsync help --vars-linux       # Linux
```

### fsync providers

List available storage backends.

```bash
fsync providers
fsync providers --cloudflare
fsync providers --supabase
```