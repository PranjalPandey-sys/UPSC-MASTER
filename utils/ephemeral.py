"""
utils/ephemeral.py — Disappearing Message System
==================================================
Handles auto-deleting messages after a delay.
Used for: processing indicators, countdown timers,
"peek tomorrow" previews, confirmation dialogs.
"""
import asyncio
import logging

from telegram import Bot
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def _delete_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """APScheduler/job_queue callback that deletes a message."""
    data = context.job.data
    try:
        await context.bot.delete_message(
            chat_id=data["chat_id"],
            message_id=data["message_id"],
        )
    except Exception:
        pass  # Message may already be deleted — silent fail is correct


async def send_ephemeral(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    text: str,
    delay_seconds: int = 30,
    parse_mode: str = "HTML",
) -> int | None:
    """
    Send a message that auto-deletes after delay_seconds.

    Returns the message_id (or None if send failed).
    """
    try:
        msg = await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
        )
        context.job_queue.run_once(
            _delete_job,
            delay_seconds,
            data={"chat_id": chat_id, "message_id": msg.message_id},
            name=f"ephem_{chat_id}_{msg.message_id}",
        )
        return msg.message_id
    except Exception as exc:
        logger.warning("send_ephemeral failed: %s", exc)
        return None


async def delete_message_safe(bot: Bot, chat_id: int, message_id: int) -> None:
    """Delete a message, silently ignoring any errors."""
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass


async def schedule_delete(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    message_id: int,
    delay_seconds: int = 30,
) -> None:
    """Schedule deletion of an existing message after delay_seconds."""
    try:
        context.job_queue.run_once(
            _delete_job,
            delay_seconds,
            data={"chat_id": chat_id, "message_id": message_id},
            name=f"ephem_{chat_id}_{message_id}",
        )
    except Exception as exc:
        logger.warning("schedule_delete failed: %s", exc)


# ── Processing indicator ───────────────────────────────────────────────────────

async def show_processing(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    text: str = "⏳ <b>Processing…</b>",
) -> int | None:
    """
    Send a 'Processing...' indicator.
    Caller is responsible for deleting it when done.
    Returns message_id.
    """
    try:
        msg = await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode="HTML",
        )
        return msg.message_id
    except Exception as exc:
        logger.warning("show_processing failed: %s", exc)
        return None
