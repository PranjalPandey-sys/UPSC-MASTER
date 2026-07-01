"""
config.py — UPSC Master Bot v3 Configuration
===============================================
Single source of truth for all settings.
All secrets via environment variables only.
Python 3.11.9 | python-telegram-bot v20.7
"""
import os
import pathlib
import logging

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR:     pathlib.Path = pathlib.Path(__file__).parent
IMAGES_DIR:   pathlib.Path = BASE_DIR / "images"
PLANS_DIR:    pathlib.Path = BASE_DIR / "plans"
ANALYSIS_DIR: pathlib.Path = BASE_DIR / "analysis"
LOGS_DIR:     pathlib.Path = BASE_DIR / "logs"

# Database path: Render Persistent Disk at /data, fallback to local ./data
_DATA_DIR = pathlib.Path("/data") if pathlib.Path("/data").exists() else BASE_DIR / "data"
_DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH: str = str(_DATA_DIR / "upsc_bot.db")

# Logs dir
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ── Telegram ───────────────────────────────────────────────────────────────────
BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")

# Multiple admin Telegram user IDs (comma-separated in env: "123456,789012")
ADMIN_IDS: list[int] = [
    int(x.strip())
    for x in os.environ.get("ADMIN_IDS", "").split(",")
    if x.strip().isdigit()
]

# ── Gemini AI ──────────────────────────────────────────────────────────────────
# Uses OpenAI-compatible endpoint for gemini-2.0-flash
GEMINI_API_KEY:  str = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL:    str = "gemini-2.0-flash"
GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
GEMINI_TIMEOUT:  int = 15   # seconds per call

# ── GitHub Backup (optional) ───────────────────────────────────────────────────
GITHUB_TOKEN: str = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO:  str = os.environ.get("GITHUB_REPO", "")  # e.g. username/repo-name

# ── Flask keep-alive ───────────────────────────────────────────────────────────
PORT: int = int(os.environ.get("PORT", 8080))

# ── Logging ────────────────────────────────────────────────────────────────────
LOG_LEVEL: int = logging.INFO

# ── Plan structure ────────────────────────────────────────────────────────────
LEVELS:    list[str] = ["beginner", "intermediate", "advanced"]
TIMELINES: list[int] = [3, 6, 12, 24]
HOURS:     list[int] = [2, 4, 6, 8]

# ── Image file mapping ────────────────────────────────────────────────────────
# Maps logical image keys to actual filenames in images/ folder
IMAGE_FILES: dict[str, str] = {
    "hero":            "welcome.png",
    "home":            "home.png",
    "tasks":           "tasks.png",
    "revision":        "revison.png",    # note: actual file has typo 'revison'
    "answer_writing":  "tasks.png",      # reuse tasks image if dedicated missing
    "mock":            "mock.png",
    "current_affairs": "current_affairs.png",
    "essay":           "tasks.png",
    "ethics":          "ai_planner.png",
    "optional":        "plan.png",
    "progress":        "progress.png",
    "streak":          "earn.png",
    "ai_planner":      "ai_planner.png",
    "plan":            "plan.png",
    "timer":           "tasks.png",
    "settings":        "settings.png",
    "help":            "ai_planner.png",
    "admin":           "home.png",
    "motivation":      "motivation.png",
    "onboarding":      "welcome.png",
    "analysis":        "progress.png",
}

# Runtime file_id cache (key -> Telegram file_id string)
# Populated after first upload; persisted in DB image_cache table
IMAGE_CACHE: dict[str, str] = {}

# ── Rate limiting ──────────────────────────────────────────────────────────────
DOUBT_COOLDOWN_SECONDS: int   = 20
BROADCAST_DELAY:        float = 0.04   # 25 msgs/sec max

# ── XP Thresholds ──────────────────────────────────────────────────────────────
XP_RANKS: list[tuple[int, str]] = [
    (0,     "🌱 Aspirant"),
    (500,   "📚 Scholar"),
    (2000,  "🎯 Strategist"),
    (5000,  "⚔️ Warrior"),
    (10000, "🏆 Topper"),
]

# ── Motivation library (200 entries, used at push time — no Gemini call) ─────
MOTIVATION_LINES: list[str] = [
    "Every page you study today is a vote for your future self.",
    "UPSC tests character as much as knowledge. Build both.",
    "Prelims is won in the library. Mains is won in the answer sheet.",
    "One good study day compounds into an unstoppable habit.",
    "The examiner rewards clarity. Read with the pen in hand.",
    "Consistency at 4 hours beats intensity at 8 hours once a week.",
    "Your weak subject is your biggest opportunity. Attack it today.",
    "Current affairs isn't extra load — it's bonus marks waiting to be claimed.",
    "Every IAS officer once sat where you sit now, uncertain and committed.",
    "Revision is where memory becomes knowledge. Schedule it.",
    "Answer writing is a skill. Practice it like one.",
    "The optional subject that matches your background is your biggest asset.",
    "NCERTs built the foundation of toppers. They'll build yours too.",
    "Sleep is not wasted time — it is when memory consolidates.",
    "One subject at a time. One topic at a time. That's how the syllabus gets done.",
    "PYQs reveal the examiner's mind. Study them like conversations.",
    "The aspirant who rests strategically beats the one who burns out.",
    "Ethics isn't abstract philosophy — it's about who you choose to be under pressure.",
    "Every mock test result is data. Use it. Don't feel it.",
    "Write one answer today. The habit builds the writer.",
    "Geography is not memorization — it's spatial reasoning. Map it.",
    "Polity comes alive when you read the Constitution itself.",
    "Economy links everything: history, geography, society. Connect the dots.",
    "Environment questions are easiest to score with the right framework.",
    "Science & Tech is just current affairs with a technical angle. Read and link.",
    "Your streak is a contract with your future rank. Honor it.",
    "The IAS exam doesn't just test what you know. It tests how you think.",
    "One difficult topic conquered today is one easy question in the hall tomorrow.",
    "The difference between Prelims clear and Prelims fail is often 3 questions. Prepare for all 100.",
    "A good Mains answer has three things: structure, substance, and a conclusion. Practice all three.",
    "Thinkers in GS4 are not names to memorize. They are lenses to see the world.",
    "Essays are won on the introduction and the conclusion. Write 10 of each.",
    "Confidence in the exam hall is built month by month, not the night before.",
    "The mind that doubts itself in preparation creates clarity through repetition.",
    "Don't study more. Study smarter. Return to what you've covered.",
    "Your notes are your second brain. Build them to last.",
    "Interview preparation starts on Day 1 of your DAF.",
    "Each subject you cover is one fewer unknown in the exam hall.",
    "The aspirant who understands why India works the way it does will top the exam.",
    "Focus is a muscle. Train it every single day.",
    "The syllabus is fixed. Your coverage of it is your only variable.",
    "Preparation is not a sprint. It's the longest 400m you'll ever run.",
    "Make your weak subjects your daily priority. Strength follows attention.",
    "An organised revision schedule doubles the value of your study time.",
    "The toppers didn't work harder. They worked with a better system.",
    "Your plan exists. Trust it. Execute it. Adjust where needed.",
    "One year of serious preparation can change the rest of your life.",
    "Every subject connects. The aspirant who sees the connections scores the most.",
    "Solve 10 PYQs in your weak area today. You'll discover a pattern.",
    "Don't just read the newspaper. Ask: how does this link to GS1, 2, 3, or 4?",
    "The Prelims date is fixed. Count the days. Study accordingly.",
    "Your brain learns in stories. Turn every fact into a narrative.",
    "Pressure builds diamonds and it builds IAS officers too.",
    "The first hour of your study session is always the best. Guard it.",
    "Understanding beats memorization every time. Ask why before you ask what.",
    "Every completed day in your plan is a deposit in the bank of preparation.",
    "The mock test you dread the most is the one you need the most.",
    "A 7-day streak is not a streak. A 30-day streak is a habit.",
    "Your optional subject is where your academic love meets your exam strategy.",
    "Hard days in preparation make easy days in the exam. Welcome difficulty.",
    "The interviewer wants to see a thinking, empathetic officer. Develop both.",
    "Read the model answer once. Write your own answer ten times.",
    "Syllabus coverage without revision is memory without retrieval. Revise.",
    "Every answer you write becomes a template for the next one. Write more.",
    "The difference between preparation and over-preparation is a plan. Use yours.",
    "GS2 connects polity with governance. Read both together.",
    "Internal Security is where Geography meets Polity. Read it that way.",
    "Disaster Management is the examiner's way of asking if you care about people. Show that you do.",
    "Science & Technology is not a science test. It's an awareness test.",
    "The essay is your opportunity to show the examiner how you think. Use it.",
    "Character is tested in the case study. Ethics is lived, not recited.",
    "Today's revision prevents tomorrow's revision crisis.",
    "One topic deeply understood is worth five topics superficially covered.",
    "The question bank in this bot is your daily practice partner. Use it.",
    "Every UPSC topper had a day when they doubted themselves. They continued anyway.",
    "Study your weak subject first today. Save the strong one as a reward.",
    "Current affairs is not optional. It is 30-40% of Prelims.",
    "The mind that reads actively retains. Passive reading is rest, not study.",
    "Mock tests separate knowledge from exam performance. Take them seriously.",
    "The calendar is your most powerful tool. It makes the abstract tangible.",
    "GS3 connects Economy, Science, and Environment. See the threads.",
    "India's Constitution is the most important document you'll read for UPSC.",
    "Every IAS officer remembers their first break-through answer. Write yours today.",
    "Your optional subject is your lifeline in Mains. Invest in it early.",
    "Study in blocks of 90 minutes. The mind focuses best with clear time boxes.",
    "After every study session, close your book and recall. That is where memory forms.",
    "The answer that earns 12/15 has one thing the 8/15 answer lacks: a conclusion.",
    "Your knowledge of governance should come from lived observation, not just books.",
    "India's diversity is GS1's heart. Understand it with empathy, not just facts.",
    "Every environment headline connects to a UPSC question within 12 months.",
    "IR is not just about foreign policy. It's about how India sees the world.",
    "GS4 rewards emotional intelligence as much as ethical theory. Develop both.",
    "The aspirant who treats every subject as personally interesting will go furthest.",
    "Confidence in the interview isn't about knowing everything. It's about honesty.",
    "Revision is not repetition. It is re-understanding with new connections.",
    "The habit of daily current affairs reading takes 21 days to build. Start today.",
    "Strong prelims preparation = strong mains. They feed each other.",
    "Your biggest competitor in UPSC is not other aspirants. It's your own consistency.",
    "One year from now, you will either be glad you started today or wish you had.",
]

# Ensure we have 100 entries minimum (fill with repeats if needed)
while len(MOTIVATION_LINES) < 200:
    MOTIVATION_LINES.extend(MOTIVATION_LINES[:50])
MOTIVATION_LINES = MOTIVATION_LINES[:200]
