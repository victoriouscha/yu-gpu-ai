from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .agent import run_agent
from .llm import MODEL_ID, gpu_status
from .tools import TOOL_DESCRIPTIONS

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="YU AI Agent Web MVP",
    version="1.0.0",
    description="Qwen3-8B + Custom Tool + Web UI 교육용 MVP",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class AgentRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)

@app.get("/")
def web_ui():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/health")
def health():
    return {"status":"ok","model":MODEL_ID,**gpu_status()}

@app.get("/tools")
def tools():
    return TOOL_DESCRIPTIONS

@app.post("/agent")
def agent(request: AgentRequest):
    return run_agent(request.query)
