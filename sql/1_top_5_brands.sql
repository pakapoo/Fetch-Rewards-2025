SELECT b.name, COUNT(r._id) as receipts_count
FROM ReceiptItems ri
JOIN Receipts r
ON ri.receiptid = r._id
JOIN Brands b
ON ri.brandid = b._id
WHERE MONTH(r.dateScanned) = MONTH(CURDATE())
GROUP BY b.name
ORDER BY receipts_count DESC
LIMIT 5
;