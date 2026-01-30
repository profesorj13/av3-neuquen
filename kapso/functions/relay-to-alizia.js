async function handler(request, env) {
  const body = await request.json();
  const userMessage = body.input?.message;
  const docId = body.input?.document_id;
  const phone = body.execution_context?.context?.phone_number || body.input?.phone;

  if (!userMessage || !docId) {
    return new Response(JSON.stringify({
      vars: { alizia_response: "Necesito un mensaje y un ID de documento para chatear." }
    }));
  }

  // Get chat history from KV
  const historyKey = `chat:${phone}:${docId}`;
  const rawHistory = await env.KV.get(historyKey);
  const history = rawHistory ? JSON.parse(rawHistory) : [];

  // Add user message to history
  history.push({ role: "user", content: userMessage });

  // Call backend chat endpoint
  const apiBase = await env.KV.get("config:api_base_url") || "http://localhost:8000";
  const res = await fetch(`${apiBase}/coordination-documents/${docId}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "ngrok-skip-browser-warning": "true" },
    body: JSON.stringify({ history })
  });

  if (!res.ok) {
    return new Response(JSON.stringify({
      vars: { alizia_response: "Error al comunicarse con Alizia." }
    }));
  }

  const data = await res.json();
  const assistantMessage = data.message;

  // Save updated history (keep last 20 messages)
  history.push({ role: "assistant", content: assistantMessage });
  const trimmed = history.slice(-20);
  await env.KV.put(historyKey, JSON.stringify(trimmed), { expirationTtl: 86400 });

  return new Response(JSON.stringify({ vars: { alizia_response: assistantMessage } }));
}
