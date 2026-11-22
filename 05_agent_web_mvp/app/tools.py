"""수업용 Custom Tool: 허용된 연산/명령만 실행한다."""
import ast
import operator as op
import math
from datetime import datetime
from zoneinfo import ZoneInfo

MAX_INPUT = 100
MAX_ABS_RESULT = 1_000_000_000_000
OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
       ast.Div: op.truediv, ast.FloorDiv: op.floordiv, ast.Mod: op.mod,
       ast.USub: op.neg, ast.UAdd: op.pos}

def _calculate(node, depth=0):
    if depth > 15:
        raise ValueError("수식의 깊이가 제한을 초과했습니다.")
    if isinstance(node, ast.Expression):
        return _calculate(node.body, depth+1)
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        value = node.value
    elif isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        value = OPS[type(node.op)](_calculate(node.operand, depth+1))
    elif isinstance(node, ast.BinOp) and type(node.op) in OPS:
        a = _calculate(node.left, depth+1)
        b = _calculate(node.right, depth+1)
        value = OPS[type(node.op)](a, b)
    elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
        a = _calculate(node.left, depth+1)
        b = _calculate(node.right, depth+1)
        if abs(a) > 1_000_000 or abs(b) > 8:
            raise ValueError("거듭제곱 범위를 초과했습니다.")
        value = a ** b
    else:
        raise ValueError("허용되지 않은 수식입니다.")
    if not isinstance(value, (int,float,complex)) or isinstance(value, complex):
        raise ValueError("실수 결과만 허용합니다.")
    if not math.isfinite(value) or abs(value) > MAX_ABS_RESULT:
        raise ValueError("결과 범위를 초과했습니다.")
    return value

def calculator(expression: str) -> dict:
    """사칙연산·거듭제곱 계산. Python eval() 사용 금지."""
    try:
        if not isinstance(expression, str) or len(expression) > MAX_INPUT:
            raise ValueError("수식은 길이 100 이하의 문자열이어야 합니다.")
        tree = ast.parse(expression, mode="eval")
        return {"ok": True, "result": _calculate(tree)}
    except (ValueError, SyntaxError, ArithmeticError, TypeError) as e:
        return {"ok": False, "error": str(e)}

def text_length(text: str) -> dict:
    if not isinstance(text, str):
        return {"ok": False, "error": "text는 문자열이어야 합니다."}
    return {"ok": True, "result": len(text)}

def current_time() -> dict:
    return {"ok": True, "result": datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S KST")}

def data_summary(values: list) -> dict:
    """수치 목록 개수/합계/평균/최솟값/최댓값 요약."""
    if not isinstance(values, list) or not (1 <= len(values) <= 100):
        return {"ok": False, "error": "values는 1~100개의 숫자 목록이어야 합니다."}
    if any(type(v) not in (int,float) or not math.isfinite(v) or abs(v)>1e9 for v in values):
        return {"ok": False, "error": "유효한 숫자만 사용할 수 있습니다."}
    return {"ok": True, "result": {"count":len(values), "sum":round(sum(values),4),
            "average":round(sum(values)/len(values),4), "min":min(values), "max":max(values)}}

TOOL_REGISTRY = {"calculator": calculator, "text_length": text_length,
                 "current_time": current_time, "data_summary": data_summary}
TOOL_DESCRIPTIONS = {
    "calculator": {"description":"수식을 정확히 계산", "arguments":{"expression":"계산할 수식 문자열"}},
    "text_length": {"description":"문자열 글자 수 계산", "arguments":{"text":"문자열"}},
    "current_time": {"description":"현재 한국 날짜·시각", "arguments":{}},
    "data_summary": {"description":"숫자 목록의 합계·평균·최솟값·최댓값", "arguments":{"values":"숫자 목록, 예: [10,20,30]"}},
}

def execute_tool(tool_name: str, arguments: dict) -> dict:
    if tool_name not in TOOL_REGISTRY:
        return {"ok": False, "error": f"등록되지 않은 Tool: {tool_name}"}
    if not isinstance(arguments, dict):
        return {"ok": False, "error": "arguments는 JSON 객체(dict)여야 합니다."}
    try:
        return TOOL_REGISTRY[tool_name](**arguments)
    except (TypeError, ValueError) as e:
        return {"ok": False, "error": f"인자 오류: {e}"}
