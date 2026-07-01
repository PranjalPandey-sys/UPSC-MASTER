"""
handlers/essay.py — Essay Writing Handler
"""
import logging
import random
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes, MessageHandler, filters

import keyboards as kb
from data.fallbacks import ESSAY_TOPICS
from media import show_section
from services.gemini import evaluate_essay, get_essay_outline
from storage.database import award_xp, get_user, log_event
from utils.helpers import esc, progress_bar

logger = logging.getLogger(__name__)
HTML  = "HTML"

ESSAY_TIPS = """📝 <b>Essay Writing Tips for UPSC</b>

<b>Structure (mandatory):</b>
1️⃣ Introduction — Hook + context + thesis (150-200 words)
2️⃣ Body Part 1 — First major theme with examples
3️⃣ Body Part 2 — Second major theme, alternate perspectives
4️⃣ Body Part 3 — Critical analysis / way forward
5️⃣ Conclusion — Synthesis, not summary (100-150 words)

<b>What examiners reward:</b>
• Original insight, not textbook reproduction
• Concrete examples (data, case studies, quotes)
• Balanced perspectives — see multiple sides
• Philosophical depth in conclusion
• Coherent flow between paragraphs

<b>Common mistakes:</b>
• Writing only one side of the argument
• Generic intro/conclusion (no memory hook)
• Ignoring abstract/philosophical interpretations
• Going off-topic in body paragraphs

<b>Word count:</b> 1,000-1,200 words (120 minutes)
<b>Practice target:</b> 1 essay per week minimum"""


async def show_essay(query, context, user) -> None:
    caption = (
        "📝 <b>Essay Practice</b>\n\n"
        "UPSC assigns 2 essays from different sections. Practice builds confidence.\n\n"
        "<b>Available:</b>\n"
        "  • 💡 Get a topic with AI outline\n"
        "  • ✍️ Submit essay for AI evaluation (scored out of 125)\n"
        "  • 📊 View your essay history\n"
        "  • 📖 Essay writing tips\n\n"
        "<i>Tip: Write at least one essay per week. Consistency > intensity.</i>"
    )
    await show_section(query, context, "essay", caption, kb.kb_essay())


async def essay_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query   = update.callback_query
    user_id = query.from_user.id
    action  = query.data.split(":")[1]

    match action:
        case "topic":
            topic = random.choice(ESSAY_TOPICS)
            await query.answer("⏳ Getting outline…")
            outline = await get_essay_outline(topic)
            caption = (
                f"📝 <b>Essay Topic</b>\n\n"
                f"<b>❝ {esc(topic)} ❞</b>\n\n"
                f"<b>📋 Suggested Outline:</b>\n{esc(outline)}\n\n"
                "<i>Take 5 minutes to plan before writing. Planning = better structure.</i>"
            )
            context.user_data["essay_topic"] = topic
            from telegram import InlineKeyboardButton as Btn, InlineKeyboardMarkup as Markup
            essay_kb = Markup([
                [Btn("✍️ Submit Essay on This Topic", callback_data="essay:submit")],
                [Btn("🔀 Get New Topic", callback_data="essay:topic")],
                [Btn("◀ Back",           callback_data="nav:essay")],
            ])
            await show_section(query, context, "essay", caption, essay_kb)

        case "outline":
            topic = context.user_data.get("essay_topic", random.choice(ESSAY_TOPICS))
            await query.answer("⏳ Generating outline…")
            outline = await get_essay_outline(topic)
            caption = f"📋 <b>Essay Outline</b>\n\n<b>{esc(topic)}</b>\n\n{esc(outline)}"
            await show_section(query, context, "essay", caption, kb.kb_back_section("essay"))

        case "submit":
            topic = context.user_data.get("essay_topic", random.choice(ESSAY_TOPICS))
            context.user_data["waiting_for"] = "essay_text"
            context.user_data["essay_topic"] = topic
            caption = (
                f"✍️ <b>Write Your Essay</b>\n\n"
                f"<b>Topic:</b> <i>{esc(topic)}</i>\n\n"
                "Type your complete essay below.\n"
                "<i>Aim for 800-1,200 words. AI scores on 125-point scale.</i>"
            )
            await show_section(query, context, "essay", caption, kb.kb_cancel_writing())

        case "tips":
            await show_section(query, context, "essay", ESSAY_TIPS, kb.kb_back_section("essay"))

        case "history":
            from storage.database import get_answer_history
            history = get_answer_history(user_id, 10)
            essays  = [r for r in history if r["answer_type"] == "Essay"]
            if not essays:
                await query.answer("No essays submitted yet!", show_alert=True)
                return
            lines = [f"{i+1}. {r['score']}/125 — {esc(r['question'][:60])}" for i, r in enumerate(essays)]
            caption = "📊 <b>Essay History</b>\n\n" + "\n".join(lines)
            await show_section(query, context, "essay", caption, kb.kb_back_section("essay"))

        case _:
            await query.answer()


async def essay_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get("waiting_for") != "essay_text":
        return
    user_id   = update.effective_user.id
    essay_text= update.message.text
    topic     = context.user_data.pop("essay_topic", "General topic")
    context.user_data.pop("waiting_for", None)

    if len(essay_text.split()) < 100:
        await update.message.reply_text("❌ Essay too short. Write at least 100 words.", parse_mode=HTML)
        return

    proc = await update.message.reply_text("⏳ <b>AI is evaluating your essay…</b>", parse_mode=HTML)
    result  = await evaluate_essay(topic, essay_text)
    score   = result.get("score", 0)
    feedback= result.get("feedback", "Keep practising!")
    best_line= result.get("best_line", "")
    bar     = progress_bar(score / 125 * 100, 10)

    reply = (
        f"📝 <b>Essay Evaluation</b>\n\n"
        f"<b>Topic:</b> <i>{esc(topic)}</i>\n\n"
        f"<b>Score: {score}/125</b> {bar}\n\n"
        f"<b>📝 Feedback:</b>\n{esc(feedback)}"
        f"{f'{chr(10)}{chr(10)}<b>⭐ Best Line:</b> <i>{esc(best_line)}</i>' if best_line else ''}"
    )
    try:
        await proc.delete()
    except Exception:
        pass
    await update.message.reply_text(reply, parse_mode=HTML, reply_markup=kb.kb_essay_after())

    from storage.database import save_answer
    save_answer(user_id, topic, essay_text, "Essay", "Essay", "Essay", score, {}, feedback)
    award_xp(user_id, 30, "Essay submitted")
    log_event(user_id, "essay_submitted", f"score={score}")


def get_essay_handlers() -> list:
    return [
        CallbackQueryHandler(essay_callback, pattern=r"^essay:"),
        MessageHandler(filters.TEXT & ~filters.COMMAND, essay_text_handler),
    ]
