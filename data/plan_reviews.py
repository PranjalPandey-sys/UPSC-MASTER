"""
data/plan_reviews.py — Pre-Generated Plan Reviews for All 48 Plans
===================================================================
CRITICAL FEATURE: All 48 plan reviews are HARDCODED here.
Zero AI calls needed during onboarding analysis — instant display.
Covers: quality score, coverage, outcome, mentor note, reality check,
best-for profile, phase highlights, syllabus coverage, suggestions.

Plans: 3 levels × 4 timelines × 4 hour-variants = 48 entries.
Levels:    beginner | intermediate | advanced
Timelines: 3 | 6 | 12 | 24 months
Hours:     2 | 4 | 6 | 8 hrs/day
"""

# ─────────────────────────────────────────────────────────────────────────────
# PLAN REVIEWS: complete pre-generated data for all 48 combinations
# ─────────────────────────────────────────────────────────────────────────────

PLAN_REVIEWS: dict[str, dict] = {

    # ══════════════════════════════════════════════════════════════════════════
    # BEGINNER × 3 MONTHS
    # ══════════════════════════════════════════════════════════════════════════

    "beginner_3months_2hours": {
        "score": 20.6, "coverage_pct": 34.1,
        "quality_label": "❌ Weak", "quality_band": "weak",
        "total_hours": 180, "subjects_covered": 6, "mock_tests": 2,
        "answer_writing_days": 0,
        "readiness": "Not ready — awareness only",
        "best_for": "Total beginners who want a 90-day orientation before committing to a longer plan.",
        "reality_check": (
            "180 hours covers barely one-third of the UPSC priority syllabus. "
            "You will not be exam-ready. This is an orientation, not preparation. "
            "Subjects like Ethics, IR, Environment, and Governance will be completely missed."
        ),
        "realistic_outcome": (
            "You'll gain a basic understanding of UPSC structure and cover 6 of 12 core subjects "
            "at an introductory level. Prelims clearing probability is under 10%. "
            "This plan is best used as the first 3 months of a longer commitment, not standalone preparation."
        ),
        "mentor_note": (
            "This combination is below the minimum threshold for competitive preparation. "
            "If 2 hours is genuinely your maximum right now, commit to 12 months minimum. "
            "Short timelines with low hours are the most common reason aspirants give up — "
            "the syllabus feels endless because there's no system to cover it."
        ),
        "phase_highlights": [
            "Month 1: History (Ancient + Medieval basics), Introduction to Polity",
            "Month 2: Geography fundamentals, Economy overview",
            "Month 3: Quick revision of months 1-2, Basic Prelims MCQ practice",
        ],
        "syllabus_coverage": {
            "History": "40%", "Geography": "35%", "Polity": "30%",
            "Economy": "20%", "Environment": "0%", "Ethics": "0%",
            "IR": "0%", "S&T": "0%", "Indian Society": "0%",
        },
        "suggestions": [
            "Extend your timeline to at least 12 months for meaningful preparation",
            "Even 2 hrs/day over 12 months = 720 hours — competitive territory for a beginner",
            "Use these 3 months to build the NCERT foundation and daily CA habit",
        ],
        "better_suggestion": {"level": "beginner", "timeline": 12, "hours": 6},
        "is_recommended": False,
    },

    "beginner_3months_4hours": {
        "score": 28.0, "coverage_pct": 34.1,
        "quality_label": "❌ Weak", "quality_band": "weak",
        "total_hours": 360, "subjects_covered": 6, "mock_tests": 2,
        "answer_writing_days": 4,
        "readiness": "Not ready",
        "best_for": "Beginners using this as an intensive orientation before a 6-12 month main push.",
        "reality_check": (
            "360 hours with a beginner base still only scratches the surface. "
            "The extra hours vs 2h/day help depth per topic, but the 3-month ceiling limits coverage. "
            "Most toppers have 1,200-2,500 hours invested — you'll have 360."
        ),
        "realistic_outcome": (
            "Strong foundation in 6 core subjects. Polity, History, and Geography will be adequately covered. "
            "Economy, Ethics, Environment, and IR will be missing. "
            "Prelims clearing probability: 15-25% if the 6 covered subjects happen to be heavily tested."
        ),
        "mentor_note": (
            "The 4h/day commitment is commendable for a beginner. The 3-month timeline is the limiting factor. "
            "Redirect this energy into a 12-month plan. Your daily habit of 4 hours, over a full year, "
            "produces 1,440 hours — genuinely competitive territory."
        ),
        "phase_highlights": [
            "Month 1: History (Ancient to Modern overview), Polity basics (Constitution)",
            "Month 2: Geography (Physical + Human India), Economy fundamentals",
            "Month 3: Mock tests, revision, identify gaps for next phase",
        ],
        "syllabus_coverage": {
            "History": "50%", "Geography": "45%", "Polity": "40%",
            "Economy": "25%", "Environment": "5%", "Ethics": "0%",
        },
        "suggestions": [
            "Treat these 3 months as your NCERTs-only phase",
            "Complete all NCERT History, Polity, Geography (Class 6-12) in this window",
            "Then enter a 6-12 month main preparation with standard books",
        ],
        "better_suggestion": {"level": "beginner", "timeline": 12, "hours": 6},
        "is_recommended": False,
    },

    "beginner_3months_6hours": {
        "score": 28.0, "coverage_pct": 34.1,
        "quality_label": "❌ Weak", "quality_band": "weak",
        "total_hours": 540, "subjects_covered": 7, "mock_tests": 3,
        "answer_writing_days": 6,
        "readiness": "Prelims partially ready for covered subjects only",
        "best_for": "Full-time aspirants doing an intensive 3-month sprint before switching to a longer plan.",
        "reality_check": (
            "540 hours is a respectable block, but 3 months limits phase progression. "
            "You can go deeper on 7 subjects but still miss 5 core areas completely. "
            "No Mains answer writing development possible in this window."
        ),
        "realistic_outcome": (
            "A sincere beginner completing this achieves a Basic-Intermediate level in priority subjects. "
            "Prelims probability: 20-30% for the covered subjects. "
            "This prepares you excellently for a follow-on 6-9 month focused preparation."
        ),
        "mentor_note": (
            "6 hours a day for 3 months shows serious intent. Channel this into a longer commitment. "
            "If you can do 6h/day, you should be planning for at least 12 months. "
            "That's 2,160 hours — the threshold where IFS/IPS rank becomes realistic."
        ),
        "phase_highlights": [
            "Month 1: Intensive NCERTs (History, Polity, Geography), daily CA habit building",
            "Month 2: Standard books begin (Laxmikanth, Spectrum), Economy overview",
            "Month 3: Environment + S&T basics, Mock practice, Weak area identification",
        ],
        "syllabus_coverage": {
            "History": "55%", "Geography": "50%", "Polity": "50%",
            "Economy": "30%", "Environment": "15%", "S&T": "10%",
        },
        "suggestions": [
            "Extend to 12 months with the same 6h/day commitment — game-changing difference",
            "Use Month 3 to identify your optional subject and start it in the next phase",
            "Begin answer writing in Month 2 — even 2 answers/week builds the habit early",
        ],
        "better_suggestion": {"level": "beginner", "timeline": 12, "hours": 6},
        "is_recommended": False,
    },

    "beginner_3months_8hours": {
        "score": 34.0, "coverage_pct": 34.1,
        "quality_label": "❌ Weak", "quality_band": "weak",
        "total_hours": 720, "subjects_covered": 8, "mock_tests": 3,
        "answer_writing_days": 8,
        "readiness": "Basic — approaching Prelims readiness for covered subjects",
        "best_for": "Full-time aspirants doing a focused pre-exam sprint if Prelims is in 3 months.",
        "reality_check": (
            "720 hours in 3 months is a genuine full-time commitment. "
            "At 8h/day you WILL cover more ground than most aspirants do in 6 months of casual study. "
            "However, retention suffers at this intensity — revision is essential."
        ),
        "realistic_outcome": (
            "Sincere beginner will reach Basic-Intermediate level in 8 of 12 subjects. "
            "Prelims clearing probability: 25-35%. Not reliable but not impossible. "
            "Burnout risk is HIGH — build recovery days into the plan."
        ),
        "mentor_note": (
            "8 hours a day for 3 months is unsustainable for most people. "
            "If you must do 3 months, pace at 6h/day and keep 2 days per week at 4h for recovery. "
            "Burnout before Prelims is the single biggest risk at this intensity level."
        ),
        "phase_highlights": [
            "Weeks 1-4: Complete NCERT foundation across all subjects",
            "Weeks 5-8: Standard books, full GS coverage sprint",
            "Weeks 9-12: Mock tests, revision, weak area focus",
        ],
        "syllabus_coverage": {
            "History": "60%", "Geography": "55%", "Polity": "60%",
            "Economy": "40%", "Environment": "25%", "S&T": "20%",
            "Ethics": "10%", "IR": "10%",
        },
        "suggestions": [
            "Plan for recovery: take one full day off per week to prevent burnout",
            "Focus heavily on PYQs from Week 6 onwards — know what the exam actually asks",
            "After this 3-month sprint, extend your preparation rather than stopping",
        ],
        "better_suggestion": {"level": "beginner", "timeline": 12, "hours": 6},
        "is_recommended": False,
    },

    # ══════════════════════════════════════════════════════════════════════════
    # BEGINNER × 6 MONTHS
    # ══════════════════════════════════════════════════════════════════════════

    "beginner_6months_2hours": {
        "score": 36.2, "coverage_pct": 46.5,
        "quality_label": "⚠️ Basic", "quality_band": "basic",
        "total_hours": 360, "subjects_covered": 8, "mock_tests": 3,
        "answer_writing_days": 8,
        "readiness": "Not ready — foundational awareness only",
        "best_for": "Working professionals with absolute time constraints who need a realistic minimum commitment.",
        "reality_check": (
            "2 hours/day is the absolute floor for UPSC preparation. "
            "Over 6 months you get 360 hours — the same as a 4h/day aspirant gets in 3 months. "
            "The timeline advantage gives you better retention through spaced repetition."
        ),
        "realistic_outcome": (
            "You'll cover 8 of 12 subjects at a basic level. Polity, History, and Geography will be adequate. "
            "Economy, Environment, Ethics, and IR will be superficial. "
            "Prelims probability: 20-30%. Mains is not realistic at this combination."
        ),
        "mentor_note": (
            "2 hours a day requires extraordinary discipline to sustain for 6 months. "
            "The quality of these 2 hours matters more than almost any other factor. "
            "No distractions. Active reading. Daily CA. Answer at least one practice question per week."
        ),
        "phase_highlights": [
            "Months 1-2: Foundation — NCERTs, Polity basics, History overview",
            "Months 3-4: Coverage — Economy, Geography, Environment",
            "Months 5-6: Revision + Prelims MCQ focus",
        ],
        "syllabus_coverage": {
            "History": "50%", "Geography": "45%", "Polity": "45%",
            "Economy": "30%", "Environment": "20%", "Ethics": "5%",
        },
        "suggestions": [
            "Use weekends to double your daily hours — 4 hrs Saturday + Sunday adds 200+ hrs/year",
            "Build a sustainable 2-hour routine: 1h study + 30min CA + 30min revision",
            "Consider extending to 12 months — same daily hours, dramatically better coverage",
        ],
        "better_suggestion": {"level": "beginner", "timeline": 12, "hours": 4},
        "is_recommended": False,
    },

    "beginner_6months_4hours": {
        "score": 50.2, "coverage_pct": 54.0,
        "quality_label": "⚠️ Basic", "quality_band": "basic",
        "total_hours": 720, "subjects_covered": 9, "mock_tests": 4,
        "answer_writing_days": 15,
        "readiness": "Prelims partially ready",
        "best_for": "Dedicated beginners who want a solid first attempt at Prelims with realistic expectations.",
        "reality_check": (
            "720 hours over 6 months is the minimum for a credible Prelims attempt. "
            "Most aspirants who clear Prelims on first attempt have 1,000-1,500 hours invested. "
            "This plan will get you close to the qualifying threshold but not comfortably through it."
        ),
        "realistic_outcome": (
            "Sincere beginner will achieve Basic-Intermediate level across 9 subjects. "
            "Prelims probability: 35-45%. Mains is possible but answer writing will be underdeveloped. "
            "This is a solid plan for a motivated beginner's first cycle."
        ),
        "mentor_note": (
            "4 hours a day for 6 months is the beginner standard — this is what most aspirants do. "
            "The key is whether you actually spend all 4 hours productively. "
            "Track your time honestly. Most people who think they study 4 hours actually study 2.5 hours."
        ),
        "phase_highlights": [
            "Month 1: NCERTs (History, Polity, Geography), CA habit",
            "Months 2-3: Standard books begin, Economy + Environment",
            "Month 4: Ethics basics, Optional subject orientation",
            "Months 5-6: Mock tests, Revision, Weak area work",
        ],
        "syllabus_coverage": {
            "History": "60%", "Geography": "55%", "Polity": "60%",
            "Economy": "45%", "Environment": "35%", "Ethics": "20%",
            "S&T": "25%", "IR": "15%",
        },
        "suggestions": [
            "Write at least 1-2 answers per week from Month 2 onwards",
            "PYQ analysis every Sunday — understand what the exam actually values",
            "If you clear Prelims, immediately extend to 12-month full plan for Mains",
        ],
        "better_suggestion": {"level": "beginner", "timeline": 12, "hours": 6},
        "is_recommended": False,
    },

    "beginner_6months_6hours": {
        "score": 58.6, "coverage_pct": 60.0,
        "quality_label": "✅ Moderate", "quality_band": "moderate",
        "total_hours": 1080, "subjects_covered": 10, "mock_tests": 5,
        "answer_writing_days": 25,
        "readiness": "Prelims ready + basic Mains exposure",
        "best_for": "Serious beginners targeting a strong first Prelims attempt with some Mains foundation.",
        "reality_check": (
            "1,080 hours is competitive territory for a first-time aspirant. "
            "You'll feel the difference — fewer gaps, better retention, actual answer writing practice. "
            "Still below the average topper's preparation time but well above the median aspirant."
        ),
        "realistic_outcome": (
            "Sincere beginner at 6h/day over 6 months will reach Intermediate level. "
            "Prelims probability: 45-55%. Mains qualification becomes realistic if Prelims is cleared. "
            "This is the minimum for a genuinely competitive attempt."
        ),
        "mentor_note": (
            "6 hours a day for 6 months is what separates the serious aspirant from the casual one. "
            "If you maintain this, you'll cover 10 of 12 subjects meaningfully. "
            "The missing piece will be optional subject depth and Mains answer quality — both fixable in a follow-on phase."
        ),
        "phase_highlights": [
            "Month 1: Full NCERT sprint + Polity basics",
            "Months 2-3: Standard books (History, Geography, Economy), Ethics starts",
            "Month 4: Environment, S&T, IR, Optional subject begins",
            "Months 5-6: Mock tests, Answer writing, Comprehensive revision",
        ],
        "syllabus_coverage": {
            "History": "70%", "Geography": "65%", "Polity": "70%",
            "Economy": "55%", "Environment": "45%", "Ethics": "35%",
            "S&T": "35%", "IR": "30%", "Optional": "30%",
        },
        "suggestions": [
            "This combination is genuinely competitive — don't downgrade your timeline",
            "Prioritise answer writing from Month 2: 3 answers/week minimum",
            "Weekly mock tests from Month 4 onwards are non-negotiable",
        ],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "beginner_6months_8hours": {
        "score": 60.1, "coverage_pct": 63.8,
        "quality_label": "✅ Moderate", "quality_band": "moderate",
        "total_hours": 1440, "subjects_covered": 11, "mock_tests": 6,
        "answer_writing_days": 35,
        "readiness": "Prelims ready + Mains partially ready",
        "best_for": "Full-time aspirants who can dedicate their complete day to preparation for 6 months.",
        "reality_check": (
            "1,440 hours is a serious commitment. At beginner level, this much intensity in 6 months "
            "risks depth-vs-breadth trade-offs. You'll cover more topics but may not go deep enough on each. "
            "Built-in revision days are essential at this pace."
        ),
        "realistic_outcome": (
            "Strong plan for a beginner. Full syllabus covered at reasonable depth. "
            "Prelims probability: 50-60%. Mains quality is above average for a first-timer. "
            "You'll arrive at Mains with 35+ answer writing sessions — well above the median."
        ),
        "mentor_note": (
            "8 hours a day for 6 months is the maximum sustainable intensity for most people. "
            "Build in 4-hour 'recovery days' every 10 days. Your brain needs consolidation time. "
            "The marginal return from 8h vs 6h/day is lower than you think — quality matters more."
        ),
        "phase_highlights": [
            "Month 1: Complete NCERT foundation (all subjects)",
            "Months 2-3: Standard books, concurrent optional subject",
            "Month 4: GS4 Ethics deep dive, Essay framework",
            "Month 5: Mock tests, PYQ analysis",
            "Month 6: Comprehensive revision, Mains answer writing",
        ],
        "syllabus_coverage": {
            "History": "75%", "Geography": "70%", "Polity": "75%",
            "Economy": "60%", "Environment": "55%", "Ethics": "50%",
            "S&T": "45%", "IR": "40%", "Optional": "40%", "Essay": "35%",
        },
        "suggestions": [
            "Take one full rest day per week — non-negotiable at 8h/day",
            "Alternate between heavy and light subjects on consecutive days",
            "Track focus time separately from total time spent — aim for 6h pure focus",
        ],
        "better_suggestion": None,
        "is_recommended": True,
    },

    # ══════════════════════════════════════════════════════════════════════════
    # BEGINNER × 12 MONTHS
    # ══════════════════════════════════════════════════════════════════════════

    "beginner_12months_2hours": {
        "score": 52.3, "coverage_pct": 54.0,
        "quality_label": "⚠️ Basic", "quality_band": "basic",
        "total_hours": 720, "subjects_covered": 9, "mock_tests": 4,
        "answer_writing_days": 20,
        "readiness": "Prelims partially ready",
        "best_for": "Working professionals with genuine time constraints who want a realistic 12-month plan.",
        "reality_check": (
            "720 hours over 12 months is better than 720 hours in 3 months — spaced repetition and "
            "long-term retention make a real difference. The coverage is still limited but the habit is stronger."
        ),
        "realistic_outcome": (
            "Sincere aspirant will develop a solid foundation across 9 subjects. "
            "Prelims probability: 35-45%. The 12-month timeline allows for quality revision cycles "
            "that shorter plans simply don't permit. Your retention will be significantly better."
        ),
        "mentor_note": (
            "2h/day over 12 months builds the most important thing: a study habit. "
            "Many toppers started exactly here. The key is zero-compromise consistency — "
            "2 hours every single day, even on tough days, is how this plan wins."
        ),
        "phase_highlights": [
            "Months 1-3: Foundation — NCERTs, Polity, History basics",
            "Months 4-6: Standard books, Economy, Geography",
            "Months 7-9: Environment, Ethics, S&T, Optional",
            "Months 10-12: Mock tests, Revision cycles, Weak area focus",
        ],
        "syllabus_coverage": {
            "History": "60%", "Geography": "55%", "Polity": "60%",
            "Economy": "45%", "Environment": "35%", "Ethics": "25%",
        },
        "suggestions": [
            "Upgrade to 4h/day if possible — the additional coverage over 12 months is dramatic",
            "Weekly answer writing practice is essential even at 2h/day",
            "Optional subject should begin by Month 4 at latest",
        ],
        "better_suggestion": {"level": "beginner", "timeline": 12, "hours": 6},
        "is_recommended": False,
    },

    "beginner_12months_4hours": {
        "score": 69.5, "coverage_pct": 63.8,
        "quality_label": "✅ Moderate", "quality_band": "moderate",
        "total_hours": 1440, "subjects_covered": 11, "mock_tests": 7,
        "answer_writing_days": 45,
        "readiness": "Prelims ready + Mains possible",
        "best_for": "The standard aspirant: working professional or student, realistic and committed.",
        "reality_check": (
            "1,440 hours over 12 months is the working professional's gold standard. "
            "You'll cover the full syllabus at meaningful depth, have time for proper revision, "
            "and develop answer writing skills. This is a real attempt, not just a preparation attempt."
        ),
        "realistic_outcome": (
            "Strong plan for a beginner. Full syllabus covered at solid depth. "
            "Prelims probability: 55-65%. Mains qualification is realistic. "
            "Optional subject coverage will be adequate. Answer writing will be above average."
        ),
        "mentor_note": (
            "4h/day for 12 months is the plan most IAS officers point to when asked what worked. "
            "It's sustainable, it compounds, and it leaves room for life. "
            "The discipline of a daily 4-hour habit for a full year is itself the preparation."
        ),
        "phase_highlights": [
            "Months 1-3: Foundation phase — NCERTs complete, CA habit established",
            "Months 4-7: Coverage — all 12 GS subjects, optional begins",
            "Months 8-10: Retention — revision cycles, PYQ mastery",
            "Months 11-12: Prelims sprint, Mock test series, Mains prep begins",
        ],
        "syllabus_coverage": {
            "History": "72%", "Geography": "68%", "Polity": "72%",
            "Economy": "60%", "Environment": "55%", "Ethics": "45%",
            "S&T": "50%", "IR": "45%", "Optional": "55%", "Essay": "40%",
        },
        "suggestions": [
            "This is a strong plan — trust the process and don't cut corners on revision",
            "Mock test series from Month 8: at least 8-10 full-length Prelims tests",
            "Start answer writing by Month 3 minimum — even one answer per week competes",
        ],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "beginner_12months_6hours": {
        "score": 79.6, "coverage_pct": 69.0,
        "quality_label": "⭐ Strong", "quality_band": "strong",
        "total_hours": 2160, "subjects_covered": 12, "mock_tests": 9,
        "answer_writing_days": 70,
        "readiness": "Prelims very likely + Mains competitive",
        "best_for": "Serious full-time aspirants targeting a competitive first-cycle result.",
        "reality_check": (
            "2,160 hours is where genuine competitive preparation begins. "
            "At this level, you'll have covered the complete syllabus with depth, "
            "written 70+ answers, taken 9+ mock tests, and built real competency across all 12 subjects."
        ),
        "realistic_outcome": (
            "Exceptional commitment. A beginner investing 2,160 hours over 12 months will likely clear Prelims "
            "and arrive at Mains with genuinely competitive preparation. "
            "Prelims probability: 70-80%. Mains: above average. IFS/IRS rank range is realistic."
        ),
        "mentor_note": (
            "This is the combination that transforms beginners into serious contenders. "
            "6 hours a day for 12 months, with a proper plan, is how the rank list gets cracked. "
            "The plan ensures you're not just covering but retaining, writing, and testing."
        ),
        "phase_highlights": [
            "Months 1-2: Deep NCERT foundation, Polity reading (Laxmikanth starts)",
            "Months 3-5: Full GS coverage, Answer writing begins, Optional subject starts",
            "Months 6-8: Retention phase, PYQ deep dive, Mock test series",
            "Months 9-10: Prelims sprint, Full mock tests, Current affairs sprint",
            "Months 11-12: Mains prep, Ethics deep dive, Essay writing",
        ],
        "syllabus_coverage": {
            "History": "80%", "Geography": "75%", "Polity": "80%",
            "Economy": "70%", "Environment": "65%", "Ethics": "60%",
            "S&T": "60%", "IR": "55%", "Optional": "65%", "Essay": "55%",
        },
        "suggestions": [
            "This plan is close to optimal for a beginner — commit to it fully",
            "The 70 answer writing days are your biggest competitive advantage",
            "Consider the 12months × 8hours variant only if you're truly full-time",
        ],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "beginner_12months_8hours": {
        "score": 80.8, "coverage_pct": 72.0,
        "quality_label": "⭐ Strong", "quality_band": "strong",
        "total_hours": 2880, "subjects_covered": 12, "mock_tests": 10,
        "answer_writing_days": 90,
        "readiness": "Prelims very likely + Mains competitive",
        "best_for": "Full-time aspirants with no professional commitments targeting first-attempt results.",
        "reality_check": (
            "2,880 hours is the kind of preparation that produces consistent Prelims clearers. "
            "At beginner level with this much time, you'll actually surpass many 'intermediate' aspirants "
            "who haven't put in the hours. Depth and breadth both become achievable."
        ),
        "realistic_outcome": (
            "Exceptional commitment. A beginner at 2,880 hours will very likely clear Prelims "
            "and deliver competitive Mains answers. Prelims probability: 75-85%. "
            "IFS/IPS/IRS rank is within realistic range with strong optional subject performance."
        ),
        "mentor_note": (
            "8 hours a day for 12 months demands serious lifestyle engineering. "
            "Plan your daily schedule with precision: fixed study blocks, fixed break times, "
            "weekly review sessions, and monthly health checks. "
            "The aspirants who sustain 8h/day for 12 months are the ones who treat this like a job."
        ),
        "phase_highlights": [
            "Months 1-2: Complete NCERT foundation (all subjects simultaneously)",
            "Months 3-5: Deep standard book coverage, full optional subject",
            "Months 6-8: Retention, PYQs, Mock test series begins",
            "Month 9: Prelims intensive sprint",
            "Months 10-12: Mains preparation, Essay, Ethics, Optional depth",
        ],
        "syllabus_coverage": {
            "History": "85%", "Geography": "80%", "Polity": "85%",
            "Economy": "75%", "Environment": "70%", "Ethics": "65%",
            "S&T": "65%", "IR": "60%", "Optional": "72%", "Essay": "60%",
        },
        "suggestions": [
            "Schedule mandatory recovery: 4h on Sundays, 6h two days/month",
            "Quality control: track active vs passive study time separately",
            "Test series from Month 5: at least 12 full-length Prelims mocks before the exam",
        ],
        "better_suggestion": None,
        "is_recommended": True,
    },

    # ══════════════════════════════════════════════════════════════════════════
    # BEGINNER × 24 MONTHS
    # ══════════════════════════════════════════════════════════════════════════

    "beginner_24months_2hours": {
        "score": 72.0, "coverage_pct": 63.0,
        "quality_label": "✅ Moderate", "quality_band": "moderate",
        "total_hours": 1440, "subjects_covered": 11, "mock_tests": 8,
        "answer_writing_days": 40,
        "readiness": "Prelims ready + Mains possible",
        "best_for": "Working professionals who cannot spare more than 2 hours daily but have 2 years to prepare.",
        "reality_check": (
            "2 hours/day × 24 months = 1,440 hours. Same total as 4h/day × 12 months, "
            "but the extended timeline dramatically improves retention through spaced repetition. "
            "The slow and steady approach genuinely works here."
        ),
        "realistic_outcome": (
            "Solid preparation for a beginner with limited daily time. "
            "Full syllabus coverage at adequate depth, 40+ answer writing sessions, "
            "and 8 mock tests. Prelims probability: 55-65%. Mains is genuinely possible."
        ),
        "mentor_note": (
            "24 months of 2h/day tests your consistency more than your intelligence. "
            "The aspirants who succeed here are the ones who never miss a day. "
            "Set up your 2-hour block as a non-negotiable daily appointment with your future."
        ),
        "phase_highlights": [
            "Months 1-6: Foundation — complete NCERTs, Polity, History",
            "Months 7-12: Coverage — all GS papers, Optional begins",
            "Months 13-18: Retention + Prelims cycles",
            "Months 19-24: Mains focus, Essay, Ethics, Interview prep (basic)",
        ],
        "syllabus_coverage": {
            "History": "70%", "Geography": "65%", "Polity": "70%",
            "Economy": "55%", "Environment": "50%", "Ethics": "45%",
            "S&T": "45%", "IR": "40%", "Optional": "55%",
        },
        "suggestions": [
            "Use Sundays to write full-length answers — 2h dedicated answer writing day",
            "Read NCERTs in Year 1; standard books in Year 2",
            "Monthly self-assessment using this bot's competency tracker",
        ],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "beginner_24months_4hours": {
        "score": 83.0, "coverage_pct": 72.0,
        "quality_label": "⭐ Strong", "quality_band": "strong",
        "total_hours": 2880, "subjects_covered": 12, "mock_tests": 12,
        "answer_writing_days": 90,
        "readiness": "Prelims very likely + Mains competitive",
        "best_for": "Aspirants who want thorough preparation without the intensity of 6-8 hours daily.",
        "reality_check": (
            "2,880 hours over 24 months is one of the strongest beginner combinations. "
            "You get deep coverage, extended revision cycles, strong answer writing development, "
            "and time to genuinely understand rather than just memorise."
        ),
        "realistic_outcome": (
            "Exceptional preparation for a beginner. Prelims probability: 75-85%. "
            "Mains is genuinely competitive. Multiple revision cycles ensure strong retention. "
            "Answer writing development over 90 sessions produces real exam-day confidence."
        ),
        "mentor_note": (
            "This is the beginner plan I'd recommend to most aspirants who ask me. "
            "4 hours a day is sustainable. 24 months is thorough. "
            "The extended timeline gives you the luxury of understanding rather than just covering. "
            "Don't rush this — the depth you build here is what wins interviews."
        ),
        "phase_highlights": [
            "Year 1: Foundation + Full GS Coverage + Optional begins",
            "Year 2: Retention + Prelims + Mains + Interview preparation basics",
        ],
        "syllabus_coverage": {
            "History": "82%", "Geography": "78%", "Polity": "85%",
            "Economy": "72%", "Environment": "68%", "Ethics": "65%",
            "S&T": "62%", "IR": "58%", "Optional": "72%", "Essay": "60%",
        },
        "suggestions": [
            "This is a strong plan — the most important variable is your consistency",
            "Complete two full Prelims mock test series (one in Year 1, one in Year 2)",
            "Interview preparation through this bot's ethics and personality modules from Month 18",
        ],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "beginner_24months_6hours": {
        "score": 85.0, "coverage_pct": 76.0,
        "quality_label": "⭐ Strong", "quality_band": "strong",
        "total_hours": 4320, "subjects_covered": 12, "mock_tests": 14,
        "answer_writing_days": 130,
        "readiness": "Fully competitive — IFS/IPS range",
        "best_for": "Serious aspirants targeting IFS/IPS/IRS with thorough, deep preparation.",
        "reality_check": (
            "4,320 hours is peak preparation territory. A beginner with 4,320 hours "
            "of quality study time is not a beginner anymore — they've covered the syllabus "
            "at the depth most 'advanced' aspirants aim for."
        ),
        "realistic_outcome": (
            "A sincere beginner completing this 24-month, 6h/day plan becomes genuinely competitive "
            "for IFS/IPS/IRS ranks. Prelims probability: 85-90%. Mains quality: strong. "
            "This combination is where the IAS dream becomes mathematically realistic."
        ),
        "mentor_note": (
            "6h/day for 24 months builds a level of preparation that very few aspirants achieve. "
            "The extended timeline means you're not just covering content — you're building expertise. "
            "By Month 18, your answers will have a depth that examiners notice."
        ),
        "phase_highlights": [
            "Year 1: Deep foundation + Complete GS coverage + Optional mastery begins",
            "Year 2: Advanced retention + Prelims cycles + Mains mastery + Interview track",
        ],
        "syllabus_coverage": {
            "History": "88%", "Geography": "85%", "Polity": "90%",
            "Economy": "80%", "Environment": "75%", "Ethics": "72%",
            "S&T": "70%", "IR": "65%", "Optional": "80%", "Essay": "72%",
        },
        "suggestions": [
            "Your biggest risk is burnout at Month 12 — plan a 2-week lighter schedule then",
            "Use Year 2's extra depth for original integration: linking subjects, finding patterns",
            "The interview module (Month 20-24) is your final differentiator",
        ],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "beginner_24months_8hours": {
        "score": 86.0, "coverage_pct": 78.0,
        "quality_label": "⭐ Strong", "quality_band": "strong",
        "total_hours": 5760, "subjects_covered": 12, "mock_tests": 16,
        "answer_writing_days": 160,
        "readiness": "Fully competitive — IAS range realistic",
        "best_for": "Full-time aspirants targeting IAS with a thorough 2-year preparation track.",
        "reality_check": (
            "5,760 hours over 24 months is extraordinary dedication. Very few aspirants reach this level. "
            "The risk is that beyond a certain point, more hours don't add proportional returns — "
            "quality of those hours and strategic focus matter more than raw time."
        ),
        "realistic_outcome": (
            "A beginner with this commitment level approaches intermediate/advanced territory by Year 2. "
            "Prelims probability: 88-93%. Mains: highly competitive. "
            "IAS rank in the top 200 is achievable with strong optional and interview performance."
        ),
        "mentor_note": (
            "8 hours a day for 24 months requires a support system, not just willpower. "
            "Get your family's understanding, join a study group, and build in quarterly breaks. "
            "The aspirants who sustain this for 2 years are exceptional — and they succeed."
        ),
        "phase_highlights": [
            "Year 1: Depth-first coverage, multiple revision cycles, mock test series starts",
            "Year 2: Advanced analysis, original answer frameworks, interview personality development",
        ],
        "syllabus_coverage": {
            "All subjects": "85-92%",
            "Optional": "85%", "Essay": "78%", "Ethics + GS4": "80%",
        },
        "suggestions": [
            "Structure your 8 hours into 3 blocks: morning (3h), afternoon (2.5h), evening (2.5h)",
            "Mandatory full-day off once per week — this is when memory consolidates",
            "After Month 18, reduce to 6h/day for the final 6 months — sharper focus",
        ],
        "better_suggestion": None,
        "is_recommended": True,
    },

    # ══════════════════════════════════════════════════════════════════════════
    # INTERMEDIATE × 3 MONTHS
    # ══════════════════════════════════════════════════════════════════════════

    "intermediate_3months_2hours": {
        "score": 27.0, "coverage_pct": 40.0,
        "quality_label": "❌ Weak", "quality_band": "weak",
        "total_hours": 180, "subjects_covered": 7, "mock_tests": 2,
        "answer_writing_days": 5,
        "readiness": "Refresher only — not exam-ready",
        "best_for": "Intermediate aspirants needing a quick revision sprint before a longer preparation break.",
        "reality_check": (
            "180 hours for an intermediate aspirant is useful for refreshing existing knowledge, "
            "not building new depth. If you're genuinely intermediate (have studied before), "
            "this serves as revision — not primary preparation."
        ),
        "realistic_outcome": (
            "An intermediate aspirant refreshes 7 core subjects, identifies current gaps, "
            "and re-establishes study habits. Prelims probability: 25-35% if knowledge base was strong before. "
            "Not suitable as a standalone preparation strategy."
        ),
        "mentor_note": (
            "If you're intermediate, your existing knowledge is your asset. "
            "2h/day for 3 months is only justified if you're currently working "
            "and need to maintain momentum before a longer leave period. "
            "Otherwise, commit more time."
        ),
        "phase_highlights": [
            "Month 1: High-priority topic revision, CA consolidation",
            "Month 2: Weak subject focus, PYQ revision",
            "Month 3: Mock tests, Answer writing practice",
        ],
        "syllabus_coverage": {
            "History": "50%", "Geography": "45%", "Polity": "50%",
            "Economy": "35%", "Environment": "25%", "Ethics": "15%",
        },
        "suggestions": [
            "Focus on your PYQ gaps — this is the highest-return activity for intermediates",
            "3 months is too short — plan to extend to 6-12 months minimum",
            "Use this time to identify your exact weak areas for targeted attack",
        ],
        "better_suggestion": {"level": "intermediate", "timeline": 12, "hours": 6},
        "is_recommended": False,
    },

    "intermediate_3months_4hours": {
        "score": 36.4, "coverage_pct": 40.0,
        "quality_label": "⚠️ Basic", "quality_band": "basic",
        "total_hours": 360, "subjects_covered": 8, "mock_tests": 3,
        "answer_writing_days": 10,
        "readiness": "Partially ready for covered subjects",
        "best_for": "Intermediate aspirants doing a targeted 3-month pre-exam revision sprint.",
        "reality_check": (
            "360 hours for an intermediate is a real refresher. You'll consolidate existing knowledge "
            "and identify gaps. But 3 months limits new depth development. "
            "Best used as the final phase of a longer preparation, not as standalone."
        ),
        "realistic_outcome": (
            "Intermediate aspirant will consolidate 8 core subjects and improve weak areas. "
            "Prelims clearing: 35-45% if base knowledge was established before. "
            "Good as a revision sprint for someone who has studied before."
        ),
        "mentor_note": (
            "Intermediate aspirants often underestimate how much time is needed to fill gaps. "
            "4h/day for 3 months is only competitive if you already have strong foundations. "
            "Be honest: are you truly intermediate or are you calling yourself that to shortcut?"
        ),
        "phase_highlights": [
            "Month 1: Gap identification + High-priority topics",
            "Month 2: Weak subject deep dive + Answer writing",
            "Month 3: Mock tests + Final revision",
        ],
        "syllabus_coverage": {
            "History": "60%", "Geography": "55%", "Polity": "60%",
            "Economy": "45%", "Environment": "35%", "Ethics": "25%",
        },
        "suggestions": [
            "Map your existing knowledge honestly before starting",
            "Focus 60% of time on your 3 weakest subjects",
            "Mock tests from Week 2 — use results to guide daily study",
        ],
        "better_suggestion": {"level": "intermediate", "timeline": 12, "hours": 6},
        "is_recommended": False,
    },

    "intermediate_3months_6hours": {
        "score": 36.4, "coverage_pct": 40.0,
        "quality_label": "⚠️ Basic", "quality_band": "basic",
        "total_hours": 540, "subjects_covered": 9, "mock_tests": 4,
        "answer_writing_days": 15,
        "readiness": "Prelims approaching readiness",
        "best_for": "Intermediate aspirants doing a final 3-month Prelims sprint if exam is imminent.",
        "reality_check": (
            "540 hours in 3 months for an intermediate is a real sprint. "
            "You can refresh the full GS syllabus and do meaningful mock test practice. "
            "This is the minimum for a respectable Prelims attempt for someone with prior preparation."
        ),
        "realistic_outcome": (
            "Intermediate aspirant will consolidate 6 core subjects and score ~90-100/200 in Prelims. "
            "Clearing probability: 40-50%. 15 answer writing sessions will noticeably improve Mains readiness. "
            "Best suited as a Prelims sprint after a longer earlier preparation phase."
        ),
        "mentor_note": (
            "If Prelims is 3 months away and you're intermediate, 6h/day is your minimum. "
            "Focus 50% on PYQ analysis, 30% on weak subject revision, 20% on current affairs. "
            "Answer writing can be reduced — time is the constraint."
        ),
        "phase_highlights": [
            "Month 1: Rapid GS revision (all 4 papers), PYQ analysis",
            "Month 2: Weak areas + Current Affairs sprint",
            "Month 3: Daily mock tests, CSAT practice, Final revision",
        ],
        "syllabus_coverage": {
            "History": "65%", "Geography": "60%", "Polity": "65%",
            "Economy": "50%", "Environment": "40%", "Ethics": "30%",
        },
        "suggestions": [
            "Attempt at least 12 full-length Prelims mocks in 3 months",
            "Current affairs: review last 12 months of Vision IAS monthly in Week 1",
            "CSAT: dedicate 1 hour daily if any weakness — it's qualifying but can eliminate you",
        ],
        "better_suggestion": {"level": "intermediate", "timeline": 6, "hours": 6},
        "is_recommended": False,
    },

    "intermediate_3months_8hours": {
        "score": 44.4, "coverage_pct": 40.0,
        "quality_label": "⚠️ Basic", "quality_band": "basic",
        "total_hours": 720, "subjects_covered": 10, "mock_tests": 4,
        "answer_writing_days": 20,
        "readiness": "Prelims ready for intermediate",
        "best_for": "Intermediate aspirants in a final 3-month full-time sprint before Prelims.",
        "reality_check": (
            "720 hours in 3 months for an intermediate aspirant is what toppers describe as a 'Prelims sprint.' "
            "You'll cover the full syllabus, do serious mock practice, and feel genuinely prepared. "
            "Burnout risk is real — pace yourself."
        ),
        "realistic_outcome": (
            "Solid intermediate plan. Full syllabus coverage at good depth. "
            "Prelims clearing: 55-65%. This is a genuinely competitive attempt. "
            "Mains quality will be moderate — the 3-month window doesn't allow full development."
        ),
        "mentor_note": (
            "This is the plan that works for the 'one last push before Prelims' scenario. "
            "If this is your 2nd or 3rd attempt and you're intermediate, 8h/day for 3 months "
            "with a laser focus on PYQ patterns and weak areas can absolutely clear Prelims."
        ),
        "phase_highlights": [
            "Weeks 1-4: Full GS revision + PYQ analysis",
            "Weeks 5-8: Weak area intensive + CA consolidation",
            "Weeks 9-12: Daily full-length mocks + Answer writing",
        ],
        "syllabus_coverage": {
            "History": "72%", "Geography": "68%", "Polity": "72%",
            "Economy": "58%", "Environment": "48%", "Ethics": "38%",
        },
        "suggestions": [
            "Day 1: Create your weakness map across all GS papers",
            "Mocks: start from Week 2, increase frequency to daily in last month",
            "Current affairs: commit 1.5h daily — it's 30-35% of Prelims",
        ],
        "better_suggestion": None,
        "is_recommended": False,
    },

    # ══════════════════════════════════════════════════════════════════════════
    # INTERMEDIATE × 6 MONTHS
    # ══════════════════════════════════════════════════════════════════════════

    "intermediate_6months_2hours": {
        "score": 43.4, "coverage_pct": 54.6,
        "quality_label": "⚠️ Basic", "quality_band": "basic",
        "total_hours": 360, "subjects_covered": 8, "mock_tests": 3,
        "answer_writing_days": 10,
        "readiness": "Partial — depends heavily on prior foundation",
        "best_for": "Intermediate working professionals maintaining preparation momentum.",
        "reality_check": "360 hours over 6 months is limited but manageable for an intermediate who already has foundations. The extended timeline helps retention even with limited daily hours.",
        "realistic_outcome": "Intermediate aspirant will consolidate existing knowledge and fill some gaps. Prelims clearing: 35-45% depending on prior preparation strength.",
        "mentor_note": "2h/day is bare minimum. Make these hours count: no passive reading, active recall only.",
        "phase_highlights": ["Months 1-2: Priority gap filling", "Months 3-4: Standard book revision", "Months 5-6: Mock tests + CA"],
        "syllabus_coverage": {"History": "55%", "Geography": "50%", "Polity": "55%", "Economy": "40%"},
        "suggestions": ["Upgrade to 4h/day if at all possible", "Focus on your 3 biggest weak areas exclusively"],
        "better_suggestion": {"level": "intermediate", "timeline": 12, "hours": 6},
        "is_recommended": False,
    },

    "intermediate_6months_4hours": {
        "score": 60.0, "coverage_pct": 63.4,
        "quality_label": "✅ Moderate", "quality_band": "moderate",
        "total_hours": 720, "subjects_covered": 10, "mock_tests": 5,
        "answer_writing_days": 25,
        "readiness": "Prelims ready + Mains partially ready",
        "best_for": "Intermediate aspirants with a 6-month window before Prelims.",
        "reality_check": "720 hours for an intermediate is genuinely competitive. Your prior knowledge leverages every hour more than a beginner gets from the same time.",
        "realistic_outcome": "Solid intermediate plan. Full GS coverage at 85% depth. Prelims: 55-65%. Mains is possible with the 25 answer writing sessions building real skill.",
        "mentor_note": "An intermediate at 4h/day for 6 months is in real competition territory. Your advantage is your existing base — build on it systematically.",
        "phase_highlights": ["Months 1-2: Gap filling + Standard books", "Months 3-4: Weak areas + Answer writing", "Months 5-6: Mock tests + Mains prep"],
        "syllabus_coverage": {"History": "70%", "Geography": "65%", "Polity": "70%", "Economy": "58%", "Environment": "50%", "Ethics": "40%"},
        "suggestions": ["3 answers per week minimum from Month 1", "PYQ analysis: 2 years back minimum", "Optional subject: complete at least 1 reading in 6 months"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "intermediate_6months_6hours": {
        "score": 70.8, "coverage_pct": 70.4,
        "quality_label": "✅ Moderate", "quality_band": "moderate",
        "total_hours": 1080, "subjects_covered": 11, "mock_tests": 7,
        "answer_writing_days": 40,
        "readiness": "Prelims very likely + Mains competitive",
        "best_for": "Serious intermediate aspirants targeting a first-time Prelims+Mains success.",
        "reality_check": "1,080 hours at intermediate level is a formidable combination. Your existing knowledge makes each hour more productive than a beginner gets from the same investment.",
        "realistic_outcome": "Solid intermediate plan achieving 85% syllabus coverage. Prelims: 65-75%. Mains quality is genuinely strong. IFS/IRS rank range is realistic with good optional performance.",
        "mentor_note": "This is the plan where intermediate aspirants start becoming genuine threats in the selection list. 6h/day for 6 months, with your prior base, is enough to be competitive.",
        "phase_highlights": ["Month 1: Full syllabus audit + Gap map creation", "Months 2-3: Targeted gap filling + Answer writing starts", "Months 4-5: Mock series + Weak area sprint", "Month 6: Comprehensive revision + Prelims preparation"],
        "syllabus_coverage": {"History": "78%", "Geography": "72%", "Polity": "78%", "Economy": "65%", "Environment": "58%", "Ethics": "52%", "S&T": "55%", "IR": "50%"},
        "suggestions": ["Treat this like a full-time job with 6-hour work days", "Answer writing: 5+ per week from Month 2", "Maintain daily current affairs without exception"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "intermediate_6months_8hours": {
        "score": 72.5, "coverage_pct": 74.8,
        "quality_label": "✅ Moderate", "quality_band": "moderate",
        "total_hours": 1440, "subjects_covered": 12, "mock_tests": 8,
        "answer_writing_days": 55,
        "readiness": "Prelims very likely + Mains very competitive",
        "best_for": "Full-time intermediate aspirants targeting IFS/IPS in first or second attempt.",
        "reality_check": "1,440 hours for an intermediate in 6 months is an elite-level effort. Burnout is the primary risk. Build in recovery intentionally.",
        "realistic_outcome": "Competitive intermediate plan. Prelims: 70-80%. Mains quality: strong. IFS/IPS/IRS rank is realistic with good optional subject score.",
        "mentor_note": "This is the 6-month max-effort plan. If Prelims is in 6 months and you're intermediate, this is your plan. Execute it with precision, not just intensity.",
        "phase_highlights": ["Months 1-2: Full GS depth coverage + Optional intensive", "Months 3-4: Mock series + Answer writing sprint", "Months 5-6: Prelims sprint + Mains preparation"],
        "syllabus_coverage": {"History": "82%", "Geography": "78%", "Polity": "82%", "Economy": "72%", "Environment": "65%", "Ethics": "60%", "S&T": "60%", "IR": "55%", "Optional": "70%"},
        "suggestions": ["Weekly recovery day is mandatory at 8h/day", "10 full-length Prelims mocks minimum", "Optional: complete both readings by Month 4"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    # ══════════════════════════════════════════════════════════════════════════
    # INTERMEDIATE × 12 MONTHS
    # ══════════════════════════════════════════════════════════════════════════

    "intermediate_12months_2hours": {
        "score": 62.1, "coverage_pct": 63.4,
        "quality_label": "✅ Moderate", "quality_band": "moderate",
        "total_hours": 720, "subjects_covered": 10, "mock_tests": 6,
        "answer_writing_days": 30,
        "readiness": "Prelims ready + Mains exposure",
        "best_for": "Working professionals who are intermediate aspirants with 12 months of limited time.",
        "reality_check": "720 hours over 12 months gives an intermediate strong retention through spaced repetition. The extended timeline is a genuine advantage even with limited daily hours.",
        "realistic_outcome": "Solid preparation. Full GS at adequate depth, 30 answer writing sessions, mock test series. Prelims: 50-60%. Mains is a realistic target.",
        "mentor_note": "For an intermediate at 2h/day, consistency over 12 months will compound significantly. Your prior knowledge means every revision session is high-yield.",
        "phase_highlights": ["Months 1-3: Priority gap filling", "Months 4-8: Full GS revision + Answer writing", "Months 9-12: Mock series + Mains prep"],
        "syllabus_coverage": {"History": "68%", "Geography": "62%", "Polity": "68%", "Economy": "55%", "Environment": "48%", "Ethics": "38%"},
        "suggestions": ["Upgrade hours on weekends — 4h Saturday/Sunday adds 400+ hours/year", "Prioritise revision over new coverage — you're intermediate", "Monthly progress self-assessment is critical"],
        "better_suggestion": {"level": "intermediate", "timeline": 12, "hours": 6},
        "is_recommended": False,
    },

    "intermediate_12months_4hours": {
        "score": 81.9, "coverage_pct": 74.8,
        "quality_label": "⭐ Strong", "quality_band": "strong",
        "total_hours": 1440, "subjects_covered": 12, "mock_tests": 9,
        "answer_writing_days": 60,
        "readiness": "Prelims very likely + Mains competitive",
        "best_for": "The standard intermediate aspirant's plan — high quality, sustainable, competitive.",
        "reality_check": "1,440 hours over 12 months is where most interview-selected candidates were. Your intermediate base leverages these hours better than any beginner starting from scratch.",
        "realistic_outcome": "Competitive intermediate plan. Prelims: 70-80%. Mains quality: strong. IFS/IPS/IRS rank is within realistic reach. 60 answer writing sessions are your biggest edge over the average candidate.",
        "mentor_note": "This is the plan I recommend to most intermediate aspirants. It's sustainable, thorough, and competitive. The extended timeline means you arrive at Prelims rested and sharp, not exhausted.",
        "phase_highlights": ["Months 1-3: Gap identification + Deep standard book revision", "Months 4-6: Full GS coverage + Ethics + Optional depth", "Months 7-9: Retention phase + Mock test series", "Months 10-12: Prelims sprint + Mains preparation"],
        "syllabus_coverage": {"History": "80%", "Geography": "75%", "Polity": "80%", "Economy": "70%", "Environment": "65%", "Ethics": "60%", "S&T": "58%", "IR": "55%", "Optional": "72%"},
        "suggestions": ["This is a strong plan — stay the course", "Answer writing from Day 1: 4-5 per week", "Mock test series: start Month 7, do 3 full series"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "intermediate_12months_6hours": {
        "score": 92.4, "coverage_pct": 81.0,
        "quality_label": "🏆 Elite", "quality_band": "elite",
        "total_hours": 2160, "subjects_covered": 12, "mock_tests": 9,
        "answer_writing_days": 124,
        "readiness": "Fully competitive — IFS/IPS/IRS range",
        "best_for": "Serious aspirants targeting IFS/IPS/IRS in the current cycle.",
        "reality_check": "2,160 hours for an intermediate is arguably the best single-cycle plan on this entire list. High hours, extended timeline, intermediate base — this combination is where the rank list is cracked.",
        "realistic_outcome": "Intermediate with 2,160 hours is genuinely competitive. Prelims: 80-90%. Mains: strong. IFS/IPS/IRS rank range is very realistic. IAS requires additional optional strength and interview edge.",
        "mentor_note": "This is an elite-tier plan. If you're intermediate and can commit 6 hours daily for 12 months, you are among the most seriously prepared aspirants in the country. Execute it methodically.",
        "phase_highlights": ["Months 1-2: Priority gap filling + Routine establishment", "Months 3-5: Full GS deep coverage + Answer writing builds", "Months 6-8: Retention + Optional mastery + Mock series", "Months 9-10: Prelims intensive", "Months 11-12: Mains writing + Ethics + Essay"],
        "syllabus_coverage": {"History": "88%", "Geography": "84%", "Polity": "90%", "Economy": "80%", "Environment": "75%", "Ethics": "72%", "S&T": "70%", "IR": "68%", "Optional": "80%", "Essay": "70%"},
        "suggestions": ["This plan doesn't need improvement — it needs execution", "124 answer writing days: this is your competitive moat", "Mock test excellence: 3 full series + chapter tests"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "intermediate_12months_8hours": {
        "score": 93.8, "coverage_pct": 84.5,
        "quality_label": "🏆 Elite", "quality_band": "elite",
        "total_hours": 2880, "subjects_covered": 12, "mock_tests": 10,
        "answer_writing_days": 140,
        "readiness": "Fully competitive — IAS range realistic",
        "best_for": "Full-time intermediate aspirants targeting IAS in the current cycle.",
        "reality_check": "2,880 hours for an intermediate over 12 months puts you in the top 1% of prepared aspirants. The challenge is sustaining 8h/day quality for 12 months without burnout.",
        "realistic_outcome": "Intermediate with 2,880 hours is highly competitive. Prelims: 85-90%. Mains: highly competitive. IAS rank in top 100-200 is a realistic target with strong optional and interview performance.",
        "mentor_note": "This is the peak plan for a serious intermediate aspirant. The key differentiator from 6h/day is not more coverage — it's deeper mastery, more revision cycles, and more answer writing. Use those extra 2 hours for depth, not breadth.",
        "phase_highlights": ["Months 1-3: Deep gap analysis + Expert-level standard books", "Months 4-6: Full coverage + Multiple optional readings", "Months 7-9: Retention + Mock series + Answer sprint", "Months 10-12: Prelims + Mains + Ethics depth + Interview track"],
        "syllabus_coverage": {"History": "92%", "Geography": "88%", "Polity": "92%", "Economy": "85%", "Environment": "80%", "Ethics": "78%", "S&T": "75%", "IR": "72%", "Optional": "85%", "Essay": "75%"},
        "suggestions": ["Use extra hours for revision, not new content", "Weekly recovery half-day: non-negotiable", "Build your answer writing portfolio — aim for 140+ quality answers"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    # ══════════════════════════════════════════════════════════════════════════
    # INTERMEDIATE × 24 MONTHS
    # ══════════════════════════════════════════════════════════════════════════

    "intermediate_24months_2hours": {
        "score": 83.0, "coverage_pct": 74.0,
        "quality_label": "⭐ Strong", "quality_band": "strong",
        "total_hours": 1440, "subjects_covered": 12, "mock_tests": 10,
        "answer_writing_days": 60,
        "readiness": "Fully competitive — IFS/IPS range",
        "best_for": "Working professional intermediate aspirants with 2 years and very limited daily time.",
        "reality_check": "1,440 hours over 24 months for an intermediate is genuinely competitive. The long timeline means excellent retention and 60 answer writing sessions to build writing muscle.",
        "realistic_outcome": "Strong preparation. Full GS coverage at solid depth. Prelims: 72-82%. Mains: competitive. Multiple revision cycles ensure real retention.",
        "mentor_note": "24 months at 2h/day is the professional's path to a competitive rank. Your prior knowledge + extended timeline + disciplined hours = a genuine threat in the merit list.",
        "phase_highlights": ["Year 1: Foundation reinforcement + Full coverage", "Year 2: Retention + Prelims + Mains mastery"],
        "syllabus_coverage": {"History": "78%", "Geography": "74%", "Polity": "80%", "Economy": "68%", "Environment": "62%", "Ethics": "56%", "Optional": "68%"},
        "suggestions": ["This plan works — stay with it and don't abandon it midway", "Increase to 3h/day on weekends if at all possible", "Year 2's answer writing quality will be exceptional"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "intermediate_24months_4hours": {
        "score": 94.0, "coverage_pct": 85.0,
        "quality_label": "🏆 Elite", "quality_band": "elite",
        "total_hours": 2880, "subjects_covered": 12, "mock_tests": 14,
        "answer_writing_days": 120,
        "readiness": "Fully competitive — IAS/IPS range",
        "best_for": "Intermediate aspirants who want thorough, sustainable, deep preparation over 2 years.",
        "reality_check": "2,880 hours over 24 months for an intermediate is one of the strongest preparation profiles possible. Sustainable pace + deep coverage + extended revision = consistently excellent performance.",
        "realistic_outcome": "Exceptional plan. Prelims: 85-92%. Mains: highly competitive. IAS rank in top 150 is a realistic target with strong optional and interview preparation.",
        "mentor_note": "This is the plan I'd choose if I were an intermediate aspirant with 2 years. Sustainable, deep, and thorough. You arrive at the exam rested, prepared, and confident — not exhausted.",
        "phase_highlights": ["Year 1: Complete GS mastery + Optional first reading", "Year 2: Advanced retention + Prelims + Mains + Interview track"],
        "syllabus_coverage": {"All GS papers": "85-90%", "Optional": "82%", "Essay": "75%", "Ethics": "78%"},
        "suggestions": ["This plan needs execution, not modification", "Use Year 2 for expert-level answer writing and original thinking", "Interview preparation module from Month 20 is critical"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "intermediate_24months_6hours": {
        "score": 96.0, "coverage_pct": 89.0,
        "quality_label": "🏆 Elite", "quality_band": "elite",
        "total_hours": 4320, "subjects_covered": 12, "mock_tests": 16,
        "answer_writing_days": 160,
        "readiness": "Fully competitive — IAS top-200 range",
        "best_for": "Serious intermediate aspirants targeting IAS (not just the services) in this cycle.",
        "reality_check": "4,320 hours for an intermediate over 24 months puts you among the top 0.5% of prepared aspirants. At this level, the difference between ranks is the optional subject and interview — not GS preparation.",
        "realistic_outcome": "Intermediate with 4,320 hours over 24 months is among the most prepared aspirants in any exam cycle. IAS rank in top 100 is achievable with excellent optional + interview performance.",
        "mentor_note": "This is elite territory. At 4,320 hours, your GS preparation will be complete. Invest extra energy in your optional and in genuine personality development for the interview — those are your final differentiators.",
        "phase_highlights": ["Year 1: Mastery-level GS + Optional depth begins", "Year 2: Advanced analysis + Prelims + Mains excellence + Interview preparation"],
        "syllabus_coverage": {"All GS papers": "88-92%", "Optional": "88%", "Essay": "82%", "Ethics + GS4": "85%"},
        "suggestions": ["Your GS preparation will be exceptional — invest in optional equally", "160 answer writing sessions: develop your own frameworks, not just standard ones", "Interview: start mock interviews from Month 20"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "intermediate_24months_8hours": {
        "score": 96.5, "coverage_pct": 91.0,
        "quality_label": "🏆 Elite", "quality_band": "elite",
        "total_hours": 5760, "subjects_covered": 12, "mock_tests": 18,
        "answer_writing_days": 180,
        "readiness": "Peak competitive — IAS top-100 range",
        "best_for": "Full-time intermediate aspirants who are completely dedicated to IAS as a life goal.",
        "reality_check": "5,760 hours at intermediate level over 24 months is extraordinary. Very few aspirants achieve this preparation depth. At this level, the question is not whether you'll clear — it's what rank you'll achieve.",
        "realistic_outcome": "Peak intermediate preparation. Prelims: 90-95%. Mains: highly competitive. IAS rank in top 100 is realistic with good optional and interview. This is the preparation profile of IAS toppers.",
        "mentor_note": "You're building a preparation profile that most officers didn't achieve. Channel this commitment into deep reading, original thinking, and genuine empathy for governance challenges. That's what the interview board looks for.",
        "phase_highlights": ["Year 1: Complete mastery preparation", "Year 2: Advanced analysis, interview personality, peer review writing"],
        "syllabus_coverage": {"All subjects": "90-95%"},
        "suggestions": ["Beyond Month 18, focus more on depth than coverage — you've already covered everything", "Peer answer review with serious aspirants will sharpen your writing exponentially", "Interview preparation: build genuine administrative vision, not just interview answers"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ADVANCED × ALL TIMELINES
    # ══════════════════════════════════════════════════════════════════════════

    "advanced_3months_2hours": {
        "score": 35.2, "coverage_pct": 45.5,
        "quality_label": "⚠️ Basic", "quality_band": "basic",
        "total_hours": 180, "subjects_covered": 8, "mock_tests": 2,
        "answer_writing_days": 8,
        "readiness": "Maintenance only — not improvement",
        "best_for": "Advanced aspirants maintaining preparation during a temporarily constrained period.",
        "reality_check": "180 hours for an advanced aspirant is maintenance, not improvement. Your existing knowledge keeps you from regressing, but you won't make meaningful progress.",
        "realistic_outcome": "Advanced aspirant maintains existing knowledge base. Prelims probability remains at existing level (75-85% if genuinely advanced). No meaningful improvement expected.",
        "mentor_note": "If you're genuinely advanced, 2h/day for 3 months is a holding pattern. Use it to maintain CA habit and answer writing practice. Don't plan to improve — plan to maintain.",
        "phase_highlights": ["Month 1-2: Current affairs + Weak area revision", "Month 3: Mock tests + Answer writing"],
        "syllabus_coverage": {"Maintenance of existing coverage": "existing level"},
        "suggestions": ["Use this as bridge period before committing to longer, higher-hour plan", "Focus exclusively on CA and answer writing — don't attempt new content coverage"],
        "better_suggestion": {"level": "advanced", "timeline": 12, "hours": 6},
        "is_recommended": False,
    },

    "advanced_3months_4hours": {
        "score": 46.6, "coverage_pct": 45.5,
        "quality_label": "⚠️ Basic", "quality_band": "basic",
        "total_hours": 360, "subjects_covered": 9, "mock_tests": 3,
        "answer_writing_days": 15,
        "readiness": "Prelims ready + Weak area improvement",
        "best_for": "Advanced aspirants doing a targeted 3-month revision before Prelims.",
        "reality_check": "360 hours for an advanced aspirant is a real revision block. You can close specific gaps and do serious mock practice. Not for new learning — for consolidation.",
        "realistic_outcome": "Advanced aspirant will maintain and modestly improve across 9 subjects. Prelims: 65-75%. Strong performance in revision-tested subjects. Limited Mains development.",
        "mentor_note": "For an advanced aspirant, this 3 months should be 40% mock tests, 40% weak area revision, 20% CA. Don't read new books — revise notes and practice.",
        "phase_highlights": ["Month 1: Comprehensive weak area identification + PYQ revision", "Month 2: Targeted revision + Answer writing", "Month 3: Full mock series + CA sprint"],
        "syllabus_coverage": {"Revision depth of existing coverage": "high"},
        "suggestions": ["Mock first, then revise weak areas identified by mocks", "Aim for 12+ full-length Prelims mocks in 3 months", "Answer writing: 5 per week to maintain Mains readiness"],
        "better_suggestion": {"level": "advanced", "timeline": 6, "hours": 6},
        "is_recommended": False,
    },

    "advanced_3months_6hours": {
        "score": 46.6, "coverage_pct": 45.5,
        "quality_label": "⚠️ Basic", "quality_band": "basic",
        "total_hours": 540, "subjects_covered": 10, "mock_tests": 4,
        "answer_writing_days": 20,
        "readiness": "Prelims very likely + Mains improving",
        "best_for": "Advanced aspirants in a final sprint for an imminent Prelims exam.",
        "reality_check": "540 hours for a genuine advanced aspirant is enough for a very strong Prelims attempt. Your existing depth means each revision hour is more productive than a beginner's study hour.",
        "realistic_outcome": "Advanced aspirant: Prelims very likely cleared (75-85%). Mains can be written with quality. This is a competitive 3-month plan for someone who has genuinely prepared before.",
        "mentor_note": "At advanced level, 6h/day for 3 months should feel manageable — you already have the habit. The key is to use it for deep practice, not superficial coverage.",
        "phase_highlights": ["Month 1: Mock test diagnostic + Gap filling", "Month 2: Advanced answer writing + CA deep dive", "Month 3: Full mocks daily + Final revision"],
        "syllabus_coverage": {"Revision of existing": "deep", "New additions": "minimal"},
        "suggestions": ["15+ full-length mocks in 3 months — non-negotiable for advanced aspirants", "Mains answer writing: 6-7/week with self-evaluation", "CA: 2 hours daily focused on Prelims-relevant topics"],
        "better_suggestion": None,
        "is_recommended": False,
    },

    "advanced_3months_8hours": {
        "score": 54.6, "coverage_pct": 45.5,
        "quality_label": "⚠️ Basic", "quality_band": "basic",
        "total_hours": 720, "subjects_covered": 11, "mock_tests": 5,
        "answer_writing_days": 25,
        "readiness": "Prelims very likely + Mains competitive",
        "best_for": "Advanced aspirants in a final intensive sprint before Prelims.",
        "reality_check": "720 hours for an advanced aspirant in 3 months is maximum Prelims preparation intensity. You'll feel exam-ready. Burnout risk is real but manageable if you've done this before.",
        "realistic_outcome": "Advanced at 720 hours over 3 months: Prelims very likely cleared (80-90%). Mains answer quality will be strong. This is a genuine competitive attempt.",
        "mentor_note": "For advanced aspirants who've been here before, 8h/day for 3 months is the final sprint. You know what to do — execute without hesitation. Mock tests, revision, and answer writing in equal measure.",
        "phase_highlights": ["Weeks 1-3: Comprehensive revision + Weakness elimination", "Weeks 4-9: Full mock series + Advanced answer writing", "Weeks 10-12: Daily mocks + Final CA sprint"],
        "syllabus_coverage": {"Full GS": "deep revision", "Optional": "2nd/3rd reading"},
        "suggestions": ["20+ full-length mocks in 3 months", "Mock analysis > mock attempts — spend equal time on review", "Body and mind health: sleep 7h/night non-negotiable"],
        "better_suggestion": None,
        "is_recommended": False,
    },

    "advanced_6months_2hours": {
        "score": 52.4, "coverage_pct": 62.0,
        "quality_label": "⚠️ Basic", "quality_band": "basic",
        "total_hours": 360, "subjects_covered": 9, "mock_tests": 4,
        "answer_writing_days": 12,
        "readiness": "Partial — prior preparation dependent",
        "best_for": "Advanced working professionals maintaining and improving during a constrained period.",
        "reality_check": "360 hours for an advanced aspirant over 6 months means the timeline advantage gives better retention. Your prior knowledge means each hour produces more than a beginner's equivalent.",
        "realistic_outcome": "Advanced aspirant maintains high base and fills select gaps. Prelims probability: 60-70%. The 6-month timeline allows proper revision cycles.",
        "mentor_note": "2h/day is challenging for retention. Ensure at least 30 minutes of that is active recall — not passive reading.",
        "phase_highlights": ["Months 1-2: Priority gap identification + CA rhythm", "Months 3-4: Targeted revision + Answer writing", "Months 5-6: Mock series + Exam preparation"],
        "syllabus_coverage": {"Maintenance + selective improvement": "existing + 10%"},
        "suggestions": ["Upgrade hours if possible — advanced aspirants benefit enormously from more time", "Use this 6 months for optional subject mastery if GS is already strong"],
        "better_suggestion": {"level": "advanced", "timeline": 12, "hours": 6},
        "is_recommended": False,
    },

    "advanced_6months_4hours": {
        "score": 71.4, "coverage_pct": 72.0,
        "quality_label": "✅ Moderate", "quality_band": "moderate",
        "total_hours": 720, "subjects_covered": 11, "mock_tests": 6,
        "answer_writing_days": 30,
        "readiness": "Prelims very likely + Mains competitive",
        "best_for": "Advanced aspirants with 6 months targeting a competitive Prelims + Mains result.",
        "reality_check": "720 hours at advanced level is genuinely competitive. Your prior knowledge means this 720 hours delivers intermediate/advanced depth results.",
        "realistic_outcome": "Advanced aspirant: Prelims very likely cleared (75-85%). Mains can be written with quality. 30 answer writing sessions build real exam-day writing fluency.",
        "mentor_note": "An advanced aspirant at 4h/day for 6 months is solidly prepared. Focus on answer quality over syllabus breadth — you likely know enough. The test is whether you can write it.",
        "phase_highlights": ["Months 1-2: Targeted gap analysis + Advanced standard books", "Months 3-4: Answer writing sprint + Optional depth", "Months 5-6: Mock series + Comprehensive revision"],
        "syllabus_coverage": {"All GS": "72-78%", "Optional": "65%"},
        "suggestions": ["5 answers per week from Month 1 — advanced aspirants must write, not just read", "2 complete Prelims mock series in 6 months", "Optional: second complete reading with notes"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "advanced_6months_6hours": {
        "score": 82.6, "coverage_pct": 80.0,
        "quality_label": "⭐ Strong", "quality_band": "strong",
        "total_hours": 1080, "subjects_covered": 12, "mock_tests": 8,
        "answer_writing_days": 50,
        "readiness": "Fully competitive — IFS/IPS/IRS range",
        "best_for": "Advanced aspirants targeting IFS/IPS/IRS in the current exam cycle.",
        "reality_check": "1,080 hours at advanced level delivers the depth of 1,500-1,800 hours for a beginner. Your existing knowledge foundation makes every hour more productive.",
        "realistic_outcome": "Advanced aspirant: Prelims very likely cleared (80-90%). Mains quality: strong to very strong. IFS/IPS/IRS rank is a realistic expectation.",
        "mentor_note": "This is where advanced aspirants separate themselves. 6h/day for 6 months, with your existing foundation, produces a preparation profile that most aspirants don't achieve in 12 months.",
        "phase_highlights": ["Month 1: Full gap audit + Advanced resources", "Months 2-3: Deep coverage + Answer writing builds", "Month 4: Optional mastery + Ethics depth", "Months 5-6: Mock series + Prelims sprint + Mains preparation"],
        "syllabus_coverage": {"All subjects": "80-85%", "Optional": "78%", "Essay": "70%"},
        "suggestions": ["This is a strong plan — don't deviate, execute", "50 answer writing sessions: maintain a quality portfolio", "Ethics case studies: 3 per week practice"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "advanced_6months_8hours": {
        "score": 84.6, "coverage_pct": 85.0,
        "quality_label": "⭐ Strong", "quality_band": "strong",
        "total_hours": 1440, "subjects_covered": 12, "mock_tests": 9,
        "answer_writing_days": 65,
        "readiness": "Fully competitive — IAS range approaching",
        "best_for": "Full-time advanced aspirants targeting top service ranks in this cycle.",
        "reality_check": "1,440 hours for a genuine advanced aspirant over 6 months is exceptional preparation. At this level, preparation gaps are minimal — execution quality becomes the differentiator.",
        "realistic_outcome": "Advanced: Fully competitive. Prelims: 85-92%. Mains quality: strong to excellent. IAS rank in top 200 is a realistic target with outstanding optional subject performance.",
        "mentor_note": "At this level, the margin is in the details. Answer writing quality, optional subject depth, and interview personality are what separate rank 50 from rank 200. Use these 6 months to build all three.",
        "phase_highlights": ["Month 1: Expert-level resources + Final gap closure", "Months 2-3: Advanced answer writing + Optional mastery", "Month 4: Ethics + Essay depth", "Months 5-6: Daily mocks + Comprehensive revision + Mains prep"],
        "syllabus_coverage": {"All subjects": "85-90%", "Optional": "82%", "Essay + Ethics": "78%"},
        "suggestions": ["Recovery days mandatory: 2 half-days per week at minimum", "Answer writing: develop your own analytical frameworks", "Mock interviews: 3-4 practice interviews by end of Month 6"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ADVANCED × 12 MONTHS
    # ══════════════════════════════════════════════════════════════════════════

    "advanced_12months_2hours": {
        "score": 73.5, "coverage_pct": 72.0,
        "quality_label": "✅ Moderate", "quality_band": "moderate",
        "total_hours": 720, "subjects_covered": 11, "mock_tests": 7,
        "answer_writing_days": 35,
        "readiness": "Prelims very likely + Mains competitive",
        "best_for": "Advanced working professionals with 2 hours daily and 12 months to prepare.",
        "reality_check": "720 hours over 12 months for an advanced aspirant is solidly competitive. The extended timeline ensures excellent retention and multiple revision cycles.",
        "realistic_outcome": "Advanced aspirant at 720 hours: Prelims very likely cleared (75-85%). Mains quality competitive. The 12-month timeline gives advanced aspirants a significant retention advantage.",
        "mentor_note": "Your advanced base + 12 months of consistent 2h/day = a genuinely competitive preparation. The key is that your revision cycles will be more effective than a beginner's primary reading.",
        "phase_highlights": ["Months 1-4: Systematic gap filling + Advanced books", "Months 5-8: Answer writing development + Optional mastery", "Months 9-12: Mock series + Prelims + Mains preparation"],
        "syllabus_coverage": {"All GS": "72-76%", "Optional": "68%"},
        "suggestions": ["Weekend upgrade: 4h on Saturdays adds 200+ hours per year", "Focus on answer writing — your biggest differentiator at advanced level", "Monthly mock test to track progress"],
        "better_suggestion": {"level": "advanced", "timeline": 12, "hours": 6},
        "is_recommended": False,
    },

    "advanced_12months_4hours": {
        "score": 94.0, "coverage_pct": 85.0,
        "quality_label": "🏆 Elite", "quality_band": "elite",
        "total_hours": 1440, "subjects_covered": 12, "mock_tests": 10,
        "answer_writing_days": 90,
        "readiness": "Fully competitive — IAS range",
        "best_for": "Advanced aspirants who want thorough 12-month preparation without extreme daily hours.",
        "reality_check": "1,440 hours over 12 months for an advanced aspirant is elite territory. Every single hour builds on an existing strong foundation. Compound returns on every revision session.",
        "realistic_outcome": "Advanced at 1,440 hours: Prelims: 85-92%. Mains: highly competitive. IAS rank in top 150-200 is a realistic expectation with strong optional and interview preparation.",
        "mentor_note": "This is the plan that consistently produces IFS/IPS toppers. Sustainable pace, advanced base, deep coverage, and 90 answer writing sessions. It's not flashy — it's effective.",
        "phase_highlights": ["Months 1-3: Expert-level coverage + Answer writing establishes", "Months 4-6: Optional mastery + Ethics depth + Essay", "Months 7-9: Mock series + Retention", "Months 10-12: Prelims sprint + Mains intensive + Interview basics"],
        "syllabus_coverage": {"All subjects": "85-90%", "Optional": "82%", "Essay + Ethics": "78%"},
        "suggestions": ["90 answer writing days: your biggest competitive advantage", "3 full Prelims mock series in 12 months", "Interview preparation: start in Month 10 with this bot's interview module"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "advanced_12months_6hours": {
        "score": 96.8, "coverage_pct": 92.0,
        "quality_label": "🏆 Elite", "quality_band": "elite",
        "total_hours": 2160, "subjects_covered": 12, "mock_tests": 11,
        "answer_writing_days": 120,
        "readiness": "Peak competitive — IAS top-100 range",
        "best_for": "Serious advanced aspirants targeting IAS in this exam cycle.",
        "reality_check": "2,160 hours at advanced level is where IAS toppers are born. You're building on an already strong foundation with expert-level books, extensive answer writing, and multiple revision cycles. This preparation profile is rarely matched.",
        "realistic_outcome": "Advanced aspirant with 2,160 hours represents peak preparation. Prelims: 90-95%. Mains: highly competitive. IAS rank in top 50-100 is realistic with exceptional optional and interview performance.",
        "mentor_note": "At this level, your GS preparation will be complete and expert. The differentiators are optional subject (aim for 280+/500), essay (genuine philosophical depth), and interview (real administrative vision). Invest equal energy in all three.",
        "phase_highlights": ["Months 1-2: Expert resources + Strategic revision architecture", "Months 3-5: Deep coverage + Answer writing mastery", "Months 6-8: Mock series + Optional depth + Ethics mastery", "Months 9-10: Prelims peak", "Months 11-12: Mains excellence + Interview preparation"],
        "syllabus_coverage": {"All GS papers": "92-95%", "Optional": "88%", "Essay": "85%", "Ethics + GS4": "88%"},
        "suggestions": ["This plan requires no modification — execute it with precision", "120 answer writing days: develop a distinctive analytical voice", "Interview preparation: genuine administrative study, not rehearsed answers"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "advanced_12months_8hours": {
        "score": 98.4, "coverage_pct": 96.0,
        "quality_label": "🏆 Elite", "quality_band": "elite",
        "total_hours": 2880, "subjects_covered": 12, "mock_tests": 12,
        "answer_writing_days": 145,
        "readiness": "Peak competitive — IAS top-50 range",
        "best_for": "Full-time advanced aspirants making their most serious attempt at IAS.",
        "reality_check": "2,880 hours at advanced level over 12 months is the preparation profile of IAS toppers. The combination of advanced foundation + 2,880 hours + 145 answer writing sessions is what rank 1-50 results look like.",
        "realistic_outcome": "Advanced aspirant with 2,880 hours represents peak preparation. Prelims: 90-95%. Mains: elite level. IAS rank in top 50 is realistic with outstanding optional (290+/500) and interview performance.",
        "mentor_note": "At this preparation level, the exam is won on the margin. It's not about knowing more — it's about expressing it better. Invest heavily in answer writing quality, essay depth, and interview authenticity.",
        "phase_highlights": ["Months 1-2: Strategic preparation architecture + Expert resources", "Months 3-5: Deep mastery + Answer writing sprint", "Month 6: Optional + Ethics deep dive", "Month 7: Essay mastery", "Months 8-9: Mock series + Final GS revision", "Month 10: Prelims", "Months 11-12: Mains intensive + Interview prep"],
        "syllabus_coverage": {"All subjects": "95-98%", "Optional": "92%", "Essay + Ethics": "90%"},
        "suggestions": ["Recovery is not optional at 8h/day — build it in structurally", "145 answers: review every single one with a self-evaluation rubric", "By Month 10, your preparation quality is complete — peak, don't overload"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ADVANCED × 24 MONTHS
    # ══════════════════════════════════════════════════════════════════════════

    "advanced_24months_2hours": {
        "score": 94.0, "coverage_pct": 84.0,
        "quality_label": "🏆 Elite", "quality_band": "elite",
        "total_hours": 1440, "subjects_covered": 12, "mock_tests": 12,
        "answer_writing_days": 80,
        "readiness": "Fully competitive — IAS range",
        "best_for": "Advanced working professionals with 2 years and 2 hours daily, targeting IAS.",
        "reality_check": "1,440 hours of advanced preparation over 24 months, with extensive spaced repetition, produces exceptional retention. The long timeline is your competitive advantage.",
        "realistic_outcome": "Advanced aspirant at 1,440 hours over 24 months: Prelims: 85-90%. Mains: highly competitive. IAS rank in top 200 is realistic with strong optional and interview preparation.",
        "mentor_note": "The 24-month timeline gives you multiple revision cycles that a 6-month aspirant simply cannot achieve. Your knowledge depth will be exceptional — especially in subjects you revise 4-5 times.",
        "phase_highlights": ["Year 1: Complete deep coverage + Optional mastery", "Year 2: Advanced retention + Prelims + Mains + Interview development"],
        "syllabus_coverage": {"All subjects": "84-88%", "Optional": "80%", "Essay": "75%"},
        "suggestions": ["Two full exam cycles of preparation — use both for real results", "Year 2's answer writing quality will be exceptional", "Interview module starts Month 20: genuine administrative vision development"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "advanced_24months_4hours": {
        "score": 98.0, "coverage_pct": 95.0,
        "quality_label": "🏆 Elite", "quality_band": "elite",
        "total_hours": 2880, "subjects_covered": 12, "mock_tests": 16,
        "answer_writing_days": 150,
        "readiness": "Peak competitive — IAS top-100 range",
        "best_for": "Advanced aspirants making a thorough 2-year push for IAS.",
        "reality_check": "2,880 hours at advanced level over 24 months is exceptional. Multiple revision cycles, deep optional coverage, extensive answer writing, and interview preparation — all developed over a sustainable timeline.",
        "realistic_outcome": "Advanced with 2,880 hours over 24 months: Prelims: 90-95%. Mains: elite. IAS rank in top 100 is a realistic target. The extended timeline ensures you arrive at the exam at your absolute peak.",
        "mentor_note": "This preparation timeline produces IAS officers who become exceptional administrators — because the extended deep study builds genuine understanding, not just exam readiness.",
        "phase_highlights": ["Year 1: Expert-level GS mastery + Optional first and second reading", "Year 2: Retention mastery + Prelims + Mains excellence + Interview"],
        "syllabus_coverage": {"All subjects": "92-96%"},
        "suggestions": ["Use Year 2's depth for original thinking and cross-subject integration", "150 answer sessions: build a distinctive analytical voice the examiner remembers", "Month 20-24: mock interviews, personality development, administrative vision building"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "advanced_24months_6hours": {
        "score": 99.2, "coverage_pct": 98.0,
        "quality_label": "🏆 Elite", "quality_band": "elite",
        "total_hours": 4320, "subjects_covered": 12, "mock_tests": 18,
        "answer_writing_days": 190,
        "readiness": "Peak competitive — IAS top-50 range",
        "best_for": "Advanced aspirants making their most serious, best-prepared attempt at IAS in this cycle.",
        "reality_check": "4,320 hours at advanced level over 24 months is the preparation of IAS rank-holders. At this level, you're not just prepared — you've developed genuine expertise in every UPSC subject.",
        "realistic_outcome": "Advanced with 4,320 hours over 24 months: this is the preparation profile of IAS toppers. Prelims: 92-96%. Mains: elite level. IAS rank in top 50 is realistic with excellent optional (290+) and interview.",
        "mentor_note": "You're building the preparation that officers look back on and credit for their service. After Month 18, your GS is complete. Invest the final 6 months in optional depth, essay mastery, and genuine administrative personality development.",
        "phase_highlights": ["Year 1: Complete GS mastery + Multiple optional readings + Answer writing establishes", "Year 2: Advanced analysis + Interview personality + Excellence in every dimension"],
        "syllabus_coverage": {"All subjects": "97-99%", "Optional": "95%", "Essay + Ethics": "90%"},
        "suggestions": ["Beyond Month 18, shift focus to quality over quantity", "190 answer sessions: develop your own distinctive approach", "Real governance study: read annual reports, CAG reports, committee recommendations — the interview board will notice"],
        "better_suggestion": None,
        "is_recommended": True,
    },

    "advanced_24months_8hours": {
        "score": 99.8, "coverage_pct": 99.0,
        "quality_label": "🏆 Elite", "quality_band": "elite",
        "total_hours": 5760, "subjects_covered": 12, "mock_tests": 20,
        "answer_writing_days": 220,
        "readiness": "Maximum competitive — IAS rank 1-20 range",
        "best_for": "Advanced aspirants aiming for the very top ranks in the IAS exam.",
        "reality_check": "5,760 hours at advanced level over 24 months is unprecedented preparation. At this level, you're not competing for IAS — you're competing for rank within IAS. The question is how far up the list you go.",
        "realistic_outcome": "This is the preparation profile of IAS rank 1-20 candidates. Prelims: 93-97%. Mains: exceptional. Combined with a strong optional (300+/500) and genuine interview personality, top 20 rank is achievable.",
        "mentor_note": "At this commitment level, the exam is not the challenge — it's the beginning. You're preparing to serve the country with genuine depth. Approach the final 6 months as if you're already in the IAS — developing administrative thinking, empathy, and solutions orientation.",
        "phase_highlights": ["Year 1: Mastery-level preparation in every dimension", "Year 2: Expert analysis, original frameworks, interview readiness, leadership development"],
        "syllabus_coverage": {"All subjects": "99%+"},
        "suggestions": ["After Month 12, depth beats breadth in every decision", "Mandatory: 220 answers reviewed for quality, not just quantity", "Real-world engagement: village visits, NGO work, committee hearings — these enrich your interview beyond any coaching"],
        "better_suggestion": None,
        "is_recommended": True,
    },
}


# ── Helper functions ───────────────────────────────────────────────────────────

def get_plan_review(plan_id: str) -> dict:
    """
    Get pre-generated review for a plan.
    Returns review dict or a generic fallback if plan_id not found.
    """
    review = PLAN_REVIEWS.get(plan_id)
    if review:
        return review

    # Fallback: parse plan_id and construct generic review
    parts = plan_id.split("_")
    try:
        level  = parts[0]
        months = int(parts[1].replace("months", ""))
        hours  = int(parts[2].replace("hours", ""))
        total  = months * hours * 30
    except Exception:
        level, months, hours, total = "beginner", 6, 4, 720

    return {
        "score": 50.0,
        "coverage_pct": 50.0,
        "quality_label": "✅ Moderate",
        "quality_band": "moderate",
        "total_hours": total,
        "subjects_covered": 10,
        "mock_tests": 5,
        "answer_writing_days": 20,
        "readiness": "Moderate preparation",
        "best_for": f"Aspirants with {months}-month timeline and {hours}h daily commitment.",
        "reality_check": "Consistent execution of this plan will produce meaningful preparation.",
        "realistic_outcome": f"With {total} total hours, you'll cover the core syllabus adequately.",
        "mentor_note": "Stay consistent and trust the plan. Consistency beats intensity every time.",
        "phase_highlights": ["Follow the daily plan for best results."],
        "syllabus_coverage": {},
        "suggestions": ["Follow the daily plan", "Write answers weekly", "Take mock tests monthly"],
        "better_suggestion": None,
        "is_recommended": True,
    }


def get_all_plan_ids() -> list[str]:
    """Return all 48 plan IDs."""
    return list(PLAN_REVIEWS.keys())


def get_top_plans_by_level(level: str, top_n: int = 3) -> list[dict]:
    """Return the top N plans for a given level, sorted by score."""
    level_plans = [
        (pid, review) for pid, review in PLAN_REVIEWS.items()
        if pid.startswith(level)
    ]
    level_plans.sort(key=lambda x: x[1]["score"], reverse=True)
    return [{"plan_id": pid, **rev} for pid, rev in level_plans[:top_n]]


def get_best_plan_suggestion(level: str, current_months: int, current_hours: int) -> dict | None:
    """
    Get the better suggestion for a given combination.
    Returns the review dict of the suggested plan, or None if current is optimal.
    """
    current_id = f"{level}_{current_months}months_{current_hours}hours"
    review = PLAN_REVIEWS.get(current_id)
    if not review:
        return None
    suggestion = review.get("better_suggestion")
    if not suggestion:
        return None
    suggested_id = f"{level}_{suggestion['timeline']}months_{suggestion['hours']}hours"
    return PLAN_REVIEWS.get(suggested_id)
