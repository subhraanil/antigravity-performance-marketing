import csv
import json
import os

# Destination folders: both the specific audit folder and root
dest_dirs = [r"website audit\victoryhcspl.com", "."]

print("=== 1. GENERATING 04_ISSUES_LOG.CSV ===")
issues_data = [
    {
        "ID": "ISS-001",
        "Category": "Crawlability & Indexability",
        "Severity": "P0 Critical",
        "Issue": "robots.txt redirects (301) to Homepage instead of serving valid directives",
        "Affected URLs": "https://victoryhcspl.com/robots.txt",
        "Evidence": "HTTP 301 Location: https://victoryhcspl.com/. Returning HTML instead of text/plain directives.",
        "Fix": "Deploy a physical or virtual robots.txt serving HTTP 200 with User-agent rules, Disallow /wp-admin/, and Sitemap: https://victoryhcspl.com/sitemap.xml.",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-002",
        "Category": "Crawlability & Architecture",
        "Severity": "P1 High",
        "Issue": "Dummy navigation links (#! / #content) create crawl traps and 10 duplicate non-indexable URLs",
        "Affected URLs": "All 10 canonical pages (e.g. /healthcare-training/#!, /#!, /about-us/#!)",
        "Evidence": "Menu item 'Services' links to href='#!'. Screaming Frog & crawlers discover 10 canonicalised /#! URLs.",
        "Fix": "Replace dummy href='#!' with semantic buttons (<button>) for dropdown toggles, or prevent linking to fragments.",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-003",
        "Category": "On-Page SEO",
        "Severity": "P0 Critical",
        "Issue": "Missing H1 Heading on 90% of Site Pages (including Primary Service Page)",
        "Affected URLs": "/healthcare-training/, /his-ris-pacs/, /infra-management/, /consulting/, /about-us/, /clientele/, /careers/, /gallery/, /contact-us/",
        "Evidence": "Crawled DOM reveals exactly 0 <h1> elements on 9 out of 10 pages. Only homepage contains an H1.",
        "Fix": "Add a unique, keyword-targeted <h1> tag to each page. For /healthcare-training/: 'Healthcare & Medical Imaging Training Programs in India'.",
        "Effort": "S",
        "Owner": "Content / Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-004",
        "Category": "On-Page SEO",
        "Severity": "P1 High",
        "Issue": "Severely Truncated, Auto-Scraped Meta Descriptions Across All Pages",
        "Affected URLs": "All 10 canonical pages (/healthcare-training/, /about-us/, etc.)",
        "Evidence": "/healthcare-training/ meta description is 423 chars, beginning with breadcrumb junk: 'Healthcare Training Home Healthcare Training Overview...'",
        "Fix": "Rewrite all meta descriptions to 140–160 characters with clear value proposition, credentials, target audience, and CTA.",
        "Effort": "S",
        "Owner": "Content",
        "Status": "Open"
    },
    {
        "ID": "ISS-005",
        "Category": "On-Page SEO",
        "Severity": "P1 High",
        "Issue": "Corrupted Heading Hierarchy & Paragraph Blocks Marked Up as H3 Headings",
        "Affected URLs": "https://victoryhcspl.com/healthcare-training/, /about-us/",
        "Evidence": "On /healthcare-training/, an entire 50-word overview paragraph is marked up inside an <h3> tag. Footer designer credit marked as <h2>.",
        "Fix": "Refactor Elementor typography settings: change paragraph blocks from <h3> to <p>. Demote footer agency credits to plain <span> or <small>.",
        "Effort": "M",
        "Owner": "Developer / Content",
        "Status": "Open"
    },
    {
        "ID": "ISS-006",
        "Category": "UX & Conversion",
        "Severity": "P0 Critical",
        "Issue": "Zero Lead Capture or Admission Enquiry Forms on Primary Service Page",
        "Affected URLs": "https://victoryhcspl.com/healthcare-training/",
        "Evidence": "DOM inspection confirms form_count = 0. No embedded lead form, brochure download, or course application.",
        "Fix": "Embed a dedicated, mobile-friendly admission enquiry form above the fold and at the bottom of /healthcare-training/.",
        "Effort": "M",
        "Owner": "Developer / Designer",
        "Status": "Open"
    },
    {
        "ID": "ISS-007",
        "Category": "Analytics & Tracking",
        "Severity": "P0 Critical",
        "Issue": "Complete Absence of Web Analytics, Conversion Tracking, and Webmaster Verification",
        "Affected URLs": "Site-wide",
        "Evidence": "0 instances of GA4 (G-XXXX), GTM (GTM-XXXX), Meta Pixel, Google Search Console meta verification, or Bing verification.",
        "Fix": "Deploy Google Tag Manager (GTM) in <head> and <body>. Set up GA4 property, GSC verification, and event tracking for WhatsApp clicks, phone calls, and form submissions.",
        "Effort": "S",
        "Owner": "SEO / Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-008",
        "Category": "Structured Data",
        "Severity": "P1 High",
        "Issue": "Missing Course, EducationalOrganization, and LocalBusiness Schema Markup",
        "Affected URLs": "https://victoryhcspl.com/healthcare-training/, https://victoryhcspl.com/",
        "Evidence": "Only default AIOSEO WebPage and basic BreadcrumbList detected. No Course, CourseInstance, or educational schema present.",
        "Fix": "Inject JSON-LD schemas for EducationalOrganization, LocalBusiness (Bangalore center), and Course schemas for CT/MRI, Sonography, and Radiology Admin.",
        "Effort": "M",
        "Owner": "SEO / Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-009",
        "Category": "Internal Linking & Redirects",
        "Severity": "P2 Medium",
        "Issue": "Internal Header Logo Links to 301-Redirected URL (/home/)",
        "Affected URLs": "All pages (site-wide header)",
        "Evidence": "Header logo links to https://victoryhcspl.com/home/ which returns HTTP 301 -> https://victoryhcspl.com/.",
        "Fix": "Update header logo link href in Elementor theme template directly to 'https://victoryhcspl.com/'.",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-010",
        "Category": "HTTP & URL Hygiene",
        "Severity": "P2 Medium",
        "Issue": "Two-Hop Redirect Chain on http://www URL Version",
        "Affected URLs": "http://www.victoryhcspl.com/",
        "Evidence": "http://www.victoryhcspl.com/ -> 301 -> https://www.victoryhcspl.com/ -> 301 -> https://victoryhcspl.com/.",
        "Fix": "Update Nginx / Plesk vhost configuration to redirect http://www directly to https://victoryhcspl.com in a single 301 hop.",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-011",
        "Category": "Security",
        "Severity": "P1 High",
        "Issue": "Missing Essential HTTP Security Headers (X-Frame-Options, CSP, X-Content-Type-Options)",
        "Affected URLs": "Site-wide",
        "Evidence": "Live response headers lack X-Frame-Options, X-Content-Type-Options, Referrer-Policy, and Content-Security-Policy.",
        "Fix": "Add security headers in Nginx configuration: add_header X-Frame-Options 'SAMEORIGIN'; add_header X-Content-Type-Options 'nosniff'; add_header Referrer-Policy 'strict-origin-when-cross-origin';",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-012",
        "Category": "Security",
        "Severity": "P2 Medium",
        "Issue": "Server Signatures and Tech Stack Exposed in HTTP Response Headers",
        "Affected URLs": "Site-wide",
        "Evidence": "Headers expose 'Server: nginx' and 'X-Powered-By: PleskLin'.",
        "Fix": "Set 'server_tokens off;' in nginx.conf and disable 'X-Powered-By' via fastcgi_hide_header or php.ini expose_php = Off.",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-013",
        "Category": "Legal & Compliance",
        "Severity": "P0 Critical",
        "Issue": "Total Absence of Privacy Policy, Terms, and Compliance with India DPDP Act 2023",
        "Affected URLs": "/privacy-policy/, /terms-and-conditions/",
        "Evidence": "HTTP 404 on /privacy-policy/, /terms-and-conditions/, /refund-policy/, /disclaimer/. Site collects personal phone/email via forms and WhatsApp.",
        "Fix": "Publish a comprehensive Privacy Policy detailing Data Fiduciary info, grievance officer, contact info, and cookie notice compliant with DPDP Act 2023.",
        "Effort": "M",
        "Owner": "Client / Legal / Content",
        "Status": "Open"
    },
    {
        "ID": "ISS-014",
        "Category": "E-E-A-T & Trust",
        "Severity": "P1 High",
        "Issue": "Exceptional Founder & Faculty Credentials Completely Omitted from Course Page",
        "Affected URLs": "https://victoryhcspl.com/healthcare-training/",
        "Evidence": "Founders Anto Ramesh Delvi and Vijaya Kumar C boast 49+ years of combined experience at Columbia Asia and Manipal, but are not mentioned on /healthcare-training/.",
        "Fix": "Add a dedicated 'Course Mentors & Faculty Credentials' section on /healthcare-training/ featuring bios, hospital backgrounds, and certifications.",
        "Effort": "M",
        "Owner": "Content",
        "Status": "Open"
    },
    {
        "ID": "ISS-015",
        "Category": "Content & Topical Authority",
        "Severity": "P1 High",
        "Issue": "Zero Blog Posts and No Dedicated Child Course Pages (Thin Service Architecture)",
        "Affected URLs": "Site-wide (/wp-json/wp/v2/posts is empty; /post-sitemap.xml is 404)",
        "Evidence": "Site has 0 published blog articles and all 7 training modalities are compressed into one 571-word overview page.",
        "Fix": "Adopt Hub-and-Spoke model: Create sub-pages for 'CT & MRI Technician Course', 'Ultrasound Sonography Training', 'Radiology Administration', and publish targeted educational articles.",
        "Effort": "L",
        "Owner": "Content / SEO",
        "Status": "Open"
    },
    {
        "ID": "ISS-016",
        "Category": "Images & Media",
        "Severity": "P2 Medium",
        "Issue": "Missing Alt Text on 25+ Images and Outdated Image Formats (No WebP/AVIF)",
        "Affected URLs": "Site-wide (25 images identified by Screaming Frog)",
        "Evidence": "Images such as Logo-Eng.png, course banners, and gallery photos lack descriptive alt text and use uncompressed PNG/JPEG formats.",
        "Fix": "Add descriptive alt attributes with relevant keywords. Convert all media to next-gen WebP formats with explicit width and height attributes.",
        "Effort": "M",
        "Owner": "Content / Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-017",
        "Category": "E-E-A-T & Professionalism",
        "Severity": "P2 Medium",
        "Issue": "Free Gmail Address and Residential Apartment Address Displayed for Healthcare Institute",
        "Affected URLs": "Header, Footer, /contact-us/, /healthcare-training/",
        "Evidence": "Email displayed is 'victoryantovijay@gmail.com'; Address is 'The Ledge Apartment, B 108 B Block, Jakkur, Yelahanka'.",
        "Fix": "Configure Google Workspace / professional domain email (e.g., admissions@victoryhcspl.com, info@victoryhcspl.com). Clarify physical training lab/hospital partner address.",
        "Effort": "S",
        "Owner": "Client / Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-018",
        "Category": "Performance & Hygiene",
        "Severity": "P2 Medium",
        "Issue": "Malformed Script Tag Causing Duplicate HTML Request as JavaScript",
        "Affected URLs": "https://victoryhcspl.com/contact-us/",
        "Evidence": "Playwright network audit logs: 'REQ: script https://victoryhcspl.com/' downloading 220KB HTML as a script.",
        "Fix": "Audit Autoptimize / Elementor script concatenation settings to eliminate empty or root-relative script tags.",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-019",
        "Category": "UX & Hygiene",
        "Severity": "P3 Low",
        "Issue": "Outdated Footer Copyright Year and Broken Social Media Links",
        "Affected URLs": "Site-wide footer",
        "Evidence": "Footer displays 'Copyright © 2024'; Twitter and Instagram icons link to dummy '#' anchors.",
        "Fix": "Update dynamic copyright year to current year (2026). Either link to active company social profiles or remove placeholder icons.",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-020",
        "Category": "International & Geo-Targeting",
        "Severity": "P3 Low",
        "Issue": "HTML Language Declared as Generic or en-US instead of Target Regional Locale (en-IN)",
        "Affected URLs": "Site-wide",
        "Evidence": "<html lang='en-US'> observed in page source.",
        "Fix": "Update WordPress Site Language in Settings -> General to 'English (India)' (<html lang='en-IN'>).",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    }
]

print("Writing 04_issues_log.csv...")
for d in dest_dirs:
    with open(f"{d}/04_issues_log.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ID", "Category", "Severity", "Issue", "Affected URLs", "Evidence", "Fix", "Effort", "Owner", "Status"])
        writer.writeheader()
        writer.writerows(issues_data)

print("=== 2. GENERATING 05_REDIRECT_MAP.CSV ===")
redirects_data = [
    {
        "Old URL": "http://victoryhcspl.com/",
        "Target Canonical URL": "https://victoryhcspl.com/",
        "Redirect Type": "301 Permanent",
        "Reason": "HTTP to HTTPS protocol consolidation"
    },
    {
        "Old URL": "http://www.victoryhcspl.com/",
        "Target Canonical URL": "https://victoryhcspl.com/",
        "Redirect Type": "301 Permanent (Direct)",
        "Reason": "Eliminate 2-hop redirect chain (http://www -> https://www -> https://)"
    },
    {
        "Old URL": "https://www.victoryhcspl.com/",
        "Target Canonical URL": "https://victoryhcspl.com/",
        "Redirect Type": "301 Permanent",
        "Reason": "Subdomain consolidation (www to non-www)"
    },
    {
        "Old URL": "https://victoryhcspl.com/home/",
        "Target Canonical URL": "https://victoryhcspl.com/",
        "Redirect Type": "301 Permanent",
        "Reason": "Consolidate duplicate WordPress /home/ slug to root domain"
    },
    {
        "Old URL": "https://victoryhcspl.com/index.php",
        "Target Canonical URL": "https://victoryhcspl.com/",
        "Redirect Type": "301 Permanent",
        "Reason": "Default directory index canonicalisation"
    },
    {
        "Old URL": "https://victoryhcspl.com/wp-sitemap.xml",
        "Target Canonical URL": "https://victoryhcspl.com/sitemap.xml",
        "Redirect Type": "301 Permanent",
        "Reason": "Convert 302 temporary redirect to 301 permanent redirect"
    },
    {
        "Old URL": "https://victoryhcspl.com/robots.txt",
        "Target Canonical URL": "Serve HTTP 200 File (No Redirect)",
        "Redirect Type": "200 Static File",
        "Reason": "Remove 301 redirect to homepage; serve valid text/plain robots.txt"
    },
    {
        "Old URL": "https://victoryhcspl.com/#!",
        "Target Canonical URL": "https://victoryhcspl.com/",
        "Redirect Type": "Remove Link / 301",
        "Reason": "Remove internal #! dummy links to stop AJAX crawling duplication"
    },
    {
        "Old URL": "https://victoryhcspl.com/healthcare-training/#!",
        "Target Canonical URL": "https://victoryhcspl.com/healthcare-training/",
        "Redirect Type": "Remove Link / 301",
        "Reason": "Remove internal #! dummy links to stop AJAX crawling duplication"
    }
]

print("Writing 05_redirect_map.csv...")
for d in dest_dirs:
    with open(f"{d}/05_redirect_map.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Old URL", "Target Canonical URL", "Redirect Type", "Reason"])
        writer.writeheader()
        writer.writerows(redirects_data)

print("=== 3. GENERATING 06_METADATA_REWRITES.CSV ===")
metadata_rewrites = [
    {
        "URL": "https://victoryhcspl.com/healthcare-training/",
        "Page Type": "Primary Service Page",
        "Current Title": "Healthcare Training - Victory Healthcare Services Pvt Ltd (57 chars)",
        "Proposed Title": "Healthcare & Radiology Imaging Training in India | Victory HCS (62 chars)",
        "Current Meta Description": "Healthcare Training Home Healthcare Training Overview Victory HealthCare Services EduTech Solutions is a pioneering healthcare education company that specializes in providing cutting-edge E-Learning Platforms for medical professionals... (423 chars - Truncated)",
        "Proposed Meta Description": "Advance your career with hands-on CT, MRI, Ultrasound, and Radiology Administration training programs in India. Mentored by hospital experts. Enquire now! (156 chars)",
        "Proposed H1": "Comprehensive Healthcare & Medical Imaging Training Programs"
    },
    {
        "URL": "https://victoryhcspl.com/",
        "Page Type": "Homepage",
        "Current Title": "Victory Healthcare Services | Empowering Technologists Professionally (69 chars)",
        "Proposed Title": "Victory Healthcare Services | Medical Imaging & Healthcare Solutions India (74 chars)",
        "Current Meta Description": "Victory Healthcare Services offers tailored solutions in software, infrastructure, and consulting to meet the unique needs of healthcare providers. (152 chars)",
        "Proposed Meta Description": "Victory Healthcare Services empowers Indian healthcare providers with cutting-edge HIS/RIS/PACS solutions, IT infrastructure, consulting, and clinical training. (160 chars)",
        "Proposed H1": "Healthcare Technology Solutions & Professional Medical Imaging Training"
    },
    {
        "URL": "https://victoryhcspl.com/about-us/",
        "Page Type": "About Page",
        "Current Title": "About Us - Victory Healthcare Services Pvt Ltd (46 chars)",
        "Proposed Title": "About Victory Healthcare Services | Radiology & Healthcare Leaders (66 chars)",
        "Current Meta Description": "About Us Home About Us About Us We Provide Essential Services to Healthcare Industry Victory Healthcare Services offers specialized software solutions... (423 chars - Truncated)",
        "Proposed Meta Description": "Learn about Victory Healthcare Services, founded by veteran radiology leaders Anto Ramesh Delvi and Vijaya Kumar C with 49+ years of healthcare excellence. (156 chars)",
        "Proposed H1": "Pioneering Excellence in Healthcare Administration & Medical Imaging"
    },
    {
        "URL": "https://victoryhcspl.com/contact-us/",
        "Page Type": "Contact / Conversion",
        "Current Title": "Contact Us - Victory Healthcare Services Pvt Ltd (48 chars)",
        "Proposed Title": "Contact Victory Healthcare Services | Healthcare Training Enquiries (68 chars)",
        "Current Meta Description": "Contact Us Home Contact Us Contact Us Get In Touch Feel free to reach out to Victory Health Care Services. We're here to help you with your healthcare needs... (341 chars - Truncated)",
        "Proposed Meta Description": "Get in touch with Victory Healthcare Services in Bangalore, India. Enquire about our healthcare training programs, hospital consulting, or software solutions. (160 chars)",
        "Proposed H1": "Get in Touch with Our Healthcare Solutions & Training Team"
    },
    {
        "URL": "https://victoryhcspl.com/his-ris-pacs/",
        "Page Type": "Software Service Page",
        "Current Title": "HIS/RIS/PACS - Victory Healthcare Services Pvt Ltd (50 chars)",
        "Proposed Title": "HIS, RIS & PACS Healthcare Software Solutions India | Victory HCS (65 chars)",
        "Current Meta Description": "Software Services Home Software Services Digital Healthcare Solutions Transforming healthcare operations with advanced HIS/RIS/PACS software... (417 chars - Truncated)",
        "Proposed Meta Description": "Streamline hospital workflows with Victory HCS's enterprise HIS, RIS, and PACS solutions. Secure teleradiology, DICOM integration, and fast diagnostic reporting. (162 chars)",
        "Proposed H1": "Advanced HIS, RIS & PACS Digital Healthcare Software Solutions"
    },
    {
        "URL": "https://victoryhcspl.com/infra-management/",
        "Page Type": "Infrastructure Service Page",
        "Current Title": "Infra Management - Victory Healthcare Services Pvt Ltd (54 chars)",
        "Proposed Title": "Healthcare Infrastructure & Medical Equipment Management | Victory HCS (70 chars)",
        "Current Meta Description": "Infra Management Home Infra Management Efficient Healthcare Infrastructure Reliable Infrastructure Management Solutions for Healthcare Organizations... (458 chars - Truncated)",
        "Proposed Meta Description": "Optimize clinical operations with complete hospital infrastructure management, medical equipment maintenance, NABH compliance, and hospital manpower solutions. (160 chars)",
        "Proposed H1": "Healthcare Infrastructure, Manpower & Medical Equipment Management"
    },
    {
        "URL": "https://victoryhcspl.com/consulting/",
        "Page Type": "Consulting Service Page",
        "Current Title": "Consulting - Victory Healthcare Services Pvt Ltd (48 chars)",
        "Proposed Title": "Hospital Healthcare Consulting & Compliance Solutions | Victory HCS (67 chars)",
        "Current Meta Description": "Consulting Home Consulting Healthcare Compliance Solutions In the realm of healthcare, compliance with regulatory standards is not merely a legal requirement... (421 chars - Truncated)",
        "Proposed Meta Description": "Expert hospital management consulting: NABH/NABL accreditation guidance, radiology quality assurance, workflow optimization, and operational advisory in India. (160 chars)",
        "Proposed H1": "Strategic Healthcare Consulting & Hospital Regulatory Compliance"
    },
    {
        "URL": "https://victoryhcspl.com/clientele/",
        "Page Type": "Social Proof Page",
        "Current Title": "Clientele - Victory Healthcare Services Pvt Ltd (47 chars)",
        "Proposed Title": "Our Clients & Partners | Trusted by Leading Hospitals - Victory HCS (67 chars)",
        "Current Meta Description": "Our Clients Home Our Clients Our Happy Clients Our clients are the heart of everything we do. We take pride in building strong relationships... (168 chars)",
        "Proposed Meta Description": "Discover leading hospitals, teleradiology networks, and diagnostic centers that rely on Victory Healthcare Services for software, training, and consulting. (156 chars)",
        "Proposed H1": "Trusted Healthcare Partners, Hospitals & Diagnostic Centers"
    },
    {
        "URL": "https://victoryhcspl.com/careers/",
        "Page Type": "Careers Page",
        "Current Title": "Careers - Victory Healthcare Services Pvt Ltd (45 chars)",
        "Proposed Title": "Careers at Victory Healthcare Services | Healthcare & IT Jobs (61 chars)",
        "Current Meta Description": "Career Home Career Lets Get In Touch Be a part of Victory Healthcare Services. Explore career opportunities with us. (117 chars)",
        "Proposed Meta Description": "Join Victory Healthcare Services! Explore exciting career opportunities in teleradiology, healthcare software support, hospital administration, and training. (159 chars)",
        "Proposed H1": "Build Your Career in Healthcare Technology & Medical Services"
    },
    {
        "URL": "https://victoryhcspl.com/gallery/",
        "Page Type": "Media Page",
        "Current Title": "Gallery - Victory Healthcare Services Pvt Ltd (45 chars)",
        "Proposed Title": "Training & Facility Gallery | Victory Healthcare Services (57 chars)",
        "Current Meta Description": "Gallery Home Gallery (20 chars - Thin)",
        "Proposed Meta Description": "Explore photos from our healthcare training workshops, radiology post-processing sessions, hands-on ultrasound labs, and hospital infrastructure projects. (155 chars)",
        "Proposed H1": "Victory Healthcare Training Workshops & Facilities Gallery"
    }
]

print("Writing 06_metadata_rewrites.csv...")
for d in dest_dirs:
    with open(f"{d}/06_metadata_rewrites.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["URL", "Page Type", "Current Title", "Proposed Title", "Current Meta Description", "Proposed Meta Description", "Proposed H1"])
        writer.writeheader()
        writer.writerows(metadata_rewrites)

print("=== 4. GENERATING 07_INTERNAL_LINKING_PLAN.CSV ===")
internal_linking_plan = [
    {
        "Source URL": "https://victoryhcspl.com/",
        "Target URL": "https://victoryhcspl.com/healthcare-training/",
        "Anchor Text": "specialized healthcare and medical imaging training programs",
        "Context / Placement": "Homepage 'Our Services' section summary paragraph"
    },
    {
        "Source URL": "https://victoryhcspl.com/",
        "Target URL": "https://victoryhcspl.com/healthcare-training/",
        "Anchor Text": "CT & MRI technician training",
        "Context / Placement": "Homepage hero or value proposition bullet points"
    },
    {
        "Source URL": "https://victoryhcspl.com/about-us/",
        "Target URL": "https://victoryhcspl.com/healthcare-training/",
        "Anchor Text": "hands-on radiology training modules",
        "Context / Placement": "In Mr. Anto Ramesh Delvi's bio discussing training 300+ imaging officers"
    },
    {
        "Source URL": "https://victoryhcspl.com/about-us/",
        "Target URL": "https://victoryhcspl.com/healthcare-training/",
        "Anchor Text": "healthcare education and clinical upskilling",
        "Context / Placement": "In Mr. Vijaya Kumar C's bio discussing quality standards & training"
    },
    {
        "Source URL": "https://victoryhcspl.com/his-ris-pacs/",
        "Target URL": "https://victoryhcspl.com/healthcare-training/",
        "Anchor Text": "Radiology Administration & PACS Administrator training",
        "Context / Placement": "In RIS/PACS software workflow section"
    },
    {
        "Source URL": "https://victoryhcspl.com/consulting/",
        "Target URL": "https://victoryhcspl.com/healthcare-training/",
        "Anchor Text": "hospital staff radiology quality assurance training",
        "Context / Placement": "Under Healthcare Compliance & NABH Quality Assurance section"
    },
    {
        "Source URL": "https://victoryhcspl.com/infra-management/",
        "Target URL": "https://victoryhcspl.com/healthcare-training/",
        "Anchor Text": "clinical equipment operational training",
        "Context / Placement": "Under Medical Equipment & Manpower Management section"
    },
    {
        "Source URL": "https://victoryhcspl.com/healthcare-training/",
        "Target URL": "https://victoryhcspl.com/contact-us/",
        "Anchor Text": "enquire about upcoming batch dates and fees",
        "Context / Placement": "Call-to-action button and admission info box on /healthcare-training/"
    },
    {
        "Source URL": "https://victoryhcspl.com/healthcare-training/",
        "Target URL": "https://victoryhcspl.com/about-us/",
        "Anchor Text": "meet our expert faculty and directors",
        "Context / Placement": "Under trainer credentials and course advisory board section"
    },
    {
        "Source URL": "https://victoryhcspl.com/healthcare-training/",
        "Target URL": "https://victoryhcspl.com/clientele/",
        "Anchor Text": "hospitals and healthcare networks where our trainees excel",
        "Context / Placement": "Under placement assistance and career pathways section"
    },
    {
        "Source URL": "https://victoryhcspl.com/healthcare-training/",
        "Target URL": "https://victoryhcspl.com/gallery/",
        "Anchor Text": "view photos of our hands-on imaging workshop sessions",
        "Context / Placement": "Under Post-Processing & Hands-On Training section"
    },
    {
        "Source URL": "https://victoryhcspl.com/healthcare-training/",
        "Target URL": "https://victoryhcspl.com/his-ris-pacs/",
        "Anchor Text": "modern PACS and DICOM viewer software",
        "Context / Placement": "Under Radiology Administration & IT modules"
    },
    {
        "Source URL": "https://victoryhcspl.com/contact-us/",
        "Target URL": "https://victoryhcspl.com/healthcare-training/",
        "Anchor Text": "Healthcare Training course catalogue",
        "Context / Placement": "Above contact form for admission inquiries"
    },
    {
        "Source URL": "https://victoryhcspl.com/gallery/",
        "Target URL": "https://victoryhcspl.com/healthcare-training/",
        "Anchor Text": "healthcare training curriculum details",
        "Context / Placement": "In image caption / gallery introduction paragraph"
    },
    {
        "Source URL": "https://victoryhcspl.com/clientele/",
        "Target URL": "https://victoryhcspl.com/healthcare-training/",
        "Anchor Text": "corporate radiology training for hospital staff",
        "Context / Placement": "In enterprise client engagement section"
    },
    {
        "Source URL": "https://victoryhcspl.com/careers/",
        "Target URL": "https://victoryhcspl.com/healthcare-training/",
        "Anchor Text": "medical imaging certification courses",
        "Context / Placement": "In 'Upskill with Us' career guidance notice"
    },
    {
        "Source URL": "https://victoryhcspl.com/",
        "Target URL": "https://victoryhcspl.com/contact-us/",
        "Anchor Text": "schedule a healthcare consultation",
        "Context / Placement": "Homepage bottom banner CTA"
    },
    {
        "Source URL": "https://victoryhcspl.com/infra-management/",
        "Target URL": "https://victoryhcspl.com/consulting/",
        "Anchor Text": "healthcare regulatory compliance consulting",
        "Context / Placement": "Under infrastructure audit section"
    },
    {
        "Source URL": "https://victoryhcspl.com/consulting/",
        "Target URL": "https://victoryhcspl.com/his-ris-pacs/",
        "Anchor Text": "cloud-based HIS and PACS implementation",
        "Context / Placement": "Under hospital digitization consulting section"
    },
    {
        "Source URL": "Site-wide Header (All Pages)",
        "Target URL": "https://victoryhcspl.com/",
        "Anchor Text": "Victory Healthcare Services Logo (Self-referencing root)",
        "Context / Placement": "Site-wide logo link (replacing 301-redirected /home/ link)"
    }
]

print("Writing 07_internal_linking_plan.csv...")
for d in dest_dirs:
    with open(f"{d}/07_internal_linking_plan.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Source URL", "Target URL", "Anchor Text", "Context / Placement"])
        writer.writeheader()
        writer.writerows(internal_linking_plan)

print("=== 5. GENERATING 08_KEYWORD_MAP.CSV ===")
keyword_clusters = [
    {
        "Cluster / Topic": "Healthcare Training Core",
        "Keyword": "healthcare training in india",
        "Search Intent": "Commercial / Informational",
        "Target URL": "https://victoryhcspl.com/healthcare-training/",
        "Priority": "High",
        "Current Visibility": "Unranked",
        "Content Requirement": "Core pillar page covering courses, modes, eligibility & certification"
    },
    {
        "Cluster / Topic": "Healthcare Training Core",
        "Keyword": "medical imaging training courses",
        "Search Intent": "Commercial",
        "Target URL": "https://victoryhcspl.com/healthcare-training/",
        "Priority": "High",
        "Current Visibility": "Unranked",
        "Content Requirement": "Dedicated modality overview (CT, MRI, X-ray, Ultrasound)"
    },
    {
        "Cluster / Topic": "CT & MRI Modality",
        "Keyword": "ct mri technician training course",
        "Search Intent": "Transactional / Commercial",
        "Target URL": "https://victoryhcspl.com/healthcare-training/ct-mri-training/ (New)",
        "Priority": "High",
        "Current Visibility": "Unranked",
        "Content Requirement": "Dedicated child course page: duration, hands-on scanner protocol, eligibility"
    },
    {
        "Cluster / Topic": "CT & MRI Modality",
        "Keyword": "cross sectional imaging course india",
        "Search Intent": "Commercial / Informational",
        "Target URL": "https://victoryhcspl.com/healthcare-training/cross-sectional-imaging/ (New)",
        "Priority": "High",
        "Current Visibility": "Unranked",
        "Content Requirement": "Anatomy protocols, axial/sagittal/coronal interpretation, syllabus"
    },
    {
        "Cluster / Topic": "Ultrasound & Sonography",
        "Keyword": "ultrasound technician training course bangalore",
        "Search Intent": "Transactional / Local",
        "Target URL": "https://victoryhcspl.com/healthcare-training/ultrasound-training/ (New)",
        "Priority": "High",
        "Current Visibility": "Unranked",
        "Content Requirement": "Sonography machine operation, hands-on scanning, certification guidelines"
    },
    {
        "Cluster / Topic": "Post-Processing & 3D Imaging",
        "Keyword": "3d post processing radiology training",
        "Search Intent": "Informational / Commercial",
        "Target URL": "https://victoryhcspl.com/healthcare-training/post-processing/ (New)",
        "Priority": "Medium",
        "Current Visibility": "Unranked",
        "Content Requirement": "Workstation software (Vitrea, TeraRecon, Siemens Syngo) training"
    },
    {
        "Cluster / Topic": "Radiology Administration",
        "Keyword": "radiology administration course",
        "Search Intent": "Commercial",
        "Target URL": "https://victoryhcspl.com/healthcare-training/radiology-administration/ (New)",
        "Priority": "Medium",
        "Current Visibility": "Unranked",
        "Content Requirement": "Department management, PACS admin, workflow optimization, turnaround time"
    },
    {
        "Cluster / Topic": "Quality Assurance & Compliance",
        "Keyword": "radiology quality assurance training india",
        "Search Intent": "Commercial / B2B",
        "Target URL": "https://victoryhcspl.com/healthcare-training/quality-assurance/ (New)",
        "Priority": "Medium",
        "Current Visibility": "Unranked",
        "Content Requirement": "AERB / NABH radiation safety guidelines, phantom testing, audit protocols"
    },
    {
        "Cluster / Topic": "Location Specific (Bangalore)",
        "Keyword": "paramedical imaging courses in bangalore",
        "Search Intent": "Transactional / Local",
        "Target URL": "https://victoryhcspl.com/healthcare-training/",
        "Priority": "High",
        "Current Visibility": "Unranked",
        "Content Requirement": "Bangalore center location, classroom & practical lab details"
    },
    {
        "Cluster / Topic": "Corporate Hospital Training",
        "Keyword": "hospital radiology staff training program",
        "Search Intent": "Commercial / B2B",
        "Target URL": "https://victoryhcspl.com/healthcare-training/",
        "Priority": "Medium",
        "Current Visibility": "Unranked",
        "Content Requirement": "B2B institutional training module for diagnostic chains & hospital departments"
    }
]

print("Writing 08_keyword_map.csv...")
for d in dest_dirs:
    with open(f"{d}/08_keyword_map.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Cluster / Topic", "Keyword", "Search Intent", "Target URL", "Priority", "Current Visibility", "Content Requirement"])
        writer.writeheader()
        writer.writerows(keyword_clusters)

print("=== 6. GENERATING 09_SCHEMA_DRAFTS.JSON ===")
schema_drafts = {
    "_comment": "Ready-to-use JSON-LD schemas. Values marked with [CONFIRM WITH CLIENT] must be confirmed prior to production deployment.",
    "educational_organization_schema": {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "@id": "https://victoryhcspl.com/#organization",
        "name": "Victory Healthcare Services Pvt Ltd",
        "legalName": "Victory Healthcare Services Private Limited",
        "url": "https://victoryhcspl.com/",
        "logo": "https://victoryhcspl.com/wp-content/uploads/2024/03/Logo-Eng.png",
        "description": "Provider of healthcare training, medical imaging continuing education, HIS/RIS/PACS software, and hospital infrastructure management in India.",
        "foundingDate": "2024",
        "founder": [
            {
                "@type": "Person",
                "name": "Anto Ramesh Delvi",
                "jobTitle": "Founder & Director",
                "description": "Healthcare operations and radiology expert with 30 years experience; former GM at Columbia Asia Hospitals.",
                "sameAs": "https://in.linkedin.com/in/antorameshdelvi"
            },
            {
                "@type": "Person",
                "name": "Vijaya Kumar C",
                "jobTitle": "Founder & Director",
                "description": "Healthcare administration & radiology specialist with 19+ years experience at Columbia Asia and Manipal Hospitals."
            }
        ],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "The Ledge Apartment, B 108 B Block, Jakkur, Yelahanka",
            "addressLocality": "Bangalore",
            "addressRegion": "Karnataka",
            "postalCode": "560064",
            "addressCountry": "IN"
        },
        "contactPoint": [
            {
                "@type": "ContactPoint",
                "telephone": "+91-9916509090",
                "contactType": "admissions",
                "areaServed": "IN",
                "availableLanguage": ["English", "Hindi", "Kannada"]
            }
        ],
        "sameAs": [
            "https://in.linkedin.com/in/antorameshdelvi",
            "https://www.facebook.com/anto.r.delvi/"
        ]
    },
    "local_business_schema": {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": "https://victoryhcspl.com/#localbusiness",
        "name": "Victory Healthcare Services - Training & Corporate Office",
        "image": "https://victoryhcspl.com/wp-content/uploads/2024/03/Logo-Eng.png",
        "telephone": "+91-9916509090",
        "email": "victoryantovijay@gmail.com",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "The Ledge Apartment, B 108 B Block, Jakkur, Yelahanka",
            "addressLocality": "Bangalore",
            "addressRegion": "Karnataka",
            "postalCode": "560064",
            "addressCountry": "IN"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 13.0784,
            "longitude": 77.6070
        },
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                "opens": "09:00",
                "closes": "18:00"
            }
        ],
        "priceRange": "INR"
    },
    "course_ct_mri_schema": {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": "CT & MRI Module-Based Training",
        "description": "Comprehensive modular training in Computed Tomography (CT) and Magnetic Resonance Imaging (MRI) scanning protocols, patient positioning, and diagnostic post-processing.",
        "provider": {
            "@type": "Organization",
            "name": "Victory Healthcare Services Pvt Ltd",
            "sameAs": "https://victoryhcspl.com/"
        },
        "hasCourseInstance": [
            {
                "@type": "CourseInstance",
                "courseMode": ["Blended", "Online", "Onsite"],
                "courseWorkload": "PT60H [CONFIRM WITH CLIENT]",
                "instructor": {
                    "@type": "Person",
                    "name": "Anto Ramesh Delvi",
                    "jobTitle": "Radiology Specialist & Senior Trainer"
                }
            }
        ]
    },
    "course_ultrasound_schema": {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": "Training on Ultrasound (Sonographer)",
        "description": "Practical hands-on training for Sonographers covering probe handling, pelvic/abdominal scanning techniques, machine optimization, and clinical reporting workflows.",
        "provider": {
            "@type": "Organization",
            "name": "Victory Healthcare Services Pvt Ltd",
            "sameAs": "https://victoryhcspl.com/"
        },
        "hasCourseInstance": [
            {
                "@type": "CourseInstance",
                "courseMode": ["Onsite", "Blended"],
                "location": {
                    "@type": "Place",
                    "name": "Victory Healthcare Clinical Training Lab [CONFIRM WITH CLIENT]",
                    "address": {
                        "@type": "PostalAddress",
                        "addressLocality": "Bangalore",
                        "addressCountry": "IN"
                    }
                }
            }
        ]
    },
    "faq_page_schema_for_healthcare_training": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "Who is eligible to enroll in the Healthcare & Medical Imaging Training programs?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "The programs are designed for medical imaging technologists, B.Sc/Diploma Radiography graduates, sonographers, radiology residents, and healthcare administrators looking to upgrade their clinical and technical competencies."
                }
            },
            {
                "@type": "Question",
                "name": "Are the training sessions conducted online or offline?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Victory Healthcare Services offers a flexible blended learning model comprising interactive online theory webinars and monthly live sessions, combined with bi-annual hands-on practical workshops on actual diagnostic workstations."
                }
            },
            {
                "@type": "Question",
                "name": "What imaging modalities are covered in the training curriculum?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "The curriculum covers Cross-Sectional Imaging, CT (Computed Tomography), MRI (Magnetic Resonance Imaging), Ultrasound/Sonography scanning, 3D Post-Processing workstations, and Radiology Department Administration."
                }
            },
            {
                "@type": "Question",
                "name": "Do participants receive a certificate upon course completion?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes, candidates who successfully complete the modular coursework, practical assessments, and attendance criteria receive a Certificate of Completion from Victory Healthcare Services Pvt Ltd."
                }
            },
            {
                "@type": "Question",
                "name": "How can I apply or enquire about course fees and upcoming batch schedules?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "You can enquire directly via the admission form on our Healthcare Training page, contact our admissions office at +91 99165 09090, or message us via WhatsApp."
                }
            }
        ]
    },
    "breadcrumb_schema_service_page": {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://victoryhcspl.com/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Healthcare Training",
                "item": "https://victoryhcspl.com/healthcare-training/"
            }
        ]
    }
}

print("Writing 09_schema_drafts.json...")
for d in dest_dirs:
    with open(f"{d}/09_schema_drafts.json", "w", encoding="utf-8") as f:
        json.dump(schema_drafts, f, indent=2)

print("Deliverables 04 through 09 created successfully!")
