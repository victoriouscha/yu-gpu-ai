# YU AI Agent Service — 4회차 Starter Project

## 목표
3회차에서 만든 Custom Tool + Agent 로직을 FastAPI 서비스로 확장합니다.

## 구조
```text
06_agent_service_starter/
├─ app/
│  ├─ __init__.py
│  ├─ tools.py
│  ├─ llm.py
│  ├─ agent.py
│  └─ main.py
├─ requirements.txt
└─ README.md
```

## 로컬에서 가능한 작업
- Codex로 코드 구조 분석
- `tools.py` Custom Tool 수정/추가
- FastAPI 라우트 구조 확인
- 문법 검사

## GPU 환경에서 실행
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

브라우저에서 `/docs`를 열어 Swagger UI로 API를 테스트합니다.

## 기본 API
- `GET /`
- `GET /health`
- `GET /tools`
- `POST /agent`

### POST /agent 예시
```json
{
  "query": "33명이 30시간씩 GPU를 사용하면 총 몇 GPU-hour야?"
}
```

## 수업 미션
Codex를 활용해 다음 중 하나를 구현합니다.
1. 새로운 Custom Tool 추가
2. `/agent` 오류 응답 개선
3. 실행 로그 저장 기능 추가
4. `/tools` 응답 개선
5. README 사용법 보강
