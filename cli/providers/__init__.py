# Provider base class

import sys
from abc import ABC, abstractmethod
from importlib import import_module
from pathlib import Path


class Provider(ABC):

    name: str = None
    display_name: str = None
    storage_type: str = None

    @property
    def description(self):
        return ""

    def get_status_extra(self, token, cfg):
        return {}

    @abstractmethod
    def get_config_schema(self) -> dict:
        pass

    @abstractmethod
    def fetch(self, config: dict) -> dict[str, bytes]:
        pass


def discover_providers():
    providers = {}

    provider_dir = Path(__file__).parent

    for item in provider_dir.iterdir():
        if not item.is_dir():
            continue
        if item.name.startswith("_"):
            continue
        if item.name == "base":
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