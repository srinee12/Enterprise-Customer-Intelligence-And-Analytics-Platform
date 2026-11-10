import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.analysis import load_customers, add_rfm_segments, calculate_kpis, RFM_LABELS

st.set_page_config(page_title="Customer Intelligence 360", page_icon="📊", layout="wide")
st.markdown("""
<style>
.main {background: #0b1220;}
[data-testid="stMetric"] {background: linear-gradient(135deg,#17243b,#111b2d); padding: 16px; border-radius: 14px; border: 1px solid #263a59;}
[data-testid="stSidebar"] {background: #101a2b;}
h1,h2,h3 {letter-spacing: -.4px;}
div[data-testid="stDataFrame"] {border: 1px solid #263a59; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    return add_rfm_segments(load_customers("data/customers.csv"))

df = get_data()
st.title("📊 Customer Intelligence 360")
st.caption("Executive customer analytics • Segmentation • Retention health • Experience insights")
st.markdown("---")

with st.sidebar:
    st.header("🎛️ Dashboard controls")
    st.caption("Filters update all charts and customer records.")
    region = st.multiselect("Region", sorted(df.region.dropna().unique()), default=sorted(df.region.dropna().unique()))
    segment = st.multiselect("Customer segment", sorted(df.customer_segment.dropna().unique()), default=sorted(df.customer_segment.dropna().unique()))
    channel = st.multiselect("Acquisition channel", sorted(df.acquisition_channel.dropna().unique()), default=sorted(df.acquisition_channel.dropna().unique()))
    lifecycle = st.multiselect("Lifecycle status", sorted(df.lifecycle_status.dropna().unique()), default=sorted(df.lifecycle_status.dropna().unique()))
    rfm = st.multiselect("RFM segment", sorted(df.rfm_segment.unique()), default=sorted(df.rfm_segment.unique()))
    min_revenue, max_revenue = float(df.total_revenue.min()), float(df.total_revenue.max())
    revenue_range = st.slider("Customer revenue range", min_revenue, max_revenue, (min_revenue, max_revenue))
    st.markdown("---")
    st.caption("Dataset: 20,000 synthetic customer records")

f = df[
    df.region.isin(region) &
    df.customer_segment.isin(segment) &
    df.acquisition_channel.isin(channel) &
    df.lifecycle_status.isin(lifecycle) &
    df.rfm_segment.isin(rfm) &
    df.total_revenue.between(revenue_range[0], revenue_range[1])
].copy()

k = calculate_kpis(f)
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Customers", f"{k['customers']:,}")
c2.metric("Revenue", f"₹{k['revenue']:,.0f}")
c3.metric("Avg. order value", f"₹{k['aov']:,.0f}")
c4.metric("Orders / customer", f"{k['orders_per_customer']:.2f}")
c5.metric("At-risk customers", f"{k['at_risk_share']:.1%}")
st.caption(f"Showing {len(f):,} of {len(df):,} customers")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📈 Executive overview", "🧩 Segmentation", "💬 Experience & retention", "🔎 Customer explorer"])

with tab1:
    left,right = st.columns([1.35,1])
    with left:
        st.subheader("Revenue by acquisition channel")
        rev = f.groupby("acquisition_channel", as_index=False).agg(revenue=("total_revenue","sum"), customers=("customer_id","count")).sort_values("revenue",ascending=False)
        fig = px.bar(rev, x="acquisition_channel", y="revenue", color="revenue", text_auto=".2s",
                     color_continuous_scale="Tealgrn", template="plotly_dark")
        fig.update_layout(height=380, xaxis_title="", yaxis_title="Revenue (₹)", coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("Customer mix by lifecycle")
        life = f.lifecycle_status.value_counts().rename_axis("lifecycle").reset_index(name="customers")
        fig = px.pie(life, names="lifecycle", values="customers", hole=.58, template="plotly_dark",
                     color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(height=380, legend_title="")
        st.plotly_chart(fig, use_container_width=True)
    a,b = st.columns(2)
    with a:
        st.subheader("Revenue by preferred category")
        cat = f.groupby("preferred_category",as_index=False).total_revenue.sum().sort_values("total_revenue",ascending=False)
        st.plotly_chart(px.bar(cat,x="preferred_category",y="total_revenue",template="plotly_dark",
                               color="total_revenue",color_continuous_scale="Viridis"),use_container_width=True)
    with b:
        st.subheader("Regional performance")
        reg = f.groupby("region",as_index=False).agg(revenue=("total_revenue","sum"), customers=("customer_id","count"))
        st.plotly_chart(px.scatter(reg,x="customers",y="revenue",size="customers",color="region",
                                   hover_name="region",template="plotly_dark"),use_container_width=True)

with tab2:
    st.subheader("RFM customer segmentation")
    seg = f.groupby("rfm_segment",as_index=False).agg(customers=("customer_id","count"), revenue=("total_revenue","sum"),
                                                     avg_recency=("days_since_last_purchase","mean"))
    seg["revenue_share"] = seg.revenue / max(seg.revenue.sum(),1)
    l,r = st.columns([1.2,1])
    with l:
        st.plotly_chart(px.bar(seg.sort_values("customers",ascending=True),x="customers",y="rfm_segment",
                               orientation="h",color="revenue_share",color_continuous_scale="Teal",
                               template="plotly_dark",text="customers"),use_container_width=True)
    with r:
        st.plotly_chart(px.treemap(seg,path=["rfm_segment"],values="revenue",
                                   color="avg_recency",color_continuous_scale="RdYlGn_r",
                                   template="plotly_dark"),use_container_width=True)
    st.dataframe(seg.assign(revenue_share=seg.revenue_share.map(lambda x:f"{x:.1%}"),
                            avg_recency=seg.avg_recency.round(0)),use_container_width=True,hide_index=True)
    selected = st.selectbox("Segment definition", list(RFM_LABELS.keys()))
    st.info(RFM_LABELS[selected])

with tab3:
    st.subheader("Customer experience signals")
    l,r = st.columns(2)
    with l:
        st.plotly_chart(px.box(f,x="customer_segment",y="satisfaction_score",color="customer_segment",
                               template="plotly_dark",points="outliers"),use_container_width=True)
    with r:
        st.plotly_chart(px.scatter(f,x="support_tickets",y="satisfaction_score",color="lifecycle_status",
                                   size="total_revenue",hover_data=["customer_id"],template="plotly_dark"),
                        use_container_width=True)
    st.subheader("Retention risk diagnostic")
    risk = f.assign(risk_band=pd.cut(f.days_since_last_purchase,[-1,30,90,180,365,100000],
                 labels=["0–30 days","31–90 days","91–180 days","181–365 days","365+ days"]))
    risk_summary = risk.groupby("risk_band",observed=False).agg(customers=("customer_id","count"),
                     revenue=("total_revenue","sum"),satisfaction=("satisfaction_score","mean")).reset_index()
    st.plotly_chart(px.bar(risk_summary,x="risk_band",y="customers",color="risk_band",
                           template="plotly_dark",text="customers"),use_container_width=True)
    st.dataframe(risk_summary.round(2),use_container_width=True,hide_index=True)

with tab4:
    st.subheader("Customer-level drill-down")
    search = st.text_input("Search customer ID")
    view = f.copy()
    if search:
        view = view[view.customer_id.str.contains(search,case=False,na=False)]
    cols = ["customer_id","region","customer_segment","acquisition_channel","orders_count","total_revenue",
            "days_since_last_purchase","rfm_segment","satisfaction_score","lifecycle_status"]
    st.dataframe(view[cols].sort_values("total_revenue",ascending=False),use_container_width=True,hide_index=True)
    st.download_button("⬇️ Download filtered customers (CSV)", view[cols].to_csv(index=False).encode("utf-8"),
                       "customer_intelligence_filtered.csv","text/csv")
    st.caption("Customer-level data is synthetic. Avoid using it to make real customer decisions.")

st.markdown("---")
st.caption("Customer Intelligence 360 • Portfolio project • Synthetic data • Rule-based risk indicators, not a production churn model")
