from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Any


def parse_date(value: Any) -> date | None:
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        return None
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        return None


class HabitObserver(ABC):
    @abstractmethod
    def update(self, event_type: str, habit: dict[str, Any]) -> None:
        pass


class HabitSubject:
    def __init__(self) -> None:
        self._observers: list[HabitObserver] = []

    def register_observer(self, observer: HabitObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: HabitObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(
        self,
        event_type: str,
        habit: dict[str, Any],
    ) -> None:
        for observer in list(self._observers):
            try:
                observer.update(event_type, habit)
            except Exception:
                # Observers must not interrupt core transaction flow
                pass


# Global event dispatcher instance
_habit_subject = HabitSubject()


def get_habit_subject() -> HabitSubject:
    return _habit_subject


def create_habit(
    data: dict[str, Any],
    name: str,
    description: str = "",
    created_on: date | str | None = None,
) -> dict[str, Any]:
    if "habits" not in data or not isinstance(data["habits"], list):
        data["habits"] = []

    c_date = parse_date(created_on) or date.today()

    habit: dict[str, Any] = {
        "id": f"h_{uuid.uuid4().hex[:8]}",
        "name": name.strip(),
        "description": description.strip(),
        "created_on": c_date.strftime("%Y-%m-%d"),
        "completed_dates": [],
    }

    data["habits"].append(habit)
    _habit_subject.notify_observers("habit_created", habit)
    return habit


def get_all_habits(data: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(data, dict):
        return []
    return list(data.get("habits", []))


def get_habit(
    data: dict[str, Any],
    habit_id: str,
) -> dict[str, Any] | None:
    for habit in get_all_habits(data):
        if str(habit.get("id")) == str(habit_id):
            return habit
    return None


def find_habit_by_name(
    data: dict[str, Any],
    name: str,
) -> dict[str, Any] | None:
    clean_target = name.strip().lower()
    for habit in get_all_habits(data):
        if str(habit.get("name", "")).strip().lower() == clean_target:
            return habit
    return None


def mark_completed(
    data: dict[str, Any],
    habit_id: str,
    completion_date: date | str | None = None,
) -> bool:
    habit = get_habit(data, habit_id)
    if not habit:
        return False

    target_date = parse_date(completion_date) or date.today()
    if target_date > date.today():
        return False

    date_str = target_date.strftime("%Y-%m-%d")

    dates_list = habit.setdefault("completed_dates", [])
    if date_str in dates_list:
        return False

    dates_list.append(date_str)
    dates_list.sort()
    _habit_subject.notify_observers("habit_completed", habit)
    return True


def delete_habit(data: dict[str, Any], habit_id: str) -> bool:
    habits_list = data.get("habits", [])
    for idx, habit in enumerate(habits_list):
        if str(habit.get("id")) == str(habit_id):
            removed = habits_list.pop(idx)
            _habit_subject.notify_observers("habit_deleted", removed)
            return True
    return False