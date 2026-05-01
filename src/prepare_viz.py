import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

import pandas as pd
from utils import RAW_DIR, START_YEAR, END_YEAR, clean_worldbank, save

# ── CO2 Share per Country ─────────────────────────────────────
share = pd.read_csv(RAW_DIR / "annual-share-of-co2-emissions.csv")
share.columns = ['Country Name', 'Country Code', 'Year', 'CO2_Share']
share = share[share['Country Code'].str.len() == 3]
share = share[(share['Year'] >= START_YEAR) & (share['Year'] <= END_YEAR)]

# ── Population (countries + world total) ─────────────────────
pop_all = clean_worldbank("Population.csv", "Population")

# World population as base
pop_world = pop_all[pop_all['Country Code'] == 'WLD'][['Year', 'Population']].copy()
pop_world.columns = ['Year', 'World_Population']

# Countries only
pop = pop_all[pop_all['Country Code'].str.len() == 3].copy()

# ── Merge ─────────────────────────────────────────────────────
df = share.merge(
    pop[['Country Code', 'Year', 'Population']],
    on=['Country Code', 'Year'],
    how='inner'
)
df = df.merge(pop_world, on='Year', how='left')

# Calculate population share
df['Pop_Share'] = (df['Population'] / df['World_Population']) * 100

df = df[['Country Name', 'Country Code', 'Year', 'CO2_Share', 'Pop_Share', 'Population', 'World_Population']]
df = df.sort_values(['Country Name', 'Year']).reset_index(drop=True)

# ── Save ──────────────────────────────────────────────────────
save(df, "co2_vs_population_share.csv")
print(f"Countries: {df['Country Name'].nunique()} | Years: {df['Year'].min()}–{df['Year'].max()}")
print("\nSample 2023 (Top CO2):")
print(df[df['Year'] == 2023].nlargest(5, 'CO2_Share')[['Country Name','CO2_Share','Pop_Share']].to_string(index=False))