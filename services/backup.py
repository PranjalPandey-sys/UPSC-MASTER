"""
services/backup.py — GitHub Backup Service
"""
import asyncio
import base64
import logging
import pathlib

import config

logger = logging.getLogger(__name__)


async def run_backup() -> str:
    """
    Backup DB to GitHub if credentials are configured.
    Returns a status string.
    """
    if not config.GITHUB_TOKEN or not config.GITHUB_REPO:
        return "⚠️ GitHub backup not configured (GITHUB_TOKEN / GITHUB_REPO not set)."

    try:
        result = await asyncio.to_thread(_backup_sync)
        return result
    except Exception as e:
        logger.exception("Backup failed: %s", e)
        return f"❌ Backup failed: {e}"


def _backup_sync() -> str:
    import json
    import urllib.request

    db_path = pathlib.Path(config.DB_PATH)
    if not db_path.exists():
        return "❌ Database file not found."

    with open(db_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()

    api_url = f"https://api.github.com/repos/{config.GITHUB_REPO}/contents/backup/upsc_bot.db"
    headers = {
        "Authorization": f"token {config.GITHUB_TOKEN}",
        "Content-Type":  "application/json",
        "User-Agent":    "UPSC-Master-Bot/3.0",
    }

    # Get current SHA (needed for update)
    sha = None
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            sha = json.loads(resp.read().decode()).get("sha")
    except Exception:
        pass

    payload: dict = {
        "message": f"Auto-backup DB — UPSC Master Bot",
        "content": content,
    }
    if sha:
        payload["sha"] = sha

    req = urllib.request.Request(
        api_url,
        data=json.dumps(payload).encode(),
        headers=headers,
        method="PUT",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        code = resp.status

    if code in (200, 201):
        size_kb = db_path.stat().st_size // 1024
        return f"✅ Backup successful!\nFile: upsc_bot.db ({size_kb} KB)\nRepo: {config.GITHUB_REPO}"
    return f"❌ Backup failed with HTTP {code}"
