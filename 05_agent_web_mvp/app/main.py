"""5회차: 4회차 FastAPI Backend에 HTML/CSS/JS 화면만 확장."""
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator
from .agent import run_agent
from .llm import MODEL_ID, gpu_status
from .tools import TOOL_DESCRIPTIONS

STATIC_DIR = Path(__file__).parent / "static"
app = FastAPI(title="YU AI Agent Web MVP", version="1.0.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class AgentRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)

    @field_validator("query")
    @classmethod
    def check_query(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("빈 질문은 허용되지 않습니다.")
        return value.strip()

@app.get("/")
def web_ui():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/health")
def health():
    return {"status":"ok", "model":MODEL_ID, **gpu_status()}

@app.get("/tools")
def tools():
    return TOOL_DESCRIPTIONS

@app.post("/agent")
def agent(request: AgentRequest):
    try:
        return run_agent(request.query)
    except (RuntimeError, OSError, ValueError) as e:
        raise HTTPException(status_code=503, detail=f"GPU/모델 준비 실패: {e}") from e
