import os
import json
import requests
from openai import OpenAI

API_BASE_URL = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.environ.get("API_KEY", "dummy-key")
MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
ENV_BASE_URL = os.environ.get("ENV_BASE_URL", "https://archit072003-email-triage-env.hf.space")
LOCAL_IMAGE_NAME = os.environ.get("LOCAL_IMAGE_NAME")

TASKS = ["categorize", "prioritize", "full_triage"]
MAX_STEPS = 1

try:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
except Exception as e:
    print(f"[DEBUG] OpenAI client init failed: {e}", flush=True)
    client = None


def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step, action, reward, done, error=None):
    error_val = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}", flush=True)


def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


def get_agent_action(observation):
    prompt = (
        "You are an email triage agent. Read the email below and respond.\n\n"
        f"Subject: {observation['subject']}\n"
        f"From: {observation['sender']}\n"
        f"Body: {observation['body']}\n"
        f"Task: {observation['task']}\n\n"
        "Respond with ONLY a JSON object (no explanation):\n"
        '{"category": "urgent" or "normal" or "spam", '
        '"priority": 1 to 5, '
        '"action": "reply" or "archive" or "delete" or "escalate"}'
    )

    if client is None:
        return {"category": "normal", "priority": 3, "action": "reply"}

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.0,
        )
        text = completion.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"[DEBUG] LLM call failed: {e}", flush=True)
        return {"category": "normal", "priority": 3, "action": "reply"}


def run_task(task):
    log_start(task=task, env="email-triage-env", model=MODEL_NAME)
    rewards = []

    try:
        res = requests.post(
            f"{ENV_BASE_URL}/reset",
            json={"task": task},
            timeout=30
        )
        obs = res.json()["observation"]
    except Exception as e:
        log_step(1, "reset_error", 0.00, True, str(e))
        log_end(False, 1, 0.0, [0.0])
        return

    for step in range(1, MAX_STEPS + 1):
        agent_action = get_agent_action(obs)

        payload = {
            "task": task,
            "category": agent_action.get("category", "normal"),
            "priority": agent_action.get("priority", 3),
            "action": agent_action.get("action", "reply")
        }

        try:
            step_res = requests.post(
                f"{ENV_BASE_URL}/step",
                json=payload,
                timeout=30
            ).json()
            reward = step_res.get("reward", 0.0)
            done = step_res.get("done", True)
        except Exception as e:
            log_step(step, "step_error", 0.00, True, str(e))
            log_end(False, step, 0.0, [0.0])
            return

        rewards.append(reward)
        action_str = f"category={payload['category']},priority={payload['priority']},action={payload['action']}"
        log_step(step, action_str, reward, done)

        if done:
            break

    score = sum(rewards) / len(rewards) if rewards else 0.0
    success = score >= 0.5
    log_end(success=success, steps=len(rewards), score=score, rewards=rewards)


if __name__ == "__main__":
    for task in TASKS:
        run_task(task)
        print()