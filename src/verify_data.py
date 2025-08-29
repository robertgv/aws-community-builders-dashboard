#!/usr/bin/env python3
"""
Script to verify the combined CB data quality.
"""

import pandas as pd

def main():
    # Read the combined data
    print("Reading combined CB data...")
    df = pd.read_csv('../dashboard/data/anonymized_cb_data_2025.csv', sep=';')
    
    print(f"Total records: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Check for missing values
    print("\nMissing values:")
    print(df.isnull().sum())
    
    # Check unique values
    print(f"\nUnique categories: {len(df['category'].unique())}")
    print(f"Categories: {sorted(df['category'].unique())}")
    
    print(f"\nUnique cohorts: {len(df['cohort'].unique())}")
    print(f"Cohorts: {sorted(df['cohort'].unique())}")
    
    print(f"\nUnique countries: {len(df['country'].unique())}")
    
    print(f"\nUnique regions: {len(df['region'].unique())}")
    print(f"Regions: {sorted(df['region'].unique())}")
    
    # Check data distribution by year
    print("\nData distribution by cohort:")
    print(df['cohort'].value_counts().sort_index())
    
    # Check for Spain consistency
    spain_entries = df[df['country'] == 'Spain']
    print(f"\nSpain entries: {len(spain_entries)}")
    if len(spain_entries) > 0:
        print("Spain cohorts:", sorted(spain_entries['cohort'].unique()))
        print("Spain categories:", sorted(spain_entries['category'].unique()))

if __name__ == "__main__":
    main()