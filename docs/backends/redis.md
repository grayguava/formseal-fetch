# Redis

Connecting formseal-fetch to your Redis database.

## What you need

To connect formseal-fetch to Redis, you'll need:

| Item | Where to find it |
|------|------------------|
| Redis URL | Your Redis connection string (e.g., `rediss://user:pass@host:port`) |
| Key prefix | The list key where ciphertexts are stored |

## Getting your credentials

### Redis URL

For Upstash Redis:
1. Go to your Upstash dashboard
2. Find the "Connection Details" or "Redis CLI" section
3. Copy the URL (starts with `rediss://`)

For self-hosted Redis:
- Use your own connection string: `redis://host:port` or `rediss://host:port` for TLS

### Key prefix

The key (Redis list) where your ciphertexts are stored. Default is `submissions`.

## Connecting

### Interactive mode

```bash
fsf connect redis
```

You'll be prompted for:
- Redis URL
- Key prefix
- Output folder (default: `data`)

### Non-interactive mode

```bash
fsf connect redis key_prefix:<prefix> output:<path>
```

**Example:**

```bash
fsf connect redis key_prefix:submissions output:data
```

## Fetching ciphertexts

```bash
fsf fetch
```

Ciphertexts are saved to `<output_folder>/ciphertexts.jsonl` — one raw ciphertext per line.

## Verifying connection

```bash
fsf status
```

Shows your key prefix and token location.

## Common issues

| Error | Cause | Solution |
|-------|-------|----------|
| "Redis connection failed" | Invalid URL or unreachable | Check your Redis URL |
| "Not set" | Token not saved | Reconnect with correct URL |
| Empty results | Wrong key prefix | Check your key prefix matches (even caps/lowercaps can cause issues)