# Getting started

FormSeal-Sync is a local CLI tool that syncs encrypted form submissions from your storage backend to your PC.

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

Ciphertexts appear in your output folder as `ciphertexts.jsonl`.

---

## Verify

```bash
fsync status
```

Shows your config, provider, and credential status.

---

## Next steps

- [Commands](./reference/commands.md) — full CLI reference
- [Configuration](./configuration.md) — config file and env vars
- [Daemon](./daemon.md) — background sync operation
- [Providers](./providers.md) — supported backends