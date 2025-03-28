from abc import ABC
from typing import Dict, Callable
import inspect


class BaseTool(ABC):
    """Base class for all tools"""
    description = "Base tool class"
    timeout = 180

    def __init__(self):
        self._name = self.__class__.__name__
        self._description = self.__doc__ or "No description available"
        self._method_docs = {}
        self._methods = {}
        self._register_methods()

    def _register_methods(self) -> None:
        """Register all public methods as tool methods"""
        for name, method in inspect.getmembers(self, inspect.ismethod):
            if not name.startswith('_'):
                self._methods[name] = method
                self._method_docs[name] = method.__doc__ or "No description available"

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def methods(self) -> Dict[str, Callable]:
        """Get registered methods"""
        return self._methods

    def get_method_description(self, method_name: str) -> str:
        """Get the description of a method"""
        return self._method_docs.get(method_name, "No description available")

