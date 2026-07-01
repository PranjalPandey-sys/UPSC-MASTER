"""
handlers/doubt.py — AI Planner / Doubt Solver
"""
import logging
from datetime import datetime, timezone, timedelta
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes, MessageHandler, filters

import keyboards as kb
from media import show_section
from services.gemini import generate_flashcard_questions, get_ca_summary, solve_doubt
from storage.database import award_xp, get_user, log_event
from utils.helpers import esc

logger = logging.getLogger(__name__)
HTML = "HTML"

COOLDOWN_SECONDS = 20
_last_doubt: dict[int, datetime] = {}


async def show_ai_planner(query, context, user) -> None:
    caption = (
        "🤖 <b>AI Planner</b>\n\n"
        "Your UPSC AI mentor — ask any Civil Services question.\n\n"
        "<b>Options:</b>\n"
        "  ❓ Ask any UPSC doubt\n"
        "  📋 Get flashcard-style revision questions\n"
        "  📰 AI current affairs summary\n"
        "  📊 Plan analysis overview\n\n"
        "<i>20-second cooldown between doubt questions. AI answers in ~5 seconds.</i>"
    )
    await show_section(query, context, "ai_planner", caption, kb.kb_ai_planner())


async def ai_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query   = update.callback_query
    user_id = query.from_user.id
    action  = query.data.split(":")[1]
    user    = get_user(user_id)
    if not user:
        await query.answer()
        return

    match action:
        case "doubt":
            context.user_data["waiting_for"] = "doubt_question"
            caption = (
                "❓ <b>Ask a Doubt</b>\n\n"
                "Type your UPSC question below.\n\n"
                "<i>Examples:\n"
                "• What is Federalism in India?\n"
                "• Explain the Goods and Services Tax structure\n"
                "• What is the difference between Fundamental Rights and DPSPs?\n"
                "• How does La Niña affect India's monsoon?</i>"
            )
            await show_section(query, context, "ai_planner", caption, kb.kb_cancel_doubt())

        case "flashcard":
            user_obj = get_user(user_id)
            subject  = (user_obj["level"] or "beginner").title()
            await query.answer("⏳ Generating flashcard questions…")
            questions = await generate_flashcard_questions(subject, "Key concepts")
            lines  = [f"{i+1}. {esc(q)}" for i, q in enumerate(questions)]
            caption = (
                f"📋 <b>Flashcard Questions</b>\n\n"
                f"<b>Subject:</b> {subject}\n\n" +
                "\n".join(lines) +
                "\n\n<i>Answer these from memory before looking up. "
                "Active recall builds retention 3-4× faster than re-reading.</i>"
            )
            await show_section(query, context, "ai_planner", caption, kb.kb_back_section("ai_planner"))

        case "ca":
            context.user_data["waiting_for"] = "ca_topic"
            caption = (
                "📰 <b>Current Affairs Summary</b>\n\n"
                "Type a topic or keyword for an AI-powered UPSC-relevant summary.\n\n"
                "<i>Examples: 'RBI rate decision', 'BRICS summit 2024', "
                "'India semiconductor policy', 'Monsoon deficit 2024'</i>"
            )
            await show_section(query, context, "ai_planner", caption, kb.kb_cancel_doubt())

        case "analysis":
            from data.plan_reviews import get_plan_review
            pid    = f"{user['level']}_{user['timeline_months']}months_{int(user['hours_per_day'])}hours"
            review = get_plan_review(pid)
            score  = review.get("score", 50)
            cov    = review.get("coverage_pct", 50)
            label  = review.get("quality_label", "✅ Moderate")
            from utils.helpers import progress_bar
            caption = (
                f"📊 <b>Your Plan Analysis</b>\n\n"
                f"<b>Plan:</b> <code>{pid}</code>\n"
                f"<b>Quality:</b> {label}\n"
                f"Score: {progress_bar(score,10)} ({score:.0f}/100)\n"
                f"Coverage: {progress_bar(cov,10)} ({cov:.0f}%)\n\n"
                f"<b>Mentor Note:</b>\n{esc(review.get('mentor_note',''))}"
            )
            await show_section(query, context, "ai_planner", caption, kb.kb_back_section("ai_planner"))

        case _:
            await query.answer()


async def doubt_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    waiting = context.user_data.get("waiting_for")
    if waiting not in ("doubt_question", "ca_topic"):
        return

    user_id = update.effective_user.id
    text    = update.message.text.strip()

    # Cooldown check
    now     = datetime.now(timezone.utc)
    last    = _last_doubt.get(user_id)
    if last and (now - last).total_seconds() < COOLDOWN_SECONDS:
        remaining = int(COOLDOWN_SECONDS - (now - last).total_seconds())
        await update.message.reply_text(
            f"⏳ Please wait {remaining}s before asking another question.", parse_mode=HTML
        )
        return

    _last_doubt[user_id] = now
    mode = context.user_data.pop("waiting_for", "doubt_question")

    proc = await update.message.reply_text("🤖 <b>AI is thinking…</b>", parse_mode=HTML)

    if mode == "ca_topic":
        result = await get_ca_summary(text)
        reply  = f"📰 <b>CA: {esc(text)}</b>\n\n{esc(result)}"
        log_event(user_id, "ai_ca", text[:50])
    else:
        user   = get_user(user_id)
        level  = user["level"] if user else "intermediate"
        result = await solve_doubt(text, level=level)
        reply  = result
        award_xp(user_id, 5, "Doubt asked")
        log_event(user_id, "doubt_asked", text[:50])

    try:
        await proc.delete()
    except Exception:
        pass
    await update.message.reply_text(reply, parse_mode=HTML, reply_markup=kb.kb_ai_planner())


def get_doubt_handlers() -> list:
    return [
        CallbackQueryHandler(ai_callback, pattern=r"^ai:"),
        MessageHandler(filters.TEXT & ~filters.COMMAND, doubt_text_handler),
    ]
