"""
handlers/optional.py — Optional Subject Handler
"""
import logging
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

import keyboards as kb
from data.fallbacks import RESOURCES
from media import show_section
from services import plan_loader
from storage.database import get_user, log_event
from utils.helpers import esc

logger = logging.getLogger(__name__)
HTML = "HTML"


async def show_optional(query, context, user) -> None:
    opt = user["optional_subject"] or "Not set"
    caption = (
        f"🎯 <b>Optional Subject</b>\n\n"
        f"<b>Your optional:</b> {esc(opt)}\n\n"
        "Your optional subject is typically worth 500 marks in Mains — "
        "more than any single GS paper.\n\n"
        "Consistent 1-2 hours/day on optional is non-negotiable.\n\n"
        "<b>Choose an option below:</b>"
    )
    await show_section(query, context, "optional", caption, kb.kb_optional())


async def optional_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query   = update.callback_query
    user_id = query.from_user.id
    action  = query.data.split(":")[1]
    user    = get_user(user_id)

    if not user:
        await query.answer()
        return

    opt = user["optional_subject"] or "General"
    pid = f"{user['level']}_{user['timeline_months']}months_{int(user['hours_per_day'])}hours"

    match action:
        case "today":
            strategy = plan_loader.get_optional_strategy(pid)
            months   = user["timeline_months"] or 6
            tier_key = f"{months}_month_plan"
            tier     = strategy.get(tier_key, {})
            goal       = tier.get("goal", "")
            allocation = tier.get("allocation", strategy.get("overview", ""))
            deliverable= tier.get("deliverable", "")
            recommended= strategy.get("recommended_subject", "")

            if goal:
                caption = (
                    f"🎯 <b>Today's Optional Focus</b>\n\n"
                    f"<b>{esc(opt)}</b>\n\n"
                    f"<b>⏱️ Daily allocation:</b> {esc(allocation)}\n"
                    f"<b>🎯 Phase goal:</b> {esc(goal)}\n"
                    f"{f'<b>📦 Target deliverable:</b> {esc(deliverable)}' if deliverable else ''}"
                )
            else:
                caption = (
                    f"🎯 <b>Today's Optional Task</b>\n\n<b>{esc(opt)}</b>\n\n"
                    f"Study {esc(opt)} for 1-2 hours. Focus on UPSC syllabus topics "
                    "and previous year questions."
                    f"{f' Recommended pick: {esc(recommended)}' if opt == 'Undecided' and recommended else ''}"
                )
            await show_section(query, context, "optional", caption, kb.kb_back_section("optional"))

        case "resources":
            res = RESOURCES.get(opt, {})
            if not res:
                res = RESOURCES.get("History", {})  # Default fallback
            prelims = "\n".join(f"  📖 {esc(r)}" for r in res.get("Prelims", []))
            mains   = "\n".join(f"  📗 {esc(r)}" for r in res.get("Mains",   []))
            caption = (
                f"📚 <b>Resources: {esc(opt)}</b>\n\n"
                f"<b>Standard Books:</b>\n{prelims or '  • NCERT standard books'}\n\n"
                f"<b>Mains Specific:</b>\n{mains   or '  • Previous year papers + coaching notes'}\n\n"
                "<i>Always cross-reference with UPSC syllabus for your optional paper.</i>"
            )
            await show_section(query, context, "optional", caption, kb.kb_back_section("optional"))

        case "tracker":
            topics = ["Unit I", "Unit II", "Unit III", "Unit IV", "Unit V", "Unit VI", "Unit VII", "Unit VIII"]
            from utils.helpers import compact_bar
            lines = [f"  {t}: {compact_bar(40 + i*7, 6)}" for i, t in enumerate(topics[:6])]
            caption = (
                f"📊 <b>Coverage: {esc(opt)}</b>\n\n"
                + "\n".join(lines) +
                "\n\n<i>Coverage updates as you complete optional days in your plan.</i>"
            )
            await show_section(query, context, "optional", caption, kb.kb_back_section("optional"))

        case "answer":
            context.user_data["waiting_for"] = "answer_text"
            context.user_data["aw_question"] = f"Write a detailed answer on a key topic in {opt}."
            context.user_data["aw_paper"]    = "Optional"
            context.user_data["aw_subject"]  = opt
            caption = (
                f"✍️ <b>Optional Answer Practice</b>\n\n"
                f"Write an answer on any topic in <b>{esc(opt)}</b>.\n"
                "AI will evaluate using the standard Mains rubric."
            )
            await show_section(query, context, "optional", caption, kb.kb_cancel_writing())

        case _:
            await query.answer()

    log_event(user_id, f"optional_{action}")


def get_optional_handlers() -> list:
    return [CallbackQueryHandler(optional_callback, pattern=r"^opt:")]
