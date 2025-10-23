SELECT page_title, views
FROM pageviews
WHERE timestamp = '2025-10-01 19:00:00'
ORDER BY views DESC
LIMIT 1;