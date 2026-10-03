const $ = (id) => document.getElementById(id);

async function runAgent() {
  const query = $("query").value.trim();
  if (!query) {
    $("status").textContent = "질문을 입력하세요.";
    return;
  }

  $("status").textContent = "Agent 실행 중...";
  $("sendBtn").disabled = true;

  try {
    const response = await fetch("/agent", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({query})
    });

    const data = await response.json();

    $("answer").textContent = data.final_answer ?? "";
    $("meta").textContent =
      `status: ${data.status}\n` +
      `used_tool: ${data.used_tool}\n` +
      `tool_name: ${data.tool_name ?? "-"}\n` +
      `elapsed_ms: ${data.elapsed_ms ?? "-"}`;

    $("raw").textContent = JSON.stringify(data, null, 2);
    $("status").textContent = response.ok ? "완료" : "HTTP 오류";
  } catch (error) {
    $("status").textContent = "요청 실패";
    $("answer").textContent = String(error);
  } finally {
    $("sendBtn").disabled = false;
  }
}

async function checkHealth() {
  $("status").textContent = "GPU 상태 확인 중...";
  try {
    const response = await fetch("/health");
    const data = await response.json();
    $("raw").textContent = JSON.stringify(data, null, 2);
    $("status").textContent = "상태 확인 완료";
  } catch (error) {
    $("status").textContent = "상태 확인 실패";
  }
}

$("sendBtn").addEventListener("click", runAgent);
$("healthBtn").addEventListener("click", checkHealth);
