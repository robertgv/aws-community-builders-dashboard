#!/usr/bin/env python3
"""
Script to update countries.csv to only contain metadata (GPS coordinates)
and identify any missing countries from the CB data.
"""

import pandas as pd

def main():
    # Read the CB data to get all countries
    print("Reading CB data...")
    df_cb = pd.read_csv('../dashboard/data/anonymized_cb_data_2025.csv', sep=';')
    cb_countries = set(df_cb['country'].unique())
    print(f"Countries in CB data: {len(cb_countries)}")
    
    # Read the current countries metadata
    print("Reading countries metadata...")
    df_countries = pd.read_csv('../dashboard/data/countries_temp.csv', sep=';')
    metadata_countries = set(df_countries['country'].unique())
    print(f"Countries in metadata: {len(metadata_countries)}")
    
    # Find missing countries
    missing_countries = cb_countries - metadata_countries
    extra_countries = metadata_countries - cb_countries
    
    print(f"\nCountries in CB data but missing from metadata: {len(missing_countries)}")
    if missing_countries:
        print("Missing countries:", sorted(missing_countries))
    
    print(f"\nCountries in metadata but not in CB data: {len(extra_countries)}")
    if extra_countries:
        print("Extra countries:", sorted(extra_countries))
    
    # Add approximate GPS coordinates for missing countries
    # These are rough center coordinates - in a real scenario you'd want more precise data
    missing_coords = {
        'Angola': (-11.2027, 17.8739),
        'Albania': (41.1533, 20.1683),
        'Luxembourg': (49.8153, 6.1296),
        'Slovenia': (46.1512, 14.9955),
        'Lithuania': (55.1694, 23.8813),
        'San Marino': (43.9424, 12.4578),
        'Congo': (-4.0383, 21.7587),
        'Senegal': (14.4974, -14.4524),
        'Bolivia': (-16.2902, -63.5887),
        'Uganda': (1.3733, 32.2903),
        'Palestinian Territory': (31.9522, 35.2332),
    }
    
    # Add missing countries to the dataframe
    new_rows = []
    for country in missing_countries:
        if country in missing_coords:
            lat, lon = missing_coords[country]
            new_rows.append({
                'country': country,
                'latitud': lat,
                'longitud': lon
            })
        else:
            print(f"Warning: No GPS coordinates available for {country}")
    
    if new_rows:
        df_new = pd.DataFrame(new_rows)
        df_countries = pd.concat([df_countries, df_new], ignore_index=True)
        df_countries = df_countries.sort_values('country')
    
    # Save the updated countries metadata
    print(f"\nSaving updated countries metadata with {len(df_countries)} countries...")
    df_countries.to_csv('../dashboard/data/countries.csv', sep=';', index=False)
    
    print("Countries metadata updated successfully!")
    print("The countries.csv file now contains only GPS coordinates.")
    print("Country counts will be calculated dynamically from the CB data.")

if __name__ == "__main__":
    main()