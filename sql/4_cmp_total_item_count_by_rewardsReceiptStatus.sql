SELECT rewardsReceiptStatus, SUM(purchasedItemCount) as total_item_count
FROM Receipts
WHERE rewardsReceiptStatus IN ('Accepted', 'Rejected')
GROUP BY rewardsReceiptStatus
;