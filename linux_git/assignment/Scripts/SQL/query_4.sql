-- Provide a table that shows the region for each sales rep along with their associated accounts.
-- Final table columns: region_name, sales_rep_name, account_name
-- Sort accounts alphabetically (A-Z) by account name.

SELECT
    r.name AS region_name,
    s.name AS sales_rep_name,
    a.name AS account_name
FROM
    region r
    JOIN sales_reps s ON s.region_id = r.id
    JOIN accounts a ON a.sales_rep_id = s.id
ORDER BY a.name;