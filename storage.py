#STUB

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

DEFAULT_DATA_FILE = Path(__file__).parent / "data" / "habits.json"


def load_data(file_path: str | Path = DEFAULT_DATA_FILE) -> dict[str, Any]:
    path = Path(file_path)
    if not path.exists():
      return {"habits": []}
    try:
        with path.open("r", encoding="utf-8") as file:
          data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Data file must contains invalid JSON: {path}") from exc

    if not isinstance(data, dict) or not isinstance(data.get("habits"), list):
        raise ValueError("Data file must contain a JSON object with a 'habits' list.")
    return data  


def save_data(data):
  pass
