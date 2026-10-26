// Student Management System - Frontend Client Logic

let currentStudents = [];
let availableCourses = [];

// DOM Elements
const studentsTableBody = document.getElementById("studentsTableBody");
const searchInput = document.getElementById("searchInput");
const courseFilter = document.getElementById("courseFilter");
const sortFilter = document.getElementById("sortFilter");
const btnResetFilters = document.getElementById("btnResetFilters");

const metricTotalStudents = document.getElementById("metricTotalStudents");
const metricTotalCourses = document.getElementById("metricTotalCourses");
const metricAiStatus = document.getElementById("metricAiStatus");
const aiStatusPill = document.getElementById("aiStatusPill");

const studentModal = document.getElementById("studentModal");
const modalTitle = document.getElementById("modalTitle");
const studentForm = document.getElementById("studentForm");
const studentIdInput = document.getElementById("studentIdInput");
const btnOpenAddModal = document.getElementById("btnOpenAddModal");
const btnCloseModal = document.getElementById("btnCloseModal");
const btnCancelModal = document.getElementById("btnCancelModal");
const formErrorMessage = document.getElementById("formErrorMessage");

const aiQueryForm = document.getElementById("aiQueryForm");
const aiInput = document.getElementById("aiInput");
const btnAskAi = document.getElementById("btnAskAi");
const aiResponseBox = document.getElementById("aiResponseBox");
const aiModelTag = document.getElementById("aiModelTag");
const aiContextTag = document.getElementById("aiContextTag");
const aiAnswerText = document.getElementById("aiAnswerText");

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
  loadStudents();
  loadStats();
  checkAiStatus();
  setupEventListeners();
});

function setupEventListeners() {
  // Search and Filter Handlers
  let searchDebounce;
  searchInput.addEventListener("input", () => {
    clearTimeout(searchDebounce);
    searchDebounce = setTimeout(loadStudents, 300);
  });

  courseFilter.addEventListener("change", loadStudents);
  sortFilter.addEventListener("change", loadStudents);
  btnResetFilters.addEventListener("click", () => {
    searchInput.value = "";
    courseFilter.value = "";
    sortFilter.value = "id-asc";
    loadStudents();
  });

  // Modal Handlers
  btnOpenAddModal.addEventListener("click", () => openStudentModal());
  btnCloseModal.addEventListener("click", closeStudentModal);
  btnCancelModal.addEventListener("click", closeStudentModal);
  studentForm.addEventListener("submit", handleStudentFormSubmit);

  // AI Prompt Chips
  document.querySelectorAll(".prompt-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      aiInput.value = chip.dataset.q;
      aiQueryForm.dispatchEvent(new Event("submit"));
    });
  });

  // AI Query Form
  aiQueryForm.addEventListener("submit", handleAiQuery);
}

// Fetch Students from API
async function loadStudents() {
  try {
    const search = searchInput.value.trim();
    const course = courseFilter.value;
    const [sort_by, order] = sortFilter.value.split("-");

    const params = new URLSearchParams({
      skip: 0,
      limit: 100,
      sort_by: sort_by || "id",
      order: order || "asc"
    });

    if (search) params.append("search", search);
    if (course) params.append("course", course);

    const res = await fetch(`/students?${params.toString()}`);
    if (!res.ok) throw new Error("Failed to fetch students");

    const data = await res.json();
    currentStudents = data;
    renderStudentsTable(data);
  } catch (err) {
    console.error(err);
    studentsTableBody.innerHTML = `<tr><td colspan="7" class="empty-cell">Error loading records: ${err.message}</td></tr>`;
  }
}

// Render Table Rows
function renderStudentsTable(students) {
  if (!students || students.length === 0) {
    studentsTableBody.innerHTML = `<tr><td colspan="7" class="empty-cell">No student records found. Click 'Add New Student' to create one!</td></tr>`;
    return;
  }

  studentsTableBody.innerHTML = students.map(s => `
    <tr>
      <td><strong>#${s.id}</strong></td>
      <td class="student-name-cell">${escapeHtml(s.name)}</td>
      <td><span class="badge-course">${escapeHtml(s.course || 'Unassigned')}</span></td>
      <td>${s.date_of_birth}</td>
      <td>
        <div class="contact-meta">
          <span>✉ ${escapeHtml(s.email)}</span>
          <span>📞 ${escapeHtml(s.phone)}</span>
        </div>
      </td>
      <td>${s.enrollment_date || 'N/A'}</td>
      <td class="text-right">
        <div class="action-btn-group">
          <button class="btn-icon edit" onclick="editStudent(${s.id})" title="Edit Student">✏ Edit</button>
          <button class="btn-icon delete" onclick="deleteStudent(${s.id})" title="Delete Student">🗑 Delete</button>
        </div>
      </td>
    </tr>
  `).join("");
}

// Load Stats & Populate Course Filter
async function loadStats() {
  try {
    const res = await fetch("/students/stats/summary");
    if (!res.ok) return;
    const stats = await res.json();

    metricTotalStudents.textContent = stats.total_students;
    const courseNames = Object.keys(stats.courses_breakdown || {});
    metricTotalCourses.textContent = courseNames.length;

    // Populate course dropdown options
    courseFilter.innerHTML = '<option value="">All Courses</option>' +
      courseNames.map(c => `<option value="${escapeHtml(c)}">${escapeHtml(c)} (${stats.courses_breakdown[c]})</option>`).join("");
  } catch (err) {
    console.warn("Could not load stats:", err);
  }
}

// Check Ollama AI Status
async function checkAiStatus() {
  try {
    const res = await fetch("/ai/status");
    const data = await res.json();

    if (data.ollama_online) {
      aiStatusPill.className = "status-pill online";
      aiStatusPill.textContent = "● Ollama Online (" + data.configured_model + ")";
      metricAiStatus.textContent = "Online (" + data.configured_model + ")";
    } else {
      aiStatusPill.className = "status-pill offline";
      aiStatusPill.textContent = "○ Offline (Safe Fallback Mode)";
      metricAiStatus.textContent = "Offline (Fallback Ready)";
    }
  } catch (err) {
    aiStatusPill.className = "status-pill offline";
    aiStatusPill.textContent = "○ AI Endpoint Offline";
    metricAiStatus.textContent = "Offline";
  }
}

// Modal Handlers
function openStudentModal(student = null) {
  formErrorMessage.classList.add("hidden");
  formErrorMessage.textContent = "";

  if (student) {
    modalTitle.textContent = "Edit Student Profile (#" + student.id + ")";
    studentIdInput.value = student.id;
    document.getElementById("formName").value = student.name;
    document.getElementById("formDob").value = student.date_of_birth;
    document.getElementById("formEmail").value = student.email;
    document.getElementById("formPhone").value = student.phone;
    document.getElementById("formCourse").value = student.course || "";
    document.getElementById("formEnrollment").value = student.enrollment_date || "";
    document.getElementById("formAddress").value = student.address || "";
  } else {
    modalTitle.textContent = "Add New Student Record";
    studentIdInput.value = "";
    studentForm.reset();
    document.getElementById("formEnrollment").value = new Date().toISOString().split("T")[0];
  }

  studentModal.classList.remove("hidden");
}

function closeStudentModal() {
  studentModal.classList.add("hidden");
  studentForm.reset();
}

function editStudent(id) {
  const student = currentStudents.find(s => s.id === id);
  if (student) openStudentModal(student);
}

// Form Submit (POST create or PUT update)
async function handleStudentFormSubmit(e) {
  e.preventDefault();
  formErrorMessage.classList.add("hidden");

  const studentId = studentIdInput.value;
  const payload = {
    name: document.getElementById("formName").value.trim(),
    date_of_birth: document.getElementById("formDob").value,
    email: document.getElementById("formEmail").value.trim(),
    phone: document.getElementById("formPhone").value.trim(),
    course: document.getElementById("formCourse").value.trim() || null,
    enrollment_date: document.getElementById("formEnrollment").value || null,
    address: document.getElementById("formAddress").value.trim() || null
  };

  try {
    const isEdit = Boolean(studentId);
    const url = isEdit ? `/students/${studentId}` : "/students";
    const method = isEdit ? "PUT" : "POST";

    const res = await fetch(url, {
      method: method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) {
      const errMsg = Array.isArray(data.detail) ? data.detail.map(d => d.msg).join(", ") : (data.detail || "Request failed");
      throw new Error(errMsg);
    }

    closeStudentModal();
    await loadStudents();
    await loadStats();
  } catch (err) {
    formErrorMessage.textContent = err.message;
    formErrorMessage.classList.remove("hidden");
  }
}

// Delete Student
async function deleteStudent(id) {
  const student = currentStudents.find(s => s.id === id);
  const name = student ? student.name : `#${id}`;
  if (!confirm(`Are you sure you want to permanently delete student "${name}"?`)) return;

  try {
    const res = await fetch(`/students/${id}`, { method: "DELETE" });
    if (!res.ok) {
      const data = await res.json();
      throw new Error(data.detail || "Delete failed");
    }
    await loadStudents();
    await loadStats();
  } catch (err) {
    alert("Error deleting student: " + err.message);
  }
}

// AI Question Form Submission
async function handleAiQuery(e) {
  e.preventDefault();
  const question = aiInput.value.trim();
  if (!question) return;

  btnAskAi.disabled = true;
  btnAskAi.innerHTML = `<span>Thinking...</span>`;
  aiResponseBox.classList.remove("hidden");
  aiAnswerText.textContent = "Analyzing database records...";

  try {
    const res = await fetch("/ai/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "AI query failed");

    aiModelTag.textContent = data.model;
    aiContextTag.textContent = data.context_summary || `Grounded on ${data.grounded_records_count} record(s)`;
    aiAnswerText.textContent = data.answer;
  } catch (err) {
    aiAnswerText.textContent = "Error: " + err.message;
  } finally {
    btnAskAi.disabled = false;
    btnAskAi.innerHTML = `<span>Ask AI</span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>`;
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/[&<>"']/g, m => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  }[m]));
}
