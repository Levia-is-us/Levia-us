from typing import Optional
from abc import ABC, abstractmethod


class KeyVault(ABC):
    """Key Management Interface"""

    @abstractmethod
    def set_key(self, key: str, value: str) -> None:
        """Store a new key-value pair"""
        pass

    @abstractmethod
    def get_key(self, key: str) -> Optional[str]:
        """Get the value for a specified key"""
        pass

    @abstractmethod
    def delete_key(self, key: str) -> bool:
        """Delete a specified key"""
        pass

    @abstractmethod
    def list_keys(self) -> list:
        """List all stored keys"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all stored keys"""
        pass