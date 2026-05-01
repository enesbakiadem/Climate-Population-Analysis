import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

import pandas as pd
from utils import RAW_DIR, clean_worldbank, load_co2, load_nasa, save

# ── Load Worldbank ────────────────────────────────────────────
gdp          = clean_worldbank("GDP.csv",           "GDP")
gdp_pc       = clean_worldbank("GDP_per_capita.csv","GDP_per_Capita")
population   = clean_worldbank("Population.csv",    "Population")
unemployment = clean_worldbank("Unemployment.csv",  "Unemployment")

# ── Merge Worldbank ───────────────────────────────────────────
master = gdp.merge(gdp_pc,       on=['Country Name', 'Country Code', 'Year'])
master = master.merge(population,    on=['Country Name', 'Country Code', 'Year'])
master = master.merge(unemployment,  on=['Country Name', 'Country Code', 'Year'])

# ── Load CO2 & NASA ───────────────────────────────────────────
co2  = load_co2()
nasa = load_nasa()

# ── Merge All ─────────────────────────────────────────────────
master = master.merge(
    co2[['Country Code', 'Year', 'CO2_per_Capita']],
    on=['Country Code', 'Year'],
    how='inner'
)
master = master.merge(nasa, on='Year', how='left')
master = master.sort_values(['Country Name', 'Year']).reset_index(drop=True)
master = master.dropna(subset=['GDP'])

# ── Save ──────────────────────────────────────────────────────
save(master, "climate_master.csv")
print(f"Countries: {master['Country Name'].nunique()} | Years: {master['Year'].min()}–{master['Year'].max()}")
print(f"\nCompleteness:")
print(master[['GDP','Population','GDP_per_Capita','Unemployment','CO2_per_Capita','Temp_Anomaly']].notna().mean().round(2))