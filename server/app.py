from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os
import uvicorn

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
def reset(req: ResetRequest):
    task = req.task or "categorize"
    if task not in ("categorize", "prioritize", "full_triage"):
        raise HTTPException(status_code=400, detail="Invalid task name")
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

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    main()