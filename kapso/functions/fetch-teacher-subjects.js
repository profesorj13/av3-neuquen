async function handler(request, env) {
  const body = await request.json();
  const teacherId = body.input?.teacher_id || body.execution_context?.vars?.user?.id;

  if (!teacherId) {
    return new Response(JSON.stringify({ vars: { subjects_text: "No se pudo identificar al docente." } }));
  }

  const apiBase = await env.KV.get("config:api_base_url") || "http://localhost:8000";
  const res = await fetch(`${apiBase}/teachers/${teacherId}/courses`);

  if (!res.ok) {
    return new Response(JSON.stringify({ vars: { subjects_text: "Error al consultar materias." } }));
  }

  const courseSubjects = await res.json();

  if (courseSubjects.length === 0) {
    return new Response(JSON.stringify({ vars: { subjects_text: "No tenés materias asignadas." } }));
  }

  const lines = courseSubjects.map(cs =>
    `• ${cs.subject_name} - ${cs.course_name} (${cs.school_year})`
  );

  const text = `📚 *Tus materias:*\n\n${lines.join("\n")}`;

  return new Response(JSON.stringify({ vars: { subjects_text: text } }));
}
