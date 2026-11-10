-- 1. Revenue and customer contribution by acquisition channel
SELECT acquisition_channel, COUNT(*) AS customers, SUM(total_revenue) AS revenue,
       AVG(total_revenue) AS revenue_per_customer
FROM customers GROUP BY acquisition_channel ORDER BY revenue DESC;

-- 2. Segment economics
SELECT customer_segment, COUNT(*) AS customers, SUM(orders_count) AS orders,
       SUM(total_revenue) AS revenue,
       SUM(total_revenue) / NULLIF(SUM(orders_count),0) AS blended_aov
FROM customers GROUP BY customer_segment ORDER BY revenue DESC;

-- 3. At-risk customer value pool (rule-based: >180 days inactive)
SELECT region, COUNT(*) AS at_risk_customers, SUM(total_revenue) AS historical_revenue
FROM customers WHERE days_since_last_purchase > 180
GROUP BY region ORDER BY at_risk_customers DESC;

-- 4. Satisfaction and support burden
SELECT customer_segment, AVG(satisfaction_score) AS avg_satisfaction,
       AVG(support_tickets) AS avg_tickets, COUNT(*) AS customers
FROM customers GROUP BY customer_segment;

-- 5. Category performance
SELECT preferred_category, COUNT(*) AS customers, SUM(total_revenue) AS revenue
FROM customers GROUP BY preferred_category ORDER BY revenue DESC;

-- 6. Acquisition cohort overview (signup-month proxy)
SELECT DATE_TRUNC('month', signup_date) AS signup_month,
       COUNT(*) AS acquired_customers, SUM(total_revenue) AS lifetime_revenue
FROM customers GROUP BY 1 ORDER BY 1;
