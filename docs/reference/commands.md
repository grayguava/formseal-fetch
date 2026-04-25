# Commands reference

Complete reference for all formseal-fetch commands.

## Usage syntax

```bash
fsf <command> [options] [arguments]
```

## Commands

### connect

Connect to a storage backend.

```bash
fsf connect <name> [field:value]...
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `<name>` | Storage provider — available: `cloudflare`, `supabase`, `redis` |
| `field:<value>` | Provider-specific fields (see provider docs) |

**Examples:**

```bash
# Interactive mode — you'll be prompted for all required values
fsf connect <name>

# Non-interactive — all values provided via arguments
fsf connect <name> field:<value> field:<value>
```

Press `Ctrl+C` at any prompt to cancel.

---

### fetch

Download ciphertexts from your connected backend.

```bash
fsf fetch [--output <path>]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--output` | Custom output file path (default: `<output_folder>/formseal.ct.jsonl`) |

**Examples:**

```bash
# Use default output folder
fsf fetch

# Custom output file
fsf fetch --output my-data.jsonl
```

**Deduplication:**

If you run `fsf fetch` multiple times, duplicates are automatically skipped based on ciphertext content. The output shows:
- Number of new ciphertexts saved
- Number of duplicates skipped

---

### status

Show current connection status and configuration.

```bash
fsf status
```

**Output includes:**

- Provider name and display name
- Provider-specific fields (from config)
- Token status and storage location
- Output folder path

---

### set

Set a configuration value.

```bash
fsf set <key> <value>
```

**Arguments:**

| Key | Description |
|-----|-------------|
| `output_folder` | Path where ciphertexts are saved |

**Examples:**

```bash
fsf set output_folder my-data
```

---

### disconnect

Clear all credentials and configuration.

```bash
fsf disconnect
fsf disconnect --wipe
```

**What it removes:**

- Provider configuration
- API token (from OS Keychain or secrets.json)
- Provider-specific fields (from OS Keychain or secrets.json)
- Configuration file

**What it does NOT remove (disconnect only):**

- Downloaded ciphertexts in your output folder

**--wipe flag:**

```bash
fsf disconnect --wipe
```

This removes everything above PLUS the ciphertexts file.

---

### providers

List available storage backends.

```bash
fsf providers
```

---

### --help

Show help information.

```bash
fsf --help
```

---

### --version

Show version number.

```bash
fsf --version
fsf version
```

---

### --aliases

Show shorthand aliases.

```bash
fsf --aliases
```

Lists all available shorthand flags:

| Short | Canonical |
|-------|-----------|
| `-s` | `status` |
| `-c` | `connect <name>` |
| `-o` | `fetch --output <path>` |
| `-p` | `providers` |

---

### --about

Show project information.

```bash
fsf --about
```
