async function handler(request, env) {
  const body = await request.json();
  const areaId = body.input?.area_id;

  if (!areaId) {
    return new Response(JSON.stringify({ vars: { teachers: [] } }));
  }

  const apiBase = await env.KV.get("config:api_base_url") || "http://localhost:8000";

  // Get subjects for this area
  const subjectsRes = await fetch(`${apiBase}/subjects`);
  if (!subjectsRes.ok) {
    return new Response(JSON.stringify({ vars: { teachers: [] } }));
  }
  const allSubjects = await subjectsRes.json();
  const areaSubjectIds = allSubjects
    .filter(s => s.area_id === areaId)
    .map(s => s.id);

  // Get course_subjects to find teachers
  const csRes = await fetch(`${apiBase}/course-subjects`);
  if (!csRes.ok) {
    return new Response(JSON.stringify({ vars: { teachers: [] } }));
  }
  const courseSubjects = await csRes.json();
  const teacherIds = [...new Set(
    courseSubjects
      .filter(cs => areaSubjectIds.includes(cs.subject_id))
      .map(cs => cs.teacher_id)
  )];

  // Get user details
  const usersRes = await fetch(`${apiBase}/users`);
  if (!usersRes.ok) {
    return new Response(JSON.stringify({ vars: { teachers: [] } }));
  }
  const users = await usersRes.json();
  const teachers = users.filter(u => teacherIds.includes(u.id) && u.phone);

  return new Response(JSON.stringify({ vars: { teachers } }));
}
