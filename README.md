[README.md](https://github.com/user-attachments/files/35232778/README.md)
# GPU 기반 오픈소스 LLM 및 AI Agent 실습

> **실습 과정:** Qwen·Gemma 모델 실행 및 성능 비교 → 모델 평가 → Custom Tool Agent → FastAPI → AI Agent Web MVP  
> **실행 환경:** RunPod GPU, Python, PyTorch, Hugging Face Transformers, JupyterLab, FastAPI  
> **대상:** GPU 기반 LLM 및 AI Agent 실습 교육

## 1. 프로젝트 소개

이 저장소는 GPU에서 오픈소스 LLM을 직접 실행하고, 모델 성능을 비교한 뒤, 도구를 사용하는 AI Agent를 구현하여 FastAPI와 웹 서비스로 확장하는 **5회차 실습 자료**입니다.

주요 실습 모델은 **Qwen3-8B**와 **Gemma 3 4B-IT**입니다. 4·5회차 Agent 서비스에서는 Qwen3-8B를 활용하며, 별도의 상용 LLM API 키 없이 로컬 추론 흐름을 실습합니다.

## 2. 회차별 실습 내용

| 회차 | Notebook | 핵심 실습 | 주요 결과 |
|---|---|---|---|
| 1회차 | `01_GPU_LLM_Qwen_Gemma.ipynb` | GPU/CUDA 확인, Qwen3-8B BF16·NF4 4-bit 추론, Gemma 3 4B-IT 실행 및 비교 | 모델 성능 비교 CSV |
| 2회차 | `02_Model_Evaluation.ipynb` | 동일 평가 문항 기반 Gemma·Qwen 응답 품질, 출력 형식, GPU 자원 비교 | 모델 평가 결과 및 선정 요약 CSV |
| 3회차 | `03_Custom_Tool_Agent.ipynb` | 계산·글자 수·현재 시각·데이터 요약 도구와 Tool 선택 Agent 구현 | Agent 실행 로그 CSV |
| 4회차 | `04_FastAPI_Agent_Service.ipynb` | Python Agent 소스를 FastAPI REST API로 구성, `/health`·`/tools`·`/agent` 검증 | `04_agent_web_mvp/` 백엔드 |
| 5회차 | `05_AI_Agent_Web_MVP.ipynb` | HTML·CSS·JavaScript 웹 UI 연계, GPU Agent 호출, 오류 입력 및 기능 평가 | `05_agent_web_mvp/` 웹 MVP 및 평가 결과 |

## 3. 저장소 구조

```text
yu-gpu-ai/
├── 01_GPU_LLM_Qwen_Gemma.ipynb
├── 02_Model_Evaluation.ipynb
├── 03_Custom_Tool_Agent.ipynb
├── 04_FastAPI_Agent_Service.ipynb
├── 05_AI_Agent_Web_MVP.ipynb
├── 04_agent_web_mvp/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── tools.py
│   │   ├── llm.py
│   │   ├── agent.py
│   │   └── main.py
│   ├── requirements.txt
│   └── README.md
├── 05_agent_web_mvp/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── tools.py
│   │   ├── llm.py
│   │   ├── agent.py
│   │   ├── main.py
│   │   └── static/
│   ├── requirements.txt
│   └── README.md
├── results/
│   ├── 01_LLM_GPU_Comparison.csv
│   ├── 02_model_evaluation_results.csv
│   ├── 02_model_selection_summary.csv
│   └── 03_agent_tool_execution_log.csv
└── workspace_source_backup_20261122.tar.gz
```

> `yu-gpu-ai.zip`는 기존 작업 공간의 보관용 백업입니다. 학생용 실습에 반드시 필요한 실행 파일은 아닙니다. 현재 실행할 5회차 프로젝트의 최종 폴더 이름은 **`05_agent_web_mvp`**입니다.

## 4. 실행 환경

- RunPod GPU Pod: 실습 전체를 위해 **NVIDIA A100 80GB** 환경을 기준으로 검증
- 데이터 보관: RunPod **Network Volume**을 `/workspace`에 마운트하는 방식 권장
- Python·CUDA·PyTorch와 Transformers 등은 Notebook 안내 또는 사전 구성된 이미지로 준비
- Gemma 3 4B-IT: Hugging Face에서 **모델 이용 조건 동의 및 접근 권한** 필요

## 5. RunPod JupyterLab에서 실습 시작

1. GPU Pod를 시작하고 **Network Volume이 `/workspace`에 마운트되었는지** 확인합니다.
2. JupyterLab에 접속하여 저장소의 Notebook 및 프로젝트 파일을 `/workspace`에 준비합니다.
3. JupyterLab의 **Terminal**에서 아래 명령을 실행합니다.

```bash
nvidia-smi
df -hT /workspace
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

4. `01_GPU_LLM_Qwen_Gemma.ipynb`부터 회차 순서대로 실행합니다.
5. 모델 다운로드는 시간이 걸릴 수 있습니다. Hugging Face 캐시가 **영구 Network Volume 내부**에 있는지 확인하세요.

> 경로 안내: Notebook 일부에는 패키지 설치와 Hugging Face 캐시 설정 단계가 포함되어 있습니다. 이미 구성된 실습 환경에서도 Notebook 실행 전 **현재 커널·패키지 버전·모델 캐시 경로**를 확인하세요. `pip install`은 일반적으로 이미지의 Python 환경을 대상으로 하며, 별도 Network Volume에 자동 보존되지는 않습니다.

## 6. 4회차 FastAPI 실행

4회차 Notebook의 프로젝트 생성 및 검증 단계를 마친 뒤, **별도의 JupyterLab Terminal**에서 다음을 실행합니다.

```bash
cd /workspace/04_agent_web_mvp
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

RunPod의 Pod 설정에서 **HTTP 포트 8000**을 노출한 경우 `Connect → HTTP services → Port 8000` 링크로 접속합니다. API 문서는 해당 서비스 URL의 `/docs`에서 확인할 수 있습니다.

VS Code의 SSH 포트 전달 방식으로만 사용할 때는 `--host 127.0.0.1`도 사용할 수 있습니다.

## 7. 5회차 Web MVP 실행

5회차 Notebook과 `05_agent_web_mvp` 프로젝트를 준비한 뒤 아래 명령으로 실행합니다.

```bash
cd /workspace/05_agent_web_mvp
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- 웹 UI: RunPod **Port 8000 → HTTP Service**의 서비스 주소
- API 문서: 위 서비스 주소의 `/docs`
- Notebook 내부 API 테스트: `BASE_URL = "http://127.0.0.1:8000"`
- GPU 실험 활성화: GPU와 Uvicorn 서버가 실행 중일 때만 `RUN_GPU_TESTS = True`
- 검증 예시: `/health`와 정상 `/agent` 요청은 성공 응답을, 공백 질문은 입력 검증에 따른 **HTTP 422**를 기대합니다.

**주의:** `0.0.0.0`은 서버의 바인딩 주소입니다. Windows 브라우저에 `http://0.0.0.0:8000`을 입력하는 주소가 아닙니다. RunPod가 제공한 HTTP Service 링크를 사용해야 합니다. 4회차와 5회차 서버를 같은 포트에서 동시에 실행할 수 없으므로, 이전 Uvicorn 실행은 `Ctrl+C`로 종료한 뒤 다음 서버를 실행하세요.

## 8. 결과 보관 및 협업 시 주의

- Notebook과 결과 CSV는 **Network Volume**에 저장하고, 수업 종료 후 로컬 PC 또는 GitHub에 별도 백업합니다.
- Hugging Face 토큰, SSH 개인키, 비밀번호 등 인증 정보는 Notebook·코드·공개 저장소·Docker 이미지에 포함하지 않습니다.
- 공개 HTTP 포트로 인증 없는 실습 API를 열면 외부 접근이 가능할 수 있습니다. 운영 방식에 맞는 접근 제한을 적용하세요.
- GPU 사용을 마치면 RunPod Pod를 중지해 GPU 과금을 관리합니다. Network Volume의 저장 요금은 별도로 계속 발생할 수 있습니다.

---

**최종 실습 프로젝트 기준:** `04_agent_web_mvp`, `05_agent_web_mvp`  
**교육용 자료:** GPU 기반 오픈소스 LLM 및 AI Agent PBL 실습
