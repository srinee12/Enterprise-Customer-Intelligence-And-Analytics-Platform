# Data dictionary

One row represents one customer in a point-in-time synthetic snapshot.

| Field | Definition |
|---|---|
| customer_id | Unique synthetic customer key |
| signup_date | Customer registration date |
| region | Broad operating region |
| acquisition_channel | First-touch acquisition channel (simulated) |
| customer_segment | Consumer, SMB, or Enterprise |
| age / gender | Optional demographic attributes; some values intentionally missing |
| preferred_category | Most-preferred product category |
| orders_count | Number of orders in the observed customer lifetime |
| total_revenue | Simulated cumulative net revenue in INR |
| avg_order_value | Total revenue divided by order count; zero if no orders |
| last_purchase_date | Simulated last purchase date |
| days_since_last_purchase | Recency in days as of 2026-10-31 |
| discount_rate | Simulated average discount rate |
| returns_count | Number of returned orders |
| support_tickets | Number of support tickets |
| satisfaction_score | Simulated satisfaction score from 1 to 5 |
| payment_method | Most-used payment method |
| lifecycle_status | Active, Cooling, or At Risk based on recency |
