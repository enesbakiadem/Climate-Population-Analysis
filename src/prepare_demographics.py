from pathlib import Path
import pandas as pd

# ── Paths ────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ── Helper: Weltbank Wide → Long ─────────────────────────────
def clean_worldbank(filename, value_name):
    df = pd.read_csv(RAW_DIR / filename)
    df = df[['Country Name', 'Country Code'] +
            [col for col in df.columns
             if col.startswith('197') or col.startswith('198')
             or col.startswith('199') or col.startswith('200')
             or col.startswith('201') or col.startswith('202')]]
    df = df.melt(id_vars=['Country Name', 'Country Code'],
                 var_name='Jahr', value_name=value_name)
    df['Jahr'] = df['Jahr'].str[:4].astype(int)
    df[value_name] = pd.to_numeric(df[value_name], errors='coerce')
    df = df[(df['Jahr'] >= 1976) & (df['Jahr'] <= 2024)]
    return df

# ── Fertilitätsrate ───────────────────────────────────────────
fertility = pd.read_csv(RAW_DIR / "children-per-woman-un.csv")
fertility.columns = ['Country Name', 'Country Code', 'Jahr', 'Fertility_Rate']
fertility = fertility[fertility['Country Code'].str.len() == 3]
fertility = fertility[(fertility['Jahr'] >= 1976) & (fertility['Jahr'] <= 2024)]

# ── CO2 per Capita ────────────────────────────────────────────
co2 = pd.read_csv(RAW_DIR / "co-emissions-per-capita.csv")
co2.columns = ['Country Name', 'Country Code', 'Jahr', 'CO2_per_Capita']
co2 = co2[co2['Country Code'].str.len() == 3]
co2 = co2[(co2['Jahr'] >= 1976) & (co2['Jahr'] <= 2024)]

# ── GDP per Capita ────────────────────────────────────────────
gdp_pc = clean_worldbank("GDP_per_capita.csv", "GDP_per_Capita")
gdp_pc = gdp_pc[gdp_pc['Country Code'].str.len() == 3]

# ── Bevölkerung ───────────────────────────────────────────────
pop = clean_worldbank("Population.csv", "Population")
pop = pop[pop['Country Code'].str.len() == 3]
pop = pop.dropna(subset=['Population'])

# ── Merge ─────────────────────────────────────────────────────
df = fertility.merge(
    co2[['Country Code', 'Jahr', 'CO2_per_Capita']],
    on=['Country Code', 'Jahr'],
    how='inner'
)
df = df.merge(
    gdp_pc[['Country Code', 'Jahr', 'GDP_per_Capita']],
    on=['Country Code', 'Jahr'],
    how='left'
)
df = df.merge(
    pop[['Country Code', 'Jahr', 'Population']],
    on=['Country Code', 'Jahr'],
    how='left'
)

df = df.dropna(subset=['Fertility_Rate', 'CO2_per_Capita'])
df = df.sort_values(['Country Name', 'Jahr']).reset_index(drop=True)

# ── Save ──────────────────────────────────────────────────────
df.to_csv(PROCESSED_DIR / "demographics.csv", index=False, sep=';', decimal=',')
print(f"demographics.csv saved: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Länder: {df['Country Name'].nunique()} | Zeitraum: {df['Jahr'].min()}–{df['Jahr'].max()}")
print()
print("Sample 2023 — niedrigste Fertilitätsrate:")
low = df[df['Jahr'] == 2023].nsmallest(10, 'Fertility_Rate')
print(low[['Country Name', 'Fertility_Rate', 'CO2_per_Capita', 'GDP_per_Capita']].to_string(index=False))
print()
print("Sample 2023 — höchste Fertilitätsrate:")
high = df[df['Jahr'] == 2023].nlargest(10, 'Fertility_Rate')
print(high[['Country Name', 'Fertility_Rate', 'CO2_per_Capita', 'GDP_per_Capita']].to_string(index=False))
