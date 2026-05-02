-- ============================================
-- CLIMATE POPULATION ANALYSIS
-- Part 2: Demographic Transition
-- Fertility vs GDP Growth (1980-2020)
-- ============================================


-- Q4: Global average — GDP today vs fertility 10 years later
SELECT 
    g.Year AS gdp_year,
    ROUND(AVG(g.GDP_per_capita), 0) AS avg_gdp,
    ROUND(AVG(f."Fertility rate"), 2) AS avg_fertility_10_years_later
FROM gdp_per_capita g
JOIN fertility f 
    ON g."Country Name" = f.Entity
    AND g.Year + 10 = f.Year
WHERE g.Year BETWEEN 1976 AND 2010
GROUP BY g.Year
ORDER BY g.Year;

-- Finding: Clear inverse relationship globally — but both variables
-- trend monotonically over decades, so correlation may be spurious.
-- Interpret with caution.


-- Q5: Fertility decline by GDP growth group (6 buckets)
SELECT 
    CASE 
        WHEN gdp_growth < 1000  THEN '1_very low (<1k)'
        WHEN gdp_growth < 5000  THEN '2_low (1k-5k)'
        WHEN gdp_growth < 10000 THEN '3_lower middle (5k-10k)'
        WHEN gdp_growth < 20000 THEN '4_upper middle (10k-20k)'
        WHEN gdp_growth < 50000 THEN '5_high (20k-50k)'
        ELSE                         '6_extreme (>50k)'
    END AS gdp_growth_group,
    COUNT(*) AS countries,
    ROUND(AVG(fertility_decline), 2) AS avg_absolute_decline,
    ROUND(AVG(fertility_decline / fertility_early * 100), 1) AS avg_relative_decline_pct
FROM (
    SELECT 
        g."Country Name",
        ROUND(MAX(g.GDP_per_capita) - MIN(g.GDP_per_capita), 0) AS gdp_growth,
        ROUND(MAX(f."Fertility rate") - MIN(f."Fertility rate"), 2) AS fertility_decline,
        ROUND(MAX(f."Fertility rate"), 2) AS fertility_early
    FROM gdp_per_capita g
    JOIN fertility f ON g."Country Name" = f.Entity
    WHERE g.Year BETWEEN 1980 AND 2020
      AND f.Year BETWEEN 1980 AND 2020
    GROUP BY g."Country Name"
    HAVING gdp_growth > 0 AND fertility_decline > 0
)
GROUP BY gdp_growth_group
ORDER BY gdp_growth_group;

-- Finding: The relationship is non-linear. Middle-income countries
-- show the strongest relative decline (~47-49%)
-- This is consistent with demographic transition theory, where factors
-- such as education, urbanization, and income growth are often linked
-- to falling fertility.
-- Wealthy countries already had low fertility in 1980 and had
-- little room left to fall.