from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from email_triage_env import EmailTriageEnv, EmailAction

app = FastAPI(title="Email Triage OpenEnv")

envs = {}


class ResetRequest(BaseModel):
    task: Optional[str] = "categorize"


class StepRequest(BaseModel):
    task: str
    category: str
    priority: int
    action: str


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
        action=req.action
    )
    result = env.step(action)
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


@app.get("/health")
def health():
    return {"status": "ok"}