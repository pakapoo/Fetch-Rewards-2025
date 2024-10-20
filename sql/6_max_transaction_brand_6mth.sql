WITH ReceiptsItems_distinct as (
    SELECT DISTINCT brandid, receiptid
    FROM ReceiptsItems
)

SELECT b.name AS name
FROM ReceiptsItems_distinct ri
JOIN Brands b
ON ri.brandid = b._id
WHERE userId IN (
    SELECT userId
    FROM Users
    WHERE createdDate >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
)
GROUP BY ri.brandid
ORDER BY COUNT(*) DESC
LIMIT 1
;