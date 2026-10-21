import csv
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path


def is_missing(value):
    return value is None or not value.strip()


def parse_number(value):
    if is_missing(value):
        return None

    try:
        return Decimal(value.strip().replace("£", "").replace(",", ""))
    except InvalidOperation:
        return None


def main():
    csv_path = Path(__file__).with_name("messy_sales.csv")

    with csv_path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise ValueError(f"{csv_path.name} does not have a header row.")

        rows = list(reader)

    required_fields = {"Date", "Salesperson"}
    missing_required_rows = [
        row
        for row in rows
        if any(is_missing(row.get(field)) for field in required_fields)
    ]
    retained_rows = [
        row
        for row in rows
        if not any(is_missing(row.get(field)) for field in required_fields)
    ]

    other_missing_rows = [
        row
        for row in retained_rows
        if any(
            is_missing(value)
            for field, value in row.items()
            if field not in required_fields
        )
    ]

    if other_missing_rows:
        missing_fields = sorted(
            {
                field
                for row in other_missing_rows
                for field, value in row.items()
                if field not in required_fields and is_missing(value)
            }
        )
        answer = input(
            f"Found {len(other_missing_rows)} record(s) with missing "
            f"other fields ({', '.join(missing_fields)}). "
            "Remove those records too? [y/N] "
        )
        if answer.strip().lower() in {"y", "yes"}:
            retained_rows = [
                row
                for row in retained_rows
                if not any(
                    is_missing(value)
                    for field, value in row.items()
                    if field not in required_fields
                )
            ]

    totals_by_region = defaultdict(Decimal)
    excluded_from_totals = 0
    for row in retained_rows:
        quantity = parse_number(row.get("Quantity"))
        unit_price = parse_number(row.get("Unit_Price"))
        if quantity is None or unit_price is None:
            excluded_from_totals += 1
            continue

        region = (row.get("Region") or "").strip().title() or "(Missing region)"
        totals_by_region[region] += quantity * unit_price

    print(
        f"Removed {len(missing_required_rows)} record(s) with missing "
        "Date or Salesperson."
    )
    print("Sales revenue by region:")
    for region in sorted(totals_by_region):
        print(f"{region}: {totals_by_region[region]:,.2f}")
    if excluded_from_totals:
        print(
            f"Excluded {excluded_from_totals} record(s) from totals due to "
            "missing or invalid Quantity or Unit_Price."
        )


if __name__ == "__main__":
    main()
