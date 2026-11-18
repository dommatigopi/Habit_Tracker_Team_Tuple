from __future__ import annotations

from datetime import date
from typing import Any

import analytics
import habits
import reports
import storage
from utils import (
    clear_screen,
    confirm,
    display_header,
    display_menu,
    get_date_input,
    get_menu_choice,
    get_non_empty_input,
    get_optional_input,)

MENU_OPTIONS = [
    "Create a new habit",
    "View all habits",
    "Mark a habit as completed",
    "View habit streaks and analytics",
    "Generate summary report",
    "Generate completion chart",
    "Delete (archive) a habit",
    "Exit",]


def choose_habit(data: dict[str, Any]) -> dict[str, Any] | None:
    habits_list = habits.get_all_habits(data)
    if not habits_list:
        print("  No habits found.")
        return None

    print("\n  Available Habits:")
    for idx, h in enumerate(habits_list, 1):
        print(f"    [{idx}] {h.get('name')} (ID: {h.get('id')})")

    choice = get_menu_choice(len(habits_list), prompt="  Select habit number: ")
    return habits_list[choice - 1]


def create_habit_flow(data: dict[str, Any]) -> None:
    display_header("CREATE NEW HABIT")
    name = get_non_empty_input("  Habit Name: ")
    description = get_optional_input("  Description: ")
    created_date = get_date_input(
        "  Creation Date (YYYY-MM-DD) [empty for today]: ")

    new_h = habits.create_habit(
        data,
        name=name,
        description=description,
        created_on=created_date,)
    storage.save_data(data)
    print(f"\n  [SUCCESS] Habit '{new_h['name']}' created successfully (ID: {new_h['id']})!")


def list_habits_flow(data: dict[str, Any]) -> None:
    display_header("ALL HABITS")
    habits_list = habits.get_all_habits(data)
    if not habits_list:
        print("  No habits currently tracked.")
        return

    for idx, h in enumerate(habits_list, 1):
        h_id = h.get("id")
        h_name = h.get("name")
        h_desc = h.get("description", "")
        h_created = h.get("created_on", "")
        comp_count = len(h.get("completed_dates", []))
        print(f"  [{idx}] {h_name} (ID: {h_id})")
        if h_desc:
            print(f"      Description: {h_desc}")
        print(f"      Created on: {h_created} | Total completed days: {comp_count}")
        print("  " + "-" * 40)


def complete_habit_flow(data: dict[str, Any]) -> None:
    display_header("MARK HABIT AS COMPLETED")
    habit = choose_habit(data)
    if not habit:
        return

    comp_date = get_date_input(
        "  Completion Date (YYYY-MM-DD) [empty for today]: ")
    success = habits.mark_completed(data, habit["id"], comp_date)
    if success:
        storage.save_data(data)
        print(
            f"\n  [SUCCESS] '{habit['name']}' marked completed for {comp_date.isoformat()}!")
    else:
        print("\n  [INFO] Could not mark completed. Date may be duplicate or in the future.")


def analytics_flow(data: dict[str, Any]) -> None:
    display_header("HABIT ANALYTICS & STREAKS")
    habit = choose_habit(data)
    if not habit:
        return

    curr_streak = analytics.calculate_current_streak(habit)
    longest_streak = analytics.calculate_longest_streak(habit)
    comp_rate = analytics.calculate_completion_rate(habit)

    print("\n  Analytics for:", habit.get("name"))
    print(f"    Current Streak : {curr_streak} days")
    print(f"    Longest Streak : {longest_streak} days")
    print(f"    Completion Rate: {comp_rate}%")


def report_flow(data: dict[str, Any]) -> None:
    display_header("SUMMARY REPORT")
    rep_text = reports.build_report(data)
    print(rep_text)

    if confirm("\n  Save report to file? (y/n): "):
        filename = get_optional_input(
            "  File path [default: habit_report.txt]: ",
            default="habit_report.txt",)
        if reports.save_report(rep_text, filename):
            print(f"  [SUCCESS] Report saved to {filename}")
        else:
            print(f"  [ERROR] Failed to save report to {filename}")


def chart_flow(data: dict[str, Any]) -> None:
    display_header("COMPLETION CHARTS")
    print("\n  ASCII Text Chart (Last 7 Days):")
    weekly_data = analytics.weekly_summary(data)
    chart_str = reports.text_chart(weekly_data)
    print(chart_str)

    if confirm("\n  Save graphical chart to PNG? (y/n): "):
        filename = get_optional_input(
            "  PNG file path [default: chart.png]: ",
            default="chart.png",)
        if reports.save_chart_image(weekly_data, filename):
            print(f"  [SUCCESS] Chart image saved to {filename}")
        else:
            print(f"  [ERROR] Failed to save chart image to {filename}")


def delete_habit_flow(data: dict[str, Any]) -> None:
    display_header("DELETE HABIT")
    habit = choose_habit(data)
    if not habit:
        return

    if confirm(f"  Are you sure you want to delete '{habit['name']}'? (y/n): "):
        if habits.delete_habit(data, habit["id"]):
            storage.save_data(data)
            print(f"\n  [SUCCESS] Habit '{habit['name']}' deleted.")
        else:
            print("\n  [ERROR] Failed to delete habit.")


def run_app() -> None:
    data = storage.load_data()

    while True:
        display_header("HABIT TRACKER - TEAM TUPLE")
        display_menu(MENU_OPTIONS)
        choice = get_menu_choice(len(MENU_OPTIONS))

        if choice == 1:
            create_habit_flow(data)
        elif choice == 2:
            list_habits_flow(data)
        elif choice == 3:
            complete_habit_flow(data)
        elif choice == 4:
            analytics_flow(data)
        elif choice == 5:
            report_flow(data)
        elif choice == 6:
            chart_flow(data)
        elif choice == 7:
            delete_habit_flow(data)
        elif choice == 8:
            print("\n  Goodbye!")
            break

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    run_app()