from fastapi import FastAPI
from pydantic import BaseModel, Field

from .agent import run_agent
from .llm import MODEL_ID, gpu_status
from .tools import TOOL_DESCRIPTIONS

app = FastAPI(
    title="YU AI Agent Service",
    version="0.1.0",
    description="Qwen3-8B + Custom Tool 기반 교육용 AI Agent API",
)

class AgentRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)

@app.get("/")
def root():
    return {
        "service": "YU AI Agent Service",
        "docs": "/docs",
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": MODEL_ID,
        **gpu_status(),
    }

@app.get("/tools")
def tools():
    return TOOL_DESCRIPTIONS

@app.post("/agent")
def agent(request: AgentRequest):
    return run_agent(request.query)
