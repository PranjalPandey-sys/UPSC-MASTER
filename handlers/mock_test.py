"""
handlers/mock_test.py — Mock Test / MCQ Handler
"""
import logging
import random

from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

import keyboards as kb
from data.fallbacks import SUBJECT_MCQ, ALL_SAMPLE_MCQ
from media import show_section
from storage.database import award_xp, get_user, log_event, save_mock_result
from utils.helpers import esc, progress_bar

logger = logging.getLogger(__name__)
HTML = "HTML"


async def show_mock_menu(query, context: ContextTypes.DEFAULT_TYPE, user) -> None:
    """Show mock test section."""
    caption = (
        "🧪 <b>Mock Tests</b>\n\n"
        "Test your knowledge with subject-wise MCQs and full Prelims practice.\n\n"
        "<b>Choose a subject:</b>\n"
        "  • Each test has 5-10 questions\n"
        "  • Explanations provided for every answer\n"
        "  • Score tracked in your analytics\n\n"
        "💡 <i>Tip: Take mocks without studying first — see your baseline!</i>"
    )
    await show_section(query, context, "mock", caption, kb.kb_mock_menu())


async def mock_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle mock: callbacks."""
    query   = update.callback_query
    user_id = query.from_user.id
    data    = query.data
    parts   = data.split(":")
    action  = parts[1]

    match action:
        case "Polity" | "History" | "Geography" | "Economy" | "Environment" | "S&T" | "Mixed":
            await _start_test(query, context, action)

        case "scorecard":
            user = get_user(user_id)
            if not user:
                await query.answer()
                return
            from storage.database import get_db
            try:
                with get_db() as conn:
                    rows = conn.execute(
                        "SELECT subject, AVG(accuracy) as avg_acc, COUNT(*) as cnt "
                        "FROM mock_results WHERE user_id=? GROUP BY subject",
                        (user_id,),
                    ).fetchall()
            except Exception:
                rows = []
            if not rows:
                await query.answer("No mock tests taken yet!", show_alert=True)
                return
            lines = [
                f"  {r['subject']}: {progress_bar(r['avg_acc'],6)} {r['avg_acc']:.0f}% ({r['cnt']} tests)"
                for r in rows
            ]
            caption = "📊 <b>Mock Test Score Card</b>\n\n" + "\n".join(lines)
            await show_section(query, context, "mock", caption, kb.kb_back_section("mock"))

        case "end":
            await _end_test_and_show_results(query, context, user_id)

        case _:
            await query.answer()


async def _end_test_and_show_results(query, context, user_id: int) -> None:
    """Finalise a mock test: save result, award XP, show score card."""
    score_data = context.user_data.pop("mock_score", {"correct": 0, "total": 0})
    correct = score_data.get("correct", 0)
    total   = score_data.get("total", 0)
    subject = context.user_data.pop("mock_subject", "Mixed")
    context.user_data.pop("mock_questions", None)
    context.user_data.pop("mock_idx", None)

    accuracy = round(correct / total * 100, 1) if total > 0 else 0
    bar      = progress_bar(accuracy, 10)

    grade = (
        "🏆 Excellent!" if accuracy >= 80 else
        "⭐ Good"       if accuracy >= 60 else
        "✅ Moderate"   if accuracy >= 40 else
        "⚠️ Needs work"
    )

    save_mock_result(user_id, "subject_quiz", subject, total, correct, 0, [])
    award_xp(user_id, 25, "Mock test complete")
    log_event(user_id, "mock_done", f"subject={subject} acc={accuracy}")

    caption = (
        f"🧪 <b>Test Complete!</b>\n\n"
        f"<b>Subject:</b> {esc(subject)}\n"
        f"<b>Score:</b> {correct}/{total} correct\n"
        f"<b>Accuracy:</b> {bar} {accuracy:.0f}%\n"
        f"<b>Grade:</b> {grade}\n\n"
        "+25 XP earned! 🎉"
    )
    await show_section(query, context, "mock", caption, kb.kb_after_mock())


async def _start_test(query, context, subject: str) -> None:
    """Start a mock test for a given subject."""
    user_id = query.from_user.id
    if subject == "Mixed":
        questions = random.sample(ALL_SAMPLE_MCQ, min(5, len(ALL_SAMPLE_MCQ)))
    else:
        pool = SUBJECT_MCQ.get(subject, ALL_SAMPLE_MCQ)
        questions = random.sample(pool, min(5, len(pool))) if pool else random.sample(ALL_SAMPLE_MCQ, 5)

    context.user_data["mock_questions"] = questions
    context.user_data["mock_idx"]       = 0
    context.user_data["mock_score"]     = {"correct": 0, "total": 0}
    context.user_data["mock_subject"]   = subject

    await query.answer()
    await _send_question(query, context, 0)


async def _send_question(query, context, idx: int) -> None:
    """Send a single MCQ question."""
    questions = context.user_data.get("mock_questions", [])
    if idx >= len(questions):
        # Safety fallback: shouldn't normally trigger since mcq_callback
        # only offers "Next" when next_idx < total
        await _end_test_and_show_results(query, context, query.from_user.id)
        return

    q    = questions[idx]
    total= len(questions)
    opts = "\n".join(
        f"  {'ABCD'[i]}) {esc(o)}" for i, o in enumerate(q["options"])
    )
    caption = (
        f"❓ <b>Question {idx+1}/{total}</b>\n\n"
        f"<b>{esc(q['q'])}</b>\n\n{opts}"
    )
    await show_section(query, context, "mock", caption, kb.kb_mock_answer(idx, total))


async def mcq_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle MCQ answer: mcq:question_idx:chosen_option"""
    query   = update.callback_query
    parts   = query.data.split(":")
    q_idx   = int(parts[1])
    chosen  = int(parts[2])

    questions = context.user_data.get("mock_questions", [])
    if q_idx >= len(questions):
        await query.answer()
        return

    q      = questions[q_idx]
    correct= q.get("answer", 0)
    is_correct = (chosen == correct)

    score_data = context.user_data.get("mock_score", {"correct": 0, "total": 0})
    score_data["total"] += 1
    if is_correct:
        score_data["correct"] += 1
    context.user_data["mock_score"] = score_data

    result_icon = "✅" if is_correct else "❌"
    correct_letter = "ABCD"[correct]
    chosen_letter  = "ABCD"[chosen]

    caption = (
        f"{result_icon} <b>{'Correct!' if is_correct else 'Incorrect'}</b>\n\n"
        f"<b>Q{q_idx+1}:</b> {esc(q['q'])}\n\n"
        f"Your answer: <b>{chosen_letter}</b>  |  Correct: <b>{correct_letter}</b>\n\n"
        f"<b>Explanation:</b>\n{esc(q.get('exp',''))}"
    )

    # Auto-advance or end
    next_idx = q_idx + 1
    total = len(questions)
    if next_idx >= total:
        from telegram import InlineKeyboardButton as Btn, InlineKeyboardMarkup as Markup
        advance_kb = Markup([[Btn("📊 See Results", callback_data="mock:end")]])
    else:
        from telegram import InlineKeyboardButton as Btn, InlineKeyboardMarkup as Markup
        advance_kb = Markup([
            [Btn(f"▶ Next Question ({next_idx+1}/{total})", callback_data=f"mcq:{next_idx}:skip")]
        ])

    await show_section(query, context, "mock", caption, advance_kb)


async def mcq_skip(update, context) -> None:
    """Show next question when Next button tapped."""
    query = update.callback_query
    parts = query.data.split(":")
    await _send_question(query, context, int(parts[1]))


def get_mock_handlers() -> list:
    return [
        CallbackQueryHandler(mock_callback, pattern=r"^mock:"),
        CallbackQueryHandler(mcq_callback, pattern=r"^mcq:\d+:\d+$"),
        CallbackQueryHandler(mcq_skip, pattern=r"^mcq:\d+:skip$"),
    ]
