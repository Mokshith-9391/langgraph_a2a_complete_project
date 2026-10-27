from fastapi import Depends, FastAPI
from common.security import require_api_key
from pydantic import BaseModel
from .graph import graph

app = FastAPI(title="LangGraph A2A Supervisor", version="1.0.0")

class TaskRequest(BaseModel):
    request: str

@app.get("/health")
async def health():
    return {"status": "ok", "agent": "LangGraph Supervisor"}

@app.post("/run", dependencies=[Depends(require_api_key)])
async def run_task(body: TaskRequest):
    result = await graph.ainvoke({"user_request": body.request})
    return {
        "request": body.request,
        "research": result.get("research", ""),
        "article": result.get("article", ""),
    }
