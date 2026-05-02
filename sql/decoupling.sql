-- ============================================
-- CLIMATE POPULATION ANALYSIS
-- Part 1: Decoupling — CO₂ vs GDP (1990-2020)
-- Baseline: 1990 (Kyoto Protocol reference year)
-- ============================================


-- Q1: Which countries reduced CO₂ while growing GDP?
SELECT 
    c1.Entity AS Country,
    ROUND(c1."Annual CO₂ emissions" / 1e9, 2) AS co2_1990_gt,
    ROUND(c2."Annual CO₂ emissions" / 1e9, 2) AS co2_2020_gt,
    ROUND((c2."Annual CO₂ emissions" - c1."Annual CO₂ emissions") 
          / c1."Annual CO₂ emissions" * 100, 1) AS co2_change_pct,
    ROUND(g1.GDP_per_capita, 0) AS gdp_1990,
    ROUND(g2.GDP_per_capita, 0) AS gdp_2020,
    ROUND((g2.GDP_per_capita - g1.GDP_per_capita) 
          / g1.GDP_per_capita * 100, 1) AS gdp_change_pct
FROM co2 c1
JOIN co2 c2 ON c1.Entity = c2.Entity
JOIN gdp_per_capita g1 ON c1.Entity = g1."Country Name" AND g1.Year = 1990
JOIN gdp_per_capita g2 ON c1.Entity = g2."Country Name" AND g2.Year = 2020
WHERE c1.Year = 1990
  AND c2.Year = 2020
  AND c2."Annual CO₂ emissions" < c1."Annual CO₂ emissions"
  AND g2.GDP_per_capita > g1.GDP_per_capita
ORDER BY co2_change_pct ASC;

-- Finding: Eastern Europe (Moldova -86%, Ukraine -71%) shows the
-- strongest decline — but driven by deindustrialization after the
-- Soviet collapse, not climate policy.


-- Q2: Genuine decoupling — high-income countries only (GDP > $10k in 1990)
SELECT 
    c1.Entity AS Country,
    ROUND((c2."Annual CO₂ emissions" - c1."Annual CO₂ emissions") 
          / c1."Annual CO₂ emissions" * 100, 1) AS co2_change_pct,
    ROUND(g1.GDP_per_capita, 0) AS gdp_1990,
    ROUND(g2.GDP_per_capita, 0) AS gdp_2020,
    ROUND((g2.GDP_per_capita - g1.GDP_per_capita) 
          / g1.GDP_per_capita * 100, 1) AS gdp_change_pct
FROM co2 c1
JOIN co2 c2 ON c1.Entity = c2.Entity
JOIN gdp_per_capita g1 ON c1.Entity = g1."Country Name" AND g1.Year = 1990
JOIN gdp_per_capita g2 ON c1.Entity = g2."Country Name" AND g2.Year = 2020
WHERE c1.Year = 1990
  AND c2.Year = 2020
  AND c2."Annual CO₂ emissions" < c1."Annual CO₂ emissions"
  AND g2.GDP_per_capita > g1.GDP_per_capita
  AND g1.GDP_per_capita > 10000
ORDER BY co2_change_pct ASC;

-- Finding: Denmark (-47%), the UK (-46%), and Germany (-39%) show the clearest
-- cases of potential decoupling in this filtered group. The US and Japan grew
-- more economically but reduced CO₂ far less (-9% and -10% respectively).


-- Q3: Efficiency ratio — GDP growth per 1% of CO₂ reduction
-- ⚠ EXPERIMENTAL: Austria's ratio is distorted because its CO₂
-- change is near zero, making the divisor unstable. Use with caution.
SELECT 
    c1.Entity AS Country,
    ROUND((c2."Annual CO₂ emissions" - c1."Annual CO₂ emissions") 
          / c1."Annual CO₂ emissions" * 100, 1) AS co2_change_pct,
    ROUND((g2.GDP_per_capita - g1.GDP_per_capita) 
          / g1.GDP_per_capita * 100, 1) AS gdp_change_pct,
    ROUND(
        ((g2.GDP_per_capita - g1.GDP_per_capita) / g1.GDP_per_capita * 100) /
        ABS((c2."Annual CO₂ emissions" - c1."Annual CO₂ emissions") 
            / c1."Annual CO₂ emissions" * 100)
    , 2) AS gdp_growth_per_co2_reduction
FROM co2 c1
JOIN co2 c2 ON c1.Entity = c2.Entity
JOIN gdp_per_capita g1 ON c1.Entity = g1."Country Name" AND g1.Year = 1990
JOIN gdp_per_capita g2 ON c1.Entity = g2."Country Name" AND g2.Year = 2020
WHERE c1.Year = 1990
  AND c2.Year = 2020
  AND c2."Annual CO₂ emissions" < c1."Annual CO₂ emissions"
  AND g2.GDP_per_capita > g1.GDP_per_capita
  AND g1.GDP_per_capita > 10000
ORDER BY gdp_growth_per_co2_reduction DESC;

-- Finding: Scandinavia and Germany sit at the bottom of this ranking —
-- meaning they achieved the most CO2 reduction per unit of GDP growth.
-- The US and Japan rank near the top: high GDP growth, low CO2 reduction.