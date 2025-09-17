-- sql/queries.sql
-- 1) Basic counts
SELECT COUNT(*) AS total_customers FROM customers;
SELECT churn, COUNT(*) AS cnt FROM customers GROUP BY churn;

-- 2) Numeric summaries
SELECT churn, AVG(monthlycharges) AS avg_monthly, AVG(totalcharges) AS avg_total, AVG(tenure) AS avg_tenure
FROM customers GROUP BY churn;

-- 3) churn by contract
SELECT contract, churn, COUNT(*) FROM customers GROUP BY contract, churn ORDER BY contract;

-- 4) suspicious nulls
SELECT COUNT(*) FROM customers WHERE totalcharges IS NULL OR monthlycharges IS NULL;

-- 5) sample rows
SELECT * FROM customers LIMIT 10;
