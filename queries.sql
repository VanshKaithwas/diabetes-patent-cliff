-- Diabetes Drug Patent Cliff Analyzer
-- SQL Queries — Vansh Kaithwas
-- Class 12 IT + Commerce + IP
--
-- I used SQLite to run these queries on my dataset.
-- In class we learned basic SELECT, WHERE, GROUP BY —
-- I tried to go a bit further with JOIN and HAVING here.
--
-- To run: load diabetes_patents.csv into a SQLite table called 'drugs'


-- ── Query 1: All drugs expiring before 2027 ──────────────────────────────────
-- Simple starting query — just wanted to see what's expiring soon

SELECT drug_name,
       company,
       patent_expiry_year,
       annual_revenue_usd_bn
FROM drugs
WHERE patent_expiry_year <= 2027
ORDER BY patent_expiry_year ASC, annual_revenue_usd_bn DESC;


-- ── Query 2: Total revenue at risk per year ───────────────────────────────────
-- GROUP BY was confusing at first — I kept forgetting to aggregate
-- the revenue column. Got it working after a few tries.

SELECT patent_expiry_year,
       COUNT(drug_name)                        AS drugs_expiring,
       ROUND(SUM(annual_revenue_usd_bn), 2)    AS total_revenue_at_risk_bn
FROM drugs
GROUP BY patent_expiry_year
ORDER BY patent_expiry_year ASC;


-- ── Query 3: Company exposure ranking ─────────────────────────────────────────
-- Wanted to rank companies by how much of their revenue is expiring
-- Added HAVING to filter only companies with more than 1 drug

SELECT company,
       country,
       COUNT(drug_name)                        AS drugs_in_dataset,
       ROUND(SUM(annual_revenue_usd_bn), 2)    AS total_revenue_bn
FROM drugs
GROUP BY company
HAVING COUNT(drug_name) > 1
ORDER BY total_revenue_bn DESC;


-- ── Query 4: Boehringer Ingelheim deep dive ───────────────────────────────────
-- This was my focus company — I wanted to see all their drugs together
-- and understand how exposed they are as a German company

SELECT drug_name,
       drug_type,
       patent_expiry_year,
       annual_revenue_usd_bn,
       generic_available,
       CASE
           WHEN patent_expiry_year <= 2025 THEN 'CRITICAL — Expiring This Year'
           WHEN patent_expiry_year <= 2027 THEN 'HIGH — Expiring Soon'
           ELSE 'MEDIUM — Some Time Remaining'
       END AS risk_level
FROM drugs
WHERE company = 'Boehringer Ingelheim'
ORDER BY patent_expiry_year ASC;


-- ── Query 5: Drugs already gone generic vs still protected ───────────────────
-- I learned you can filter on string columns with WHERE
-- This shows how much of the market is already open to generics

SELECT generic_available,
       COUNT(*)                                AS drug_count,
       ROUND(SUM(annual_revenue_usd_bn), 2)    AS revenue_bn
FROM drugs
GROUP BY generic_available;


-- ── Query 6: Most valuable drugs expiring within 3 years ─────────────────────
-- Combined WHERE with ORDER BY — this gives the most urgent cases
-- These are the drugs that investment analysts worry about most

SELECT drug_name,
       company,
       country,
       patent_expiry_year,
       annual_revenue_usd_bn AS revenue_bn,
       drug_type
FROM drugs
WHERE (patent_expiry_year - 2024) BETWEEN 0 AND 3
  AND generic_available = 'No'
ORDER BY annual_revenue_usd_bn DESC;


-- ── Query 7: German vs non-German company comparison ─────────────────────────
-- I added this query specifically because I'm applying to German universities
-- Wanted to understand Germany's position in the diabetes drug market

SELECT
    CASE WHEN country = 'Germany' THEN 'German Company'
         ELSE 'Non-German Company'
    END AS company_origin,
    COUNT(drug_name)                        AS drugs_tracked,
    ROUND(SUM(annual_revenue_usd_bn), 2)    AS total_revenue_bn
FROM drugs
GROUP BY company_origin;
