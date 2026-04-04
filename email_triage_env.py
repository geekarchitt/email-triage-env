import random
from typing import Optional
from pydantic import BaseModel

# ── Typed Models (required by OpenEnv spec) ──────────────────────────────────

class EmailObservation(BaseModel):
    email_id: str
    subject: str
    body: str
    sender: str
    task: str  # which task is active: categorize / prioritize / full_triage

class EmailAction(BaseModel):
    category: str          # "urgent", "normal", "spam"
    priority: int          # 1 (highest) to 5 (lowest)
    action: str            # "reply", "archive", "delete", "escalate"

class EmailReward(BaseModel):
    score: float           # 0.0 to 1.0
    breakdown: dict        # shows partial scores

# ── Sample Emails Dataset ─────────────────────────────────────────────────────

EMAILS = [
    {
        "email_id": "e001",
        "subject": "URGENT: Server is down in production",
        "body": "Our main server crashed 10 minutes ago. Customers cannot access the app. Need immediate help.",
        "sender": "ops-team@company.com",
        "correct_category": "urgent",
        "correct_priority": 1,
        "correct_action": "escalate"
    },
    {
        "email_id": "e002",
        "subject": "Congratulations! You won $1,000,000",
        "body": "Click here to claim your prize. Limited time offer!",
        "sender": "noreply@totallylegit.xyz",
        "correct_category": "spam",
        "correct_priority": 5,
        "correct_action": "delete"
    },
    {
        "email_id": "e003",
        "subject": "Q3 report ready for review",
        "body": "Hi, the Q3 financial report is ready. Please review when you get a chance.",
        "sender": "finance@company.com",
        "correct_category": "normal",
        "correct_priority": 3,
        "correct_action": "reply"
    },
    {
        "email_id": "e004",
        "subject": "Re: Meeting tomorrow",
        "body": "Just confirming our 10am meeting is still on. Let me know if you need to reschedule.",
        "sender": "colleague@company.com",
        "correct_category": "normal",
        "correct_priority": 2,
        "correct_action": "reply"
    },
    {
        "email_id": "e005",
        "subject": "Security breach detected",
        "body": "Our monitoring system detected unauthorized access attempts on your account. Immediate action required.",
        "sender": "security@company.com",
        "correct_category": "urgent",
        "correct_priority": 1,
        "correct_action": "escalate"
    },
    {
        "email_id": "e006",
        "subject": "Newsletter: Tips for productivity",
        "body": "Here are 5 tips to boost your productivity this week...",
        "sender": "newsletter@productivity.io",
        "correct_category": "spam",
        "correct_priority": 5,
        "correct_action": "archive"
    },
]

# ── The Environment Class ─────────────────────────────────────────────────────

class EmailTriageEnv:
    def __init__(self, task: str = "categorize"):
        assert task in ("categorize", "prioritize", "full_triage"), \
            "task must be: categorize, prioritize, or full_triage"
        self.task = task
        self.current_email = None
        self.done = False
        self.step_count = 0

    def reset(self) -> EmailObservation:
        """Start a new episode with a random email."""
        self.current_email = random.choice(EMAILS)
        self.done = False
        self.step_count = 0
        return EmailObservation(
            email_id=self.current_email["email_id"],
            subject=self.current_email["subject"],
            body=self.current_email["body"],
            sender=self.current_email["sender"],
            task=self.task
        )

    def step(self, action: EmailAction) -> dict:
        """Agent submits a triage decision. Returns reward + next state."""
        if self.done:
            raise RuntimeError("Episode is done. Call reset() first.")

        reward_obj = self._grade(action)
        self.done = True  # one email = one episode
        self.step_count += 1

        return {
            "observation": EmailObservation(
                email_id=self.current_email["email_id"],
                subject=self.current_email["subject"],
                body=self.current_email["body"],
                sender=self.current_email["sender"],
                task=self.task
            ),
            "reward": reward_obj.score,
            "done": self.done,
            "info": {"breakdown": reward_obj.breakdown}
        }

    def state(self) -> dict:
        """Returns current environment state."""
        return {
            "task": self.task,
            "step_count": self.step_count,
            "done": self.done,
            "current_email_id": self.current_email["email_id"] if self.current_email else None
        }

    def _grade(self, action: EmailAction) -> EmailReward:
        """Score the agent's action with partial credit."""
        email = self.current_email
        breakdown = {}
        total = 0.0

        # ── Task 1: categorize (worth 100% of score) ─────────────────────────
        cat_correct = action.category == email["correct_category"]
        breakdown["category"] = 1.0 if cat_correct else 0.0

        if self.task == "categorize":
            total = breakdown["category"]

        # ── Task 2: prioritize (category 50% + priority 50%) ─────────────────
        elif self.task == "prioritize":
            pri_diff = abs(action.priority - email["correct_priority"])
            pri_score = max(0.0, 1.0 - (pri_diff * 0.25))  # -0.25 per level off
            breakdown["priority"] = round(pri_score, 2)
            total = (breakdown["category"] * 0.5) + (breakdown["priority"] * 0.5)

        # ── Task 3: full_triage (category 40% + priority 30% + action 30%) ───
        elif self.task == "full_triage":
            pri_diff = abs(action.priority - email["correct_priority"])
            pri_score = max(0.0, 1.0 - (pri_diff * 0.25))
            act_correct = action.action == email["correct_action"]
            breakdown["priority"] = round(pri_score, 2)
            breakdown["action"] = 1.0 if act_correct else 0.0
            total = (
                breakdown["category"] * 0.4 +
                breakdown["priority"] * 0.3 +
                breakdown["action"] * 0.3
            )

        return EmailReward(score=round(total, 2), breakdown=breakdown)