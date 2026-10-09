const q = document.getElementById("query");
const sendBtn = document.getElementById("sendBtn");
const healthBtn = document.getElementById("healthBtn");
const statusEl = document.getElementById("status");
const answerEl = document.getElementById("answer");
const detailsEl = document.getElementById("details");

async function runAgent() {
  const query = q.value.trim();
  if (!query) {
    statusEl.textContent = "질문을 입력하세요.";
    return;
  }
  sendBtn.disabled = true;
  statusEl.textContent = "Agent 실행 중...";
  answerEl.textContent = "처리 중...";
  try {
    const res = await fetch("/agent", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({query})
    });
    const data = await res.json();
    answerEl.textContent = data.final_answer ?? "응답 없음";
    detailsEl.textContent = JSON.stringify(data, null, 2);
    statusEl.textContent = `완료 · ${data.elapsed_ms ?? "-"} ms`;
  } catch (err) {
    answerEl.textContent = "요청 처리 중 오류가 발생했습니다.";
    detailsEl.textContent = String(err);
    statusEl.textContent = "오류";
  } finally {
    sendBtn.disabled = false;
  }
}

async function checkHealth() {
  statusEl.textContent = "GPU 상태 확인 중...";
  try {
    const res = await fetch("/health");
    const data = await res.json();
    detailsEl.textContent = JSON.stringify(data, null, 2);
    statusEl.textContent = data.cuda_available ? `GPU 준비: ${data.gpu}` : "CUDA GPU 없음";
  } catch (err) {
    statusEl.textContent = "상태 확인 실패";
  }
}

sendBtn.addEventListener("click", runAgent);
healthBtn.addEventListener("click", checkHealth);
