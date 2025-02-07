from typing import Optional
import json
import os
from memory.key_vault.main import KeyVault


class LocalKeyVault(KeyVault):
    def __init__(self):
        self.vault_path = "vault.json"
        if not os.path.exists(self.vault_path):
            with open(self.vault_path, "w") as f:
                json.dump({}, f)

    def _load_vault(self):
        with open(self.vault_path, "r") as f:
            return json.load(f)

    def _save_vault(self, data):
        with open(self.vault_path, "w") as f:
            json.dump(data, f, indent=2)

    def set_key(self, key: str, value: str) -> None:
        vault = self._load_vault()
        vault[key] = value
        self._save_vault(vault)
        print(f"Key '{key}' set to '{value}' in vault.json")

    def get_key(self, key: str) -> Optional[str]:
        vault = self._load_vault()
        return vault.get(key, None)

    def delete_key(self, key: str) -> bool:
        vault = self._load_vault()
        if key in vault:
            del vault[key]
            self._save_vault(vault)
            print(f"Key '{key}' deleted from vault.json")
            return True
        return False

    def list_keys(self) -> list:
        vault = self._load_vault()
        return list(vault.keys())
