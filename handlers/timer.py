"""
handlers/timer.py — Pomodoro / Study Timer
"""
import asyncio
import logging
from datetime import datetime, timezone
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

import keyboards as kb
from media import show_section
from utils.ephemeral import send_ephemeral
from utils.helpers import esc

logger = logging.getLogger(__name__)
HTML = "HTML"

_active_timers: dict[int, asyncio.Task] = {}


async def show_timer(query, context) -> None:
    caption = (
        "⏱️ <b>Study Timer</b>\n\n"
        "Pomodoro and custom timers for focused study sessions.\n\n"
        "<b>Choose a duration:</b>\n"
        "  🍅 25 min — Classic Pomodoro\n"
        "  📖 45 min — Extended focus\n"
        "  📚 60 min — Full study session\n"
        "  🧠 90 min — Deep work block\n\n"
        "<i>You'll get a notification when time is up!</i>"
    )
    await show_section(query, context, "timer", caption, kb.kb_timer())


async def timer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query   = update.callback_query
    user_id = query.from_user.id
    action  = query.data.split(":")[1]

    match action:
        case "25" | "45" | "60" | "90":
            minutes = int(action)
            # Cancel existing timer
            existing = _active_timers.get(user_id)
            if existing and not existing.done():
                existing.cancel()

            await query.answer(f"⏱️ {minutes}-minute timer started!")
            task = asyncio.create_task(_run_timer(context, query.message.chat_id, user_id, minutes))
            _active_timers[user_id] = task

            caption = (
                f"⏱️ <b>Timer Running: {minutes} Minutes</b>\n\n"
                f"Your study session has started.\n"
                f"Notification in <b>{minutes} minutes</b>.\n\n"
                "💡 <i>Put your phone face-down. Focus on one topic only.</i>"
            )
            await show_section(query, context, "timer", caption, kb.kb_timer())

        case "stop":
            existing = _active_timers.pop(user_id, None)
            if existing and not existing.done():
                existing.cancel()
                await query.answer("⏹ Timer stopped!")
            else:
                await query.answer("No active timer.", show_alert=True)

        case _:
            await query.answer()


async def _run_timer(context, chat_id: int, user_id: int, minutes: int) -> None:
    await asyncio.sleep(minutes * 60)
    _active_timers.pop(user_id, None)
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"⏰ <b>Time's Up! {minutes} minutes complete.</b>\n\n"
                "🎉 Great focus session! Take a 5-minute break, then continue.\n\n"
                "<i>Consistent study sessions build unstoppable momentum.</i>"
            ),
            parse_mode=HTML,
            reply_markup=kb.kb_timer(),
        )
    except Exception as e:
        logger.warning("Timer notification failed uid=%d: %s", user_id, e)


def get_timer_handlers() -> list:
    return [CallbackQueryHandler(timer_callback, pattern=r"^timer:")]
