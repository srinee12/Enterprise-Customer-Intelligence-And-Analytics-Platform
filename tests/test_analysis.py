import pandas as pd
from src.analysis import clean_customers, add_rfm_segments, calculate_kpis

def test_clean_removes_duplicate_customer_ids():
    df = pd.DataFrame({"customer_id":["A","A","B"],"orders_count":[1,2,0],
                       "total_revenue":[10,20,0],"days_since_last_purchase":[2,3,400]})
    out = clean_customers(df)
    assert len(out) == 2
    assert out.customer_id.is_unique

def test_rfm_segments_are_populated():
    df = pd.DataFrame({"customer_id":[str(i) for i in range(100)],
                       "orders_count":list(range(100)),
                       "total_revenue":[i*10 for i in range(100)],
                       "days_since_last_purchase":list(range(100)),
                       "satisfaction_score":[4]*100})
    out = add_rfm_segments(df)
    assert out.rfm_segment.notna().all()
    assert set(out.risk_flag.unique()).issubset({"At Risk","Healthy"})

def test_kpi_empty_data_is_safe():
    df = pd.DataFrame({"total_revenue":[],"orders_count":[],"days_since_last_purchase":[],"satisfaction_score":[]})
    k = calculate_kpis(df)
    assert k["customers"] == 0
    assert k["aov"] == 0
