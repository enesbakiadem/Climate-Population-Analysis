-- ============================================
-- CLIMATE POPULATION ANALYSIS
-- Part 3: Regional CO₂ Analysis (1990-2020)
-- Baseline: 1990 (Kyoto Protocol reference year)
-- ============================================


-- Q6: Regional CO₂ change since Kyoto baseline
SELECT 
    c1.Entity AS Region,
    ROUND((c2."Annual CO₂ emissions" - c1."Annual CO₂ emissions") 
          / c1."Annual CO₂ emissions" * 100, 1) AS co2_change_pct
FROM co2 c1
JOIN co2 c2 ON c1.Entity = c2.Entity
WHERE c1.Year = 1990
  AND c2.Year = 2020
  AND c1.Entity IN ('Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America')
ORDER BY co2_change_pct ASC;

-- Finding: Europe is the only region that reduced CO2 (-37.5%).
-- North America barely moved (-3.3%) despite being wealthy.
-- Africa (+108%) and Asia (+214%) grew fast, but Q7 shows why
-- the percentage alone is misleading.


-- Q7: Absolute regional CO2 emissions in 2020 — context for Q6
SELECT 
    Entity AS Region,
    ROUND("Annual CO₂ emissions" / 1e9, 1) AS co2_2020_gt
FROM co2
WHERE Year = 2020
  AND Entity IN ('Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America')
ORDER BY co2_2020_gt DESC;

-- Finding: Asia alone accounts for 20.7 Gt — more than all other
-- regions combined. Africa emits just 1.4 Gt despite +108% growth.
-- North America (-3.3%) still emits 5.8 Gt — more than all of Europe.