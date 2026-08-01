"""Adapter Factory for dynamic vendor adapter instantiation."""

from typing import Dict, Type, Set
from .base import ValveAdapter
from .sonoff_swv import SonoffSWVAdapter


class AdapterFactory:
    """Factory pattern for registering and retrieving ValveAdapter instances."""

    _adapters: Dict[str, Type[ValveAdapter]] = {
        "sonoff_swv": SonoffSWVAdapter,
    }

    @classmethod
    def register(cls, name: str, adapter_cls: Type[ValveAdapter]) -> None:
        """Register a new vendor adapter class.

        Args:
            name: Adapter identifier (e.g. 'esphome', 'shelly').
            adapter_cls: Class inheriting from ValveAdapter.
        """
        if not issubclass(adapter_cls, ValveAdapter):
            raise TypeError(f"Adapter class '{adapter_cls.__name__}' must inherit from ValveAdapter")
        cls._adapters[name.lower()] = adapter_cls

    @classmethod
    def get_adapter(cls, name: str) -> ValveAdapter:
        """Instantiate an adapter by name.

        Args:
            name: Adapter identifier.

        Returns:
            Instance of ValveAdapter.

        Raises:
            KeyError: If adapter name is not registered.
        """
        adapter_name = name.lower()
        if adapter_name not in cls._adapters:
            raise KeyError(f"Unknown adapter '{name}'. Registered adapters: {sorted(list(cls._adapters.keys()))}")
        return cls._adapters[adapter_name]()

    @classmethod
    def available_adapters(cls) -> Set[str]:
        """Return set of registered adapter names."""
        return set(cls._adapters.keys())
