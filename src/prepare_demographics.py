import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

import pandas as pd
from utils import RAW_DIR, START_YEAR, END_YEAR, clean_worldbank, load_co2, save

# ── Fertility Rate ────────────────────────────────────────────
fertility = pd.read_csv(RAW_DIR / "children-per-woman-un.csv")
fertility.columns = ['Country Name', 'Country Code', 'Year', 'Fertility_Rate']
fertility = fertility[fertility['Country Code'].str.len() == 3]
fertility = fertility[(fertility['Year'] >= START_YEAR) & (fertility['Year'] <= END_YEAR)]

# ── CO2 & GDP per Capita ──────────────────────────────────────
co2    = load_co2()
gdp_pc = clean_worldbank("GDP_per_capita.csv", "GDP_per_Capita")
gdp_pc = gdp_pc[gdp_pc['Country Code'].str.len() == 3]

# ── Population ────────────────────────────────────────────────
pop = clean_worldbank("Population.csv", "Population")
pop = pop[pop['Country Code'].str.len() == 3].dropna(subset=['Population'])

# ── Merge ─────────────────────────────────────────────────────
df = fertility.merge(
    co2[['Country Code', 'Year', 'CO2_per_Capita']],
    on=['Country Code', 'Year'],
    how='inner'
)
df = df.merge(gdp_pc[['Country Code', 'Year', 'GDP_per_Capita']], on=['Country Code', 'Year'], how='left')
df = df.merge(pop[['Country Code', 'Year', 'Population']],        on=['Country Code', 'Year'], how='left')

df = df.dropna(subset=['Fertility_Rate', 'CO2_per_Capita'])
df = df.sort_values(['Country Name', 'Year']).reset_index(drop=True)

# ── Save ──────────────────────────────────────────────────────
save(df, "demographics.csv")
print(f"Countries: {df['Country Name'].nunique()} | Years: {df['Year'].min()}–{df['Year'].max()}")
print("\nSample 2023 — lowest fertility rate:")
print(df[df['Year'] == 2023].nsmallest(5, 'Fertility_Rate')[['Country Name','Fertility_Rate','CO2_per_Capita']].to_string(index=False))
print("\nSample 2023 — highest fertility rate:")
print(df[df['Year'] == 2023].nlargest(5, 'Fertility_Rate')[['Country Name','Fertility_Rate','CO2_per_Capita']].to_string(index=False))