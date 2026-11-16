---
name: website-recreation-cro
description: >-
  Pixel-perfect website recreation, marketing page cloning, design system extraction, and conversion rate optimization (CRO) UI teardown.
---

# Website Recreation & CRO Landing Page Cloning Playbook

Follow this standard procedure to recreate any landing page or marketing URL with 100% visual fidelity, clean responsive code, and conversion-optimized structure.

---

### 1. Visual & Structural Discovery
1. Use the `browser_subagent` to perform a full-page scan:
   - Capture high-resolution screenshots of the **Hero**, **Social Proof / Logos**, **Features / Grid**, **Pricing**, **Testimonials**, **FAQ**, and **Footer**.
   - Inspect branding: logo SVG, color palette (hex codes via dev tools), and typography (Google Fonts / Typekit).

### 2. Deep Data & Content Extraction
2. Extract complete textual and asset content:
   - **FAQ Items**: Questions and direct answers.
   - **Pricing Tiers**: Plan names, billing cadences, feature matrices, and CTA URLs.
   - **Social Proof**: Statistics, client metrics, badge SVGs, and testimonial quotes.

### 3. Semantic HTML5 Foundation
3. Build `index.html` using modular semantic HTML5 elements:
   - Structure sections cleanly (`<header>`, `<main>`, `<section class="hero">`, `<section class="features">`, `<footer>`).
   - Use BEM or utility-class naming conventions.
   - Ensure semantic heading hierarchy (`h1` -> `h2` -> `h3`).

### 4. Design System & CSS Implementation
4. Construct `styles.css` with a unified CSS variable system:
   - Define `:root` variables for brand colors, background surfaces, text contrasts, and spacing scales.
   - Import necessary typography from Google Fonts.
   - Build responsive layout grids using CSS Grid and Flexbox matching original pixel margins.

### 5. Pixel-Perfect Refinement & CRO Hardening
5. Compare local renders side-by-side with original screenshots:
   - Match subtle styling details: backdrop filters (glassmorphism), box shadows, gradient borders, and border radii.
   - Ensure zero inline CSS.
   - Eliminate conversion friction: optimize CTA button contrast, simplify form fields, and establish clear visual hierarchy.

### 6. Fluid Responsive Tuning
6. Apply responsive design principles:
   - Use CSS `clamp()` for headline font sizes to eliminate awkward word wraps across mobile and desktop.
   - Test layout breakpoints on Mobile (375px), Tablet (768px), and Desktop (1440px).

### 7. Interactive Polish & Microinteractions
7. Add functional front-end interactivity:
   - FAQ accordions with smooth CSS transitions.
   - Sticky navigation header with blur on scroll.
   - Hover and focus states on interactive buttons and cards for a premium feel.
