"""
services/gemini.py — UPSC Master Bot Gemini AI Service
========================================================
Uses OpenAI-compatible endpoint for gemini-2.0-flash.
Every function has a 15s timeout AND a hardcoded fallback.
Bot NEVER crashes or hangs due to AI unavailability.
"""
import asyncio
import logging

import config

logger = logging.getLogger(__name__)

# ── Client singleton ───────────────────────────────────────────────────────────
_client = None


def _get_client():
    global _client
    if _client is not None:
        return _client
    if not config.GEMINI_API_KEY:
        return None
    try:
        from openai import AsyncOpenAI
        _client = AsyncOpenAI(
            api_key=config.GEMINI_API_KEY,
            base_url=config.GEMINI_BASE_URL,
        )
        logger.info("✅ Gemini client ready | model=%s", config.GEMINI_MODEL)
        return _client
    except ImportError:
        logger.error("❌ openai package not installed. Add to requirements.txt")
        return None
    except Exception as exc:
        logger.exception("❌ Gemini client init failed: %s", exc)
        return None


# ── Core async call ────────────────────────────────────────────────────────────

async def _call(
    system: str,
    user_msg: str,
    max_tokens: int = 500,
    temperature: float = 0.4,
) -> str | None:
    """
    Make a Gemini API call.
    Returns the text response or None on any failure.
    """
    client = _get_client()
    if not client:
        return None
    try:
        response = await asyncio.wait_for(
            client.chat.completions.create(
                model=config.GEMINI_MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user_msg},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            ),
            timeout=config.GEMINI_TIMEOUT,
        )
        text = (response.choices[0].message.content or "").strip()
        logger.info("✅ Gemini response | chars=%d", len(text))
        return text or None
    except asyncio.TimeoutError:
        logger.warning("❌ Gemini timeout after %ds", config.GEMINI_TIMEOUT)
        return None
    except Exception as exc:
        logger.warning("❌ Gemini call failed: %s | %s", type(exc).__name__, exc)
        return None


# ── Fallback strings ───────────────────────────────────────────────────────────

_FB_DOUBT = (
    "⚠️ <b>AI temporarily unavailable</b>\n\n"
    "For UPSC topics, refer to:\n"
    "• NCERTs (primary source for all subjects)\n"
    "• Laxmikanth — Polity\n"
    "• Shankar IAS — Environment\n"
    "• Spectrum — Modern History\n"
    "• Economic Survey + Budget — Economy\n\n"
    "<i>Try again in a moment.</i>"
)

_FB_EVALUATE = {
    "score": 0, "introduction": 0, "content": 0, "examples": 0,
    "structure": 0, "conclusion": 0,
    "feedback": "⚠️ AI evaluation unavailable. Please retry in a moment.",
    "model_outline": "Review standard frameworks for this question type.",
    "raw": "",
}

_FB_CA = (
    "⚠️ AI summary unavailable.\n\n"
    "Recommended CA sources:\n"
    "• The Hindu (daily)\n"
    "• PIB (schemes & government)\n"
    "• Vision IAS monthly magazine"
)

_FB_NARRATIVE = (
    "Your plan is well-structured for your timeline and available hours. "
    "Stay consistent — consistency at your level beats intensity every time. "
    "Focus extra attention on your weak subjects from the very first week. 🎯"
)

_FB_WEEKLY = "AI weekly report unavailable. Check your stats in the Progress section."

_FB_OUTLINE = "AI outline unavailable. Use the standard Introduction → Body → Conclusion framework."


# ── Public AI functions ────────────────────────────────────────────────────────

async def solve_doubt(
    question: str,
    subject: str = "",
    phase: str = "",
    level: str = "",
    history: list[dict] | None = None,
) -> str:
    """
    Answer a UPSC doubt question with full context.
    context-aware: calibrated by level/phase/subject.
    """
    if not question or len(question.strip()) < 5:
        return "❓ Please type a complete question (at least 5 characters)."

    level_note = {
        "beginner":     "Explain simply, with examples. No jargon.",
        "intermediate": "Standard depth. Use structured points.",
        "advanced":     "Advanced depth. Include nuances and analytical perspectives.",
    }.get(level, "Standard UPSC depth.")

    system = (
        "You are an expert UPSC Civil Services tutor for Indian aspirants. "
        f"Student level: {level or 'intermediate'}. {level_note} "
        "Answer History, Geography, Polity, Economy, S&T, Environment, Ethics, IR. "
        "Format: 150-250 words. Plain numbered points only. "
        "No markdown, no asterisks, no bold. "
        "End with one memory tip: 'TIP: ...'."
    )

    context_line = ""
    if subject:
        context_line += f"Subject context: {subject}. "
    if phase:
        context_line += f"Preparation phase: {phase}. "

    result = await _call(system, f"{context_line}\nQuestion: {question.strip()}", max_tokens=450)
    if result:
        return f"🤖 <b>AI Answer</b>\n\n{result}"
    return _FB_DOUBT


async def evaluate_answer(
    question: str,
    answer_text: str,
    answer_type: str = "GS",
    gs_paper: str = "GS1",
) -> dict:
    """
    Evaluate a UPSC answer using the 5-criterion rubric (100 points total).
    Returns structured dict with scores and feedback.
    """
    system = (
        "You are a strict UPSC Mains examiner with 20 years experience. "
        "Evaluate using EXACT 100-point rubric. Respond ONLY in this format:\n"
        "SCORE: X\n"
        "INTRO: X (out of 20) — [one line]\n"
        "CONTENT: X (out of 30) — [one line]\n"
        "EXAMPLES: X (out of 20) — [one line]\n"
        "STRUCTURE: X (out of 15) — [one line]\n"
        "CONCLUSION: X (out of 15) — [one line]\n"
        "FEEDBACK: [3 specific improvement points, numbered]\n"
        "OUTLINE: [6-point model answer outline]"
    )
    user_msg = f"Paper: {gs_paper} | Type: {answer_type}\nQuestion:\n{question}\n\nAnswer:\n{answer_text}"
    result = await _call(system, user_msg, max_tokens=600)

    if not result:
        return _FB_EVALUATE.copy()

    parsed: dict = {}
    for line in result.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            parsed[k.strip().upper()] = v.strip()

    def _extract_score(raw: str, max_pts: int) -> int:
        try:
            return min(max_pts, int(str(raw).split("(")[0].strip().split()[0]))
        except Exception:
            return 0

    total = _extract_score(parsed.get("SCORE", "0"), 100)
    return {
        "score":        total,
        "introduction": _extract_score(parsed.get("INTRO", "0"), 20),
        "content":      _extract_score(parsed.get("CONTENT", "0"), 30),
        "examples":     _extract_score(parsed.get("EXAMPLES", "0"), 20),
        "structure":    _extract_score(parsed.get("STRUCTURE", "0"), 15),
        "conclusion":   _extract_score(parsed.get("CONCLUSION", "0"), 15),
        "feedback":     parsed.get("FEEDBACK", "Keep practising!"),
        "model_outline": parsed.get("OUTLINE", ""),
        "raw":          result,
    }


async def evaluate_essay(topic: str, essay_text: str) -> dict:
    """Evaluate an essay using essay-specific rubric."""
    system = (
        "You are a UPSC essay examiner. Evaluate on 125-point scale. "
        "Format:\nSCORE: X\nHOOK: X/15\nSTRUCTURE: X/25\n"
        "INSIGHT: X/40\nEXAMPLES: X/25\nCONCLUSION: X/20\n"
        "FEEDBACK: [3 specific improvements]\nBEST_LINE: [quote the strongest sentence]"
    )
    result = await _call(system, f"Topic: {topic}\n\nEssay:\n{essay_text}", max_tokens=500)
    if not result:
        return {"score": 0, "feedback": _FB_OUTLINE, "raw": ""}
    parsed = {}
    for line in result.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            parsed[k.strip().upper()] = v.strip()
    try:
        score = int(str(parsed.get("SCORE", "0")).split()[0])
    except Exception:
        score = 0
    return {
        "score": score,
        "feedback": parsed.get("FEEDBACK", "Keep writing!"),
        "best_line": parsed.get("BEST_LINE", ""),
        "raw": result,
    }


async def evaluate_ethics_case(scenario: str, analysis_text: str) -> dict:
    """Evaluate ethics case study using 7-step framework."""
    system = (
        "You are a UPSC GS4 Ethics examiner. Evaluate using the 7-step framework: "
        "1.Stakeholder identification 2.Core ethical dilemma 3.Values at stake "
        "4.Options analysis 5.Recommended action 6.Justification 7.Safeguards. "
        "Format:\nSCORE: X/100\nSTEPS_COVERED: [list which of 7 steps covered]\n"
        "STRENGTHS: [2 points]\nGAPS: [2 points]\nFEEDBACK: [3 specific improvements]"
    )
    result = await _call(system, f"Scenario:\n{scenario}\n\nAnalysis:\n{analysis_text}", max_tokens=500)
    if not result:
        return {"score": 0, "feedback": "AI unavailable. Review 7-step framework.", "raw": ""}
    parsed = {}
    for line in result.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            parsed[k.strip().upper()] = v.strip()
    try:
        score = int(str(parsed.get("SCORE", "0/100")).split("/")[0].strip())
    except Exception:
        score = 0
    return {
        "score": score,
        "steps_covered": parsed.get("STEPS_COVERED", ""),
        "strengths": parsed.get("STRENGTHS", ""),
        "gaps": parsed.get("GAPS", ""),
        "feedback": parsed.get("FEEDBACK", "Keep practising."),
        "raw": result,
    }


async def extract_handwritten(image_base64: str) -> str:
    """
    Use Gemini Vision to extract text from a handwritten answer photo.
    Returns extracted text string.
    """
    client = _get_client()
    if not client:
        return ""
    try:
        response = await asyncio.wait_for(
            client.chat.completions.create(
                model=config.GEMINI_MODEL,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                        },
                        {
                            "type": "text",
                            "text": (
                                "Transcribe this handwritten UPSC answer sheet exactly. "
                                "Preserve all text. If illegible in parts, note [illegible]. "
                                "Return ONLY the transcribed text, nothing else."
                            ),
                        },
                    ],
                }],
                max_tokens=800,
            ),
            timeout=20.0,
        )
        return (response.choices[0].message.content or "").strip()
    except Exception as exc:
        logger.warning("extract_handwritten failed: %s", exc)
        return ""


async def get_plan_narrative(
    level: str,
    months: int,
    hrs: float,
    weak: list,
    total_hrs: float,
) -> str:
    """
    Generate a 3-sentence realistic mentor assessment for a plan combo.
    Called during onboarding analysis — 15s timeout with fallback.
    """
    system = "You are a senior IAS coaching mentor. Be realistic, warm, and direct. Plain text only."
    prompt = (
        f"UPSC aspirant: Level={level}, Timeline={months} months, "
        f"Hours/day={hrs}, Weak subjects={weak or 'none mentioned'}, "
        f"Total planned hours={total_hrs:.0f}.\n"
        "Write 3 sentences: (1) realistic assessment of this plan "
        "(2) specific advice for their weak area if any "
        "(3) one motivating line about consistency. Plain text, no bullets."
    )
    result = await _call(system, prompt, max_tokens=180, temperature=0.5)
    return result or _FB_NARRATIVE


async def get_ca_summary(topic: str) -> str:
    """Get a concise UPSC-focused current affairs summary."""
    system = (
        "You are a UPSC Current Affairs expert. Give exam-relevant summaries. "
        "5 key points (numbered), 1 Prelims angle, 1 Mains angle. "
        "Max 220 words. Plain text, no markdown."
    )
    result = await _call(system, f"UPSC CA summary on: {topic}", max_tokens=350)
    return result or _FB_CA


async def get_weekly_report(user_stats: dict) -> str:
    """
    Generate personalised weekly performance insight.
    Called scheduled Monday 6AM — NOT on demand.
    """
    system = (
        "You are a data-driven UPSC study coach. "
        "Give 3 short paragraphs: "
        "1. Performance grade (A/B/C/D) with brief justification. "
        "2. Best moment and growth edge this week. "
        "3. One specific recommendation for next week. "
        "Max 200 words. Plain text."
    )
    prompt = (
        f"Student weekly stats:\n"
        f"Days completed: {user_stats.get('days_done', 0)}/7\n"
        f"Answers written: {user_stats.get('answers', 0)}\n"
        f"Mock tests: {user_stats.get('mocks', 0)}\n"
        f"Current streak: {user_stats.get('streak', 0)}\n"
        f"XP earned this week: {user_stats.get('xp_week', 0)}\n"
        f"Best subject: {user_stats.get('best_subject', 'unknown')}\n"
        f"Weak subject: {user_stats.get('weak_subject', 'unknown')}"
    )
    result = await _call(system, prompt, max_tokens=300, temperature=0.5)
    return result or _FB_WEEKLY


async def get_ai_insights(stats: dict) -> str:
    """
    Admin cohort analysis. Cached 6 hours — NOT on demand.
    """
    system = (
        "You are a data analyst for a UPSC EdTech platform. "
        "Give 5 numbered actionable insights based on cohort data. "
        "Be specific and data-driven. Max 300 words. Plain text."
    )
    prompt = (
        f"Platform stats:\n"
        f"Total users: {stats.get('total_users', 0)}\n"
        f"Active today: {stats.get('active_today', 0)}\n"
        f"Active this week: {stats.get('active_week', 0)}\n"
        f"Avg streak: {stats.get('avg_streak', 0):.1f}\n"
        f"Completions today: {stats.get('completions_today', 0)}\n"
        f"Drop-off (7+ days): {stats.get('dropped_off', 0)}\n"
        f"Top weak subject: {stats.get('top_weak', 'unknown')}\n"
        f"Most popular plan: {stats.get('top_plan', 'unknown')}"
    )
    result = await _call(system, prompt, max_tokens=400)
    return result or "AI insights unavailable. Check logs for API status."


async def get_essay_outline(topic: str) -> str:
    """Generate a 6-point essay outline for a given topic."""
    system = (
        "You are a UPSC essay coach. Generate a crisp 6-point essay outline. "
        "Format: numbered points, each 1 line with a suggested angle/example. "
        "Max 200 words. Plain text."
    )
    result = await _call(system, f"Essay topic: {topic}", max_tokens=250)
    return result or _FB_OUTLINE


async def generate_flashcard_questions(subject: str, subtopic: str) -> list[str]:
    """Generate 3 recall questions for a topic (used in flashcard mode)."""
    system = (
        "You are a UPSC tutor. Generate exactly 3 short-answer recall questions "
        "for quick revision. Each question on its own line. "
        "Questions should test key facts and concepts. Plain text only."
    )
    prompt = f"Subject: {subject}\nTopic: {subtopic}\n\nGenerate 3 recall questions:"
    result = await _call(system, prompt, max_tokens=200)
    if not result:
        return [
            f"What are the key features of {subtopic}?",
            f"How does {subtopic} relate to the UPSC syllabus?",
            f"Name 3 important points about {subtopic}.",
        ]
    questions = [q.strip() for q in result.strip().split("\n") if q.strip()]
    return questions[:3] if questions else [f"What is {subtopic}?"]
