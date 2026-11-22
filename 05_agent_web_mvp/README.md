# 5회차: AI Agent Web Service MVP

구조: Web UI → FastAPI → Agent → Qwen3-8B → Custom Tool. **Codex/API 유료키는 사용하지 않습니다.**

1. VS Code Remote-SSH로 RunPod GPU Pod에 연결하고 `/workspace`에서 압축을 풉니다.
2. `cd /workspace/05\_agent\_web\_mvp`
3. `python -m pip install -r requirements.txt` (RunPod PyTorch 설치 상태 확인)
4. `uvicorn app.main:app --host 127.0.0.1 --port 8000`
5. VS Code의 Ports에서 8000을 포워딩하고 \*\*로컬 PC의 `http://localhost:8000/`\*\*로 접속합니다.
6. Web UI에서 GPU 상태 및 계산/글자 수/통계 질문을 테스트합니다. 최초 /agent 호출은 모델을 내려받아 느릴 수 있습니다.

**주의:** RunPod Pod/VS Code의 포트 포워딩 방식은 환경에 따라 다릅니다. 교육용 서버는 인증 없이 인터넷에 직접 공개하지 않습니다.
HF 모델 캐시는 `/workspace/hf-cache`에 저장됩니다. 영구 저장 여부는 별도로 확인하세요.

오류/검증: CUDA가 없는 환경은 GET /health는 가능하지만 POST /agent는 503. 빈 질문은 422.

최종 평가: 동일 질문 세트(정상 4개 + 오류 1개), 성공/실패, tool\_name, elapsed\_ms를 `results/05\_mvp\_evaluation.csv`에 기록하고 개선 전후를 비교합니다.

