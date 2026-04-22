# fsf/providers/__init__.py
# Provider system

import json
from abc import ABC, abstractmethod
from importlib import import_module
from pathlib import Path


class BaseProvider(ABC):

    name: str = None

    def __init__(self):
        self._schema = None

    @property
    def schema(self):
        if self._schema is None:
            self._schema = self._load_schema()
        return self._schema

    @property
    def display_name(self):
        return self.schema.get("display_name", self.name.capitalize())

    @property
    def storage_type(self):
        return self.schema.get("storage_type", self.name)

    def _load_schema(self):
        provider_dir = Path(__file__).parent / self.name
        config_file = provider_dir / "config.json"
        if config_file.exists():
            with open(config_file, encoding="utf-8") as f:
                return json.load(f)
        return {}

    def get_inputs(self):
        return self.schema.get("inputs", [])

    def get_sensitive_fields(self):
        return [f["name"] for f in self.schema.get("inputs", []) if f.get("sensitive")]

    def get_non_sensitive_fields(self):
        return [f["name"] for f in self.schema.get("inputs", []) if not f.get("sensitive")]

    def get_token_label(self):
        return self.schema.get("token_label", "Token")

    @abstractmethod
    def fetch(self, config: dict) -> dict[str, bytes]:
        pass


Provider = BaseProvider


def discover_providers():
    providers = {}

    provider_dir = Path(__file__).parent

    for item in provider_dir.iterdir():
        if not item.is_dir():
            continue
        if item.name.startswith("_"):
            continue

        init_file = item / "__init__.py"
        if not init_file.exists():
            continue

        module_name = f"{__name__}.{item.name}"

        try:
            module = import_module(module_name)
        except Exception:
            continue

        cls = getattr(module, "Provider", None)
        if cls:
            providers[cls.name] = cls()

    return providers


def get_providers():
    return discover_providers()


def get_provider(name):
    providers = get_providers()
    return providers.get(name)