# How it works

---

## The flow

```
Browser (formseal-embed)
       │
       ▼ (encrypted submissions)
  Your server (POST endpoint)
       │
       ▼ (ciphertext storage)
  fsf fetch (download ciphertexts)
       │
       ▼ (ciphertexts.jsonl)
  You (decrypt offline)
```

1. formseal-embed encrypts form submissions in the browser
2. Ciphertexts are stored at your endpoint (prefixed `formseal.`)
3. fsf fetches ciphertexts from your storage backend
4. You decrypt locally using your private key

---

## What fsf does

- Connects to storage backends (Cloudflare KV, Supabase, Redis)
- Downloads ciphertexts to `ciphertexts.jsonl`
- Skips duplicates automatically
- Never sends data to any server except your storage backend
- Credentials stored in OS keychain

---

## What fsf does NOT do

- Never decrypts data (you do this offline)
- Never sends data to external servers
- Never stores plaintext anywhere
- Never requires your private key

See [Deployment → Decryption](../deployment/decryption.md).
