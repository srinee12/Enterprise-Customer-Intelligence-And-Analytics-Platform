# Executive insight brief

## How to read this project
This brief describes the analytical lenses built into the dashboard. Because the dataset is synthetic,
treat all displayed numeric outcomes as demonstration outputs, not market facts.

## Business questions and recommended actions
1. **Acquisition efficiency:** Compare revenue per customer, customer volume, and order value by channel.
   Do not optimize on revenue alone; include acquisition cost and incremental lift when real spend data exists.
2. **Customer value:** Use RFM segments to distinguish Champions/Loyal customers from At Risk/Hibernating groups.
   Protect high-value customers with service recovery and relevant loyalty benefits.
3. **Reactivation:** Prioritize customers inactive for 181–365 days, then test personalized win-back journeys.
   Suppress customers with recent complaints until service issues are resolved.
4. **Customer experience:** Review satisfaction alongside support-ticket burden and return behavior.
   Diagnose root causes by issue category before changing policy or staffing.
5. **Regional/category mix:** Compare both customer count and revenue to identify over- or under-indexing.

## Proposed KPI operating cadence
- Weekly: active customers, at-risk share, orders/customer, revenue/customer, support tickets.
- Monthly: acquisition channel mix, RFM migration, cohort retention, repeat purchase rate.
- Quarterly: customer lifetime value, incremental campaign lift, cost-to-serve, NPS/CSAT drivers.

## Limitations and production requirements
- Customer snapshot is not transaction-level history; true repeat-purchase cohorts cannot be reconstructed.
- Rule-based recency risk is not a predictive churn score.
- Revenue is simulated and no acquisition spend/margin data is supplied.
- Validate definitions with Finance, Marketing, and CX before production reporting.
