from pathlib import Path
import pandas as pd

# ── Paths ────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ── CO2 Share pro Land ────────────────────────────────────────
share = pd.read_csv(RAW_DIR / "annual-share-of-co2-emissions.csv")
share.columns = ['Country Name', 'Country Code', 'Jahr', 'CO2_Share']
# Nur echte Länder (keine Regionen/Aggregate)
share = share[share['Country Code'].str.len() == 3]
share = share[(share['Jahr'] >= 1976) & (share['Jahr'] <= 2024)]

# ── Weltbevölkerung (als Basis) ───────────────────────────────
def weltbank_to_long(path, value_name):
    df = pd.read_csv(path)
    id_cols = ['Country Name', 'Country Code']
    year_cols = [c for c in df.columns if '[YR' in c]
    df = df[id_cols + year_cols]
    df = df.melt(id_vars=id_cols, var_name='Jahr_raw', value_name=value_name)
    df['Jahr'] = df['Jahr_raw'].str.extract(r'(\d{4})').astype(int)
    df = df.drop(columns=['Jahr_raw'])
    df[value_name] = pd.to_numeric(df[value_name], errors='coerce')
    df = df[(df['Jahr'] >= 1976) & (df['Jahr'] <= 2024)]
    df.columns = ['Country_Name', 'Country_Code', value_name, 'Jahr']
    return df[['Country_Code', 'Jahr', value_name]]

pop_all = weltbank_to_long(RAW_DIR / "Population.csv", 'Population')

# Weltbevölkerung separat
pop_world = pop_all[pop_all['Country_Code'] == 'WLD'][['Jahr', 'Population']].copy()
pop_world.columns = ['Jahr', 'World_Population']

# Länderbevölkerung (keine Aggregate)
pop = pop_all[pop_all['Country_Code'].str.len() == 3].copy()

# ── Merge ─────────────────────────────────────────────────────
df = share.merge(
    pop[['Country_Code', 'Jahr', 'Population']],
    left_on=['Country Code', 'Jahr'],
    right_on=['Country_Code', 'Jahr'],
    how='inner'
)
df = df.merge(pop_world, on='Jahr', how='left')

# Bevölkerungsanteil berechnen
df['Pop_Share'] = (df['Population'] / df['World_Population']) * 100

df = df[['Country Name', 'Country Code', 'Jahr', 'CO2_Share', 'Pop_Share', 'Population', 'World_Population']]
df = df.sort_values(['Country Name', 'Jahr']).reset_index(drop=True)

# ── Save ──────────────────────────────────────────────────────
df.to_csv(PROCESSED_DIR / "co2_vs_population_share.csv", index=False, sep=';', decimal=',')
print(f"co2_vs_population_share.csv saved: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Länder: {df['Country Name'].nunique()} | Zeitraum: {df['Jahr'].min()}–{df['Jahr'].max()}")
print()
print("Sample 2023 (Top CO2):")
print(df[df['Jahr'] == 2023].nlargest(5, 'CO2_Share')[['Country Name','CO2_Share','Pop_Share']].to_string(index=False))
