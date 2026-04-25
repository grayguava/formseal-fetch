# Getting started

This guide will help you install formseal-fetch and connect to your storage backend within minutes.

## Prerequisites

- **Python 3.8 or later**
- **Operating System**: Windows, macOS, or Linux
- **Network access** to your storage backend

## Installation

### From PyPI (recommended)

```bash
pip install formseal-fetch
```

### From source

```bash
git clone https://github.com/grayguava/formseal-fetch.git
cd formseal-fetch
pip install -e .
```

### Verify installation

```bash
fsf
# or
fsf --about
```

You should see the about page with version info.

```bash
fsf providers
```

Shows available storage backends.

## Quick start

### Step 1: Connect to your backend

```bash
fsf connect <name>
```

You'll be prompted for provider-specific credentials.

**For Cloudflare:**
- KV Namespace ID
- API Token
- Output folder (default: `data`)

**For Supabase:**
- Project Reference
- Table Name
- Service Role Key
- Output folder (default: `data`)

**For Redis:**
- Redis URL
- Key prefix
- Output folder (default: `data`)

You can also provide these non-interactively:

```bash
fsf connect cloudflare namespace:<id> token:<value> output:<path>
fsf connect supabase project_ref:<ref> table:<name> token:<key> output:<path>
fsf connect redis key_prefix:<prefix> output:<path>
```

### Step 2: Fetch ciphertexts

```bash
fsf fetch
```

This downloads all encrypted form submissions from your storage to `<output_folder>/formseal.ct.jsonl`. Each line is a raw ciphertext string, one per line.

### Step 3: Check connection and configuration status

```bash
fsf status
```

Shows your current provider, credentials, and output folder.

## Next steps

- See [Commands reference](./reference/commands.md) for all available commands
- [Cloudflare KV setup](./backends/cloudflare-kv.md)
- [Supabase setup](./backends/supabase.md)
- [Redis setup](./backends/redis.md)
- Read [Security](./security.md) to understand how credentials are stored
- Check [Troubleshooting](./troubleshooting.md) if you encounter issues