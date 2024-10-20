SELECT b.name AS name, SUM(ri.totalSpent) as total_spend
FROM ReceiptsItems ri
JOIN Brands b
ON ri.brandid = b._id
WHERE userId IN (
    SELECT userId
    FROM Users
    WHERE createdDate >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
)
GROUP BY ri.brandid
ORDER BY total_spend DESC
LIMIT 1
;