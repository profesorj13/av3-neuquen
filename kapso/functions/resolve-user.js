async function handler(request, env) {
  const body = await request.json();
  const phone = body.execution_context?.context?.phone_number || body.input?.phone;

  if (!phone) {
    return new Response(JSON.stringify({ vars: { user: null, error: "no_phone" } }));
  }

  // Check KV cache first
  const cacheKey = `user:${phone}`;
  const cached = await env.KV.get(cacheKey);
  if (cached) {
    return new Response(JSON.stringify({ vars: { user: JSON.parse(cached) } }));
  }

  // Lookup via backend API
  const apiBase = await env.KV.get("config:api_base_url") || "http://localhost:8000";
  const res = await fetch(`${apiBase}/users/by-phone/${encodeURIComponent(phone)}`);

  if (res.status === 404) {
    return new Response(JSON.stringify({ vars: { user: null, error: "not_registered" } }));
  }

  if (!res.ok) {
    return new Response(JSON.stringify({ vars: { user: null, error: "api_error" } }));
  }

  const user = await res.json();

  // Cache for 1 hour
  await env.KV.put(cacheKey, JSON.stringify(user), { expirationTtl: 3600 });

  return new Response(JSON.stringify({ vars: { user } }));
}
