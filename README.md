<p align="center">
  <img src="fsf.png" alt="formseal-fetch">
</p>

<p align="center">
  <img src="https://img.shields.io/pypi/v/formseal-fetch?style=flat&label=pypi&labelColor=1e293b&color=3776ab">
  <img src="https://img.shields.io/badge/license-MIT-fc8181?style=flat&labelColor=1e293b">
  <img src="https://img.shields.io/github/actions/workflow/status/grayguava/formseal-fetch/publish.yml">
  <img src="https://img.shields.io/badge/formseal-ecosystem-10b981?style=flat&labelColor=1e293b">
</p>

<p align="center">
  Download encrypted form submissions from your storage backend.
</p>

---

formseal-fetch pulls ciphertexts stored by your backend down to your machine. Nothing is decrypted in transit or on the server — only the holder of the private key can read submissions.

formseal-fetch is not a hosted service or dashboard. It is a CLI fetch utility.

---

## Installation

**Via pipx (recommended)**

```bash
pipx install formseal-fetch
```

**Via pip**

```bash
pip install formseal-fetch
```

---

## Quick start

```bash
fsf connect provider:<name>
fsf fetch
fsf status
```

---

## How it works

```
Browser (formseal-embed)
       │
       ▼ (encrypted submissions)
 Cloudflare KV / Supabase / any other server
       │
       ▼ (fsf fetch)
  ciphertexts.jsonl ──► Your PC
```

Your backend stores opaque ciphertext only. `fsf fetch` downloads it. Decryption happens separately, offline, with your private key.

---

## Commands

| Command | Description |
|---------|-------------|
| `fsf` | Show about / info |
| `fsf connect` | Connect to a storage provider |
| `fsf fetch` | Download ciphertexts |
| `fsf status` | Show connection info |
| `fsf disconnect` | Clear credentials |
| `fsf disconnect --wipe` | Clear everything including ciphertexts |
| `fsf providers` | List available backends |

Run `fsf --help` for all options.

---

## Security

Your API tokens never leave your machine. formseal-fetch:

- Stores credentials in your OS keychain (Windows Credential Manager / macOS Keychain / Linux Secret Service)
- Makes direct API calls to your storage backend only
- Sends no telemetry, has no analytics
- Skips already-downloaded ciphertexts automatically

---

## Documentation

- [Getting Started](./docs/getting-started.md)
- [Security](./docs/security.md)
- [Commands Reference](./docs/reference/commands.md)
- [Troubleshooting](./docs/troubleshooting.md)

---

## License

MIT