#STUB

from __future__ import annotations

import os
from datetime import date, datetime
from typing import Callable


def parse_date(value: str | date | None) -> date | None:
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        return None
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        return None


def display_header(title: str) -> None:
    banner = "=" * 54
    print("\n" + banner)
    print(title.center(54))
    print(banner)


def display_menu(options: list[str]) -> None:
    print()
    for idx, opt in enumerate(options, 1):
        print(f"  [{idx}] {opt}")
    print()


def get_non_empty_input(
    prompt: str = "Enter value: ",
    input_func: Callable[[str], str] = input,
) -> str:
    while True:
        val = input_func(prompt).strip()
        if val:
            return val
        print("  Error: Input cannot be empty. Please try again.")


def get_optional_input(
    prompt: str = "Enter value (optional): ",
    default: str = "",
    input_func: Callable[[str], str] = input,
) -> str:
    val = input_func(prompt).strip()
    return val if val else default


def validate_date(date_str: str) -> bool:
    return parse_date(date_str) is not None


def get_date_input(
    prompt: str = "Enter date (YYYY-MM-DD) [Leave empty for today]: ",
    input_func: Callable[[str], str] = input,
) -> date:
    while True:
        val = input_func(prompt).strip()
        if not val:
            return date.today()
        parsed = parse_date(val)
        if parsed is not None:
            return parsed
        print("  Error: Invalid date format. Please use YYYY-MM-DD.")


def get_menu_choice(
    max_option: int,
    prompt: str = "Select an option: ",
    input_func: Callable[[str], str] = input,
) -> int:
    while True:
        val = input_func(prompt).strip()
        if val.isdigit():
            choice = int(val)
            if 1 <= choice <= max_option:
                return choice
        print(f"  Error: Please enter a number between 1 and {max_option}.")


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def confirm(
    prompt: str = "Are you sure? (y/n): ",
    input_func: Callable[[str], str] = input,
) -> bool:
    """Prompt user for a yes/no confirmation."""
    val = input_func(prompt).strip().lower()
    return val in ("y", "yes")