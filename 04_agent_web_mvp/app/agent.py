
"""LLM의 JSON 결정 → 허용된 Tool 실행 → 최종 응답."""
import json
import re
import time
from .llm import generate_llm
from .tools import TOOL_DESCRIPTIONS, execute_tool

TOOL_SYSTEM_PROMPT = (
    "당신은 도구 선택 AI Agent다. 가능한 행동은 tool 또는 answer뿐이다.\n"
    "필요한 경우 calculator, text_length, current_time, data_summary 중 하나를 선택한다.\n"
    "숫자 목록 통계에는 data_summary를, 계산에는 calculator를 사용한다.\n"
    "도구가 필요 없는 개념 설명은 answer로 반환한다.\n"
    "반드시 Markdown 없는 JSON 객체 하나만 반환한다.\n"
    '도구 호출: {"action":"tool","tool_name":"calculator","arguments":{"expression":"2+2"}}\n'
    '일반 답변: {"action":"answer","answer":"간단한 설명"}\n'
    + "사용 가능한 Tool: " + json.dumps(TOOL_DESCRIPTIONS, ensure_ascii=False)
)

def parse_agent_json(raw: str) -> dict:
    text = raw.strip()
    # Markdown code fence가 있으면 제거해 파싱을 시도하지만, 실패는 그대로 기록한다.
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
        text = re.sub(r"\s*```$", "", text)
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as e:
        return {"action":"error", "error":f"JSON 파싱 실패: {e}"}
    if not isinstance(obj, dict) or obj.get("action") not in ("tool","answer"):
        return {"action":"error", "error":"action은 tool 또는 answer여야 합니다."}
    if obj["action"] == "tool" and (not isinstance(obj.get("tool_name"),str) or not isinstance(obj.get("arguments"),dict)):
        return {"action":"error", "error":"tool_name/arguments 형식 오류"}
    if obj["action"] == "answer" and not isinstance(obj.get("answer"),str):
        return {"action":"error", "error":"answer는 문자열이어야 합니다."}
    return obj

def make_final_answer(query: str, tool_name: str, tool_result: dict) -> str:
    return generate_llm([
        {"role":"system", "content":"아래 Tool 결과에 근거해 짧고 정확하게 한국어로 답하라."},
        {"role":"user", "content":f"질문: {query}\nTool: {tool_name}\n결과: {json.dumps(tool_result,ensure_ascii=False)}"}
    ], max_new_tokens=160)

def run_agent(user_query: str) -> dict:
    start = time.perf_counter()
    raw = generate_llm([
        {"role":"system", "content":TOOL_SYSTEM_PROMPT},
        {"role":"user", "content":user_query}
    ])
    decision = parse_agent_json(raw)
    result = {"status":"error", "used_tool":False, "tool_name":None,
              "arguments":{}, "tool_result":None, "decision":decision,
              "final_answer":"Agent 결정을 처리하지 못했습니다."}
    if decision["action"] == "answer":
        result.update(status="success", final_answer=decision["answer"])
    elif decision["action"] == "tool":
        tool_name = decision["tool_name"]
        arguments = decision["arguments"]
        tool_result = execute_tool(tool_name, arguments)
        result.update(used_tool=True, tool_name=tool_name,
                      arguments=arguments, tool_result=tool_result)
        if tool_result.get("ok"):
            result.update(status="success",
                          final_answer=make_final_answer(user_query, tool_name, tool_result))
        else:
            result.update(status="tool_error",
                          final_answer=f"Tool 실행 오류: {tool_result.get('error')}")
    result["elapsed_ms"] = round((time.perf_counter()-start)*1000, 1)
    return result

    