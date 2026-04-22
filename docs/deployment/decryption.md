# Decryption

> Decryption tooling is under development. This page will be updated when it ships.

---

## What you'll need

- Your **private key** — generated during formseal-embed setup
- The **ciphertext** — downloaded via `fsf fetch`

---

## In the meantime

Decryption is straightforward with libsodium. The ciphertext is a standard sealed box — any libsodium binding will open it.

```python
import base64, json
from nacl.public import PrivateKey, SealedBox

# Your private key (base64url, without padding)
raw_key = base64.urlsafe_b64decode(your_private_key_base64 + "==")
box = SealedBox(PrivateKey(raw_key))

# Ciphertext from fsf fetch output (remove "formseal." prefix)
ciphertext = base64.urlsafe_b64decode(your_ciphertext_here + "==")
payload = json.loads(box.decrypt(ciphertext))

print(payload)
```

**Output:**

```json
{
  "version": "fse.v1.0",
  "origin": "contact-form",
  "id": "uuid",
  "submitted_at": "2024-01-15T10:30:00Z",
  "data": {
    "name": "John",
    "email": "john@example.com",
    "message": "Hello"
  }
}
```

This is the full decryption — no custom parsing, no proprietary format. The output is plain JSON.

See [Concepts → How it works](../concepts/how-it-works.md).
