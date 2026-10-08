# Retention Marketing & Lifecycle Email Automation Playbook
# Scope: Klaviyo / Customer.io Lifecycle Sequences, RFM Segmentation, Churn Mitigation

## 1. The Core Retention Objective
While paid media acquires the first transaction, the lifetime value (LTV) and second-order profitability are built in retention. A 5% increase in customer retention increases profits by 25% to 95%.

---

## 2. The 6 Mandatory Automated Lifecycle Flows

Every brand must have these 6 core automated flows active:

```
+-----------------------------------------------------------------------------+
|                        6 CORE LIFECYCLE FLOWS                               |
+-----------------------------------------------------------------------------+
| 1. Welcome Series (Non-Buyers)    --> 3-4 emails (Brand story, offer, FAQ)  |
| 2. Abandoned Cart                 --> 3 emails (1h, 12h, 24h urgency)      |
| 3. Browse Abandonment             --> 2 emails (Soft reminder, social proof)|
| 4. Post-Purchase Onboarding       --> 4 emails (Usage guide, UGC, reviews)  |
| 5. VIP Customer Nurture           --> Exclusive access, early drops, perks  |
| 6. Win-Back & Sunset Series       --> Re-engagement or unsubscribe prompt   |
+-----------------------------------------------------------------------------+
```

### Detailed Flow Specifications:

### A. Abandoned Cart Flow (High-Converting Architecture)
- **Email 1 (60 minutes post-abandonment)**: "Did you leave something behind?"
  - Tone: Helpful, customer-service oriented. Show exact cart items, clear button: "Return to Cart".
- **Email 2 (18 hours post-abandonment)**: "Still thinking about it?"
  - Tone: Social proof focus. 3 top customer reviews, FAQs, risk-reversal (free returns / 60-day guarantee).
- **Email 3 (36 hours post-abandonment)**: "Your cart expires soon"
  - Tone: Urgency + optional incentive (10% off or free gift) if non-discounted in previous steps.

### B. Post-Purchase & Replenishment Flow
- **Email 1 (Immediate)**: Order confirmation with excitement, unboxing preview.
- **Email 2 (Estimated Delivery Day + 2)**: How-to-use guide, optimal routine instructions, dosage or setup tips.
- **Email 3 (Day 14)**: Check-in & review request (link to Trustpilot, Google Reviews, or native app).
- **Email 4 (Day 25–45, based on consumable cycle)**: Automatic replenishment / reorder reminder with 1-click reorder link.

---

## 3. RFM Segmentation Strategy

Segment customer databases using Recency, Frequency, and Monetary value:

| Segment | Recency | Frequency | Spend | Tactical Action |
| :--- | :--- | :--- | :--- | :--- |
| **Champions / VIPs** | Bought < 30d ago | 3+ orders | Top 10% | Early access to product drops, no discounts needed |
| **Loyal Customers** | Bought < 60d ago | 2+ orders | Average | Cross-sell complementary categories |
| **Potential Loyalists**| Bought < 30d ago | 1 order | Average | Trigger second-purchase offer within 21 days |
| **At-Risk** | Bought 90–150d ago| 2+ orders | High | Send aggressive win-back or personal founder survey |
| **Lost / Dormant** | Bought > 180d ago | Any | Any | 1 win-back attempt; if unread, purge to protect deliverability |

---

## 4. Deliverability & Inbound Health Guardrails

- **Sunset Policy**: Automatically exclude profiles that haven't opened or clicked an email in 90 days from general newsletter campaigns.
- **Domain Authentication**: Ensure strict 100% compliance with Google/Yahoo sender guidelines (DMARC `p=quarantine` or `p=reject`, SPF, DKIM aligned, One-Click Unsubscribe header).
- **Unsubscribe Rate**: Keep campaign unsubscribe rate < 0.25% and spam complaint rate < 0.08%.
