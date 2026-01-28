async function handler(request, env) {
  const body = await request.json();
  const user = body.execution_context?.vars?.user;
  const edges = body.available_edges || [];

  if (!user) {
    return new Response(JSON.stringify({ next_edge: edges.includes("not_registered") ? "not_registered" : edges[0] }));
  }

  if (user.role === "coordinator") {
    return new Response(JSON.stringify({
      next_edge: edges.includes("coordinator") ? "coordinator" : edges[0],
      vars: { role: "coordinator" }
    }));
  }

  return new Response(JSON.stringify({
    next_edge: edges.includes("teacher") ? "teacher" : edges[0],
    vars: { role: "teacher" }
  }));
}
