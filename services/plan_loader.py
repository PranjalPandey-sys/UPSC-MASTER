"""
services/plan_loader.py — UPSC Master Bot Plan Loader
=======================================================
FIX FOR BUG 1: All file I/O wrapped in asyncio.to_thread().
Pre-warms all 48 plan files at startup via asyncio.gather().
Zero blocking of the event loop. Plans cached in memory.

Each plan file is ~230KB. 48 files = ~11MB total.
All loaded concurrently at startup: ~1-2s total load time.
"""
import asyncio
import json
import logging
import pathlib
from functools import lru_cache

import config

logger = logging.getLogger(__name__)

# ── In-memory plan cache ───────────────────────────────────────────────────────
# Structure: { "beginner_12months_6hours": { ...full plan dict... } }
_PLAN_CACHE: dict[str, dict] = {}

# ── Analysis cache ─────────────────────────────────────────────────────────────
_METADATA: dict[str, dict] = {}
_RECOMMENDATIONS: dict = {}


# ── File loading (async) ───────────────────────────────────────────────────────

def _load_json_sync(path: pathlib.Path) -> dict | None:
    """Synchronous JSON load — always called via asyncio.to_thread()."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Plan file not found: %s", path)
        return None
    except json.JSONDecodeError as exc:
        logger.error("JSON parse error in %s: %s", path, exc)
        return None


async def _load_plan_file(plan_id: str) -> tuple[str, dict | None]:
    """Load a single plan file asynchronously."""
    path = config.PLANS_DIR / f"{plan_id}.json"
    data = await asyncio.to_thread(_load_json_sync, path)
    return plan_id, data


async def pre_warm_all_plans() -> int:
    """
    Pre-warm all 48 plan files concurrently at startup.
    Returns the count of successfully loaded plans.
    Uses asyncio.gather() — all files load in parallel.
    """
    global _PLAN_CACHE

    plan_ids = [
        f"{level}_{months}months_{hours}hours"
        for level   in config.LEVELS
        for months  in config.TIMELINES
        for hours   in config.HOURS
    ]

    logger.info("Pre-warming %d plan files...", len(plan_ids))
    results = await asyncio.gather(*[_load_plan_file(pid) for pid in plan_ids])

    loaded = 0
    for plan_id, data in results:
        if data:
            _PLAN_CACHE[plan_id] = data
            loaded += 1
        else:
            logger.warning("Failed to load plan: %s", plan_id)

    logger.info("✅ Plans pre-warmed | %d/%d loaded", loaded, len(plan_ids))
    return loaded


async def load_analysis_files() -> None:
    """Load plan_metadata.json and recommendations.json into memory."""
    global _METADATA, _RECOMMENDATIONS

    meta_path = config.ANALYSIS_DIR / "plan_metadata.json"
    rec_path  = config.ANALYSIS_DIR / "recommendations.json"

    meta = await asyncio.to_thread(_load_json_sync, meta_path)
    recs = await asyncio.to_thread(_load_json_sync, rec_path)

    if meta:
        _METADATA = meta
        logger.info("✅ Plan metadata loaded | %d entries", len(meta))
    else:
        logger.warning("plan_metadata.json not loaded — using fallback")

    if recs:
        _RECOMMENDATIONS = recs
        logger.info("✅ Recommendations loaded")


# ── Plan access functions ──────────────────────────────────────────────────────

def get_plan(plan_id: str) -> dict | None:
    """Get a full plan dict by ID. Returns None if not in cache."""
    return _PLAN_CACHE.get(plan_id)


def get_day_task(plan_id: str, day_number: int) -> dict | None:
    """
    Get a specific day's task from a plan.
    day_number is 1-indexed.
    Returns the task dict or None.
    """
    plan = _PLAN_CACHE.get(plan_id)
    if not plan:
        logger.warning("Plan not in cache: %s", plan_id)
        return None

    daily_plan = plan.get("daily_plan", [])
    if not daily_plan:
        return None

    # Day tasks are 1-indexed; array is 0-indexed
    idx = day_number - 1
    if 0 <= idx < len(daily_plan):
        return daily_plan[idx]

    # Safety: if day_number exceeds plan length, return last day
    if day_number > len(daily_plan):
        logger.debug("day %d beyond plan length %d, returning last", day_number, len(daily_plan))
        return daily_plan[-1]

    return None


def get_plan_length(plan_id: str) -> int:
    """Return total number of days in a plan."""
    plan = _PLAN_CACHE.get(plan_id)
    if not plan:
        return 0
    return len(plan.get("daily_plan", []))


def get_plan_meta(plan_id: str) -> dict:
    """Return plan_meta section from a plan."""
    plan = _PLAN_CACHE.get(plan_id)
    if not plan:
        return {}
    return plan.get("plan_meta", {})


def get_plan_metadata(plan_id: str) -> dict:
    """Return analysis metadata for a plan from plan_metadata.json."""
    return _METADATA.get(plan_id, {})


def get_all_metadata() -> dict:
    """Return full plan metadata dict."""
    return _METADATA


def get_recommendations() -> dict:
    """Return full recommendations dict."""
    return _RECOMMENDATIONS


def get_revision_due_days(plan_id: str, day_number: int) -> list[int]:
    """
    Return list of future day numbers when today's task should be revised.
    Converts "D0008" format to integer day numbers.
    """
    task = get_day_task(plan_id, day_number)
    if not task:
        return []
    raw = task.get("revision_due", [])
    days = []
    for ref in raw:
        try:
            days.append(int(str(ref).replace("D", "").lstrip("0") or "0"))
        except Exception:
            pass
    return days


def get_weekly_summary(plan_id: str, week: int) -> dict | None:
    """
    Get the weekly summary for a given week number.
    Real schema: weekly_summaries is a DICT keyed "Week_1", "Week_2", etc.
    (not a list — confirmed against actual plan JSON structure).
    """
    plan = _PLAN_CACHE.get(plan_id)
    if not plan:
        return None
    summaries = plan.get("weekly_summaries", {})
    if isinstance(summaries, dict):
        return summaries.get(f"Week_{week}")
    # Defensive fallback in case format ever changes back to a list
    if isinstance(summaries, list):
        for s in summaries:
            if s.get("week") == week:
                return s
    return None


def get_phase_for_day(plan_id: str, day_number: int) -> str:
    """Get the phase name for a given day."""
    task = get_day_task(plan_id, day_number)
    return task.get("phase", "Foundation") if task else "Foundation"


def search_tasks_by_subject(plan_id: str, subject: str) -> list[dict]:
    """Find all tasks in a plan for a given subject."""
    plan = _PLAN_CACHE.get(plan_id)
    if not plan:
        return []
    daily = plan.get("daily_plan", [])
    return [t for t in daily if t.get("subject", "").lower() == subject.lower()]


def get_current_affairs_engine(plan_id: str) -> dict:
    """Return the current affairs engine config from a plan."""
    plan = _PLAN_CACHE.get(plan_id)
    if not plan:
        return {}
    return plan.get("current_affairs_engine", {})


def get_essay_framework(plan_id: str) -> dict:
    """Return essay framework from a plan."""
    plan = _PLAN_CACHE.get(plan_id)
    if not plan:
        return {}
    return plan.get("essay_framework", {})


def get_ethics_framework(plan_id: str) -> dict:
    """Return ethics framework from a plan."""
    plan = _PLAN_CACHE.get(plan_id)
    if not plan:
        return {}
    return plan.get("ethics_framework", {})


def get_optional_strategy(plan_id: str) -> dict:
    """Return optional subject strategy from a plan."""
    plan = _PLAN_CACHE.get(plan_id)
    if not plan:
        return {}
    return plan.get("optional_subject_strategy", {})


def is_loaded() -> bool:
    """Return True if plans are loaded in cache."""
    return len(_PLAN_CACHE) > 0


def cache_size() -> int:
    """Return number of plans currently in cache."""
    return len(_PLAN_CACHE)


def get_better_suggestion(plan_id: str) -> dict | None:
    """
    Check if a better plan is suggested for this combo.
    Returns suggestion dict or None if current plan is optimal.
    """
    meta = _METADATA.get(plan_id, {})
    return meta.get("better_suggestion")
