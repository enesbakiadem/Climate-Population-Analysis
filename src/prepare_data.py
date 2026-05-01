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
    df = df[(df['Jahr'] >= 1976) & (df['Jahr'] <= 2026)]
    return df

# ── Load Weltbank ─────────────────────────────────────────────
gdp        = clean_worldbank("GDP.csv",           "GDP")
gdp_pc     = clean_worldbank("GDP_per_capita.csv","GDP_per_Capita")
population = clean_worldbank("Population.csv",    "Population")
unemployment = clean_worldbank("Unemployment.csv","Unemployment")

# ── Merge Weltbank ────────────────────────────────────────────
master = gdp.merge(gdp_pc,       on=['Country Name', 'Country Code', 'Jahr'])
master = master.merge(population,    on=['Country Name', 'Country Code', 'Jahr'])
master = master.merge(unemployment,  on=['Country Name', 'Country Code', 'Jahr'])

# ── Load CO2 (Our World in Data) ──────────────────────────────
co2 = pd.read_csv(RAW_DIR / "co-emissions-per-capita.csv")
co2.columns = ['Country Name', 'Country Code', 'Jahr', 'CO2_per_Capita']
co2 = co2[(co2['Jahr'] >= 1976) & (co2['Jahr'] <= 2026)]

# ── Load NASA Temperatur ──────────────────────────────────────
nasa = pd.read_csv(RAW_DIR / "GLB_Ts_dSST.csv", skiprows=1)
nasa = nasa[['Year', 'J-D']].copy()
nasa.columns = ['Jahr', 'Temp_Anomalie']
nasa['Temp_Anomalie'] = pd.to_numeric(nasa['Temp_Anomalie'], errors='coerce')
nasa = nasa.dropna(subset=['Temp_Anomalie'])
nasa = nasa[(nasa['Jahr'] >= 1976) & (nasa['Jahr'] <= 2026)]

# ── Merge All ─────────────────────────────────────────────────
master = master.merge(
    co2[['Country Code', 'Jahr', 'CO2_per_Capita']],
    on=['Country Code', 'Jahr'],
    how='inner'  # nur Länder mit CO2-Daten
)
master = master.merge(nasa, on='Jahr', how='left')

master = master.sort_values(['Country Name', 'Jahr']).reset_index(drop=True)
master = master.dropna(subset=['GDP'])

# ── Save ──────────────────────────────────────────────────────
master.to_csv(PROCESSED_DIR / "climate_master.csv", index=False, decimal=',', sep=';')
print(f"climate_master.csv saved: {master.shape[0]} rows, {master.shape[1]} columns")
print(f"Länder: {master['Country Name'].nunique()} | Zeitraum: {master['Jahr'].min()}–{master['Jahr'].max()}")
print(f"\nVollständigkeit:")
print(master[['GDP','Population','GDP_per_Capita','Unemployment','CO2_per_Capita','Temp_Anomalie']].notna().mean().round(2))
