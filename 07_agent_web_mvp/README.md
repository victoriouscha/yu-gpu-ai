# 5회차 — AI Agent Web Service MVP

## 실행
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

브라우저에서 서비스 루트(`/`)를 열면 Web UI가 표시됩니다.

## 구조
Web UI → FastAPI → Agent → Qwen3-8B → Custom Tool → 최종 응답

## API
- GET /
- GET /health
- GET /tools
- POST /agent

## 최종 테스트
1. 계산 질문
2. 글자 수 질문
3. 현재 시각 질문
4. 일반 설명 질문
5. 빈 입력/오류 상황
6. 응답시간(elapsed_ms) 확인
