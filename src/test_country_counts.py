#!/usr/bin/env python3
"""
Test script to verify that country counts are calculated correctly from CB data.
"""

import pandas as pd
from pathlib import Path

def main():
    print("Testing country count calculation...")
    
    # Read CB data
    df = pd.read_csv('../dashboard/data/anonymized_cb_data_2025.csv', delimiter=';')
    print(f"Total CB records: {len(df)}")
    
    # Read countries metadata (GPS coordinates only)
    df_countries_metadata = pd.read_csv('../dashboard/data/countries.csv', delimiter=';')
    print(f"Countries with GPS metadata: {len(df_countries_metadata)}")
    
    # Calculate country counts from CB data
    df_country_counts = (
        df.groupby("country")
        .size()
        .reset_index(name="count")
    )
    print(f"Countries with CB members: {len(df_country_counts)}")
    
    # Merge GPS coordinates with calculated counts
    df_countries = df_countries_metadata.merge(
        df_country_counts, 
        on="country", 
        how="inner"  # Only include countries that have CB members
    )
    print(f"Countries with both GPS and CB data: {len(df_countries)}")
    
    # Show top 10 countries by member count
    print("\nTop 10 countries by member count:")
    top_countries = df_countries.sort_values('count', ascending=False).head(10)
    for _, row in top_countries.iterrows():
        print(f"  {row['country']}: {row['count']} members")
    
    # Check for countries with CB data but no GPS coordinates
    cb_countries = set(df_country_counts['country'])
    gps_countries = set(df_countries_metadata['country'])
    missing_gps = cb_countries - gps_countries
    
    if missing_gps:
        print(f"\nWarning: {len(missing_gps)} countries have CB members but no GPS coordinates:")
        for country in sorted(missing_gps):
            count = df_country_counts[df_country_counts['country'] == country]['count'].iloc[0]
            print(f"  {country}: {count} members")
    else:
        print("\n✅ All countries with CB members have GPS coordinates!")
    
    print(f"\nSummary:")
    print(f"- Total CB records: {len(df)}")
    print(f"- Countries with CB members: {len(df_country_counts)}")
    print(f"- Countries with GPS metadata: {len(df_countries_metadata)}")
    print(f"- Countries ready for map display: {len(df_countries)}")

if __name__ == "__main__":
    main()