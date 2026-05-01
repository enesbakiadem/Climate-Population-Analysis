import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

import pandas as pd
from utils import RAW_DIR, load_nasa, save

# ── Global CO2 Total Emissions (OWID_WRL) ─────────────────────
co2 = pd.read_csv(RAW_DIR / "annual-co2-emissions-per-country.csv")
co2.columns = ['Entity', 'Country Code', 'Year', 'CO2_Tonnes']
co2_world = co2[co2['Country Code'] == 'OWID_WRL'].copy()
co2_world = co2_world[['Year', 'CO2_Tonnes']]

# Tonnes → Gigatonnes (more readable)
co2_world['CO2_Gt'] = co2_world['CO2_Tonnes'] / 1_000_000_000
co2_world = co2_world.drop(columns=['CO2_Tonnes'])

# ── NASA Temperature Anomaly (global) ────────────────────────
nasa = load_nasa()

# ── Merge ─────────────────────────────────────────────────────
global_df = co2_world.merge(nasa, on='Year', how='inner')

# ── Save ──────────────────────────────────────────────────────
save(global_df, "global_co2_temp.csv")
print(f"Years: {global_df['Year'].min()}–{global_df['Year'].max()}")
print(global_df.tail(5).to_string(index=False))