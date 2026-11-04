# Baruipur Online Homepage UI/UX Redesign
## Detailed Design and Implementation Specification

**Website:** https://baruipur.online/  
**Project:** Homepage UI/UX improvement  
**Document purpose:** Provide a clear, implementation-ready brief for an AI coding agent, UI designer, or frontend developer.

---

## 1. Project Objective

Redesign the Baruipur Online homepage as a modern Bengali local news and information portal. The website should combine the clarity of a regional newspaper with the usefulness of a local directory.

The redesign must help visitors:

1. Find the latest local news quickly.
2. Identify the most important stories at a glance.
3. Reach local information such as doctors, schools, train updates, civic services, restaurants, markets, landmarks, and emergency resources.
4. Navigate comfortably on mobile devices.
5. Read Bengali content comfortably with consistent typography.
6. Trust the site through clear publication metadata, consistent layouts, and accessible design.

### Core design principle

**Improve information hierarchy and usability without removing useful content or changing the website’s identity unnecessarily.**

Do not redesign the site as a generic corporate website, ecommerce store, or overly decorative blog.

---

## 2. Important Constraints

Before implementation:

- Inspect the existing homepage, header, footer, article templates, category pages, and current navigation.
- Identify the existing framework, CSS approach, reusable components, and content source.
- Preserve all working routes and existing content.
- Do not change existing URLs, slugs, canonical URLs, or metadata unless explicitly requested.
- Do not delete or hide important directory categories.
- Do not create fake news, fake article titles, fake publication dates, fake authors, or fake directory listings.
- Use real content and images already available on the website.
- If content is unavailable, use clearly marked placeholders only in a design prototype. Do not publish placeholder content.
- Keep the homepage lightweight and responsive.
- Avoid unnecessary dependencies and large animation libraries.
- Do not make changes to article pages or other templates unless required for shared components or explicitly approved.
- Keep existing English and Bengali content intact. This task is primarily a presentation and UX redesign.

---

## 3. Brand and Visual Direction

### Design style

Use a modern editorial design with:

- White and light-gray surfaces.
- Strong Bengali headlines.
- A compact navigation bar.
- A clear breaking-news strip.
- Image-led featured news.
- Consistent news cards.
- An easy-to-scan local information directory.
- Restrained use of accent colors.
- Minimal shadows and rounded corners.
- Clear spacing between sections.

The website should feel like a trustworthy local publication, not a crowded link directory.

### Suggested color system

Use the following as the starting palette. First inspect the existing logo and brand assets. If the current logo uses a different established palette, adapt these colors to preserve brand consistency.

| Token | Hex | Usage |
|---|---|---|
| `--color-primary` | `#102A43` | Header, footer, primary brand areas |
| `--color-accent` | `#C62828` | Breaking news, active navigation, important labels |
| `--color-text` | `#263238` | Main body text |
| `--color-muted` | `#64748B` | Metadata, secondary text |
| `--color-background` | `#FFFFFF` | Main page background |
| `--color-surface` | `#F3F5F7` | Section backgrounds and secondary surfaces |
| `--color-border` | `#E5E7EB` | Card borders and separators |
| `--color-footer-text` | `#CBD5E1` | Text on dark footer surfaces |

#### Color usage rules

- Use navy for the main brand structure.
- Use red only for meaningful emphasis, such as breaking news, selected navigation, or important labels.
- Do not make every heading, button, and link red.
- Maintain readable contrast between text and backgrounds.
- Avoid gradients unless the current brand already uses them.
- Do not use color alone to communicate a status.

### Suggested CSS variables

```css
:root {
  --color-primary: #102A43;
  --color-accent: #C62828;
  --color-text: #263238;
  --color-muted: #64748B;
  --color-background: #FFFFFF;
  --color-surface: #F3F5F7;
  --color-border: #E5E7EB;

  --font-bengali: "Hind Siliguri", "Noto Sans Bengali", sans-serif;
  --content-width: 1200px;

  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;

  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
}
```

Adjust these values to match the existing project conventions instead of duplicating an established design-token system.

---

## 4. Bengali Typography

Typography is a core part of the redesign. Bengali text must remain readable across desktop and mobile.

### Preferred font

**Hind Siliguri** is the recommended primary font for the interface and Bengali content.

Google Fonts:
https://fonts.google.com/specimen/Hind+Siliguri

Alternative:
- Noto Sans Bengali: https://fonts.google.com/specimen/Noto+Sans+Bengali
- Tiro Bangla: https://fonts.google.com/specimen/Tiro+Bangla

Use one primary font family for the site. Do not load multiple Bengali families unless there is a specific editorial reason.

### Recommended font weights

Use only the weights required by the interface:

- 400: body text
- 500: navigation and supporting labels
- 600: card titles and section headings
- 700: main headlines

Avoid loading every available font weight.

### Type scale

| Element | Desktop | Mobile |
|---|---:|---:|
| Main featured headline | 32–40px | 25–30px |
| Section heading | 23–26px | 20–22px |
| News card headline | 19–22px | 18–20px |
| Body and summary | 17–18px | 16–17px |
| Navigation | 15–16px | 14–15px |
| Metadata | 13–14px | 12–13px |
| Category label | 13–14px | 12–13px |

### Line-height and Bengali rendering

- Body text: approximately `1.6`.
- Headlines: approximately `1.35–1.45`.
- Navigation: approximately `1.4`.
- Avoid tight line-height that clips Bengali vowel marks or conjunct characters.
- Do not apply letter spacing to Bengali text.
- Test long Bengali words and headlines at narrow widths.
- Avoid fixed-height text containers that crop Bengali glyphs.
- Prefer line clamping only where the content remains available on the linked article page.

Example:

```css
body {
  font-family: var(--font-bengali);
  font-size: 16px;
  line-height: 1.6;
  color: var(--color-text);
}

h1,
h2,
h3 {
  line-height: 1.4;
  letter-spacing: normal;
}
```

### Font loading

- Prefer a locally hosted font or a properly optimized font request if the project supports it.
- Use `font-display: swap`.
- Preload only the font file needed for above-the-fold text.
- Avoid preloading several weights or language subsets unnecessarily.
- Check for layout shift during font loading.

---

## 5. Homepage Information Architecture

Use this recommended section order:

1. Main header and navigation
2. Breaking-news ticker
3. Featured news / hero editorial grid
4. Quick Access directory
5. Latest news feed
6. News category sections
7. Local directory highlights
8. Baruipur guides and evergreen information
9. Optional community or special feature section
10. Footer

The hero and latest news should receive the strongest visual priority. Directory content should remain easy to find but should not compete with the main news story.

Do not repeat the same article in several homepage sections unless the editorial system intentionally marks it as featured.

---

## 6. Header and Navigation

### Desktop header

Recommended structure:

- Logo on the left.
- Main navigation in the center.
- Search control on the right.
- Optional menu or utility control on the far right.
- Breaking-news ticker on a separate row below the main navigation.

The header should be compact. Avoid making it so tall that the user sees very little content before scrolling.

### Navigation categories

Use a concise set of top-level categories. The exact labels should be mapped to existing site routes.

Suggested grouping:

| Main item | Possible submenu items |
|---|---|
| সংবাদ | সর্বশেষ, রাজনীতি, অপরাধ, স্বাস্থ্য |
| ডিরেক্টরি | ডাক্তার, স্কুল, প্রতিষ্ঠান, ক্লাব |
| নাগরিক পরিষেবা | পৌরসভা, জরুরি নম্বর, সরকারি অফিস |
| বারুইপুর গাইড | বাজার, রেস্তোরাঁ, দর্শনীয় স্থান |
| ট্রেন ও যাতায়াত | লোকাল ট্রেন, পরিবহন |

Rules:

- Do not display every subcategory in the main navigation.
- Use dropdowns only where necessary.
- Dropdowns must work with keyboard, mouse, and touch.
- Keep the active page/category visually clear.
- Use the existing URLs and routes.
- Provide a visible focus state.
- Do not use hover-only navigation that becomes inaccessible on mobile.

### Mobile header

- Use a compact header with the logo, search, and menu.
- The menu should open a clear, scrollable navigation panel.
- Keep the search accessible without requiring several taps.
- Ensure the header does not occupy too much vertical space.
- If sticky, ensure it does not cover anchor targets or page content.

---

## 7. Breaking-News Ticker

Place a compact ticker below the main header.

### Design

- Red or dark accent background.
- A text label such as “BREAKING” or the appropriate Bengali equivalent.
- One current headline at a time, or a short list that can be navigated.
- Clear link to the full article.

### Behavior

- Do not use fast or continuous movement by default.
- Avoid auto-scrolling text if it harms readability.
- If animation is used, respect `prefers-reduced-motion`.
- Do not use a ticker for old or evergreen stories.
- If no breaking news is available, hide the ticker or use a non-breaking latest-news strip. Do not invent an item.

---

## 8. Featured News / Hero Section

### Desktop layout

Use an editorial grid:

- One large featured story.
- Two or three smaller secondary stories.
- Main image and headline receive the strongest emphasis.
- Category, publication time, and optional short summary are visible.
- Keep the layout balanced and aligned.

A possible layout is:

```text
+------------------------------------+----------------------+
|                                    | Secondary story 1    |
| Main featured story                +----------------------+
| Large image                        | Secondary story 2    |
| Headline and summary               +----------------------+
|                                    | Secondary story 3    |
+------------------------------------+----------------------+
```

Use actual content from the CMS. The diagram is only a layout reference.

### Mobile layout

- Show the main story first.
- Use a single-column layout.
- Secondary stories follow below.
- Do not squeeze a desktop multi-column grid into a narrow screen.
- Keep the headline readable without excessive truncation.

### Carousel guidance

Prefer a static editorial grid over a carousel for the main hero.

If the existing carousel must remain:

- Provide visible previous/next controls.
- Do not autoplay by default.
- If autoplay is retained, use a slow interval and allow pause.
- Support keyboard interaction.
- Use accessible labels for controls.
- Ensure the active slide and all story links are accessible.
- Avoid placing critical information only in a slide that users may never see.

---

## 9. Quick Access Directory

The local directory is a major utility of Baruipur Online. Preserve its useful destinations while improving visual scanning.

### Recommended categories

Map these to existing routes where available:

- ডাক্তার ও স্বাস্থ্য
- ট্রেন আপডেট
- স্কুল ও শিক্ষা
- গুরুত্বপূর্ণ স্থান
- নাগরিক পরিষেবা
- খাবার ও রেস্তোরাঁ
- বাজার ও শপিং
- ক্লাব ও প্রতিষ্ঠান
- জরুরি পরিষেবা
- আরও

Do not create new destination pages unless that is part of a separate approved content project.

### Visual design

Use a compact icon grid:

- Desktop: 4 to 6 columns depending on available width.
- Tablet: 3 or 4 columns.
- Mobile: 3 columns, or 2 columns if Bengali labels become cramped.
- Each item has one simple icon and a short label.
- Use a light-gray or white card surface.
- Use a subtle border or hover state.
- Avoid heavy shadows and decorative gradients.

### Interaction

- Entire card should be clickable.
- Use semantic links, not generic clickable `div` elements.
- Provide a minimum touch target of 44 × 44 CSS pixels.
- Include keyboard focus styling.
- Icons should be decorative when the text label already describes the destination.
- Do not use emoji as the main icon system.

---

## 10. Latest News Feed

Create a clear “সর্বশেষ সংবাদ” or equivalent latest-news section.

### News item structure

Each item should include:

1. Thumbnail image
2. Category label
3. Headline
4. Publication date/time
5. Optional short summary
6. Link to the article

### Desktop

Use a consistent card grid or a main feed with a sidebar only if the current content and layout support it.

### Mobile

Prefer a compact horizontal news item:

- Image on the left.
- Text on the right.
- Image width around 100–120px where space permits.
- Headline should remain readable.
- Metadata should not overwhelm the headline.

### Card rules

- Use a consistent image ratio, preferably 16:9 for larger cards.
- Use 1:1 or 4:3 thumbnails for compact list items if that fits the design.
- Limit summaries to 2 or 3 lines.
- Keep card padding consistent.
- Avoid excessive border radius.
- Avoid repeating the same story in multiple sections.
- Do not show “minutes ago” if the underlying timestamp is missing or invalid.
- Display publication and update dates accurately.

---

## 11. News Category Sections

Use category sections to help visitors explore topics.

Possible categories include:

- স্থানীয় সংবাদ
- রাজনীতি ও প্রশাসন
- স্বাস্থ্য
- শিক্ষা
- অপরাধ
- ব্যবসা ও বাজার
- সংস্কৃতি ও উৎসব
- খেলাধুলা, if the site has relevant content

Each category block should include:

- Clear section heading.
- “সব দেখুন” link.
- One lead story or a small set of cards.
- Consistent card styling.
- No empty category section.

Do not add every category to the homepage. Prioritize categories with useful, current content.

If a category has no recent content, either omit it or show evergreen content only when clearly identified.

---

## 12. Local Directory Highlights and Evergreen Guides

After the latest news, present useful local information in a separate section.

Potential topics:

- Doctors and clinics
- Schools and education
- Train and transport information
- Markets and shopping
- Restaurants and food
- Important places and landmarks
- Civic services
- Emergency contact information
- Local festivals and community guides

### Presentation

- Use a section heading that clearly signals local utility.
- Use cards or short lists.
- Include a brief descriptive label.
- Link to the relevant guide or directory.
- Do not present directory listings as news.
- Keep news and evergreen information visually distinct.

### Editorial accuracy

For time-sensitive details such as train schedules, phone numbers, admission dates, or office hours:

- Show the last verified date where appropriate.
- Do not imply that information is current if it has not been checked.
- Avoid publishing unsupported contact details.
- Provide a way to report outdated information if the site supports it.

---

## 13. Search UX

Make search easy to find in the header.

### Search field

Suggested Bengali placeholder:

`বারুইপুরে কী খুঁজছেন? ডাক্তার, ট্রেন, স্কুল, খবর...`

### Search behavior

Search should support:

- Bengali queries.
- English queries.
- Common transliterations where the existing search system supports them.
- News headlines and article content.
- Directory pages and local guides.

Possible suggestions:

- Baruipur doctor
- বারুইপুর ডাক্তার
- Train timings
- ট্রেনের সময়
- School admission
- স্কুল ভর্তি
- Municipality services
- Local restaurants

### UX requirements

- Provide a clear submit action.
- Support Enter key submission.
- Do not show suggestions that are not backed by real content.
- Provide a useful empty state.
- Keep search results readable on mobile.
- Do not add a new search service or dependency without approval.

---

## 14. Mobile-First Design Requirements

Test the homepage at minimum at:

- 320px
- 360px
- 390px
- 430px
- 768px
- 1024px
- 1280px
- 1440px

### Mobile rules

- No horizontal page overflow.
- No clipped Bengali glyphs.
- No overlapping header, ticker, or bottom navigation.
- Avoid tiny text and tightly packed links.
- Use a single-column hero.
- Use 3-column quick access cards only when labels fit comfortably.
- Ensure image crops retain the important subject.
- Make tap targets at least 44 × 44 CSS pixels.
- Keep important content accessible without hover.
- Use sufficient space between adjacent controls.

### Optional bottom navigation

A fixed mobile bottom navigation may be used if it improves the existing experience.

Suggested items:

- হোম
- সংবাদ
- খুঁজুন
- ডিরেক্টরি
- আরও

Use it only if:

- It does not duplicate or confuse the main menu.
- It does not cover content.
- It includes safe-area padding on supported devices.
- It has accessible labels and focus states.
- The current site structure supports these destinations.

If used, add enough bottom padding to the page so the final content and footer remain reachable.

---

## 15. Spacing, Containers, and Layout

### Main content width

Use a centered content container with a maximum width around 1200px, adjusted to the existing site.

```css
.container {
  width: min(100% - 32px, 1200px);
  margin-inline: auto;
}
```

For small mobile screens, use approximately 16px side padding.

### Spacing rules

- Use a consistent spacing scale.
- Give major sections 32–48px vertical separation on desktop.
- Give major sections 24–32px vertical separation on mobile.
- Use 12–20px inside cards depending on card size.
- Avoid large blank spaces that push useful content far below the fold.
- Keep section heading and section content visually connected.

### Card styling

- Use a subtle border.
- Use a consistent radius, typically 8–14px.
- Avoid deep shadows.
- Keep image and text edges aligned.
- Use consistent card heights only where it does not crop content.

---

## 16. Images and Media

### Image selection

- Use actual website images and article media.
- Do not replace real local reporting images with unrelated stock images.
- Do not use AI-generated images as factual news photography.
- Do not fabricate local events or people.
- Use neutral placeholders only in non-production mockups.

### Image treatment

- Use `object-fit: cover` for editorial thumbnails.
- Set a consistent aspect ratio.
- Ensure focal subjects are not cut off.
- Use a suitable `object-position` when needed.
- Avoid large image files when a smaller responsive version is available.

### Performance

- Use WebP or AVIF where supported by the current image pipeline.
- Provide responsive image sources or framework image components.
- Lazy-load below-the-fold images.
- Do not lazy-load the main LCP/hero image.
- Set image width and height or aspect ratio to prevent layout shift.
- Avoid loading multiple copies of the same image at different sizes unnecessarily.

---

## 17. Accessibility

Target WCAG 2.2 AA practices where practical.

Requirements:

- Use semantic `header`, `nav`, `main`, `section`, and `footer` landmarks.
- Use a logical heading hierarchy.
- Provide visible keyboard focus.
- Ensure all interactive elements work with keyboard input.
- Use descriptive link text.
- Provide alt text for meaningful images.
- Use empty alt text for decorative images.
- Maintain adequate text contrast.
- Do not rely on color alone for status or category.
- Respect `prefers-reduced-motion`.
- Make menus, search, and carousel controls accessible.
- Ensure the page remains usable at 200% zoom.
- Avoid fixed heights that crop text.

---

## 18. SEO and Structured Content

This is a UI redesign, but it must preserve the site's SEO foundations.

### Preserve

- Existing page URLs and slugs.
- Canonical URLs.
- Existing title tags and meta descriptions unless separately approved.
- Article schema and breadcrumb schema already in use.
- Internal links to existing content.
- Existing Bengali and English content.
- Existing indexability settings.

### Homepage semantic structure

- Use one clear primary `h1`.
- Use `h2` for major homepage sections.
- Use `h3` for individual story or card headings where appropriate.
- Do not use headings only to style text.
- Keep article titles as links to the article.
- Use descriptive anchor text.

### Structured data

Do not add duplicate or conflicting schema.

If structured data is already implemented:

- Preserve it.
- Verify that the visual content matches the schema.
- Avoid marking directory content as news articles.
- Do not invent publication dates, authors, ratings, or organization details.

Any schema changes should be handled carefully and tested separately.

---

## 19. Performance Requirements

The redesigned homepage should remain fast on mobile networks.

### Implementation requirements

- Avoid unnecessary JavaScript.
- Avoid large animation packages.
- Use CSS for simple hover and transition effects.
- Lazy-load below-the-fold media.
- Optimize font loading.
- Prevent layout shift.
- Avoid excessive DOM nesting.
- Avoid loading hidden carousel slides with large media if not needed.
- Reuse existing components and dependencies.
- Do not add a dependency for a simple icon or layout feature if the project already has an equivalent.

### Core Web Vitals goals

Use these as practical targets, measured with real tools and representative devices:

- LCP: 2.5 seconds or less.
- INP: 200 milliseconds or less.
- CLS: 0.1 or less.

Do not claim these targets are met without measurement.

---

## 20. Suggested Component Structure

Adapt component names to the existing codebase. Do not create duplicate components if equivalent ones already exist.

```text
Homepage
├── SiteHeader
│   ├── BrandLogo
│   ├── PrimaryNavigation
│   ├── SearchControl
│   └── MobileMenu
├── BreakingNewsTicker
├── FeaturedNews
│   ├── LeadStory
│   └── SecondaryStories
├── QuickAccessDirectory
│   └── QuickAccessItem
├── LatestNewsSection
│   └── NewsCard / NewsListItem
├── NewsCategorySection
├── LocalDirectoryHighlights
├── LocalGuidesSection
└── SiteFooter
```

### Component principles

- Keep data separate from presentation where the current framework supports it.
- Reuse existing article and category data models.
- Avoid hardcoding article content into the homepage component.
- Use stable keys when rendering lists.
- Keep component props clear and typed if the project uses TypeScript.
- Avoid unnecessary client-side state.
- Prefer server-rendered content where appropriate for SEO and performance.
- Ensure loading, empty, and error states are handled where data is asynchronous.

---

## 21. Suggested Implementation Workflow

### Phase 1: Audit

1. Inspect the current homepage at desktop and mobile sizes.
2. Inspect the existing logo and brand colors.
3. Identify current routes and navigation destinations.
4. Identify existing components and styles.
5. Identify the current source of news and directory content.
6. Record any layout or accessibility issues.
7. Confirm the framework and build process.

### Phase 2: Design system

1. Define color tokens.
2. Define typography and font loading.
3. Define spacing and container widths.
4. Define card and button styles.
5. Define responsive breakpoints.
6. Confirm the design against the actual logo.

### Phase 3: Homepage layout

1. Simplify the header.
2. Implement the breaking-news strip.
3. Redesign the featured news area.
4. Redesign Quick Access.
5. Improve latest-news cards.
6. Organize category sections.
7. Improve directory highlights and guides.
8. Refine the footer.

### Phase 4: Responsive and accessibility QA

1. Test all target viewport widths.
2. Test navigation with keyboard.
3. Test search behavior.
4. Check Bengali font rendering.
5. Check image crops.
6. Check tap target sizes.
7. Check page overflow and sticky elements.
8. Test reduced-motion preferences.

### Phase 5: Performance and SEO QA

1. Check image sizes and loading behavior.
2. Check font loading and layout shift.
3. Confirm semantic headings.
4. Confirm internal links and routes.
5. Confirm canonical and metadata are unchanged.
6. Run Lighthouse or equivalent checks.
7. Fix regressions before deployment.

---

## 22. Acceptance Criteria

The redesign is complete only when all applicable criteria below are satisfied.

### Visual and layout

- [ ] Homepage has a clear editorial hierarchy.
- [ ] Header is compact and navigation is understandable.
- [ ] Breaking-news strip appears only when appropriate.
- [ ] Featured news is visually distinct.
- [ ] Quick Access uses a clear and consistent grid.
- [ ] News cards use consistent image ratios and spacing.
- [ ] Section headings and links are consistent.
- [ ] Color use is restrained and accessible.
- [ ] Bengali typography is consistent.

### Responsive behavior

- [ ] No horizontal overflow at 320px and above.
- [ ] Mobile hero uses a single-column layout.
- [ ] Quick Access labels fit without clipping.
- [ ] Header and menu work on touch devices.
- [ ] Sticky elements do not cover content.
- [ ] Bottom navigation, if used, does not cover the footer.

### Content and functionality

- [ ] Existing homepage content is preserved.
- [ ] Existing URLs and routes continue to work.
- [ ] News cards link to the correct articles.
- [ ] Directory cards link to the correct pages.
- [ ] Search works with Bengali and English input where supported.
- [ ] No fake content or fabricated metadata is published.
- [ ] No important category has been removed without approval.

### Accessibility and performance

- [ ] Keyboard navigation works.
- [ ] Focus states are visible.
- [ ] Meaningful images have suitable alt text.
- [ ] Bengali glyphs are not clipped.
- [ ] Images reserve space to prevent layout shift.
- [ ] Below-the-fold images are lazy-loaded.
- [ ] Hero image loading is prioritized appropriately.
- [ ] No unnecessary dependency or animation has been introduced.
- [ ] Performance is measured rather than assumed.

### SEO

- [ ] Existing metadata and canonical URLs are preserved.
- [ ] Heading hierarchy is logical.
- [ ] Internal links remain crawlable.
- [ ] Structured data is not duplicated or contradicted.
- [ ] No indexability or robots settings have changed unintentionally.

---

## 23. Final Instructions for the AI Developer

Implement the redesign directly in the existing Baruipur Online codebase.

Before writing code, inspect the current implementation and identify the safest way to reuse existing components and content.

Prioritize:

1. Readability of Bengali content.
2. Clear news hierarchy.
3. Quick access to local information.
4. Mobile usability.
5. Fast loading.
6. Preservation of existing SEO and routes.

Do not rebuild the entire site unnecessarily. Do not change the site's content strategy, URL structure, or brand identity as part of this task.

After implementation, provide a concise summary of:

- Files changed.
- Components updated or created.
- Responsive behavior implemented.
- Accessibility improvements.
- Performance optimizations.
- Any remaining issues or decisions requiring approval.

The final result should be a polished, readable, modern local news and information homepage that feels native to Baruipur Online and works well for Bengali-speaking users on mobile and desktop.
