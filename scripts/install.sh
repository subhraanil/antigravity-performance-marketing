#!/usr/bin/env bash
# One-Click Installer for Antigravity Performance Marketing Skill & Knowledge
# Run on macOS / Linux: bash install.sh

set -e

echo "=========================================================="
echo "Installing Antigravity Performance Marketing Operating System"
echo "=========================================================="

USER_HOME="${HOME}"
GEMINI_CONFIG_DIR="${USER_HOME}/.gemini/config/skills/performance-marketing"
GEMINI_KNOWLEDGE_DIR="${USER_HOME}/.gemini/antigravity/knowledge"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "${SCRIPT_DIR}")"

# 1. Install Skill globally
echo "[1/3] Installing Performance Marketing Skill to ${GEMINI_CONFIG_DIR}..."
mkdir -p "${GEMINI_CONFIG_DIR}"
cp -f "${REPO_ROOT}/SKILL.md" "${GEMINI_CONFIG_DIR}/"
cp -rf "${REPO_ROOT}/knowledge" "${GEMINI_CONFIG_DIR}/"
cp -rf "${REPO_ROOT}/rules" "${GEMINI_CONFIG_DIR}/"
cp -rf "${REPO_ROOT}/subagents" "${GEMINI_CONFIG_DIR}/"
cp -rf "${REPO_ROOT}/templates" "${GEMINI_CONFIG_DIR}/"
cp -rf "${REPO_ROOT}/workflows" "${GEMINI_CONFIG_DIR}/"

# 2. Populate Knowledge Base
echo "[2/3] Installing Knowledge Base to ${GEMINI_KNOWLEDGE_DIR}..."
mkdir -p "${GEMINI_KNOWLEDGE_DIR}"
cp -f "${REPO_ROOT}"/knowledge/*.md "${GEMINI_KNOWLEDGE_DIR}/"

# 3. Configure Global Rules (GEMINI.md & AGENTS.md)
echo "[3/3] Configuring Global Rules in ~/.gemini..."
cp -f "${REPO_ROOT}/rules/GEMINI.md" "${USER_HOME}/.gemini/GEMINI.md"
cp -f "${REPO_ROOT}/rules/AGENTS.md" "${USER_HOME}/.gemini/AGENTS.md"

echo ""
echo "SUCCESS! The Performance Marketing Skill and Knowledge Base are installed."
echo "Antigravity will automatically load the skill and rules in any conversation."
echo "=========================================================="
