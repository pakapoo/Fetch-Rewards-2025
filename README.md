# Fetch-Rewards-2025
Fetch Rewards Coding Exercise - Analytics Engineer

# Requirements
1. ER diagram based on the given JSON data
2. SQL queries for predetermined business questions
3. Data quality indentification
4. A short email to the business stakeholder

# Part 1: ER diagram

ReceiptItems <rewardsReceiptItemList> -> Brand <barcode>
Receipts <userId> -> Users <_id>
Brands: move out category -> categoryCode 1:1 (normalize to ensure consistency, and easy to maintain)
Receipt: move out ReceiptItems

# Part 2: SQL commands
* What are the top 5 brands by receipts scanned for most recent month?
SELECT COUNT(*) FROM Brands b LEFT JOIN Receipts r ON b.barcode = r.
* How does the ranking of the top 5 brands by receipts scanned for the recent month compare to the ranking for the previous month?
* When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
* When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
* Which brand has the most spend among users who were created within the past 6 months?
* Which brand has the most transactions among users who were created within the past 6 months?