-- Find all company names that start with 'C' or 'W', and where the primary contact contains 'ana' or 'Ana',
-- but does NOT contain 'eana'.

SELECT
    name
FROM
    accounts
WHERE
    (name LIKE 'C%' OR name LIKE 'W%')
    AND (primary_poc ILIKE '%ana%')
    AND (primary_poc NOT ILIKE '%eana%');