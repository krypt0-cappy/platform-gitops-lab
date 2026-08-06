import csv
from pathlib import Path
from typing import Any


def write_csv(
    rows: list[dict[str, Any]],
    fieldnames: list[str],
    output_path: Path,
) -> None:
    """Write normalized inventory records to a CSV file."""
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        mode="w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV written to: {output_path}")
