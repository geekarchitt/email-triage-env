---
title: Email Triage Env
<<<<<<< HEAD
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
tags:
  - openenv
---

# 📧 Email Triage OpenEnv Environment

An OpenEnv-compliant environment where an AI agent learns to triage emails
by categorizing, prioritizing, and deciding the correct action.

## 🎯 Why This Environment?

Email triage is a task every knowledge worker does daily. Training agents
to handle it well has immediate real-world value for productivity tools,
enterprise automation, and AI assistants.

## 📐 Observation Space

| Field      | Type   | Description                        |
|------------|--------|------------------------------------|
| email_id   | string | Unique identifier for the email    |
| subject    | string | Email subject line                 |
| body       | string | Email body text                    |
| sender     | string | Sender's email address             |
| task       | string | Active task name                   |

## 🎮 Action Space

| Field    | Type    | Values                                      |
|----------|---------|---------------------------------------------|
| category | string  | `urgent`, `normal`, `spam`                  |
| priority | integer | `1` (highest) to `5` (lowest)               |
| action   | string  | `reply`, `archive`, `delete`, `escalate`    |

## 📋 Tasks

| Task         | Difficulty | Description                                              |
|--------------|------------|----------------------------------------------------------|
| categorize   | Easy       | Classify email as urgent / normal / spam                 |
| prioritize   | Medium     | Classify + assign priority 1–5                           |
| full_triage  | Hard       | Classify + prioritize + choose correct action            |

## 🏆 Reward Function

- **categorize**: 1.0 if category correct, else 0.0
- **prioritize**: category (50%) + priority accuracy (50%), partial credit for close guesses
- **full_triage**: category (40%) + priority (30%) + action (30%)

Priority scoring gives partial credit: -0.25 per level away from correct answer.

## 🚀 Setup & Usage

### Run locally with Docker
```bash
docker build -t email-triage-env .
docker run -p 7860:7860 email-triage-env
```

### Run inference script
```bash
export HF_TOKEN=your_token_here
export MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
export API_BASE_URL=https://router.huggingface.co/v1
export ENV_BASE_URL=http://localhost:7860
python inference.py
```

## 📊 Baseline Scores

| Task        | Model                  | Score |
|-------------|------------------------|-------|
| categorize  | Qwen2.5-72B-Instruct   | ~0.95 |
| prioritize  | Qwen2.5-72B-Instruct   | ~0.78 |
| full_triage | Qwen2.5-72B-Instruct   | ~0.65 |
=======
emoji: 👀
colorFrom: yellow
colorTo: yellow
sdk: docker
pinned: false
license: mit
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
>>>>>>> 35f9ba432e55d124fa29973766fac7f6135b31b6
