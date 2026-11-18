"""Analytics and streak calculation module for Habit Tracker (Role C).

Provides algorithms for:
- Current streak calculation
- Longest historical streak calculation
- Completion percentage rates
- Weekly completion summaries

Does not import any other project module.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any


def parse_date(value: Any) -> date | None:
    """Safely parse a date object or YYYY-MM-DD string into a date.

    Returns None if the value cannot be parsed.
    """
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        return None
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        return None


def _extract_dates(habit: Any) -> list[date]:
    """Extract valid date objects from a habit dictionary or date list."""
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
    """Calculate consecutive daily completions up to today or yesterday.

    If today is completed, streak counts backward from today.
    If today is not completed, streak counts backward from yesterday.
    If neither today nor yesterday is completed, returns 0.
    """
    if habit is None:
        return 0

    valid_dates = _extract_dates(habit)
    if not valid_dates:
        return 0

    ref_date = parse_date(today) or date.today()
    completed_set = {d for d in valid_dates if d <= ref_date}

    if not completed_set:
        return 0

    # Determine whether streak starts today or yesterday
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
    """Calculate the longest consecutive daily completion streak.

    Duplicates are ignored. Gaps reset the current count.
    """
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
    """Calculate completion percentage (0.0 to 100.0) over a period.

    If start_date is not given, uses habit's 'created_on' or earliest date.
    If end_date is not given, defaults to today.
    Handles zero-day durations safely without ZeroDivisionError.
    """
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
    """Calculate 7-day completion count for every habit in data.

    Returns a dictionary mapping habit ID (or name) to count of
    completed days within the last 7 days (today - 6 days through today).
    """
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
