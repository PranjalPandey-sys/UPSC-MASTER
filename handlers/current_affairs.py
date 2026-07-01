"""
handlers/current_affairs.py — Current Affairs Handler
"""
import logging
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes, MessageHandler, filters

import keyboards as kb
from data.fallbacks import CA_FALLBACK, CA_SOURCES, CA_TOPICS
from media import show_section
from services.gemini import get_ca_summary
from storage.database import award_xp, log_event
from utils.helpers import esc

logger = logging.getLogger(__name__)
HTML = "HTML"


async def show_ca(query, context: ContextTypes.DEFAULT_TYPE, user) -> None:
    caption = (
        "📰 <b>Current Affairs</b>\n\n"
        "UPSC-focused daily digest — exam-relevant angles on today's news.\n\n"
        "Choose a topic for an AI-powered summary, or browse sources:\n\n"
        "💡 <i>30-40% of Prelims is current affairs. Don't skip this!</i>"
    )
    await show_section(query, context, "current_affairs", caption, kb.kb_ca())


async def ca_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query  = update.callback_query
    user_id= query.from_user.id
    parts  = query.data.split(":", 1)
    action = parts[1] if len(parts) > 1 else ""

    match action:
        case topic if topic in CA_TOPICS or topic not in ("full_digest", "sources", "topic_input"):
            # Topic summary request
            await query.answer("⏳ Generating summary…")
            summary = await get_ca_summary(topic)
            caption = (
                f"📰 <b>CA: {esc(topic)}</b>\n\n"
                f"{esc(summary)}\n\n"
                "<i>Source: AI summary from recent news. Always verify from primary sources.</i>"
            )
            await show_section(query, context, "current_affairs", caption, kb.kb_back_section("current_affairs"))
            award_xp(user_id, 5, "CA summary viewed")
            log_event(user_id, "ca_topic", topic)

        case "full_digest":
            caption = CA_FALLBACK + "\n\n<i>Tap a topic button for AI-powered exam-relevant summary.</i>"
            await show_section(query, context, "current_affairs", caption, kb.kb_back_section("current_affairs"))

        case "sources":
            src_text = "\n".join(CA_SOURCES)
            caption  = f"📚 <b>Recommended CA Sources</b>\n\n{src_text}\n\n" \
                       "<i>Combine: The Hindu + PIB + Vision IAS Monthly for complete coverage.</i>"
            await show_section(query, context, "current_affairs", caption, kb.kb_back_section("current_affairs"))

        case _:
            await query.answer()


def get_ca_handlers() -> list:
    return [CallbackQueryHandler(ca_callback, pattern=r"^ca:")]
