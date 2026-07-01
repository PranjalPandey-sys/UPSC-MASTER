"""
handlers/home.py — UPSC Master Bot Home / Navigation
======================================================
Main dashboard + central nav:home callback router.
Every section nav callback is handled here and dispatched
to the appropriate handler module.
"""
import json
import logging
from datetime import date, timedelta

from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

import keyboards as kb
from data.fallbacks import HELP_TEXT
from media import show_section
from storage.database import (
    award_xp, get_user, log_event, update_last_active, update_user_field,
)
from utils.helpers import (
    bold, days_remaining_label, esc, get_motivation, get_rank,
    level_emoji, parse_plan_id, plan_id as make_plan_id,
    progress_bar, streak_emoji, xp_to_next_rank,
)

logger = logging.getLogger(__name__)
HTML  = "HTML"


# ── Show home dashboard ────────────────────────────────────────────────────────

async def show_home(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    welcome_back: bool = False,
) -> None:
    """
    Render the main home dashboard.
    Called from /start (existing user) and nav:home callback.
    """
    if update.callback_query:
        query   = update.callback_query
        user_id = query.from_user.id
    else:
        query   = None
        user_id = update.effective_user.id

    user = get_user(user_id)
    if not user or not user["setup_done"]:
        # Not set up — redirect to onboarding via /start
        if query:
            await query.answer("Please complete setup first.")
        from handlers.onboarding import cmd_start
        await cmd_start(update, context)
        return

    # Update last active (fire and forget)
    update_last_active(user_id)
    log_event(user_id, "home_view")

    # Pull stats
    level   = user["level"] or "beginner"
    months  = user["timeline_months"] or 6
    hours   = user["hours_per_day"]   or 4
    day_num = user["current_day"]      or 1
    streak  = user["streak"]           or 0
    xp      = user["xp"]               or 0
    rank    = get_rank(xp)
    best    = user["best_streak"]      or 0
    opt     = user["optional_subject"] or "—"

    pid       = make_plan_id(level, months, hours)
    _, needed, to_go = xp_to_next_rank(xp)
    next_rank_label  = _[0] if isinstance(_, tuple) else _

    from services.plan_loader import get_plan_length, get_phase_for_day
    total_days = get_plan_length(pid)
    phase      = get_phase_for_day(pid, day_num) if total_days > 0 else "Foundation"
    pct_done   = round(day_num / total_days * 100, 1) if total_days > 0 else 0
    days_left  = max(0, total_days - day_num)

    prog_bar = progress_bar(pct_done, 10)
    xp_bar   = progress_bar(
        min(100, (xp / needed * 100) if needed > 0 else 100), 8
    ) if to_go > 0 else "███████████ MAX"
    s_emoji  = streak_emoji(streak)

    greet = "👋 Welcome back" if welcome_back else "🏠 Dashboard"
    motivation = get_motivation(user_id, day_num)

    caption = (
        f"<b>{greet}, {esc(update.effective_user.first_name)}!</b>\n\n"
        f"<b>{level_emoji(level)} Plan:</b> {level.title()} × {months}m × {int(hours)}h/day\n"
        f"<b>📅 Today:</b> Day {day_num} of {total_days} — {phase} Phase\n"
        f"<b>📈 Progress:</b> {prog_bar} ({pct_done:.0f}%)\n"
        f"<b>⏳ Remaining:</b> {days_remaining_label(days_left)}\n\n"
        f"<b>{s_emoji} Streak:</b> {streak} day{'s' if streak != 1 else ''}"
        f" (Best: {best})\n"
        f"<b>⚡ XP:</b> {xp:,} — {rank}\n"
        f"    {xp_bar}"
        f"{f' (+{to_go:,} to {next_rank_label})' if to_go > 0 else ''}\n"
        f"<b>📚 Optional:</b> {esc(opt)}\n\n"
        f"<i>{esc(motivation)}</i>\n\n"
        "Choose a section below 👇"
    )

    if query:
        await show_section(query, context, "home", caption, kb.kb_home(streak, day_num))
    else:
        from media import send_photo_message
        await send_photo_message(
            context,
            update.effective_chat.id,
            "home",
            caption,
            kb.kb_home(streak, day_num),
        )


# ── Navigation callback dispatcher ─────────────────────────────────────────────

async def nav_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Central dispatcher for all nav:SECTION callbacks.
    Routes to the correct handler module.
    """
    query  = update.callback_query
    user_id = query.from_user.id

    # Check setup
    user = get_user(user_id)
    if not user or not user["setup_done"]:
        await query.answer("Please /start first to set up your plan.")
        return

    # Check banned
    if user.get("banned"):
        await query.answer("⛔ Your account has been suspended.", show_alert=True)
        return

    update_last_active(user_id)

    section = query.data.split(":")[1]
    log_event(user_id, f"nav_{section}")

    # Route to correct handler
    match section:
        case "home":
            await show_home(update, context)

        case "tasks":
            from handlers.tasks import show_tasks
            await show_tasks(query, context, user)

        case "revision":
            from handlers.revision import show_revision
            await show_revision(query, context, user)

        case "answer_writing":
            from handlers.answer_writing import show_answer_writing
            await show_answer_writing(query, context, user)

        case "mock":
            from handlers.mock_test import show_mock_menu
            await show_mock_menu(query, context, user)

        case "current_affairs":
            from handlers.current_affairs import show_ca
            await show_ca(query, context, user)

        case "essay":
            from handlers.essay import show_essay
            await show_essay(query, context, user)

        case "ethics":
            from handlers.ethics import show_ethics
            await show_ethics(query, context, user)

        case "optional":
            from handlers.optional import show_optional
            await show_optional(query, context, user)

        case "progress":
            from handlers.progress import show_progress
            await show_progress(query, context, user)

        case "streak":
            from handlers.streak import show_streak
            await show_streak(query, context, user)

        case "ai_planner":
            from handlers.doubt import show_ai_planner
            await show_ai_planner(query, context, user)

        case "settings":
            from handlers.settings import show_settings
            await show_settings(query, context, user)

        case "help":
            await show_help(query, context)

        case "admin":
            from handlers.admin import show_admin
            await show_admin(query, context, user_id)

        case "timer":
            from handlers.timer import show_timer
            await show_timer(query, context)

        case _:
            await query.answer(f"Section '{section}' coming soon!", show_alert=False)
            logger.warning("Unknown nav section: %s uid=%d", section, user_id)


async def show_help(query, context) -> None:
    """Show the help / guide screen."""
    await show_section(query, context, "help", HELP_TEXT, kb.kb_back_home())


# ── CallbackQueryHandler for global nav ───────────────────────────────────────

def get_nav_handler() -> CallbackQueryHandler:
    return CallbackQueryHandler(nav_callback, pattern=r"^nav:")
