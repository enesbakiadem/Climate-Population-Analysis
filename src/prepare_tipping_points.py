import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

import pandas as pd
from utils import RAW_DIR, FERTILITY_THRESHOLD, load_co2, save

# ── Fertility Rate ────────────────────────────────────────────
fertility = pd.read_csv(RAW_DIR / "children-per-woman-un.csv")
fertility.columns = ['Country Name', 'Country Code', 'Year', 'Fertility_Rate']
fertility = fertility[fertility['Country Code'].str.len() == 3]
fertility = fertility.sort_values(['Country Code', 'Year'])

# ── CO2 per Capita ────────────────────────────────────────────
co2 = load_co2(real_countries_only=True)

# ── Find Tipping Points ───────────────────────────────────────
records = []
for code, group in fertility.groupby('Country Code'):
    group = group.sort_values('Year')
    below = group[group['Fertility_Rate'] < FERTILITY_THRESHOLD]

    if below.empty:
        continue

    tipping_year     = below['Year'].iloc[0]
    tipping_fertility = below['Fertility_Rate'].iloc[0]
    country_name     = group['Country Name'].iloc[0]

    # CO2 at tipping point year
    co2_then = co2[(co2['Country Code'] == code) & (co2['Year'] == tipping_year)]['CO2_per_Capita']
    co2_then = co2_then.iloc[0] if not co2_then.empty else None

    # CO2 current (latest available year)
    co2_latest = co2[co2['Country Code'] == code].sort_values('Year')
    co2_current     = co2_latest['CO2_per_Capita'].iloc[-1] if not co2_latest.empty else None
    co2_current_year = co2_latest['Year'].iloc[-1]          if not co2_latest.empty else None

    records.append({
        'Country Name':              country_name,
        'Country Code':              code,
        'Tipping_Point_Year':        tipping_year,
        'Fertility_At_Tipping_Point': round(tipping_fertility, 3),
        'Fertility_Current':         round(group['Fertility_Rate'].iloc[-1], 3),
        'Fertility_Current_Year':    group['Year'].iloc[-1],
        'CO2_At_Tipping_Point':      round(co2_then, 3)    if co2_then    else None,
        'CO2_Current':               round(co2_current, 3) if co2_current else None,
        'CO2_Current_Year':          co2_current_year,
    })

df = pd.DataFrame(records).sort_values('Tipping_Point_Year').reset_index(drop=True)

# ── Save ──────────────────────────────────────────────────────
save(df, "tipping_points.csv")
print(f"\nEarliest Tipping Points:")
print(df.head(10)[['Country Name','Tipping_Point_Year','Fertility_At_Tipping_Point','CO2_At_Tipping_Point','CO2_Current']].to_string(index=False))
print(f"\nCountries still ABOVE {FERTILITY_THRESHOLD}:")
never = fertility.groupby('Country Code').apply(lambda g: (g['Fertility_Rate'] < FERTILITY_THRESHOLD).any())
above = fertility[fertility['Country Code'].isin(never[~never].index)][['Country Name']].drop_duplicates()
print(f"{len(above)} countries: {above['Country Name'].tolist()}")