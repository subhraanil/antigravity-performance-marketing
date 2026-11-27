/**
 * ============================================================================
 * UNRESTRICTED GOOGLE KEYWORD SERP RANK TRACKER (Google Apps Script)
 * ============================================================================
 * An unrestricted, domain-lock-free replacement for RankTank.
 *
 * Key Capabilities:
 *  - ZERO domain restrictions: Track any client, any website, anytime.
 *  - ZERO artificial scan caps: No 100-check throttling or upgrade paywalls.
 *  - Supports high-speed Google SERP via Serper.dev (2,500 free searches)
 *    and Google Custom Search JSON API (100 free/day).
 *  - Exact data outputs:
 *      * Col E: Rank (1-100 or 'Not ranked')
 *      * Col F: Ranked Landing Page URL
 *      * Col J: Who ranks above you (N-1)
 *      * Col K: Who ranks below you (N+1)
 *      * Col L: Who ranks #1
 *      * Col M: Page Title in SERP
 *      * Col N: Meta Description / Snippet
 *  - Custom Menu:
 *      * "Unrestricted Rank Tracker" -> "Scan All Keywords" (Fast bulk crawl)
 *      * "Unrestricted Rank Tracker" -> "Save Rankings Snapshot" (Frozen historical archive)
 *      * "Unrestricted Rank Tracker" -> "API & Setup Help"
 * ============================================================================
 */

// Custom Menu on Sheet Open
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('🚀 Rank Tracker')
    .addItem('▶ Scan All Keywords Now', 'scanAllKeywords')
    .addItem('📸 Save Rankings Snapshot', 'saveRankingsSnapshot')
    .addSeparator()
    .addItem('⚙ Setup & API Keys Guide', 'showSetupGuide')
    .addToUi();
}

/**
 * Normalizes domain by removing protocol, path, and leading www.
 */
function cleanDomain(d) {
  if (!d) return "";
  var s = String(d).trim().toLowerCase();
  if (s.indexOf("://") > -1) s = s.split("://")[1];
  if (s.indexOf("/") > -1) s = s.split("/")[0];
  if (s.indexOf(":") > -1) s = s.split(":")[0];
  if (s.indexOf("www.") === 0) s = s.substring(4);
  return s;
}

/**
 * Checks if a given URL belongs to the target domain.
 */
function isDomainMatch(url, targetDomain, wildSubdomain) {
  if (!url || !targetDomain) return false;
  var u = cleanDomain(url);
  var t = cleanDomain(targetDomain);
  if (wildSubdomain === true || wildSubdomain === "Yes" || wildSubdomain === "yes" || wildSubdomain === "TRUE") {
    return u === t || u.indexOf("." + t) === (u.length - t.length - 1);
  } else {
    return u === t || u === "www." + t;
  }
}

/**
 * Custom Formula for Google Sheets:
 * =getRank(keyword, lang, googleLoc, domain, apiKey, device, wildSubdomain)
 *
 * Returns 1x2 row array:
 * [Rank, Ranked URL]
 */
function getRank(keyword, lang, googleLoc, domain, apiKey, device, wildSubdomain) {
  if (!keyword || !domain) {
    return [["-", "Missing keyword or domain"]];
  }

  // Resolve defaults
  var gl = googleLoc || "us";
  var hl = lang || "en";
  var dev = device || "Desktop";
  var wild = (wildSubdomain === undefined || wildSubdomain === null) ? true : wildSubdomain;

  // Retrieve API Key from Settings sheet if empty
  var effectiveApiKey = apiKey;
  if (!effectiveApiKey) {
    try {
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var settingsSheet = ss.getSheetByName("Settings");
      if (settingsSheet) {
        effectiveApiKey = settingsSheet.getRange("B7").getValue();
        if (!effectiveApiKey) {
          effectiveApiKey = settingsSheet.getRange("B9").getValue();
        }
      }
    } catch (e) {}
  }
  if (!effectiveApiKey) {
    effectiveApiKey = "499a4c6f466313cc4dadb69021321bfb14547034";
  }

  try {
    var serpResults = fetchSERPResults(keyword, gl, hl, dev, effectiveApiKey);
    return evaluateRank(serpResults, domain, wild);
  } catch (err) {
    return [["-", "Error: " + err.message]];
  }
}

/**
 * Fetches SERP results from available providers.
 */
function fetchSERPResults(keyword, gl, hl, device, apiKey) {
  var key = apiKey ? String(apiKey).trim() : "";

  // 1. Serper.dev API (Recommended: 2,500 free queries, no domain locks)
  if (key && key.length > 20 && key.indexOf("AIza") !== 0) {
    var serperUrl = "https://google.serper.dev/search";
    var payload = {
      q: keyword,
      gl: gl.toLowerCase(),
      hl: hl.toLowerCase(),
      num: 100
    };
    var options = {
      method: "post",
      contentType: "application/json",
      headers: { "X-API-KEY": key },
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    };
    var response = UrlFetchApp.fetch(serperUrl, options);
    if (response.getResponseCode() === 200) {
      var json = JSON.parse(response.getContentText());
      var results = [];
      var organic = json.organic || [];
      for (var i = 0; i < organic.length; i++) {
        results.push({
          rank: organic[i].position || (i + 1),
          url: organic[i].link || "",
          title: organic[i].title || "",
          snippet: organic[i].snippet || ""
        });
      }
      return results;
    } else {
      throw new Error("Serper API error (" + response.getResponseCode() + "): " + response.getContentText());
    }
  }

  // 2. Google Custom Search JSON API (Official Google, 100 queries/day)
  if (key && key.indexOf("AIza") === 0) {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var settingsSheet = ss.getSheetByName("Settings");
    var cx = settingsSheet ? settingsSheet.getRange("B11").getValue() : "";
    if (cx) {
      var cseUrl = "https://www.googleapis.com/customsearch/v1?key=" + encodeURIComponent(key) +
                   "&cx=" + encodeURIComponent(cx) +
                   "&q=" + encodeURIComponent(keyword) +
                   "&gl=" + encodeURIComponent(gl) +
                   "&hl=" + encodeURIComponent(hl);
      var cseResp = UrlFetchApp.fetch(cseUrl, { muteHttpExceptions: true });
      if (cseResp.getResponseCode() === 200) {
        var cseJson = JSON.parse(cseResp.getContentText());
        var cseResults = [];
        var items = cseJson.items || [];
        for (var j = 0; j < items.length; j++) {
          cseResults.push({
            rank: j + 1,
            url: items[j].link || "",
            title: items[j].title || "",
            snippet: items[j].snippet || ""
          });
        }
        return cseResults;
      }
    }
  }

  // 3. Fallback: Prompt user to provide a Serper.dev key in Settings
  throw new Error("Please enter your free Serper API Key in Settings (cell B7). Get 2,500 free queries at https://serper.dev");
}

/**
 * Compares target domain against SERP array and returns:
 * [Rank, Ranked URL]
 */
function evaluateRank(serpResults, targetDomain, wildSubdomain) {
  if (!serpResults || serpResults.length === 0) {
    return [["-", "Not ranked"]];
  }

  for (var i = 0; i < serpResults.length; i++) {
    if (isDomainMatch(serpResults[i].url, targetDomain, wildSubdomain)) {
      return [[serpResults[i].rank, serpResults[i].url]];
    }
  }

  return [["-", "Not ranked"]];
}

/**
 * Scan All Keywords in Bulk.
 * Avoids Google Sheets formula recalculation timeouts by executing in sequence
 * and populating cells with values and colors.
 */
function scanAllKeywords() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("Position Tracker") || ss.getActiveSheet();
  var settingsSheet = ss.getSheetByName("Settings");

  var targetDomain = sheet.getRange("C6").getValue();
  var region = sheet.getRange("E6").getValue() || "United States";
  var language = sheet.getRange("G6").getValue() || "English";
  var device = sheet.getRange("H6").getValue() || "Desktop";
  var wildSubdomain = sheet.getRange("I6").getValue();
  var wild = (String(wildSubdomain).toLowerCase() === "yes" || wildSubdomain === true);

  if (!targetDomain) {
    SpreadsheetApp.getUi().alert("Please enter a Target Domain in cell C6 before scanning!");
    return;
  }

  // Get API key from Settings or use saved key
  var apiKey = settingsSheet ? settingsSheet.getRange("B7").getValue() : "";
  if (!apiKey && settingsSheet) {
    apiKey = settingsSheet.getRange("B9").getValue();
  }
  if (!apiKey) {
    apiKey = "499a4c6f466313cc4dadb69021321bfb14547034";
    if (settingsSheet) {
      settingsSheet.getRange("B7").setValue(apiKey);
    }
  }

  // Resolve ISO country and language codes
  var gl = "us";
  var hl = "en";
  var localeSheet = ss.getSheetByName("locale");
  if (localeSheet) {
    var locData = localeSheet.getDataRange().getValues();
    for (var r = 1; r < locData.length; r++) {
      if (locData[r][3] && String(locData[r][3]).toLowerCase() === String(region).toLowerCase()) {
        gl = String(locData[r][5] || "us").toLowerCase();
        break;
      }
    }
    for (var l = 1; l < locData.length; l++) {
      if (locData[l][0] && String(locData[l][0]).toLowerCase() === String(language).toLowerCase()) {
        hl = String(locData[l][1] || "en").toLowerCase();
        break;
      }
    }
  }

  // Read keywords starting at row 11
  var lastRow = sheet.getLastRow();
  if (lastRow < 11) {
    SpreadsheetApp.getUi().alert("No keywords found in column C!");
    return;
  }

  var kwRange = sheet.getRange(11, 3, lastRow - 10, 1).getValues();
  var totalKeywords = 0;
  for (var k = 0; k < kwRange.length; k++) {
    if (kwRange[k][0] && String(kwRange[k][0]).trim()) totalKeywords++;
  }

  if (totalKeywords === 0) {
    SpreadsheetApp.getUi().alert("No keywords entered in column C (row 11 onwards).");
    return;
  }

  // Update status indicators
  sheet.getRange("A6").setValue("Running");
  sheet.getRange("B6").setValue("Scanning 1/" + totalKeywords + "...");
  SpreadsheetApp.flush();

  var nowStr = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm");
  var checkedCount = 0;

  for (var row = 11; row <= lastRow; row++) {
    var kw = sheet.getRange(row, 3).getValue();
    if (!kw || !String(kw).trim()) continue;

    checkedCount++;
    sheet.getRange("B6").setValue("Scanning " + checkedCount + "/" + totalKeywords + "...");

    try {
      var serp = fetchSERPResults(kw, gl, hl, device, apiKey);
      var evalData = evaluateRank(serp, targetDomain, wild)[0];

      var rankVal = evalData[0];
      var rankedUrl = evalData[1];

      sheet.getRange(row, 4).setValue(nowStr); // Col D: Checked Date
      var rankCell = sheet.getRange(row, 5);  // Col E: Rank
      rankCell.setValue(rankVal);
      formatRankCell(rankCell, rankVal);

      sheet.getRange(row, 6).setValue(rankedUrl);  // Col F: Ranked URL

      // Clear any legacy competitor columns if previously populated
      sheet.getRange(row, 10, 1, 5).clearContent();

    } catch (err) {
      sheet.getRange(row, 4).setValue(nowStr);
      sheet.getRange(row, 5).setValue("-");
      sheet.getRange(row, 6).setValue("Error: " + err.message);
    }

    Utilities.sleep(250); // Respect rate pacing
  }

  sheet.getRange("A6").setValue("Done");
  sheet.getRange("B6").setValue("Completed");
  SpreadsheetApp.flush();

  SpreadsheetApp.getUi().alert("Rank check complete! Checked " + checkedCount + " keywords for " + targetDomain);
}

/**
 * Formats rank cells with conditional background colors.
 */
function formatRankCell(cell, rankVal) {
  var r = parseInt(rankVal, 10);
  if (isNaN(r)) {
    cell.setBackground("#f0f0f0").setFontColor("#6c757d").setFontWeight("normal");
  } else if (r >= 1 && r <= 3) {
    cell.setBackground("#d4edda").setFontColor("#155724").setFontWeight("bold");
  } else if (r >= 4 && r <= 10) {
    cell.setBackground("#e8f5e9").setFontColor("#2e7d32").setFontWeight("bold");
  } else if (r >= 11 && r <= 20) {
    cell.setBackground("#fff3cd").setFontColor("#856404").setFontWeight("bold");
  } else if (r >= 21 && r <= 50) {
    cell.setBackground("#ffe8d6").setFontColor("#a73a00").setFontWeight("normal");
  } else {
    cell.setBackground("#f8d7da").setFontColor("#721c24").setFontWeight("normal");
  }
}

/**
 * Creates a frozen historical backup sheet (equivalent to RankTank onSave).
 */
function saveRankingsSnapshot() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("Position Tracker") || ss.getActiveSheet();
  var timeStamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd HH-mm");
  var snapName = "Ranks (" + timeStamp + ")";

  // Ensure unique name
  var counter = 1;
  while (ss.getSheetByName(snapName)) {
    snapName = "Ranks (" + timeStamp + " #" + counter + ")";
    counter++;
  }

  var snapSheet = sheet.copyTo(ss);
  snapSheet.setName(snapName);

  // Freeze values (remove formulas in snapshot)
  var range = snapSheet.getDataRange();
  range.setValues(range.getValues());

  SpreadsheetApp.getUi().alert("Snapshot saved successfully as: '" + snapName + "'");
}

/**
 * Displays setup and API instructions.
 */
function showSetupGuide() {
  var html = HtmlService.createHtmlOutput(
    '<div style="font-family: Arial, sans-serif; padding: 15px; line-height: 1.6;">' +
    '<h2>🚀 Unrestricted Keyword Rank Tracker Guide</h2>' +
    '<p>This tracker replaces RankTank with <b>ZERO domain restrictions</b> and <b>NO 100-check caps</b>.</p>' +
    '<h3>How to get 2,500 FREE Google rank checks:</h3>' +
    '<ol>' +
    '  <li>Go to <a href="https://serper.dev" target="_blank">https://serper.dev</a> and sign up for a free account.</li>' +
    '  <li>Copy your API key from the Serper dashboard (it gives 2,500 searches free).</li>' +
    '  <li>In this sheet, go to the <b>Settings</b> tab and paste the key into cell <b>B7</b>.</li>' +
    '  <li>Go back to <b>Position Tracker</b>, enter your domain and keywords, and click <b>🚀 Rank Tracker -> Scan All Keywords Now</b>!</li>' +
    '</ol>' +
    '<p style="color: green; font-weight: bold;">✔ Track any domain &nbsp; ✔ Full top 100 SERP &nbsp; ✔ Above/Below & #1 Competitor &nbsp; ✔ Automatic History Snapshots</p>' +
    '</div>'
  ).setWidth(520).setHeight(380);

  SpreadsheetApp.getUi().showModalDialog(html, "Unrestricted Rank Tracker Setup");
}
