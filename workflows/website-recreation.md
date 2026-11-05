---
description: Pixel-perfect website recreation and marketing page cloning
---

Follow these steps to recreate any landing page or marketing URL with 100% accuracy and professional aesthetics.

### 1. Visual & Structural Discovery
// turbo
1. Use the `browser_subagent` to perform a full-page scan. 
   - Capture high-resolution screenshots of the **Hero**, **Features**, **Pricing**, **FAQ**, and **Footer**.
   - Note the branding (Logo SVG), colors (using browser dev tools), and font families (Google Fonts).

### 2. Deep Data Extraction
// turbo
2. Use `execute_browser_javascript` within the subagent to extract raw text content for complex sections:
   - Extract FAQ pairs: `{question: string, answer: string}`.
   - Extract Pricing details: `Tier, Price, Description, Features`.
   - Extract Stats: `Numerical values and labels`.

### 3. Foundation Building (HTML)
3. Create an `index.html` file using semantic HTML5 elements.
   - Organize content into modular `<section>` blocks.
   - Use descriptive class names for styling (e.g., `.section-hero`, `.service-card`).
   - Implement the navigation and footer structures based on the visual scan.

### 4. Design System Implementation (CSS)
4. Create a `styles.css` file and establish the design system:
   - Define `:root` variables for brand colors (Primary, Accent, Backgrounds).
   - Set up standard resets and typography using the identified Google Fonts.
   - Build a consistent layout grid (using Flexbox or Grid) that matches the original spacing.

### 5. Pixel-Perfect Refinement
5. Iterate on the design by comparing local renders with original screenshots:
   - Match specific design details: tilted backgrounds, offset shadows, unique gradients.
   - Move any temporary styles to the CSS file—ensure zero inline CSS.
   - Use `generate_image` for any complex assets or placeholders if required.

### 6. Responsive Tuning
6. Apply fluid design principles:
   - Use `clamp()` for font sizes to ensure headlines scale perfectly on every screen.
   - Test grid layouts on mobile and tablet views.
   - Ensure the Hero section remains on a single line or follows the exact layout of the target.

### 7. Interactive Polish
7. Add functional elements:
   - FAQ accordions using JavaScript.
   - Fixed/Scrolled header states.
   - Subtle hover animations and button press effects for a "premium" feel.
