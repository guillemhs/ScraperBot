#!/bin/bash
# Cron wrapper that executes the upload post script.
#
# Acceptance criteria addressed:
#   - Runs on a Linux box via cron (schedule defined in cron/crontab).
#   - Compromise between execution time and execution of the script:
#     the job runs once per hour and logs its output for auditing.

set -u

# Project layout, overridable via the environment.
PROJECT_DIR="${SCRAPER_BOT_DIR:-$HOME/ScraperBot}"
PYTHON_BIN="${PYTHON_BIN:-/usr/bin/python}"
LOG_FILE="${LOG_FILE:-$HOME/ScraperBot/cron/upload_post.log}"

# Make sure the log file can be written.
mkdir -p "$(dirname "$LOG_FILE")"

# Run the upload post script from the project directory.
cd "$PROJECT_DIR" || exit 1

exec "$PYTHON_BIN" upload_post.py >> "$LOG_FILE" 2>&1
