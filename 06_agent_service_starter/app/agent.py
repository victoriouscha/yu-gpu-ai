import json
from .llm import generate_llm
from .tools import TOOL_DESCRIPTIONS, execute_tool

TOOL_SYSTEM_PROMPT = f"""
너는 Tool을 사용할 수 있는 AI Agent다.

사용 가능한 Tool:
{json.dumps(TOOL_DESCRIPTIONS, ensure_ascii=False, indent=2)}

규칙:
1. 계산이 필요하면 calculator를 사용한다.
2. 문자열 글자 수가 필요하면 text_length를 사용한다.
3. 현재 날짜/시각이 필요하면 current_time을 사용한다.
4. Tool이 필요하지 않은 일반 설명 질문은 직접 답한다.
5. 반드시 JSON 하나만 출력한다. Markdown 코드블록은 사용하지 않는다.

Tool이 필요한 경우:
{{
  "action": "tool",
  "tool_name": "도구이름",
  "arguments": {{...}}
}}

Tool이 필요 없는 경우:
{{
  "action": "answer",
  "answer": "최종 답변"
}}
"""

def parse_agent_json(text: str):
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        return {
            "action": "error",
            "error": f"JSON 파싱 실패: {e}",
            "raw_output": text,
        }

def make_final_answer(user_query, tool_name, tool_result):
    messages = [
        {
            "role": "system",
            "content": (
                "사용자의 질문과 Tool 실행 결과만 근거로 "
                "간결하고 정확한 한국어 답변을 작성해라."
            ),
        },
        {
            "role": "user",
            "content": (
                f"사용자 질문: {user_query}\n"
                f"사용한 Tool: {tool_name}\n"
                f"Tool 결과: {json.dumps(tool_result, ensure_ascii=False)}"
            ),
        },
    ]
    return generate_llm(messages, max_new_tokens=200)

def run_agent(user_query: str):
    raw = generate_llm([
        {"role": "system", "content": TOOL_SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ])
    decision = parse_agent_json(raw)

    if decision.get("action") == "answer":
        return {
            "status": "success",
            "used_tool": False,
            "decision": decision,
            "final_answer": decision.get("answer", ""),
        }

    if decision.get("action") == "error":
        return {
            "status": "error",
            "used_tool": False,
            "decision": decision,
            "final_answer": "Agent의 구조화 출력을 해석하지 못했습니다.",
        }

    if decision.get("action") == "tool":
        tool_name = decision.get("tool_name")
        arguments = decision.get("arguments", {})
        tool_result = execute_tool(tool_name, arguments)

        if not tool_result.get("ok", False):
            return {
                "status": "tool_error",
                "used_tool": True,
                "tool_name": tool_name,
                "arguments": arguments,
                "tool_result": tool_result,
                "final_answer": f"Tool 실행 오류: {tool_result.get('error')}",
            }

        return {
            "status": "success",
            "used_tool": True,
            "tool_name": tool_name,
            "arguments": arguments,
            "tool_result": tool_result,
            "decision": decision,
            "final_answer": make_final_answer(
                user_query, tool_name, tool_result
            ),
        }

    return {
        "status": "error",
        "used_tool": False,
        "decision": decision,
        "final_answer": "지원하지 않는 Agent action입니다.",
    }
