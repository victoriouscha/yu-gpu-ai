const el=id=>document.getElementById(id);
async function fetchJSON(url, options={}) {
  const res=await fetch(url,options);
  const data=await res.json();
  if (!res.ok) throw new Error(typeof data.detail === "string" ? data.detail : `HTTP ${res.status}: ${JSON.stringify(data.detail)}`);
  return data;
}
async function runAgent() {
  const query=el("question").value.trim();
  if(!query){el("state").textContent="질문을 입력하세요.";return;}
  el("send").disabled=true;el("state").textContent="Agent 실행 중... (최초 모델 로딩 시 지연될 수 있음)";
  try {
    const data=await fetchJSON("/agent",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({query})});
    el("answer").textContent=data.final_answer||"답변 없음";
    el("meta").textContent=JSON.stringify({status:data.status,used_tool:data.used_tool,tool_name:data.tool_name,
      arguments:data.arguments,tool_result:data.tool_result,elapsed_ms:data.elapsed_ms},null,2);
    el("state").textContent="완료";
  } catch(e) {el("state").textContent="실행 오류";el("answer").textContent=e.message;}
  finally{el("send").disabled=false;}
}
async function checkHealth(){try{const data=await fetchJSON("/health");el("meta").textContent=JSON.stringify(data,null,2);
 el("state").textContent=data.cuda_available?"GPU 사용 가능":"CUDA GPU 없음 (Agent 실행 불가)";
}catch(e){el("state").textContent=e.message;}}
el("send").addEventListener("click",runAgent);el("health").addEventListener("click",checkHealth);
el("question").addEventListener("keydown",e=>{if(e.key==="Enter"&&e.ctrlKey){e.preventDefault();runAgent();}});
