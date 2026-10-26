# System Migration & Restoration Guide

This guide ensures complete, seamless restoration of your **Performance Marketing Operating System, Knowledge Base, Brand Profiles, Case Studies, and Subagents** when transitioning to a new computer or virtual environment.

---

## ⚡ Quick 1-Click Restoration (TL;DR)

Open your terminal on your new computer and run the corresponding command:

### 🪟 Windows (PowerShell - Run as Administrator or Standard User)
```powershell
# 1. Clone repository to your local Antigravity skills directory
git clone https://github.com/subhraanil/antigravity-performance-marketing.git $HOME\.gemini\config\skills\performance-marketing

# 2. Run the automated installer & knowledge sync script
powershell -ExecutionPolicy Bypass -File $HOME\.gemini\config\skills\performance-marketing\scripts\install.ps1
```

### 🍎 macOS / 🐧 Linux (Terminal)
```bash
# 1. Clone repository to your local Antigravity skills directory
git clone https://github.com/subhraanil/antigravity-performance-marketing.git ~/.gemini/config/skills/performance-marketing

# 2. Run the automated installer & knowledge sync script
bash ~/.gemini/config/skills/performance-marketing/scripts/install.sh
```

That's it! Everything will be automatically placed in the correct directories for Antigravity, the Antigravity IDE, and the Antigravity CLI.

---

## 📦 What Is Restored Automatically

When you run `install.ps1` or `install.sh`, the following assets are synchronized across your new system:

| Asset Category | Target System Path | Description |
| :--- | :--- | :--- |
| **Agent Skill** | `~/.gemini/config/skills/performance-marketing/` | Complete performance marketing skill package with `SKILL.md` |
| **Global Knowledge Base** | `~/.gemini/antigravity/knowledge/` | 13 persistent domain playbooks (Meta, Google, GMC, SEO, AEO/GEO, MMM, etc.) |
| **Brand Profiles** | `~/.gemini/antigravity/scratch/digital-marketing/brands/` | Brand context cards (Amma Alochana, Pet Mode, Pajama Village, Kuri, Nutrabytes, etc.) |
| **Case Studies & Audits** | `~/.gemini/antigravity/scratch/digital-marketing/case-studies/` | Structured forensic audits across 6 client verticals (22 deep-dive markdown files) |
| **Global Agent Rules** | `~/.gemini/antigravity/scratch/digital-marketing/.antigravity/rules` | Campaign guardrails (PAUSED status, ≤20% budget swing, EU AI Act) |
| **Workspace Manifests** | `~/.gemini/antigravity/scratch/digital-marketing/rules/` | `GEMINI.md`, `AGENTS.md`, and subagent definitions |
| **Deliverable Templates** | `~/.gemini/antigravity/scratch/digital-marketing/templates/` | Meta Ads JSON, Google Ads JSON, Proposal Markdown, Launch Briefs |
| **SOP Workflows** | `~/.gemini/antigravity/scratch/digital-marketing/workflows/` | 12-Part Flow, Campaign Launch Checklist, Competitor Sweep, Onboarding |

---

## 🔍 Verification & Health Check

After running the installer on your new machine, verify that everything is intact by running:

### 1. Inspect Brand Profiles
```powershell
# Windows
python $HOME\.gemini\config\skills\performance-marketing\scripts\brand_manager.py list

# macOS / Linux
python3 ~/.gemini/config/skills/performance-marketing/scripts/brand_manager.py list
```
*Expected output*: Lists all 7 brands (`amma-alochana`, `airdog`, `kuri`, `nutrabytes`, `pajama-village`, `pet-mode`, `share-samadhan`).

### 2. Verify Case Studies
```powershell
# Windows
Get-ChildItem -Recurse $HOME\.gemini\config\skills\performance-marketing\case-studies

# macOS / Linux
find ~/.gemini/config/skills/performance-marketing/case-studies -type f
```
*Expected output*: Lists all 6 organized folders (`amma-alochana`, `kuri`, `pajama-village`, `pet-mode`, `seo-and-publishing`, `share-samadhan`).

### 3. Verify Knowledge Playbooks
```powershell
# Windows
Get-ChildItem $HOME\.gemini\antigravity\knowledge

# macOS / Linux
ls -l ~/.gemini/antigravity/knowledge
```
*Expected output*: Lists all 13 playbooks.

---

## 🛠️ Step-by-Step Manual Restoration (If Git Clone Fails)

If you prefer to configure manually or are restoring from a USB drive/zip backup:

1. **Extract Repository**:
   Place the files into:
   - Windows: `C:\Users\<username>\.gemini\config\skills\performance-marketing`
   - Linux/Mac: `/home/<username>/.gemini/config/skills/performance-marketing`

2. **Copy Knowledge Playbooks**:
   Copy everything from `knowledge/` to:
   - Windows: `C:\Users\<username>\.gemini\antigravity\knowledge\`
   - Linux/Mac: `/home/<username>/.gemini/antigravity/knowledge/`

3. **Copy Rules**:
   Copy `rules/.antigravity-rules` to:
   - Windows: `C:\Users\<username>\.gemini\antigravity\scratch\digital-marketing\.antigravity\rules`
   - Linux/Mac: `/home/<username>/.gemini/antigravity/scratch/digital-marketing/.antigravity/rules`

4. **Copy Brand Contexts & Case Studies**:
   Copy `brands/` and `case-studies/` to:
   - Windows: `C:\Users\<username>\.gemini\antigravity\scratch\digital-marketing\`
   - Linux/Mac: `/home/<username>/.gemini/antigravity/scratch/digital-marketing/`

---

## 💡 Best Practices on the New PC

1. **Active Workspace**:
   Set your Antigravity active workspace to:
   `C:\Users\<username>\.gemini\antigravity\scratch\digital-marketing` (Windows) or
   `~/.gemini/antigravity/scratch/digital-marketing` (macOS/Linux).
2. **Subagents Active**:
   Antigravity will automatically detect `media_buyer`, `marketing_strategist`, `growth_engineer`, `seo_specialist`, `brand_guardian`, and `analytics_analyst`.
3. **Always Paused Safety Net**:
   The safety rules are globally baked into `.antigravity/rules` and `GEMINI.md`. All newly generated campaigns will default to `PAUSED` state.
