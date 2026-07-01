"""
handlers/onboarding.py — UPSC Master Bot Onboarding Flow
=========================================================
5-step ConversationHandler:
  0 → Level  1 → Timeline  2 → Hours  3 → Optional  4 → Weak Subjects → Done
After setup: show full pre-generated plan analysis, then activate plan.
"""
import asyncio
import json
import logging

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

import config
import keyboards as kb
from data.fallbacks import WELCOME_TEXT, SETUP_DONE_TEXT
from data.plan_reviews import get_plan_review, get_best_plan_suggestion
from media import send_photo_message, show_section
from services import plan_loader
from storage.database import (
    award_xp, grant_badge, log_event, save_plan_meta,
    update_user_field, upsert_user,
)
from utils.helpers import (
    bold, esc, get_motivation, hours_label,
    level_emoji, parse_plan_id, plan_id as make_plan_id,
    progress_bar, timeline_label,
)

logger = logging.getLogger(__name__)
HTML = "HTML"

# ── ConversationHandler states ─────────────────────────────────────────────────
STEP_LEVEL   = 0
STEP_TL      = 1
STEP_HOURS   = 2
STEP_OPT     = 3
STEP_WEAK    = 4


# ── /start entry point ─────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point for /start command."""
    user    = update.effective_user
    chat_id = update.effective_chat.id

    # Register user in DB
    upsert_user(user.id, user.username or "", user.full_name or "")
    log_event(user.id, "start")

    # Fetch from DB to check if setup already done
    from storage.database import get_user
    db_user = get_user(user.id)

    if db_user and db_user["setup_done"]:
        # User already set up — go to dashboard
        from handlers.home import show_home
        await show_home(update, context, welcome_back=True)
        return ConversationHandler.END

    # New user or reset — show welcome
    context.user_data.clear()
    await _send_welcome(update, context)
    return STEP_LEVEL


async def _send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the welcome message with level selection."""
    user = update.effective_user
    chat_id = update.effective_chat.id

    caption = (
        f"🇮🇳 <b>Welcome, {esc(user.first_name)}!</b>\n\n"
        f"{WELCOME_TEXT}\n\n"
        "<b>Step 1 of 5 — What is your current preparation level?</b>"
    )
    await send_photo_message(context, chat_id, "hero", caption, kb.kb_select_level())


# ── Step 1: Level Selection ────────────────────────────────────────────────────

async def step_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle level selection callback."""
    query = update.callback_query
    await query.answer()

    level = query.data.split(":")[1]
    if level not in config.LEVELS:
        await query.answer("❌ Invalid choice", show_alert=True)
        return STEP_LEVEL

    context.user_data["level"] = level
    emoji = level_emoji(level)

    level_desc = {
        "beginner":     "You're starting fresh or have limited previous prep. NCERTs form your base.",
        "intermediate": "You have a solid foundation. Focus shifts to depth and answer quality.",
        "advanced":     "You've already covered the syllabus. Focus is retention and exam performance.",
    }[level]

    caption = (
        f"✅ Level: <b>{emoji} {level.title()}</b>\n\n"
        f"<i>{level_desc}</i>\n\n"
        "<b>Step 2 of 5 — How long is your preparation timeline?</b>"
    )
    await show_section(query, context, "onboarding", caption, kb.kb_select_timeline())
    return STEP_TL


# ── Step 2: Timeline Selection ────────────────────────────────────────────────

async def step_timeline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle timeline selection callback."""
    query = update.callback_query
    await query.answer()

    months = int(query.data.split(":")[1])
    if months not in config.TIMELINES:
        await query.answer("❌ Invalid choice", show_alert=True)
        return STEP_TL

    context.user_data["timeline_months"] = months
    level = context.user_data.get("level", "beginner")
    emoji = level_emoji(level)
    tl_label = timeline_label(months)

    caption = (
        f"✅ Level: <b>{emoji} {level.title()}</b>\n"
        f"✅ Timeline: <b>{tl_label}</b>\n\n"
        "<b>Step 3 of 5 — How many hours can you study per day?</b>\n"
        "<i>Be honest — it's better to undercommit and overdeliver.</i>"
    )
    await show_section(query, context, "onboarding", caption, kb.kb_select_hours())
    return STEP_HOURS


# ── Step 3: Hours Selection ───────────────────────────────────────────────────

async def step_hours(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle hours selection callback."""
    query = update.callback_query
    await query.answer()

    hours = int(query.data.split(":")[1])
    if hours not in config.HOURS:
        await query.answer("❌ Invalid choice", show_alert=True)
        return STEP_HOURS

    context.user_data["hours_per_day"] = hours
    level  = context.user_data.get("level", "beginner")
    months = context.user_data.get("timeline_months", 6)
    emoji  = level_emoji(level)

    total_hours = months * hours * 30

    caption = (
        f"✅ Level: <b>{emoji} {level.title()}</b>\n"
        f"✅ Timeline: <b>{timeline_label(months)}</b>\n"
        f"✅ Hours: <b>{hours_label(hours)}</b>\n"
        f"📊 Total study hours: <b>{total_hours:,}</b>\n\n"
        "<b>Step 4 of 5 — What is your Optional Subject?</b>\n"
        "<i>Choose carefully — this is your highest-scoring opportunity in Mains.</i>"
    )
    await show_section(query, context, "onboarding", caption, kb.kb_select_optional())
    return STEP_OPT


# ── Step 4: Optional Subject ──────────────────────────────────────────────────

async def step_optional_pick(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle optional subject selection (show with tick)."""
    query = update.callback_query
    await query.answer()

    opt = query.data.split(":", 1)[1][:50]
    context.user_data["optional_subject"] = opt

    level  = context.user_data.get("level", "beginner")
    months = context.user_data.get("timeline_months", 6)
    hours  = context.user_data.get("hours_per_day", 4)
    emoji  = level_emoji(level)

    caption = (
        f"✅ Level: <b>{emoji} {level.title()}</b>\n"
        f"✅ Timeline: <b>{timeline_label(months)}</b>\n"
        f"✅ Hours: <b>{hours_label(hours)}</b>\n"
        f"✅ Optional: <b>{esc(opt)}</b>\n\n"
        "<b>Step 4 of 5 — Optional Subject</b>\n"
        f"Selected: <b>{esc(opt)}</b>\n\n"
        "Tap <b>Confirm Selection</b> or pick a different subject below."
    )
    await show_section(query, context, "onboarding", caption, kb.kb_select_optional(current=opt))
    return STEP_OPT


async def step_optional_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Confirm optional subject and move to weak subjects step."""
    query = update.callback_query
    await query.answer()

    opt    = context.user_data.get("optional_subject", "Undecided")
    level  = context.user_data.get("level", "beginner")
    months = context.user_data.get("timeline_months", 6)
    hours  = context.user_data.get("hours_per_day", 4)
    emoji  = level_emoji(level)

    caption = (
        f"✅ Level: <b>{emoji} {level.title()}</b>\n"
        f"✅ Timeline: <b>{timeline_label(months)}</b>\n"
        f"✅ Hours: <b>{hours_label(hours)}</b>\n"
        f"✅ Optional: <b>{esc(opt)}</b>\n\n"
        "<b>Step 5 of 5 — Your Weak Areas</b>\n"
        "Which subjects need the most attention?\n"
        "<i>Select all that apply (tap to toggle).</i>"
    )
    context.user_data["weak_subjects"] = []
    await show_section(query, context, "onboarding", caption, kb.kb_select_weak_subjects([]))
    return STEP_WEAK


# ── Step 5: Weak Subjects ─────────────────────────────────────────────────────

async def step_weak_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Toggle a weak subject selection."""
    query = update.callback_query
    await query.answer()

    subj = query.data.split(":", 1)[1][:40]
    weak = context.user_data.get("weak_subjects", [])

    if subj in weak:
        weak.remove(subj)
    else:
        weak.append(subj)
    context.user_data["weak_subjects"] = weak

    opt    = context.user_data.get("optional_subject", "Undecided")
    level  = context.user_data.get("level", "beginner")
    months = context.user_data.get("timeline_months", 6)
    hours  = context.user_data.get("hours_per_day", 4)
    emoji  = level_emoji(level)

    selected_str = ", ".join(weak) if weak else "None selected"
    caption = (
        f"✅ Level: <b>{emoji} {level.title()}</b>\n"
        f"✅ Timeline: <b>{timeline_label(months)}</b>\n"
        f"✅ Hours: <b>{hours_label(hours)}</b>\n"
        f"✅ Optional: <b>{esc(opt)}</b>\n\n"
        f"<b>Step 5 of 5 — Weak Areas</b>\n"
        f"Selected: <b>{esc(selected_str)}</b>\n\n"
        "Toggle subjects then tap <b>Done</b>."
    )
    await show_section(query, context, "onboarding", caption, kb.kb_select_weak_subjects(weak))
    return STEP_WEAK


async def step_weak_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Complete setup: save to DB and show plan analysis."""
    query = update.callback_query
    await query.answer("⏳ Analysing your plan…")

    user_id = update.effective_user.id
    level   = context.user_data.get("level", "beginner")
    months  = context.user_data.get("timeline_months", 6)
    hours   = context.user_data.get("hours_per_day", 4)
    opt     = context.user_data.get("optional_subject", "Undecided")
    weak    = context.user_data.get("weak_subjects", [])
    pid     = make_plan_id(level, months, hours)

    # Save to DB immediately
    update_user_field(user_id, "level",           level)
    update_user_field(user_id, "timeline_months", months)
    update_user_field(user_id, "hours_per_day",   hours)
    update_user_field(user_id, "optional_subject", opt)
    update_user_field(user_id, "weak_subjects",    json.dumps(weak))

    total_days = plan_loader.get_plan_length(pid)
    save_plan_meta(user_id, pid, level, months, hours, opt, total_days)

    # Show pre-generated analysis (INSTANT — no AI call)
    await _show_plan_analysis(query, context, pid, level, months, hours, opt, weak, total_days)
    return STEP_OPT  # Re-enter same state, waiting for confirm


async def _show_plan_analysis(
    query, context, pid, level, months, hours, opt, weak, total_days
):
    """Display the pre-generated plan analysis — completely offline/instant."""
    review = get_plan_review(pid)
    score  = review.get("score", 50.0)
    cov    = review.get("coverage_pct", 50.0)
    qlabel = review.get("quality_label", "✅ Moderate")
    tot_h  = review.get("total_hours", months * hours * 30)
    best   = review.get("best_for", "")
    outc   = review.get("realistic_outcome", "")
    note   = review.get("mentor_note", "")
    rc     = review.get("reality_check", "")
    mock_t = review.get("mock_tests", 5)
    aw_d   = review.get("answer_writing_days", 20)
    subs   = review.get("subjects_covered", 10)
    suggs  = review.get("suggestions", [])
    phases = review.get("phase_highlights", [])
    better = review.get("better_suggestion")

    # Coverage bar
    cov_bar = progress_bar(cov, 10)
    score_bar = progress_bar(score, 10)

    weak_str = ", ".join(weak) if weak else "None identified"

    phase_text = ""
    if phases:
        phase_text = "\n<b>📅 Phase Highlights:</b>\n" + "\n".join(
            f"  • {esc(p)}" for p in phases[:3]
        )

    sugg_text = ""
    if suggs:
        sugg_text = "\n<b>💡 Mentor Suggestions:</b>\n" + "\n".join(
            f"  {i+1}. {esc(s)}" for i, s in enumerate(suggs[:3])
        )

    better_text = ""
    if better:
        better_id = make_plan_id(level, better["timeline"], better["hours"])
        b_rev     = get_plan_review(better_id)
        better_text = (
            f"\n\n⬆️ <b>Better Combo Available:</b>\n"
            f"  <b>{timeline_label(better['timeline'])} × {hours_label(better['hours'])}</b>"
            f" — Score: {b_rev.get('score', 0):.0f}/100"
        )

    caption = (
        f"📊 <b>YOUR PLAN ANALYSIS</b>\n\n"
        f"<b>Plan:</b> {level_emoji(level)} {level.title()} × {months}m × {hours}h/day\n"
        f"<b>Plan ID:</b> <code>{pid}</code>\n\n"
        f"<b>Quality Rating:</b> {qlabel}\n"
        f"Score:    {score_bar} ({score:.0f}/100)\n"
        f"Coverage: {cov_bar} ({cov:.0f}%)\n\n"
        f"<b>📈 Plan Stats:</b>\n"
        f"  • Total study hours: <b>{tot_h:,}</b>\n"
        f"  • Subjects covered: <b>{subs}/12</b>\n"
        f"  • Mock tests: <b>{mock_t}</b>\n"
        f"  • Answer writing days: <b>{aw_d}</b>\n"
        f"  • Your optional: <b>{esc(opt)}</b>\n"
        f"  • Weak areas: <b>{esc(weak_str)}</b>\n\n"
        f"<b>🎯 Best For:</b> {esc(best)}\n\n"
        f"<b>📋 Realistic Outcome:</b>\n{esc(outc)}"
        f"{phase_text}"
        f"\n\n<b>⚡ Reality Check:</b>\n{esc(rc)}"
        f"\n\n<b>🧑‍🏫 Mentor Note:</b>\n{esc(note)}"
        f"{sugg_text}"
        f"{better_text}"
    )

    await show_section(
        query, context, "analysis", caption,
        kb.kb_plan_analysis(show_better=bool(better)),
    )


# ── Confirm Plan from Analysis ─────────────────────────────────────────────────

async def confirm_plan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """User confirmed plan from analysis screen — activate plan."""
    query   = update.callback_query
    user_id = update.effective_user.id

    level  = context.user_data.get("level", "beginner")
    months = context.user_data.get("timeline_months", 6)
    hours  = context.user_data.get("hours_per_day", 4)
    pid    = make_plan_id(level, months, hours)

    # Mark setup complete, start from Day 1
    update_user_field(user_id, "setup_done",   1)
    update_user_field(user_id, "current_day",  1)
    update_user_field(user_id, "xp",           0)
    update_user_field(user_id, "streak",       0)
    update_user_field(user_id, "rank_title",   "🌱 Aspirant")

    # First-time badge
    grant_badge(user_id, "first_login")
    award_xp(user_id, 100, "Setup complete")
    log_event(user_id, "setup_complete", pid)

    await query.answer("🎉 Plan activated!")

    total_days = plan_loader.get_plan_length(pid)
    motivation = get_motivation(user_id, 1)

    caption = (
        f"🎉 <b>Your Plan is Live!</b>\n\n"
        f"<b>{level_emoji(level)} {level.title()} × {months} Months × {hours}h/day</b>\n"
        f"Plan ID: <code>{pid}</code>\n"
        f"Total days: <b>{total_days}</b>\n\n"
        f"<b>You've earned:</b> +100 XP 🎊\n\n"
        f"<i>{esc(motivation)}</i>\n\n"
        f"{SETUP_DONE_TEXT}"
    )
    await show_section(query, context, "hero", caption, kb.kb_home())
    context.user_data.clear()
    return ConversationHandler.END


async def restart_onboarding(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Let user restart the onboarding flow from scratch."""
    query = update.callback_query
    await query.answer()
    context.user_data.clear()

    caption = (
        "🔄 <b>Let's start fresh!</b>\n\n"
        "<b>Step 1 of 5 — What is your current preparation level?</b>"
    )
    await show_section(query, context, "hero", caption, kb.kb_select_level())
    return STEP_LEVEL


async def show_better_suggestion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show the better plan suggestion from analysis screen."""
    query  = update.callback_query
    await query.answer()

    level  = context.user_data.get("level", "beginner")
    months = context.user_data.get("timeline_months", 6)
    hours  = context.user_data.get("hours_per_day", 4)
    pid    = make_plan_id(level, months, hours)

    review = get_plan_review(pid)
    better = review.get("better_suggestion")
    if not better:
        await query.answer("Your current plan is already optimal!", show_alert=True)
        return STEP_OPT

    better_id  = make_plan_id(level, better["timeline"], better["hours"])
    better_rev = get_plan_review(better_id)
    b_score    = better_rev.get("score", 50)
    b_cov      = better_rev.get("coverage_pct", 50)
    b_hours    = better_rev.get("total_hours", 720)

    caption = (
        f"⬆️ <b>Better Plan Available</b>\n\n"
        f"<b>Suggested:</b> {level_emoji(level)} {level.title()} × "
        f"{timeline_label(better['timeline'])} × {hours_label(better['hours'])}\n\n"
        f"Score: {progress_bar(b_score, 10)} ({b_score:.0f}/100)\n"
        f"Coverage: {progress_bar(b_cov, 10)} ({b_cov:.0f}%)\n"
        f"Total hours: <b>{b_hours:,}</b>\n\n"
        f"<b>Why better?</b>\n{esc(better_rev.get('mentor_note', ''))}\n\n"
        f"<i>Tap below to switch to this plan or stick with your original.</i>"
    )

    # Offer to switch
    from telegram import InlineKeyboardButton as Btn, InlineKeyboardMarkup as Markup
    switch_kb = Markup([
        [Btn(f"✅ Switch to {better['timeline']}m × {better['hours']}h",
             callback_data=f"ob:switch:{better['timeline']}:{better['hours']}")],
        [Btn("🔙 Keep My Original Plan", callback_data="ob:confirm")],
    ])
    await show_section(query, context, "analysis", caption, switch_kb)
    return STEP_OPT


async def switch_to_better(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """User chose to switch to the better suggested plan."""
    query  = update.callback_query
    parts  = query.data.split(":")  # ob:switch:months:hours
    months = int(parts[2])
    hours  = int(parts[3])

    context.user_data["timeline_months"] = months
    context.user_data["hours_per_day"]   = hours

    # Show updated analysis
    level = context.user_data.get("level", "beginner")
    opt   = context.user_data.get("optional_subject", "Undecided")
    weak  = context.user_data.get("weak_subjects", [])
    pid   = make_plan_id(level, months, hours)
    total = plan_loader.get_plan_length(pid)

    await query.answer("✅ Plan updated!")
    await _show_plan_analysis(query, context, pid, level, months, hours, opt, weak, total)
    return STEP_OPT


# ── Reset plan command ─────────────────────────────────────────────────────────

async def cmd_reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Allow user to reset and choose a new plan."""
    user_id = update.effective_user.id
    update_user_field(user_id, "setup_done", 0)
    context.user_data.clear()
    await _send_welcome(update, context)
    log_event(user_id, "plan_reset")
    return STEP_LEVEL


# ── Cancel handler ─────────────────────────────────────────────────────────────

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel onboarding (also handles /cancel command)."""
    if update.callback_query:
        await update.callback_query.answer("Setup cancelled.")
    context.user_data.clear()
    return ConversationHandler.END


# ── ConversationHandler builder ────────────────────────────────────────────────

def get_onboarding_handler() -> ConversationHandler:
    """Build and return the ConversationHandler for onboarding."""
    return ConversationHandler(
        entry_points=[
            CommandHandler("start", cmd_start),
            CommandHandler("reset", cmd_reset),
        ],
        states={
            STEP_LEVEL: [
                CallbackQueryHandler(step_level, pattern=r"^set_level:"),
            ],
            STEP_TL: [
                CallbackQueryHandler(step_timeline, pattern=r"^set_tl:"),
            ],
            STEP_HOURS: [
                CallbackQueryHandler(step_hours, pattern=r"^set_hrs:"),
            ],
            STEP_OPT: [
                CallbackQueryHandler(step_optional_pick,    pattern=r"^set_opt:"),
                CallbackQueryHandler(step_optional_confirm, pattern=r"^confirm_opt$"),
                CallbackQueryHandler(confirm_plan,          pattern=r"^ob:confirm$"),
                CallbackQueryHandler(restart_onboarding,    pattern=r"^ob:restart$"),
                CallbackQueryHandler(show_better_suggestion,pattern=r"^ob:better$"),
                CallbackQueryHandler(switch_to_better,      pattern=r"^ob:switch:"),
            ],
            STEP_WEAK: [
                CallbackQueryHandler(step_weak_toggle,  pattern=r"^tog_weak:"),
                CallbackQueryHandler(step_weak_confirm, pattern=r"^confirm_weak$"),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start",  cmd_start),
        ],
        allow_reentry=True,
        per_message=False,
    )
