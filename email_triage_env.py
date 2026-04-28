import random
from pydantic import BaseModel
from typing import List


class EmailObservation(BaseModel):
    email_id: str
    subject: str
    body: str
    sender: str
    task: str
    inbox_position: int = 1
    inbox_size: int = 1


class EmailAction(BaseModel):
    category: str
    priority: int
    action: str
    sender_type: str = "internal"
    reply_subject: str = ""


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
        "correct_action": "escalate",
        "correct_sender_type": "internal",
        "correct_reply_subject": "Re: URGENT: Server is down in production"
    },
    {
        "email_id": "e002",
        "subject": "Congratulations! You won $1,000,000",
        "body": "Click here to claim your prize. Limited time offer!",
        "sender": "noreply@totallylegit.xyz",
        "correct_category": "spam",
        "correct_priority": 5,
        "correct_action": "delete",
        "correct_sender_type": "external",
        "correct_reply_subject": ""
    },
    {
        "email_id": "e003",
        "subject": "Q3 report ready for review",
        "body": "Hi, the Q3 financial report is ready. Please review when you get a chance.",
        "sender": "finance@company.com",
        "correct_category": "normal",
        "correct_priority": 3,
        "correct_action": "reply",
        "correct_sender_type": "internal",
        "correct_reply_subject": "Re: Q3 report ready for review"
    },
    {
        "email_id": "e004",
        "subject": "Re: Meeting tomorrow",
        "body": "Just confirming our 10am meeting is still on. Let me know if you need to reschedule.",
        "sender": "colleague@company.com",
        "correct_category": "normal",
        "correct_priority": 2,
        "correct_action": "reply",
        "correct_sender_type": "internal",
        "correct_reply_subject": "Re: Meeting tomorrow"
    },
    {
        "email_id": "e005",
        "subject": "Security breach detected",
        "body": "Our monitoring system detected unauthorized access attempts on your account. Immediate action required.",
        "sender": "security@company.com",
        "correct_category": "urgent",
        "correct_priority": 1,
        "correct_action": "escalate",
        "correct_sender_type": "internal",
        "correct_reply_subject": "Re: Security breach detected"
    },
    {
        "email_id": "e006",
        "subject": "Newsletter: Tips for productivity",
        "body": "Here are 5 tips to boost your productivity this week...",
        "sender": "newsletter@productivity.io",
        "correct_category": "spam",
        "correct_priority": 5,
        "correct_action": "archive",
        "correct_sender_type": "external",
        "correct_reply_subject": ""
    },
    {
        "email_id": "e007",
        "subject": "Invoice #4521 overdue",
        "body": "Your invoice #4521 for $2,400 is 30 days overdue. Please make payment immediately.",
        "sender": "billing@vendor.com",
        "correct_category": "urgent",
        "correct_priority": 2,
        "correct_action": "escalate",
        "correct_sender_type": "external",
        "correct_reply_subject": "Re: Invoice #4521 overdue"
    },
    {
        "email_id": "e008",
        "subject": "Welcome to the team!",
        "body": "Hi! I just joined the engineering team. Looking forward to working with everyone.",
        "sender": "newjoin@company.com",
        "correct_category": "normal",
        "correct_priority": 4,
        "correct_action": "reply",
        "correct_sender_type": "internal",
        "correct_reply_subject": "Re: Welcome to the team!"
    },
    {
        "email_id": "e009",
        "subject": "FREE iPhone 15 - Limited offer",
        "body": "You have been selected to receive a FREE iPhone 15! Click now!",
        "sender": "promo@freeiphonez.net",
        "correct_category": "spam",
        "correct_priority": 5,
        "correct_action": "delete",
        "correct_sender_type": "external",
        "correct_reply_subject": ""
    },
    {
        "email_id": "e010",
        "subject": "Database backup failed",
        "body": "Automated backup for production database failed at 03:00 AM. Manual intervention required.",
        "sender": "alerts@company.com",
        "correct_category": "urgent",
        "correct_priority": 1,
        "correct_action": "escalate",
        "correct_sender_type": "internal",
        "correct_reply_subject": "Re: Database backup failed"
    },
    {
        "email_id": "e011",
        "subject": "Feedback on your presentation",
        "body": "Great job on the presentation yesterday. The client was very impressed with the demo.",
        "sender": "manager@company.com",
        "correct_category": "normal",
        "correct_priority": 3,
        "correct_action": "reply",
        "correct_sender_type": "internal",
        "correct_reply_subject": "Re: Feedback on your presentation"
    },
    {
        "email_id": "e012",
        "subject": "Your account password has been reset",
        "body": "Your password was reset from IP 192.168.1.1. If this was not you, contact support immediately.",
        "sender": "no-reply@company.com",
        "correct_category": "urgent",
        "correct_priority": 1,
        "correct_action": "escalate",
        "correct_sender_type": "internal",
        "correct_reply_subject": "Re: Your account password has been reset"
    },
    {
        "email_id": "e013",
        "subject": "Team lunch this Friday",
        "body": "We are organizing a team lunch this Friday at 1pm. Please confirm your attendance.",
        "sender": "hr@company.com",
        "correct_category": "normal",
        "correct_priority": 4,
        "correct_action": "reply",
        "correct_sender_type": "internal",
        "correct_reply_subject": "Re: Team lunch this Friday"
    },
    {
        "email_id": "e014",
        "subject": "Exclusive deal just for you!",
        "body": "Save 90% on all products today only. Use code SAVE90 at checkout.",
        "sender": "deals@shopnow.biz",
        "correct_category": "spam",
        "correct_priority": 5,
        "correct_action": "delete",
        "correct_sender_type": "external",
        "correct_reply_subject": ""
    },
    {
        "email_id": "e015",
        "subject": "Client contract renewal due",
        "body": "The contract with Acme Corp is due for renewal on the 15th. Please review and sign.",
        "sender": "legal@company.com",
        "correct_category": "normal",
        "correct_priority": 2,
        "correct_action": "reply",
        "correct_sender_type": "internal",
        "correct_reply_subject": "Re: Client contract renewal due"
    },
    {
        "email_id": "e016",
        "subject": "API rate limit exceeded",
        "body": "Your application has exceeded the API rate limit. Service is degraded for all users.",
        "sender": "alerts@company.com",
        "correct_category": "urgent",
        "correct_priority": 1,
        "correct_action": "escalate",
        "correct_sender_type": "internal",
        "correct_reply_subject": "Re: API rate limit exceeded"
    },
    {
        "email_id": "e017",
        "subject": "Request for project update",
        "body": "Could you please send me the latest update on the mobile app project? Thanks.",
        "sender": "stakeholder@client.com",
        "correct_category": "normal",
        "correct_priority": 2,
        "correct_action": "reply",
        "correct_sender_type": "external",
        "correct_reply_subject": "Re: Request for project update"
    },
    {
        "email_id": "e018",
        "subject": "You have won a lottery!",
        "body": "Congratulations! You are our lucky winner. Send us your bank details to claim your prize.",
        "sender": "lottery@winner-notify.com",
        "correct_category": "spam",
        "correct_priority": 5,
        "correct_action": "delete",
        "correct_sender_type": "external",
        "correct_reply_subject": ""
    },
    {
        "email_id": "e019",
        "subject": "Office closed on Monday",
        "body": "Please note the office will be closed on Monday for a public holiday.",
        "sender": "admin@company.com",
        "correct_category": "normal",
        "correct_priority": 4,
        "correct_action": "archive",
        "correct_sender_type": "internal",
        "correct_reply_subject": ""
    },
    {
        "email_id": "e020",
        "subject": "Critical vulnerability in production code",
        "body": "A critical security vulnerability has been found in our payment module. Immediate patch required.",
        "sender": "security@company.com",
        "correct_category": "urgent",
        "correct_priority": 1,
        "correct_action": "escalate",
        "correct_sender_type": "internal",
        "correct_reply_subject": "Re: Critical vulnerability in production code"
    },
    {
        "email_id": "e021",
        "subject": "Disk space critical on prod server",
        "body": "Production server disk usage is at 95%. Immediate cleanup required to prevent outage.",
        "sender": "monitoring@company.com",
        "correct_category": "urgent",
        "correct_priority": 1,
        "correct_action": "escalate",
        "correct_sender_type": "internal",
        "correct_reply_subject": "Re: Disk space critical on prod server"
    },
    {
        "email_id": "e022",
        "subject": "Interview scheduled for Monday",
        "body": "Your interview for the Senior Engineer role is scheduled for Monday 10am. Please confirm.",
        "sender": "hr@company.com",
        "correct_category": "normal",
        "correct_priority": 2,
        "correct_action": "reply",
        "correct_sender_type": "internal",
        "correct_reply_subject": "Re: Interview scheduled for Monday"
    },
    {
        "email_id": "e023",
        "subject": "Make money fast working from home",
        "body": "Earn $5000 per week working just 2 hours a day! No experience needed. Click to start.",
        "sender": "jobs@easymoney4u.net",
        "correct_category": "spam",
        "correct_priority": 5,
        "correct_action": "delete",
        "correct_sender_type": "external",
        "correct_reply_subject": ""
    },
    {
        "email_id": "e024",
        "subject": "Budget approval needed urgently",
        "body": "The Q4 budget proposal needs your approval by EOD today for the finance team to proceed.",
        "sender": "cfo@company.com",
        "correct_category": "urgent",
        "correct_priority": 1,
        "correct_action": "reply",
        "correct_sender_type": "internal",
        "correct_reply_subject": "Re: Budget approval needed urgently"
    },
    {
        "email_id": "e025",
        "subject": "Your subscription is expiring",
        "body": "Your annual software subscription expires in 7 days. Renew now to avoid interruption.",
        "sender": "billing@softwaretool.com",
        "correct_category": "normal",
        "correct_priority": 3,
        "correct_action": "reply",
        "correct_sender_type": "external",
        "correct_reply_subject": "Re: Your subscription is expiring"
    },
]

INBOX_SIZES = {
    "categorize": 1,
    "prioritize": 1,
    "full_triage": 3,
    "sender_analysis": 2,
    "reply_drafting": 3,
}


class EmailTriageEnv:
    def __init__(self, task: str = "categorize"):
        assert task in (
            "categorize", "prioritize", "full_triage",
            "sender_analysis", "reply_drafting"
        ), "Invalid task name"
        self.task = task
        self.inbox = []
        self.current_index = 0
        self.done = False
        self.step_count = 0
        self.episode_rewards = []

    def reset(self) -> EmailObservation:
        inbox_size = INBOX_SIZES.get(self.task, 1)
        self.inbox = random.sample(EMAILS, min(inbox_size, len(EMAILS)))
        self.current_index = 0
        self.done = False
        self.step_count = 0
        self.episode_rewards = []
        return self._make_observation()

    def _make_observation(self) -> EmailObservation:
        email = self.inbox[self.current_index]
        return EmailObservation(
            email_id=email["email_id"],
            subject=email["subject"],
            body=email["body"],
            sender=email["sender"],
            task=self.task,
            inbox_position=self.current_index + 1,
            inbox_size=len(self.inbox)
        )

    def step(self, action: EmailAction) -> dict:
        if self.done:
            raise RuntimeError("Episode is done. Call reset() first.")

        reward_obj = self._grade(action)
        self.episode_rewards.append(reward_obj.score)
        self.step_count += 1
        self.current_index += 1

        if self.current_index >= len(self.inbox):
            self.done = True

        next_obs = self._make_observation() if not self.done else EmailObservation(
            email_id="done",
            subject="",
            body="",
            sender="",
            task=self.task,
            inbox_position=len(self.inbox),
            inbox_size=len(self.inbox)
        )

        return {
            "observation": next_obs,
            "reward": reward_obj.score,
            "done": self.done,
            "info": {
                "breakdown": reward_obj.breakdown,
                "episode_avg": round(
                    sum(self.episode_rewards) / len(self.episode_rewards), 3
                )
            }
        }

    def state(self) -> dict:
        return {
            "task": self.task,
            "step_count": self.step_count,
            "done": self.done,
            "inbox_size": len(self.inbox),
            "current_index": self.current_index,
            "episode_rewards": self.episode_rewards
        }

    def _grade(self, action: EmailAction) -> EmailReward:
        email = self.inbox[self.current_index]
        breakdown = {}

        cat_correct = action.category == email["correct_category"]
        cat_score = 0.85 if cat_correct else 0.15

        pri_diff = abs(action.priority - email["correct_priority"])
        pri_score = max(0.15, min(0.85, round(0.85 - (pri_diff * 0.15), 2)))

        act_correct = action.action == email["correct_action"]
        act_score = 0.85 if act_correct else 0.15

        sender_correct = action.sender_type == email["correct_sender_type"]
        sender_score = 0.85 if sender_correct else 0.15

        correct_subj = email["correct_reply_subject"].lower()
        agent_subj = action.reply_subject.lower()
        if correct_subj == "":
            reply_score = 0.85 if agent_subj == "" else 0.15
        elif agent_subj == "":
            reply_score = 0.15
        elif "re:" in agent_subj and any(
            word in agent_subj for word in correct_subj.split() if len(word) > 3
        ):
            reply_score = 0.85
        else:
            reply_score = 0.45

        if self.task == "categorize":
            total = cat_score
        elif self.task == "prioritize":
            breakdown["priority"] = pri_score
            total = round((cat_score * 0.5) + (pri_score * 0.5), 2)
        elif self.task == "full_triage":
            breakdown["priority"] = pri_score
            breakdown["action"] = act_score
            total = round(
                (cat_score * 0.4) + (pri_score * 0.3) + (act_score * 0.3), 2
            )
        elif self.task == "sender_analysis":
            breakdown["sender_type"] = sender_score
            total = round((cat_score * 0.5) + (sender_score * 0.5), 2)
        elif self.task == "reply_drafting":
            breakdown["reply_subject"] = reply_score
            total = round(
                (cat_score * 0.4) + (pri_score * 0.3) + (reply_score * 0.3), 2
            )
        else:
            total = 0.5

        breakdown["category"] = cat_score
        total = max(0.15, min(0.85, total))
        return EmailReward(score=total, breakdown=breakdown)