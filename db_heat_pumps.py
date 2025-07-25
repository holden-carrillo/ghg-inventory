# -*- coding: utf-8 -*-
"""db.heat_pumps.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bySejPeQWIE-5ZWy_xFe3BMYdM90gqDb
"""

import pandas as pd
import numpy as np
import io
from itertools import product

from google.colab import drive
drive.mount('/content/drive')
single_family = pd.read_excel('/content/drive/MyDrive/ecodatalab/policy/data/heat pump/data/TECHWorkingDataset_Single-Family_2025-05-26.xlsx')
multi_family = pd.read_excel('/content/drive/MyDrive/ecodatalab/policy/data/heat pump/data/TECHWorkingDataset_Multifamily_2025-05-26.xlsx')
swapped_names = pd.read_csv(io.StringIO('''
PACIFIC PALISADES,Los Angeles
RESEDA,Los Angeles
SAN PEDRO,Los Angeles
SHERMAN OAKS,San Fernando
STUDIO CITY,Los Angeles
SUN CITY,Menifee
SYLMAR,Los Angeles
TARZANA,Los Angeles
TRABUCO CANYON,Other
TUJUNGA,Los Angeles
VAN NUYS,Los Angeles
VENICE,Los Angeles
VENTURA,San Buenaventura (Ventura)
WEST HILLS,Los Angeles
WOODLAND HILLS,Los Angeles
CARMEL,Carmel-by-the-Sea
CARMEL VALLEY,Carmel Valley Village
CHATSWORTH,Los Angeles
LOS  ANGELES,Los Angeles
Emerald Hills,Redwood City
Encino,Los Angeles
Granada Hills,Los Angeles
Greenbrae,Larkspur
Hillsborough,Hillsborough
La Jolla,San Diego
North Hills,Los Angeles
North Hollywood,Los Angeles
Northridge,Los Angeles
Canoga Park,Los Angeles
Winnetka,Los Angeles
San Luis Obisp,San Luis Obispo
Sun Valley,Los Angeles
Foothill Ranch,Lake Forest
Valencia,Santa Clarita
'''), header=None, names=['old', 'new'])

place_id = pd.read_csv('/content/drive/MyDrive/ecodatalab/policy/data/heat pump/data/place_id.csv')
single_family_filtered = single_family[(single_family['Total Project Cost ($)'] != "Removed during QA")]

single_family_filtered = single_family_filtered[[
    'Customer City',
    'Customer County',
    'Building Type',
    'Product Group',
    'Installation End Date',
    'Count Units Installed',
    'Total Project Cost ($)',
    'Total Project Cost per Unit ($)',
    'Ex Ante annual electricity savings (kWh)',
    'Ex Ante annual gas/propane savings (Therms)',
    'Ex Ante annual GHG savings (Metric tons CO2e)'
]]

single_family_filtered.loc[:, 'Installation End Date'] = pd.to_datetime(single_family_filtered['Installation End Date'], errors='coerce').dt.year

single_family_filtered['Count Units Installed'] = single_family_filtered['Count Units Installed'].astype(float)
single_family_filtered['Total Project Cost ($)'] = single_family_filtered['Total Project Cost ($)'].astype(float)
single_family_filtered['Total Project Cost per Unit ($)'] = single_family_filtered['Total Project Cost per Unit ($)'].astype(float)
single_family_filtered['Ex Ante annual electricity savings (kWh)'] = single_family_filtered['Ex Ante annual electricity savings (kWh)'].astype(float)
single_family_filtered['Ex Ante annual gas/propane savings (Therms)'] = single_family_filtered['Ex Ante annual gas/propane savings (Therms)'].astype(float)
single_family_filtered['Ex Ante annual GHG savings (Metric tons CO2e)'] = single_family_filtered['Ex Ante annual GHG savings (Metric tons CO2e)'].astype(float)
single_family_filtered['Customer City'] = single_family_filtered['Customer City'].str.title()

multi_family_filtered = multi_family[(multi_family['Total Project Cost ($)'] != "Removed during QA")]

multi_family_filtered = multi_family_filtered[[
    'Customer City',
    'Customer County',
    'Building Type',
    'Product Group',
    'Installation End Date',
    'Count Units Installed',
    'Total Project Cost ($)',
    'Total Project Cost per Unit ($)',
    'Ex Ante annual electricity savings (kWh)',
    'Ex Ante annual gas/propane savings (Therms)',
    'Ex Ante annual GHG savings (Metric tons CO2e)'
]]

multi_family_filtered.loc[:, 'Installation End Date'] = pd.to_datetime(multi_family_filtered['Installation End Date'], errors='coerce').dt.year

multi_family_filtered['Count Units Installed'] = multi_family_filtered['Count Units Installed'].astype(float)
multi_family_filtered['Total Project Cost ($)'] = multi_family_filtered['Total Project Cost ($)'].astype(float)
multi_family_filtered['Total Project Cost per Unit ($)'] = multi_family_filtered['Total Project Cost per Unit ($)'].astype(float)
multi_family_filtered['Ex Ante annual electricity savings (kWh)'] = multi_family_filtered['Ex Ante annual electricity savings (kWh)'].astype(float)
multi_family_filtered['Ex Ante annual gas/propane savings (Therms)'] = multi_family_filtered['Ex Ante annual gas/propane savings (Therms)'].astype(float)
multi_family_filtered['Ex Ante annual GHG savings (Metric tons CO2e)'] = multi_family_filtered['Ex Ante annual GHG savings (Metric tons CO2e)'].astype(float)
multi_family_filtered['Customer City'] = multi_family_filtered['Customer City'].str.title()

swapped_names['old'] = swapped_names['old'].str.strip().str.title()
swapped_names['new'] = swapped_names['new'].str.strip()
city_swap_dict = dict(zip(swapped_names['old'], swapped_names['new']))
heat_pumps = pd.concat([single_family_filtered, multi_family_filtered])

heat_pumps['Customer City'] = heat_pumps['Customer City'].str.strip().str.title()
heat_pumps['Customer City'] = heat_pumps['Customer City'].replace(city_swap_dict)

heat_pumps = heat_pumps.rename(columns={
    "Customer City": "location_name",
    "Customer County": "county",
    "Installation End Date": "year"
})

heat_pumps['location_name'] = heat_pumps['location_name'].replace({
    "Coto De Caza": "Coto de Caza",
    "Mcfarland": "McFarland",
    "Marina Del Rey": "Marina del Rey"
})

heat_pumps = heat_pumps[~heat_pumps['location_name'].isin(['Hillsborough', 'Jurupa Valley'])]
place_id = place_id.drop(167)

heat_pumps = heat_pumps.merge(place_id, how='left', left_on='location_name', right_on='place_name').reset_index(drop=True)

heat_pumps[['Ex Ante annual electricity savings (kWh)',
            'Ex Ante annual gas/propane savings (Therms)',
            'Ex Ante annual GHG savings (Metric tons CO2e)']] = \
    heat_pumps[['Ex Ante annual electricity savings (kWh)',
                'Ex Ante annual gas/propane savings (Therms)',
                'Ex Ante annual GHG savings (Metric tons CO2e)']].fillna(0)

group_cols = ['location_name', 'county', 'year', 'Building Type', 'Product Group']
agg = heat_pumps.groupby(group_cols, dropna=False).agg({
    'Count Units Installed': 'sum',
    'Total Project Cost ($)': 'sum',
    'Ex Ante annual electricity savings (kWh)': 'sum',
    'Ex Ante annual gas/propane savings (Therms)': 'sum',
    'Ex Ante annual GHG savings (Metric tons CO2e)': 'sum'
}).reset_index()

agg = agg.rename(columns={
    'Count Units Installed': 'units_installed',
    'Total Project Cost ($)': 'total_project_cost_usd',
    'Ex Ante annual electricity savings (kWh)': 'annual_electricity_savings_kwh',
    'Ex Ante annual gas/propane savings (Therms)': 'annual_gas_savings_therms',
    'Ex Ante annual GHG savings (Metric tons CO2e)': 'annual_ghg_savings_mtco2e',
})

agg['project_cost_per_unit_usd'] = agg['total_project_cost_usd'] / agg['units_installed']
agg['electricity_savings_per_unit_kwh'] = agg['annual_electricity_savings_kwh'] / agg['units_installed']
agg['gas_savings_per_unit_therms'] = agg['annual_gas_savings_therms'] / agg['units_installed']
agg['ghg_savings_per_unit_mtco2e'] = agg['annual_ghg_savings_mtco2e'] / agg['units_installed']

geo_info = heat_pumps[['location_name', 'geo_fips', 'state']].drop_duplicates(subset='location_name')
agg = agg.merge(geo_info, how='left', on='location_name')

county_info = place_id[['place_name', 'counties']].drop_duplicates()
agg = agg.merge(county_info, how='left', left_on='location_name', right_on='place_name')
agg['county'] = np.where(
    agg['geo_fips'].notna(),
    agg['counties'].str.split(',').str[0].str.strip(),
    agg['county']
)
agg = agg.drop(columns=['counties', 'place_name'])
agg['geography_type'] = 'location'

final_cols = [
    'geo_fips', 'location_name', 'county', 'state', 'geography_type', 'year', 'Building Type', 'Product Group',
    'units_installed', 'total_project_cost_usd', 'project_cost_per_unit_usd',
    'annual_electricity_savings_kwh', 'electricity_savings_per_unit_kwh',
    'annual_gas_savings_therms', 'gas_savings_per_unit_therms',
    'annual_ghg_savings_mtco2e', 'ghg_savings_per_unit_mtco2e'
]

agg = agg[final_cols]
agg = agg[agg['year'].notna()]
agg = agg.groupby([
    'geo_fips', 'location_name', 'county', 'state', 'geography_type', 'year', 'Building Type', 'Product Group'
], dropna=False).sum(numeric_only=True).reset_index()
agg = agg[agg['county'].notna()]

# Fill No Data Locations With 0
place_id['place_name'] = place_id['place_name'].str.strip().str.title()
place_id['state'] = place_id['state'].str.strip().str.title()

place_meta = place_id[['place_name', 'geo_fips', 'state', 'counties']].drop_duplicates()
place_meta['county'] = place_meta['counties'].str.split(',').str[0].str.strip()
place_meta['geography_type'] = 'location'
years = list(range(2021, 2026))
building_types = agg['Building Type'].dropna().unique()
product_groups = agg['Product Group'].dropna().unique()
locations = place_meta['place_name'].unique()

full_index = pd.MultiIndex.from_tuples(
    product(locations, years, building_types, product_groups),
    names=['location_name', 'year', 'Building Type', 'Product Group']
)
quant_cols = [
    'units_installed', 'total_project_cost_usd', 'project_cost_per_unit_usd',
    'annual_electricity_savings_kwh', 'electricity_savings_per_unit_kwh',
    'annual_gas_savings_therms', 'gas_savings_per_unit_therms',
    'annual_ghg_savings_mtco2e', 'ghg_savings_per_unit_mtco2e'
]
agg_collapsed = agg.groupby(['location_name', 'year', 'Building Type', 'Product Group'], dropna=False).sum(numeric_only=True).reset_index()

agg_collapsed = agg_collapsed.set_index(['location_name', 'year', 'Building Type', 'Product Group'])
agg_collapsed = agg_collapsed.reindex(full_index)
agg_collapsed[quant_cols] = agg_collapsed[quant_cols].fillna(0)
agg_collapsed = agg_collapsed.reset_index()

agg_final = agg_collapsed.merge(place_meta, how='left', left_on='location_name', right_on='place_name')
agg_final['geo_fips'] = agg_final['geo_fips_y']
final_cols = [
    'geo_fips', 'location_name', 'county', 'state', 'geography_type',
    'year', 'Building Type', 'Product Group'
] + quant_cols
agg_final = agg_final[final_cols]

# Add Counties
county_lookup = pd.DataFrame([
    (6001, 'Alameda County'), (6003, 'Alpine County'), (6005, 'Amador County'),
    (6007, 'Butte County'), (6009, 'Calaveras County'), (6011, 'Colusa County'),
    (6013, 'Contra Costa County'), (6015, 'Del Norte County'), (6017, 'El Dorado County'),
    (6019, 'Fresno County'), (6021, 'Glenn County'), (6023, 'Humboldt County'),
    (6025, 'Imperial County'), (6027, 'Inyo County'), (6029, 'Kern County'),
    (6031, 'Kings County'), (6033, 'Lake County'), (6035, 'Lassen County'),
    (6037, 'Los Angeles County'), (6039, 'Madera County'), (6041, 'Marin County'),
    (6043, 'Mariposa County'), (6045, 'Mendocino County'), (6047, 'Merced County'),
    (6049, 'Modoc County'), (6051, 'Mono County'), (6053, 'Monterey County'),
    (6055, 'Napa County'), (6057, 'Nevada County'), (6059, 'Orange County'),
    (6061, 'Placer County'), (6063, 'Plumas County'), (6065, 'Riverside County'),
    (6067, 'Sacramento County'), (6069, 'San Benito County'), (6071, 'San Bernardino County'),
    (6073, 'San Diego County'), (6075, 'San Francisco County'), (6077, 'San Joaquin County'),
    (6079, 'San Luis Obispo County'), (6081, 'San Mateo County'), (6083, 'Santa Barbara County'),
    (6085, 'Santa Clara County'), (6087, 'Santa Cruz County'), (6089, 'Shasta County'),
    (6091, 'Sierra County'), (6093, 'Siskiyou County'), (6095, 'Solano County'),
    (6097, 'Sonoma County'), (6099, 'Stanislaus County'), (6101, 'Sutter County'),
    (6103, 'Tehama County'), (6105, 'Trinity County'), (6107, 'Tulare County'),
    (6109, 'Tuolumne County'), (6111, 'Ventura County'), (6113, 'Yolo County'),
    (6115, 'Yuba County')
], columns=['geo_fips', 'county'])

quant_cols = [
    'units_installed', 'total_project_cost_usd',
    'annual_electricity_savings_kwh', 'annual_gas_savings_therms',
    'annual_ghg_savings_mtco2e'
]
grouped = agg_final.groupby(['county', 'year', 'Building Type', 'Product Group'], dropna=False)[quant_cols].sum().reset_index()
grouped['project_cost_per_unit_usd'] = grouped['total_project_cost_usd'] / grouped['units_installed']
grouped['electricity_savings_per_unit_kwh'] = grouped['annual_electricity_savings_kwh'] / grouped['units_installed']
grouped['gas_savings_per_unit_therms'] = grouped['annual_gas_savings_therms'] / grouped['units_installed']
grouped['ghg_savings_per_unit_mtco2e'] = grouped['annual_ghg_savings_mtco2e'] / grouped['units_installed']
grouped = grouped.merge(county_lookup, on='county', how='left')
grouped['location_name'] = grouped['county']
grouped['state'] = 'California'
grouped['geography_type'] = 'county'
grouped = grouped[agg_final.columns]

agg_final = pd.concat([agg_final, grouped], ignore_index=True)
agg_final = agg_final.fillna(0)

# Add California with outliers removed from county aggregation
county_df = agg_final[agg_final['geography_type'] == 'county'].copy()
county_df = county_df.rename(columns={'Building Type': 'building_type', 'Product Group': 'system'})

# Exclude county outliers based on 99th percentile thresholds
cost_threshold = county_df['project_cost_per_unit_usd'].quantile(0.99)
ghg_threshold = county_df['ghg_savings_per_unit_mtco2e'].quantile(0.99)

filtered_county_df = county_df[
    (county_df['project_cost_per_unit_usd'] <= cost_threshold) &
    (county_df['ghg_savings_per_unit_mtco2e'] <= ghg_threshold)
]

# Aggregate state-level totals from filtered county-level data
state_rows = filtered_county_df.groupby(['year', 'building_type', 'system'], as_index=False).apply(
    lambda group: pd.Series({
        'units_installed': group['units_installed'].sum(),
        'total_project_cost_usd': group['total_project_cost_usd'].sum(),
        'annual_electricity_savings_kwh': group['annual_electricity_savings_kwh'].sum(),
        'annual_gas_savings_therms': group['annual_gas_savings_therms'].sum(),
        'annual_ghg_savings_mtco2e': group['annual_ghg_savings_mtco2e'].sum()
    })
).reset_index()

# Compute per-unit averages
state_rows['project_cost_per_unit_usd'] = state_rows['total_project_cost_usd'] / state_rows['units_installed']
state_rows['electricity_savings_per_unit_kwh'] = state_rows['annual_electricity_savings_kwh'] / state_rows['units_installed']
state_rows['gas_savings_per_unit_therms'] = state_rows['annual_gas_savings_therms'] / state_rows['units_installed']
state_rows['ghg_savings_per_unit_mtco2e'] = state_rows['annual_ghg_savings_mtco2e'] / state_rows['units_installed']

# Assign metadata
state_rows['geo_fips'] = 6
state_rows['location_name'] = 'California'
state_rows['county'] = 'NA'
state_rows['state'] = 'California'
state_rows['geography_type'] = 'state'

# Final column selection
final_cols = [
    'geo_fips', 'location_name', 'county', 'state', 'geography_type',
    'year', 'building_type', 'system',
    'units_installed', 'total_project_cost_usd', 'project_cost_per_unit_usd',
    'annual_electricity_savings_kwh', 'electricity_savings_per_unit_kwh',
    'annual_gas_savings_therms', 'gas_savings_per_unit_therms',
    'annual_ghg_savings_mtco2e', 'ghg_savings_per_unit_mtco2e'
]

state_rows = state_rows[final_cols]
agg_final = agg_final.rename(columns={'Building Type': 'building_type', 'Product Group': 'system'})
agg_final = agg_final[final_cols]
agg_final = pd.concat([agg_final, state_rows], ignore_index=True).sort_values(['geo_fips', 'year', 'building_type', 'system'])

agg_final.to_csv("/content/drive/MyDrive/ecodatalab/policy/data/heat pump/db.heat_pumps.csv", index=False)