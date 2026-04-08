import random
from pydantic import BaseModel
from typing import Optional


class EmailObservation(BaseModel):
    email_id: str
    subject: str
    body: str
    sender: str
    task: str


class EmailAction(BaseModel):
    category: str
    priority: int
    action: str


class EmailReward(BaseModel):
    score: float
    breakdown: dict


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


class EmailTriageEnv:
    def __init__(self, task: str = "categorize"):
        assert task in ("categorize", "prioritize", "full_triage")
        self.task = task
        self.current_email = None
        self.done = False
        self.step_count = 0

    def reset(self) -> EmailObservation:
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
        if self.done:
            raise RuntimeError("Episode is done. Call reset() first.")
        reward_obj = self._grade(action)
        self.done = True
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
        return {
            "task": self.task,
            "step_count": self.step_count,
            "done": self.done,
            "current_email_id": self.current_email["email_id"] if self.current_email else None
        }

    def _grade(self, action: EmailAction) -> EmailReward:
        email = self.current_email
        breakdown = {}

        cat_correct = action.category == email["correct_category"]
        cat_score = 0.85 if cat_correct else 0.15

        if self.task == "categorize":
            total = cat_score

        elif self.task == "prioritize":
            pri_diff = abs(action.priority - email["correct_priority"])
            pri_score = max(0.15, min(0.85, round(0.85 - (pri_diff * 0.15), 2)))
            breakdown["priority"] = pri_score
            total = round((cat_score * 0.5) + (pri_score * 0.5), 2)

        elif self.task == "full_triage":
            pri_diff = abs(action.priority - email["correct_priority"])
            pri_score = max(0.15, min(0.85, round(0.85 - (pri_diff * 0.15), 2)))
            act_correct = action.action == email["correct_action"]
            act_score = 0.85 if act_correct else 0.15
            breakdown["priority"] = pri_score
            breakdown["action"] = act_score
            total = round((cat_score * 0.4) + (pri_score * 0.3) + (act_score * 0.3), 2)

        else:
            total = 0.5

        breakdown["category"] = cat_score
        total = max(0.15, min(0.85, total))
        return EmailReward(score=total, breakdown=breakdown)