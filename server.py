from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from email_triage_env import EmailTriageEnv, EmailAction

app = FastAPI(title="Email Triage OpenEnv")

envs = {}

# Tracks history across all episodes
episode_history = []


class ResetRequest(BaseModel):
    task: Optional[str] = "categorize"


class StepRequest(BaseModel):
    task: str
    category: str
    priority: int
    action: str
    sender_type: Optional[str] = "internal"
    reply_subject: Optional[str] = ""


@app.post("/reset")
def reset(req: ResetRequest = None):
    if req is None:
        task = "categorize"
    else:
        task = req.task or "categorize"
    if task not in ("categorize", "prioritize", "full_triage", "sender_analysis", "reply_drafting"):
        task = "categorize"
    env = EmailTriageEnv(task=task)
    envs[task] = env
    obs = env.reset()
    return {"observation": obs.model_dump(), "done": False}


@app.post("/step")
def step(req: StepRequest):
    task = req.task
    if task not in envs:
        raise HTTPException(status_code=400, detail="Call /reset first")
    env = envs[task]
    if env.done:
        raise HTTPException(status_code=400, detail="Episode done. Call /reset again.")
    action = EmailAction(
        category=req.category,
        priority=req.priority,
        action=req.action,
        sender_type=req.sender_type or "internal",
        reply_subject=req.reply_subject or ""
    )
    result = env.step(action)

    # Record episode in history
    episode_history.append({
        "task": task,
        "email_id": result["observation"].email_id,
        "reward": result["reward"],
        "breakdown": result["info"]["breakdown"]
    })

    return {
        "observation": result["observation"].model_dump(),
        "reward": result["reward"],
        "done": result["done"],
        "info": result["info"]
    }


@app.get("/state")
def state(task: str = "categorize"):
    if task not in envs:
        raise HTTPException(status_code=400, detail="Call /reset first")
    return envs[task].state()


@app.get("/episode_summary")
def episode_summary():
    """Returns aggregated stats across all episodes played so far."""
    if not episode_history:
        return {"message": "No episodes played yet. Call /reset and /step first."}

    # Overall stats
    total_episodes = len(episode_history)
    avg_reward = round(sum(e["reward"] for e in episode_history) / total_episodes, 3)

    # Per task stats
    task_stats = {}
    for episode in episode_history:
        t = episode["task"]
        if t not in task_stats:
            task_stats[t] = {"episodes": 0, "total_reward": 0.0, "scores": []}
        task_stats[t]["episodes"] += 1
        task_stats[t]["total_reward"] += episode["reward"]
        task_stats[t]["scores"].append(episode["reward"])

    task_summary = {}
    for t, stats in task_stats.items():
        scores = stats["scores"]
        task_summary[t] = {
            "episodes": stats["episodes"],
            "avg_score": round(stats["total_reward"] / stats["episodes"], 3),
            "best_score": round(max(scores), 3),
            "worst_score": round(min(scores), 3)
        }

    # Best and worst episodes
    best = max(episode_history, key=lambda e: e["reward"])
    worst = min(episode_history, key=lambda e: e["reward"])

    return {
        "total_episodes": total_episodes,
        "overall_avg_reward": avg_reward,
        "per_task": task_summary,
        "best_episode": best,
        "worst_episode": worst
    }


@app.delete("/episode_summary")
def reset_summary():
    """Clear episode history."""
    episode_history.clear()
    return {"message": "Episode history cleared."}


@app.get("/health")
def health():
    return {"status": "ok"}