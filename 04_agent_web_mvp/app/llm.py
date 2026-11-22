
"""RunPod GPU의 Qwen3-8B 로컬 추론. 첫 /agent 요청 시 모델 지연 로딩."""
import os
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "Qwen/Qwen3-8B"
if Path("/workspace").is_dir():
    os.environ.setdefault("HF_HOME", "/workspace/hf-cache")
    Path(os.environ["HF_HOME"]).mkdir(parents=True, exist_ok=True)
_tokenizer = None
_model = None

def gpu_status() -> dict:
    ok = torch.cuda.is_available()
    return {"cuda_available": bool(ok),
            "gpu": torch.cuda.get_device_name(0) if ok else None}

def load_model():
    global _tokenizer, _model
    if _model is None:
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA GPU가 없습니다. RunPod GPU에 접속하세요.")
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID, dtype=torch.bfloat16, device_map="auto"
        ).eval()
    return _tokenizer, _model

def generate_llm(messages: list, max_new_tokens: int=256) -> str:
    tokenizer, model = load_model()
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True,
        enable_thinking=False
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.inference_mode():
        outputs = model.generate(**inputs, max_new_tokens=max_new_tokens,
                                 do_sample=False, pad_token_id=tokenizer.eos_token_id)
    n_in = inputs["input_ids"].shape[-1]
    return tokenizer.decode(outputs[0][n_in:], skip_special_tokens=True).strip()

    