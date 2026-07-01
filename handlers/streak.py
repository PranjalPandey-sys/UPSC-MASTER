"""
handlers/streak.py — Streak & Leaderboard Handler
"""
import logging
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

import keyboards as kb
from media import show_section
from storage.database import get_badges, get_user, log_event
from utils.helpers import esc, get_rank, progress_bar, streak_emoji, xp_to_next_rank

logger = logging.getLogger(__name__)
HTML  = "HTML"


async def show_streak(query, context, user) -> None:
    streak  = user["streak"]      or 0
    best    = user["best_streak"] or 0
    shields = user["streak_shields"] or 0
    xp      = user["xp"]         or 0
    s_emoji = streak_emoji(streak)
    rank    = get_rank(xp)
    _, needed, to_go = xp_to_next_rank(xp)

    milestones = [(7,"🔥 Week"),(14,"⚡ Fortnight"),(30,"🌟 Month"),(60,"💫 Two Months"),(100,"🏆 100 Days")]
    next_mile  = next((m for m in milestones if m[0] > streak), None)
    mile_text  = f"\nNext milestone: <b>{next_mile[1]}</b> ({next_mile[0]-streak} days away)" if next_mile else "\n🎉 All major milestones achieved!"

    caption = (
        f"🔥 <b>Your Streak & XP</b>\n\n"
        f"<b>{s_emoji} Current Streak:</b> {streak} days\n"
        f"<b>🏆 Best Streak:</b> {best} days\n"
        f"<b>🛡️ Streak Shields:</b> {shields} remaining\n"
        f"{mile_text}\n\n"
        f"<b>⚡ XP:</b> {xp:,}\n"
        f"<b>🎖️ Rank:</b> {rank}\n"
        f"{f'Progress to {_}: {progress_bar(min(100,(xp/needed*100)) if needed else 100,8)} (+{to_go:,} XP)' if to_go else 'MAX RANK achieved!'}\n\n"
        "<i>Streak Shields protect your streak for 1 missed day. Earned every 7 days.</i>"
    )
    await show_section(query, context, "streak", caption, kb.kb_streak(streak, xp))


async def streak_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query   = update.callback_query
    user_id = query.from_user.id
    action  = query.data.split(":")[1]
    user    = get_user(user_id)
    if not user:
        await query.answer()
        return

    match action:
        case "leaderboard":
            from storage.database import get_db
            try:
                with get_db() as conn:
                    rows = conn.execute(
                        "SELECT full_name, username, xp, streak FROM users WHERE leaderboard_opt=1 ORDER BY xp DESC LIMIT 10"
                    ).fetchall()
            except Exception:
                rows = []
            if not rows:
                caption = "🏆 <b>Leaderboard</b>\n\nNo users on the leaderboard yet.\nEnable in Settings to appear here!"
            else:
                medals = ["🥇","🥈","🥉"] + ["🎯"]*7
                lines  = [
                    f"{medals[i]} {esc(r['full_name'] or r['username'] or 'Aspirant')} — {r['xp']:,} XP | 🔥{r['streak']}"
                    for i, r in enumerate(rows)
                ]
                caption = "🏆 <b>XP Leaderboard</b>\n\n" + "\n".join(lines)
            await show_section(query, context, "streak", caption, kb.kb_back_section("streak"))

        case "badges":
            badges = get_badges(user_id)
            from handlers.progress import BADGE_INFO
            if not badges:
                caption = "🎖️ No badges yet! Complete tasks to earn your first."
            else:
                lines = [f"  {BADGE_INFO.get(b,('🏅',b,''))[0]} {BADGE_INFO.get(b,('','',b))[1]}" for b in badges]
                caption = "🎖️ <b>Your Badges</b>\n\n" + "\n".join(lines)
            await show_section(query, context, "streak", caption, kb.kb_back_section("streak"))

        case "shields":
            shields = user["streak_shields"] or 0
            caption = (
                f"🛡️ <b>Streak Shields</b>\n\n"
                f"You have <b>{shields}</b> shield{'s' if shields != 1 else ''}.\n\n"
                "Streak Shields protect your streak for 1 missed day.\n"
                "You earn 1 shield every 7-day milestone (up to max 3)."
            )
            await show_section(query, context, "streak", caption, kb.kb_back_section("streak"))

        case "xp_log":
            from storage.database import get_db
            try:
                with get_db() as conn:
                    rows = conn.execute(
                        "SELECT amount, reason, created_at FROM xp_log WHERE user_id=? ORDER BY created_at DESC LIMIT 10",
                        (user_id,),
                    ).fetchall()
            except Exception:
                rows = []
            if not rows:
                caption = "⚡ No XP events yet."
            else:
                lines = [f"  +{r['amount']} — {esc(r['reason'])}" for r in rows]
                caption = "⚡ <b>XP History</b>\n\n" + "\n".join(lines)
            await show_section(query, context, "streak", caption, kb.kb_back_section("streak"))

        case _:
            await query.answer()


def get_streak_handlers() -> list:
    return [CallbackQueryHandler(streak_callback, pattern=r"^streak:")]
