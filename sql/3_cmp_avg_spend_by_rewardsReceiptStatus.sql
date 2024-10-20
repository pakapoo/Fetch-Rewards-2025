SELECT rewardsReceiptStatus, AVG(totalSpent) as avg_spend
FROM Receipts
WHERE rewardsReceiptStatus IN ('Accepted', 'Rejected')
GROUP BY rewardsReceiptStatus
;