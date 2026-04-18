# Supabase

Connecting formseal-fetch to your Supabase database.

## What you need

To connect formseal-fetch to Supabase, you'll need:

| Item | Where to find it |
|------|------------------|
| Project Reference | Your Supabase project URL (e.g., `abcd1234` from `abcd1234.supabase.co`) |
| Table Name | Name of table storing ciphertexts (e.g., `submissions`, `ciphertexts`) |
| Service Role Key | Supabase Dashboard → Settings → API |

## Getting your credentials

### Project Reference

From your Supabase project URL:
- URL: `https://[ref].supabase.co`
- Use just the `[ref]` part (e.g., `abcd1234`)

### Table Name

The table where your ciphertexts are stored. Common names:
- `submissions`
- `ciphertexts`
- `forms`
- `data`

### Service Role Key

1. Go to Supabase Dashboard → Settings → API
2. Copy the `service_role` key (not `anon` key)

The service_role key bypasses RLS and can read all rows.

## Connecting

### Interactive mode

```bash
fsf connect provider:supabase
```

You'll be prompted for:
- Project Reference
- Table Name
- Service Role Key (shows as "Service Role Key" prompt)
- Output folder (default: `data`)

### Non-interactive mode

```bash
fsf connect provider:supabase project_ref:<ref> table:<name> token:<key> output:<path>
```

**Example:**

```bash
fsf connect provider:supabase project_ref:abcd1234 table:submissions token:eyJhbGci... output:data
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

Shows your project reference, table name, and token location.

## Common issues

| Error | Cause | Solution |
|-------|-------|----------|
| HTTP 403 | Using anon key instead of service_role | Use service_role key |
| HTTP 404 | Invalid project reference | Check your project URL |
| "No table" | Wrong table name | Verify table exists in Supabase |
| Empty results | Table has no rows or wrong columns | Check your table data |