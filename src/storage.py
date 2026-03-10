# src/storage.py
import json
from pathlib import Path

class FileStore:
    def __init__(self, base_dir: str):
        self.base = Path(base_dir)
        self.base.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        return self.base / f"{key}.json"

    def get(self, key: str):
        p = self._path(key)
        return json.loads(p.read_text()) if p.exists() else None

    def set(self, key: str, value):
        p = self._path(key)
        p.write_text(json.dumps(value, ensure_ascii=False, indent=2))
