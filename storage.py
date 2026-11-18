from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_DATA_FILE = Path(__file__).resolve().parent / "habits.json"


def load_data(file_path: str | Path = DEFAULT_DATA_FILE) -> dict[str, Any]:
    
    path = Path(file_path)
    if not path.exists():
        return {"habits": []}

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Data file contains invalid JSON: {path}") from exc

    if not isinstance(data, dict) or not isinstance(data.get("habits"), list):
        raise ValueError(
            "Data file must contain a JSON object with a 'habits' list."
        )

    return data


def save_data(
    data: dict[str, Any],
    file_path: str | Path = DEFAULT_DATA_FILE,
) -> bool:
    
    path = Path(file_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    except Exception as exc:
        raise OSError(f"Failed to save habit data to {path}: {exc}") from exc
