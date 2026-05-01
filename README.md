# Climate & Population Analysis

How do CO2 emissions, economic development, and demographic change relate to global warming?

> A data analysis project combining climate, economic, and demographic data to explore the structural drivers of CO2 emissions — developed as part of a political science class at Abendgymnasium Göttingen.

## 📸 Key Visuals

### Global CO2 Emissions & Temperature Anomaly (1976–2024)
![CO2 & Temperature](./visuals/01_co2_temp.png)

### CO2 Share vs. Population Share by Country
![CO2 vs Population Share](./visuals/02_co2_population_share.png)

### Fertility Rate vs. CO2 Emissions per Capita
![Fertility vs CO2](./visuals/05_fertility_co2.png)

## 🎯 Research Question

Which countries drive global CO2 emissions, and how do economic development and demographic change relate to carbon output?

## 🧠 Background

Climate change is often discussed in terms of global totals. But the distribution of emissions is deeply unequal — shaped by wealth, population size, and demographic trajectory.

This project explores these relationships using publicly available data, asking not just *how much* is emitted, but *by whom*, *why*, and *what the demographic future might mean* for global emissions.

## 📊 Data Sources

- **Our World in Data** — CO2 per capita, annual CO2 emissions, CO2 share by country, fertility rates
- **World Bank Open Data** — GDP, GDP per capita, population, unemployment
- **NASA GISS** — Global surface temperature anomaly (baseline: 1951–1980)

## ⚙️ Methodology

- Data cleaning and merging across multiple sources using Python (pandas)
- Long-format transformation of Worldbank wide-format data
- Filtering to real countries (ISO 3-letter codes) to exclude regional aggregates
- Calculation of population share and fertility tipping points (first year below replacement level of 2.1)
- Visualization using Power BI with interactive year slicer

## 📈 Key Results

**CO2 & Temperature**
Global CO2 emissions have more than doubled since 1976 — from 18 to 38 Gt. The temperature anomaly follows the same trajectory, reaching +1.28°C above the 1951–1980 baseline in 2024.

**Who emits?**
China and the US alone account for nearly half of global CO2 emissions. The US emits approximately 3x its demographic weight.

**Why?**
Wealthier nations consistently emit more CO2 per person. Prosperity comes at a carbon cost.

**The demographic paradox**
Countries below the fertility replacement level (2.1) emit significantly more CO2 per person than those still growing. The nations contributing most to the next generation emit the least.

134 out of 204 countries have already fallen below replacement level. Of the 102 still above it, almost all are in Sub-Saharan Africa or South Asia — the regions least responsible for historical emissions.

## ⚠️ Limitations

- CO2 data from Our World in Data is based on production-based emissions and does not account for trade-embedded emissions
- Fertility tipping points are defined as the first year below 2.1, not a sustained period — some countries may have temporarily dipped below before recovering
- Correlation does not imply causation
- Power BI visuals are interactive and best experienced live — static screenshots lose the year slicer functionality

## 🛠️ Tools

- Python (pandas, pathlib)
- Power BI
- Git / GitHub

## ⚙️ Reproducing the Analysis

All raw data must be placed in `data/raw/`. Then run:

```bash
python src/run_all.py
```

This generates all processed CSVs in `data/processed/`, ready to be loaded into Power BI.

## 🤖 Use of AI (Transparency)

AI tools were used to support structuring, wording, and parts of the code.

The core analysis, interpretation, and all decisions were developed independently.