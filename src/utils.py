from pathlib import Path
import pandas as pd

# ── Paths ────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ── Constants ─────────────────────────────────────────────────
START_YEAR = 1976
END_YEAR = 2024
FERTILITY_THRESHOLD = 2.1  # Replacement level

# ── Helper: Worldbank Wide → Long ────────────────────────────
def clean_worldbank(filename, value_name, start=START_YEAR, end=END_YEAR):
    """
    Reads a Worldbank CSV in wide format and returns a long format DataFrame.
    Filters to real countries (3-letter code) and the specified year range.
    """
    df = pd.read_csv(RAW_DIR / filename)
    df = df[['Country Name', 'Country Code'] +
            [col for col in df.columns
             if col.startswith('197') or col.startswith('198')
             or col.startswith('199') or col.startswith('200')
             or col.startswith('201') or col.startswith('202')]]
    df = df.melt(id_vars=['Country Name', 'Country Code'],
                 var_name='Year', value_name=value_name)
    df['Year'] = df['Year'].str[:4].astype(int)
    df[value_name] = pd.to_numeric(df[value_name], errors='coerce')
    df = df[(df['Year'] >= start) & (df['Year'] <= end)]
    return df

# ── Helper: Load CO2 per Capita ───────────────────────────────
def load_co2(start=START_YEAR, end=END_YEAR, real_countries_only=True):
    """
    Loads CO2 per capita from Our World in Data.
    Optionally filters to real countries only (3-letter code).
    """
    df = pd.read_csv(RAW_DIR / "co-emissions-per-capita.csv")
    df.columns = ['Country Name', 'Country Code', 'Year', 'CO2_per_Capita']
    if real_countries_only:
        df = df[df['Country Code'].str.len() == 3]
    df = df[(df['Year'] >= start) & (df['Year'] <= end)]
    return df

# ── Helper: Load NASA Temperature Anomaly ────────────────────
def load_nasa(start=START_YEAR, end=END_YEAR):
    """
    Loads global temperature anomaly from NASA GISS.
    Returns annual mean (J-D column).
    """
    df = pd.read_csv(RAW_DIR / "GLB_Ts_dSST.csv", skiprows=1)
    df = df[['Year', 'J-D']].copy()
    df.columns = ['Year', 'Temp_Anomaly']
    df['Temp_Anomaly'] = pd.to_numeric(df['Temp_Anomaly'], errors='coerce')
    df = df.dropna(subset=['Temp_Anomaly'])
    df = df[(df['Year'] >= start) & (df['Year'] <= end)]
    return df

# ── Helper: Save to processed ─────────────────────────────────
def save(df, filename):
    """
    Saves DataFrame to processed folder as CSV with semicolon and comma decimal.
    """
    path = PROCESSED_DIR / filename
    df.to_csv(path, index=False, sep=';', decimal=',')
    print(f"✅ {filename} saved: {df.shape[0]} rows, {df.shape[1]} columns")
    return path