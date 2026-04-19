# Contributing to formseal-fetch

Thanks for your interest in contributing! This guide covers everything you need to get started.

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
   # or
   pip install -e .
   ```

3. Verify it works:
   ```bash
   fsf
   ```
   You should see the header with the version from `cli/version.txt`.

> **Note:** Always use `pipx install -e .` for local dev — it gives you an isolated environment and the version header will display correctly from source.

---

## Project structure

```
formseal-fetch/
├── cli/
│   ├── fsf.py                  # Entry point, argument dispatch
│   ├── ui.py                   # Terminal output helpers (colors, header)
│   ├── version.txt             # Source of truth for the version string
│   ├── commands/               # One file per CLI command
│   │   ├── config.py           # fsf status, fsf set, fsf disconnect
│   │   ├── fetch.py            # fsf fetch
│   │   ├── providers.py        # fsf providers
│   │   └── setup.py            # fsf connect
│   ├── providers/              # Storage backend implementations
│   │   ├── __init__.py         # Provider base class + registry
│   │   ├── cloudflare/         # Cloudflare KV provider
│   │   └── supabase/           # Supabase provider
│   └── security/
│       └── tokens.py           # Keyring-backed credential storage
├── docs/                       # End-user documentation
├── .github/
│   └── ISSUE_TEMPLATE/         # GitHub issue forms
├── pyproject.toml
└── MANIFEST.in
```

---

## Adding a new provider

Providers are storage backends that `fsf fetch` reads ciphertexts from. Each lives in its own sub-package under `cli/providers/`.

**1. Create the package folder:**
```
cli/providers/<name>/
└── __init__.py
```

**2. Implement the `Provider` class in `__init__.py`:**

```python
from cli.providers import Provider

class MyProvider(Provider):
    name = "<name>"                      # used in `fsf connect provider:<name>`
    display_name = "👾 MyProvider"       # shown in `fsf providers`

    def get_config_schema(self):
        """
        Return a dict describing the config fields this provider needs.
        Fields marked sensitive=True are stored in the system keyring.
        """
        return {
            "api_key": {
                "required": True,
                "description": "Your API key",
                "sensitive": True
            },
            "bucket": {
                "required": True,
                "description": "Storage bucket name",
                "sensitive": False
            }
        }

    def fetch(self, config):
        """
        Fetch all ciphertexts from the backend.
        Returns dict[str, bytes] — one entry per submission.
        """
        return {"submission-id": b"ciphertext bytes here"}

    def get_status_extra(self, token, cfg):
        """
        Optional: return extra key-value rows shown in `fsf status`.
        """
        return {"Bucket": cfg.get("bucket")}

Provider = MyProvider
```

**3. Register it** by adding the package to `pyproject.toml` under `[tool.setuptools].packages`:
```toml
[tool.setuptools]
packages = [
    ...
    "cli.providers.<name>",
]
```

**4. Verify** it appears:
```bash
fsf providers
```

---

## Versioning

The version string lives in **`cli/version.txt`** and is the single source of truth. The publish workflow reads it and injects it into `pyproject.toml` at build time.

When preparing a release:
1. Update `cli/version.txt` with the new version (e.g. `2.3.0`)
2. Create and push a git tag: `git tag v2.3.0 && git push --tags`
3. Trigger the **Publish to PyPI** workflow from GitHub Actions

Do not edit the `version` field in `pyproject.toml` manually — it gets overwritten by the workflow.

---

## Code style

- Add a comment at the top of each logical block explaining what it does — not required for every line or function, but each distinct section of logic should have one
- Follow the patterns already in the file you're editing
- Use the `ui.py` helpers (`info`, `fail`, `warn`, `br`, `header`) for all terminal output — don't print directly
- Sensitive config values must go through `cli/security/tokens.py` (keyring-backed), never stored in plaintext config

---

## Submitting changes

1. Create a branch off `main`:
   ```bash
   git checkout -b feat/my-feature
   # or
   git checkout -b fix/some-bug
   ```

2. Make your changes and test locally (see [Testing](#testing))

3. Commit with clear, descriptive messages:
   ```
   fix: include version.txt in package data
   feat: add Supabase storage provider
   docs: expand provider contribution guide
   ```

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

If your change touches the install/packaging path, test both install methods:
```bash
pipx install -e .            # local dev
pip install formseal-fetch   # from PyPI (after publishing)
```

---

## Reporting issues

Use the GitHub issue templates — they're structured to make sure we get the info needed to help quickly:

- **[Bug report](https://github.com/grayguava/formseal-fetch/issues/new?template=bug_report.yml)** : something isn't working
- **[Documentation issue](https://github.com/grayguava/formseal-fetch/issues/new?template=documentation.yml)** : something in the docs is wrong or missing
- **[Question / support](https://github.com/grayguava/formseal-fetch/issues/new?template=question.yml)** : need help with setup or usage