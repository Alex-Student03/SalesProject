# Sales Data Summary

A small Python script that reads `messy_sales.csv`, filters records with missing required fields, and prints sales revenue totals by region.

## Requirements

- Python 3.8 or later

The script uses only Python's standard library; no extra packages are required.

## Run

Place `messy_sales.csv` in the same directory as `attempt1.py`, then run:

```powershell
python .\attempt1.py
```

## What it does

- Removes records with a missing `Date` or `Salesperson`.
- If other fields are missing, asks whether to remove those records as well. Press `y` or `yes` to remove them; any other response keeps them.
- Calculates revenue as `Quantity × Unit_Price` and prints totals by region.
- Excludes records with a missing or invalid `Quantity` or `Unit_Price` from the revenue totals. The `£` symbol and commas in numeric values are accepted.
- Trims region whitespace and normalizes capitalization when grouping totals.

The script prints a summary to the console and does not write or modify a data file.
