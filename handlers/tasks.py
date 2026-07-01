"""
handlers/tasks.py — Today's Mission Handler
============================================
Shows today's study tasks from the plan JSON.
Handles: mark done, snooze, note, bookmark, prev/next day navigation.
"""
import json
import logging
from datetime import date, timedelta

from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes, MessageHandler, filters

import keyboards as kb
from media import show_section
from services import plan_loader
from storage.database import (
    award_xp, count_completed_days, get_user, grant_badge,
    log_event, mark_day_done, save_revision_entries,
    update_streak, update_user_field,
)
from utils.helpers import (
    bold, compact_bar, days_remaining_label, esc, get_motivation,
    level_emoji, phase_display, progress_bar, streak_emoji,
)

logger = logging.getLogger(__name__)
HTML  = "HTML"


def _build_plan_id(user) -> str:
    return f"{user['level']}_{user['timeline_months']}months_{int(user['hours_per_day'])}hours"


async def show_tasks(query, context: ContextTypes.DEFAULT_TYPE, user) -> None:
    """Display today's mission card."""
    user_id = user["user_id"]
    day_num = user["current_day"] or 1
    pid     = _build_plan_id(user)
    status  = user.get("last_done_date", "") == str(date.today())

    task = plan_loader.get_day_task(pid, day_num)
    if not task:
        caption = (
            "📚 <b>Today's Mission</b>\n\n"
            "⚠️ No task found for today. Your plan may have ended or is loading.\n\n"
            "Try /start to refresh."
        )
        await show_section(query, context, "tasks", caption, kb.kb_back_home())
        return

    caption = _format_task_card(task, day_num, user, status)
    done_status = "done" if status else "pending"
    await show_section(query, context, "tasks", caption, kb.kb_tasks(day_num, done_status))


DAY_TYPE_HEADER = {
    "STUDY":          ("📚", "Today's Mission"),
    "REVISION":       ("🔄", "Revision Day"),
    "MOCK_TEST":      ("🧪", "Mock Test Day"),
    "MONTHLY_REVIEW": ("📊", "Monthly Review"),
}

DIFFICULTY_BADGE = {"Low": "🟢 Low", "Medium": "🟡 Medium", "High": "🔴 High"}
PRIORITY_BADGE   = {"Low": "Low", "Medium": "Medium", "High": "⭐ High"}


def _format_task_card(task: dict, day_num: int, user, done_today: bool) -> str:
    """
    Format the task card text using the REAL plan JSON schema:
    task_id, day, week, month, day_type, phase, exam_phase, subject, subtopic,
    gs_paper, time_allocation_min{}, estimated_total_min, difficulty, priority,
    resources[], dependencies[], revision_due[], answer_writing_required,
    PYQ_required, completion_criteria, AI_hint, current_affairs_integration, note.
    There is no "tasks" list or "study_tip" key in the actual data — those are
    derived here from the real fields instead.
    """
    subject   = task.get("subject", "—").replace("_", " ")
    subtopic  = task.get("subtopic", "—")
    phase     = task.get("phase", "Foundation")
    gs_paper  = task.get("gs_paper", "")
    day_type  = task.get("day_type", "STUDY")
    difficulty= task.get("difficulty", "")
    priority  = task.get("priority", "")
    total_min = task.get("estimated_total_min", 0)
    alloc     = task.get("time_allocation_min", {}) or {}
    resources = task.get("resources", [])
    rev_due   = task.get("revision_due", [])
    hint      = task.get("AI_hint", "")
    criteria  = task.get("completion_criteria", "")
    ca_link   = task.get("current_affairs_integration", "")
    aw_req    = task.get("answer_writing_required", False)
    pyq_req   = task.get("PYQ_required", False)
    note      = task.get("note", "")

    icon, header = DAY_TYPE_HEADER.get(day_type, ("📚", "Today's Mission"))

    total = plan_loader.get_plan_length(_build_plan_id(user))
    pct   = round(day_num / total * 100, 1) if total else 0
    bar   = progress_bar(pct, 8)
    hrs   = round(total_min / 60, 1) if total_min else (user["hours_per_day"] or 4)

    done_indicator = "✅ <b>COMPLETED TODAY</b>\n\n" if done_today else ""

    # Time allocation breakdown (only show non-zero entries)
    alloc_labels = {
        "new_study": "📘 New study", "revision": "🔄 Revision",
        "answer_writing": "✍️ Answer writing", "current_affairs": "📰 Current affairs",
        "optional": "🎯 Optional", "mock_test": "🧪 Mock test",
    }
    alloc_lines = [
        f"  {alloc_labels.get(k, k)}: {v} min"
        for k, v in alloc.items() if v
    ]
    alloc_text = "\n".join(alloc_lines) if alloc_lines else f"  📘 Focused study: {total_min} min"

    rev_text = ""
    if rev_due:
        rev_days = ", ".join(str(int(str(r).replace("D", "").lstrip("0") or "0")) for r in rev_due[:3])
        rev_text = f"\n🔄 <b>Revision scheduled:</b> Day {rev_days}"

    action_flags = []
    if aw_req:
        action_flags.append("✍️ Answer writing required today")
    if pyq_req:
        action_flags.append("❓ PYQ practice required today")
    flags_text = ("\n" + "\n".join(f"  • {f}" for f in action_flags)) if action_flags else ""

    note_text = f"\n\n💬 <i>{esc(note)}</i>" if note else ""
    hint_text = f"\n\n💡 <b>AI Hint:</b> <i>{esc(hint)}</i>" if hint else ""
    goal_text = f"\n\n🎯 <b>Completion Goal:</b> {esc(criteria)}" if criteria else ""
    ca_text   = f"\n📰 <b>CA Link:</b> {esc(ca_link)}" if ca_link else ""

    badge_line = ""
    if difficulty or priority:
        d_badge = DIFFICULTY_BADGE.get(difficulty, difficulty)
        p_badge = PRIORITY_BADGE.get(priority, priority)
        badge_line = f"<i>Difficulty: {esc(d_badge)}  |  Priority: {esc(p_badge)}</i>\n"

    res_text = ""
    if resources:
        res_text = "\n\n<b>📚 Resources:</b>\n" + "\n".join(f"  📖 {esc(r)}" for r in resources[:4])

    return (
        f"{done_indicator}"
        f"{icon} <b>Day {day_num} — {header}</b>\n"
        f"{bar} {pct:.0f}% through plan\n"
        f"{badge_line}\n"
        f"<b>📌 {phase_display(phase)}</b>"
        f"{f'  |  <b>{esc(gs_paper)}</b>' if gs_paper else ''}\n\n"
        f"<b>Subject:</b> {esc(subject)}\n"
        f"<b>Topic:</b> {esc(subtopic)}\n"
        f"<b>Duration:</b> ~{hrs}h ({total_min} min)\n\n"
        f"<b>⏱️ Time Breakdown:</b>\n{alloc_text}"
        f"{flags_text}"
        f"{res_text}"
        f"{goal_text}"
        f"{ca_text}"
        f"{rev_text}"
        f"{hint_text}"
        f"{note_text}"
    )


async def tasks_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle all tasks: callbacks."""
    query   = update.callback_query
    user_id = query.from_user.id
    data    = query.data  # "tasks:mark_done" | "tasks:snooze" | etc.
    action  = data.split(":")[1]

    user = get_user(user_id)
    if not user:
        await query.answer("User not found. Please /start again.")
        return

    day_num = user["current_day"] or 1
    pid     = _build_plan_id(user)

    match action:
        case "mark_done":
            await _mark_done(query, context, user, pid, day_num)

        case "done_already":
            await query.answer("✅ You've already completed today! Come back tomorrow.", show_alert=True)

        case "snooze":
            mark_day_done(user_id, day_num, "main", "snoozed")
            await query.answer("⏭️ Snoozed to tomorrow!")
            next_day = day_num + 1
            update_user_field(user_id, "current_day", next_day)
            # Re-show tasks for next day
            user_fresh = get_user(user_id)
            await show_tasks(query, context, user_fresh)

        case "details":
            task = plan_loader.get_day_task(pid, day_num)
            if task:
                await _show_task_details(query, context, task, day_num)
            else:
                await query.answer("No details available.")

        case "note":
            context.user_data["waiting_for"] = "task_note"
            context.user_data["note_day"]    = day_num
            caption = "📔 <b>Add Note</b>\n\nType your note for today's task:"
            await show_section(query, context, "tasks", caption, kb.kb_cancel_writing())

        case "bookmark":
            task = plan_loader.get_day_task(pid, day_num)
            if task:
                from storage.database import add_bookmark
                add_bookmark(user_id, "task", f"D{day_num:04d}", task.get("subtopic", ""))
                await query.answer("🔖 Bookmarked!")
            else:
                await query.answer("Nothing to bookmark.")

        case "prev":
            prev_day = max(1, day_num - 1)
            task = plan_loader.get_day_task(pid, prev_day)
            if task:
                caption = _format_task_card(task, prev_day, user, False)
                await show_section(query, context, "tasks", caption, kb.kb_tasks(prev_day))
            else:
                await query.answer("No previous task.")

        case "next":
            next_day = day_num + 1
            total    = plan_loader.get_plan_length(pid)
            if next_day > total:
                await query.answer("🎉 You've reached the end of the plan!", show_alert=True)
                return
            task = plan_loader.get_day_task(pid, next_day)
            if task:
                caption = _format_task_card(task, next_day, user, False)
                await show_section(query, context, "tasks", caption, kb.kb_tasks(next_day))
            else:
                await query.answer("No next task available.")

        case _:
            await query.answer()


async def _mark_done(query, context, user, pid, day_num) -> None:
    """Mark today's task done, update streak and XP, show celebration."""
    user_id = user["user_id"]

    # Already done today?
    today = str(date.today())
    if user.get("last_done_date") == today:
        await query.answer("✅ Already marked done today!", show_alert=True)
        return

    # Mark in DB
    mark_day_done(user_id, day_num, "main", "done")
    update_user_field(user_id, "current_day", day_num + 1)

    # Schedule revision entries
    task = plan_loader.get_day_task(pid, day_num)
    if task and task.get("revision_due"):
        save_revision_entries(user_id, task, day_num)

    # Update streak
    new_streak, milestone = update_streak(user_id)

    # Award XP
    xp_earned = 50
    if new_streak % 7 == 0 and new_streak > 0:
        xp_earned += 100  # Streak milestone bonus
    new_xp = award_xp(user_id, xp_earned, f"Day {day_num} complete")

    # Badges
    completed = count_completed_days(user_id)
    if completed == 1:   grant_badge(user_id, "first_day")
    if completed == 7:   grant_badge(user_id, "week_warrior")
    if completed == 30:  grant_badge(user_id, "month_master")
    if completed == 100: grant_badge(user_id, "century")
    if new_streak == 7:  grant_badge(user_id, "streak_7")
    if new_streak == 30: grant_badge(user_id, "streak_30")

    from utils.helpers import get_rank, xp_to_next_rank
    rank = get_rank(new_xp)
    s_e  = streak_emoji(new_streak)

    milestone_text = ""
    if milestone:
        milestone_text = f"\n🎉 <b>{new_streak}-day streak milestone!</b> +100 bonus XP!"

    # Preview tomorrow
    tomorrow_task = plan_loader.get_day_task(pid, day_num + 1)
    tomorrow_preview = ""
    if tomorrow_task:
        tomorrow_preview = (
            f"\n\n<b>📅 Tomorrow (Day {day_num + 1}):</b>\n"
            f"  {esc(tomorrow_task.get('subject', ''))}: "
            f"{esc(tomorrow_task.get('subtopic', ''))}"
        )

    caption = (
        f"✅ <b>Day {day_num} Complete!</b>{milestone_text}\n\n"
        f"<b>{s_e} Streak:</b> {new_streak} days\n"
        f"<b>⚡ XP:</b> +{xp_earned} → {new_xp:,} total\n"
        f"<b>🎖️ Rank:</b> {rank}"
        f"{tomorrow_preview}\n\n"
        f"<i>{esc(get_motivation(user_id, day_num))}</i>"
    )
    await show_section(query, context, "tasks", caption, kb.kb_task_done_celebration(day_num, new_streak))

    log_event(user_id, "task_done", f"day={day_num}")


async def _show_task_details(query, context, task: dict, day_num: int) -> None:
    """
    Show expanded task details using the REAL schema fields:
    resources[], dependencies[], completion_criteria (string), AI_hint,
    current_affairs_integration, PYQ_required (bool), answer_writing_required (bool).
    """
    subject   = task.get("subject", "—").replace("_", " ")
    subtopic  = task.get("subtopic", "—")
    resources = task.get("resources", [])
    deps      = task.get("dependencies", [])
    criteria  = task.get("completion_criteria", "")
    hint      = task.get("AI_hint", "")
    ca_link   = task.get("current_affairs_integration", "")
    pyq_req   = task.get("PYQ_required", False)
    aw_req    = task.get("answer_writing_required", False)
    task_id   = task.get("task_id", "")

    res_text = "\n".join(f"  📖 {esc(r)}" for r in resources[:6]) if resources else "  • See plan books list"

    pyq_text = (
        "  ❓ PYQ practice required today — pull 3-5 previous year questions on this topic"
        if pyq_req else "  • Optional: attempt a few PYQs if time allows"
    )
    aw_text = (
        "  ✍️ Answer writing required today — head to the Answer Writing section"
        if aw_req else ""
    )

    dep_text = ""
    if deps:
        dep_text = f"\n\n<b>🔗 Builds on:</b> {esc(', '.join(str(d) for d in deps[:3]))}"

    caption = (
        f"🔍 <b>Day {day_num} — Full Details</b>\n\n"
        f"<b>Subject:</b> {esc(subject)}\n"
        f"<b>Topic:</b> {esc(subtopic)}\n"
        f"<code>{esc(task_id)}</code>\n\n"
        f"<b>📚 Recommended Resources:</b>\n{res_text}\n\n"
        f"<b>❓ PYQ Focus:</b>\n{pyq_text}\n"
        f"{f'{aw_text}{chr(10)}' if aw_text else ''}"
        f"{f'{chr(10)}<b>🎯 Completion Goal:</b>{chr(10)}  {esc(criteria)}{chr(10)}' if criteria else ''}"
        f"{f'{chr(10)}<b>💡 AI Hint:</b>{chr(10)}  <i>{esc(hint)}</i>{chr(10)}' if hint else ''}"
        f"{f'{chr(10)}<b>📰 Current Affairs Link:</b>{chr(10)}  {esc(ca_link)}' if ca_link else ''}"
        f"{dep_text}"
    )
    await show_section(query, context, "tasks", caption, kb.kb_back_section("tasks"))


async def tasks_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text input while in tasks note mode."""
    if context.user_data.get("waiting_for") != "task_note":
        return

    user_id  = update.effective_user.id
    note_day = context.user_data.pop("note_day", 1)
    context.user_data.pop("waiting_for", None)
    note_text= update.message.text[:500]

    user = get_user(user_id)
    if user:
        from storage.database import save_note
        save_note(user_id, note_day, user["level"], note_text)
        await update.message.reply_text(
            f"📔 Note saved for Day {note_day}!\n\n<code>{esc(note_text)}</code>",
            parse_mode=HTML,
        )
    log_event(user_id, "note_saved", f"day={note_day}")


def get_tasks_handlers() -> list:
    return [
        CallbackQueryHandler(tasks_callback, pattern=r"^tasks:"),
        MessageHandler(filters.TEXT & ~filters.COMMAND, tasks_text_handler),
    ]
