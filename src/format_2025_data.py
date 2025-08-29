#!/usr/bin/env python3
"""
Script to format the 2025 CB data to match the 2024 format.
"""

import pandas as pd
import re

# Country name mappings to standardize inconsistencies
COUNTRY_MAPPINGS = {
    # Remove country codes in parentheses and standardize names
    'India (IN)': 'India',
    'United States of America (US)': 'USA',
    'United States of America': 'USA',
    'Germany (DE)': 'Germany',
    'Nepal (NP)': 'Nepal',
    'France (FR)': 'France',
    'Nigeria (NG)': 'Nigeria',
    'United Arab Emirates (AE)': 'United Arab Emirates',
    'Spain (ES)': 'Spain',
    'Italy (IT)': 'Italy',
    'United Kingdom of Great Britain and Northern Ireland (GB)': 'UK',
    'United Kingdom of Great Britain and Northern Ireland': 'UK',
    'Philippines (PH)': 'Philippines',
    'Pakistan (PK)': 'Pakistan',
    'Egypt (EG)': 'Egypt',
    'Malaysia (MY)': 'Malaysia',
    'Canada (CA)': 'Canada',
    'Australia (AU)': 'Australia',
    'Bangladesh (BD)': 'Bangladesh',
    'Japan (JP)': 'Japan',
    'Indonesia (ID)': 'Indonesia',
    'Qatar (QA)': 'Qatar',
    'Kenya (KE)': 'Kenya',
    'Kazakhstan (KZ)': 'Kazakhstan',
    'Ukraine (UA)': 'Ukraine',
    'Israel (IL)': 'Israel',
    'Serbia (RS)': 'Serbia',
    'Romania (RO)': 'Romania',
    'Mexico (MX)': 'Mexico',
    'Poland (PL)': 'Poland',
    'Brazil (BR)': 'Brazil',
    'Portugal (PT)': 'Portugal',
    'Sweden (SE)': 'Sweden',
    'New Zealand (NZ)': 'New Zealand',
    'Hong Kong (HK)': 'Hong Kong',
    'Viet Nam (VN)': 'Viet Nam',
    'Switzerland (CH)': 'Switzerland',
    'Sri Lanka (LK)': 'Sri Lanka',
    'Republic of Korea (KR)': 'South Korea',
    'Thailand (TH)': 'Thailand',
    'Angola (AO)': 'Angola',
    'Armenia (AM)': 'Armenia',
    'Netherlands (NL)': 'Netherlands',
    'Panama (PA)': 'Panama',
    'Guatemala (GT)': 'Guatemala',
    'Norway (NO)': 'Norway',
    'Chile (CL)': 'Chile',
    'Bolivia (BO)': 'Bolivia',
    'Uganda (UG)': 'Uganda',
    'Ghana (GH)': 'Ghana',
    'Colombia (CO)': 'Colombia',
    'Argentina (AR)': 'Argentina',
    'Belgium (BE)': 'Belgium',
    'Myanmar (MM)': 'Myanmar',
    'Singapore (SG)': 'Singapore',
    'South Africa (ZA)': 'South Africa',
    'Ireland (IE)': 'Ireland',
    'China (CN)': 'China',
    'Uruguay (UY)': 'Uruguay',
    'Georgia (GE)': 'Georgia',
    'Cameroon (CM)': 'Cameroon',
    'Ecuador (EC)': 'Ecuador',
    'Zimbabwe (ZW)': 'Zimbabwe',
    'El Salvador (SV)': 'El Salvador',
    'Saudi Arabia (SA)': 'Saudi Arabia',
    'Oman (OM)': 'Oman',
    'Bosnia and Herzegovina (BA)': 'Bosnia and Herzegovina',
    'Latvia (LV)': 'Latvia',
    'Lithuania (LT)': 'Lithuania',
    'Uzbekistan (UZ)': 'Uzbekistan',
    'Albania (AL)': 'Albania',
    'Hong Kong (S.A.R.)': 'Hong Kong',
    'Peru (PE)': 'Peru',
    'Tunisia (TN)': 'Tunisia',
    'Lebanon (LB)': 'Lebanon',
    'Slovenia (SI)': 'Slovenia',
    'T√ºrkiye / Turkey (TR)': 'Turkey',
    'Hungary (HU)': 'Hungary',
    'Senegal (SN)': 'Senegal',
    'Malta (MT)': 'Malta',
    'Congo (CD)': 'Congo',
    'Morocco (MA)': 'Morocco',
    'Cyprus (CY)': 'Cyprus',
    'Luxembourg (LU)': 'Luxembourg',
    'Finland (FI)': 'Finland',
    'San Marino (SM)': 'San Marino',
    'Montenegro (ME)': 'Montenegro',
    'Taiwan (TW)': 'Taiwan',
    'Palestinian Territory': 'Palestine'
}

# Region mappings based on the 2024 data patterns
REGION_MAPPINGS = {
    'Australia': 'APJ',
    'Bangladesh': 'APJ',
    'Cambodia': 'APJ',
    'India': 'APJ',
    'Indonesia': 'APJ',
    'Japan': 'APJ',
    'Malaysia': 'APJ',
    'Myanmar': 'APJ',
    'Nepal': 'APJ',
    'New Zealand': 'APJ',
    'Pakistan': 'APJ',
    'Philippines': 'APJ',
    'Singapore': 'APJ',
    'South Korea': 'APJ',
    'Sri Lanka': 'APJ',
    'Thailand': 'APJ',
    'Viet Nam': 'APJ',
    
    'Austria': 'EMEA',
    'Bahrain': 'EMEA',
    'Belarus': 'EMEA',
    'Belgium': 'EMEA',
    'Benin': 'EMEA',
    'Bosnia and Herzegovina': 'EMEA',
    'Bulgaria': 'EMEA',
    'Cameroon': 'EMEA',
    'Cyprus': 'EMEA',
    'Czech Republic': 'EMEA',
    'Denmark': 'EMEA',
    'Egypt': 'EMEA',
    'Estonia': 'EMEA',
    'Finland': 'EMEA',
    'France': 'EMEA',
    'Germany': 'EMEA',
    'Ghana': 'EMEA',
    'Hungary': 'EMEA',
    'Iraq': 'EMEA',
    'Ireland': 'EMEA',
    'Israel': 'EMEA',
    'Italy': 'EMEA',
    'Jordan': 'EMEA',
    'Kazakhstan': 'EMEA',
    'Kenya': 'EMEA',
    'Latvia': 'EMEA',
    'Lebanon': 'EMEA',
    'Lithuania': 'EMEA',
    'Macedonia': 'EMEA',
    'Montenegro': 'EMEA',
    'Morocco': 'EMEA',
    'Mozambique': 'EMEA',
    'Netherlands': 'EMEA',
    'Nigeria': 'EMEA',
    'Norway': 'EMEA',
    'Oman': 'EMEA',
    'Palestine': 'EMEA',
    'Poland': 'EMEA',
    'Portugal': 'EMEA',
    'Qatar': 'EMEA',
    'Romania': 'EMEA',
    'Russian Federation': 'EMEA',
    'Saudi Arabia': 'EMEA',
    'Serbia': 'EMEA',
    'South Africa': 'EMEA',
    'Spain': 'EMEA',
    'Sweden': 'EMEA',
    'Switzerland': 'EMEA',
    'Turkey': 'EMEA',
    'UK': 'EMEA',
    'Ukraine': 'EMEA',
    'United Arab Emirates': 'EMEA',
    'Zimbabwe': 'EMEA',
    
    'Hong Kong': 'GCR',
    'Taiwan': 'GCR',
    'China': 'GCR',
    
    'Argentina': 'LATAM',
    'Barbados': 'LATAM',
    'Bolivia': 'LATAM',
    'Brazil': 'LATAM',
    'Chile': 'LATAM',
    'Colombia': 'LATAM',
    'Costa Rica': 'LATAM',
    'Ecuador': 'LATAM',
    'El Salvador': 'LATAM',
    'Guatemala': 'LATAM',
    'Mexico': 'LATAM',
    'Nicaragua': 'LATAM',
    'Panama': 'LATAM',
    'Peru': 'LATAM',
    'Uruguay': 'LATAM',
    
    'Bahamas': 'NAMER',
    'Canada': 'NAMER',
    'USA': 'NAMER',
    
    # Additional countries found in 2025 data
    'Armenia': 'EMEA',
    'Mauritius': 'EMEA',
    'Uganda': 'EMEA',
    'Greece': 'EMEA',
    'Angola': 'EMEA',
    'Georgia': 'EMEA',
    'Belize': 'LATAM',
    'Tunisia': 'EMEA',
    'Uzbekistan': 'EMEA',
    'Slovenia': 'EMEA',
    'Slovakia': 'EMEA',
    'Senegal': 'EMEA',
    'Palestinian Territory': 'EMEA',
    'Malta': 'EMEA',
    'Congo': 'EMEA',
    'Albania': 'EMEA',
    'Algeria': 'EMEA',
    'Luxembourg': 'EMEA',
    'San Marino': 'EMEA',
    'Republic of Moldova': 'EMEA',
}

# Category mappings to standardize naming
CATEGORY_MAPPINGS = {
    'AI Engineering': 'Machine Learning & GenAI',
    'Machine Learning': 'Machine Learning & GenAI',
    'Network C&D': 'Networking & Content Delivery',
    'Security': 'Security & Identity',
    'Cloud Operations': 'Cloud Operations',
    'Containers': 'Containers',
    'Data': 'Data',
    'Dev Tools': 'Dev Tools',
    'Serverless': 'Serverless',
}

def clean_country_name(country):
    """Clean and standardize country names."""
    if country in COUNTRY_MAPPINGS:
        return COUNTRY_MAPPINGS[country]
    return country

def get_region(country):
    """Get region for a country."""
    return REGION_MAPPINGS.get(country, 'UNKNOWN')

def clean_category(category):
    """Clean and standardize category names."""
    return CATEGORY_MAPPINGS.get(category, category)

def main():
    # Read the 2025 original data
    print("Reading 2025 original data...")
    # The file has semicolon header but comma-separated data, so we need to handle this
    with open('../dashboard/data/anonymized_cb_data_2025_original.csv', 'r') as f:
        lines = f.readlines()
    
    # Fix the header to use commas
    lines[0] = lines[0].replace(';', ',')
    
    # Write to a temporary file
    with open('temp_2025.csv', 'w') as f:
        f.writelines(lines)
    
    df_2025 = pd.read_csv('temp_2025.csv')
    
    print(f"Original data shape: {df_2025.shape}")
    print(f"Original columns: {df_2025.columns.tolist()}")
    
    # Clean the data
    print("Cleaning data...")
    
    # Clean country names
    df_2025['country'] = df_2025['country'].apply(clean_country_name)
    
    # Clean categories
    # df_2025['category'] = df_2025['category'].apply(clean_category)
    
    # Fix specific category issues
    df_2025 = df_2025[df_2025['category'] != 'A']  # Remove invalid entries
    
    # Add region column
    df_2025['region'] = df_2025['country'].apply(get_region)
    
    # Reorder columns to match 2024 format
    df_2025 = df_2025[['category', 'cohort', 'country', 'region']]
    
    # Check for unknown regions
    unknown_regions = df_2025[df_2025['region'] == 'UNKNOWN']
    if not unknown_regions.empty:
        print(f"Warning: Found {len(unknown_regions)} rows with unknown regions:")
        print(unknown_regions['country'].unique())
    
    # Save the cleaned data
    output_file = '../dashboard/data/anonymized_cb_data_2025.csv'
    print(f"Saving cleaned data to {output_file}...")
    df_2025.to_csv(output_file, sep=';', index=False)
    
    print(f"Cleaned data shape: {df_2025.shape}")
    print(f"Final columns: {df_2025.columns.tolist()}")
    
    # Show some statistics
    print("\nData summary:")
    print(f"Categories: {sorted(df_2025['category'].unique())}")
    print(f"Cohorts: {sorted(df_2025['cohort'].unique())}")
    print(f"Countries: {len(df_2025['country'].unique())} unique countries")
    print(f"Regions: {sorted(df_2025['region'].unique())}")
    
    print("\nFirst few rows of cleaned data:")
    print(df_2025.head())
    
    # Clean up temporary file
    import os
    if os.path.exists('temp_2025.csv'):
        os.remove('temp_2025.csv')

if __name__ == "__main__":
    main()