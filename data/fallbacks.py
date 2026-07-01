"""
data/fallbacks.py — UPSC Master Bot Hardcoded Fallbacks
=========================================================
All text content that displays when AI is unavailable.
Bot NEVER shows empty screens — always has something useful.
"""

# ── Welcome & Onboarding ───────────────────────────────────────────────────────

WELCOME_TEXT = """🇮🇳 <b>Welcome to UPSC Master Bot</b>

Your AI-powered Civil Services preparation companion — built for serious aspirants.

<b>What you get:</b>
• 48 personalised study plans (3 to 24 months)
• Daily tasks with built-in revision scheduling
• AI answer evaluation (Prelims + Mains)
• Real-time current affairs digest
• Mock tests with performance analytics
• Streak tracking + XP rewards system

Let's set up your personalised plan in <b>5 quick steps</b>.
Takes less than 2 minutes. 👇"""

SETUP_DONE_TEXT = """✅ <b>Your UPSC Command Centre is Ready!</b>

Your personalised plan has been activated.

<b>Start here:</b>
• Tap <b>📚 Today's Mission</b> for Day 1
• Complete daily tasks to build your streak
• Use <b>✍️ Answer Writing</b> to practise Mains

<i>Tip: Come back every day — even 30 minutes counts.</i>"""

# ── Subject options for onboarding ────────────────────────────────────────────

OPTIONAL_SUBJECTS = [
    ("📜 History", "History"),
    ("🌍 Geography", "Geography"),
    ("⚖️ Public Administration", "Public Administration"),
    ("💡 Political Science & IR", "Political Science & IR"),
    ("📊 Sociology", "Sociology"),
    ("🧮 Economics", "Economics"),
    ("🔬 Physics", "Physics"),
    ("🧪 Chemistry", "Chemistry"),
    ("🌱 Agriculture", "Agriculture"),
    ("🦁 Zoology", "Zoology"),
    ("⚡ Electrical Engineering", "Electrical Engineering"),
    ("💻 Computer Science", "Computer Science"),
    ("⚙️ Mechanical Engineering", "Mechanical Engineering"),
    ("🏛️ Civil Engineering", "Civil Engineering"),
    ("📐 Mathematics", "Mathematics"),
    ("🏥 Medical Science", "Medical Science"),
    ("🌿 Botany", "Botany"),
    ("📚 Philosophy", "Philosophy"),
    ("🧠 Psychology", "Psychology"),
    ("⚖️ Law", "Law"),
    ("✍️ Literature (any)", "Literature"),
    ("🤔 Undecided", "Undecided"),
]

WEAK_SUBJECT_OPTIONS = [
    ("📜 History", "History"),
    ("🌍 Geography", "Geography"),
    ("⚖️ Polity", "Polity"),
    ("💰 Economy", "Economy"),
    ("🌱 Environment", "Environment"),
    ("🔬 Science & Technology", "Science & Technology"),
    ("🌐 International Relations", "International Relations"),
    ("🤝 Ethics & GS4", "Ethics & GS4"),
    ("📰 Current Affairs", "Current Affairs"),
    ("✍️ Answer Writing", "Answer Writing"),
    ("📝 Essay", "Essay"),
    ("🧮 CSAT", "CSAT"),
]

# ── Dashboard texts ────────────────────────────────────────────────────────────

DASHBOARD_DESCRIPTION = {
    "tasks":          "📚 Study today's mission — tasks, topics, revision targets",
    "revision":       "🔄 See topics due for revision based on spaced repetition",
    "answer_writing": "✍️ Practice Mains answers with AI scoring (Prelims + Mains)",
    "mock":           "🧪 Take subject-wise MCQ tests & full Prelims mocks",
    "current_affairs":"📰 Daily current affairs digest with UPSC relevance",
    "essay":          "📝 Essay topic brainstorm, outline builder & evaluation",
    "ethics":         "⚖️ Ethics case studies with 7-step framework evaluation",
    "optional":       "🎯 Optional subject strategies, resources & daily tasks",
    "progress":       "📊 Track your syllabus coverage, XP & weekly performance",
    "streak":         "🔥 Your consistency score, badges & leaderboard",
    "ai_planner":     "🤖 AI study planner — ask any UPSC question",
    "settings":       "⚙️ Notifications, plan change, vacation mode & preferences",
}

# ── Current affairs topics (displayed when AI unavailable) ────────────────────

CA_TOPICS = [
    "Economy & Budget", "Environment & Climate", "Science & Technology",
    "International Relations", "Polity & Governance", "Social Issues",
    "Security & Defence", "Infrastructure & Urban", "Agriculture",
    "Health & Education", "Space & Nuclear", "Awards & Rankings",
]

CA_SOURCES = [
    "📰 <b>The Hindu</b> — Hindu.com (daily newspaper)",
    "📋 <b>PIB</b> — pib.gov.in (government schemes & policies)",
    "📊 <b>Economic Survey</b> — Download from finance.gov.in",
    "📗 <b>Yojana Magazine</b> — Available at yojana.gov.in",
    "📘 <b>Vision IAS Monthly</b> — visionias.in",
    "📙 <b>Insights IAS</b> — insightsonindia.com",
    "📱 <b>UPSC Official</b> — upsc.gov.in (syllabi, notifications)",
]

CA_FALLBACK = """📰 <b>Current Affairs — Today's Framework</b>

AI summary unavailable. Use these proven sources:

<b>Must-read today:</b>
• The Hindu — Page 1, Editorial, National, Business
• PIB (pib.gov.in) — Recent government schemes
• Environment news — Down to Earth or CSE website

<b>UPSC CA Formula:</b>
For each news item, ask:
1️⃣ What happened? (Facts)
2️⃣ Why does it matter for India? (Significance)
3️⃣ Which GS paper does this link to? (Relevance)
4️⃣ What policy/scheme is involved? (Governance angle)

<i>This framework turns any news article into a UPSC answer.</i>"""

# ── Mock test questions bank (basic set) ─────────────────────────────────────

SAMPLE_MCQ_POLITY = [
    {
        "q": "Which Article of the Constitution provides for the Right to Constitutional Remedies?",
        "options": ["Article 30", "Article 32", "Article 35", "Article 36"],
        "answer": 1,
        "exp": "Article 32 — the 'Heart and Soul of the Constitution' per Dr. Ambedkar — guarantees the right to move the Supreme Court for enforcement of Fundamental Rights.",
        "subject": "Polity",
    },
    {
        "q": "The Directive Principles of State Policy are contained in which part of the Constitution?",
        "options": ["Part III", "Part IV", "Part IVA", "Part V"],
        "answer": 1,
        "exp": "DPSPs are in Part IV (Articles 36-51). They are non-justiciable but fundamental to governance.",
        "subject": "Polity",
    },
    {
        "q": "Which schedule of the Constitution deals with the allocation of seats in Rajya Sabha?",
        "options": ["First Schedule", "Third Schedule", "Fourth Schedule", "Seventh Schedule"],
        "answer": 2,
        "exp": "Fourth Schedule: allocation of seats in the Council of States (Rajya Sabha) for States/UTs.",
        "subject": "Polity",
    },
    {
        "q": "The concept of 'Basic Structure' was established in which landmark case?",
        "options": ["Golak Nath Case", "Kesavananda Bharati Case", "Minerva Mills Case", "Maneka Gandhi Case"],
        "answer": 1,
        "exp": "Kesavananda Bharati v. State of Kerala (1973): Parliament cannot alter the 'basic structure' of the Constitution.",
        "subject": "Polity",
    },
    {
        "q": "Money Bills can be introduced in which House?",
        "options": ["Rajya Sabha only", "Either House", "Lok Sabha only", "Joint sitting only"],
        "answer": 2,
        "exp": "Money Bills (Article 110) can only be introduced in Lok Sabha on the recommendation of the President.",
        "subject": "Polity",
    },
]

SAMPLE_MCQ_HISTORY = [
    {
        "q": "The Dandi March (Salt March) began on which date?",
        "options": ["12 March 1930", "6 April 1930", "26 January 1930", "15 August 1930"],
        "answer": 0,
        "exp": "Gandhi began the Dandi March from Sabarmati Ashram on 12 March 1930, reaching Dandi on 5 April to make salt and defy the Salt Laws.",
        "subject": "History",
    },
    {
        "q": "Who founded the Indian National Congress in 1885?",
        "options": ["Dadabhai Naoroji", "Bal Gangadhar Tilak", "A.O. Hume", "Gopal Krishna Gokhale"],
        "answer": 2,
        "exp": "Allan Octavian Hume, a retired British civil servant, founded the INC in 1885. The first session was held in Bombay.",
        "subject": "History",
    },
    {
        "q": "The Permanent Settlement was introduced by which Governor-General?",
        "options": ["Warren Hastings", "Lord Cornwallis", "Lord Wellesley", "Lord Dalhousie"],
        "answer": 1,
        "exp": "Permanent Settlement (1793) by Lord Cornwallis fixed land revenue permanently with zamindars, who became revenue collectors.",
        "subject": "History",
    },
    {
        "q": "The Revolt of 1857 began at which place?",
        "options": ["Meerut", "Lucknow", "Delhi", "Kanpur"],
        "answer": 0,
        "exp": "The Revolt began in Meerut on 10 May 1857 when sepoys refused to use the new Enfield cartridges and mutinied.",
        "subject": "History",
    },
    {
        "q": "Simon Commission visited India in which year?",
        "options": ["1925", "1927", "1928", "1930"],
        "answer": 2,
        "exp": "Simon Commission (1928) — appointed in 1927, arrived in India in 1928. Boycotted by Congress as it had no Indian member.",
        "subject": "History",
    },
]

SAMPLE_MCQ_GEOGRAPHY = [
    {
        "q": "Which of the following is the longest river of India?",
        "options": ["Godavari", "Indus", "Ganga", "Krishna"],
        "answer": 1,
        "exp": "The Indus (3,180 km in India + Pakistan) is the longest, but only ~709 km flows through India. The Ganga (2,525 km) is the longest river flowing entirely within India.",
        "subject": "Geography",
    },
    {
        "q": "The Tropic of Cancer passes through how many Indian states?",
        "options": ["6", "7", "8", "9"],
        "answer": 2,
        "exp": "The Tropic of Cancer passes through 8 Indian states: Rajasthan, Gujarat, MP, Chhattisgarh, Jharkhand, West Bengal, Tripura, and Mizoram.",
        "subject": "Geography",
    },
    {
        "q": "Which is the highest peak of the Western Ghats?",
        "options": ["Anai Mudi", "Doddabetta", "Vavul Mala", "Mullayanagiri"],
        "answer": 0,
        "exp": "Anai Mudi (2,695 m) in Kerala is the highest peak of the Western Ghats and also of Peninsular India (outside the Himalayas).",
        "subject": "Geography",
    },
    {
        "q": "Tehri Dam is located on which river?",
        "options": ["Beas", "Chenab", "Bhagirathi", "Alaknanda"],
        "answer": 2,
        "exp": "Tehri Dam is located on the Bhagirathi river (a major tributary of the Ganga) in Uttarakhand. It is India's tallest dam.",
        "subject": "Geography",
    },
    {
        "q": "Which state has the longest coastline in India?",
        "options": ["Tamil Nadu", "Maharashtra", "Andhra Pradesh", "Gujarat"],
        "answer": 3,
        "exp": "Gujarat has the longest coastline (~1,600 km) among Indian states, due to its irregular indented coasts and the Gulf of Khambhat.",
        "subject": "Geography",
    },
]

# Combine all MCQs
ALL_SAMPLE_MCQ = SAMPLE_MCQ_POLITY + SAMPLE_MCQ_HISTORY + SAMPLE_MCQ_GEOGRAPHY

SUBJECT_MCQ = {
    "Polity":    SAMPLE_MCQ_POLITY,
    "History":   SAMPLE_MCQ_HISTORY,
    "Geography": SAMPLE_MCQ_GEOGRAPHY,
}

# ── Essay topics ───────────────────────────────────────────────────────────────

ESSAY_TOPICS = [
    # GS1-type
    "Women empowerment is a prerequisite for inclusive development",
    "The real voyage of discovery consists not in seeking new landscapes but in having new eyes",
    "Forests are the world's air conditioning system — the lungs of the planet",
    "Has urbanisation led to the weakening of India's cultural heritage?",
    "Cooperative federalism: myth or reality?",
    "The values of past define the vision for the future",
    # GS2-type
    "Justice must reach the poor",
    "Social media is making democracy more fragile",
    "Can capitalism bring inclusive growth?",
    "The need for well-educated diplomats in a multipolar world",
    "Agriculture is the backbone of India — needs urgent reform",
    # GS4-type
    "Attitude is a little thing that makes a big difference",
    "The good of the people is the greatest law",
    "A life spent in making mistakes is more honourable than a life spent doing nothing",
    "Discipline is the bridge between goals and accomplishment",
    "Technology as the great equalizer",
    # Mixed themes
    "India's soft power in a fractured world",
    "Jobless growth is a threat to social stability",
    "Climate justice and equity: India's responsibility",
    "The digital divide widens the gap between haves and have-nots",
]

# ── Ethics case studies (7-step framework) ────────────────────────────────────

ETHICS_CASES = [
    {
        "title": "The Honest Officer",
        "scenario": (
            "You are an IAS officer posted as District Collector. Your senior (a Secretary-rank officer) "
            "asks you to approve a contractor's bill worth ₹50 lakh for work that was clearly substandard. "
            "The contractor has political connections. Your refusal may harm your career. "
            "Your approval would deprive the public of quality infrastructure."
        ),
        "keywords": ["integrity", "pressure", "public interest", "career", "political nexus"],
        "gist": "Conflict between personal career safety and public duty/integrity",
    },
    {
        "title": "Whistleblower's Dilemma",
        "scenario": (
            "As an IPS officer, you discover that your department head is involved in a major scam "
            "affecting thousands of farmers. Reporting it will end your career advancement. "
            "Not reporting makes you complicit. You have a family to support."
        ),
        "keywords": ["whistleblowing", "loyalty", "courage", "family", "corruption"],
        "gist": "Personal loyalty vs institutional integrity vs social responsibility",
    },
    {
        "title": "The Disaster Response",
        "scenario": (
            "A cyclone has hit your district. You have limited rescue resources. "
            "You must choose between rescuing a village with 200 poor farmers vs. "
            "a flood-hit town with 50 people including some VIPs. "
            "Your superior is pressuring you to prioritise the town."
        ),
        "keywords": ["impartiality", "equity", "utilitarian", "pressure", "triage"],
        "gist": "Utilitarian decision-making under pressure with impartiality challenge",
    },
    {
        "title": "The Promotion Dilemma",
        "scenario": (
            "You are in a selection committee and your close colleague, who is also your subordinate, "
            "is competing for a promotion against a better-qualified candidate. "
            "Your colleague has helped you personally in the past. "
            "The selection is entirely within your discretion."
        ),
        "keywords": ["conflict of interest", "meritocracy", "gratitude", "fairness", "bias"],
        "gist": "Personal gratitude vs merit-based selection — conflict of interest",
    },
]

# ── UPSC Trivia (static, 50 entries for daily rotation) ──────────────────────

DAILY_TRIVIA = [
    {
        "q": "What year was the first UPSC Civil Services Examination held after Independence?",
        "a": "1947 — the first post-Independence ICS exam was held in 1947. The exam was fully Indianised and renamed IAS from 1948.",
        "tag": "#History",
    },
    {
        "q": "Which country was the first to conduct a merit-based civil service examination?",
        "a": "China — the Imperial Examination (Keju) system, begun around 605 CE under the Sui Dynasty, is the world's first merit-based civil service exam.",
        "tag": "#GS2",
    },
    {
        "q": "How many days does the UPSC Mains examination spread across?",
        "a": "5 days — Mains has 9 papers (GS1-GS4, Essay, 2 Optional papers, 1 language paper, 1 English paper) spread over 5 days.",
        "tag": "#UPSC",
    },
    {
        "q": "What is the maximum number of attempts for General category in UPSC CSE?",
        "a": "6 attempts — General category candidates can attempt 6 times between ages 21-32. OBC: 9 attempts. SC/ST: unlimited till age 37.",
        "tag": "#UPSC",
    },
    {
        "q": "The UPSC was established by which article of the Constitution?",
        "a": "Article 315 — UPSC is established under Article 315. It is a constitutional body. The Chairman and members are appointed by the President.",
        "tag": "#Polity",
    },
    {
        "q": "Which schedule of the Indian Constitution lists the languages in the 8th schedule?",
        "a": "Currently 22 languages are listed in the 8th Schedule, including Assamese, Bengali, Bodo, Dogri, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Meitei, Marathi, Nepali, Odia, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu, and Urdu.",
        "tag": "#Polity",
    },
    {
        "q": "What does 'Concurrent List' in the 7th Schedule of the Constitution mean?",
        "a": "Concurrent List: both Centre and State can legislate on these subjects. In case of conflict, Centre's law prevails. Includes subjects like education, forests, trade unions, criminal law.",
        "tag": "#Polity",
    },
    {
        "q": "Which river forms the Chilika Lake in Odisha?",
        "a": "Chilika Lake is formed by the delta of the Daya River. It is India's largest brackish water lagoon and Asia's largest coastal lagoon — a Ramsar site since 1981.",
        "tag": "#Geography",
    },
    {
        "q": "What is the full form of NITI Aayog and when was it established?",
        "a": "National Institution for Transforming India — established 1 January 2015, replacing the Planning Commission. It serves as a policy think-tank for the Government of India.",
        "tag": "#Economy",
    },
    {
        "q": "Which committee recommended the three-tier Panchayati Raj system?",
        "a": "Balwant Rai Mehta Committee (1957) recommended three-tier Panchayati Raj: Gram Panchayat (village), Panchayat Samiti (block), Zila Parishad (district).",
        "tag": "#Polity",
    },
    {
        "q": "What is the 'Green Revolution' and when did it begin in India?",
        "a": "Green Revolution began in India in the late 1960s under the leadership of M.S. Swaminathan. It introduced HYV seeds, irrigation, and chemical fertilisers — dramatically increasing wheat and rice production.",
        "tag": "#Economy",
    },
    {
        "q": "The 'Doctrine of Lapse' was introduced by which Governor-General?",
        "a": "Lord Dalhousie (1848-1856) introduced the Doctrine of Lapse — states without a natural male heir would be annexed by the British. It was a major cause of the 1857 Revolt.",
        "tag": "#History",
    },
    {
        "q": "What is the 'Van Gujjars' issue in Indian environmental governance?",
        "a": "Van Gujjars are a nomadic pastoralist community of J&K and Uttarakhand. The Forest Rights Act (2006) conflict arises between their traditional rights to forest lands and conservation objectives of reserved forests.",
        "tag": "#Environment",
    },
    {
        "q": "What is the 'Western Disturbance' and how does it affect India?",
        "a": "Western Disturbances are eastward-moving extratropical cyclones originating in the Mediterranean. They bring winter rainfall to Northwest India (Punjab, Haryana, HP, J&K) — critical for Rabi crops, especially wheat.",
        "tag": "#Geography",
    },
    {
        "q": "What is 'Mission Shakti' in the context of India's space programme?",
        "a": "Mission Shakti (27 March 2019) was India's ASAT (Anti-Satellite Weapon) test that destroyed a live Indian satellite in Low Earth Orbit. India became the 4th country to demonstrate this capability after USA, Russia, China.",
        "tag": "#S&T",
    },
]

# ── Help texts ─────────────────────────────────────────────────────────────────

HELP_TEXT = """📖 <b>UPSC Master Bot — Complete Guide</b>

<b>Core Features:</b>
📚 <b>Today's Mission</b> — Daily study tasks from your plan
🔄 <b>Revision</b> — Auto-scheduled revision reminders (spaced repetition)
✍️ <b>Answer Writing</b> — Mains practice with AI rubric evaluation
🧪 <b>Mock Test</b> — Subject MCQs + full Prelims practice
📰 <b>Current Affairs</b> — Daily UPSC-relevant news digest
📝 <b>Essay</b> — Topic ideas, outlines, evaluation
⚖️ <b>Ethics</b> — Case studies with 7-step framework
🎯 <b>Optional</b> — Your optional subject resources
📊 <b>Progress</b> — Competency tracking + XP analytics
🔥 <b>Streak</b> — Consistency rewards + leaderboard
🤖 <b>AI Planner</b> — Ask any UPSC question

<b>Commands:</b>
/start — Launch bot / return to home
/help — This help message
/reset — Change your study plan
/admin — Admin panel (admins only)

<b>XP System:</b>
• Complete day: +50 XP
• Write answer: +20 XP
• Mock test: +25 XP
• 7-day streak: +100 XP
• 30-day streak: +500 XP

<b>Ranks:</b>
🌱 Aspirant → 📚 Scholar → 🎯 Strategist → ⚔️ Warrior → 🏆 Topper

<b>Tips:</b>
• Use the bot daily — even 10 minutes counts
• Complete tasks in order for spaced repetition to work
• Answer writing is your biggest Mains advantage
• Review every mock test answer — scores without review are wasted"""

# ── Study resources ────────────────────────────────────────────────────────────

RESOURCES = {
    "History": {
        "Prelims": ["Spectrum Modern History (R. Rajasekaran)", "Tamil Nadu Board 12th History", "NCERT Class 6-12 History"],
        "Mains":   ["Bipin Chandra — India's Struggle for Independence", "R.C. Majumdar — British India History", "NCERT Old + New both"],
    },
    "Polity": {
        "Prelims": ["M. Laxmikanth — Indian Polity (5th/6th edition)", "D.D. Basu — Introduction to the Constitution"],
        "Mains":   ["Laxmikanth (primary)", "Constitutional Assembly Debates excerpts", "PRS Legislative Research"],
    },
    "Geography": {
        "Prelims": ["NCERT Class 6-12 Geography", "Goh Cheng Leong — Physical Geography", "Orient Black Swan Atlas"],
        "Mains":   ["Majid Husain — Geography of India", "G.C. Leong (physical geo)", "NCERT Class 11 (both India + World)"],
    },
    "Economy": {
        "Prelims": ["NCERT Class 11-12 Economics", "Ramesh Singh — Indian Economy"],
        "Mains":   ["Economic Survey (current year)", "Union Budget highlights", "Ramesh Singh", "EPW key articles"],
    },
    "Environment": {
        "Prelims": ["Shankar IAS Environment", "NCERT Class 11 Biology (ecology chapters)"],
        "Mains":   ["Shankar IAS", "Down to Earth magazine", "IPCC reports summary", "MoEFCC notifications"],
    },
    "Ethics": {
        "Prelims": ["Ethics is not directly tested in Prelims"],
        "Mains":   ["G. Subba Rao — Ethics, Integrity, Aptitude", "Lexicon for Ethics", "ARC 4th report (Ethics)", "Case study banks"],
    },
    "Science & Technology": {
        "Prelims": ["Ravi P. Agrahari — Science & Technology", "The Hindu S&T section"],
        "Mains":   ["PIB for government science schemes", "India Year Book S&T section", "DST/ISRO official websites"],
    },
    "International Relations": {
        "Prelims": ["NCERT Class 12 Political Science Part 2", "The Hindu International section"],
        "Mains":   ["Ministry of External Affairs Annual Report", "Rajya Sabha TV discussions", "Carnegie Endowment articles"],
    },
}
