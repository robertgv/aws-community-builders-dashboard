#!/usr/bin/env python3
"""
Format the 2026 CB export into the dashboard CSV schema.
"""

import csv
import re
from collections import Counter
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT_DIR / "dashboard/data/anonymized_cb_data_2026_original.csv"
OUTPUT_FILE = ROOT_DIR / "dashboard/data/anonymized_cb_data_2026.csv"

UNKNOWN_COUNTRY = "Unknown"
UNKNOWN_REGION = "Unknown"

COUNTRY_CODE_MAPPINGS = {
    "BA": "Bosnia and Herzegovina",
    "CD": "Congo",
    "CI": "Cote d'Ivoire",
    "CZ": "Czech Republic",
    "GB": "UK",
    "MK": "Macedonia",
    "MM": "Myanmar",
    "PS": "Palestine",
    "TR": "Turkey",
    "US": "USA",
    "VN": "Viet Nam",
}

COUNTRY_NAME_MAPPINGS = {
    "Bosnia & Herzegovina": "Bosnia and Herzegovina",
    "Congo - Kinshasa": "Congo",
    "Czechia": "Czech Republic",
    "Myanmar (Burma)": "Myanmar",
    "North Macedonia": "Macedonia",
    "Türkiye": "Turkey",
    "United Kingdom": "UK",
    "United States": "USA",
    "Vietnam": "Viet Nam",
}

REGION_MAPPINGS = {
    "Afghanistan": "APJ",
    "Australia": "APJ",
    "Bangladesh": "APJ",
    "Cambodia": "APJ",
    "India": "APJ",
    "Indonesia": "APJ",
    "Japan": "APJ",
    "Malaysia": "APJ",
    "Myanmar": "APJ",
    "Nepal": "APJ",
    "New Zealand": "APJ",
    "Pakistan": "APJ",
    "Philippines": "APJ",
    "Singapore": "APJ",
    "South Korea": "APJ",
    "Sri Lanka": "APJ",
    "Thailand": "APJ",
    "Viet Nam": "APJ",
    "Albania": "EMEA",
    "Algeria": "EMEA",
    "Angola": "EMEA",
    "Armenia": "EMEA",
    "Austria": "EMEA",
    "Azerbaijan": "EMEA",
    "Bahrain": "EMEA",
    "Belarus": "EMEA",
    "Belgium": "EMEA",
    "Benin": "EMEA",
    "Bosnia and Herzegovina": "EMEA",
    "Bulgaria": "EMEA",
    "Cameroon": "EMEA",
    "Congo": "EMEA",
    "Cote d'Ivoire": "EMEA",
    "Croatia": "EMEA",
    "Cyprus": "EMEA",
    "Czech Republic": "EMEA",
    "Denmark": "EMEA",
    "Egypt": "EMEA",
    "Estonia": "EMEA",
    "Finland": "EMEA",
    "France": "EMEA",
    "Georgia": "EMEA",
    "Germany": "EMEA",
    "Ghana": "EMEA",
    "Greece": "EMEA",
    "Hungary": "EMEA",
    "Iceland": "EMEA",
    "Iraq": "EMEA",
    "Ireland": "EMEA",
    "Israel": "EMEA",
    "Italy": "EMEA",
    "Jordan": "EMEA",
    "Kazakhstan": "EMEA",
    "Kenya": "EMEA",
    "Latvia": "EMEA",
    "Lebanon": "EMEA",
    "Lithuania": "EMEA",
    "Luxembourg": "EMEA",
    "Macedonia": "EMEA",
    "Malta": "EMEA",
    "Mauritius": "EMEA",
    "Montenegro": "EMEA",
    "Morocco": "EMEA",
    "Netherlands": "EMEA",
    "Nigeria": "EMEA",
    "Norway": "EMEA",
    "Palestine": "EMEA",
    "Poland": "EMEA",
    "Portugal": "EMEA",
    "Romania": "EMEA",
    "Rwanda": "EMEA",
    "Saudi Arabia": "EMEA",
    "Senegal": "EMEA",
    "Serbia": "EMEA",
    "Slovakia": "EMEA",
    "Slovenia": "EMEA",
    "South Africa": "EMEA",
    "Spain": "EMEA",
    "Sweden": "EMEA",
    "Switzerland": "EMEA",
    "Togo": "EMEA",
    "Tunisia": "EMEA",
    "Turkey": "EMEA",
    "UK": "EMEA",
    "Uganda": "EMEA",
    "Ukraine": "EMEA",
    "United Arab Emirates": "EMEA",
    "Uzbekistan": "EMEA",
    "Zambia": "EMEA",
    "Zimbabwe": "EMEA",
    "China": "GCR",
    "Hong Kong": "GCR",
    "Taiwan": "GCR",
    "Argentina": "LATAM",
    "Bolivia": "LATAM",
    "Brazil": "LATAM",
    "Chile": "LATAM",
    "Colombia": "LATAM",
    "Costa Rica": "LATAM",
    "Ecuador": "LATAM",
    "El Salvador": "LATAM",
    "Guatemala": "LATAM",
    "Mexico": "LATAM",
    "Panama": "LATAM",
    "Paraguay": "LATAM",
    "Peru": "LATAM",
    "Uruguay": "LATAM",
    "Canada": "NAMER",
    "USA": "NAMER",
    UNKNOWN_COUNTRY: UNKNOWN_REGION,
}

CATEGORY_MAPPINGS = {
    "Networking and Content Delivery": "Network C&D",
}


def clean_category(category):
    category = (category or "").strip()
    return CATEGORY_MAPPINGS.get(category, category)


def clean_country(country):
    country = (country or "").strip()
    if country in {"", "-", "\u2014"}:
        return UNKNOWN_COUNTRY

    code_first = re.fullmatch(r"([A-Z]{2}) \((.*)\)", country)
    if code_first:
        code, name = code_first.groups()
        country = COUNTRY_CODE_MAPPINGS.get(code, name)

    country = COUNTRY_NAME_MAPPINGS.get(country, country)
    return country


def get_region(country):
    return REGION_MAPPINGS.get(country, "UNKNOWN")


def main():
    with INPUT_FILE.open(newline="", encoding="utf-8-sig") as input_file:
        reader = csv.DictReader(input_file)
        source_rows = list(reader)

    output_rows = []
    skipped_rows = Counter()

    for row in source_rows:
        category = clean_category(row.get("CB Category") or row.get("category"))
        cohort = (row.get("Cohort") or row.get("cohort") or "").strip()
        country = clean_country(row.get("Country") or row.get("country"))

        if not category or category == "A":
            skipped_rows["invalid_category"] += 1
            continue
        if not cohort:
            skipped_rows["missing_cohort"] += 1
            continue

        output_rows.append(
            {
                "category": category,
                "cohort": cohort,
                "country": country,
                "region": get_region(country),
            }
        )

    unknown_regions = sorted(
        {row["country"] for row in output_rows if row["region"] == "UNKNOWN"}
    )
    if unknown_regions:
        raise SystemExit(
            "Missing region mappings for: " + ", ".join(unknown_regions)
        )

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(
            output_file,
            fieldnames=["category", "cohort", "country", "region"],
            delimiter=";",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Read {len(source_rows)} rows from {INPUT_FILE}")
    print(f"Wrote {len(output_rows)} rows to {OUTPUT_FILE}")
    if skipped_rows:
        print(f"Skipped rows: {dict(skipped_rows)}")
    unknown_country_rows = sum(
        row["country"] == UNKNOWN_COUNTRY for row in output_rows
    )
    print(f"Unknown country rows preserved: {unknown_country_rows}")
    print(f"Categories: {sorted({row['category'] for row in output_rows})}")
    print(f"Cohorts: {sorted({row['cohort'] for row in output_rows})}")
    print(f"Countries: {len({row['country'] for row in output_rows})}")
    print(f"Regions: {sorted({row['region'] for row in output_rows})}")


if __name__ == "__main__":
    main()
