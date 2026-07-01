"""
handlers/progress.py — Progress & Analytics Handler
"""
import logging
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

import keyboards as kb
from media import show_section
from services import plan_loader
from storage.database import count_completed_days, get_badges, get_user, log_event
from utils.helpers import compact_bar, esc, get_rank, progress_bar, sparkline, streak_emoji

logger = logging.getLogger(__name__)
HTML = "HTML"

BADGE_INFO = {
    "first_login":   ("🌱", "First Login", "Joined the bot"),
    "first_day":     ("📅", "Day 1 Done", "Completed first study day"),
    "week_warrior":  ("⚡", "Week Warrior", "7 days completed"),
    "month_master":  ("📅", "Month Master", "30 days completed"),
    "century":       ("💯", "Centurion",    "100 days completed"),
    "streak_7":      ("🔥", "Streak 7",     "7-day streak"),
    "streak_30":     ("🔥🔥", "Streak 30", "30-day streak"),
    "answer_10":     ("✍️", "Pen Master",   "10 answers written"),
    "mock_5":        ("🧪", "Mock Expert",  "5 mock tests taken"),
}


async def show_progress(query, context, user) -> None:
    user_id   = user["user_id"]
    level     = user["level"] or "beginner"
    months    = user["timeline_months"] or 6
    hours     = user["hours_per_day"]   or 4
    day_num   = user["current_day"]     or 1
    xp        = user["xp"]              or 0
    streak    = user["streak"]          or 0
    best      = user["best_streak"]     or 0

    pid        = f"{level}_{months}months_{int(hours)}hours"
    total_days = plan_loader.get_plan_length(pid)
    done_days  = count_completed_days(user_id)
    pct_done   = round(done_days / total_days * 100, 1) if total_days else 0
    rank       = get_rank(xp)

    prog_bar = progress_bar(pct_done, 10)
    s_emoji  = streak_emoji(streak)

    # Phase stats
    phase = plan_loader.get_phase_for_day(pid, day_num)

    caption = (
        f"📊 <b>Your Progress Report</b>\n\n"
        f"<b>📈 Overall Progress:</b>\n"
        f"  {prog_bar} {pct_done:.0f}%\n"
        f"  Days done: <b>{done_days}/{total_days}</b>\n\n"
        f"<b>⚡ XP & Rank:</b>\n"
        f"  XP: <b>{xp:,}</b> — <b>{rank}</b>\n\n"
        f"<b>{s_emoji} Streak:</b> {streak} days (Best: {best})\n\n"
        f"<b>📅 Current Phase:</b> {esc(phase)}\n\n"
        "Explore detailed stats below 👇"
    )
    await show_section(query, context, "progress", caption, kb.kb_progress())


async def progress_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query   = update.callback_query
    user_id = query.from_user.id
    action  = query.data.split(":")[1]
    user    = get_user(user_id)

    if not user:
        await query.answer()
        return

    match action:
        case "subjects":
            pid    = f"{user['level']}_{user['timeline_months']}months_{int(user['hours_per_day'])}hours"
            review = __import__("data.plan_reviews", fromlist=["get_plan_review"]).get_plan_review(pid)
            cov    = review.get("syllabus_coverage", {})
            if cov:
                lines = [f"  {esc(sub)}: {compact_bar(int(str(pct).replace('%','').strip() or 0), 6)} {esc(str(pct))}"
                         for sub, pct in cov.items()]
                caption = "📊 <b>Subject Coverage</b>\n\n" + "\n".join(lines[:12])
            else:
                caption = (
                    "📊 <b>Subject Coverage</b>\n\n"
                    "Coverage details will appear as you complete daily tasks.\n\n"
                    f"Plan: <code>{pid}</code>"
                )
            await show_section(query, context, "progress", caption, kb.kb_back_section("progress"))

        case "weekly":
            # Simple stats — no AI call
            xp   = user["xp"] or 0
            done = count_completed_days(user_id)
            caption = (
                "📈 <b>This Week's Snapshot</b>\n\n"
                f"Days completed (total): <b>{done}</b>\n"
                f"Current streak: <b>{user['streak'] or 0}</b>\n"
                f"Total XP: <b>{xp:,}</b>\n"
                f"Rank: <b>{get_rank(xp)}</b>\n\n"
                "<i>Detailed weekly AI report available every Monday morning.</i>"
            )
            await show_section(query, context, "progress", caption, kb.kb_back_section("progress"))

        case "mocks":
            from storage.database import get_db
            try:
                with get_db() as conn:
                    rows = conn.execute(
                        "SELECT subject, accuracy, created_at FROM mock_results WHERE user_id=? ORDER BY created_at DESC LIMIT 10",
                        (user_id,),
                    ).fetchall()
            except Exception:
                rows = []
            if not rows:
                await query.answer("No mock tests yet!", show_alert=True)
                return
            lines = [f"  {r['subject'][:15]}: {progress_bar(r['accuracy'],6)} {r['accuracy']:.0f}%" for r in rows]
            caption = "🧪 <b>Mock Test History</b>\n\n" + "\n".join(lines)
            await show_section(query, context, "progress", caption, kb.kb_back_section("progress"))

        case "answers":
            from storage.database import get_answer_history
            history = get_answer_history(user_id, 10)
            if not history:
                await query.answer("No answers written yet!", show_alert=True)
                return
            scores = [r["score"] for r in history if r["score"]]
            avg    = round(sum(scores) / len(scores), 1) if scores else 0
            lines  = [f"  {r['gs_paper']}: {r['score']}/100" for r in history[:8]]
            caption = (
                f"✍️ <b>Answer Writing Stats</b>\n\n"
                f"Total answers: <b>{len(history)}</b>\n"
                f"Average score: <b>{avg}/100</b>\n\n" +
                "\n".join(lines)
            )
            await show_section(query, context, "progress", caption, kb.kb_back_section("progress"))

        case "badges":
            badges = get_badges(user_id)
            if not badges:
                caption = "🎖️ <b>Badges</b>\n\nNo badges yet! Complete tasks to earn your first badge."
            else:
                lines = []
                for bid in badges:
                    info = BADGE_INFO.get(bid, ("🏅", bid, ""))
                    lines.append(f"  {info[0]} <b>{info[1]}</b> — {info[2]}")
                caption = "🎖️ <b>Your Badges</b>\n\n" + "\n".join(lines)
            await show_section(query, context, "progress", caption, kb.kb_back_section("progress"))

        case "weak":
            import json
            weak = json.loads(user["weak_subjects"] or "[]")
            if not weak:
                caption = "✅ No weak areas flagged. Update in Settings if needed."
            else:
                lines = [f"  ⚠️ {esc(s)}" for s in weak]
                caption = "📉 <b>Weak Areas</b>\n\n" + "\n".join(lines) + "\n\n<i>These get extra attention in your daily plan.</i>"
            await show_section(query, context, "progress", caption, kb.kb_back_section("progress"))

        case _:
            await query.answer()

    log_event(user_id, f"progress_{action}")


def get_progress_handlers() -> list:
    return [CallbackQueryHandler(progress_callback, pattern=r"^prog:")]
