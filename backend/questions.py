"""
questions.py
------------
Quiz question bank and scoring engine for CareerCompass.
Made by stealthcoderX | All rights reserved.

Career categories:
    software  → Software / Full-Stack Engineer
    data      → Data Scientist / AI Engineer
    design    → UX/UI Designer
    business  → Product Manager / Business Analyst
    security  → Cybersecurity Specialist
"""

from __future__ import annotations
from typing import Any

# ── Career display labels ─────────────────────────────────────────────────────
CAREER_LABELS: dict[str, str] = {
    "software": "Software Engineer",
    "data":     "Data Scientist",
    "design":   "UX/UI Designer",
    "business": "Product Manager",
    "security": "Cybersecurity Specialist",
}

CAREER_ICONS: dict[str, str] = {
    "software": "💻",
    "data":     "📊",
    "design":   "🎨",
    "business": "📈",
    "security": "🛡️",
}

CAREER_DESCRIPTIONS: dict[str, str] = {
    "software": (
        "You think in systems, love building scalable products, and get energised "
        "by elegant code. Software Engineering channels your analytical drive and "
        "creative problem-solving into real-world applications used by millions."
    ),
    "data": (
        "You are drawn to patterns hiding inside complexity. Data Science lets you "
        "combine statistical rigour with curiosity to answer questions that change "
        "how organisations make decisions and build intelligent systems."
    ),
    "design": (
        "You see the world through the lens of human experience. UX/UI Design gives "
        "you a canvas to translate empathy and visual thinking into interfaces that "
        "delight users and make technology feel intuitive and beautiful."
    ),
    "business": (
        "You connect strategy with execution and people with purpose. Product "
        "Management is where your leadership, communication, and analytical skills "
        "come together to create measurable business impact at scale."
    ),
    "security": (
        "You think like an attacker to defend like a pro. Cybersecurity rewards your "
        "detail-oriented mindset and passion for keeping systems, data, and people "
        "safe in an ever-evolving digital threat landscape."
    ),
}

CAREER_TRAITS: dict[str, list[tuple[str, str]]] = {
    "software": [("⚡", "Logical"), ("🔭", "Curious"), ("🛠️", "Builder"),
                 ("🧩", "Systematic"), ("🔍", "Detail-oriented"), ("🚀", "Driven")],
    "data":     [("📊", "Analytical"), ("🔬", "Scientific"), ("🧮", "Numerical"),
                 ("🔎", "Inquisitive"), ("💡", "Insightful"), ("🎯", "Precise")],
    "design":   [("🎨", "Creative"), ("🤝", "Empathetic"), ("👁️", "Visual"),
                 ("✨", "Aesthetic"), ("🧠", "Intuitive"), ("🌟", "Expressive")],
    "business": [("🏆", "Strategic"), ("📣", "Communicator"), ("🤝", "Collaborative"),
                 ("📈", "Growth-minded"), ("🌐", "Big-picture"), ("💼", "Leader")],
    "security": [("🛡️", "Protective"), ("🕵️", "Investigative"), ("🔒", "Security-focused"),
                 ("⚡", "Alert"), ("🧩", "Methodical"), ("🎯", "Focused")],
}

# ── Question bank ─────────────────────────────────────────────────────────────
# Each question has:
#   id       : int
#   text     : str  – the question shown to the user
#   category : str  – grouping label shown as a badge
#   options  : list[str]  – exactly 4 answer choices
#   scores   : list[dict] – parallel to options; each dict maps category→points

QUESTIONS: list[dict[str, Any]] = [
    {
        "id": 1,
        "text": "When you face a complex problem, what is your natural first step?",
        "category": "Problem Solving",
        "options": [
            "Break it into logical steps and write an algorithm",
            "Gather data and look for patterns or trends",
            "Sketch a user flow to understand the human side",
            "Map out stakeholder impact and business risk",
        ],
        "scores": [
            {"software": 3, "security": 1},
            {"data": 3, "security": 1},
            {"design": 3, "business": 1},
            {"business": 3, "design": 1},
        ],
    },
    {
        "id": 2,
        "text": "Which weekend project would you find most exciting?",
        "category": "Personal Interest",
        "options": [
            "Building a web app or automating a repetitive task",
            "Analysing a dataset and creating interactive charts",
            "Redesigning the UI of an app you find frustrating",
            "Researching a market and writing a business strategy",
        ],
        "scores": [
            {"software": 3, "security": 1},
            {"data": 3, "business": 1},
            {"design": 3, "data": 1},
            {"business": 3, "design": 1},
        ],
    },
    {
        "id": 3,
        "text": "In a group project, which role do you naturally take?",
        "category": "Team Dynamics",
        "options": [
            "The builder who implements the core features",
            "The analyst who validates ideas with evidence",
            "The designer who owns look, feel, and flow",
            "The coordinator who drives timeline and alignment",
        ],
        "scores": [
            {"software": 3, "security": 1},
            {"data": 3, "business": 1},
            {"design": 3, "data": 1},
            {"business": 3, "design": 1},
        ],
    },
    {
        "id": 4,
        "text": "How do you feel about working with statistics and data models?",
        "category": "Data Affinity",
        "options": [
            "I enjoy it when it helps optimise system performance",
            "It is my primary craft — notebooks and dashboards are home",
            "I use it lightly, mainly for A/B testing design decisions",
            "I rely on it to validate product hypotheses and KPIs",
        ],
        "scores": [
            {"software": 2, "security": 2},
            {"data": 3, "business": 1},
            {"design": 2, "data": 2},
            {"business": 3, "data": 1},
        ],
    },
    {
        "id": 5,
        "text": "How would you describe your relationship with computer security?",
        "category": "Security Mindset",
        "options": [
            "I write secure code and think about attack surfaces",
            "I protect data pipelines and sensitive model outputs",
            "I apply privacy-by-design principles in my interfaces",
            "I navigate compliance frameworks like GDPR and ISO 27001",
        ],
        "scores": [
            {"security": 3, "software": 2},
            {"security": 2, "data": 2},
            {"design": 3, "security": 1},
            {"business": 3, "security": 2},
        ],
    },
    {
        "id": 6,
        "text": "Which set of tools would you be most excited to master?",
        "category": "Tooling",
        "options": [
            "Docker, Kubernetes, and a modern backend framework",
            "TensorFlow, PyTorch, and Jupyter Notebooks",
            "Figma, Framer, and usability testing platforms",
            "Jira, Confluence, and OKR tracking dashboards",
        ],
        "scores": [
            {"software": 3, "security": 1},
            {"data": 3, "software": 1},
            {"design": 3, "business": 1},
            {"business": 3, "design": 1},
        ],
    },
    {
        "id": 7,
        "text": "A colleague asks for your input on a major product decision. You:",
        "category": "Decision Making",
        "options": [
            "Assess technical feasibility and flag potential tech debt",
            "Pull historical data before making any recommendation",
            "Ask about the target user persona and their pain points",
            "Frame it as a cost-benefit trade-off on the roadmap",
        ],
        "scores": [
            {"software": 3, "security": 1},
            {"data": 3, "business": 1},
            {"design": 3, "data": 1},
            {"business": 3, "design": 1},
        ],
    },
    {
        "id": 8,
        "text": "How do you prefer to present your work to others?",
        "category": "Communication",
        "options": [
            "A pull request with detailed commit messages and inline docs",
            "An interactive dashboard with annotated charts",
            "A polished prototype or clickable Figma mock-up",
            "An executive summary deck with key metrics and next steps",
        ],
        "scores": [
            {"software": 3, "security": 2},
            {"data": 3, "business": 1},
            {"design": 3, "data": 1},
            {"business": 3, "design": 1},
        ],
    },
    {
        "id": 9,
        "text": "You discover a critical security vulnerability in a live system. You:",
        "category": "Security Response",
        "options": [
            "Patch it immediately, write a regression test, and file a post-mortem",
            "Analyse access logs to quantify the breach impact on data",
            "Alert the team and suggest a user-trust recovery strategy",
            "Draft an incident response plan and escalate to leadership",
        ],
        "scores": [
            {"security": 3, "software": 2},
            {"security": 2, "data": 3},
            {"design": 2, "security": 1},
            {"security": 3, "business": 2},
        ],
    },
    {
        "id": 10,
        "text": "Which academic subject area excites you the most?",
        "category": "Intellectual Interest",
        "options": [
            "Algorithms, operating systems, and distributed computing",
            "Statistics, linear algebra, and machine learning theory",
            "Cognitive psychology, colour theory, and human behaviour",
            "Economics, game theory, and organisational strategy",
        ],
        "scores": [
            {"software": 3, "security": 2},
            {"data": 3, "security": 1},
            {"design": 3, "data": 1},
            {"business": 3, "design": 1},
        ],
    },
    {
        "id": 11,
        "text": "How do you define a successful product launch?",
        "category": "Success Metrics",
        "options": [
            "Zero critical bugs, 99.9% uptime, and fast load times",
            "Data confirms statistically significant improvement in KPIs",
            "Usability tests show high task-completion and NPS scores",
            "Revenue targets met and stakeholders aligned on the roadmap",
        ],
        "scores": [
            {"software": 3, "security": 1},
            {"data": 3, "business": 2},
            {"design": 3, "data": 1},
            {"business": 3, "design": 1},
        ],
    },
    {
        "id": 12,
        "text": "How comfortable are you reading and writing code?",
        "category": "Coding Comfort",
        "options": [
            "Very comfortable — it is my primary day-to-day skill",
            "Comfortable with Python/R for scripting and data analysis",
            "Basic scripting for automation; I prefer design tools",
            "I prefer no-code/low-code tools and clear specifications",
        ],
        "scores": [
            {"software": 3, "security": 2},
            {"data": 3, "software": 1},
            {"design": 2, "security": 1},
            {"business": 3, "design": 1},
        ],
    },
    {
        "id": 13,
        "text": "What motivates you most in a professional environment?",
        "category": "Motivation",
        "options": [
            "Solving hard technical problems nobody has cracked before",
            "Uncovering hidden insights that change how people think",
            "Creating experiences that genuinely delight real users",
            "Building a strategy that scales a business significantly",
        ],
        "scores": [
            {"software": 2, "security": 3},
            {"data": 3, "business": 1},
            {"design": 3, "data": 1},
            {"business": 3, "design": 1},
        ],
    },
    {
        "id": 14,
        "text": "Which scenario describes your ideal working day?",
        "category": "Work Style",
        "options": [
            "Deep-focus coding sessions with some pair programming",
            "Iterating on ML models and evaluating performance metrics",
            "Running user interviews, then translating insights into wireframes",
            "Stakeholder meetings followed by writing a product strategy doc",
        ],
        "scores": [
            {"software": 3, "security": 1},
            {"data": 3, "software": 1},
            {"design": 3, "business": 1},
            {"business": 3, "design": 1},
        ],
    },
    {
        "id": 15,
        "text": "Which emerging technology trend excites you the most?",
        "category": "Future Vision",
        "options": [
            "Edge computing, WebAssembly, and quantum-safe cryptography",
            "Large Language Models, AutoML, and real-time AI pipelines",
            "Immersive AR/VR interfaces and AI-generated design tools",
            "Platform economics, AI governance, and decentralised finance",
        ],
        "scores": [
            {"security": 3, "software": 2},
            {"data": 3, "software": 1},
            {"design": 3, "data": 1},
            {"business": 3, "security": 1},
        ],
    },
]


# ── Scoring engine ────────────────────────────────────────────────────────────

def calculate_result(answers: dict[str, str]) -> tuple[str, dict[str, int]]:
    """
    Compute career category scores from submitted quiz answers.

    Parameters
    ----------
    answers : dict
        Keys are question field names like "q1" … "q15",
        values are stringified answer indices ("0"–"3").

    Returns
    -------
    tuple[str, dict[str, int]]
        (predicted_career_key, full_score_dict)

    Raises
    ------
    ValueError
        If no valid answers are found in the submission.
    """
    score_dict: dict[str, int] = {
        "software": 0,
        "data":     0,
        "design":   0,
        "business": 0,
        "security": 0,
    }

    valid_count = 0

    for question in QUESTIONS:
        key = f"q{question['id']}"
        raw = answers.get(key)
        if raw is None:
            continue
        try:
            idx = int(raw)
        except (ValueError, TypeError):
            continue
        if not (0 <= idx < len(question["options"])):
            continue

        for category, points in question["scores"][idx].items():
            score_dict[category] = score_dict.get(category, 0) + points

        valid_count += 1

    if valid_count == 0:
        raise ValueError("No valid answers found in submission.")

    predicted = max(score_dict, key=score_dict.get)   # type: ignore[arg-type]
    return predicted, score_dict


def get_career_label(key: str) -> str:
    """Return the human-readable career title for a given category key."""
    return CAREER_LABELS.get(key, key.replace("_", " ").title())


def get_score_percentages(score_dict: dict[str, int]) -> dict[str, int]:
    """
    Convert raw scores to percentages (0–100) relative to max possible (45).
    Caps at 99 to avoid showing 100% for any category.
    """
    max_possible = 45  # 15 questions × max 3 pts
    return {
        k: min(int(v / max_possible * 100), 99)
        for k, v in score_dict.items()
    }
