-- PostgreSQL-compatible analytical table
CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    signup_date DATE,
    region VARCHAR(30),
    acquisition_channel VARCHAR(40),
    customer_segment VARCHAR(30),
    age INTEGER,
    gender VARCHAR(30),
    preferred_category VARCHAR(40),
    orders_count INTEGER,
    total_revenue NUMERIC(14,2),
    avg_order_value NUMERIC(12,2),
    last_purchase_date DATE,
    days_since_last_purchase INTEGER,
    discount_rate NUMERIC(5,3),
    returns_count INTEGER,
    support_tickets INTEGER,
    satisfaction_score NUMERIC(2,1),
    payment_method VARCHAR(30),
    lifecycle_status VARCHAR(20)
);
