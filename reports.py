from __future__ import annotations

import os
import tempfile
from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "mpl_config")
)

def parse_date(value: Any) -> date | None:

    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        return None
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        return None


class ChartStrategy(ABC):

    @abstractmethod
    def render(self, data: Any, **kwargs: Any) -> Any:
        """Render the chart given data and options."""
        pass


class TextChartStrategy(ChartStrategy):

    def render(self, data: Any, **kwargs: Any) -> str:
        if not data:
            return "No data to display"

        # Normalize data to a list of (label, int_val)
        items: list[tuple[str, int]] = []
        if isinstance(data, dict):
            for k, v in data.items():
                try:
                    val = max(0, int(v))
                except (ValueError, TypeError):
                    val = 0
                items.append((str(k), val))
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, tuple) and len(item) == 2:
                    k, v = item
                    try:
                        val = max(0, int(v))
                    except (ValueError, TypeError):
                        val = 0
                    items.append((str(k), val))
                elif isinstance(item, dict) and "name" in item:
                    # Habit dict
                    label = f"{item.get('name', 'Habit')} ({item.get('id', '')})"
                    dates = item.get("completed_dates", [])
                    val = len(dates) if isinstance(dates, list) else 0
                    items.append((label, val))

        if not items:
            return "No data to display"

        max_val = max(val for _, val in items)
        max_label_len = max(len(label) for label, _ in items)
        max_bar_len = 40

        lines: list[str] = []
        for label, val in items:
            padded_label = label.ljust(max_label_len)
            if val == 0 or max_val == 0:
                bar = ""
            else:
                bar_len = max(1, int((val / max_val) * max_bar_len))
                bar = "#" * bar_len
            lines.append(f"{padded_label} | {bar} ({val})")

        return "\n".join(lines)


class ImageChartStrategy(ChartStrategy):
    def render(
        self,
        data: Any,
        file_path: str = "chart.png",
        title: str = "Habit completion - last 7 days",
        **kwargs: Any,
    ) -> bool:
        target_path = Path(file_path)
        parent = target_path.parent
        if not parent.exists():
            return False

        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt

            # Extract labels and values
            labels: list[str] = []
            values: list[int] = []

            if isinstance(data, dict):
                for k, v in data.items():
                    labels.append(str(k))
                    values.append(int(v) if isinstance(v, (int, float)) else 0)
            elif isinstance(data, list):
                for idx, item in enumerate(data):
                    if isinstance(item, dict):
                        h_name = item.get("name", f"Habit {idx+1}")
                        h_id = item.get("id", "")
                        labels.append(f"{h_name} ({h_id})")
                        d_list = item.get("completed_dates", [])
                        values.append(len(d_list) if isinstance(d_list, list) else 0)
                    elif isinstance(item, tuple) and len(item) == 2:
                        labels.append(str(item[0]))
                        values.append(int(item[1]))

            if not labels:
                labels = ["No Habits"]
                values = [0]

            fig, ax = plt.subplots(figsize=(8, 4.5))
            bars = ax.barh(labels, values, color="teal")
            ax.set_xlabel("Completions")
            ax.set_title(title)
            plt.tight_layout()

            fig.savefig(str(target_path), dpi=150)
            plt.close(fig)
            return True
        except Exception:
            return False


def text_chart(data: Any) -> str:
    strategy = TextChartStrategy()
    return strategy.render(data)


def save_chart_image(
    data: Any,
    file_path: str,
    title: str = "Habit completion - last 7 days",
) -> bool:
    strategy = ImageChartStrategy()
    return strategy.render(data, file_path=file_path, title=title)


def build_report(data: dict[str, Any], today: date | None = None) -> str:
    if today is None:
        today = date.today()

    seven_days_ago = today - timedelta(days=6)

    if not isinstance(data, dict) or not data.get("habits"):
        return "Habit Tracker Summary Report\nNo habits tracked."

    habits_list = data.get("habits", [])
    lines: list[str] = [
        "=" * 50,
        "HABIT TRACKER SUMMARY REPORT",
        f"Generated on: {today.isoformat()}",
        f"Total Habits Tracked: {len(habits_list)}",
        "=" * 50,
    ]

    for habit in habits_list:
        if not isinstance(habit, dict):
            continue

        h_id = habit.get("id", "unknown")
        h_name = habit.get("name", "Unnamed Habit")
        raw_dates = habit.get("completed_dates", [])

        valid_dates: set[date] = set()
        if isinstance(raw_dates, list):
            for d in raw_dates:
                parsed = parse_date(d)
                if parsed and parsed <= today:
                    valid_dates.add(parsed)

        total_days = len(valid_dates)
        last_7_days = sum(
            1 for d in valid_dates if seven_days_ago <= d <= today
        )

        lines.append(
            f"Habit [{h_id}] {h_name}: "
            f"{total_days} days in total and {last_7_days} in the last 7 days"
        )

    lines.append("=" * 50)
    return "\n".join(lines)


def save_report(report_text: str, file_path: str) -> bool:
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            f.write(report_text)
        return True
    except Exception:
        return False


def generate_summary_report(data: dict[str, Any]) -> str:
    return build_report(data)


def generate_chart(data: Any, output_path: str = "chart.png") -> None:
    save_chart_image(data, output_path)