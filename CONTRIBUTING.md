# Contributing to formseal-fetch

Thanks for your interest in contributing! Contributions of all kinds are welcome — bug fixes, new features, docs, and more. **Provider and security contributions are especially valued since the tool is designed to be backend-agnostic.**

---

## Table of contents

- [Getting started](#getting-started)
- [Project structure](#project-structure)
- [Adding a new provider](#adding-a-new-provider)
- [Versioning](#versioning)
- [Code style](#code-style)
- [Submitting changes](#submitting-changes)
- [Testing](#testing)
- [Reporting issues](#reporting-issues)

---

## Getting started

1. Fork the repository and clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/formseal-fetch.git
   cd formseal-fetch
   ```

2. Install in development mode using `pipx` (recommended) or `pip`:
   ```bash
   pipx install -e .
    ```
3. Verify it works:
   ```bash
   fsf
   ```

> **Note:** Always use `pipx install -e .` for local dev — it gives you an isolated environment and the version header will display correctly from source.

---

## Project structure

```
formseal-fetch/
├── fsf/
│   ├── fsf.py                  # Entry point, argument dispatch
│   ├── cmd.py                 # Command registry
│   ├── ui.py                  # Terminal output helpers (colors, header)
│   ├── general/               # Helpers (aliases, errors)
│   ├── commands/              # CLI commands
│   │   ├── general/           # about, version, help, providers
│   │   ├── fetch/             # fsf fetch
│   │   ├── connect/           # fsf connect
│   │   └── config/            # fsf status, fsf set, fsf disconnect
│   ├── providers/             # Storage backend implementations
│   │   ├── __init__.py       # Provider base class + registry
│   │   ├── cloudflare/       # Cloudflare KV provider
│   │   └── supabase/         # Supabase provider
│   └── security/
│       └── tokens.py         # Keyring-backed credential storage
├── docs/                     # End-user documentation
├── .github/
│   ├── workflows/            # GitHub Actions workflows
│   └── ISSUE_TEMPLATE/      # GitHub issue forms
├── pyproject.toml
└── version.txt              # Source of truth for the version string
```

---

## Adding a new provider

Providers are storage backends that `fsf fetch` reads ciphertexts from. Each lives in its own sub-package under `fsf/providers/`.

**1. Create the package folder:**
```
fsf/providers/<name>/
├── config.json    # Provider metadata
├── __init__.py  # Provider class
└── engine.py    # Fetch logic
```

**2. Create `config.json`:**
```json
{
  "name": "<name>",
  "display_name": "Display Name",
  "storage_type": "Storage Type",
  "token_label": "Token Prompt Label",
  "inputs": [
    {
      "name": "field_name",
      "description": "Field description",
      "required": true,
      "sensitive": false
    }
  ]
}
```

**3. Implement the provider in `__init__.py`:**
```python
from fsf.providers import BaseProvider
from fsf.providers.<name>.engine import run

class MyProvider(BaseProvider):
    name = "<name>"

    def fetch(self, config):
        return run(config)

Provider = MyProvider
```

**4. Implement fetch logic in `engine.py`:**
```python
def run(config):
    return {"submission-id": b"ciphertext bytes here"}
```

**5. Register it** by adding the package to `pyproject.toml` under `[tool.setuptools].packages`:
```toml
[tool.setuptools]
packages = [
    ...
    "fsf.providers.<name>",
]
```

**6. Verify** it appears:
```bash
fsf providers
```

---

## Versioning

The version string lives in **`version.txt`** and is the single source of truth. The publish workflow reads it and injects it into the code at build time.

When preparing a release:
1. Update `version.txt` with the new version (e.g., `2.3.0`)
2. Trigger the **Inject Version** workflow from GitHub Actions

---

## Code style

- Add a comment at the top of each logical block explaining what it does
- Follow the patterns already in the file you're editing
- Use the `ui.py` helpers (`info`, `fail`, `warn`, `br`, `header`) for all terminal output
- Sensitive config values must go through `security/tokens.py` (keyring-backed), never stored in plaintext config

---

## Submitting changes

1. Create a branch off `main`:
   ```bash
   git checkout -b feat/my-feature
   ```

2. Make your changes and test locally (see [Testing](#testing))

3. Commit with clear, descriptive messages

4. Push and open a pull request against `main`

---

## Testing

There is no automated test suite yet. Test the relevant commands manually before opening a PR:

```bash
fsf                          # check version header displays correctly
fsf providers                # verify your provider appears (if adding one)
fsf connect provider:<name>  # walk through the setup flow
fsf status                   # confirm credentials were saved
fsf fetch                    # fetch ciphertexts end-to-end
fsf disconnect               # confirm credentials are cleared
```

---

## Reporting issues

Use the GitHub issue templates — they're structured to make sure we get the info needed to help quickly:

- **[Bug report](https://github.com/grayguava/formseal-fetch/issues/new?template=bug_report.yml)** : something isn't working
- **[Documentation issue](https://github.com/grayguava/formseal-fetch/issues/new?template=documentation.yml)** : something in the docs is wrong or missing
- **[Question / support](https://github.com/grayguava/formseal-fetch/issues/new?template=question.yml)** : need help with setup or usage