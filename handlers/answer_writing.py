"""
handlers/answer_writing.py — Mains Answer Writing Practice
"""
import base64
import logging

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler, ContextTypes, MessageHandler, filters,
)

import keyboards as kb
from media import show_section
from services.gemini import evaluate_answer, evaluate_ethics_case, extract_handwritten
from storage.database import (
    award_xp, get_answer_history, get_user, log_event, save_answer,
)
from utils.helpers import esc, progress_bar

logger = logging.getLogger(__name__)
HTML = "HTML"

# Sample questions per GS paper
GS_QUESTIONS = {
    "gs1": [
        ("The partition of India in 1947 left deep scars. Analyse the social and psychological impact on displaced communities.", "History"),
        ("Discuss the role of women in India's freedom struggle with examples.", "History"),
        ("What are the major factors responsible for seasonal and annual variation of rainfall in India?", "Geography"),
        ("Analyse the causes and consequences of urbanisation in India.", "Indian Society"),
    ],
    "gs2": [
        ("Parliamentary committees play a vital role in Indian democracy. Examine with examples.", "Polity"),
        ("Analyse India's neighbourhood-first policy and its challenges.", "IR"),
        ("Right to Health is implicit in Article 21. Discuss the judicial interventions.", "Governance"),
        ("What are the constitutional safeguards for minorities in India? Are they adequate?", "Polity"),
    ],
    "gs3": [
        ("Discuss the role of the agricultural sector in doubling farmers' income by 2022 — targets and achievements.", "Economy"),
        ("What are the challenges and opportunities in India's semiconductor manufacturing sector?", "S&T"),
        ("Analyse the impact of climate change on India's monsoon patterns and agriculture.", "Environment"),
        ("Cybersecurity is the biggest threat to national security today. Discuss.", "Security"),
    ],
    "gs4": [
        ("A civil servant faces a situation where following the letter of the law harms the spirit of justice. How should they act?", "Ethics"),
        ("What are the ethical dimensions of using AI in governance and policy-making?", "Ethics"),
        ("Discuss the role of conscience in public service with reference to the Bhagavad Gita's concept of Nishkama Karma.", "Ethics"),
        ("Evaluate: 'Honesty may be the best policy, but it is not always the most convenient policy.'", "Ethics"),
    ],
}


async def show_answer_writing(query, context: ContextTypes.DEFAULT_TYPE, user) -> None:
    """Show answer writing section."""
    user_id = user["user_id"]
    history = get_answer_history(user_id, 5)
    count   = len(history)

    avg_score = 0
    if history:
        scores = [r["score"] for r in history if r["score"]]
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0

    recent_str = ""
    if history:
        recent_str = "\n<b>Recent answers:</b>\n" + "\n".join(
            f"  • {esc(r['gs_paper'])} — {r['score']}/100"
            for r in history[:3]
        )

    caption = (
        "✍️ <b>Answer Writing Practice</b>\n\n"
        "Master the art of UPSC Mains answer writing with AI evaluation.\n\n"
        f"<b>📊 Your Stats:</b>\n"
        f"  • Answers written: <b>{count}</b>\n"
        f"  • Average score: <b>{avg_score}/100</b>\n"
        f"{recent_str}\n\n"
        "<b>Choose a paper below to get a question</b> 👇\n"
        "<i>Tip: Type your answer when prompted. AI gives score out of 100.</i>"
    )
    await show_section(query, context, "answer_writing", caption, kb.kb_answer_writing())


async def aw_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle aw: callbacks."""
    query   = update.callback_query
    user_id = query.from_user.id
    data    = query.data
    parts   = data.split(":")
    action  = parts[1]

    user = get_user(user_id)
    if not user:
        await query.answer()
        return

    match action:
        case "gs1" | "gs2" | "gs3" | "gs4":
            import random
            questions = GS_QUESTIONS.get(action, GS_QUESTIONS["gs1"])
            q_text, subject = random.choice(questions)
            gs_map = {"gs1": "GS Paper I", "gs2": "GS Paper II", "gs3": "GS Paper III", "gs4": "GS Paper IV"}
            gs_paper = gs_map[action]

            context.user_data["aw_question"]  = q_text
            context.user_data["aw_paper"]     = gs_paper
            context.user_data["aw_subject"]   = subject
            context.user_data["waiting_for"]  = "answer_text"

            caption = (
                f"✍️ <b>{gs_paper} Question</b>\n"
                f"<b>Subject:</b> {esc(subject)}\n\n"
                f"❓ <b>{esc(q_text)}</b>\n\n"
                "📝 Type your answer below.\n"
                "<i>Suggested: 150-250 words for 10-mark, 200-300 for 15-mark questions.\n"
                "Or send a photo of your handwritten answer.</i>"
            )
            await show_section(query, context, "answer_writing", caption, kb.kb_cancel_writing())

        case "history":
            history = get_answer_history(user_id, 10)
            if not history:
                await query.answer("No answers written yet!", show_alert=True)
                return
            lines = [
                f"{i+1}. {esc(r['gs_paper'])} — {r['score']}/100 — {r['subject'][:20]}"
                for i, r in enumerate(history)
            ]
            caption = (
                "📊 <b>Answer History</b>\n\n" +
                "\n".join(lines)
            )
            await show_section(query, context, "answer_writing", caption,
                               kb.kb_back_section("answer_writing"))

        case "photo":
            context.user_data["waiting_for"] = "answer_photo"
            context.user_data["aw_question"] = context.user_data.get("aw_question", "Your practice answer")
            caption = (
                "📸 <b>Upload Handwritten Answer</b>\n\n"
                "Send a clear photo of your handwritten answer.\n"
                "<i>AI will extract the text and evaluate it.</i>"
            )
            await show_section(query, context, "answer_writing", caption, kb.kb_cancel_writing())

        case _:
            await query.answer()


async def aw_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle typed answer submission."""
    if context.user_data.get("waiting_for") != "answer_text":
        return

    user_id     = update.effective_user.id
    answer_text = update.message.text
    question    = context.user_data.pop("aw_question", "")
    gs_paper    = context.user_data.pop("aw_paper", "GS Paper I")
    subject     = context.user_data.pop("aw_subject", "General")
    context.user_data.pop("waiting_for", None)

    if len(answer_text) < 30:
        await update.message.reply_text(
            "❌ Answer too short. Write at least 30 words for meaningful evaluation.",
            parse_mode=HTML,
        )
        return

    proc = await update.message.reply_text("⏳ <b>AI is evaluating your answer…</b>", parse_mode=HTML)

    result   = await evaluate_answer(question, answer_text, "GS", gs_paper)
    score    = result.get("score", 0)
    feedback = result.get("feedback", "Keep practising!")
    outline  = result.get("model_outline", "")

    score_bar = progress_bar(score, 10)
    criteria  = (
        f"Intro: {result.get('introduction',0)}/20  "
        f"Content: {result.get('content',0)}/30  "
        f"Examples: {result.get('examples',0)}/20\n"
        f"Structure: {result.get('structure',0)}/15  "
        f"Conclusion: {result.get('conclusion',0)}/15"
    )

    grade = (
        "🏆 Excellent!" if score >= 80 else
        "⭐ Good"       if score >= 65 else
        "✅ Moderate"   if score >= 50 else
        "⚠️ Needs work" if score >= 35 else
        "❌ Rewrite"
    )

    reply = (
        f"✍️ <b>Answer Evaluation</b>\n\n"
        f"<b>Score: {score}/100</b> {score_bar}\n"
        f"<b>Grade:</b> {grade}\n\n"
        f"<code>{criteria}</code>\n\n"
        f"<b>📝 Feedback:</b>\n{esc(feedback)}"
        f"{f'{chr(10)}{chr(10)}<b>📋 Model Outline:</b>{chr(10)}{esc(outline)}' if outline else ''}"
    )

    try:
        await proc.delete()
    except Exception:
        pass

    await update.message.reply_text(reply, parse_mode=HTML, reply_markup=kb.kb_after_answer_eval())

    save_answer(user_id, question, answer_text, "GS", gs_paper, subject, score,
                {k: result[k] for k in ["introduction","content","examples","structure","conclusion"] if k in result},
                feedback)
    award_xp(user_id, 20, "Answer written")
    log_event(user_id, "answer_written", f"score={score}")


async def aw_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle photo upload for handwritten answers."""
    if context.user_data.get("waiting_for") != "answer_photo":
        return

    user_id  = update.effective_user.id
    question = context.user_data.pop("aw_question", "Your answer")
    context.user_data.pop("waiting_for", None)

    proc = await update.message.reply_text("⏳ <b>Extracting text from photo…</b>", parse_mode=HTML)

    photo = update.message.photo[-1]  # Highest resolution
    try:
        file = await photo.get_file()
        file_bytes = await file.download_as_bytearray()
        img_b64    = base64.b64encode(file_bytes).decode("utf-8")
        extracted  = await extract_handwritten(img_b64)
    except Exception as e:
        logger.warning("Photo extraction failed: %s", e)
        extracted  = ""

    if not extracted:
        try:
            await proc.delete()
        except Exception:
            pass
        await update.message.reply_text(
            "❌ Could not extract text from the photo. "
            "Please ensure the image is clear and well-lit, or type your answer instead.",
            parse_mode=HTML,
            reply_markup=kb.kb_answer_writing(),
        )
        return

    # Evaluate the extracted text
    result = await evaluate_answer(question, extracted, "GS", "Mains")
    score  = result.get("score", 0)
    score_bar = progress_bar(score, 10)

    reply = (
        f"📸 <b>Handwritten Answer Evaluation</b>\n\n"
        f"<b>Extracted text:</b> <i>{esc(extracted[:100])}…</i>\n\n"
        f"<b>Score: {score}/100</b> {score_bar}\n\n"
        f"<b>Feedback:</b>\n{esc(result.get('feedback','Keep practising!'))}"
    )

    try:
        await proc.delete()
    except Exception:
        pass
    await update.message.reply_text(reply, parse_mode=HTML, reply_markup=kb.kb_after_answer_eval())

    save_answer(user_id, question, extracted, "Handwritten", "Mains", "General", score, {}, result.get("feedback",""))
    award_xp(user_id, 25, "Handwritten answer evaluated")
    log_event(user_id, "handwritten_answer", f"score={score}")


def get_aw_handlers() -> list:
    return [
        CallbackQueryHandler(aw_callback, pattern=r"^aw:"),
        MessageHandler(filters.PHOTO, aw_photo_handler),
        MessageHandler(filters.TEXT & ~filters.COMMAND, aw_text_handler),
    ]
