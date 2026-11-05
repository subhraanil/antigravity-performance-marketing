---
description: Check Core Web Vitals score using PageSpeed Insights and view page source
---
1. Ask the user for the website URL they want to check.

2. Run the following command to fetch the PageSpeed Insights score (strategy defaults to mobile):
   ```powershell
   $url = "TARGET_URL_HERE" # User provided URL
   curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$url&strategy=mobile"
   ```
   *Note: Extract the score from the JSON response at `lighthouseResult.categories.performance.score` (0-1 scale).*

3. Display the Performance Score (multiply by 100 for percentage).

4. Open the page source in the default browser using the `view-source:` scheme:
   ```powershell
   Start-Process "chrome" "view-source:$url"
   # OR if Chrome is not available/default, instruct user to visit view-source:URL
   ```
---
**Note**: If finding relevant images from Google is getting difficult for you during any step, you can just generate those relevant images using **Google nano banana** (via the `generate_image` tool).
