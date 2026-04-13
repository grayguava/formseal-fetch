# FormSeal-Sync

<p align="center">
  <img src="https://img.shields.io/badge/CLI-fsync-10b981?style=flat&labelColor=1e293b">
  <img src="https://img.shields.io/badge/FormSeal-daemon-f59e0b?style=flat&labelColor=1e293b">
  <img src="https://img.shields.io/npm/v/@formseal/sync?style=flat&label=npm&labelColor=fff&color=cb0000">
  <img src="https://img.shields.io/badge/license-MIT-fc8181?style=flat&labelColor=1e293b">
</p>

FormSeal-Sync is a local CLI tool that pulls encrypted form submissions from your storage backend and saves them to your PC. Use it together with FormSeal-Embed — the client-side form encryption library.

---

## What it does

FormSeal-Embed encrypts form data in the browser before submission. The ciphertext is stored in your backend (Cloudflare KV, Supabase, etc.). FormSeal-Sync syncs those ciphertexts to your local machine so you can decrypt them offline with your private key.

---

## Install

```bash
npm install -g @formseal/sync
```

Requires Python 3.8+.

---

## Quick start

```bash
# 1. Configure your storage backend
fsync setup quick

# 2. Set API credentials as environment variables
fsync help --vars

# 3. Start background sync
fsync sync start
```

Ciphertexts are saved to `ciphertexts.jsonl` in your configured output folder.

---

## How it works

```
Browser (FormSeal-Embed)
       │
       ▼ (encrypted submissions)
  Storage backend (Cloudflare KV / Supabase)
       │
       ▼ (fsync pulls)
  Your PC ──► ciphertexts.jsonl
       │
       ▼ (decrypt offline)
  Plaintext form data
```

---

## Commands

| Command | Description |
|---|---|
| `fsync setup quick` | Interactive setup wizard |
| `fsync setup sync` | Set sync interval |
| `fsync sync start` | Start background sync |
| `fsync sync stop` | Stop background sync |
| `fsync sync status` | Check sync status and logs |
| `fsync sync run` | Run sync once (manual) |
| `fsync status` | Show current configuration |
| `fsync fetch` | Download ciphertexts |
| `fsync providers` | List available backends |

Run `fsync --help` for all commands.

---

## Supported backends

- **Cloudflare KV** — Cloudflare Workers Key-Value store
- **Supabase** — PostgreSQL database

More coming soon.

---

## Documentation

- [Getting started](./docs/getting-started.md)
- [Concepts → Architecture](./docs/concepts/architecture.md)
- [Reference → Commands](./docs/reference/commands.md)
- [Configuration](./docs/configuration.md)
- [Daemon](./docs/daemon.md)
- [Providers](./docs/providers.md)

---

## Related

- [FormSeal-Embed](https://github.com/grayguava/formseal-embed) — Client-side form encryption

---

## License

MIT