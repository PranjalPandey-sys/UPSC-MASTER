"""
bot.py — UPSC Master Bot v3 Entry Point
=========================================
Production-grade startup sequence:
1. Logging
2. DB init + migration
3. Plan pre-warming (all 48 plans, async parallel)
4. Image cache pre-loading
5. Handler registration
6. Scheduler setup
7. Flask keep-alive thread
8. Polling start

Python 3.11.9 | python-telegram-bot 20.7
Deployed on Render — persistent disk at /data
"""
import asyncio
import logging
import os
import sys
import threading

from telegram import BotCommand, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ── Bootstrap logging FIRST ────────────────────────────────────────────────────
from utils.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

import config
from media import preload_image_cache
from storage.database import init_db, log_error
from services.plan_loader import pre_warm_all_plans, load_analysis_files


# ── Flask keep-alive (Render requires open port) ───────────────────────────────
def _start_flask() -> None:
    """Minimal Flask server to keep Render slot alive."""
    try:
        from flask import Flask
        app = Flask(__name__)

        @app.route("/")
        def health():
            return {"status": "ok", "service": "UPSC Master Bot v3"}, 200

        @app.route("/health")
        def health_check():
            return {"status": "healthy"}, 200

        app.run(host="0.0.0.0", port=config.PORT, debug=False, use_reloader=False)
    except ImportError:
        logger.warning("Flask not installed — skipping keep-alive server")
    except Exception as e:
        logger.error("Flask server failed: %s", e)


# ── Bot commands ───────────────────────────────────────────────────────────────
BOT_COMMANDS = [
    BotCommand("start",  "Start the bot / return to home"),
    BotCommand("help",   "Show help & feature guide"),
    BotCommand("reset",  "Change your study plan"),
    BotCommand("admin",  "Admin panel (admins only)"),
    BotCommand("cancel", "Cancel current action"),
]


# ── Error handler ──────────────────────────────────────────────────────────────
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log all errors. Never crash the bot."""
    import traceback
    user_id = 0
    try:
        if update and hasattr(update, "effective_user") and update.effective_user:
            user_id = update.effective_user.id
    except Exception:
        pass

    tb = "".join(traceback.format_exception(None, context.error, context.error.__traceback__))
    logger.error("Update %s caused error %s\n%s", update, context.error, tb)
    log_error("ERROR", "bot", "error_handler", str(context.error)[:500], tb[:1000], user_id)

    # Try to notify user
    try:
        if update and hasattr(update, "effective_chat") and update.effective_chat:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    "⚠️ <b>Something went wrong.</b>\n\n"
                    "The error has been logged. Please try again or use /start.\n"
                    "<i>If this keeps happening, tap the thumbs-down button to report.</i>"
                ),
                parse_mode="HTML",
            )
    except Exception:
        pass


# ── Admin command ──────────────────────────────────────────────────────────────
async def cmd_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Direct /admin command — shows admin panel."""
    user_id = update.effective_user.id
    if user_id not in config.ADMIN_IDS:
        await update.message.reply_text("⛔ Admin access only.", parse_mode="HTML")
        return

    from handlers.admin import show_admin
    from media import send_photo_message

    user_obj = update.effective_user
    caption  = (
        "🛡️ <b>Admin Panel</b>\n\n"
        f"Welcome, {user_obj.first_name}!\n"
        "Use the buttons below."
    )
    from keyboards import kb_admin
    await send_photo_message(context, update.effective_chat.id, "admin", caption, kb_admin())


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Direct /help command."""
    from data.fallbacks import HELP_TEXT
    from keyboards import kb_back_home
    from media import send_photo_message
    await send_photo_message(context, update.effective_chat.id, "help", HELP_TEXT, kb_back_home())


# ── Build the Application ──────────────────────────────────────────────────────
def build_application() -> Application:
    """Build and configure the PTB Application."""
    if not config.BOT_TOKEN:
        logger.critical("❌ BOT_TOKEN not set in environment! Exiting.")
        sys.exit(1)

    app = (
        Application.builder()
        .token(config.BOT_TOKEN)
        .read_timeout(30)
        .write_timeout(30)
        .connect_timeout(30)
        .pool_timeout(30)
        .build()
    )

    # ── Import all handlers ──────────────────────────────────────────────────

    # Onboarding ConversationHandler (MUST be first)
    from handlers.onboarding import get_onboarding_handler
    app.add_handler(get_onboarding_handler(), group=0)

    # Navigation dispatcher
    from handlers.home import get_nav_handler
    app.add_handler(get_nav_handler(), group=1)

    # Feature handlers
    from handlers.tasks         import get_tasks_handlers
    from handlers.revision      import get_revision_handlers
    from handlers.answer_writing import get_aw_handlers
    from handlers.mock_test     import get_mock_handlers
    from handlers.current_affairs import get_ca_handlers
    from handlers.essay         import get_essay_handlers
    from handlers.ethics        import get_ethics_handlers
    from handlers.optional      import get_optional_handlers
    from handlers.progress      import get_progress_handlers
    from handlers.streak        import get_streak_handlers
    from handlers.doubt         import get_doubt_handlers
    from handlers.timer         import get_timer_handlers
    from handlers.settings      import get_settings_handlers
    from handlers.admin         import get_admin_handlers

    for handler in get_tasks_handlers():
        app.add_handler(handler, group=2)
    for handler in get_revision_handlers():
        app.add_handler(handler, group=2)
    for handler in get_aw_handlers():
        app.add_handler(handler, group=2)
    for handler in get_mock_handlers():
        app.add_handler(handler, group=2)
    for handler in get_ca_handlers():
        app.add_handler(handler, group=2)
    for handler in get_essay_handlers():
        app.add_handler(handler, group=2)
    for handler in get_ethics_handlers():
        app.add_handler(handler, group=2)
    for handler in get_optional_handlers():
        app.add_handler(handler, group=2)
    for handler in get_progress_handlers():
        app.add_handler(handler, group=2)
    for handler in get_streak_handlers():
        app.add_handler(handler, group=2)
    for handler in get_doubt_handlers():
        app.add_handler(handler, group=2)
    for handler in get_timer_handlers():
        app.add_handler(handler, group=2)
    for handler in get_settings_handlers():
        app.add_handler(handler, group=2)
    for handler in get_admin_handlers():
        app.add_handler(handler, group=2)

    # Standalone commands
    app.add_handler(CommandHandler("help",   cmd_help),  group=3)
    app.add_handler(CommandHandler("admin",  cmd_admin), group=3)

    # Unknown callback fallback (prevents spinner on unhandled callbacks)
    async def fallback_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            await update.callback_query.answer("⏳ Processing…")
        except Exception:
            pass

    app.add_handler(CallbackQueryHandler(fallback_callback), group=99)

    # Global error handler
    app.add_error_handler(error_handler)

    return app


# ── Post-init: runs after Application is built but before polling ─────────────
async def post_init(application: Application) -> None:
    """
    Async startup: DB, plan pre-warming, image cache, scheduler, commands.
    This runs inside the existing event loop — no asyncio.run() needed.
    """
    logger.info("=" * 60)
    logger.info("UPSC Master Bot v3 — Starting up")
    logger.info("=" * 60)

    # 1. Database
    logger.info("1/6 Initialising database…")
    init_db()

    # 2. Pre-warm all 48 plan files (parallel async)
    logger.info("2/6 Pre-warming plan files…")
    loaded = await pre_warm_all_plans()
    await load_analysis_files()
    logger.info("   Plans loaded: %d/48", loaded)

    # 3. Image cache from DB
    logger.info("3/6 Loading image cache…")
    preload_image_cache()

    # 4. Scheduler
    logger.info("4/6 Registering notification schedules…")
    try:
        from services.notifier import register_all_schedules
        register_all_schedules(application.job_queue)
    except Exception as e:
        logger.warning("Scheduler registration failed (non-fatal): %s", e)

    # 5. Bot commands
    logger.info("5/6 Setting bot commands…")
    try:
        await application.bot.set_my_commands(BOT_COMMANDS)
    except Exception as e:
        logger.warning("set_my_commands failed (non-fatal): %s", e)

    # 6. Health check
    logger.info("6/6 Running health check…")
    try:
        me = await application.bot.get_me()
        logger.info("✅ Bot ready | @%s | Admins: %s", me.username, config.ADMIN_IDS)
    except Exception as e:
        logger.error("Health check failed: %s", e)

    logger.info("=" * 60)
    logger.info("🚀 Bot is live and polling!")
    logger.info("=" * 60)


# ── Main ───────────────────────────────────────────────────────────────────────
def main() -> None:
    """Entry point."""

    # Validate required env vars
    missing = []
    if not config.BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if not config.GEMINI_API_KEY:
        logger.warning("⚠️ GEMINI_API_KEY not set — AI features will use fallback responses only")

    if missing:
        logger.critical("❌ Missing required environment variables: %s", ", ".join(missing))
        sys.exit(1)

    # Start Flask keep-alive in background thread
    flask_thread = threading.Thread(target=_start_flask, daemon=True, name="flask-keepalive")
    flask_thread.start()
    logger.info("✅ Flask keep-alive thread started on port %d", config.PORT)

    # Build app
    app = build_application()
    app.post_init = post_init

    # Run with polling
    logger.info("Starting polling…")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        close_loop=False,
    )


if __name__ == "__main__":
    main()
