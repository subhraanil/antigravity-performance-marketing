# Local SEO & Google Maps Visibility Playbook

## Executive Overview

Local SEO drives commercial visibility across Google Search Local Packs, Google Maps, and localized mobile searches. This playbook provides the definitive operational blueprint to optimize **Google Business Profiles (GBP)**, enforce **NAP (Name, Address, Phone) consistency**, implement **localized Schema graphs**, and build localized authority hubs.

---

## 1. Google Local 3-Pack Ranking Factors

Google's Local Algorithm ranks businesses primarily on three core pillars:
1. **Relevance (Weight: 35%):** How well a local business profile matches what the user is searching for (Primary Category, secondary categories, service listings, on-page localized signals).
2. **Prominence (Weight: 35%):** Offline and online authority (Review count, review velocity, star ratings, local media mentions, backlinks from regional civic/industry sites, structured citations).
3. **Proximity (Weight: 30%):** Distance from the searcher's physical location or specified geographic center.

---

## 2. Google Business Profile (GBP) Optimization Architecture

### Primary Category Selection:
- **Rule of Singularity:** Select the exact primary category matching your highest-margin core service (e.g. "Pet Groomer" vs "Pet Supply Store"). 
- **Secondary Categories:** Add up to 9 secondary categories to capture related intent without diluting the primary focus.

### Business Details Hygiene:
- **Title Optimization:** Use official business name. Avoid keyword-stuffing city or service names into the title unless legally registered (risk of suspension).
- **Service Areas:** Specify explicit ZIP/postal codes and municipalities rather than broad radius rings.
- **Attributes:** Enable all relevant transactional attributes (wheelchair accessible, free consultation, online appointments, etc.).
- **Visual Assets:** Upload high-resolution interior, exterior, team, and work product photos weekly with geotag and naming metadata.

---

## 3. NAP Citation Consistency & Data Aggregators

Discrepancies in Name, Address, or Phone number across directories dilute Google's confidence in your physical location.

### Primary Aggregator Distribution:
Ensure authoritative synchronization across primary tier aggregators:
- **Data Axle (formerly Infogroup)**
- **Localeze / Neustar**
- **Foursquare**
- **YellowPages / YP.com**
- **Apple Business Connect** & **Bing Places for Business**

### Citation Audit Rules:
- Address formatting must match USPS / Royal Mail official postal address exactly (Suite # vs Ste, Street vs St).
- Track citations in a unified register to prevent duplicate or conflicting legacy listings.

---

## 4. Localized JSON-LD Schema Graphs

Deploy nested `LocalBusiness` schema directly on corresponding location landing pages:

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://example.com/#localbusiness",
  "name": "Apex Marketing Hub London",
  "image": "https://example.com/assets/london-office.jpg",
  "telephone": "+44 20 7946 0912",
  "email": "london@example.com",
  "url": "https://example.com/london",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "100 Bishopsgate",
    "addressLocality": "London",
    "postalCode": "EC2N 4AG",
    "addressCountry": "GB"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 51.5154,
    "longitude": -0.0818
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "18:00"
    }
  ],
  "sameAs": [
    "https://www.facebook.com/example",
    "https://www.linkedin.com/company/example",
    "https://maps.google.com/?cid=123456789"
  ]
}
```

---

## 5. Review Velocity & Reputation Mechanics

- **Velocity Over Volume:** 3 fresh 5-star reviews every week significantly outperforms 50 legacy reviews from two years ago.
- **Review Content Optimization:** Train staff or automated follow-up sequences to encourage customers to mention specific services and cities in their reviews (e.g. "Best dog grooming in Wimbledon!").
- **Owner Response SLA:** Respond to 100% of reviews within 48 hours. For negative reviews, offer an offline resolution channel within 2 hours.
