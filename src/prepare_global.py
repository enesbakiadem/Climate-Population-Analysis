from pathlib import Path
import pandas as pd

# ── Paths ────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ── CO2 Global Gesamtausstoß (OWID_WRL) ──────────────────────
co2 = pd.read_csv(RAW_DIR / "annual-co2-emissions-per-country.csv")
co2.columns = ['Entity', 'Country Code', 'Jahr', 'CO2_Tonnen']
co2_world = co2[co2['Country Code'] == 'OWID_WRL'].copy()
co2_world = co2_world[(co2_world['Jahr'] >= 1976) & (co2_world['Jahr'] <= 2024)]
co2_world = co2_world[['Jahr', 'CO2_Tonnen']]

# Tonnen → Gigatonnen (lesbarer)
co2_world['CO2_Gt'] = co2_world['CO2_Tonnen'] / 1_000_000_000
co2_world = co2_world.drop(columns=['CO2_Tonnen'])

# ── NASA Temperaturanomalie (global) ──────────────────────────
nasa = pd.read_csv(RAW_DIR / "GLB_Ts_dSST.csv", skiprows=1)
nasa = nasa[['Year', 'J-D']].copy()
nasa.columns = ['Jahr', 'Temp_Anomalie']
nasa['Temp_Anomalie'] = pd.to_numeric(nasa['Temp_Anomalie'], errors='coerce')
nasa = nasa.dropna(subset=['Temp_Anomalie'])
nasa = nasa[(nasa['Jahr'] >= 1976) & (nasa['Jahr'] <= 2024)]

# ── Merge ─────────────────────────────────────────────────────
global_df = co2_world.merge(nasa, on='Jahr', how='inner')

# ── Save ──────────────────────────────────────────────────────
global_df.to_csv(PROCESSED_DIR / "global_co2_temp.csv", index=False, sep=';', decimal=',')
print(f"global_co2_temp.csv saved: {global_df.shape[0]} rows, {global_df.shape[1]} columns")
print(f"Zeitraum: {global_df['Jahr'].min()}–{global_df['Jahr'].max()}")
print()
print(global_df.tail(5).to_string(index=False))
