-- ============================================
-- CLIMATE POPULATION ANALYSIS
-- SQL Exploration — Key Questions & Findings
-- ============================================


-- ============================================
-- PART 1: DECOUPLING — CO2 vs GDP 1990-2020
-- ============================================

-- Q1: Which countries reduced CO2 while growing GDP? (all countries)
SELECT 
    c1.Entity AS Land,
    ROUND(c1."Annual CO₂ emissions" / 1e9, 2) AS co2_1990_mrd,
    ROUND(c2."Annual CO₂ emissions" / 1e9, 2) AS co2_2020_mrd,
    ROUND((c2."Annual CO₂ emissions" - c1."Annual CO₂ emissions") 
          / c1."Annual CO₂ emissions" * 100, 1) AS co2_veränderung_pct,
    ROUND(g1.GDP_per_capita, 0) AS gdp_1990,
    ROUND(g2.GDP_per_capita, 0) AS gdp_2020,
    ROUND((g2.GDP_per_capita - g1.GDP_per_capita) 
          / g1.GDP_per_capita * 100, 1) AS gdp_veränderung_pct
FROM co2 c1
JOIN co2 c2 ON c1.Entity = c2.Entity
JOIN gdp_per_capita g1 ON c1.Entity = g1."Country Name" AND g1.Year = 1990
JOIN gdp_per_capita g2 ON c1.Entity = g2."Country Name" AND g2.Year = 2020
WHERE c1.Year = 1990
  AND c2.Year = 2020
  AND c2."Annual CO₂ emissions" < c1."Annual CO₂ emissions"
  AND g2.GDP_per_capita > g1.GDP_per_capita
ORDER BY co2_veränderung_pct ASC;

-- Finding: Eastern Europe (Moldova, Ukraine) shows strong CO2 decline
-- but driven by deindustrialization after 1991, not green policy.


-- Q2: Genuine decoupling — only high-income countries (GDP > 10k in 1990)
SELECT 
    c1.Entity AS Land,
    ROUND((c2."Annual CO₂ emissions" - c1."Annual CO₂ emissions") 
          / c1."Annual CO₂ emissions" * 100, 1) AS co2_veränderung_pct,
    ROUND(g1.GDP_per_capita, 0) AS gdp_1990,
    ROUND(g2.GDP_per_capita, 0) AS gdp_2020,
    ROUND((g2.GDP_per_capita - g1.GDP_per_capita) 
          / g1.GDP_per_capita * 100, 1) AS gdp_veränderung_pct
FROM co2 c1
JOIN co2 c2 ON c1.Entity = c2.Entity
JOIN gdp_per_capita g1 ON c1.Entity = g1."Country Name" AND g1.Year = 1990
JOIN gdp_per_capita g2 ON c1.Entity = g2."Country Name" AND g2.Year = 2020
WHERE c1.Year = 1990
  AND c2.Year = 2020
  AND c2."Annual CO₂ emissions" < c1."Annual CO₂ emissions"
  AND g2.GDP_per_capita > g1.GDP_per_capita
  AND g1.GDP_per_capita > 10000
ORDER BY co2_veränderung_pct ASC;

-- Finding: Among rich nations, Denmark (-47%), UK (-46%) and 
-- Germany (-39%) lead. USA and Japan grew more but reduced far less.


-- Q3: Efficiency ratio — GDP growth per % CO2 reduction
SELECT 
    c1.Entity AS Land,
    ROUND((c2."Annual CO₂ emissions" - c1."Annual CO₂ emissions") 
          / c1."Annual CO₂ emissions" * 100, 1) AS co2_veränderung_pct,
    ROUND((g2.GDP_per_capita - g1.GDP_per_capita) 
          / g1.GDP_per_capita * 100, 1) AS gdp_veränderung_pct,
    ROUND(
        ((g2.GDP_per_capita - g1.GDP_per_capita) / g1.GDP_per_capita * 100) /
        ABS((c2."Annual CO₂ emissions" - c1."Annual CO₂ emissions") 
            / c1."Annual CO₂ emissions" * 100)
    , 2) AS gdp_wachstum_pro_co2_reduktion
FROM co2 c1
JOIN co2 c2 ON c1.Entity = c2.Entity
JOIN gdp_per_capita g1 ON c1.Entity = g1."Country Name" AND g1.Year = 1990
JOIN gdp_per_capita g2 ON c1.Entity = g2."Country Name" AND g2.Year = 2020
WHERE c1.Year = 1990
  AND c2.Year = 2020
  AND c2."Annual CO₂ emissions" < c1."Annual CO₂ emissions"
  AND g2.GDP_per_capita > g1.GDP_per_capita
  AND g1.GDP_per_capita > 10000
ORDER BY gdp_wachstum_pro_co2_reduktion DESC;

-- Note: Austria ratio is distorted (~0% CO2 change = near-zero divisor)
-- Most meaningful at bottom of list: Scandinavia and Germany.


-- ============================================
-- PART 2: DEMOGRAPHIC TRANSITION
-- Fertility vs GDP Growth 1980-2020
-- ============================================

-- Q4: Global trend — GDP today vs fertility 10 years later
SELECT 
    g.Year AS gdp_year,
    ROUND(AVG(g.GDP_per_capita), 0) AS avg_gdp,
    ROUND(AVG(f.`Fertility rate`), 2) AS avg_fertilität_10_jahre_später
FROM gdp_per_capita g
JOIN fertility f 
    ON g.`Country Name` = f.Entity
    AND g.Year + 10 = f.Year
WHERE g.Year BETWEEN 1976 AND 2010
GROUP BY g.Year
ORDER BY g.Year;

-- Finding: Clear inverse relationship globally — but driven by
-- simultaneous long-term trends, not necessarily causation.


-- Q5: Fertility decline by GDP growth group (6 buckets)
SELECT 
    CASE 
        WHEN gdp_wachstum < 1000 THEN '1_sehr niedrig (<1k)'
        WHEN gdp_wachstum < 5000 THEN '2_niedrig (1k-5k)'
        WHEN gdp_wachstum < 10000 THEN '3_unteres Mittel (5k-10k)'
        WHEN gdp_wachstum < 20000 THEN '4_oberes Mittel (10k-20k)'
        WHEN gdp_wachstum < 50000 THEN '5_hoch (20k-50k)'
        ELSE '6_extrem (>50k)'
    END AS gdp_wachstum_gruppe,
    COUNT(*) AS länder,
    ROUND(AVG(fertilität_rückgang), 2) AS avg_absoluter_rückgang,
    ROUND(AVG(fertilität_rückgang / fertilität_früh * 100), 1) AS avg_relativer_rückgang_pct
FROM (
    SELECT 
        g.`Country Name`,
        ROUND(MAX(g.GDP_per_capita) - MIN(g.GDP_per_capita), 0) AS gdp_wachstum,
        ROUND(MAX(f.`Fertility rate`) - MIN(f.`Fertility rate`), 2) AS fertilität_rückgang,
        ROUND(MAX(f.`Fertility rate`), 2) AS fertilität_früh
    FROM gdp_per_capita g
    JOIN fertility f ON g.`Country Name` = f.Entity
    WHERE g.Year BETWEEN 1980 AND 2020
      AND f.Year BETWEEN 1980 AND 2020
    GROUP BY g.`Country Name`
    HAVING gdp_wachstum > 0 AND fertilität_rückgang > 0
)
GROUP BY gdp_wachstum_gruppe
ORDER BY gdp_wachstum_gruppe;

-- Finding: Relationship is non-linear. Middle-income countries show
-- strongest relative decline (~47-49%) — the demographic transition
-- accelerates fastest where education and urbanization are rising.
-- Rich countries already had low fertility in 1980, less room to fall.