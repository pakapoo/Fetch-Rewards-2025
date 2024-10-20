WITH cur_month AS (
  SELECT b.name, COUNT(r._id) as receipts_count, ROW_NUMBER() OVER (ORDER BY COUNT(r._id) DESC) as rank
  FROM ReceiptItems ri
  JOIN Receipts r
  ON ri.receiptid = r._id
  JOIN Brands b
  ON ri.brandid = b._id
  WHERE MONTH(r.dateScanned) = MONTH(CURRENT_DATE())
  GROUP BY b.name
  ORDER BY receipts_count DESC
  LIMIT 5
), prev_month AS (
  SELECT b.name, COUNT(r._id) as receipts_count, ROW_NUMBER() OVER (ORDER BY COUNT(r._id) DESC) as rank
  FROM ReceiptItems ri
  JOIN Receipts r
  ON ri.receiptid = r._id
  JOIN Brands b
  ON ri.brandid = b._id
  WHERE MONTH(r.dateScanned) = MONTH(CURRENT_DATE()) - 1
  GROUP BY b.name
)

SELECT cur_month.name as name, cur_month.rank as cur_rank, prev_month.rank as prev_rank, (cur_month.rank - COALESCE(prev_month.rank, 0)) as rank_change
FROM cur_month
LEFT JOIN prev_month
ON cur_month.name = prev_month.name
;