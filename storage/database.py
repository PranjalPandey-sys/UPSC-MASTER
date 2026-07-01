"""
storage/database.py — UPSC Master Bot SQLite Database Layer
=============================================================
Full schema + all query functions.
WAL mode for concurrent read performance.
Path: /data/upsc_bot.db (Render) or ./data/upsc_bot.db (local).
"""
import json
import logging
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime, timezone, timedelta
from typing import Any, Generator

import config
from utils.helpers import iso_now, today_ist, date_str

logger = logging.getLogger(__name__)

# ── Connection factory ─────────────────────────────────────────────────────────

def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(config.DB_PATH, check_same_thread=False, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Context manager that yields a DB connection and auto-commits/rolls-back."""
    conn = _get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ── Schema initialisation ──────────────────────────────────────────────────────

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    user_id          INTEGER PRIMARY KEY,
    username         TEXT    DEFAULT '',
    full_name        TEXT    DEFAULT '',
    language         TEXT    DEFAULT 'en',
    level            TEXT    DEFAULT 'beginner',
    timeline_months  INTEGER DEFAULT 6,
    hours_per_day    REAL    DEFAULT 4.0,
    optional_subject TEXT    DEFAULT '',
    weak_subjects    TEXT    DEFAULT '[]',
    setup_done       INTEGER DEFAULT 0,
    onboarding_step  INTEGER DEFAULT 0,
    current_day      INTEGER DEFAULT 1,
    streak           INTEGER DEFAULT 0,
    best_streak      INTEGER DEFAULT 0,
    streak_shields   INTEGER DEFAULT 0,
    xp               INTEGER DEFAULT 0,
    rank_title       TEXT    DEFAULT 'Aspirant',
    last_done_date   TEXT    DEFAULT '',
    tasks_completed  INTEGER DEFAULT 0,
    vacation_mode    INTEGER DEFAULT 0,
    vacation_end     TEXT    DEFAULT '',
    leaderboard_opt  INTEGER DEFAULT 0,
    exam_date        TEXT    DEFAULT '',
    notify_morning   INTEGER DEFAULT 1,
    notify_morning_t TEXT    DEFAULT '09:00',
    notify_midday    INTEGER DEFAULT 1,
    notify_midday_t  TEXT    DEFAULT '13:00',
    notify_evening   INTEGER DEFAULT 1,
    notify_evening_t TEXT    DEFAULT '20:00',
    notify_preview   INTEGER DEFAULT 1,
    notify_preview_t TEXT    DEFAULT '22:00',
    notify_revision  INTEGER DEFAULT 1,
    notify_weekly    INTEGER DEFAULT 1,
    banned           INTEGER DEFAULT 0,
    ban_reason       TEXT    DEFAULT '',
    created_at       TEXT,
    updated_at       TEXT,
    last_active      TEXT
);

CREATE TABLE IF NOT EXISTS plan_meta (
    user_id          INTEGER PRIMARY KEY,
    plan_id          TEXT,
    level            TEXT,
    timeline_months  INTEGER,
    hours_per_day    REAL,
    optional_subject TEXT,
    total_days       INTEGER,
    start_date       TEXT,
    created_at       TEXT,
    updated_at       TEXT
);

CREATE TABLE IF NOT EXISTS day_completions (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER,
    day_number INTEGER,
    task_id    TEXT,
    status     TEXT    DEFAULT 'pending',
    done_at    TEXT,
    UNIQUE(user_id, day_number, task_id)
);

CREATE TABLE IF NOT EXISTS revision_log (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER,
    task_id      TEXT,
    subject      TEXT,
    subtopic     TEXT,
    due_day      INTEGER,
    due_date     TEXT,
    completed    INTEGER DEFAULT 0,
    completed_at TEXT
);

CREATE TABLE IF NOT EXISTS answer_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER,
    question    TEXT,
    answer_text TEXT,
    answer_type TEXT,
    gs_paper    TEXT,
    subject     TEXT,
    score       INTEGER,
    rubric_json TEXT,
    feedback    TEXT,
    created_at  TEXT
);

CREATE TABLE IF NOT EXISTS mock_results (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER,
    test_type   TEXT,
    subject     TEXT,
    total_q     INTEGER,
    correct     INTEGER,
    accuracy    REAL,
    time_taken  INTEGER,
    weak_topics TEXT,
    created_at  TEXT
);

CREATE TABLE IF NOT EXISTS competency_scores (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id          INTEGER,
    subject          TEXT,
    coverage_pct     INTEGER DEFAULT 0,
    retention_pct    INTEGER DEFAULT 0,
    answer_writing   INTEGER DEFAULT 0,
    revision_pct     INTEGER DEFAULT 0,
    pyq_performance  INTEGER DEFAULT 0,
    mock_performance INTEGER DEFAULT 0,
    confidence       INTEGER DEFAULT 0,
    readiness        INTEGER DEFAULT 0,
    updated_at       TEXT
);

CREATE TABLE IF NOT EXISTS study_sessions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER,
    session_type TEXT,
    duration_min INTEGER,
    completed    INTEGER DEFAULT 1,
    started_at   TEXT,
    ended_at     TEXT
);

CREATE TABLE IF NOT EXISTS user_notes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER,
    day_number INTEGER,
    subject    TEXT,
    note_text  TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS bookmarks (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER,
    item_type  TEXT,
    item_key   TEXT,
    item_text  TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS xp_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER,
    amount     INTEGER,
    reason     TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS badges (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER,
    badge_id   TEXT,
    earned_at  TEXT,
    UNIQUE(user_id, badge_id)
);

CREATE TABLE IF NOT EXISTS study_buddies (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_a      INTEGER,
    user_b      INTEGER,
    matched_at  TEXT,
    active      INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS notification_queue (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER,
    notif_type   TEXT,
    message_text TEXT,
    scheduled_at TEXT,
    sent         INTEGER DEFAULT 0,
    sent_at      TEXT
);

CREATE TABLE IF NOT EXISTS image_cache (
    image_key TEXT PRIMARY KEY,
    file_id   TEXT,
    cached_at TEXT
);

CREATE TABLE IF NOT EXISTS content_overrides (
    key        TEXT PRIMARY KEY,
    value      TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS error_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    severity   TEXT,
    module     TEXT,
    function   TEXT,
    message    TEXT,
    traceback  TEXT,
    user_id    INTEGER,
    resolved   INTEGER DEFAULT 0,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS admin_audit (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id   INTEGER,
    action     TEXT,
    detail     TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS broadcast_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id    INTEGER,
    audience    TEXT,
    message     TEXT,
    total_sent  INTEGER DEFAULT 0,
    total_fail  INTEGER DEFAULT 0,
    created_at  TEXT
);

CREATE TABLE IF NOT EXISTS announcements (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT,
    body       TEXT,
    expires_at TEXT,
    active     INTEGER DEFAULT 1,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS events (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER,
    event_type TEXT,
    detail     TEXT,
    created_at TEXT
);
"""

INDEXES_SQL = """
CREATE INDEX IF NOT EXISTS idx_day_completions_user ON day_completions(user_id, day_number);
CREATE INDEX IF NOT EXISTS idx_revision_log_user    ON revision_log(user_id, due_day);
CREATE INDEX IF NOT EXISTS idx_answer_history_user  ON answer_history(user_id);
CREATE INDEX IF NOT EXISTS idx_mock_results_user    ON mock_results(user_id);
CREATE INDEX IF NOT EXISTS idx_events_user          ON events(user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_error_log_created    ON error_log(created_at);
CREATE INDEX IF NOT EXISTS idx_users_last_active    ON users(last_active);
"""


def init_db() -> None:
    """Initialise the database, create tables and indexes."""
    try:
        with get_db() as conn:
            conn.executescript(SCHEMA_SQL)
            conn.executescript(INDEXES_SQL)
        logger.info("✅ Database initialised | path=%s", config.DB_PATH)
    except Exception:
        logger.exception("❌ Database initialisation failed")
        raise


# ── Image cache ────────────────────────────────────────────────────────────────

def load_image_cache() -> dict[str, str]:
    """Load all cached Telegram file_ids from DB into memory."""
    try:
        with get_db() as conn:
            rows = conn.execute("SELECT image_key, file_id FROM image_cache").fetchall()
            return {r["image_key"]: r["file_id"] for r in rows}
    except Exception:
        logger.exception("load_image_cache failed")
        return {}


def save_image_cache(key: str, file_id: str) -> None:
    """Persist a Telegram file_id to DB."""
    try:
        with get_db() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO image_cache(image_key, file_id, cached_at) VALUES(?,?,?)",
                (key, file_id, iso_now()),
            )
    except Exception:
        logger.exception("save_image_cache failed key=%s", key)


def clear_image_cache() -> None:
    """Clear all cached file_ids (e.g. after file corruption)."""
    try:
        with get_db() as conn:
            conn.execute("DELETE FROM image_cache")
        config.IMAGE_CACHE.clear()
    except Exception:
        logger.exception("clear_image_cache failed")


# ── User CRUD ─────────────────────────────────────────────────────────────────

def get_user(user_id: int) -> sqlite3.Row | None:
    try:
        with get_db() as conn:
            return conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
    except Exception:
        logger.exception("get_user failed uid=%d", user_id)
        return None


def upsert_user(user_id: int, username: str = "", full_name: str = "") -> None:
    """Create user if not exists; update username/full_name and last_active."""
    now = iso_now()
    try:
        with get_db() as conn:
            conn.execute(
                """INSERT INTO users(user_id, username, full_name, created_at, updated_at, last_active)
                   VALUES(?,?,?,?,?,?)
                   ON CONFLICT(user_id) DO UPDATE SET
                       username=excluded.username,
                       full_name=excluded.full_name,
                       updated_at=excluded.updated_at,
                       last_active=excluded.last_active""",
                (user_id, username or "", full_name or "", now, now, now),
            )
    except Exception:
        logger.exception("upsert_user failed uid=%d", user_id)


def update_user_field(user_id: int, field: str, value: Any) -> None:
    """Generic field update for users table."""
    ALLOWED = {
        "language", "level", "timeline_months", "hours_per_day", "optional_subject",
        "weak_subjects", "setup_done", "onboarding_step", "current_day", "streak",
        "best_streak", "streak_shields", "xp", "rank_title", "last_done_date",
        "tasks_completed", "vacation_mode", "vacation_end", "leaderboard_opt",
        "exam_date", "notify_morning", "notify_morning_t", "notify_midday",
        "notify_midday_t", "notify_evening", "notify_evening_t", "notify_preview",
        "notify_preview_t", "notify_revision", "notify_weekly", "banned", "ban_reason",
        "full_name", "username", "updated_at", "last_active",
    }
    if field not in ALLOWED:
        logger.error("update_user_field: disallowed field=%s", field)
        return
    try:
        with get_db() as conn:
            conn.execute(
                f"UPDATE users SET {field}=?, updated_at=? WHERE user_id=?",
                (value, iso_now(), user_id),
            )
    except Exception:
        logger.exception("update_user_field failed uid=%d field=%s", user_id, field)


def update_last_active(user_id: int) -> None:
    """Update last_active timestamp for user."""
    try:
        with get_db() as conn:
            conn.execute(
                "UPDATE users SET last_active=? WHERE user_id=?",
                (iso_now(), user_id),
            )
    except Exception:
        pass  # Non-critical; never raise


def save_plan_meta(
    user_id: int,
    plan_id: str,
    level: str,
    months: int,
    hours: float,
    optional: str,
    total_days: int,
) -> None:
    """Save which plan a user is on."""
    now = iso_now()
    try:
        with get_db() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO plan_meta
                   (user_id, plan_id, level, timeline_months, hours_per_day,
                    optional_subject, total_days, start_date, created_at, updated_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (user_id, plan_id, level, months, hours, optional,
                 total_days, date_str(), now, now),
            )
    except Exception:
        logger.exception("save_plan_meta failed uid=%d", user_id)


def get_plan_meta(user_id: int) -> sqlite3.Row | None:
    try:
        with get_db() as conn:
            return conn.execute("SELECT * FROM plan_meta WHERE user_id=?", (user_id,)).fetchone()
    except Exception:
        logger.exception("get_plan_meta failed uid=%d", user_id)
        return None


# ── Day completions ────────────────────────────────────────────────────────────

def get_day_status(user_id: int, day_number: int) -> str:
    """
    Get the overall status for a day.
    Returns: 'done' | 'partial' | 'snoozed' | 'pending'
    """
    try:
        with get_db() as conn:
            row = conn.execute(
                "SELECT status FROM day_completions WHERE user_id=? AND day_number=? LIMIT 1",
                (user_id, day_number),
            ).fetchone()
            return row["status"] if row else "pending"
    except Exception:
        logger.exception("get_day_status failed uid=%d day=%d", user_id, day_number)
        return "pending"


def mark_day_done(user_id: int, day_number: int, task_id: str, status: str = "done") -> None:
    """Mark a specific task as done/partial/snoozed."""
    try:
        with get_db() as conn:
            conn.execute(
                """INSERT INTO day_completions(user_id, day_number, task_id, status, done_at)
                   VALUES(?,?,?,?,?)
                   ON CONFLICT(user_id, day_number, task_id) DO UPDATE SET
                       status=excluded.status, done_at=excluded.done_at""",
                (user_id, day_number, task_id, status, iso_now()),
            )
    except Exception:
        logger.exception("mark_day_done failed uid=%d day=%d", user_id, day_number)


def count_completed_days(user_id: int) -> int:
    """Count total days marked as done."""
    try:
        with get_db() as conn:
            row = conn.execute(
                "SELECT COUNT(DISTINCT day_number) FROM day_completions WHERE user_id=? AND status='done'",
                (user_id,),
            ).fetchone()
            return row[0] if row else 0
    except Exception:
        return 0


# ── Streak logic ───────────────────────────────────────────────────────────────

def update_streak(user_id: int) -> tuple[int, bool]:
    """
    Update streak after a day is marked done.
    Returns (new_streak, milestone_hit) where milestone_hit=True if 7/30-day milestone.
    """
    today = date_str()
    try:
        user = get_user(user_id)
        if not user:
            return 0, False

        last_done = user["last_done_date"] or ""
        streak    = user["streak"] or 0
        best      = user["best_streak"] or 0

        # Yesterday's date
        yesterday = date_str(date.fromisoformat(today) - timedelta(days=1))

        if last_done == today:
            return streak, False  # Already marked done today
        elif last_done == yesterday:
            streak += 1           # Consecutive day
        else:
            streak = 1            # Streak broken, restart

        best = max(best, streak)
        milestone = streak in (7, 14, 30, 60, 100, 180, 365)

        with get_db() as conn:
            conn.execute(
                """UPDATE users SET streak=?, best_streak=?, last_done_date=?, updated_at=?
                   WHERE user_id=?""",
                (streak, best, today, iso_now(), user_id),
            )

        # Streak shield at every 7-day milestone
        if milestone and streak % 7 == 0:
            shields = min((user["streak_shields"] or 0) + 1, 3)
            update_user_field(user_id, "streak_shields", shields)

        return streak, milestone

    except Exception:
        logger.exception("update_streak failed uid=%d", user_id)
        return 0, False


# ── XP system ─────────────────────────────────────────────────────────────────

def award_xp(user_id: int, amount: int, reason: str) -> int:
    """
    Award XP to user. Returns new total XP.
    Logs the transaction to xp_log table.
    """
    try:
        with get_db() as conn:
            conn.execute(
                "UPDATE users SET xp = xp + ?, updated_at=? WHERE user_id=?",
                (amount, iso_now(), user_id),
            )
            conn.execute(
                "INSERT INTO xp_log(user_id, amount, reason, created_at) VALUES(?,?,?,?)",
                (user_id, amount, reason, iso_now()),
            )
            row = conn.execute("SELECT xp FROM users WHERE user_id=?", (user_id,)).fetchone()
            return row["xp"] if row else 0
    except Exception:
        logger.exception("award_xp failed uid=%d amount=%d", user_id, amount)
        return 0


# ── Badge system ───────────────────────────────────────────────────────────────

def grant_badge(user_id: int, badge_id: str) -> bool:
    """
    Grant a badge to user. Returns True if newly earned, False if already had it.
    """
    try:
        with get_db() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO badges(user_id, badge_id, earned_at) VALUES(?,?,?)",
                (user_id, badge_id, iso_now()),
            )
            return conn.execute("SELECT changes()").fetchone()[0] > 0
    except Exception:
        logger.exception("grant_badge failed uid=%d badge=%s", user_id, badge_id)
        return False


def get_badges(user_id: int) -> list[str]:
    """Return list of badge_ids earned by user."""
    try:
        with get_db() as conn:
            rows = conn.execute(
                "SELECT badge_id FROM badges WHERE user_id=? ORDER BY earned_at",
                (user_id,),
            ).fetchall()
            return [r["badge_id"] for r in rows]
    except Exception:
        return []


# ── Answer writing ─────────────────────────────────────────────────────────────

def save_answer(
    user_id: int,
    question: str,
    answer_text: str,
    answer_type: str,
    gs_paper: str,
    subject: str,
    score: int,
    rubric: dict,
    feedback: str,
) -> int:
    """Save an evaluated answer. Returns the new row id."""
    try:
        with get_db() as conn:
            cursor = conn.execute(
                """INSERT INTO answer_history
                   (user_id, question, answer_text, answer_type, gs_paper, subject,
                    score, rubric_json, feedback, created_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (user_id, question, answer_text, answer_type, gs_paper, subject,
                 score, json.dumps(rubric), feedback, iso_now()),
            )
            return cursor.lastrowid or 0
    except Exception:
        logger.exception("save_answer failed uid=%d", user_id)
        return 0


def get_answer_history(user_id: int, limit: int = 10) -> list[sqlite3.Row]:
    try:
        with get_db() as conn:
            return conn.execute(
                "SELECT * FROM answer_history WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
                (user_id, limit),
            ).fetchall()
    except Exception:
        return []


# ── Mock tests ─────────────────────────────────────────────────────────────────

def save_mock_result(
    user_id: int,
    test_type: str,
    subject: str,
    total_q: int,
    correct: int,
    time_taken: int,
    weak_topics: list[str],
) -> None:
    accuracy = round(correct / total_q * 100, 1) if total_q > 0 else 0
    try:
        with get_db() as conn:
            conn.execute(
                """INSERT INTO mock_results
                   (user_id, test_type, subject, total_q, correct, accuracy, time_taken, weak_topics, created_at)
                   VALUES(?,?,?,?,?,?,?,?,?)""",
                (user_id, test_type, subject, total_q, correct, accuracy,
                 time_taken, json.dumps(weak_topics), iso_now()),
            )
    except Exception:
        logger.exception("save_mock_result failed uid=%d", user_id)


# ── Notes ──────────────────────────────────────────────────────────────────────

def save_note(user_id: int, day_number: int, subject: str, note_text: str) -> None:
    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO user_notes(user_id, day_number, subject, note_text, created_at) VALUES(?,?,?,?,?)",
                (user_id, day_number, subject, note_text, iso_now()),
            )
    except Exception:
        logger.exception("save_note failed uid=%d", user_id)


def get_notes(user_id: int, limit: int = 20) -> list[sqlite3.Row]:
    try:
        with get_db() as conn:
            return conn.execute(
                "SELECT * FROM user_notes WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
                (user_id, limit),
            ).fetchall()
    except Exception:
        return []


# ── Revision log ───────────────────────────────────────────────────────────────

def save_revision_entries(user_id: int, task: dict, current_day: int) -> None:
    """Create revision_log entries for a completed task based on its revision_due field."""
    due_days = task.get("revision_due", [])
    subject  = task.get("subject", "")
    subtopic = task.get("subtopic", "")
    task_id  = task.get("task_id", "")

    if not due_days:
        return

    now_date = date.today()
    try:
        with get_db() as conn:
            for due_ref in due_days:
                # due_ref like "D0008" → day 8 → offset from current_day
                try:
                    due_day_num = int(str(due_ref).replace("D", "").lstrip("0") or "0")
                    due_date_obj = now_date + timedelta(days=due_day_num - current_day)
                    conn.execute(
                        """INSERT OR IGNORE INTO revision_log
                           (user_id, task_id, subject, subtopic, due_day, due_date, completed)
                           VALUES(?,?,?,?,?,?,0)""",
                        (user_id, task_id, subject, subtopic, due_day_num, due_date_obj.isoformat()),
                    )
                except Exception:
                    pass
    except Exception:
        logger.exception("save_revision_entries failed uid=%d", user_id)


def get_due_revisions(user_id: int, current_day: int) -> list[sqlite3.Row]:
    """Get all revision entries due on or before the current day."""
    try:
        with get_db() as conn:
            return conn.execute(
                """SELECT * FROM revision_log
                   WHERE user_id=? AND due_day<=? AND completed=0
                   ORDER BY due_day""",
                (user_id, current_day),
            ).fetchall()
    except Exception:
        return []


def mark_revision_done(user_id: int, revision_id: int) -> None:
    try:
        with get_db() as conn:
            conn.execute(
                "UPDATE revision_log SET completed=1, completed_at=? WHERE id=? AND user_id=?",
                (iso_now(), revision_id, user_id),
            )
    except Exception:
        logger.exception("mark_revision_done failed uid=%d rid=%d", user_id, revision_id)


# ── Events / audit ─────────────────────────────────────────────────────────────

def log_event(user_id: int, event_type: str, detail: str = "") -> None:
    """Log a user event (non-critical — never raises)."""
    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO events(user_id, event_type, detail, created_at) VALUES(?,?,?,?)",
                (user_id, event_type, detail[:500], iso_now()),
            )
    except Exception:
        pass


def log_error(
    severity: str,
    module: str,
    function: str,
    message: str,
    traceback_str: str = "",
    user_id: int = 0,
) -> None:
    """Log an error to error_log table (non-critical — never raises)."""
    try:
        with get_db() as conn:
            conn.execute(
                """INSERT INTO error_log(severity, module, function, message, traceback, user_id, created_at)
                   VALUES(?,?,?,?,?,?,?)""",
                (severity, module, function, message[:1000], traceback_str[:2000], user_id, iso_now()),
            )
    except Exception:
        pass


def log_admin_action(admin_id: int, action: str, detail: str = "") -> None:
    """Log an admin action to audit table."""
    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO admin_audit(admin_id, action, detail, created_at) VALUES(?,?,?,?)",
                (admin_id, action, detail[:500], iso_now()),
            )
    except Exception:
        pass


# ── Admin / analytics queries ──────────────────────────────────────────────────

def total_users() -> int:
    try:
        with get_db() as conn:
            r = conn.execute("SELECT COUNT(*) FROM users").fetchone()
            return r[0] if r else 0
    except Exception:
        return 0


def active_users_count(days: int = 1) -> int:
    """Count users active in the last N days."""
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        with get_db() as conn:
            r = conn.execute(
                "SELECT COUNT(*) FROM users WHERE last_active >= ?", (cutoff,)
            ).fetchone()
            return r[0] if r else 0
    except Exception:
        return 0


def get_all_users_for_push() -> list[sqlite3.Row]:
    """Return all non-banned users with notification preferences."""
    try:
        with get_db() as conn:
            return conn.execute(
                "SELECT * FROM users WHERE setup_done=1 AND banned=0"
            ).fetchall()
    except Exception:
        return []


def get_users_paginated(offset: int = 0, limit: int = 15) -> list[sqlite3.Row]:
    try:
        with get_db() as conn:
            return conn.execute(
                "SELECT * FROM users ORDER BY last_active DESC LIMIT ? OFFSET ?",
                (limit, offset),
            ).fetchall()
    except Exception:
        return []


def search_users(query: str) -> list[sqlite3.Row]:
    """Search users by username, full_name, or user_id."""
    pattern = f"%{query}%"
    try:
        with get_db() as conn:
            return conn.execute(
                """SELECT * FROM users
                   WHERE username LIKE ? OR full_name LIKE ? OR CAST(user_id AS TEXT) LIKE ?
                   LIMIT 20""",
                (pattern, pattern, pattern),
            ).fetchall()
    except Exception:
        return []


def get_recent_errors(limit: int = 20) -> list[sqlite3.Row]:
    try:
        with get_db() as conn:
            return conn.execute(
                "SELECT * FROM error_log ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
    except Exception:
        return []


def get_db_stats() -> dict:
    """Return database statistics."""
    try:
        import os
        size = os.path.getsize(config.DB_PATH)
        with get_db() as conn:
            tables = ["users", "day_completions", "answer_history", "mock_results",
                      "events", "error_log", "revision_log"]
            counts = {}
            for t in tables:
                r = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()
                counts[t] = r[0] if r else 0
        return {"file_size_mb": round(size / 1024 / 1024, 2), "row_counts": counts}
    except Exception:
        return {}


# ── Content overrides ──────────────────────────────────────────────────────────

def get_content(key: str, default: str = "") -> str:
    try:
        with get_db() as conn:
            r = conn.execute("SELECT value FROM content_overrides WHERE key=?", (key,)).fetchone()
            return r["value"] if r else default
    except Exception:
        return default


def set_content(key: str, value: str) -> None:
    try:
        with get_db() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO content_overrides(key, value, updated_at) VALUES(?,?,?)",
                (key, value, iso_now()),
            )
    except Exception:
        logger.exception("set_content failed key=%s", key)


# ── Bookmarks ──────────────────────────────────────────────────────────────────

def add_bookmark(user_id: int, item_type: str, item_key: str, item_text: str) -> None:
    try:
        with get_db() as conn:
            conn.execute(
                """INSERT OR IGNORE INTO bookmarks(user_id, item_type, item_key, item_text, created_at)
                   VALUES(?,?,?,?,?)""",
                (user_id, item_type, item_key, item_text[:500], iso_now()),
            )
    except Exception:
        logger.exception("add_bookmark failed uid=%d", user_id)


def get_bookmarks(user_id: int) -> list[sqlite3.Row]:
    try:
        with get_db() as conn:
            return conn.execute(
                "SELECT * FROM bookmarks WHERE user_id=? ORDER BY created_at DESC",
                (user_id,),
            ).fetchall()
    except Exception:
        return []
