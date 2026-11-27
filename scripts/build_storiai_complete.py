import os
import sys
import json
import csv
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

# Ensure scripts directory is in sys.path
sys.path.append(r"C:\Users\test\Videos\Office\scripts")
from generate_issue_only_report_engine import build_docx_report, build_pdf_report

office_out_dir = r"C:\Users\test\Videos\Office\website audit\storiai.ai"
workspace_out_dir = r"website audit/storiai.ai"
os.makedirs(office_out_dir, exist_ok=True)
os.makedirs(workspace_out_dir, exist_ok=True)

# 1. Audit Data Payload
audit_data = {
    "client_name": "StoriAI",
    "domain": "https://storiai.ai/",
    "primary_service": "https://storiai.ai/create-story",
    "core_offering": "AI-Powered Personalized Storytelling Platform for Children & Families",
    "technology_stack": "Client-Side Rendered (CSR) React SPA (Vite + Redux + MUI) on AWS / Nginx",
    "audit_date": "November 5, 2026 (Empirically Verified via Screaming Frog, PageSpeed & HTTP Probes)",
    "domain_authority_summary": "Lighthouse: Mobile LCP 19.4s | Speed Index 17.6s | Desktop Perf 69 | Mobile Perf 63 | 0 Crawlable Links (CSR)",
    "health_score": 22,
    "badge_text": "Single Page Application (CSR) Technical SEO & Core Web Vitals Audit",
    "report_title": "TECHNICAL SEO & WEB PERFORMANCE AUDIT REPORT",
    "meta_items": [
        ("Target Website:", "https://storiai.ai/"),
        ("Core Platform / Product:", "StoriAI - AI Children's Emotion-Aware Storytelling Platform"),
        ("Technology Architecture:", "Client-Side Rendered (CSR) React SPA (Vite + Redux + MUI) on AWS / Nginx"),
        ("Audit Crawl Baseline:", "Screaming Frog Raw Crawl (1 URL, 0 outlinks) vs 61 React Router Internal Routes"),
        ("Performance Benchmark:", "Google PageSpeed Insights: Mobile LCP 19.4s | Speed Index 17.6s | Desktop LCP 3.4s"),
        ("Technical Health Rubric Score:", "22 / 100 (Internal Agency Diagnostic Rubric — Critical Remediation Required)")
    ],
    "executive_summary": [
        {
            "bold_prefix": "Executive Context & Architectural Lockout: ",
            "text": "StoriAI (https://storiai.ai/) is an innovative AI-powered personalized storytelling SaaS designed to nurture emotional intelligence, imagination, and bedtime comfort in children ('Where Your Child\\'s Emotions Become Stories'). The application is architected as a pure Client-Side Rendered (CSR) Single Page Application using React (Vite bundler), Redux Toolkit, Material-UI (Emotion CSS-in-JS), and React Router DOM, hosted on AWS EC2 (us-east-2) behind an Nginx 1.31.8 reverse proxy. While the platform contains extensive, high-converting commercial copy (How it Works, Pricing, FAQs, Multilingual stories, COPPA safety, Story galleries), it is completely invisible to search engines and web crawlers because 100% of its content and navigation links require client-side JavaScript execution."
        },
        {
            "bold_prefix": "Screaming Frog Raw Crawl & Routing Inspection: ",
            "text": "When crawled in standard HTTP/raw HTML mode, Screaming Frog crawled exactly 1 URL (https://storiai.ai/) and terminated immediately. The server delivers a bare 1,123-byte HTML shell containing only an empty <div id='root'></div> and a script reference to /assets/index-CVHzEv9o.js. The raw HTML contains 0 body words, 0 internal links, a 7-character title ('StoriAI'), an empty meta description, 0 H1 headings, 0 H2 headings, and 0 canonical tags. Decompilation of the 1.52MB application chunk (App-XFfRbN91.js) revealed at least 61 internal client-side routes (including /about, /pricing, /faq, /contact, /stories-across-languages, /child-landing, /choose-plan, /create-story, /library, /comic). Furthermore, Nginx enforces a blanket SPA catch-all rule (try_files $uri $uri/ /index.html;) that improperly returns HTTP 200 with the HTML index shell for /robots.txt, /sitemap.xml, and all non-existent URLs (Soft 404 trap)."
        },
        {
            "bold_prefix": "Google PageSpeed Insights & Real-User Performance Crisis: ",
            "text": "Official PageSpeed Insights (Lighthouse 13.6.0) exposes an acute performance failure on mobile devices: Mobile Performance Score is 63/100, Largest Contentful Paint (LCP) is an alarming 19.4 seconds (against Google\\'s 2.5s benchmark), and Speed Index is 17.6 seconds. On Desktop, Performance is 69/100 with an LCP of 3.4 seconds and Speed Index of 5.9 seconds. Crucially, synthetic tools report fast First Contentful Paint (0.2s desktop / 0.8s mobile) because the blank 1.1KB shell paints background color #FFD9D1 instantly. However, real users wait 19.4 seconds on mobile while the browser downloads an enormous 4,429 KiB (4.4 MB) uncompressed network payload, parses JavaScript for 3.7 seconds of blocking main-thread time, and initializes eager background WebSockets (Ably Realtime and TTS). Nginx completely lacks Gzip/Brotli compression and sets Cache-Control: None across all static assets (Lighthouse estimated cache savings: 4,633 KiB Desktop / 4,323 KiB Mobile)."
        }
    ],
    "scorecard": [
        ["Crawlability & Bot Rendering", "10", "1 / 10", "Critical", "100% CSR lockout; raw HTML contains 0 outlinks, 0 text, terminating crawler at 1 URL."],
        ["Indexability & Sitemaps", "10", "1 / 10", "Critical", "No robots.txt (HTML SPA fallback); no XML sitemap; 0 canonical tags across all routes."],
        ["URL & Architecture Hygiene", "10", "2 / 10", "Critical", "Both www and non-www return 200 OK; port :443 leaked in 301; trailing slash duplicate; Soft 404 trap."],
        ["SERP Metadata & Snippets", "10", "2 / 10", "Critical", "Title is 7 chars ('StoriAI'); meta description is empty 0 chars; 0 OpenGraph/Twitter cards."],
        ["Mobile & Core Web Vitals", "10", "2 / 10", "Critical", "Mobile LCP is 19.4s (7.7x threshold); Speed Index 17.6s; 3.7s main-thread JS execution."],
        ["Heading Hierarchy (H1/H2)", "10", "3 / 10", "Poor", "0 H1 and 0 H2 in server HTML; headings only exist inside client-side JS bundle."],
        ["Content Architecture & Depth", "10", "5 / 10", "Warning", "Rich emotional storytelling copy exists in React code, but 0 words delivered to search crawlers."],
        ["Structured Data (Schema.org)", "10", "1 / 10", "Critical", "0 Schema.org JSON-LD tags site-wide; missing Organization, WebApplication, and FAQPage."],
        ["Asset Delivery & Caching", "10", "2 / 10", "Critical", "Cache-Control is None across all JS/CSS; no Gzip/Brotli compression on 1.52MB bundle."],
        ["Security & Server Headers", "10", "3 / 10", "Warning", "Missing HSTS, CSP, X-Frame-Options, nosniff; server header leaks 'nginx/1.31.8'."],
        ["TOTAL DIAGNOSTIC RUBRIC SCORE", "100", "22 / 100", "Critical Remediation Required", "Ten 10-point categories derived strictly from Screaming Frog crawl, PageSpeed, and live probes."]
    ],
    "issues": [
        {
            "title": "Total Search Engine Crawl Lockout via 100% Client-Side Rendering (CSR)",
            "severity": "Critical",
            "urls": "Site-wide (All 61 internal routes locked inside client-side React bundle)",
            "impact": "The server delivers an empty 1,123-byte HTML shell with <div id='root'></div> and no pre-rendered markup. Search crawlers that do not execute heavy JavaScript (Bing, Yahoo, DuckDuckGo, social scrapers, and AI bots like GPTBot, ClaudeBot, Perplexity) see zero words, zero headings, and zero outlinks. Screaming Frog terminates after crawling only 1 URL because no anchor links exist in the server response. Even Googlebot's second-wave rendering queue experiences severe indexing delays and timeouts."
        },
        {
            "title": "Catastrophic Mobile Core Web Vitals: LCP 19.4s & Speed Index 17.6s",
            "severity": "Critical",
            "urls": "Site-wide (Mobile PageSpeed Insights / Lighthouse 13.6.0)",
            "impact": "While synthetic tools report an initial FCP of 0.8s on the empty shell, real mobile visitors must wait 19.4 seconds before the Largest Contentful Paint (hero image and headline) renders. The Speed Index is 17.6 seconds, reflecting an excruciatingly sluggish visual completion rate. The page triggers 3.7 seconds of blocking main-thread JavaScript execution and downloads an enormous 4,429 KiB (4.4 MB) uncompressed payload, causing massive mobile user abandonment."
        },
        {
            "title": "Absence of a Valid Robots.txt File (Nginx SPA HTML Rewrite Trap)",
            "severity": "Critical",
            "urls": "https://storiai.ai/robots.txt (Returns HTTP 200 with text/html SPA shell)",
            "impact": "Nginx's blanket SPA rewrite rule intercepts requests for /robots.txt and serves the React index.html. Search engines requesting /robots.txt parse HTML markup as syntax errors, which can cause unpredictable crawling behavior, default to unrestricted crawling of sensitive private routes (/dashboard, /account-settings, /orders), or block indexing altogether."
        },
        {
            "title": "Complete Absence of an XML Sitemap for Search Engine Discovery",
            "severity": "Critical",
            "urls": "https://storiai.ai/sitemap.xml (Returns HTTP 200 with text/html SPA shell)",
            "impact": "No XML sitemap exists on the domain. Because internal navigation links are buried inside client-side JavaScript components, search engines have zero crawlable discovery pathways to find and index critical marketing pages such as /about, /pricing, /faq, /contact, and /stories-across-languages."
        },
        {
            "title": "SPA Catch-All Soft 404 / Phantom URL Trap on All Non-Existent Routes",
            "severity": "Critical",
            "urls": "Site-wide (e.g. https://storiai.ai/non-existent-page-xyz returns HTTP 200)",
            "impact": "The Nginx configuration (try_files $uri $uri/ /index.html;) returns HTTP 200 OK for every non-existent, mistyped, or deleted URL. Because the server never emits HTTP 404 Not Found or HTTP 410 Gone status codes, search engine crawlers interpret broken links and typo URLs as valid pages, resulting in severe Soft 404 penalties and crawl budget exhaustion."
        },
        {
            "title": "Split Indexing & Hostname Canonical Dilution (www vs non-www Both 200 OK)",
            "severity": "Critical",
            "urls": "https://www.storiai.ai/ and https://storiai.ai/ (Both live HTTP 200)",
            "impact": "Both https://www.storiai.ai/ and https://storiai.ai/ respond with HTTP 200 OK independently without a 301 permanent redirect consolidating them. Combined with the absence of canonical tags, search engines treat the www and non-www versions as two competing duplicate websites, splitting domain authority and ranking equity."
        },
        {
            "title": "Complete Absence of Canonical Link Tags Across All Domain Routes",
            "severity": "Critical",
            "urls": "Site-wide (100% of pages lack <link rel='canonical'>)",
            "impact": "The HTML shell completely omits canonical link elements. In a Single Page Application where URLs can be accessed via trailing slashes, query parameters, or alternative hostnames, the absence of canonical tags leaves search engines to guess which version to index, leading to index fragmentation."
        },
        {
            "title": "Missing Server-Side Caching Headers (Cache-Control: None on 4.4MB Payloads)",
            "severity": "Critical",
            "urls": "Site-wide (/assets/index-CVHzEv9o.js, /assets/App-XFfRbN91.js, /assets/App-CsDpWzVI.css)",
            "impact": "Nginx sends no Cache-Control or max-age headers for static JavaScript and CSS assets. Lighthouse identifies an estimated cache savings of 4,633 KiB on Desktop and 4,323 KiB on Mobile. Every time a visitor navigates between pages or returns to the site, their browser must revalidate or re-download multi-megabyte bundles, destroying repeat user experience."
        },
        {
            "title": "Zero HTTP Compression on 1.52MB Unminified JavaScript Bundles",
            "severity": "High",
            "urls": "https://storiai.ai/assets/App-XFfRbN91.js (1,524,830 bytes uncompressed)",
            "impact": "Nginx transmits JavaScript and CSS files without Gzip or Brotli compression (Content-Encoding: None). The main application chunk (App-XFfRbN91.js) is served as a massive 1.52 MB raw text file. Standard Brotli compression would reduce this file by over 75% to approximately 350 KB, immediately resolving the primary network bottleneck causing the 19.4s mobile LCP."
        },
        {
            "title": "Missing Meta Descriptions Across All Marketing & Informational Pages",
            "severity": "High",
            "urls": "Site-wide (<meta name='description' content='' /> in raw HTML shell)",
            "impact": "The raw HTML shell contains a hardcoded empty meta description tag. In search engine results, Google is forced to either auto-generate snippets from fragmented client-side text or display empty snippets, resulting in depressed click-through rates (CTR) on branded and commercial searches."
        },
        {
            "title": "Minimal Hardcoded Page Title ('StoriAI' - 7 Characters / 59 Pixels)",
            "severity": "High",
            "urls": "Site-wide (<title>StoriAI</title> across all URLs in raw HTML shell)",
            "impact": "The title tag is hardcoded in the HTML shell as just 'StoriAI' (7 characters / 59 pixels). It fails to communicate core value propositions (e.g. 'Personalized AI Children's Bedtime Stories') or secondary keywords, wasting Google's 561-pixel desktop / 60-character snippet allowance across all 61 routes."
        },
        {
            "title": "Complete Absence of OpenGraph and Twitter Social Share Cards",
            "severity": "High",
            "urls": "Site-wide (0 og:* and 0 twitter:* tags in HTML shell)",
            "impact": "The HTML shell contains zero OpenGraph (og:title, og:description, og:image, og:url) and zero Twitter Card tags. When links to StoriAI are shared on WhatsApp, LinkedIn, X, Facebook, or Slack, no visual preview card or description generates, severely impeding viral and social user acquisition."
        },
        {
            "title": "Complete Absence of Schema.org Structured Data (0 JSON-LD Entities)",
            "severity": "High",
            "urls": "Site-wide (0 structured data blocks discovered)",
            "impact": "The website provides zero Schema.org structured data. Search engines cannot programmatically identify StoriAI as a SoftwareApplication / WebApplication, recognize its subscription pricing, understand its Organization entity, or ingest the extensive FAQs embedded in the React code for SERP rich results."
        },
        {
            "title": "Trailing Slash Duplicate Content Proliferation Without 301 Consolidation",
            "severity": "High",
            "urls": "https://storiai.ai/pricing vs /pricing/, /about vs /about/, /contact vs /contact/",
            "impact": "Both trailing slash and non-trailing slash URL variations return HTTP 200 OK independently without a 301 redirect enforcing a single format. Combined with www and non-www variations, every single page on the site can be resolved at 4 separate URLs without canonical consolidation."
        },
        {
            "title": "Leaked Port 443 in HTTP-to-HTTPS 301 Redirect Headers",
            "severity": "Medium",
            "urls": "http://storiai.ai/ -> 301 -> https://storiai.ai:443/",
            "impact": "HTTP requests to http://storiai.ai/ and http://www.storiai.ai/ return a 301 redirect with an explicit port 443 in the Location header (https://storiai.ai:443/). While modern browsers normalize the port, legacy crawlers and proxy servers treat the explicit port as a distinct URL string, causing unnecessary redirect hops."
        },
        {
            "title": "3.7 Seconds of Blocking Main-Thread JavaScript Execution on Mobile",
            "severity": "Medium",
            "urls": "Site-wide (Lighthouse Diagnostic: Minimize main-thread work - 3.7 s)",
            "impact": "Lighthouse flags 3.7 seconds of continuous main-thread JavaScript execution on mobile CPU, identifying 4 long tasks and 1,133 KiB of unused JavaScript in the initial bundle. Compiling Redux store slices, Material-UI Emotion styling engines, and unused routes on the initial load freezes the browser UI and drives up the Speed Index to 17.6s."
        },
        {
            "title": "Default Boilerplate Web App Manifest Leaking Development Metadata",
            "severity": "Medium",
            "urls": "https://storiai.ai/manifest.webmanifest",
            "impact": "The web app manifest contains unedited default development boilerplate: 'TypeScript + React + Redux + MUI + RRD + ESLint + Prettier => Boilerplate'. This leaks internal development stack details to search engines and PWA browsers instead of describing the production children's storytelling product."
        },
        {
            "title": "Missing Explicit Image Dimensions (width/height) Triggering Layout Shifts",
            "severity": "Medium",
            "urls": "Site-wide (Lighthouse Diagnostic: Image elements do not have explicit width and height)",
            "impact": "Hero and illustrative images (hero-home.webp, avatar illustrations, book covers) are inserted into the DOM without explicit HTML width and height attributes or CSS aspect ratios, causing layout instability during client-side rendering."
        },
        {
            "title": "Missing Security Response Headers (HSTS, CSP, X-Frame-Options, nosniff)",
            "severity": "Medium",
            "urls": "Site-wide (HTTP Headers Probe)",
            "impact": "The Nginx server completely omits Strict-Transport-Security (HSTS), X-Frame-Options, X-Content-Type-Options (nosniff), Content-Security-Policy (CSP), and Referrer-Policy headers. This exposes visitors to MIME-sniffing, clickjacking in malicious iframes, and man-in-the-middle protocol downgrade attacks."
        },
        {
            "title": "Server Software Footprint and Version Exposure (nginx/1.31.8)",
            "severity": "Low",
            "urls": "Site-wide (HTTP Server Header: nginx/1.31.8)",
            "impact": "The HTTP response headers publicly broadcast the exact web server software and version (Server: nginx/1.31.8). Exposing software version banners provides automated vulnerability scanners and malicious actors with intelligence on known CVEs."
        }
    ],
    "scope_of_improvement": [
        {
            "bold_prefix": "1. Architectural Pre-Rendering & SSR Migration (Hydration Bridge):",
            "text": "The single most impactful architectural fix is implementing Server-Side Rendering (SSR) via Next.js / Remix or an automated static pre-rendering pipeline (Vite SSG / prerender-spa-plugin) for all public marketing, about, pricing, FAQ, and multilingual routes. Delivering fully hydrated static HTML ensures that Google, Bing, social platforms, and AI search engines receive complete body text, structured heading hierarchies, and crawlable <a href> links on initial byte delivery, eliminating the 1-page crawl lockout."
        },
        {
            "bold_prefix": "2. Mobile Core Web Vitals & Network Payload Optimization:",
            "text": "Eradicate the 19.4s mobile LCP and 17.6s Speed Index by enabling Brotli/Gzip compression on Nginx, setting immutable 1-year cache headers (Cache-Control: public, max-age=31536000, immutable) on hashed Vite assets, lazy-loading heavy non-critical dependencies (Ably Realtime, Redux slices, TTS sockets) until user interaction, and code-splitting the massive 1.52MB bundle to eliminate 1.1MB of unused initial JavaScript."
        },
        {
            "bold_prefix": "3. Canonical, Domain & Server Infrastructure Hardening:",
            "text": "Consolidate www and non-www hostnames into a single canonical target via a permanent 301 redirect, strip the leaked :443 port from redirect strings, enforce strict trailing-slash normalization, generate a real static robots.txt and XML sitemap, and configure Nginx to return proper HTTP 404 status codes for non-existent routes rather than serving the 200 OK index shell."
        },
        {
            "bold_prefix": "4. SERP Snippet Optimization & Semantic Metadata Architecture:",
            "text": "Deploy dynamic title and meta description injection across all public routes, targeting high-intent parent/child emotional storytelling keywords. Implement rich OpenGraph and Twitter card metadata for social virality, and replace the default boilerplate PWA manifest description with professional branded copy."
        },
        {
            "bold_prefix": "5. Semantic Entity Authority & Schema.org Structured Data:",
            "text": "Deploy comprehensive JSON-LD schemas including Organization, WebSite (with SearchAction), SoftwareApplication (specifying pricing, operating systems, and family category), and FAQPage schema mapped to the platform's rich bedtime story and safety Q&As to dominate rich snippets in Google and AI search engines."
        }
    ],
    "immediate_fixations": [
        "Deploy Pre-Rendering / SSR for Public Marketing Routes: Render full HTML for /, /about, /pricing, /faq, /contact, and /stories-across-languages so search bots see content and links.",
        "Enable Nginx Gzip / Brotli Compression: Compress App-XFfRbN91.js (1.52MB) and index-CVHzEv9o.js (550KB) to reduce initial network transfer weight by >70%.",
        "Configure 1-Year Asset Caching Headers: Inject Cache-Control: public, max-age=31536000, immutable for /assets/* to eliminate repeat multi-megabyte downloads.",
        "Deploy Real Static robots.txt: Remove Nginx SPA rewrite on /robots.txt and serve a clean crawler directive file referencing the XML sitemap.",
        "Generate and Deploy XML Sitemap: Create an automated sitemap.xml mapping all public routes with lastmod timestamps and submit to Google Search Console.",
        "Resolve Hostname Splitting (www vs non-www): Implement a permanent 301 redirect from https://www.storiai.ai/ to https://storiai.ai/ and strip port :443 from redirect headers.",
        "Inject Canonical Tags Sitewide: Add self-referencing <link rel='canonical' ...> tags on every public page to prevent duplicate content dilution.",
        "Rewrite Homepage Title & Meta Description: Replace <title>StoriAI</title> (7 chars) and empty description with keyword-optimized, high-CTR metadata.",
        "Eliminate SPA Soft 404s: Reconfigure Nginx to return real HTTP 404 status codes for invalid routes rather than serving the 200 OK index.html shell.",
        "Defer Eager WebSockets on Initial Page Load: Delay Ably Realtime and TTS socket connections until user registration or story creation, freeing the mobile CPU thread."
    ],
    "roadmap": [
        {
            "phase": "Phase 1: Days 1–15\nArchitectural SSR Bridge & Indexing Foundation",
            "objectives": "• Implement static pre-rendering (SSG/SSR) for core public routes (/, /about, /pricing, /faq, /contact, /stories-across-languages).\n• Deploy static robots.txt and automated sitemap.xml; submit to Google Search Console.\n• Fix Nginx 301 redirect from www to non-www and strip leaked :443 port.\n• Reconfigure Nginx to return real HTTP 404 status codes for invalid routes.\n• Enable Gzip/Brotli compression and 1-year Cache-Control headers on static assets in Nginx.",
            "milestone": "All public pages deliver 100% crawlable HTML with intact links; Screaming Frog crawls full site; raw asset transfer weight reduced by 70%."
        },
        {
            "phase": "Phase 2: Days 16–30\nCore Web Vitals & Mobile Speed Recovery",
            "objectives": "• Code-split React bundle (App-XFfRbN91.js) to eliminate 1.1MB of unused JavaScript from the initial landing page.\n• Defer Ably Realtime, Redux slices, and TTS WebSockets until story creation flow.\n• Inject explicit width and height dimensions on all hero and illustrative images.\n• Preload critical fonts and hero WebP image assets; eliminate main-thread blocking tasks.",
            "milestone": "Mobile LCP reduced from 19.4s to < 2.5s; Speed Index drops from 17.6s to < 3.5s; 100% compliance with Google Core Web Vitals thresholds."
        },
        {
            "phase": "Phase 3: Days 31–60\nSERP Metadata, Social Cards & PWA Cleanup",
            "objectives": "• Inject keyword-rich, high-CTR page titles (< 60 chars) and meta descriptions (< 155 chars) across all public pages.\n• Deploy complete OpenGraph and Twitter Card metadata with branded story preview graphics.\n• Sanitize manifest.webmanifest to remove framework boilerplate text and describe StoriAI's value proposition.\n• Enforce trailing slash canonical consolidation across all server routes.",
            "milestone": "Professional search snippets across Google and rich preview cards on WhatsApp, LinkedIn, X, and Facebook; zero boilerplate leaks."
        },
        {
            "phase": "Phase 4: Days 61–90\nStructured Data, Entity Authority & Expansion",
            "objectives": "• Deploy Schema.org JSON-LD structured data: Organization, WebApplication, WebSite, and FAQPage schemas.\n• Launch dedicated programmatic landing pages for high-intent queries (e.g. Bedtime Stories for Toddlers, Emotion Intelligence Stories).\n• Deploy llms.txt and AI search crawler optimization for Perplexity, ChatGPT, and Google AI Overviews.\n• Re-audit technical health scorecard against the 22/100 baseline.",
            "milestone": "Dominant rich snippets in Google SERPs; established brand entity authority in AI search engines; technical health score > 85/100."
        }
    ]
}

# 2. Save structured audit_data.json
json_path_office = os.path.join(office_out_dir, "audit_data.json")
json_path_ws = os.path.join(workspace_out_dir, "audit_data.json")
with open(json_path_office, "w", encoding="utf-8") as f:
    json.dump(audit_data, f, indent=2)
with open(json_path_ws, "w", encoding="utf-8") as f:
    json.dump(audit_data, f, indent=2)
shutil.copyfile(json_path_office, "audit_data.json")
print("[+] Saved audit_data.json successfully.")

# 3. Generate 01_url_inventory.csv (61 routes discovered from React Router)
routes_list = [
    ("/", "Marketing / Home", "200", "Indexable (Raw: 1,123 B shell, 0 links, 0 words | Rendered: Rich UI)", "Raw Crawl & App Bundle"),
    ("/about", "Marketing / About Us", "200 (SPA shell)", "Uncrawlable in raw HTML (Client-Side Route)", "App Bundle (React Router)"),
    ("/pricing", "Marketing / Pricing Plans", "200 (SPA shell)", "Uncrawlable in raw HTML (Client-Side Route)", "App Bundle (React Router)"),
    ("/contact", "Marketing / Contact & Sales", "200 (SPA shell)", "Uncrawlable in raw HTML (Client-Side Route)", "App Bundle (React Router)"),
    ("/faq", "Marketing / FAQ & Support", "200 (SPA shell)", "Uncrawlable in raw HTML (Client-Side Route)", "App Bundle (React Router)"),
    ("/stories-across-languages", "Feature / Multilingual Stories", "200 (SPA shell)", "Uncrawlable in raw HTML (Client-Side Route)", "App Bundle (React Router)"),
    ("/child-landing", "Product / Child Landing View", "200 (SPA shell)", "Uncrawlable in raw HTML (Client-Side Route)", "App Bundle (React Router)"),
    ("/choose-plan", "Commerce / Plan Selection", "200 (SPA shell)", "Uncrawlable in raw HTML (Client-Side Route)", "App Bundle (React Router)"),
    ("/login", "Authentication / Login", "200 (SPA shell)", "Private / Utility (Should be Noindex)", "App Bundle (React Router)"),
    ("/signup", "Authentication / Sign Up", "200 (SPA shell)", "Private / Utility (Should be Noindex)", "App Bundle (React Router)"),
    ("/reset-password", "Authentication / Password Reset", "200 (SPA shell)", "Private / Utility (Should be Noindex)", "App Bundle (React Router)"),
    ("/dashboard", "App / Parent Dashboard", "200 (SPA shell)", "Private / Auth-Gated (Should be Noindex)", "App Bundle (React Router)"),
    ("/create-story", "Core App / Story Generator", "200 (SPA shell)", "Product Feature / Interactive", "App Bundle (React Router)"),
    ("/create-child", "App / Add Child Profile", "200 (SPA shell)", "Private / Auth-Gated (Should be Noindex)", "App Bundle (React Router)"),
    ("/manage-children", "App / Manage Children", "200 (SPA shell)", "Private / Auth-Gated (Should be Noindex)", "App Bundle (React Router)"),
    ("/library", "App / Story Library", "200 (SPA shell)", "Product Feature / Gallery", "App Bundle (React Router)"),
    ("/library/story/:jobId", "App / View Saved Story", "200 (SPA shell)", "Dynamic / Auth-Gated", "App Bundle (React Router)"),
    ("/comic", "Feature / Comic Book Mode", "200 (SPA shell)", "Product Feature / Interactive", "App Bundle (React Router)"),
    ("/comic/book/:jobId", "App / View Comic Book", "200 (SPA shell)", "Dynamic / Auth-Gated", "App Bundle (React Router)"),
    ("/comic/print-order/:jobId", "Commerce / Comic Print Order", "200 (SPA shell)", "Private / Transactional", "App Bundle (React Router)"),
    ("/comic/share/:jobId", "Feature / Share Comic Book", "200 (SPA shell)", "Viral / Public Shared Asset", "App Bundle (React Router)"),
    ("/comic/view/:jobId", "App / Public Comic Reader", "200 (SPA shell)", "Product Feature / Gallery", "App Bundle (React Router)"),
    ("/event-gift", "Feature / Event Gift Stories", "200 (SPA shell)", "Product Feature / Interactive", "App Bundle (React Router)"),
    ("/event-gift/:jobId", "App / View Event Gift Story", "200 (SPA shell)", "Dynamic / Auth-Gated", "App Bundle (React Router)"),
    ("/event-gift/print-order/:jobId", "Commerce / Event Print Order", "200 (SPA shell)", "Private / Transactional", "App Bundle (React Router)"),
    ("/event-gift/print-book-order/:jobId", "Commerce / Print Book Order", "200 (SPA shell)", "Private / Transactional", "App Bundle (React Router)"),
    ("/event-gift/view/:jobId", "App / Public Event Story Reader", "200 (SPA shell)", "Product Feature / Gallery", "App Bundle (React Router)"),
    ("/quick-story/:jobId", "App / Quick Story Reader", "200 (SPA shell)", "Dynamic / Auth-Gated", "App Bundle (React Router)"),
    ("/quick-story/print-order/:jobId", "Commerce / Quick Story Print", "200 (SPA shell)", "Private / Transactional", "App Bundle (React Router)"),
    ("/quick-story/view/:jobId", "App / Quick Story View", "200 (SPA shell)", "Dynamic / Auth-Gated", "App Bundle (React Router)"),
    ("/story/:jobId", "App / Story Reader", "200 (SPA shell)", "Dynamic / Auth-Gated", "App Bundle (React Router)"),
    ("/avatar/entry", "Feature / Avatar Creation Entry", "200 (SPA shell)", "Product Feature / Interactive", "App Bundle (React Router)"),
    ("/avatar/photo", "Feature / Avatar Photo Upload", "200 (SPA shell)", "Product Feature / Interactive", "App Bundle (React Router)"),
    ("/avatar/preview/:jobId", "App / Avatar Preview", "200 (SPA shell)", "Dynamic / Auth-Gated", "App Bundle (React Router)"),
    ("/child-create-story", "Product / Child Story Creation", "200 (SPA shell)", "Product Feature / Interactive", "App Bundle (React Router)"),
    ("/child-account-settings", "App / Child Settings", "200 (SPA shell)", "Private / Auth-Gated", "App Bundle (React Router)"),
    ("/account-settings", "App / Account Settings", "200 (SPA shell)", "Private / Auth-Gated", "App Bundle (React Router)"),
    ("/billing-payment", "App / Billing & Payment", "200 (SPA shell)", "Private / Auth-Gated", "App Bundle (React Router)"),
    ("/orders", "App / Order History", "200 (SPA shell)", "Private / Auth-Gated", "App Bundle (React Router)"),
    ("/orders/:orderId/cancelled", "Commerce / Order Cancelled", "200 (SPA shell)", "Private / Transactional", "App Bundle (React Router)"),
    ("/orders/:orderId/success", "Commerce / Order Success", "200 (SPA shell)", "Private / Transactional", "App Bundle (React Router)"),
    ("/payment-cancel", "Commerce / Payment Cancel", "200 (SPA shell)", "Private / Transactional", "App Bundle (React Router)"),
    ("/payment-success", "Commerce / Payment Success", "200 (SPA shell)", "Private / Transactional", "App Bundle (React Router)"),
    ("/offline-stories", "PWA / Offline Story Cache", "200 (SPA shell)", "Product Feature / Offline PWA", "App Bundle (React Router)"),
    ("/test-offline-stories", "Internal / Test Offline Mode", "200 (SPA shell)", "Internal Testing (Should be Removed)", "App Bundle (React Router)"),
    ("/favourites", "App / Favourite Stories", "200 (SPA shell)", "Private / Auth-Gated", "App Bundle (React Router)"),
    ("/notifications", "App / Notifications Center", "200 (SPA shell)", "Private / Auth-Gated", "App Bundle (React Router)"),
    ("/generating-story", "App / Generation Loading State", "200 (SPA shell)", "Transient State / Interactive", "App Bundle (React Router)"),
    ("/verify-account", "Auth / Verify Email", "200 (SPA shell)", "Private / Transactional", "App Bundle (React Router)"),
    ("/verify-account-success", "Auth / Email Verified Success", "200 (SPA shell)", "Private / Transactional", "App Bundle (React Router)"),
    ("/verify-child-account", "Auth / Verify Child Account", "200 (SPA shell)", "Private / Transactional", "App Bundle (React Router)"),
    ("/verify-child-account-success", "Auth / Child Verified Success", "200 (SPA shell)", "Private / Transactional", "App Bundle (React Router)"),
    ("/manage-children/child/:childId/accessibility", "App / Accessibility Settings", "200 (SPA shell)", "Private / Auth-Gated", "App Bundle (React Router)"),
    ("/cms", "Internal / Admin CMS", "200 (SPA shell)", "Admin / Private (Should be Blocked)", "App Bundle (React Router)"),
    ("/auth/social-login", "Auth / OAuth Callback", "200 (SPA shell)", "Private / Transactional", "App Bundle (React Router)"),
    ("/tts-socket", "Service / Text-to-Speech Socket", "200 (SPA shell)", "WebSocket Service Endpoint", "App Bundle (React Router)"),
    ("/engine.io", "Service / Engine.IO Socket", "200 (SPA shell)", "WebSocket Service Endpoint", "App Bundle (React Router)"),
    ("/robots.txt", "Crawler / Robots Directives", "200 (Improper HTML)", "Defective: Serves React HTML shell instead of text", "Live HTTP Probe"),
    ("/sitemap.xml", "Crawler / XML Sitemap", "200 (Improper HTML)", "Defective: Serves React HTML shell instead of XML", "Live HTTP Probe"),
    ("/manifest.webmanifest", "PWA / Web App Manifest", "200 (octet-stream)", "Leaking development boilerplate text", "Live HTTP Probe"),
    ("/assets/App-XFfRbN91.js", "Static Asset / Application Bundle", "200 (1.52MB)", "Critical: Uncompressed raw JS; Cache-Control: None", "Live HTTP Probe"),
    ("/assets/index-CVHzEv9o.js", "Static Asset / Vendor Runtime", "200 (550KB)", "Critical: Uncompressed raw JS; Cache-Control: None", "Live HTTP Probe")
]

csv_path_office = os.path.join(office_out_dir, "01_url_inventory.csv")
csv_path_ws = os.path.join(workspace_out_dir, "01_url_inventory.csv")
with open(csv_path_office, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["URL Path", "Page Category & Purpose", "HTTP Status", "Crawlability & Rendering State", "Discovery Source"])
    for r in routes_list:
        writer.writerow(r)
shutil.copyfile(csv_path_office, csv_path_ws)
print(f"[+] Saved 01_url_inventory.csv ({len(routes_list)} URLs mapped).")

# 4. Generate 02_page_data.csv (Technical Breakdown of Core Landing & Public Pages)
page_data_rows = [
    ("https://storiai.ai/", "StoriAI", 7, "", 0, "", 0, "", 0, 0, 1123, "None", "None", "Missing", "Critical (100% CSR)"),
    ("https://storiai.ai/about", "StoriAI (Raw HTML)", 7, "", 0, "", 0, "", 0, 0, 1123, "None", "None", "Missing", "Uncrawlable (CSR)"),
    ("https://storiai.ai/pricing", "StoriAI (Raw HTML)", 7, "", 0, "", 0, "", 0, 0, 1123, "None", "None", "Missing", "Uncrawlable (CSR)"),
    ("https://storiai.ai/faq", "StoriAI (Raw HTML)", 7, "", 0, "", 0, "", 0, 0, 1123, "None", "None", "Missing", "Uncrawlable (CSR)"),
    ("https://storiai.ai/contact", "StoriAI (Raw HTML)", 7, "", 0, "", 0, "", 0, 0, 1123, "None", "None", "Missing", "Uncrawlable (CSR)"),
    ("https://storiai.ai/stories-across-languages", "StoriAI (Raw HTML)", 7, "", 0, "", 0, "", 0, 0, 1123, "None", "None", "Missing", "Uncrawlable (CSR)"),
    ("https://storiai.ai/choose-plan", "StoriAI (Raw HTML)", 7, "", 0, "", 0, "", 0, 0, 1123, "None", "None", "Missing", "Uncrawlable (CSR)"),
    ("https://storiai.ai/create-story", "StoriAI (Raw HTML)", 7, "", 0, "", 0, "", 0, 0, 1123, "None", "None", "Missing", "Uncrawlable (CSR)"),
    ("https://storiai.ai/library", "StoriAI (Raw HTML)", 7, "", 0, "", 0, "", 0, 0, 1123, "None", "None", "Missing", "Uncrawlable (CSR)"),
    ("https://storiai.ai/comic", "StoriAI (Raw HTML)", 7, "", 0, "", 0, "", 0, 0, 1123, "None", "None", "Missing", "Uncrawlable (CSR)"),
    ("https://storiai.ai/event-gift", "StoriAI (Raw HTML)", 7, "", 0, "", 0, "", 0, 0, 1123, "None", "None", "Missing", "Uncrawlable (CSR)"),
    ("https://storiai.ai/robots.txt", "StoriAI (Improper HTML)", 7, "", 0, "", 0, "", 0, 0, 1123, "None", "None", "Missing", "Syntax Error"),
    ("https://storiai.ai/sitemap.xml", "StoriAI (Improper HTML)", 7, "", 0, "", 0, "", 0, 0, 1123, "None", "None", "Missing", "Syntax Error")
]

csv_pdata_office = os.path.join(office_out_dir, "02_page_data.csv")
csv_pdata_ws = os.path.join(workspace_out_dir, "02_page_data.csv")
with open(csv_pdata_office, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["URL", "Title", "Title Length", "Meta Description", "Meta Desc Length", "H1", "H1 Length", "H2", "H2 Count", "Body Word Count (Raw)", "HTML Bytes", "Cache-Control", "Content-Encoding", "Canonical Tag", "Indexability Verdict"])
    for r in page_data_rows:
        writer.writerow(r)
shutil.copyfile(csv_pdata_office, csv_pdata_ws)
print("[+] Saved 02_page_data.csv.")

# 5. Generate 04_issues_log.csv
csv_iss_office = os.path.join(office_out_dir, "04_issues_log.csv")
csv_iss_ws = os.path.join(workspace_out_dir, "04_issues_log.csv")
with open(csv_iss_office, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Issue ID", "Severity", "Category", "Issue Title", "Affected Scope", "Observed Defect & Commercial Consequence", "Recommended Technical Fix", "Effort"])
    for idx, iss in enumerate(audit_data["issues"], 1):
        writer.writerow([
            f"ISS-{idx:02d}",
            iss["severity"],
            "Technical SEO / Architecture",
            iss["title"],
            iss["urls"],
            iss["impact"],
            "See Phased Strategic Roadmap",
            "High" if iss["severity"] == "Critical" else ("Medium" if iss["severity"] == "High" else "Low")
        ])
shutil.copyfile(csv_iss_office, csv_iss_ws)
print(f"[+] Saved 04_issues_log.csv ({len(audit_data['issues'])} issues).")

# 6. Generate 10_roadmap_30_60_90.md
rm_file = os.path.join(office_out_dir, "10_roadmap_30_60_90.md")
with open(rm_file, "w", encoding="utf-8") as f:
    f.write("""# StoriAI (storiai.ai) — 30-60-90 Day Technical SEO & Web Performance Roadmap

## Phase 1: Architectural SSR Bridge & Indexing Foundation (Days 1–15)
- [ ] Implement static pre-rendering (SSG) or Server-Side Rendering (SSR) for all public marketing routes (`/`, `/about`, `/pricing`, `/faq`, `/contact`, `/stories-across-languages`).
- [ ] Ensure pre-rendered HTML includes full body text, heading tags (`<h1>`, `<h2>`), and standard `<a href="...">` anchor links.
- [ ] Remove Nginx SPA catch-all rewrite on `/robots.txt`; deploy a static, plain-text `robots.txt` file referencing the XML sitemap.
- [ ] Generate a production `sitemap.xml` mapping all public marketing and story gallery routes with accurate `<lastmod>` timestamps; submit to Google Search Console.
- [ ] Reconfigure Nginx to return real HTTP 404 Not Found status codes for non-existent URLs rather than serving the 200 OK index.html shell.
- [ ] Configure permanent 301 redirect from `https://www.storiai.ai/` to `https://storiai.ai/` and strip explicit port `:443` from redirect headers.
- [ ] Enable Gzip or Brotli compression on Nginx (`gzip on; gzip_types text/plain application/javascript text/css application/json;`).
- [ ] Configure 1-year immutable caching headers on Nginx for Vite assets: `location /assets/ { expires 1y; add_header Cache-Control "public, max-age=31536000, immutable"; }`.

## Phase 2: Core Web Vitals & Mobile Speed Recovery (Days 16–30)
- [ ] Code-split the massive 1.52MB `App-XFfRbN91.js` React bundle via dynamic `React.lazy()` imports to eliminate 1.1MB of unused JavaScript from the initial landing page.
- [ ] Defer eager WebSocket connections (Ably Realtime socket `/v1/auth/ably`, Engine.io `/engine.io`, and TTS socket `/tts-socket`) until the user enters the story generator flow.
- [ ] Inject explicit `width` and `height` dimensions and aspect ratios on all image elements (`hero-home.webp`, avatar illustrations, book covers) to eliminate layout shifts.
- [ ] Preload critical fonts and hero WebP image assets via `<link rel="preload">` in the HTML document `<head>`.
- [ ] Benchmark and verify that Mobile LCP drops below 2.5 seconds and Mobile Speed Index drops below 3.5 seconds.

## Phase 3: SERP Metadata, Social Cards & PWA Cleanup (Days 31–60)
- [ ] Implement unique, keyword-optimized `<title>` tags (< 60 chars / 561 px) across all public pages (e.g., `StoriAI | Personalized Emotion-Aware Stories for Kids`).
- [ ] Craft compelling `<meta name="description">` tags (< 155 chars) highlighting emotional intelligence, child safety, and personalized bedtime storytelling.
- [ ] Deploy complete OpenGraph (`og:title`, `og:description`, `og:image`, `og:url`) and Twitter Card (`summary_large_image`) tags with branded story preview graphics.
- [ ] Sanitize `manifest.webmanifest`: replace the default development boilerplate string with production brand descriptions and metadata.
- [ ] Enforce canonical trailing slash normalization across all routes (e.g. 301 redirect from `/pricing/` to `/pricing`).

## Phase 4: Structured Data, Entity Authority & Expansion (Days 61–90)
- [ ] Deploy Schema.org JSON-LD structured data: `Organization`, `WebSite` (with `SearchAction`), `SoftwareApplication` (specifying pricing, operating systems, and family category), and `FAQPage` schemas.
- [ ] Launch dedicated programmatic SEO landing pages for high-intent queries (e.g., *Bedtime Stories for Toddlers*, *Personalized Fairy Tales for Kids*, *Emotion Regulation Stories for Children*).
- [ ] Deploy `llms.txt` and optimize for AI search engine discovery across Perplexity, ChatGPT, Claude, and Google AI Overviews.
- [ ] Re-audit technical health scorecard against the 22/100 baseline.
""")
shutil.copyfile(rm_file, os.path.join(workspace_out_dir, "10_roadmap_30_60_90.md"))
print("[+] Saved 10_roadmap_30_60_90.md.")

# 7. Copy Screaming Frog CSVs to Office stoirai.ai folder for permanent record
shutil.copyfile(r"C:\Users\test\Videos\Office\website audit\internal_all.csv", os.path.join(office_out_dir, "screaming_frog_internal_all.csv"))
shutil.copyfile(r"C:\Users\test\Videos\Office\website audit\issues_overview_report.csv", os.path.join(office_out_dir, "screaming_frog_issues_overview.csv"))

# 8. Build DOCX and PDF Reports via Universal Engine
docx_path_office = os.path.join(office_out_dir, "StoriAI_SEO_Audit_Report.docx")
pdf_path_office = os.path.join(office_out_dir, "StoriAI_SEO_Audit_Report.pdf")

print("[*] Generating DOCX report...")
build_docx_report(audit_data, docx_path_office)
print(f"[+] DOCX report built: {docx_path_office}")

print("[*] Generating PDF report via Playwright Chromium...")
build_pdf_report(audit_data, pdf_path_office)
print(f"[+] PDF report built: {pdf_path_office}")

# Mirror reports to workspace out_dir and root
shutil.copyfile(docx_path_office, os.path.join(workspace_out_dir, "StoriAI_SEO_Audit_Report.docx"))
shutil.copyfile(pdf_path_office, os.path.join(workspace_out_dir, "StoriAI_SEO_Audit_Report.pdf"))
shutil.copyfile(docx_path_office, "StoriAI_SEO_Audit_Report.docx")
shutil.copyfile(pdf_path_office, "StoriAI_SEO_Audit_Report.pdf")

print("\n==========================================")
print("[+] ALL STORIAI DELIVERABLES CREATED SUCCESSFULLY!")
print("==========================================")
