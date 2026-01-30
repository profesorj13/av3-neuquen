async function handler(request, env) {
  const body = await request.json();
  const areaId = body.input?.area_id;

  const apiBase = await env.KV.get("config:api_base_url") || "http://localhost:8000";
  const res = await fetch(`${apiBase}/coordination-documents`, {
    headers: { "ngrok-skip-browser-warning": "true" }
  });

  if (!res.ok) {
    return new Response(JSON.stringify({ vars: { documents_text: "Error al consultar documentos." } }));
  }

  let docs = await res.json();

  if (areaId) {
    docs = docs.filter(d => d.area_id === areaId);
  }

  if (docs.length === 0) {
    return new Response(JSON.stringify({ vars: { documents_text: "No hay documentos de coordinación.", documents: [] } }));
  }

  const statusMap = { draft: "Borrador", published: "Publicado", archived: "Archivado" };
  const lines = docs.map(d =>
    `• [${d.id}] ${d.name} - ${statusMap[d.status] || d.status}`
  );

  const text = `📄 *Documentos de coordinación:*\n\n${lines.join("\n")}`;

  return new Response(JSON.stringify({ vars: { documents_text: text, documents: docs } }));
}
