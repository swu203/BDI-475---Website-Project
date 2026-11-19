#!/usr/bin/env python3
"""Make data/city_median_sale_price.json from data/college_town_home_sales.csv.

Rule: a sale counts only if sale_price is $10,000 or more. Sales under that are
left out of the median (see docs/data_description_sheet.md, "Some prices are impossible").

Run from the repository root:
    python3 scripts/make_city_median_prices.py
"""

import csv
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "college_town_home_sales.csv"
OUTPUT = ROOT / "data" / "city_median_sale_price.json"
MIN_PRICE = 10_000


def main() -> None:
    prices_by_city: dict[str, list[int]] = {}
    total_rows = 0
    kept_rows = 0

    with SOURCE.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total_rows += 1
            price_text = (row["sale_price"] or "").strip()
            if not price_text:
                continue
            price = int(price_text)
            if price < MIN_PRICE:
                continue
            kept_rows += 1
            prices_by_city.setdefault(row["city"].strip(), []).append(price)

    cities = [
        {
            "city": city,
            "median_sale_price": int(statistics.median(prices)),
            "sales": len(prices),
        }
        for city, prices in prices_by_city.items()
    ]
    cities.sort(key=lambda c: c["median_sale_price"], reverse=True)

    result = {
        "source": "data/college_town_home_sales.csv",
        "rule": f"Sales with sale_price of ${MIN_PRICE:,} or more",
        "rows_in_source": total_rows,
        "rows_used": kept_rows,
        "cities": cities,
    }

    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")

    print(f"Wrote {OUTPUT.relative_to(ROOT)}: {len(cities)} cities, {kept_rows} of {total_rows} rows used")


if __name__ == "__main__":
    main()
