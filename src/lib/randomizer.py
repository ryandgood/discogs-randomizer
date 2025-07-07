import json
import random
from pathlib import Path
from ..models.discogs import Release  # reuse the Pydantic model

class AlbumRandomizer:
    def __init__(self, json_path: str):
        self.json_path = Path(json_path)
        self.releases =  self._load_releases()

    def _load_releases(self) -> list[Release]:
        if not self.json_path.exists():
            with open(self.json_path, "w", encoding="utf-8") as f:
                f.write("{}")

            raise FileNotFoundError(f"Collection file not found: {self.json_path}")

        with open(self.json_path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        return [Release(**r) for r in raw]

    def pick_random(self) -> Release:
        if not self.releases:
            raise ValueError("No releases available to choose from.")
        return random.choice(self.releases)
