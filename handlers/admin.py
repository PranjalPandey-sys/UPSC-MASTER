"""
handlers/admin.py — Admin Panel Handler
"""
import asyncio
import logging
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes, MessageHandler, filters

import config
import keyboards as kb
from media import show_section
from storage.database import (
    active_users_count, get_db, get_db_stats, get_recent_errors,
    get_users_paginated, log_admin_action, log_event, search_users,
    total_users, update_user_field,
)
from utils.helpers import esc

logger = logging.getLogger(__name__)
HTML  = "HTML"


def _is_admin(user_id: int) -> bool:
    return user_id in config.ADMIN_IDS


async def show_admin(query, context, user_id: int) -> None:
    if not _is_admin(user_id):
        await query.answer("⛔ Admin only.", show_alert=True)
        return
    total   = total_users()
    active1 = active_users_count(1)
    active7 = active_users_count(7)
    caption = (
        "🛡️ <b>Admin Panel</b>\n\n"
        f"👥 Total users: <b>{total}</b>\n"
        f"⚡ Active today: <b>{active1}</b>\n"
        f"📅 Active this week: <b>{active7}</b>\n\n"
        "Choose an action:"
    )
    await show_section(query, context, "admin", caption, kb.kb_admin())


async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query   = update.callback_query
    user_id = query.from_user.id

    if not _is_admin(user_id):
        await query.answer("⛔ Admin only.", show_alert=True)
        return

    action = query.data.split(":")[1]

    match action:
        case "stats":
            total    = total_users()
            active1  = active_users_count(1)
            active7  = active_users_count(7)
            active30 = active_users_count(30)
            db_stats = get_db_stats()
            caption  = (
                "📊 <b>Platform Statistics</b>\n\n"
                f"<b>Users:</b>\n"
                f"  Total: <b>{total}</b>\n"
                f"  Active today: <b>{active1}</b>\n"
                f"  Active this week: <b>{active7}</b>\n"
                f"  Active this month: <b>{active30}</b>\n\n"
                f"<b>Database:</b>\n"
                f"  Size: <b>{db_stats.get('file_size_mb', 0):.2f} MB</b>\n"
            )
            row_counts = db_stats.get("row_counts", {})
            for table, count in row_counts.items():
                caption += f"  {table}: <b>{count:,}</b>\n"
            await show_section(query, context, "admin", caption, kb.kb_back_section("admin"))
            log_admin_action(user_id, "view_stats")

        case "users":
            offset = int(query.data.split(":")[2]) if len(query.data.split(":")) > 2 else 0
            users  = get_users_paginated(offset, 10)
            total  = total_users()
            lines  = []
            for u in users:
                name = u["full_name"] or u["username"] or f"uid_{u['user_id']}"
                lines.append(
                    f"  {'✅' if u['setup_done'] else '⏳'} "
                    f"<code>{u['user_id']}</code> {esc(name[:20])} "
                    f"| {u['level'] or '—'} | XP:{u['xp'] or 0}"
                )
            caption = (
                f"👥 <b>Users</b> (showing {offset+1}–{min(offset+10, total)} of {total})\n\n"
                + "\n".join(lines)
            )
            await show_section(query, context, "admin", caption,
                               kb.kb_admin_users_nav(offset, total, 10))
            log_admin_action(user_id, "view_users", f"offset={offset}")

        case "broadcast":
            context.user_data["admin_action"] = "broadcast"
            caption = (
                "📣 <b>Broadcast Message</b>\n\n"
                "Type the message to send to ALL users with completed setup.\n\n"
                "Supports HTML formatting:\n"
                "<code>&lt;b&gt;bold&lt;/b&gt;</code>, "
                "<code>&lt;i&gt;italic&lt;/i&gt;</code>, "
                "<code>&lt;code&gt;code&lt;/code&gt;</code>"
            )
            await show_section(query, context, "admin", caption, kb.kb_back_section("admin"))

        case "bc_confirm":
            msg = context.user_data.pop("broadcast_message", "")
            if not msg:
                await query.answer("No message to send!", show_alert=True)
                return
            asyncio.create_task(_do_broadcast(context, user_id, msg))
            await query.answer("📣 Broadcast started!")
            log_admin_action(user_id, "broadcast_sent", f"len={len(msg)}")

        case "ai_insights":
            await query.answer("⏳ Generating insights…")
            from services.gemini import get_ai_insights
            stats = {
                "total_users":  total_users(),
                "active_today": active_users_count(1),
                "active_week":  active_users_count(7),
            }
            insights = await get_ai_insights(stats)
            caption  = f"🤖 <b>AI Platform Insights</b>\n\n{esc(insights)}"
            await show_section(query, context, "admin", caption, kb.kb_back_section("admin"))

        case "db_info":
            db_stats = get_db_stats()
            row_counts = db_stats.get("row_counts", {})
            lines = [f"  {t}: {c:,}" for t, c in row_counts.items()]
            caption = (
                f"🗃️ <b>Database Info</b>\n\n"
                f"Path: <code>{config.DB_PATH}</code>\n"
                f"Size: <b>{db_stats.get('file_size_mb',0):.2f} MB</b>\n\n"
                "<b>Row counts:</b>\n" + "\n".join(lines)
            )
            await show_section(query, context, "admin", caption, kb.kb_back_section("admin"))

        case "errors":
            errors = get_recent_errors(15)
            if not errors:
                caption = "✅ No recent errors in the log."
            else:
                lines = [
                    f"  [{e['severity']}] {e['module']}.{e['function']}: {esc(str(e['message'])[:60])}"
                    for e in errors
                ]
                caption = "🚨 <b>Recent Errors</b>\n\n" + "\n".join(lines)
            await show_section(query, context, "admin", caption, kb.kb_back_section("admin"))

        case "clear_cache":
            from storage.database import clear_image_cache
            clear_image_cache()
            await query.answer("✅ Image cache cleared!")
            log_admin_action(user_id, "clear_image_cache")

        case "backup":
            await query.answer("⏳ Starting backup…")
            from services.backup import run_backup
            result = await run_backup()
            caption = f"💾 <b>Backup</b>\n\n{esc(result)}"
            await show_section(query, context, "admin", caption, kb.kb_back_section("admin"))
            log_admin_action(user_id, "manual_backup")

        case "announce":
            context.user_data["admin_action"] = "announce"
            caption = "📢 <b>System Announcement</b>\n\nType the announcement message:"
            await show_section(query, context, "admin", caption, kb.kb_back_section("admin"))

        case "ban":
            target_uid = int(query.data.split(":")[2])
            target     = get_users_paginated(0, 1)  # placeholder
            from storage.database import get_user
            t = get_user(target_uid)
            if t:
                new_ban = 0 if t["banned"] else 1
                update_user_field(target_uid, "banned", new_ban)
                await query.answer(f"{'Banned' if new_ban else 'Unbanned'} uid={target_uid}")
                log_admin_action(user_id, f"{'ban' if new_ban else 'unban'}", str(target_uid))

        case "search_user":
            context.user_data["admin_action"] = "search_user"
            caption = "🔍 Type user ID or username to search:"
            await show_section(query, context, "admin", caption, kb.kb_back_section("admin"))

        case _:
            await query.answer()


async def _do_broadcast(context, admin_id: int, message: str) -> None:
    """Background task: send broadcast to all setup users."""
    from storage.database import get_all_users_for_push
    users = get_all_users_for_push()
    sent = fail = 0
    for u in users:
        try:
            await context.bot.send_message(
                chat_id=u["user_id"],
                text=message,
                parse_mode=HTML,
            )
            sent += 1
            await asyncio.sleep(config.BROADCAST_DELAY)
        except Exception:
            fail += 1

    try:
        await context.bot.send_message(
            chat_id=admin_id,
            text=f"📣 <b>Broadcast Done</b>\n\nSent: {sent}\nFailed: {fail}",
            parse_mode=HTML,
        )
    except Exception:
        pass

    log_admin_action(admin_id, "broadcast_complete", f"sent={sent} fail={fail}")
    logger.info("Broadcast complete | sent=%d fail=%d", sent, fail)


async def admin_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not _is_admin(user_id):
        return

    action = context.user_data.get("admin_action")
    if not action:
        return

    text = update.message.text

    if action == "broadcast":
        context.user_data["broadcast_message"] = text
        context.user_data.pop("admin_action", None)
        preview = text[:200] + ("…" if len(text) > 200 else "")
        caption = (
            f"📣 <b>Broadcast Preview</b>\n\n{preview}\n\n"
            f"Send to <b>{total_users()}</b> users?"
        )
        await update.message.reply_text(caption, parse_mode=HTML, reply_markup=kb.kb_admin_confirm_broadcast())

    elif action == "announce":
        from storage.database import set_content
        set_content("announcement", text)
        context.user_data.pop("admin_action", None)
        await update.message.reply_text("✅ Announcement saved.", parse_mode=HTML)

    elif action == "search_user":
        context.user_data.pop("admin_action", None)
        results = search_users(text)
        if not results:
            await update.message.reply_text("❌ No users found.", parse_mode=HTML)
            return
        lines = [
            f"  <code>{r['user_id']}</code> {esc(r['full_name'] or r['username'] or '—')} | {r['level'] or '—'}"
            for r in results[:10]
        ]
        await update.message.reply_text(
            "🔍 <b>Search Results</b>\n\n" + "\n".join(lines),
            parse_mode=HTML,
        )


def get_admin_handlers() -> list:
    return [
        CallbackQueryHandler(admin_callback, pattern=r"^adm:"),
        MessageHandler(filters.TEXT & ~filters.COMMAND, admin_text_handler),
    ]
