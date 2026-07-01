"""
handlers/revision.py — Spaced Repetition Revision Handler
"""
import logging
from telegram.ext import CallbackQueryHandler, ContextTypes

import keyboards as kb
from media import show_section
from storage.database import (
    award_xp, get_due_revisions, get_user,
    log_event, mark_revision_done,
)
from utils.helpers import esc, progress_bar

logger = logging.getLogger(__name__)
HTML = "HTML"


async def show_revision(query, context: ContextTypes.DEFAULT_TYPE, user) -> None:
    """Show revision items due today."""
    user_id  = user["user_id"]
    day_num  = user["current_day"] or 1
    due_list = get_due_revisions(user_id, day_num)

    if not due_list:
        caption = (
            "🔄 <b>Revision — Spaced Repetition</b>\n\n"
            "✅ <b>No revisions due today!</b>\n\n"
            "Your revision schedule is clear. Keep completing daily tasks "
            "and revision entries will appear here automatically.\n\n"
            "💡 <i>Spaced repetition schedules each topic at the optimal time for memory consolidation.</i>"
        )
        await show_section(query, context, "revision", caption, kb.kb_revision(has_items=False))
        return

    items = []
    for rev in due_list[:10]:
        subject  = rev["subject"]  or "General"
        subtopic = rev["subtopic"] or "Review"
        due_day  = rev["due_day"]  or 0
        rid      = rev["id"]
        items.append(f"  • <b>Day {due_day}</b>: {esc(subject)} — {esc(subtopic)}")

    count = len(due_list)
    caption = (
        f"🔄 <b>Revision Due — Day {day_num}</b>\n\n"
        f"<b>{count} topic{'s' if count != 1 else ''} to revise today</b>\n\n"
        + "\n".join(items[:10]) +
        ("\n  <i>...and more</i>" if count > 10 else "") +
        "\n\n💡 Revising at the right time doubles retention. Don't skip!"
    )
    await show_section(query, context, "revision", caption, kb.kb_revision(has_items=True))


async def revision_callback(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle revision: callbacks."""
    query   = update.callback_query
    user_id = query.from_user.id
    data    = query.data
    parts   = data.split(":")

    user = get_user(user_id)
    if not user:
        await query.answer()
        return

    action = parts[1]

    match action:
        case "mark_all":
            due = get_due_revisions(user_id, user["current_day"] or 1)
            for rev in due:
                mark_revision_done(user_id, rev["id"])
            xp = award_xp(user_id, 30 * len(due), "Revision complete")
            await query.answer(f"✅ {len(due)} items revised! +{30*len(due)} XP")
            log_event(user_id, "revision_all_done")
            await show_revision(query, context, get_user(user_id))

        case "done":
            rid = int(parts[2])
            mark_revision_done(user_id, rid)
            award_xp(user_id, 30, "Single revision done")
            await query.answer("✅ Revised! +30 XP")
            await show_revision(query, context, get_user(user_id))

        case "skip":
            await query.answer("⏭️ Skipped for now")

        case "list":
            due = get_due_revisions(user_id, user["current_day"] or 1)
            lines = [
                f"{i+1}. {esc(r['subject'])} — {esc(r['subtopic'])} (Day {r['due_day']})"
                for i, r in enumerate(due[:15])
            ]
            caption = (
                "📋 <b>Full Revision List</b>\n\n" +
                "\n".join(lines) +
                f"\n\nTotal: {len(due)} items"
            )
            await show_section(query, context, "revision", caption, kb.kb_back_section("revision"))

        case _:
            await query.answer()


def get_revision_handlers() -> list:
    return [CallbackQueryHandler(revision_callback, pattern=r"^rev:")]
