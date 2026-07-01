"""
handlers/ethics.py — Ethics Case Study Handler
"""
import logging
import random
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes, MessageHandler, filters

import keyboards as kb
from data.fallbacks import ETHICS_CASES
from media import show_section
from services.gemini import evaluate_ethics_case
from storage.database import award_xp, log_event
from utils.helpers import esc, progress_bar

logger = logging.getLogger(__name__)
HTML = "HTML"

FRAMEWORK_TEXT = """⚖️ <b>7-Step Ethics Framework</b>

<b>Step 1 — Stakeholder Identification</b>
Who is involved? Who is affected? (direct/indirect)

<b>Step 2 — Core Ethical Dilemma</b>
What is the central conflict? (duty vs. integrity, loyalty vs. accountability, etc.)

<b>Step 3 — Values at Stake</b>
Which values are in tension? (honesty, compassion, justice, rule of law, efficiency, equity)

<b>Step 4 — Options Analysis</b>
List 3-4 possible courses of action. For each: pros, cons, and ethical weight.

<b>Step 5 — Recommended Action</b>
State clearly what you would do. Be specific.

<b>Step 6 — Justification</b>
Why is this the right choice? Reference ethical theories (Kant, Utilitarianism, Virtue Ethics).

<b>Step 7 — Safeguards</b>
What systems would prevent this dilemma from recurring? (structural, procedural reforms)

<b>Key Thinkers to Reference:</b>
• Kant — Categorical Imperative (duty-based)
• Bentham/Mill — Utilitarianism (greatest good)
• Aristotle — Virtue Ethics (character)
• Gandhi — Trusteeship, Ahimsa
• Bhagavad Gita — Nishkama Karma (selfless action)"""


async def show_ethics(query, context, user) -> None:
    caption = (
        "⚖️ <b>Ethics & GS4 Practice</b>\n\n"
        "Case studies with AI evaluation using the 7-step framework.\n\n"
        "<b>Available:</b>\n"
        "  • 📋 Get a case study scenario\n"
        "  • ✍️ Submit your ethical analysis\n"
        "  • 📖 7-Step framework reference\n"
        "  • 🧠 Key thinkers and theories\n\n"
        "<i>GS4 is scored on framework clarity + empathy + administrative practicality.</i>"
    )
    await show_section(query, context, "ethics", caption, kb.kb_ethics())


async def ethics_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query   = update.callback_query
    user_id = query.from_user.id
    action  = query.data.split(":")[1]

    match action:
        case "case":
            case_data = random.choice(ETHICS_CASES)
            context.user_data["ethics_case"] = case_data
            caption = (
                f"📋 <b>Ethics Case Study</b>\n\n"
                f"<b>{esc(case_data['title'])}</b>\n\n"
                f"{esc(case_data['scenario'])}\n\n"
                f"<b>Key themes:</b> {', '.join(case_data['keywords'])}\n\n"
                "<i>Use the 7-step framework in your analysis. "
                "Tap 'Submit Analysis' when ready.</i>"
            )
            from telegram import InlineKeyboardButton as Btn, InlineKeyboardMarkup as Markup
            case_kb = Markup([
                [Btn("✍️ Submit My Analysis",   callback_data="ethics:submit")],
                [Btn("📖 7-Step Framework",      callback_data="ethics:framework")],
                [Btn("◀ Back",                  callback_data="nav:ethics")],
            ])
            await show_section(query, context, "ethics", caption, case_kb)

        case "submit":
            case_data = context.user_data.get("ethics_case", random.choice(ETHICS_CASES))
            context.user_data["waiting_for"]  = "ethics_analysis"
            context.user_data["ethics_case"]  = case_data
            caption = (
                f"✍️ <b>Write Your Analysis</b>\n\n"
                f"<b>Case:</b> {esc(case_data['title'])}\n\n"
                "Type your ethical analysis using the 7-step framework:\n"
                "<i>Stakeholders → Dilemma → Values → Options → Action → Justification → Safeguards</i>"
            )
            await show_section(query, context, "ethics", caption, kb.kb_cancel_writing())

        case "framework":
            await show_section(query, context, "ethics", FRAMEWORK_TEXT, kb.kb_back_section("ethics"))

        case "thinkers":
            thinkers = (
                "🧠 <b>Key Ethical Thinkers for UPSC GS4</b>\n\n"
                "<b>Western:</b>\n"
                "• <b>Kant</b> — Categorical Imperative: Act only as you'd will everyone to act\n"
                "• <b>Bentham</b> — Utilitarianism: Greatest happiness of greatest number\n"
                "• <b>John Stuart Mill</b> — Rule utilitarianism; quality of happiness matters\n"
                "• <b>Aristotle</b> — Virtue Ethics: Good character leads to good actions\n"
                "• <b>Rawls</b> — Veil of ignorance: Justice as fairness\n\n"
                "<b>Indian:</b>\n"
                "• <b>Gandhi</b> — Trusteeship, Ahimsa, Satyagraha, Sarvodaya\n"
                "• <b>Bhagavad Gita</b> — Nishkama Karma: duty without attachment to results\n"
                "• <b>Kautilya</b> — Practical governance ethics (Arthashastra)\n"
                "• <b>Ambedkar</b> — Constitutional morality, social justice\n"
                "• <b>Tagore</b> — Humanism, universal brotherhood"
            )
            await show_section(query, context, "ethics", thinkers, kb.kb_back_section("ethics"))

        case "history":
            from storage.database import get_answer_history
            history = get_answer_history(user_id, 10)
            ethics_answers = [r for r in history if "Ethics" in (r["subject"] or "")]
            if not ethics_answers:
                await query.answer("No ethics answers yet!", show_alert=True)
                return
            lines = [f"{i+1}. {r['score']}/100 — {esc(str(r['question'])[:60])}" for i, r in enumerate(ethics_answers)]
            caption = "📊 <b>Ethics History</b>\n\n" + "\n".join(lines)
            await show_section(query, context, "ethics", caption, kb.kb_back_section("ethics"))

        case _:
            await query.answer()


async def ethics_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get("waiting_for") != "ethics_analysis":
        return
    user_id   = update.effective_user.id
    analysis  = update.message.text
    case_data = context.user_data.pop("ethics_case", {})
    context.user_data.pop("waiting_for", None)

    if len(analysis.split()) < 50:
        await update.message.reply_text("❌ Analysis too short. Write at least 50 words covering the 7 steps.", parse_mode=HTML)
        return

    proc   = await update.message.reply_text("⏳ <b>AI evaluating your analysis…</b>", parse_mode=HTML)
    result = await evaluate_ethics_case(case_data.get("scenario", ""), analysis)
    score  = result.get("score", 0)
    bar    = progress_bar(score, 10)

    reply = (
        f"⚖️ <b>Ethics Evaluation</b>\n\n"
        f"<b>Score: {score}/100</b> {bar}\n\n"
        f"<b>Steps Covered:</b> {esc(result.get('steps_covered',''))}\n"
        f"<b>✅ Strengths:</b> {esc(result.get('strengths',''))}\n"
        f"<b>⚠️ Gaps:</b> {esc(result.get('gaps',''))}\n\n"
        f"<b>📝 Feedback:</b>\n{esc(result.get('feedback','Keep practising!'))}"
    )
    try:
        await proc.delete()
    except Exception:
        pass
    await update.message.reply_text(reply, parse_mode=HTML, reply_markup=kb.kb_ethics())

    from storage.database import save_answer
    save_answer(user_id, case_data.get("scenario",""), analysis, "Ethics", "GS4", "Ethics", score, {}, result.get("feedback",""))
    award_xp(user_id, 25, "Ethics case evaluated")
    log_event(user_id, "ethics_submitted", f"score={score}")


def get_ethics_handlers() -> list:
    return [
        CallbackQueryHandler(ethics_callback, pattern=r"^ethics:"),
        MessageHandler(filters.TEXT & ~filters.COMMAND, ethics_text_handler),
    ]
