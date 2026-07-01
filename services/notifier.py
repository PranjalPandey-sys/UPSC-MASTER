"""
services/notifier.py — Push Notification Service
==================================================
Sends morning, midday, evening and weekly notifications.
All schedules run via APScheduler (job_queue).
"""
import asyncio
import logging
import random
from datetime import datetime, timezone

from telegram.ext import ContextTypes

import config
from storage.database import award_xp, get_all_users_for_push, get_due_revisions, log_event
from utils.helpers import get_motivation, level_emoji, streak_emoji

logger = logging.getLogger(__name__)
HTML = "HTML"


async def send_morning_push(context: ContextTypes.DEFAULT_TYPE) -> None:
    """09:00 IST — Morning motivation + today's mission preview."""
    from services import plan_loader
    users = get_all_users_for_push()
    sent  = 0
    for u in users:
        if not u["notify_morning"]:
            continue
        if u["vacation_mode"]:
            continue
        try:
            user_id = u["user_id"]
            day_num = u["current_day"] or 1
            streak  = u["streak"] or 0
            level   = u["level"] or "beginner"
            months  = u["timeline_months"] or 6
            hours   = u["hours_per_day"]   or 4
            pid     = f"{level}_{months}months_{int(hours)}hours"

            task = plan_loader.get_day_task(pid, day_num)
            task_preview = ""
            if task:
                task_preview = (
                    f"\n\n<b>📚 Today:</b> {task.get('subject','')} — "
                    f"{task.get('subtopic','')}\n"
                    f"<i>{task.get('hours', hours)}h | {task.get('phase','Foundation')} Phase</i>"
                )

            motivation = get_motivation(user_id, day_num)
            s_emoji    = streak_emoji(streak)
            level_e    = level_emoji(level)

            msg = (
                f"🌅 <b>Good morning, Aspirant!</b>\n\n"
                f"{s_emoji} Streak: <b>{streak}</b> days  |  {level_e} Day {day_num}\n"
                f"{task_preview}\n\n"
                f"<i>\u201c{motivation}\u201d</i>\n\n"
                f"Open the bot to start your day 👇"
            )

            from keyboards import kb_home
            await context.bot.send_message(
                chat_id=user_id,
                text=msg,
                parse_mode=HTML,
                reply_markup=kb_home(streak, day_num),
            )
            sent += 1
            await asyncio.sleep(config.BROADCAST_DELAY)
        except Exception as e:
            logger.debug("Morning push failed uid=%d: %s", u["user_id"], e)

    logger.info("Morning push sent to %d users", sent)


async def send_midday_push(context: ContextTypes.DEFAULT_TYPE) -> None:
    """13:00 IST — Midday check-in."""
    users = get_all_users_for_push()
    sent  = 0
    for u in users:
        if not u["notify_midday"] or u["vacation_mode"]:
            continue
        try:
            today_done = u.get("last_done_date") == str(datetime.now(timezone.utc).date())
            if today_done:
                continue  # Already done — skip midday push

            day_num = u["current_day"] or 1
            msg = (
                "⏰ <b>Midday Check-in</b>\n\n"
                f"Day {day_num} — Have you started today's mission?\n\n"
                "Even 30 minutes now makes a difference.\n"
                "Open the bot and mark progress 📚"
            )
            await context.bot.send_message(chat_id=u["user_id"], text=msg, parse_mode=HTML)
            sent += 1
            await asyncio.sleep(config.BROADCAST_DELAY)
        except Exception as e:
            logger.debug("Midday push failed uid=%d: %s", u["user_id"], e)

    logger.info("Midday push sent to %d users", sent)


async def send_evening_push(context: ContextTypes.DEFAULT_TYPE) -> None:
    """20:00 IST — Evening revision reminder + trivia."""
    from data.fallbacks import DAILY_TRIVIA
    users = get_all_users_for_push()
    sent  = 0
    trivia = random.choice(DAILY_TRIVIA) if DAILY_TRIVIA else None

    for u in users:
        if not u["notify_evening"] or u["vacation_mode"]:
            continue
        try:
            user_id = u["user_id"]
            day_num = u["current_day"] or 1
            due     = get_due_revisions(user_id, day_num)
            rev_msg = f"\n🔄 <b>{len(due)} revision{'s' if len(due) != 1 else ''} due</b>" if due else ""

            trivia_text = ""
            if trivia:
                trivia_text = (
                    f"\n\n🧠 <b>UPSC Trivia</b>\n"
                    f"<i>{trivia['q']}</i>\n"
                    f"<b>Answer:</b> {trivia['a'][:100]}…"
                )

            msg = (
                f"🌙 <b>Evening Check-in — Day {day_num}</b>"
                f"{rev_msg}"
                f"{trivia_text}\n\n"
                "Complete today's tasks before midnight! 🎯"
            )
            await context.bot.send_message(chat_id=user_id, text=msg, parse_mode=HTML)
            sent += 1
            await asyncio.sleep(config.BROADCAST_DELAY)
        except Exception as e:
            logger.debug("Evening push failed uid=%d: %s", u["user_id"], e)

    logger.info("Evening push sent to %d users", sent)


async def send_weekly_report(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Monday 06:00 IST — Weekly performance report."""
    from services.gemini import get_weekly_report
    from storage.database import count_completed_days, get_db

    users = get_all_users_for_push()
    sent  = 0
    for u in users:
        if not u["notify_weekly"] or u["vacation_mode"]:
            continue
        try:
            user_id = u["user_id"]
            # Gather weekly stats (last 7 days)
            try:
                with get_db() as conn:
                    r1 = conn.execute(
                        "SELECT COUNT(*) FROM day_completions WHERE user_id=? AND done_at > datetime('now','-7 days')",
                        (user_id,),
                    ).fetchone()
                    r2 = conn.execute(
                        "SELECT COUNT(*) FROM answer_history WHERE user_id=? AND created_at > datetime('now','-7 days')",
                        (user_id,),
                    ).fetchone()
                    r3 = conn.execute(
                        "SELECT COUNT(*) FROM mock_results WHERE user_id=? AND created_at > datetime('now','-7 days')",
                        (user_id,),
                    ).fetchone()
                    r4 = conn.execute(
                        "SELECT SUM(amount) FROM xp_log WHERE user_id=? AND created_at > datetime('now','-7 days')",
                        (user_id,),
                    ).fetchone()
                days_done = r1[0] if r1 else 0
                answers   = r2[0] if r2 else 0
                mocks     = r3[0] if r3 else 0
                xp_week   = r4[0] if r4 and r4[0] else 0
            except Exception:
                days_done = answers = mocks = xp_week = 0

            stats = {
                "days_done":    days_done,
                "answers":      answers,
                "mocks":        mocks,
                "streak":       u["streak"] or 0,
                "xp_week":      xp_week,
                "best_subject": "Polity",
                "weak_subject": "Economy",
            }
            report = await get_weekly_report(stats)
            msg = f"📊 <b>Weekly Report — {u['level'].title() if u['level'] else 'Aspirant'}</b>\n\n{report}"
            await context.bot.send_message(chat_id=user_id, text=msg, parse_mode=HTML)
            sent += 1
            await asyncio.sleep(config.BROADCAST_DELAY)
        except Exception as e:
            logger.debug("Weekly report failed uid=%d: %s", u["user_id"], e)

    logger.info("Weekly reports sent to %d users", sent)


def register_all_schedules(job_queue) -> None:
    """Register all recurring notification jobs in APScheduler."""
    from apscheduler.triggers.cron import CronTrigger

    # Morning: 09:00 IST = 03:30 UTC
    job_queue.run_custom(send_morning_push, CronTrigger(hour=3, minute=30), name="morning_push")

    # Midday: 13:00 IST = 07:30 UTC
    job_queue.run_custom(send_midday_push,  CronTrigger(hour=7, minute=30), name="midday_push")

    # Evening: 20:00 IST = 14:30 UTC
    job_queue.run_custom(send_evening_push, CronTrigger(hour=14, minute=30), name="evening_push")

    # Weekly: Monday 06:00 IST = Monday 00:30 UTC
    job_queue.run_custom(
        send_weekly_report,
        CronTrigger(day_of_week="mon", hour=0, minute=30),
        name="weekly_report",
    )

    logger.info("✅ All notification schedules registered")
