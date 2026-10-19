# Advanced Schema.org Entity Graph Templates
# Production-Ready JSON-LD Code Snippets for Rich Search Results

## 1. Organization & Brand Entity Graph (Sitewide)

Place this snippet in your sitewide `<head>` or root layout template:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Brand Name",
      "url": "https://example.com",
      "logo": {
        "@type": "ImageObject",
        "@id": "https://example.com/#logo",
        "url": "https://example.com/assets/logo.png",
        "caption": "Brand Name Logo"
      },
      "sameAs": [
        "https://www.linkedin.com/company/example",
        "https://x.com/example",
        "https://www.facebook.com/example",
        "https://www.wikidata.org/wiki/Q12345"
      ],
      "contactPoint": [
        {
          "@type": "ContactPoint",
          "telephone": "+1-800-555-0199",
          "contactType": "customer service",
          "availableLanguage": ["English"]
        }
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://example.com/#website",
      "url": "https://example.com",
      "name": "Brand Name",
      "publisher": { "@id": "https://example.com/#organization" },
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://example.com/search?q={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    }
  ]
}
</script>
```

---

## 2. E-Commerce Product & Offer Schema

For product detail pages (PDPs) with customer ratings and price specifications:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Pure Marine Collagen Peptides",
  "image": [
    "https://example.com/images/product-front.jpg",
    "https://example.com/images/product-back.jpg"
  ],
  "description": "Hydrolyzed Type 1 & 3 marine collagen with verified 98% bioavailability.",
  "sku": "COLLAGEN-MAR-300G",
  "gtin13": "5060123456789",
  "brand": {
    "@type": "Brand",
    "name": "Brand Name"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/products/marine-collagen",
    "priceCurrency": "GBP",
    "price": "29.99",
    "priceValidUntil": "2027-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "128"
  }
}
</script>
```

---

## 3. High-Converting FAQPage Schema (Rich Results Snippets)

Add to service or commercial pillar pages to trigger expandable FAQ dropdowns in Google Search:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How long does it take to see results?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Most customers report noticeable improvements in joint mobility and skin hydration within 3 to 4 weeks of consistent daily usage."
      }
    },
    {
      "@type": "Question",
      "name": "Is this product third-party lab tested?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, every production batch is independently tested by accredited UK laboratories for purity, heavy metals, and active peptide potency."
      }
    }
  ]
}
</script>
```
