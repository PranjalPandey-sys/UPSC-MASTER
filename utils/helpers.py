"""
utils/helpers.py — UPSC Master Bot Utility Functions
======================================================
Date utilities, text formatters, ASCII bar chart renderer,
XP/rank calculators, and miscellaneous helpers.
"""
import hashlib
import logging
import random
from datetime import date, datetime, timezone, timedelta
from typing import Any

import config

logger = logging.getLogger(__name__)

# ── IST timezone ───────────────────────────────────────────────────────────────
IST = timezone(timedelta(hours=5, minutes=30))


def now_ist() -> datetime:
    """Return current datetime in IST."""
    return datetime.now(IST)


def today_ist() -> date:
    """Return today's date in IST."""
    return now_ist().date()


def iso_now() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def date_str(d: date | None = None) -> str:
    """Return date as YYYY-MM-DD string."""
    return (d or today_ist()).isoformat()


def fmt_datetime(dt_str: str) -> str:
    """Format ISO datetime string for display."""
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.astimezone(IST).strftime("%d %b %Y, %I:%M %p IST")
    except Exception:
        return dt_str or "—"


# ── Text formatting ────────────────────────────────────────────────────────────

def esc(text: str) -> str:
    """Escape HTML special characters for Telegram HTML parse mode."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def bold(text: str) -> str:
    return f"<b>{esc(text)}</b>"


def italic(text: str) -> str:
    return f"<i>{esc(text)}</i>"


def code(text: str) -> str:
    return f"<code>{esc(text)}</code>"


def truncate(text: str, max_len: int = 200) -> str:
    """Truncate text with ellipsis if too long."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


# ── ASCII progress bars ────────────────────────────────────────────────────────

def progress_bar(pct: float, width: int = 10, filled: str = "█", empty: str = "░") -> str:
    """
    Render a text progress bar.
    
    Example: progress_bar(65, 10) → "██████░░░░ 65%"
    """
    pct = max(0.0, min(100.0, float(pct)))
    filled_count = round(pct / 100 * width)
    bar = filled * filled_count + empty * (width - filled_count)
    return f"{bar} {pct:.0f}%"


def compact_bar(pct: float, width: int = 8) -> str:
    """Compact progress bar for inline display."""
    return progress_bar(pct, width, "▓", "░")


def subject_score_card(subject: str, score: float, max_len: int = 20) -> str:
    """Format a single subject score line for dashboard display."""
    label = subject[:max_len].ljust(max_len)
    bar = compact_bar(score, 8)
    return f"<code>{label}</code> {bar}"


def sparkline(values: list[int | float], width: int = 24) -> str:
    """
    Generate a text-based sparkline.
    
    values: list of numbers
    Returns something like: ▁▂▃▅▂▁▁▂▁▁▃▅
    """
    blocks = " ▁▂▃▄▅▆▇█"
    if not values:
        return "▁" * width
    mn, mx = min(values), max(values)
    if mx == mn:
        return "▄" * min(len(values), width)
    result = []
    for v in values[-width:]:
        idx = round((v - mn) / (mx - mn) * (len(blocks) - 1))
        result.append(blocks[idx])
    return "".join(result)


# ── XP / Rank helpers ──────────────────────────────────────────────────────────

def get_rank(xp: int) -> str:
    """Return rank title for given XP."""
    for threshold, title in reversed(config.XP_RANKS):
        if xp >= threshold:
            return title
    return config.XP_RANKS[0][1]


def xp_to_next_rank(xp: int) -> tuple[str, int, int]:
    """
    Return (next_rank_title, xp_needed, xp_to_go).
    
    Returns ('MAX', 0, 0) if already at max rank.
    """
    for i, (threshold, title) in enumerate(config.XP_RANKS):
        if xp < threshold:
            needed = threshold
            to_go  = threshold - xp
            return title, needed, to_go
    return ("MAX", 0, 0)


# ── Plan ID helpers ────────────────────────────────────────────────────────────

def plan_id(level: str, months: int, hours: int) -> str:
    """Build a canonical plan ID string."""
    return f"{level}_{months}months_{hours}hours"


def parse_plan_id(pid: str) -> tuple[str, int, int] | None:
    """
    Parse a plan ID back into (level, months, hours).
    Returns None if parsing fails.
    """
    try:
        parts = pid.split("_")
        # pid format: "beginner_12months_6hours"
        level  = parts[0]
        months = int(parts[1].replace("months", ""))
        hours  = int(parts[2].replace("hours", ""))
        return level, months, hours
    except Exception:
        return None


# ── Streak helpers ─────────────────────────────────────────────────────────────

def streak_emoji(streak: int) -> str:
    """Return appropriate emoji for streak count."""
    if streak >= 30:
        return "🔥🔥🔥"
    if streak >= 14:
        return "🔥🔥"
    if streak >= 7:
        return "🔥"
    if streak >= 3:
        return "⚡"
    return "✨"


def level_emoji(level: str) -> str:
    """Return emoji for preparation level."""
    return {"beginner": "🌱", "intermediate": "📘", "advanced": "🚀"}.get(level, "📚")


def timeline_label(months: int) -> str:
    """Human-readable timeline label."""
    return {
        3:  "3 Months — Prelims Sprint",
        6:  "6 Months — Focused Prep",
        12: "12 Months — Full Cycle",
        24: "24 Months — IAS Track",
    }.get(months, f"{months} Months")


def hours_label(hours: int) -> str:
    """Human-readable daily hours label."""
    return {
        2: "2 hrs/day — Working Professional",
        4: "4 hrs/day — Balanced Aspirant",
        6: "6 hrs/day — Dedicated Aspirant",
        8: "8 hrs/day — Full-Time Aspirant",
    }.get(hours, f"{hours} hrs/day")


# ── Phase helpers ──────────────────────────────────────────────────────────────

PHASE_EMOJI = {
    "Foundation":     "🌱",
    "Coverage":       "📚",
    "Retention":      "🔄",
    "Prelims":        "⚡",
    "Mains":          "✍️",
    "Interview":      "🎤",
    "Consolidation":  "🏁",
    "Mains_Intro":    "✍️",
}

PHASE_COLOR_LABEL = {
    "Foundation":    "Green",
    "Coverage":      "Blue",
    "Retention":     "Orange",
    "Prelims":       "Red",
    "Mains":         "Purple",
    "Interview":     "Gold",
    "Consolidation": "Teal",
}


def phase_display(phase: str) -> str:
    """Format phase name with emoji."""
    emoji = PHASE_EMOJI.get(phase, "📌")
    return f"{emoji} {phase}"


# ── Daily motivation ───────────────────────────────────────────────────────────

def get_motivation(user_id: int, day: int = 0) -> str:
    """
    Get a deterministic but varied motivation line.
    Uses user_id + day to seed selection (same line per user per day).
    """
    seed = int(hashlib.sha256(f"{user_id}-{day}".encode()).hexdigest(), 16)
    idx  = seed % len(config.MOTIVATION_LINES)
    return config.MOTIVATION_LINES[idx]


# ── Miscellaneous ──────────────────────────────────────────────────────────────

def pluralize(count: int, singular: str, plural: str | None = None) -> str:
    """Return correct singular/plural form."""
    if plural is None:
        plural = singular + "s"
    return f"{count} {singular if count == 1 else plural}"


def days_remaining_label(days: int) -> str:
    """Human-friendly label for days remaining."""
    if days <= 0:
        return "Plan complete!"
    if days == 1:
        return "1 day left"
    if days <= 7:
        return f"{days} days left ⚡"
    if days <= 30:
        return f"{days} days left"
    months = days // 30
    rem    = days % 30
    if rem == 0:
        return f"{months} month{'s' if months > 1 else ''} left"
    return f"~{months}m {rem}d left"


def safe_int(value: Any, default: int = 0) -> int:
    """Safely convert value to int."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def chunk_list(lst: list, size: int) -> list[list]:
    """Split a list into chunks of given size."""
    return [lst[i:i+size] for i in range(0, len(lst), size)]
