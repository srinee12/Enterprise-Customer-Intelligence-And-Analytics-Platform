import pandas as pd
import numpy as np

RFM_LABELS = {
    "Champions": "High-value customers with recent and frequent purchases",
    "Loyal": "Frequent customers with strong monetary value",
    "Potential Loyalists": "Recent customers with room to grow",
    "New Customers": "Recently active, lower purchase frequency",
    "At Risk": "Previously engaged customers with declining recency",
    "Hibernating": "Long-inactive customers with low engagement",
}

def load_customers(path):
    df = pd.read_csv(path, parse_dates=["signup_date", "last_purchase_date"])
    required = {"customer_id", "orders_count", "total_revenue", "days_since_last_purchase"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return clean_customers(df)

def clean_customers(df):
    out = df.copy()
    out["customer_id"] = out["customer_id"].astype(str).str.strip()
    for col in ["orders_count", "total_revenue", "avg_order_value", "days_since_last_purchase",
                "discount_rate", "returns_count", "support_tickets", "satisfaction_score"]:
        if col in out:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    out = out.drop_duplicates(subset=["customer_id"])
    out["orders_count"] = out["orders_count"].fillna(0).clip(lower=0)
    out["total_revenue"] = out["total_revenue"].fillna(0).clip(lower=0)
    out["days_since_last_purchase"] = out["days_since_last_purchase"].fillna(
        out["days_since_last_purchase"].median()
    ).clip(lower=0)
    out["avg_order_value"] = np.where(
        out["orders_count"] > 0,
        out["total_revenue"] / out["orders_count"].replace(0, np.nan),
        0
    )
    return out

def add_rfm_segments(df):
    out = df.copy()
    # Rank first so duplicate quantile boundaries do not break qcut on low-cardinality data.
    out["R_score"] = pd.qcut(out["days_since_last_purchase"].rank(method="first"),
                             5, labels=[5,4,3,2,1]).astype(int)
    out["F_score"] = pd.qcut(out["orders_count"].rank(method="first"),
                             5, labels=[1,2,3,4,5]).astype(int)
    out["M_score"] = pd.qcut(out["total_revenue"].rank(method="first"),
                             5, labels=[1,2,3,4,5]).astype(int)
    score = out["R_score"] + out["F_score"] + out["M_score"]
    conditions = [
        (out["R_score"] >= 4) & (out["F_score"] >= 4) & (out["M_score"] >= 4),
        (out["F_score"] >= 4) & (out["M_score"] >= 3),
        (out["R_score"] >= 4) & (out["F_score"] <= 3),
        (out["R_score"] >= 4) & (out["F_score"] <= 2),
        (out["R_score"] <= 2) & (score >= 8),
    ]
    choices = ["Champions", "Loyal", "Potential Loyalists", "New Customers", "At Risk"]
    out["rfm_segment"] = np.select(conditions, choices, default="Hibernating")
    out["risk_flag"] = np.where(out["days_since_last_purchase"] > 180, "At Risk", "Healthy")
    return out

def calculate_kpis(df):
    customers = len(df)
    revenue = float(df["total_revenue"].sum())
    orders = float(df["orders_count"].sum())
    return {
        "customers": customers,
        "revenue": revenue,
        "aov": revenue / orders if orders else 0.0,
        "orders_per_customer": orders / customers if customers else 0.0,
        "at_risk_share": float((df["days_since_last_purchase"] > 180).mean()) if customers else 0.0,
        "avg_satisfaction": float(df["satisfaction_score"].mean()) if customers and "satisfaction_score" in df else 0.0,
    }
