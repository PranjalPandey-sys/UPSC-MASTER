# 🇮🇳 UPSC Master Bot v3

A production-grade Telegram bot for Civil Services exam preparation. Built for serious aspirants — 48 personalised study plans, AI-powered answer evaluation, streak tracking, and daily push notifications.

---

## Architecture Highlights

| Feature | Implementation |
|---|---|
| **Parallel image loading** | Images upload in background via `asyncio.create_task()` — text always appears instantly |
| **Caption-length safety** | Screens > 950 chars auto-route to plain-text messages; self-heals photo↔text transitions |
| **48 pre-generated plans** | All loaded at startup via `asyncio.gather()` — zero disk I/O per request |
| **Pre-generated reviews** | All 48 plan combinations have hardcoded reviews — zero AI call during onboarding |
| **PTB v20 immutability** | Uses `current_message` local variable, never reassigns `query.message` |
| **All AI has fallbacks** | Every Gemini call has a 15s timeout + hardcoded response; bot never crashes on AI failure |

---

## Quick Start

### 1. Clone and set up files

```bash
git clone <your-repo>
cd upsc-master-bot
```

Place the `plans/` folder (48 JSON files from `UPSC_MASTER_PLANS_v2.zip`) and the `images/` folder (12 PNG files) in the project root.

### 2. Environment Variables

Only **3 required** to start:

| Variable | Required | Description |
|---|---|---|
| `BOT_TOKEN` | ✅ | Your Telegram bot token from @BotFather |
| `GEMINI_API_KEY` | ✅ | Google Gemini API key (for AI features; fallbacks exist without it) |
| `ADMIN_IDS` | ✅ | Comma-separated Telegram user IDs: `123456,789012` |
| `GITHUB_TOKEN` | Optional | For automated DB backup to GitHub |
| `GITHUB_REPO` | Optional | e.g. `username/upsc-bot-backup` |

### 3. Local Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export BOT_TOKEN="your_token_here"
export GEMINI_API_KEY="your_key_here"
export ADMIN_IDS="your_telegram_id"

python bot.py
```

### 4. Deploy on Render

1. Push to GitHub
2. Create a **Web Service** on Render
3. Set **Python version to `3.11.9`** (critical — other versions have had issues)
4. Build command: `pip install -r requirements.txt`
5. Start command: `python bot.py`
6. Add a **Persistent Disk** at `/data` (1 GB) — stores the SQLite database
7. Add the 3 required environment variables
8. Deploy

`render.yaml` is pre-configured for this setup.

---

## Project Structure

```
upsc-master-bot/
├── bot.py                    # Entry point; Application builder + startup sequence
├── config.py                 # Single source of truth for all settings
├── keyboards.py              # All InlineKeyboardMarkup builders
├── media.py                  # Parallel image loading + caption-length safety
│
├── handlers/
│   ├── onboarding.py         # 5-step ConversationHandler + plan selection
│   ├── home.py               # Dashboard + nav:* callback dispatcher
│   ├── tasks.py              # Today's Mission (real schema: day_type, time_allocation_min, AI_hint…)
│   ├── revision.py           # Spaced repetition revision tracker
│   ├── answer_writing.py     # Mains answer evaluation (typed + handwritten photo)
│   ├── mock_test.py          # Subject MCQs + score tracking
│   ├── current_affairs.py    # CA digest + AI summaries
│   ├── essay.py              # Essay topic, outline, evaluation
│   ├── ethics.py             # Case studies + 7-step framework evaluation
│   ├── optional.py           # Optional subject strategy + resources
│   ├── progress.py           # Analytics dashboard
│   ├── streak.py             # XP, badges, leaderboard
│   ├── doubt.py              # AI planner / doubt solver
│   ├── timer.py              # Pomodoro / study timer
│   ├── settings.py           # Notifications, vacation, plan change
│   └── admin.py              # Admin panel: stats, broadcast, user management
│
├── services/
│   ├── plan_loader.py        # Async plan pre-warming (all 48 in parallel at startup)
│   ├── gemini.py             # Gemini AI with 15s timeouts + hardcoded fallbacks
│   ├── notifier.py           # APScheduler push notifications (morning/midday/evening/weekly)
│   └── backup.py             # GitHub DB backup service
│
├── storage/
│   └── database.py           # SQLite WAL-mode DB; full schema + all query functions
│
├── data/
│   ├── plan_reviews.py       # Pre-generated reviews for all 48 plan combinations
│   └── fallbacks.py          # All static content: MCQ bank, essay topics, ethics cases, CA sources
│
├── utils/
│   ├── logger.py             # Rotating file logger (5 MB, 3 backups)
│   ├── helpers.py            # Date utils, text formatters, XP/rank helpers, progress bars
│   └── ephemeral.py          # Auto-deleting message manager
│
├── plans/                    # 48 UPSC_MASTER_PLANS_v2 JSON files (not committed to git)
├── analysis/                 # plan_metadata.json, recommendations.json
├── images/                   # 12 section images (PNG)
├── logs/                     # Rotating logs (auto-created)
│
├── requirements.txt
└── render.yaml
```

---

## Plan JSON Schema (Real Fields)

The actual plan JSON structure differs significantly from naive assumptions. Key fields per daily task:

```json
{
  "task_id": "BEG_12M_6H_D001",
  "day": 1,
  "week": 1,
  "month": 1,
  "day_type": "STUDY",          // STUDY | REVISION | MOCK_TEST | MONTHLY_REVIEW
  "phase": "Foundation",
  "exam_phase": "Prelims+Mains",
  "subject": "History",
  "subtopic": "Ancient India — Indus Valley Civilisation",
  "gs_paper": "GS Paper I",
  "time_allocation_min": {
    "new_study": 180,
    "revision": 60,
    "answer_writing": 60,
    "current_affairs": 30,
    "optional": 0
  },
  "estimated_total_min": 360,
  "difficulty": "Medium",
  "priority": "High",
  "resources": ["NCERT Class 6 Our Pasts", "Spectrum Modern History Ch 1"],
  "dependencies": [],
  "revision_due": ["D0008", "D0015", "D0030"],
  "answer_writing_required": false,
  "PYQ_required": true,
  "completion_criteria": "Able to write 150-word answer on IVC features",
  "AI_hint": "Connect IVC urban planning with modern town planning questions",
  "current_affairs_integration": "Link to recent archaeological discoveries",
  "note": ""
}
```

`weekly_summaries` is a **dict** keyed `"Week_1"`, `"Week_2"`, etc. (not a list).

---

## Known Issues Fixed in v3

| Bug | Fix |
|---|---|
| `query.message = x` raises `AttributeError` in PTB v20 (immutable objects) | Uses `current_message` local variable throughout |
| Photo captions > 1024 chars silently fail (plan analysis, help, framework screens) | `CAPTION_SAFE_LIMIT = 950`; long screens auto-route to plain-text |
| Photo↔text state mismatch causes stuck screens | Self-healing: delete + resend fresh message when edit type conflicts |
| Plan JSON field names assumed incorrectly (`tasks`, `study_tip`, `pyqs`, `learning_goals`) | All task display rewritten to use real fields: `time_allocation_min`, `AI_hint`, `completion_criteria`, `PYQ_required`, etc. |
| `weekly_summaries` accessed as list | Fixed to dict lookup: `summaries.get("Week_N")` |
| Mock test `_end_test` referenced as method on `mock_callback` function | Extracted to standalone `_end_test_and_show_results()` helper |
| Callback data contained walrus operator (`:=`) inside import statement | Fixed to proper function definition |

---

## XP System

| Action | XP |
|---|---|
| Complete setup | +100 |
| Mark day done | +50 |
| 7-day streak milestone | +100 bonus |
| Write Mains answer | +20 |
| Handwritten answer | +25 |
| Mock test complete | +25 |
| Essay submitted | +30 |
| Ethics case evaluated | +25 |
| Ask AI doubt | +5 |
| CA summary viewed | +5 |
| All revision done | +30 per item |

**Ranks:** 🌱 Aspirant (0) → 📚 Scholar (500) → 🎯 Strategist (2000) → ⚔️ Warrior (5000) → 🏆 Topper (10000)

---

## Notifications Schedule (IST)

| Time | Notification |
|---|---|
| 09:00 | Morning motivation + today's task preview |
| 13:00 | Midday check-in (skips users who already completed the day) |
| 20:00 | Evening reminder + revision due count + UPSC trivia |
| Monday 06:00 | Weekly performance report (AI-generated, weekly stats) |

All notifications respect individual user preferences (`notify_morning`, `notify_midday`, `notify_evening`, `notify_weekly` flags in settings).

---

## Admin Panel

Access via `/admin` or the bot menu (admin IDs set in `ADMIN_IDS` env var).

- 📊 Platform stats (users, activity, DB size)
- 👥 User management (paginated list, search, ban/unban)
- 📣 Broadcast message to all users
- 🤖 AI cohort insights
- 🗃️ DB info + error log
- 🖼️ Clear image cache (if images appear broken)
- 💾 Manual GitHub backup

---

## Python Version

**Use Python 3.11.9 on Render.** Other versions (especially 3.12+) have caused deployment issues in past iterations of this project. The `render.yaml` specifies `pythonVersion: "3.11.9"` explicitly.
