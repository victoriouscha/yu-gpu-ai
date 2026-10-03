import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "Qwen/Qwen3-8B"

_tokenizer = None
_model = None

def gpu_status():
    return {
        "cuda_available": torch.cuda.is_available(),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    }

def load_model():
    global _tokenizer, _model
    if _model is not None:
        return _tokenizer, _model
    if not torch.cuda.is_available():
        raise RuntimeError("Qwen 추론은 CUDA GPU 환경에서 실행하세요.")

    _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    _model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        dtype=torch.bfloat16,
        device_map="auto",
    )
    _model.eval()
    return _tokenizer, _model

def generate_llm(messages, max_new_tokens=300):
    tokenizer, model = load_model()

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )
    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
        )

    input_tokens = inputs["input_ids"].shape[1]
    return tokenizer.decode(
        outputs[0][input_tokens:],
        skip_special_tokens=True,
    ).strip()
