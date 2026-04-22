# Security policy

## Supported versions

Only the latest release is actively supported.

| Version | Supported |
|----------|------------|
| latest   | ✅ |
| older versions | ❌ |

Please upgrade before reporting vulnerabilities on outdated releases.

---

## Reporting a vulnerability

**Do not open public GitHub issues for security vulnerabilities.**

Report vulnerabilities privately through GitHub:

https://github.com/grayguava/formseal-fetch/security/advisories/new

Include:

- affected version
- reproduction steps
- impact
- proof-of-concept (if available)

Do not include real credentials, tokens, or production secrets in reports.

---

## Security scope

`formseal-fetch` is a **ciphertext retrieval CLI**.

Its responsibility is limited to:

- authenticating with your configured backend
- retrieving encrypted payloads
- returning ciphertext to the client

It does **not**:

- perform decryption
- manage private keys
- generate encryption keys
- inspect plaintext secrets
- transmit analytics or telemetry

If your decryption workflow is handled elsewhere, that system is outside the security scope of this project.

---

## Credential storage

Backend credentials are stored locally using Python's `keyring` library.

Depending on your operating system, this may use: 

- Windows Credential Manager
- macOS Keychain
- Linux Secret Service / compatible keyring backend

In rare environments where no supported keyring backend is available, `formseal-fetch` falls back to a local secrets file.

This fallback stores credentials using Base64 formatting for portability only.

**Base64 is not encryption.** It only encodes data into a readable transport format and provides significantly weaker protection than system keychains.

This is used as a fallback only when a secure system keyring is unavailable, or `keyring` is not installed on the host machine.

---

## What this project cannot protect against

This project cannot protect against:

- malware on your machine
- stolen API tokens
- compromised backend infrastructure
- weak access controls on your storage provider
- accidental exposure of retrieved ciphertext

If your backend credentials are compromised, rotate them immediately.

---

## Local credential removal

To remove locally stored credentials:

```bash
fsf disconnect
```
