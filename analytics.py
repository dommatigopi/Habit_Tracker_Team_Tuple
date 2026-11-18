from __future__ import annotations

from datetime import date, datetime, timedelta
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


def _extract_dates(habit: Any) -> list[date]:
    raw_dates: list[Any] = []
    if isinstance(habit, dict):
        raw_dates = habit.get("completed_dates", [])
    elif isinstance(habit, list):
        raw_dates = habit

    parsed_dates: set[date] = set()
    for item in raw_dates:
        parsed = parse_date(item)
        if parsed is not None:
            parsed_dates.add(parsed)

    return sorted(parsed_dates)


def calculate_current_streak(
    habit: Any = None,
    today: date | str | None = None,
) -> int:
    if habit is None:
        return 0

    valid_dates = _extract_dates(habit)
    if not valid_dates:
        return 0

    ref_date = parse_date(today) or date.today()
    completed_set = {d for d in valid_dates if d <= ref_date}

    if not completed_set:
        return 0

    if ref_date in completed_set:
        cursor = ref_date
    elif (ref_date - timedelta(days=1)) in completed_set:
        cursor = ref_date - timedelta(days=1)
    else:
        return 0

    streak = 0
    while cursor in completed_set:
        streak += 1
        cursor -= timedelta(days=1)

    return streak


def calculate_longest_streak(habit: Any = None) -> int:
    if habit is None:
        return 0

    valid_dates = _extract_dates(habit)
    if not valid_dates:
        return 0

    longest = 1
    current = 1

    for i in range(1, len(valid_dates)):
        diff = (valid_dates[i] - valid_dates[i - 1]).days
        if diff == 1:
            current += 1
            if current > longest:
                longest = current
        elif diff > 1:
            current = 1

    return longest


def calculate_completion_rate(
    habit: Any = None,
    start_date: date | str | None = None,
    end_date: date | str | None = None,
) -> float:
    if habit is None:
        return 0.0

    valid_dates = _extract_dates(habit)

    end = parse_date(end_date) or date.today()

    start = parse_date(start_date)
    if start is None and isinstance(habit, dict):
        start = parse_date(habit.get("created_on"))
    if start is None:
        start = valid_dates[0] if valid_dates else end

    if start > end:
        return 0.0

    total_days = (end - start).days + 1
    if total_days <= 0:
        return 0.0

    completed_in_range = sum(1 for d in valid_dates if start <= d <= end)
    rate = (completed_in_range / total_days) * 100.0
    return round(min(100.0, max(0.0, rate)), 2)


def weekly_summary(
    data: Any = None,
    today: date | str | None = None,
) -> dict[str, int]:
    summary: dict[str, int] = {}
    if not data:
        return summary

    ref_date = parse_date(today) or date.today()
    seven_days_ago = ref_date - timedelta(days=6)

    habits_list: list[Any] = []
    if isinstance(data, dict):
        habits_list = data.get("habits", [])
    elif isinstance(data, list):
        habits_list = data

    for habit in habits_list:
        if not isinstance(habit, dict):
            continue
        h_id = str(habit.get("id") or habit.get("name") or "unknown")
        valid_dates = _extract_dates(habit)
        count = sum(
            1 for d in valid_dates if seven_days_ago <= d <= ref_date
        )
        summary[h_id] = count

    return summary
