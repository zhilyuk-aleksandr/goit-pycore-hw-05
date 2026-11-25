import argparse
from collections import Counter
from datetime import datetime
from pathlib import Path


LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def parse_log_line(line: str) -> dict[str, str]:
    """Розбирає рядок формату YYYY-MM-DD HH:MM:SS LEVEL повідомлення."""
    parts = line.strip().split(maxsplit=3)
    if len(parts) != 4:
        raise ValueError("очікується дата, час, рівень і повідомлення")

    date, time, level, message = parts
    try:
        datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
    except ValueError as error:
        raise ValueError("очікується дійсна дата й час у форматі YYYY-MM-DD HH:MM:SS") from error
    if level not in LOG_LEVELS:
        raise ValueError(f"невідомий рівень логування {level!r}")

    return {"date": date, "time": time, "level": level, "message": message}


def load_logs(file_path: str | Path) -> list[dict[str, str]]:
    logs = []
    with Path(file_path).open(encoding="utf-8") as source:
        for number, line in enumerate(source, start=1):
            if not line.strip():
                continue
            try:
                logs.append(parse_log_line(line))
            except ValueError as error:
                raise ValueError(f"рядок {number}: {error}") from error
    return logs


def filter_logs_by_level(logs: list[dict[str, str]], level: str) -> list[dict[str, str]]:
    level = level.upper()
    return [log for log in logs if log["level"] == level]


def count_logs_by_level(logs: list[dict[str, str]]) -> dict[str, int]:
    return dict(Counter(log["level"] for log in logs))


def display_log_counts(counts: dict[str, int]) -> None:
    level_header = "Рівень логування"
    count_header = "Кількість"
    level_width = len(level_header)
    count_width = len(count_header)

    print(f"{level_header} | {count_header}")
    print(f"{'-' * (level_width + 1)}+-{'-' * count_width}")
    for level, count in counts.items():
        print(f"{level:<{level_width}} | {count:>{count_width}}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Підрахунок рівнів логування у файлі.")
    parser.add_argument("path", type=Path, help="шлях до файлу логів")
    parser.add_argument("level", nargs="?", type=str.upper, choices=LOG_LEVELS, help="рівень для фільтрації")
    args = parser.parse_args()

    try:
        logs = load_logs(args.path)
    except (OSError, ValueError) as error:
        parser.error(f"Не вдалося прочитати файл {args.path}: {error}")

    display_log_counts(count_logs_by_level(logs))
    if args.level:
        print(f"\nДеталі логів для рівня {args.level}:")
        filtered_logs = filter_logs_by_level(logs, args.level)
        if not filtered_logs:
            print("Записів немає.")
        for log in filtered_logs:
            print(f"{log['date']} {log['time']} — {log['message']}")


if __name__ == "__main__":
    main()
