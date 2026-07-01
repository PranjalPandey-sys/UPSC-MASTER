"""
keyboards.py — UPSC Master Bot Keyboard Builders
=================================================
All InlineKeyboardMarkup builders in one place.
Callbacks are short strings (≤ 64 bytes enforced by Telegram).
"""
from telegram import InlineKeyboardButton as Btn
from telegram import InlineKeyboardMarkup as Markup

from config import LEVELS, TIMELINES, HOURS
from utils.helpers import level_emoji, timeline_label, hours_label


# ─────────────────────────────────────────────────────────────────────────────
# Onboarding keyboards
# ─────────────────────────────────────────────────────────────────────────────

def kb_select_level() -> Markup:
    """Onboarding Step 1: select preparation level."""
    return Markup([
        [Btn("🌱 Beginner",      callback_data="set_level:beginner")],
        [Btn("📘 Intermediate",  callback_data="set_level:intermediate")],
        [Btn("🚀 Advanced",      callback_data="set_level:advanced")],
    ])


def kb_select_timeline() -> Markup:
    """Onboarding Step 2: select preparation timeline."""
    return Markup([
        [Btn("⚡ 3 Months — Prelims Sprint",  callback_data="set_tl:3")],
        [Btn("📅 6 Months — Focused Prep",   callback_data="set_tl:6")],
        [Btn("📆 12 Months — Full Cycle",     callback_data="set_tl:12")],
        [Btn("🏁 24 Months — IAS Track",      callback_data="set_tl:24")],
    ])


def kb_select_hours() -> Markup:
    """Onboarding Step 3: select daily study hours."""
    return Markup([
        [Btn("⏱️ 2 hrs/day — Working Professional", callback_data="set_hrs:2")],
        [Btn("📖 4 hrs/day — Balanced Aspirant",    callback_data="set_hrs:4")],
        [Btn("📚 6 hrs/day — Dedicated Aspirant",   callback_data="set_hrs:6")],
        [Btn("🔥 8 hrs/day — Full-Time Aspirant",   callback_data="set_hrs:8")],
    ])


def kb_select_optional(current: str = "") -> Markup:
    """Onboarding Step 4: select optional subject (3 columns)."""
    subjects = [
        ("📜 History",             "History"),
        ("🌍 Geography",           "Geography"),
        ("⚖️ Public Admin",        "Public Administration"),
        ("💡 Pol Sci & IR",        "Political Science & IR"),
        ("📊 Sociology",           "Sociology"),
        ("💰 Economics",           "Economics"),
        ("🔬 Physics",             "Physics"),
        ("🧪 Chemistry",           "Chemistry"),
        ("🌱 Agriculture",         "Agriculture"),
        ("🦁 Zoology",             "Zoology"),
        ("⚡ Electrical Engg",     "Electrical Engineering"),
        ("💻 CS & IT",             "Computer Science"),
        ("⚙️ Mech Engg",           "Mechanical Engineering"),
        ("🏛️ Civil Engg",          "Civil Engineering"),
        ("📐 Mathematics",         "Mathematics"),
        ("🏥 Medical Science",     "Medical Science"),
        ("🌿 Botany",              "Botany"),
        ("📚 Philosophy",          "Philosophy"),
        ("🧠 Psychology",          "Psychology"),
        ("⚖️ Law",                 "Law"),
        ("✍️ Literature",          "Literature"),
        ("🤔 Undecided",           "Undecided"),
    ]
    rows = []
    row = []
    for label, val in subjects:
        mark = " ✓" if val == current else ""
        row.append(Btn(f"{label}{mark}", callback_data=f"set_opt:{val[:20]}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([Btn("✅ Confirm Selection", callback_data="confirm_opt")])
    return Markup(rows)


def kb_select_weak_subjects(current: list[str] | None = None) -> Markup:
    """Onboarding Step 5: select weak subjects (multi-select)."""
    current = current or []
    subjects = [
        ("📜 History",      "History"),
        ("🌍 Geography",    "Geography"),
        ("⚖️ Polity",       "Polity"),
        ("💰 Economy",      "Economy"),
        ("🌱 Environment",  "Environment"),
        ("🔬 S&T",          "Science & Technology"),
        ("🌐 IR",           "International Relations"),
        ("🤝 Ethics",       "Ethics & GS4"),
        ("📰 Current Aff",  "Current Affairs"),
        ("✍️ Ans Writing",  "Answer Writing"),
        ("📝 Essay",        "Essay"),
        ("🧮 CSAT",         "CSAT"),
    ]
    rows = []
    row = []
    for label, val in subjects:
        mark = " ✓" if val in current else ""
        row.append(Btn(f"{label}{mark}", callback_data=f"tog_weak:{val[:20]}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([Btn("✅ Done — Complete Setup", callback_data="confirm_weak")])
    return Markup(rows)


def kb_confirm_plan(plan_id: str) -> Markup:
    """Confirm plan selection after analysis."""
    return Markup([
        [Btn("✅ Start This Plan",      callback_data="confirm_plan")],
        [Btn("🔁 Choose Different Plan", callback_data="restart_onboarding")],
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Main Dashboard
# ─────────────────────────────────────────────────────────────────────────────

def kb_home(streak: int = 0, current_day: int = 1) -> Markup:
    """Main home screen keyboard."""
    fire = "🔥" * min(streak // 7 + 1, 3) if streak >= 7 else "✨"
    return Markup([
        [Btn("📚 Today's Mission", callback_data="nav:tasks"),
         Btn("🔄 Revision Due",   callback_data="nav:revision")],
        [Btn("✍️ Answer Writing", callback_data="nav:answer_writing"),
         Btn("🧪 Mock Test",      callback_data="nav:mock")],
        [Btn("📰 Current Affairs",callback_data="nav:current_affairs"),
         Btn("📝 Essay",          callback_data="nav:essay")],
        [Btn("⚖️ Ethics",         callback_data="nav:ethics"),
         Btn("🎯 Optional",       callback_data="nav:optional")],
        [Btn("📊 Progress",       callback_data="nav:progress"),
         Btn(f"{fire} Streak",    callback_data="nav:streak")],
        [Btn("🤖 AI Planner",     callback_data="nav:ai_planner"),
         Btn("⚙️ Settings",       callback_data="nav:settings")],
        [Btn("❓ Help",           callback_data="nav:help")],
    ])


def kb_back_home() -> Markup:
    """Simple back to home button."""
    return Markup([[Btn("🏠 Home", callback_data="nav:home")]])


def kb_back_section(section: str) -> Markup:
    """Back to a specific section + home."""
    return Markup([
        [Btn("◀ Back", callback_data=f"nav:{section}"),
         Btn("🏠 Home", callback_data="nav:home")],
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Today's Mission
# ─────────────────────────────────────────────────────────────────────────────

def kb_tasks(day: int, status: str = "pending") -> Markup:
    """Today's mission keyboard."""
    if status == "done":
        done_btn = Btn("✅ Completed!", callback_data="tasks:done_already")
    else:
        done_btn = Btn("✅ Mark Day Done", callback_data="tasks:mark_done")
    return Markup([
        [done_btn],
        [Btn("⏭️ Snooze to Tomorrow", callback_data="tasks:snooze"),
         Btn("🔍 See Details",         callback_data="tasks:details")],
        [Btn("📔 Add Note",    callback_data="tasks:note"),
         Btn("🔖 Bookmark",   callback_data="tasks:bookmark")],
        [Btn("⬅ Yesterday",  callback_data=f"tasks:prev:{day}"),
         Btn("➡ Tomorrow",   callback_data=f"tasks:next:{day}")],
        [Btn("🏠 Home",       callback_data="nav:home")],
    ])


def kb_task_done_celebration(day: int, streak: int) -> Markup:
    """Post-completion keyboard with XP and streak info."""
    return Markup([
        [Btn("📊 See Progress",  callback_data="nav:progress"),
         Btn("🔄 Revision Due", callback_data="nav:revision")],
        [Btn("📚 Next Day Preview", callback_data=f"tasks:next:{day}")],
        [Btn("🏠 Home",             callback_data="nav:home")],
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Revision
# ─────────────────────────────────────────────────────────────────────────────

def kb_revision(has_items: bool = True) -> Markup:
    """Revision section keyboard."""
    if has_items:
        return Markup([
            [Btn("✅ Mark All Revised",  callback_data="rev:mark_all"),
             Btn("📋 See Full List",      callback_data="rev:list")],
            [Btn("🔁 Set Next Revision",  callback_data="rev:reschedule")],
            [Btn("🏠 Home", callback_data="nav:home")],
        ])
    return Markup([
        [Btn("📚 Go to Today's Task", callback_data="nav:tasks")],
        [Btn("🏠 Home",              callback_data="nav:home")],
    ])


def kb_mark_revision(revision_id: int) -> Markup:
    """Mark single revision item as done."""
    return Markup([
        [Btn("✅ Revised", callback_data=f"rev:done:{revision_id}"),
         Btn("⏭️ Skip",   callback_data=f"rev:skip:{revision_id}")],
        [Btn("◀ Back",    callback_data="nav:revision")],
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Answer Writing
# ─────────────────────────────────────────────────────────────────────────────

def kb_answer_writing() -> Markup:
    """Answer writing section keyboard."""
    return Markup([
        [Btn("📝 GS1 Question",   callback_data="aw:gs1"),
         Btn("📝 GS2 Question",   callback_data="aw:gs2")],
        [Btn("📝 GS3 Question",   callback_data="aw:gs3"),
         Btn("📝 GS4 Ethics",     callback_data="aw:gs4")],
        [Btn("📊 My Answer History", callback_data="aw:history"),
         Btn("📸 Upload Photo",      callback_data="aw:photo")],
        [Btn("🏠 Home", callback_data="nav:home")],
    ])


def kb_after_answer_eval() -> Markup:
    """After answer evaluation keyboard."""
    return Markup([
        [Btn("✍️ Write Another",   callback_data="nav:answer_writing"),
         Btn("📊 My History",       callback_data="aw:history")],
        [Btn("🏠 Home", callback_data="nav:home")],
    ])


def kb_cancel_writing() -> Markup:
    return Markup([[Btn("❌ Cancel", callback_data="nav:answer_writing")]])


# ─────────────────────────────────────────────────────────────────────────────
# Mock Test
# ─────────────────────────────────────────────────────────────────────────────

def kb_mock_menu() -> Markup:
    """Mock test section keyboard."""
    return Markup([
        [Btn("📜 Polity MCQs",  callback_data="mock:Polity"),
         Btn("📜 History MCQs", callback_data="mock:History")],
        [Btn("🌍 Geography",    callback_data="mock:Geography"),
         Btn("💰 Economy",       callback_data="mock:Economy")],
        [Btn("🌱 Environment",  callback_data="mock:Environment"),
         Btn("🔬 S&T",           callback_data="mock:S&T")],
        [Btn("🎲 Mixed Prelims", callback_data="mock:Mixed"),
         Btn("📊 My Score Card",  callback_data="mock:scorecard")],
        [Btn("🏠 Home", callback_data="nav:home")],
    ])


def kb_mock_answer(question_idx: int, total: int) -> Markup:
    """Mock test answer options keyboard."""
    return Markup([
        [Btn("A", callback_data=f"mcq:{question_idx}:0"),
         Btn("B", callback_data=f"mcq:{question_idx}:1"),
         Btn("C", callback_data=f"mcq:{question_idx}:2"),
         Btn("D", callback_data=f"mcq:{question_idx}:3")],
        [Btn("❌ End Test", callback_data="mock:end")],
    ])


def kb_after_mock() -> Markup:
    return Markup([
        [Btn("🔁 Try Another", callback_data="nav:mock"),
         Btn("📊 Score Card",  callback_data="mock:scorecard")],
        [Btn("🏠 Home", callback_data="nav:home")],
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Current Affairs
# ─────────────────────────────────────────────────────────────────────────────

def kb_ca() -> Markup:
    """Current affairs section keyboard."""
    return Markup([
        [Btn("💰 Economy",    callback_data="ca:Economy"),
         Btn("🌱 Environment", callback_data="ca:Environment")],
        [Btn("🌐 IR",          callback_data="ca:International Relations"),
         Btn("⚖️ Polity",      callback_data="ca:Polity & Governance")],
        [Btn("🔬 S&T",         callback_data="ca:Science & Technology"),
         Btn("🤝 Social",      callback_data="ca:Social Issues")],
        [Btn("🛡️ Security",    callback_data="ca:Security & Defence"),
         Btn("🌾 Agriculture", callback_data="ca:Agriculture")],
        [Btn("📰 Full Digest", callback_data="ca:full_digest"),
         Btn("📚 CA Sources",  callback_data="ca:sources")],
        [Btn("🏠 Home", callback_data="nav:home")],
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Essay
# ─────────────────────────────────────────────────────────────────────────────

def kb_essay() -> Markup:
    """Essay section keyboard."""
    return Markup([
        [Btn("💡 Get Topic",       callback_data="essay:topic"),
         Btn("📋 Get Outline",     callback_data="essay:outline")],
        [Btn("✍️ Submit Essay",    callback_data="essay:submit"),
         Btn("📊 My Essays",       callback_data="essay:history")],
        [Btn("📖 Essay Tips",      callback_data="essay:tips")],
        [Btn("🏠 Home", callback_data="nav:home")],
    ])


def kb_essay_after() -> Markup:
    return Markup([
        [Btn("✍️ Write Another", callback_data="nav:essay"),
         Btn("📊 History",       callback_data="essay:history")],
        [Btn("🏠 Home", callback_data="nav:home")],
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Ethics
# ─────────────────────────────────────────────────────────────────────────────

def kb_ethics() -> Markup:
    """Ethics section keyboard."""
    return Markup([
        [Btn("📋 Case Study",       callback_data="ethics:case"),
         Btn("✍️ Submit Analysis",  callback_data="ethics:submit")],
        [Btn("📖 7-Step Framework", callback_data="ethics:framework"),
         Btn("🧠 Key Thinkers",     callback_data="ethics:thinkers")],
        [Btn("📊 My Performance",   callback_data="ethics:history")],
        [Btn("🏠 Home", callback_data="nav:home")],
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Optional
# ─────────────────────────────────────────────────────────────────────────────

def kb_optional() -> Markup:
    """Optional subject section keyboard."""
    return Markup([
        [Btn("📅 Today's Optional Task", callback_data="opt:today"),
         Btn("📚 Resources",             callback_data="opt:resources")],
        [Btn("📊 Coverage Tracker",      callback_data="opt:tracker"),
         Btn("✍️ Answer Practice",       callback_data="opt:answer")],
        [Btn("🏠 Home", callback_data="nav:home")],
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Progress
# ─────────────────────────────────────────────────────────────────────────────

def kb_progress() -> Markup:
    """Progress section keyboard."""
    return Markup([
        [Btn("📊 Subject Coverage",   callback_data="prog:subjects"),
         Btn("📈 Weekly Report",      callback_data="prog:weekly")],
        [Btn("🧪 Mock Scores",        callback_data="prog:mocks"),
         Btn("✍️ Answer Stats",       callback_data="prog:answers")],
        [Btn("🎖️ My Badges",         callback_data="prog:badges"),
         Btn("📉 Weak Areas",         callback_data="prog:weak")],
        [Btn("🏠 Home", callback_data="nav:home")],
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Streak
# ─────────────────────────────────────────────────────────────────────────────

def kb_streak(streak: int = 0, xp: int = 0) -> Markup:
    """Streak section keyboard."""
    return Markup([
        [Btn("🏆 Leaderboard",    callback_data="streak:leaderboard"),
         Btn("🎖️ Badges",         callback_data="streak:badges")],
        [Btn("🛡️ Streak Shields", callback_data="streak:shields"),
         Btn("📊 XP History",     callback_data="streak:xp_log")],
        [Btn("🏠 Home", callback_data="nav:home")],
    ])


# ─────────────────────────────────────────────────────────────────────────────
# AI Planner / Doubt
# ─────────────────────────────────────────────────────────────────────────────

def kb_ai_planner() -> Markup:
    """AI Planner section keyboard."""
    return Markup([
        [Btn("❓ Ask a Doubt",        callback_data="ai:doubt"),
         Btn("📋 Flash Questions",    callback_data="ai:flashcard")],
        [Btn("📰 CA Summary",         callback_data="ai:ca"),
         Btn("📊 Plan Analysis",      callback_data="ai:analysis")],
        [Btn("🏠 Home", callback_data="nav:home")],
    ])


def kb_cancel_doubt() -> Markup:
    return Markup([[Btn("❌ Cancel", callback_data="nav:ai_planner")]])


# ─────────────────────────────────────────────────────────────────────────────
# Settings
# ─────────────────────────────────────────────────────────────────────────────

def kb_settings(user) -> Markup:
    """Settings section keyboard (user is a sqlite3.Row)."""
    # Toggle labels
    morn  = "🔔" if user["notify_morning"] else "🔕"
    mid   = "🔔" if user["notify_midday"]  else "🔕"
    eve   = "🔔" if user["notify_evening"] else "🔕"
    vac   = "🏖️ ON" if user["vacation_mode"] else "✈️ OFF"
    board = "🏆 ON" if user["leaderboard_opt"] else "🙈 OFF"
    return Markup([
        [Btn(f"{morn} Morning Notif ({user['notify_morning_t']})", callback_data="set:notif_morn")],
        [Btn(f"{mid} Midday Notif ({user['notify_midday_t']})",   callback_data="set:notif_mid")],
        [Btn(f"{eve} Evening Notif ({user['notify_evening_t']})", callback_data="set:notif_eve")],
        [Btn(f"🏖️ Vacation Mode: {vac}",       callback_data="set:vacation"),
         Btn(f"🏆 Leaderboard: {board}",        callback_data="set:leaderboard")],
        [Btn("🔁 Change Study Plan",            callback_data="set:change_plan")],
        [Btn("📅 Set Exam Date",                callback_data="set:exam_date")],
        [Btn("🗑️ Delete My Data",               callback_data="set:delete_data")],
        [Btn("🏠 Home", callback_data="nav:home")],
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Admin Panel
# ─────────────────────────────────────────────────────────────────────────────

def kb_admin() -> Markup:
    """Admin panel keyboard."""
    return Markup([
        [Btn("📊 Stats",          callback_data="adm:stats"),
         Btn("👥 Users",          callback_data="adm:users")],
        [Btn("📣 Broadcast",      callback_data="adm:broadcast"),
         Btn("🤖 AI Insights",    callback_data="adm:ai_insights")],
        [Btn("🗃️ DB Info",        callback_data="adm:db_info"),
         Btn("🚨 Error Log",      callback_data="adm:errors")],
        [Btn("🖼️ Clear Img Cache", callback_data="adm:clear_cache"),
         Btn("💾 Backup Now",      callback_data="adm:backup")],
        [Btn("📢 Announcement",   callback_data="adm:announce")],
        [Btn("🏠 Home", callback_data="nav:home")],
    ])


def kb_admin_confirm_broadcast() -> Markup:
    return Markup([
        [Btn("✅ Confirm Send",  callback_data="adm:bc_confirm"),
         Btn("❌ Cancel",        callback_data="adm:broadcast")],
    ])


def kb_admin_user(user_id: int, banned: bool) -> Markup:
    """Admin single-user actions keyboard."""
    ban_label = "✅ Unban" if banned else "🚫 Ban"
    return Markup([
        [Btn(ban_label,               callback_data=f"adm:ban:{user_id}"),
         Btn("📩 Message User",       callback_data=f"adm:msg:{user_id}")],
        [Btn("📊 User Stats",         callback_data=f"adm:ustats:{user_id}"),
         Btn("🗑️ Reset User",         callback_data=f"adm:reset:{user_id}")],
        [Btn("◀ Back to Users",      callback_data="adm:users")],
    ])


def kb_admin_users_nav(offset: int, total: int, page_size: int = 15) -> Markup:
    """Pagination keyboard for admin user list."""
    rows = []
    nav = []
    if offset > 0:
        nav.append(Btn("◀ Prev", callback_data=f"adm:users:{offset - page_size}"))
    if offset + page_size < total:
        nav.append(Btn("Next ▶", callback_data=f"adm:users:{offset + page_size}"))
    if nav:
        rows.append(nav)
    rows.append([Btn("◀ Admin Panel", callback_data="nav:admin")])
    return Markup(rows)


def kb_admin_search() -> Markup:
    return Markup([
        [Btn("🔍 Search by ID/Username", callback_data="adm:search_user")],
        [Btn("◀ Admin Panel", callback_data="nav:admin")],
    ])


# ─────────────────────────────────────────────────────────────────────────────
# Analysis / Plan review (shown during onboarding after plan chosen)
# ─────────────────────────────────────────────────────────────────────────────

def kb_plan_analysis(show_better: bool = False) -> Markup:
    """Plan analysis keyboard — shown after onboarding combo selected."""
    rows = [
        [Btn("✅ Confirm & Start Plan", callback_data="ob:confirm")],
    ]
    if show_better:
        rows.append([Btn("⬆️ See Better Suggestion", callback_data="ob:better")])
    rows.append([Btn("🔁 Choose Different", callback_data="ob:restart")])
    return Markup(rows)


# ─────────────────────────────────────────────────────────────────────────────
# Utility keyboards
# ─────────────────────────────────────────────────────────────────────────────

def kb_yes_no(yes_cb: str, no_cb: str) -> Markup:
    return Markup([[Btn("✅ Yes", callback_data=yes_cb), Btn("❌ No", callback_data=no_cb)]])


def kb_confirm_delete() -> Markup:
    return Markup([
        [Btn("⚠️ Yes, Delete Everything", callback_data="set:confirm_delete")],
        [Btn("❌ Cancel",                  callback_data="nav:settings")],
    ])


def kb_vacation_duration() -> Markup:
    return Markup([
        [Btn("1 Day",  callback_data="vac:1"),  Btn("3 Days", callback_data="vac:3")],
        [Btn("5 Days", callback_data="vac:5"),  Btn("7 Days", callback_data="vac:7")],
        [Btn("14 Days",callback_data="vac:14"), Btn("30 Days",callback_data="vac:30")],
        [Btn("❌ Cancel", callback_data="nav:settings")],
    ])


def kb_timer() -> Markup:
    """Timer / Pomodoro section keyboard."""
    return Markup([
        [Btn("⏱ 25 min Pomodoro",  callback_data="timer:25"),
         Btn("⏱ 45 min Session",   callback_data="timer:45")],
        [Btn("⏱ 60 min Session",   callback_data="timer:60"),
         Btn("⏱ 90 min Session",   callback_data="timer:90")],
        [Btn("⏹ Stop Timer",        callback_data="timer:stop")],
        [Btn("🏠 Home",             callback_data="nav:home")],
    ])
