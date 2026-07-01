"""
handlers/settings.py — User Settings Handler
"""
import logging
from datetime import date, timedelta
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes, MessageHandler, filters

import keyboards as kb
from media import show_section
from storage.database import get_user, log_event, update_user_field
from utils.helpers import esc

logger = logging.getLogger(__name__)
HTML  = "HTML"


async def show_settings(query, context, user) -> None:
    caption = (
        "⚙️ <b>Settings</b>\n\n"
        f"<b>Current Plan:</b>\n"
        f"  {user['level'].title()} × {user['timeline_months']}m × {int(user['hours_per_day'])}h/day\n\n"
        f"<b>Optional Subject:</b> {esc(user['optional_subject'] or '—')}\n"
        f"<b>Vacation Mode:</b> {'🏖️ ON' if user['vacation_mode'] else 'OFF'}\n"
        f"<b>Leaderboard:</b> {'🏆 Visible' if user['leaderboard_opt'] else '🙈 Hidden'}\n\n"
        "Adjust your preferences below:"
    )
    await show_section(query, context, "settings", caption, kb.kb_settings(user))


async def settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query   = update.callback_query
    user_id = query.from_user.id
    action  = query.data.split(":")[1]
    user    = get_user(user_id)
    if not user:
        await query.answer()
        return

    match action:
        case "notif_morn":
            current = user["notify_morning"]
            update_user_field(user_id, "notify_morning", 0 if current else 1)
            await query.answer(f"Morning notifications {'OFF' if current else 'ON'}")
            await show_settings(query, context, get_user(user_id))

        case "notif_mid":
            current = user["notify_midday"]
            update_user_field(user_id, "notify_midday", 0 if current else 1)
            await query.answer(f"Midday notifications {'OFF' if current else 'ON'}")
            await show_settings(query, context, get_user(user_id))

        case "notif_eve":
            current = user["notify_evening"]
            update_user_field(user_id, "notify_evening", 0 if current else 1)
            await query.answer(f"Evening notifications {'OFF' if current else 'ON'}")
            await show_settings(query, context, get_user(user_id))

        case "vacation":
            if user["vacation_mode"]:
                update_user_field(user_id, "vacation_mode", 0)
                update_user_field(user_id, "vacation_end", "")
                await query.answer("✅ Vacation mode OFF")
                await show_settings(query, context, get_user(user_id))
            else:
                caption = (
                    "🏖️ <b>Vacation Mode</b>\n\n"
                    "Your streak is protected during vacation.\n"
                    "Daily tasks are paused. XP continues on return.\n\n"
                    "How long will you be away?"
                )
                await show_section(query, context, "settings", caption, kb.kb_vacation_duration())

        case "leaderboard":
            current = user["leaderboard_opt"]
            update_user_field(user_id, "leaderboard_opt", 0 if current else 1)
            msg = "Leaderboard: Hidden" if current else "Leaderboard: Visible"
            await query.answer(msg)
            await show_settings(query, context, get_user(user_id))

        case "change_plan":
            caption = (
                "🔁 <b>Change Study Plan</b>\n\n"
                "⚠️ This will reset your current day counter and plan settings.\n"
                "Your XP, streak, and answer history are preserved.\n\n"
                "Are you sure you want to start a new plan selection?"
            )
            await show_section(query, context, "settings", caption,
                               kb.kb_yes_no("set:confirm_change", "nav:settings"))

        case "confirm_change":
            update_user_field(user_id, "setup_done", 0)
            update_user_field(user_id, "current_day", 1)
            await query.answer("Plan reset. Starting setup…")
            log_event(user_id, "plan_change")
            from handlers.onboarding import cmd_start
            await cmd_start(update, context)

        case "exam_date":
            context.user_data["waiting_for"] = "exam_date"
            caption = (
                "📅 <b>Set Exam Date</b>\n\n"
                "Type your Prelims exam date in format:\n"
                "<code>YYYY-MM-DD</code>\n\n"
                "Example: <code>2025-05-25</code>"
            )
            await show_section(query, context, "settings", caption, kb.kb_back_section("settings"))

        case "delete_data":
            caption = (
                "⚠️ <b>Delete All Data</b>\n\n"
                "This will permanently delete:\n"
                "• Your study plan and progress\n"
                "• All XP, streaks, and badges\n"
                "• Answer history and mock results\n"
                "• All settings and preferences\n\n"
                "<b>This cannot be undone!</b>"
            )
            await show_section(query, context, "settings", caption, kb.kb_confirm_delete())

        case "confirm_delete":
            await _delete_user_data(user_id)
            await query.answer("✅ Data deleted")
            from handlers.onboarding import cmd_start
            await cmd_start(update, context)

        case _:
            await query.answer()

    log_event(user_id, f"setting_{action}")


async def _delete_user_data(user_id: int) -> None:
    """Delete all user data from the database."""
    from storage.database import get_db
    try:
        with get_db() as conn:
            for table in ["day_completions","revision_log","answer_history","mock_results",
                          "competency_scores","study_sessions","user_notes","bookmarks",
                          "xp_log","badges","plan_meta","events"]:
                conn.execute(f"DELETE FROM {table} WHERE user_id=?", (user_id,))
            conn.execute("UPDATE users SET setup_done=0, current_day=1, xp=0, streak=0, best_streak=0, rank_title='Aspirant' WHERE user_id=?", (user_id,))
        logger.info("Deleted all data for user_id=%d", user_id)
    except Exception:
        logger.exception("delete_user_data failed uid=%d", user_id)


async def vacation_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query   = update.callback_query
    user_id = query.from_user.id
    days    = int(query.data.split(":")[1])
    end_date= (date.today() + timedelta(days=days)).isoformat()

    update_user_field(user_id, "vacation_mode", 1)
    update_user_field(user_id, "vacation_end",  end_date)
    await query.answer(f"🏖️ Vacation mode ON for {days} days!")
    log_event(user_id, "vacation_on", f"days={days}")
    await show_settings(query, context, get_user(user_id))


async def settings_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get("waiting_for") != "exam_date":
        return
    user_id = update.effective_user.id
    text    = update.message.text.strip()
    context.user_data.pop("waiting_for", None)

    try:
        exam_dt = date.fromisoformat(text)
        update_user_field(user_id, "exam_date", text)
        days_left = (exam_dt - date.today()).days
        await update.message.reply_text(
            f"📅 Exam date set: <b>{text}</b>\n<b>{days_left}</b> days remaining!",
            parse_mode=HTML,
        )
        log_event(user_id, "exam_date_set", text)
    except ValueError:
        await update.message.reply_text(
            "❌ Invalid format. Use YYYY-MM-DD (e.g. 2025-05-25)", parse_mode=HTML
        )


def get_settings_handlers() -> list:
    return [
        CallbackQueryHandler(settings_callback, pattern=r"^set:"),
        CallbackQueryHandler(vacation_callback, pattern=r"^vac:"),
        MessageHandler(filters.TEXT & ~filters.COMMAND, settings_text_handler),
    ]
