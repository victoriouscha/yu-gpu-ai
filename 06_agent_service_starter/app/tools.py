import ast
import operator as op
from datetime import datetime

_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

def _safe_eval_node(node):
    if isinstance(node, ast.Expression):
        return _safe_eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](
            _safe_eval_node(node.left),
            _safe_eval_node(node.right),
        )
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](_safe_eval_node(node.operand))
    raise ValueError("허용되지 않은 수식입니다.")

def calculator(expression: str):
    try:
        tree = ast.parse(expression, mode="eval")
        return {"ok": True, "result": _safe_eval_node(tree)}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def text_length(text: str):
    return {"ok": True, "text": text, "length": len(text)}

def current_time():
    return {
        "ok": True,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

TOOL_REGISTRY = {
    "calculator": calculator,
    "text_length": text_length,
    "current_time": current_time,
}

TOOL_DESCRIPTIONS = {
    "calculator": {
        "description": "수학 수식을 계산합니다.",
        "arguments": {"expression": "계산할 수식 문자열"},
    },
    "text_length": {
        "description": "문자열의 글자 수를 계산합니다.",
        "arguments": {"text": "길이를 확인할 문자열"},
    },
    "current_time": {
        "description": "현재 시스템 날짜와 시각을 확인합니다.",
        "arguments": {},
    },
}

def execute_tool(tool_name: str, arguments: dict):
    if tool_name not in TOOL_REGISTRY:
        return {"ok": False, "error": f"존재하지 않는 Tool: {tool_name}"}
    if not isinstance(arguments, dict):
        return {"ok": False, "error": "arguments는 dict 형식이어야 합니다."}
    try:
        return TOOL_REGISTRY[tool_name](**arguments)
    except TypeError as e:
        return {"ok": False, "error": f"인자 오류: {e}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
