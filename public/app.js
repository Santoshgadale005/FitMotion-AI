/* FitMotion AI — Interactive WHOOP × Strava × Nike × GOWOD × Darebee Frontend */

const state = {
  meta: null,
  user: null,
  profile: null,
  activeView: "dashboard",
  lib: { category: "All", sport: "All", difficulty: "All", query: "", bodyweightOnly: false, page: 1 },
  generatedRoutine: null,
  checkedSteps: {},
  chatMessages: [],
};

const QUICK_PROMPTS = [
  "What should I do before playing football?",
  "Give me a 15-minute full-body mobility routine.",
  "How can I improve my flexibility?",
  "Suggest a warm-up before badminton.",
  "What exercises can I do without gym equipment?",
  "Give me a beginner-friendly stretching routine.",
  "Suggest a cooldown after running.",
];

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Request failed");
  return data;
}

function esc(str) {
  return String(str ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function showToast(msg) {
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.classList.remove("hidden");
  clearTimeout(window._toastTimer);
  window._toastTimer = setTimeout(() => el.classList.add("hidden"), 3200);
}

function updateUserBadge() {
  const badge = document.getElementById("user-badge");
  if (state.user && state.profile) {
    badge.textContent = `● ${state.profile.full_name} · ${state.profile.primary_sport}`;
  } else if (state.user) {
    badge.textContent = `● ${state.user.full_name}`;
  } else {
    badge.textContent = "○ Guest Preview Mode";
  }
}

function whoopRingHTML(pct, label, sublabel, color) {
  const clamped = Math.max(0, Math.min(100, Number(pct) || 0));
  const r = 44;
  const circ = 2 * Math.PI * r;
  const offset = circ * (1 - clamped / 100);
  return `
    <div style="display:flex;flex-direction:column;align-items:center;min-width:130px;">
      <svg width="116" height="116" viewBox="0 0 116 116">
        <circle cx="58" cy="58" r="${r}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="9"/>
        <circle cx="58" cy="58" r="${r}" fill="none" stroke="${color}" stroke-width="9" stroke-linecap="round"
                stroke-dasharray="${circ.toFixed(1)}" stroke-dashoffset="${offset.toFixed(1)}"
                transform="rotate(-90 58 58)"/>
        <text x="58" y="57" text-anchor="middle" font-family="Barlow Condensed,Inter,sans-serif" font-size="28" font-weight="800" fill="#fff">${Math.round(clamped)}%</text>
        <text x="58" y="73" text-anchor="middle" font-family="Inter,sans-serif" font-size="8.5" font-weight="700" fill="#9ca3af" letter-spacing="1">${esc(label.toUpperCase())}</text>
      </svg>
      <div style="font-size:0.74rem;color:#a1a1aa;text-align:center;">${esc(sublabel)}</div>
    </div>
  `;
}

function posterGridHTML(schedule) {
  return `
    <div class="poster-grid">
      ${schedule
        .map((d, i) => {
          const intensity = d.intensity || (d.is_rest_day ? "Rest" : "Moderate");
          const cls = intensity.toLowerCase();
          const dayLbl = (d.day || d.day_name || `Day ${i + 1}`).slice(0, 3);
          const title = d.title || d.routine_title || "Rest Day";
          const dur = d.duration_min || d.estimated_duration_min || 0;
          const doneMark = d.status === "completed" ? "✓ " : "";
          const meta = intensity === "Rest" ? "REST DAY" : `${doneMark}${intensity.toUpperCase()} · ${dur}M`;
          return `
            <div class="day-tile ${cls}">
              <div class="day-num">D0${i + 1} · ${esc(dayLbl)}</div>
              <div class="day-title">${esc(title)}</div>
              <div class="day-meta">${esc(meta)}</div>
            </div>
          `;
        })
        .join("")}
    </div>
  `;
}

function exerciseCardHTML(ex, { showExplanation = false, showPrescription = false, stepIndex = null } = {}) {
  const diffCls = ex.difficulty_level === "Advanced" ? "chip-orange" : ex.difficulty_level === "Intermediate" ? "chip-cyan" : "chip-green";
  const equip = ex.required_equipment && ex.required_equipment.length ? ex.required_equipment.join(", ") : "Bodyweight";
  const sets = ex.prescribed_sets || ex.recommended_sets || 2;
  const reps = ex.prescribed_reps || ex.recommended_reps || "10";
  const rest = ex.prescribed_rest_sec || ex.rest_seconds || 30;
  const rating = ex.user_rating || 0;

  const stepHeader =
    stepIndex !== null
      ? `<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.55rem;">
           <span class="pill pill-orange">STEP ${String(stepIndex).padStart(2, "0")} · ${esc(ex.phase || ex.category)}</span>
           <label style="font-size:0.8rem;color:#e4e4e7;display:flex;align-items:center;gap:0.4rem;cursor:pointer;">
             <input type="checkbox" class="step-check" data-step="${stepIndex}" ${state.checkedSteps[stepIndex] ? "checked" : ""}/> Completed
           </label>
         </div>`
      : "";

  return `
    <div class="card">
      ${stepHeader}
      <img class="ex-visual" src="/${esc(ex.media_reference)}" alt="${esc(ex.name)}" loading="lazy" />
      <div style="display:flex;justify-content:space-between;align-items:center;margin-top:0.65rem;gap:0.4rem;flex-wrap:wrap;">
        <div class="chip-row">
          <span class="chip ${diffCls}">${esc(ex.difficulty_level)}</span>
          <span class="chip">${esc(equip)}</span>
          ${showExplanation && ex.match_score ? `<span class="chip chip-cyan">AI Match ${ex.match_score}%</span>` : ""}
        </div>
        <span style="font-size:0.75rem;color:#a1a1aa;font-weight:600;">${sets}×${esc(reps)} · Rest ${rest}s</span>
      </div>
      <div class="ex-title">${esc(ex.name)}</div>
      <p class="ex-desc">${esc(ex.description)}</p>
      <div class="chip-row">
        ${(ex.target_muscles || []).slice(0, 3).map((m) => `<span class="chip">${esc(m)}</span>`).join("")}
        ${(ex.relevant_sports || []).slice(0, 3).map((s) => `<span class="chip chip-cyan">${esc(s)}</span>`).join("")}
      </div>
      ${showExplanation && ex.explanation ? `<div class="ex-why"><strong>Why recommended:</strong> ${esc(ex.explanation)}</div>` : ""}
      <details class="ex-details">
        <summary>Form Cues, Safety Precautions &amp; Beginner Modification</summary>
        <div style="margin-top:0.55rem;font-size:0.75rem;font-weight:700;color:#9ca3af;text-transform:uppercase;">Instructions</div>
        <ol>${(ex.instructions || []).map((s) => `<li>${esc(s)}</li>`).join("")}</ol>
        <div style="font-size:0.75rem;font-weight:700;color:#ffb020;text-transform:uppercase;">Safety Precautions</div>
        <ul>${(ex.safety_instructions || []).map((s) => `<li>${esc(s)}</li>`).join("")}</ul>
        <div style="font-size:0.75rem;font-weight:700;color:#f87171;text-transform:uppercase;">Common Mistakes</div>
        <ul>${(ex.common_mistakes || []).map((s) => `<li>${esc(s)}</li>`).join("")}</ul>
        ${ex.beginner_modification ? `<div style="margin-top:0.4rem;font-size:0.81rem;color:#69f0ae;"><strong>Beginner Mod:</strong> ${esc(ex.beginner_modification)}</div>` : ""}
      </details>
      ${
        state.user
          ? `<div class="ex-actions">
               <select class="rate-select" data-ex="${esc(ex.id)}" style="background:#0c0d12;color:#fff;border:1px solid rgba(255,255,255,0.16);border-radius:8px;padding:0.35rem 0.55rem;font-size:0.78rem;">
                 <option value="0" ${rating === 0 ? "selected" : ""}>Rate for ML...</option>
                 ${[5, 4, 3, 2, 1].map((n) => `<option value="${n}" ${rating === n ? "selected" : ""}>${"★".repeat(n)} (${n}/5)</option>`).join("")}
               </select>
               <button class="btn btn-secondary btn-sm btn-exclude" data-ex="${esc(ex.id)}" data-excl="${ex.is_excluded ? "1" : "0"}">
                 ${ex.is_excluded ? "Restore" : "Exclude"}
               </button>
             </div>`
          : ""
      }
    </div>
  `;
}

function bindExerciseCardActions(container, onReload) {
  container.querySelectorAll(".rate-select").forEach((sel) => {
    sel.addEventListener("change", async (e) => {
      const val = Number(e.target.value);
      if (!val || !state.user) return;
      await api("/api/feedback", {
        method: "POST",
        body: JSON.stringify({ user_id: state.user.id, exercise_id: e.target.dataset.ex, rating: val }),
      });
      showToast(`Saved ${val}/5 rating — Ridge ML ranker updated!`);
      if (onReload) onReload();
    });
  });

  container.querySelectorAll(".btn-exclude").forEach((btn) => {
    btn.addEventListener("click", async () => {
      if (!state.user) return;
      const currentlyExcluded = btn.dataset.excl === "1";
      await api("/api/feedback", {
        method: "POST",
        body: JSON.stringify({
          user_id: state.user.id,
          exercise_id: btn.dataset.ex,
          is_excluded: !currentlyExcluded,
        }),
      });
      showToast(currentlyExcluded ? "Exercise restored to recommendations." : "Exercise excluded from recommendations.");
      if (onReload) onReload();
    });
  });
}

/* ==================== VIEWS ==================== */

async function renderDashboard() {
  const root = document.getElementById("app-view");
  const uid = state.user?.id || null;
  const [recs, analytics, planner] = await Promise.all([
    api("/api/recommendations", { method: "POST", body: JSON.stringify({ user_id: uid, top_n: 3 }) }),
    uid ? api(`/api/analytics/${uid}`) : Promise.resolve(null),
    uid ? api(`/api/planner/${uid}`) : Promise.resolve(null),
  ]);

  const prof = state.profile || { full_name: "Guest Athlete", primary_sport: "Football", experience_level: "Intermediate", primary_goal: "Improve mobility", available_duration_min: 25, preferred_intensity: "Moderate" };
  const pct = analytics ? analytics.weekly_goal_adherence_pct : 0;
  const ringColor = pct >= 75 ? "#00e676" : pct >= 40 ? "#ffb020" : "#fc4c02";
  const ringSub = analytics ? `${analytics.workouts_last_7_days}/${analytics.weekly_target_frequency} sessions this week` : "Sign in to track goal";

  root.innerHTML = `
    <section class="hero">
      <div class="hero-split">
        <div>
          <div class="pill-row">
            <span class="pill pill-orange">${esc(prof.primary_sport)} · ${esc(prof.experience_level)}</span>
            <span class="pill ${recs.ml_active ? "pill-green" : "pill-cyan"}">● ${recs.ml_active ? "Hybrid ML + Rules Active" : "Rule-Based AI Active"}</span>
          </div>
          <h1>Ready to Train, ${esc(prof.full_name)}</h1>
          <p>
            Primary Goal: <strong style="color:#fff;">${esc(prof.primary_goal)}</strong> ·
            Session Budget: <strong style="color:#fff;">${prof.available_duration_min} min</strong> ·
            Intensity: <strong style="color:#fff;">${esc(prof.preferred_intensity)}</strong>
          </p>
        </div>
        ${whoopRingHTML(pct, "Weekly Goal", ringSub, ringColor)}
      </div>
    </section>

    <div class="grid-4" style="margin-bottom:1.1rem;">
      <button class="btn btn-primary" data-jump="generator">🔥 Build Custom Workout</button>
      <button class="btn btn-secondary" data-jump="library">🏃 Browse ${state.meta.counts.total_exercises} Exercises</button>
      <button class="btn btn-secondary" data-jump="plans">🗂️ 4-Week Sport Plans</button>
      <button class="btn btn-secondary" data-jump="assistant">🤖 Ask AI Coach</button>
    </div>

    <div class="grid-4">
      <div class="card">
        <div class="kpi-label">Exercise Catalog</div>
        <div class="kpi-value">${state.meta.counts.total_exercises}</div>
        <div class="kpi-sub">${state.meta.counts.Advanced} Advanced · 8 Sports</div>
      </div>
      <div class="card">
        <div class="kpi-label">Sessions Logged</div>
        <div class="kpi-value" style="color:var(--green);">${analytics ? analytics.total_workouts : 0}</div>
        <div class="kpi-sub">${analytics ? `${analytics.workouts_last_7_days} in last 7 days` : "No logs yet"}</div>
      </div>
      <div class="card">
        <div class="kpi-label">Training Volume</div>
        <div class="kpi-value" style="color:var(--cyan);">${analytics ? `${analytics.total_minutes}m` : `${prof.available_duration_min}m`}</div>
        <div class="kpi-sub">${analytics ? `${analytics.total_hours} total hours logged` : "Per-session budget"}</div>
      </div>
      <div class="card">
        <div class="kpi-label">AI Personalization</div>
        <div class="kpi-value" style="color:var(--orange);">${recs.ml_active ? "ML LIVE" : "RULES"}</div>
        <div class="kpi-sub">${recs.ml_active ? `Trained on ${recs.ml_training_samples} signals` : "Rate 2+ drills to train ML"}</div>
      </div>
    </div>

    <div class="section-title">Top AI Exercise Picks For You</div>
    <div class="grid-3">
      ${recs.recommendations.map((ex) => exerciseCardHTML(ex, { showExplanation: true })).join("")}
    </div>

    <div class="section-title">This Week At A Glance (Darebee Strip)</div>
    ${planner && planner.week ? posterGridHTML(planner.week) : `<div class="card">No weekly schedule yet. Visit Weekly Planner or 4-Week Sport Plans to apply a full program.</div>`}

    <div class="card" style="margin-top:1rem;">
      <div class="kpi-label">${esc(prof.primary_sport)} Athletic Demands</div>
      <p style="color:#d4d4d8;font-size:0.9rem;margin:0.35rem 0 0.7rem;">${esc(recs.sport_profile.summary)}</p>
      <div class="chip-row">
        ${recs.sport_profile.physical_demands.map((d) => `<span class="chip chip-cyan">${esc(d)}</span>`).join("")}
      </div>
    </div>
  `;

  root.querySelectorAll("[data-jump]").forEach((b) => b.addEventListener("click", () => switchView(b.dataset.jump)));
  bindExerciseCardActions(root, renderDashboard);
}

async function renderLibrary() {
  const root = document.getElementById("app-view");
  const params = new URLSearchParams({
    query: state.lib.query,
    category: state.lib.category,
    sport: state.lib.sport,
    difficulty: state.lib.difficulty,
    bodyweight_only: state.lib.bodyweightOnly ? "true" : "false",
  });
  if (state.user) params.set("user_id", String(state.user.id));

  const data = await api(`/api/exercises?${params.toString()}`);
  const pageSize = 12;
  const totalPages = Math.max(1, Math.ceil(data.total / pageSize));
  state.lib.page = Math.min(state.lib.page, totalPages);
  const slice = data.exercises.slice((state.lib.page - 1) * pageSize, state.lib.page * pageSize);

  const shortMap = {
    All: "All",
    "Warm-up": "Warm-up",
    Mobility: "Mobility",
    "Stretching and Flexibility": "Stretch",
    "Strength Training": "Strength",
    "Cardiovascular Training": "Cardio",
    "Balance and Stability": "Balance",
    "Recovery and Cooldown": "Recovery",
    "Sport-Specific Conditioning": "Sport Drills",
  };

  root.innerHTML = `
    <section class="hero">
      <div class="pill-row">
        <span class="pill pill-green">● ${state.meta.counts.total_exercises} Animated Motion Demos</span>
        <span class="pill pill-cyan">${state.meta.counts.Beginner} Beginner · ${state.meta.counts.Intermediate} Intermediate · ${state.meta.counts.Advanced} Advanced</span>
      </div>
      <h1>Exercise Library</h1>
      <p>GOWOD-inspired visual catalog across 8 categories and 8 sports. Switching <strong>Relevant Sport</strong> prioritizes sport-authentic drills at the top.</p>
    </section>

    <div class="pill-row" style="margin-bottom:0.95rem;">
      ${["All", ...state.meta.categories]
        .map((c) => `<button class="pill-btn ${state.lib.category === c ? "active" : ""}" data-cat="${esc(c)}">${esc(shortMap[c] || c)}</button>`)
        .join("")}
    </div>

    <div class="form-grid">
      <div class="field">
        <label>Search Exercise / Muscle</label>
        <input id="lib-q" value="${esc(state.lib.query)}" placeholder="e.g., Nordic, Copenhagen, badminton, swim..." />
      </div>
      <div class="field">
        <label>Relevant Sport</label>
        <select id="lib-sport">
          ${["All", ...state.meta.sports].map((s) => `<option value="${esc(s)}" ${state.lib.sport === s ? "selected" : ""}>${esc(s)}</option>`).join("")}
        </select>
      </div>
      <div class="field">
        <label>Difficulty</label>
        <select id="lib-diff">
          ${["All", ...state.meta.levels].map((l) => `<option value="${esc(l)}" ${state.lib.difficulty === l ? "selected" : ""}>${esc(l)}</option>`).join("")}
        </select>
      </div>
      <div class="field" style="display:flex;align-items:flex-end;">
        <label style="display:flex;align-items:center;gap:0.45rem;margin-bottom:0.65rem;cursor:pointer;color:#e4e4e7;">
          <input type="checkbox" id="lib-bw" ${state.lib.bodyweightOnly ? "checked" : ""} style="width:auto;" /> Bodyweight Only
        </label>
      </div>
    </div>

    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem;flex-wrap:wrap;gap:0.5rem;">
      <div style="font-size:0.84rem;color:#a1a1aa;">
        Showing <strong>${data.total}</strong> exercises${state.lib.sport !== "All" ? ` prioritized for <strong>${esc(state.lib.sport)}</strong>` : ""}${state.lib.difficulty !== "All" ? ` · <strong>${esc(state.lib.difficulty)}</strong>` : ""} (Page ${state.lib.page} of ${totalPages})
      </div>
      ${
        totalPages > 1
          ? `<div style="display:flex;gap:0.5rem;">
               <button class="btn btn-secondary btn-sm" id="lib-prev" ${state.lib.page <= 1 ? "disabled" : ""}>← Prev</button>
               <button class="btn btn-secondary btn-sm" id="lib-next" ${state.lib.page >= totalPages ? "disabled" : ""}>Next →</button>
             </div>`
          : ""
      }
    </div>

    <div class="grid-2">
      ${slice.length ? slice.map((ex) => exerciseCardHTML(ex)).join("") : `<div class="card">No exercises match those filters.</div>`}
    </div>
  `;

  root.querySelectorAll("[data-cat]").forEach((b) =>
    b.addEventListener("click", () => {
      state.lib.category = b.dataset.cat;
      state.lib.page = 1;
      renderLibrary();
    })
  );
  let debounce;
  document.getElementById("lib-q").addEventListener("input", (e) => {
    clearTimeout(debounce);
    debounce = setTimeout(() => {
      state.lib.query = e.target.value;
      state.lib.page = 1;
      renderLibrary();
    }, 240);
  });
  document.getElementById("lib-sport").addEventListener("change", (e) => {
    state.lib.sport = e.target.value;
    state.lib.page = 1;
    renderLibrary();
  });
  document.getElementById("lib-diff").addEventListener("change", (e) => {
    state.lib.difficulty = e.target.value;
    state.lib.page = 1;
    renderLibrary();
  });
  document.getElementById("lib-bw").addEventListener("change", (e) => {
    state.lib.bodyweightOnly = e.target.checked;
    state.lib.page = 1;
    renderLibrary();
  });
  document.getElementById("lib-prev")?.addEventListener("click", () => { state.lib.page--; renderLibrary(); });
  document.getElementById("lib-next")?.addEventListener("click", () => { state.lib.page++; renderLibrary(); });
  bindExerciseCardActions(root, renderLibrary);
}

async function renderRecommendations(customOverrides = null) {
  const root = document.getElementById("app-view");
  const prof = state.profile || { primary_sport: "Football", primary_goal: "Improve mobility", experience_level: "Intermediate", preferred_intensity: "Moderate" };
  const payload = {
    user_id: state.user?.id || null,
    top_n: 10,
    primary_sport: customOverrides?.primary_sport || prof.primary_sport,
    primary_goal: customOverrides?.primary_goal || prof.primary_goal,
    experience_level: customOverrides?.experience_level || prof.experience_level,
    preferred_intensity: customOverrides?.preferred_intensity || prof.preferred_intensity,
  };
  const res = await api("/api/recommendations", { method: "POST", body: JSON.stringify(payload) });

  root.innerHTML = `
    <section class="hero">
      <div class="pill-row">
        <span class="pill ${res.ml_active ? "pill-green" : "pill-orange"}">${res.ml_active ? "● Hybrid Rule + Ridge ML Active" : "● Rule-Based AI Active"}</span>
        <span class="pill pill-cyan">${res.ml_training_samples} ML Signals · ${res.filtered_out_count} Safety/Equip Filtered</span>
      </div>
      <h1>AI Exercise Recommendations</h1>
      <p>Every recommendation blends sports-science rules with personalized Ridge regression + cosine-similarity reranking and explains why each exercise fits your profile.</p>
    </section>

    <div class="card" style="margin-bottom:1.1rem;">
      <div class="form-grid" style="margin-bottom:0.4rem;">
        <div class="field"><label>Sport</label><select id="rec-sport">${state.meta.sports.map((s) => `<option ${payload.primary_sport === s ? "selected" : ""}>${esc(s)}</option>`).join("")}</select></div>
        <div class="field"><label>Primary Goal</label><select id="rec-goal">${state.meta.goals.map((g) => `<option ${payload.primary_goal === g ? "selected" : ""}>${esc(g)}</option>`).join("")}</select></div>
        <div class="field"><label>Experience</label><select id="rec-exp">${state.meta.levels.map((l) => `<option ${payload.experience_level === l ? "selected" : ""}>${esc(l)}</option>`).join("")}</select></div>
        <div class="field"><label>Intensity</label><select id="rec-int">${state.meta.intensities.map((i) => `<option ${payload.preferred_intensity === i ? "selected" : ""}>${esc(i)}</option>`).join("")}</select></div>
      </div>
      <button class="btn btn-primary btn-sm" id="rec-run">⚡ Re-Rank Recommendations</button>
    </div>

    <div class="grid-2">
      ${res.recommendations.map((ex) => exerciseCardHTML(ex, { showExplanation: true })).join("")}
    </div>
  `;

  document.getElementById("rec-run").addEventListener("click", () => {
    renderRecommendations({
      primary_sport: document.getElementById("rec-sport").value,
      primary_goal: document.getElementById("rec-goal").value,
      experience_level: document.getElementById("rec-exp").value,
      preferred_intensity: document.getElementById("rec-int").value,
    });
  });
  bindExerciseCardActions(root, () => renderRecommendations(payload));
}

async function renderGenerator() {
  const root = document.getElementById("app-view");
  const prof = state.profile || { primary_sport: "Football", experience_level: "Intermediate", available_duration_min: 20, preferred_intensity: "Moderate" };

  if (!state.generatedRoutine) {
    const res = await api("/api/routines/generate", {
      method: "POST",
      body: JSON.stringify({
        user_id: state.user?.id || null,
        routine_type: "20-minute full-body workout",
        duration_min: prof.available_duration_min || 20,
        primary_sport: prof.primary_sport,
        difficulty: prof.experience_level,
        intensity: prof.preferred_intensity,
      }),
    });
    state.generatedRoutine = res.routine;
    state.checkedSteps = {};
  }

  const r = state.generatedRoutine;
  const totalEx = r.exercises.length || 1;
  const doneCount = Object.values(state.checkedSteps).filter(Boolean).length;
  const pctDone = Math.round((doneCount / totalEx) * 100);

  root.innerHTML = `
    <section class="hero">
      <span class="pill pill-orange">Guided Session Runner &amp; Custom Builder</span>
      <h1>Personalized Workout Generator</h1>
      <p>Generate time-budgeted routines across 9 presets, check off steps live, save favorites, and log directly to your Progress Dashboard.</p>
    </section>

    <div class="card" style="margin-bottom:1.1rem;">
      <div class="form-grid">
        <div class="field"><label>Routine Type</label><select id="gen-type">${state.meta.routine_types.map((t) => `<option ${r.routine_type === t ? "selected" : ""}>${esc(t)}</option>`).join("")}</select></div>
        <div class="field"><label>Sport</label><select id="gen-sport">${state.meta.sports.map((s) => `<option ${r.target_sport === s ? "selected" : ""}>${esc(s)}</option>`).join("")}</select></div>
        <div class="field"><label>Duration (min)</label><input id="gen-dur" type="number" min="5" max="60" step="5" value="${r.target_duration_min || 20}" /></div>
        <div class="field"><label>Difficulty</label><select id="gen-diff">${state.meta.levels.map((l) => `<option ${r.difficulty_level === l ? "selected" : ""}>${esc(l)}</option>`).join("")}</select></div>
        <div class="field"><label>Intensity</label><select id="gen-int">${state.meta.intensities.map((i) => `<option ${r.intensity === i ? "selected" : ""}>${esc(i)}</option>`).join("")}</select></div>
      </div>
      <button class="btn btn-primary" id="gen-go">⚡ Generate Personalized Routine</button>
    </div>

    <div class="card" style="margin-bottom:1.1rem;">
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.75rem;">
        <div>
          <h2 style="font-size:1.75rem;">${esc(r.title)}</h2>
          <div style="font-size:0.84rem;color:#a1a1aa;">~${r.estimated_duration_min} min · ${r.exercises.length} exercises · ${esc(r.intensity)} intensity · ${r.ml_active ? "Hybrid ML" : "Rule-Based"}</div>
        </div>
        <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">
          <button class="btn btn-secondary btn-sm" id="gen-save">⭐ Save Favorite</button>
          <button class="btn btn-primary btn-sm" id="gen-log">✅ Log Workout (${doneCount ? pctDone : 100}%)</button>
        </div>
      </div>
      <div style="margin-top:0.8rem;font-size:0.8rem;color:#a1a1aa;">Guided Session Progress: ${doneCount} / ${r.exercises.length} steps completed (${pctDone}%)</div>
      <div class="progress-track"><div class="progress-fill" style="width:${pctDone}%"></div></div>
    </div>

    <div class="grid-2">
      ${r.exercises.map((ex, i) => exerciseCardHTML(ex, { showExplanation: true, showPrescription: true, stepIndex: i + 1 })).join("")}
    </div>
  `;

  document.getElementById("gen-go").addEventListener("click", async () => {
    const res = await api("/api/routines/generate", {
      method: "POST",
      body: JSON.stringify({
        user_id: state.user?.id || null,
        routine_type: document.getElementById("gen-type").value,
        primary_sport: document.getElementById("gen-sport").value,
        duration_min: Number(document.getElementById("gen-dur").value),
        difficulty: document.getElementById("gen-diff").value,
        intensity: document.getElementById("gen-int").value,
      }),
    });
    state.generatedRoutine = res.routine;
    state.checkedSteps = {};
    renderGenerator();
  });

  root.querySelectorAll(".step-check").forEach((chk) => {
    chk.addEventListener("change", (e) => {
      state.checkedSteps[Number(e.target.dataset.step)] = e.target.checked;
      renderGenerator();
    });
  });

  document.getElementById("gen-save").addEventListener("click", async () => {
    if (!state.user) return showToast("Sign in under Profile to save favorites.");
    await api(`/api/routines/${state.user.id}/save`, {
      method: "POST",
      body: JSON.stringify({ routine: r, is_favorite: true }),
    });
    showToast("Saved routine to Favorites!");
  });

  document.getElementById("gen-log").addEventListener("click", async () => {
    if (!state.user) return showToast("Sign in under Profile to log workouts.");
    const pct = doneCount > 0 ? pctDone : 100;
    await api(`/api/history/${state.user.id}/log`, {
      method: "POST",
      body: JSON.stringify({
        routine_title: r.title,
        actual_duration_min: r.estimated_duration_min || 20,
        completion_percentage: pct,
        perceived_effort_rpe: r.intensity === "High" ? 8 : r.intensity === "Low" ? 4 : 6,
        exercises_completed: r.exercises.map((e, i) => ({
          exercise_id: e.id,
          name: e.name,
          category: e.category,
          completed: doneCount > 0 ? Boolean(state.checkedSteps[i + 1]) : true,
        })),
        notes: `Logged from Workout Generator (${r.target_sport}).`,
      }),
    });
    showToast("Workout logged to History & Progress Dashboard!");
  });

  bindExerciseCardActions(root);
}

async function renderPlans(filterSport = "All", filterDiff = "All") {
  const root = document.getElementById("app-view");
  const data = await api(`/api/plans?sport=${encodeURIComponent(filterSport)}&difficulty=${encodeURIComponent(filterDiff)}`);

  root.innerHTML = `
    <section class="hero">
      <span class="pill pill-orange">Darebee-Inspired Visual Programs · NSCA / ACSM / FIFA 11+ / BWF</span>
      <h1>Complete 4-Week Sport &amp; Fitness Plans</h1>
      <p>Structured, recovery-balanced 7-day weekly cycles across every sport. Apply any program directly to your Weekly Training Planner in one click.</p>
    </section>

    <div class="form-grid" style="max-width:520px;">
      <div class="field"><label>Sport</label><select id="pl-sport">${["All", ...state.meta.sports].map((s) => `<option ${filterSport === s ? "selected" : ""}>${esc(s)}</option>`).join("")}</select></div>
      <div class="field"><label>Difficulty</label><select id="pl-diff">${["All", ...state.meta.levels].map((l) => `<option ${filterDiff === l ? "selected" : ""}>${esc(l)}</option>`).join("")}</select></div>
    </div>

    <div style="display:flex;flex-direction:column;gap:1.1rem;">
      ${data.plans
        .map(
          (p) => `
          <div class="card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.8rem;">
              <div>
                <div class="pill-row" style="margin-bottom:0.45rem;">
                  <span class="pill pill-orange">${esc(p.sport)}</span>
                  <span class="pill pill-cyan">${esc(p.difficulty)}</span>
                  <span class="pill pill-dim">${p.duration_weeks} Weeks · ${p.days_per_week} Days/Wk</span>
                </div>
                <h2 style="font-size:1.65rem;">${esc(p.title)}</h2>
                <div style="font-size:0.8rem;color:#9ca3af;margin-top:0.2rem;">Framework: ${esc(p.framework)}</div>
                <p style="font-size:0.88rem;color:#d4d4d8;margin:0.45rem 0 0;">${esc(p.summary)}</p>
              </div>
              <button class="btn btn-primary btn-sm apply-plan-btn" data-plan="${esc(p.id)}">📅 Apply to Weekly Planner</button>
            </div>
            ${posterGridHTML(p.weekly_schedule)}
            <details class="ex-details">
              <summary>Inspect Exercise-by-Exercise Sequence</summary>
              <ul>
                ${p.weekly_schedule
                  .map((d) =>
                    d.intensity === "Rest"
                      ? `<li><strong>${esc(d.day)}:</strong> ${esc(d.title)} (Rest)</li>`
                      : `<li><strong>${esc(d.day)} — ${esc(d.title)}:</strong> ${(d.exercise_details || []).map((e) => esc(e.name)).join(" → ")}</li>`
                  )
                  .join("")}
              </ul>
            </details>
          </div>
        `
        )
        .join("")}
    </div>
  `;

  document.getElementById("pl-sport").addEventListener("change", (e) => renderPlans(e.target.value, filterDiff));
  document.getElementById("pl-diff").addEventListener("change", (e) => renderPlans(filterSport, e.target.value));
  root.querySelectorAll(".apply-plan-btn").forEach((btn) =>
    btn.addEventListener("click", async () => {
      if (!state.user) return showToast("Sign in under Profile to apply a plan.");
      const res = await api("/api/plans/apply", {
        method: "POST",
        body: JSON.stringify({ user_id: state.user.id, plan_id: btn.dataset.plan }),
      });
      showToast(res.message.replace(/\*\*/g, ""));
    })
  );
}

async function renderSports(selectedSport = null) {
  const root = document.getElementById("app-view");
  const sport = selectedSport || state.profile?.primary_sport || "Football";
  const spMeta = state.meta.sport_profiles[sport];
  const [routineRes, plansRes] = await Promise.all([
    api("/api/routines/generate", {
      method: "POST",
      body: JSON.stringify({
        user_id: state.user?.id || null,
        routine_type: "Sport-specific conditioning routine",
        duration_min: 25,
        primary_sport: sport,
      }),
    }),
    api(`/api/plans?sport=${encodeURIComponent(sport)}`),
  ]);

  root.innerHTML = `
    <section class="hero">
      <span class="pill pill-orange">Multi-Sport Conditioning Science</span>
      <h1>${esc(sport)} Conditioning Hub</h1>
      <p>${esc(spMeta.summary)}</p>
    </section>

    <div class="pill-row" style="margin-bottom:1.1rem;">
      ${state.meta.sports.map((s) => `<button class="pill-btn ${sport === s ? "active" : ""}" data-sp="${esc(s)}">${esc(s)}</button>`).join("")}
    </div>

    <div class="grid-2" style="margin-bottom:1.1rem;">
      <div class="card">
        <div class="kpi-label">Physical Demands</div>
        <div class="chip-row" style="margin-top:0.5rem;">${spMeta.physical_demands.map((d) => `<span class="chip chip-orange">${esc(d)}</span>`).join("")}</div>
      </div>
      <div class="card">
        <div class="kpi-label">Warm-up &amp; Recovery Protocol</div>
        <p style="font-size:0.84rem;color:#d4d4d8;margin:0.4rem 0;"><strong>Warm-up:</strong> ${esc(spMeta.warmup_focus)}</p>
        <p style="font-size:0.84rem;color:#d4d4d8;margin:0.4rem 0 0;"><strong>Recovery:</strong> ${esc(spMeta.recovery_focus)}</p>
      </div>
    </div>

    ${plansRes.plans.length ? `<div class="section-title">${esc(sport)} 4-Week Program</div>${posterGridHTML(plansRes.plans[0].weekly_schedule)}` : ""}

    <div class="section-title">Generated ${esc(sport)} Conditioning Session (~${routineRes.routine.estimated_duration_min} min)</div>
    <div class="grid-2">
      ${routineRes.routine.exercises.map((ex) => exerciseCardHTML(ex, { showExplanation: true, showPrescription: true })).join("")}
    </div>
  `;

  root.querySelectorAll("[data-sp]").forEach((b) => b.addEventListener("click", () => renderSports(b.dataset.sp)));
  bindExerciseCardActions(root);
}

function renderAssistant() {
  const root = document.getElementById("app-view");
  if (!state.chatMessages.length) {
    state.chatMessages.push({
      role: "assistant",
      text: `Hi ${state.profile?.full_name || "Athlete"}! Ask me anything about warm-ups, mobility, flexibility, equipment-free workouts, cooldowns, or sport-specific prep. Every answer pulls directly from FitMotion AI's 90-exercise database & recommendation engine.`,
      mode: "FitMotion Local Engine (Offline-Ready)",
    });
  }

  root.innerHTML = `
    <section class="hero">
      <span class="pill pill-green">● Grounded in 90-Exercise Catalog · Medical Safety Guardrail</span>
      <h1>AI Training Assistant</h1>
      <p>Ask natural-language training questions and get structured routines with rationales and safety cues. Automatically detects pain/injury queries and directs to professional medical care.</p>
    </section>

    <div class="pill-row">
      ${QUICK_PROMPTS.map((q) => `<button class="pill-btn qp-btn" data-q="${esc(q)}">${esc(q)}</button>`).join("")}
    </div>

    <div class="chat-box" id="chat-box">
      ${state.chatMessages
        .map(
          (m) => `
          <div class="chat-msg ${m.role}">
            <div>${esc(m.text).replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>").replace(/### (.*)/g, "<h3 style='margin:0.2rem 0 0.4rem;'>$1</h3>")}</div>
            ${m.mode ? `<div style="margin-top:0.45rem;font-size:0.72rem;color:#9ca3af;">Engine: ${esc(m.mode)}</div>` : ""}
          </div>
        `
        )
        .join("")}
    </div>

    <form class="chat-input-row" id="chat-form">
      <input id="chat-input" placeholder="Ask e.g. 'Give me a 15-minute badminton mobility routine without equipment'..." autocomplete="off" />
      <button class="btn btn-primary" type="submit">Send</button>
    </form>
  `;

  const box = document.getElementById("chat-box");
  box.scrollTop = box.scrollHeight;

  async function ask(q) {
    if (!q.trim()) return;
    state.chatMessages.push({ role: "user", text: q });
    renderAssistant();
    const res = await api("/api/assistant/ask", {
      method: "POST",
      body: JSON.stringify({ question: q, user_id: state.user?.id || null }),
    });
    state.chatMessages.push({ role: "assistant", text: res.answer, mode: res.mode });
    renderAssistant();
  }

  document.getElementById("chat-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const inp = document.getElementById("chat-input");
    ask(inp.value);
  });
  root.querySelectorAll(".qp-btn").forEach((b) => b.addEventListener("click", () => ask(b.dataset.q)));
}

async function renderPlanner() {
  const root = document.getElementById("app-view");
  if (!state.user) {
    root.innerHTML = `<div class="card">Sign in or load the Demo Athlete under <strong>Profile &amp; Sign In</strong> to manage your Weekly Training Planner.</div>`;
    return;
  }

  const [planner, history] = await Promise.all([
    api(`/api/planner/${state.user.id}`),
    api(`/api/history/${state.user.id}`),
  ]);

  root.innerHTML = `
    <section class="hero">
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
        <div>
          <span class="pill pill-cyan">Load-Balanced Scheduling &amp; Rest-Day Protection</span>
          <h1>Weekly Training Planner &amp; History</h1>
          <p>Visual 7-day calendar with automatic load-balance guardrails and instant workout completion logging.</p>
        </div>
        <button class="btn btn-primary" id="auto-week-btn">⚡ Auto-Generate Balanced Week</button>
      </div>
    </section>

    <div class="grid-4">
      <div class="card"><div class="kpi-label">Planned Workouts</div><div class="kpi-value">${planner.load.planned_workouts}</div></div>
      <div class="card"><div class="kpi-label">Protected Rest Days</div><div class="kpi-value" style="color:var(--green);">${planner.load.rest_days}</div></div>
      <div class="card"><div class="kpi-label">High-Intensity Days</div><div class="kpi-value" style="color:var(--orange);">${planner.load.high_intensity_days}</div></div>
      <div class="card"><div class="kpi-label">Planned Volume</div><div class="kpi-value" style="color:var(--cyan);">${planner.load.total_planned_minutes}m</div></div>
    </div>

    ${
      planner.load.warnings.length
        ? `<div class="safety-box" style="margin-top:0.9rem;"><strong>Load Balance Warning:</strong> ${planner.load.warnings.map(esc).join(" ")}</div>`
        : ""
    }

    <div class="section-title">7-Day Schedule</div>
    ${posterGridHTML(planner.week)}

    <div class="grid-2" style="margin-top:1rem;">
      ${planner.week
        .filter((d) => !d.is_rest_day && d.routine_id)
        .map(
          (d) => `
          <div class="card" style="display:flex;justify-content:space-between;align-items:center;gap:0.8rem;">
            <div>
              <div style="font-size:0.75rem;color:#9ca3af;font-weight:700;text-transform:uppercase;">${esc(d.day_name)} · ${esc(d.date)}</div>
              <div style="font-weight:700;margin:0.2rem 0;">${esc(d.routine_title)}</div>
              <div style="font-size:0.78rem;color:#a1a1aa;">${esc(d.intensity)} · ~${d.estimated_duration_min} min · Status: <strong>${esc(d.status)}</strong></div>
            </div>
            ${
              d.status !== "completed"
                ? `<button class="btn btn-primary btn-sm mark-done-btn" data-sid="${d.schedule_id}" data-rid="${d.routine_id}" data-title="${esc(d.routine_title)}" data-dur="${d.estimated_duration_min}">✅ Done</button>`
                : `<span class="pill pill-green">✓ Logged</span>`
            }
          </div>
        `
        )
        .join("")}
    </div>

    <div class="section-title">Completed Workout History (${history.logs.length})</div>
    <div style="display:flex;flex-direction:column;gap:0.75rem;">
      ${
        history.logs.length
          ? history.logs
              .map(
                (l) => `
                <div class="card" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.6rem;">
                  <div>
                    <div style="font-weight:700;font-size:0.98rem;">${esc(l.routine_title)}</div>
                    <div style="font-size:0.8rem;color:#a1a1aa;">${new Date(l.completed_at).toLocaleDateString()} · ${l.actual_duration_min} min · Completion ${l.completion_percentage}%${l.perceived_effort_rpe ? ` · RPE ${l.perceived_effort_rpe}/10` : ""}</div>
                    ${l.notes ? `<div style="font-size:0.8rem;color:#d4d4d8;margin-top:0.2rem;"><em>${esc(l.notes)}</em></div>` : ""}
                  </div>
                  <span class="pill pill-green">${Math.round(l.completion_percentage)}%</span>
                </div>
              `
              )
              .join("")
          : `<div class="card">No logged workouts yet.</div>`
      }
    </div>
  `;

  document.getElementById("auto-week-btn").addEventListener("click", async () => {
    await api(`/api/planner/${state.user.id}/auto`, { method: "POST" });
    showToast("Generated a balanced 7-day plan with rest days!");
    renderPlanner();
  });

  root.querySelectorAll(".mark-done-btn").forEach((btn) =>
    btn.addEventListener("click", async () => {
      await api(`/api/history/${state.user.id}/log`, {
        method: "POST",
        body: JSON.stringify({
          schedule_id: Number(btn.dataset.sid),
          routine_id: Number(btn.dataset.rid),
          routine_title: btn.dataset.title,
          actual_duration_min: Number(btn.dataset.dur) || 20,
          completion_percentage: 100,
          perceived_effort_rpe: 6,
          exercises_completed: [],
          notes: "Completed from Weekly Training Planner.",
        }),
      });
      showToast("Session marked complete & logged!");
      renderPlanner();
    })
  );
}

async function renderAnalytics() {
  const root = document.getElementById("app-view");
  if (!state.user) {
    root.innerHTML = `<div class="card">Sign in or load the Demo Athlete under <strong>Profile &amp; Sign In</strong> to view Plotly progress charts.</div>`;
    return;
  }

  const s = await api(`/api/analytics/${state.user.id}`);
  root.innerHTML = `
    <section class="hero">
      <span class="pill pill-cyan">Interactive Plotly Activity Telemetry</span>
      <h1>Progress Dashboard</h1>
      <p>Tracks logged workout attendance, duration, completion rates, and exercise frequency. <em>Note: Workout completion measures activity consistency and does not alone prove physiological changes in strength, flexibility, or cardiovascular health.</em></p>
    </section>

    <div class="grid-4" style="margin-bottom:1.1rem;">
      <div class="card"><div class="kpi-label">Total Workouts</div><div class="kpi-value">${s.total_workouts}</div></div>
      <div class="card"><div class="kpi-label">Last 7 Days</div><div class="kpi-value" style="color:var(--green);">${s.workouts_last_7_days} / ${s.weekly_target_frequency}</div></div>
      <div class="card"><div class="kpi-label">Total Duration</div><div class="kpi-value" style="color:var(--cyan);">${s.total_minutes}m</div><div class="kpi-sub">${s.total_hours} hours</div></div>
      <div class="card"><div class="kpi-label">Avg Completion</div><div class="kpi-value" style="color:var(--orange);">${s.avg_completion_pct}%</div></div>
    </div>

    <div class="grid-2">
      <div class="chart-card" id="chart-weekly"></div>
      <div class="chart-card" id="chart-daily"></div>
      <div class="chart-card" id="chart-top"></div>
      <div class="chart-card" id="chart-cat"></div>
    </div>
  `;

  if (typeof Plotly === "undefined") return;

  const baseLayout = {
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(9,9,11,0.65)",
    font: { color: "#fafafa", family: "Inter, sans-serif" },
    margin: { l: 42, r: 30, t: 44, b: 38 },
  };

  Plotly.newPlot(
    "chart-weekly",
    [
      { x: s.weekly_series.map((w) => w.week), y: s.weekly_series.map((w) => w.total_minutes), type: "bar", name: "Minutes", marker: { color: "#fc4c02" } },
      { x: s.weekly_series.map((w) => w.week), y: s.weekly_series.map((w) => w.workouts), type: "scatter", mode: "lines+markers", name: "Sessions", yaxis: "y2", line: { color: "#00e676", width: 3 } },
    ],
    { ...baseLayout, title: "Weekly Training Minutes & Sessions", yaxis: { title: "Minutes", gridcolor: "rgba(255,255,255,0.08)" }, yaxis2: { title: "Sessions", overlaying: "y", side: "right", showgrid: false } },
    { responsive: true, displayModeBar: false }
  );

  Plotly.newPlot(
    "chart-daily",
    [{ x: s.daily_series.map((d) => d.date), y: s.daily_series.map((d) => d.total_minutes), type: "scatter", fill: "tozeroy", mode: "lines+markers", line: { color: "#00d4ff", width: 3 }, fillcolor: "rgba(0,212,255,0.16)" }],
    { ...baseLayout, title: "Daily Training Volume (Minutes)", yaxis: { title: "Minutes", gridcolor: "rgba(255,255,255,0.08)" } },
    { responsive: true, displayModeBar: false }
  );

  const topRev = [...s.top_exercises].reverse();
  Plotly.newPlot(
    "chart-top",
    [{ y: topRev.map((x) => x.Exercise), x: topRev.map((x) => x["Times Completed"]), type: "bar", orientation: "h", marker: { color: "#fc4c02" } }],
    { ...baseLayout, title: "Most Frequently Performed Exercises", margin: { l: 170, r: 20, t: 44, b: 36 } },
    { responsive: true, displayModeBar: false }
  );

  Plotly.newPlot(
    "chart-cat",
    [{ labels: s.categories.map((c) => c.Category), values: s.categories.map((c) => c["Exercises Completed"]), type: "pie", hole: 0.56, marker: { colors: ["#fc4c02", "#00e676", "#00d4ff", "#ffb020", "#a855f7", "#ff3b30"] } }],
    { ...baseLayout, title: "Training Category Balance" },
    { responsive: true, displayModeBar: false }
  );
}

function renderProfile() {
  const root = document.getElementById("app-view");
  const p = state.profile || { full_name: state.user?.full_name || "", age: 23, primary_sport: "Football", experience_level: "Intermediate", primary_goal: "Improve mobility", weekly_frequency: 4, available_duration_min: 25, preferred_intensity: "Moderate", available_equipment: [], physical_restrictions: "" };

  root.innerHTML = `
    <section class="hero">
      <span class="pill pill-orange">Athlete Onboarding &amp; Account</span>
      <h1>Athlete Profile &amp; Sign In</h1>
      <p>Update your sport, experience level, goals, equipment, and movement safety restrictions—or register a brand-new account.</p>
    </section>

    <div class="grid-2" style="margin-bottom:1.1rem;">
      <div class="card">
        <div class="kpi-label">Quick Demo Access</div>
        <p style="font-size:0.85rem;color:#a1a1aa;margin:0.4rem 0 0.85rem;">Load the pre-populated Football Intermediate demo athlete with ML ratings, weekly schedule, and Plotly workout history.</p>
        <button class="btn btn-primary" id="btn-load-demo">⚡ Load Portfolio Demo Athlete</button>
      </div>
      <div class="card">
        <div class="kpi-label">Create New Account</div>
        <div class="form-grid" style="margin-top:0.5rem;">
          <div class="field"><label>Full Name</label><input id="reg-name" placeholder="Priya Nair" /></div>
          <div class="field"><label>Email</label><input id="reg-email" placeholder="priya@example.com" /></div>
          <div class="field"><label>Password (8+ chars)</label><input id="reg-pw" type="password" /></div>
        </div>
        <button class="btn btn-secondary btn-sm" id="btn-register">Create Account</button>
      </div>
    </div>

    ${
      state.user
        ? `<div class="card">
             <div class="kpi-label" style="margin-bottom:0.8rem;">Edit Active Athlete Profile (${esc(state.user.email)})</div>
             <form id="prof-form">
               <div class="form-grid">
                 <div class="field"><label>Name</label><input id="p-name" value="${esc(p.full_name)}" /></div>
                 <div class="field"><label>Age</label><input id="p-age" type="number" min="10" max="110" value="${p.age || 23}" /></div>
                 <div class="field"><label>Primary Sport</label><select id="p-sport">${state.meta.sports.map((s) => `<option ${p.primary_sport === s ? "selected" : ""}>${esc(s)}</option>`).join("")}</select></div>
                 <div class="field"><label>Experience Level</label><select id="p-exp">${state.meta.levels.map((l) => `<option ${p.experience_level === l ? "selected" : ""}>${esc(l)}</option>`).join("")}</select></div>
                 <div class="field"><label>Primary Goal</label><select id="p-goal">${state.meta.goals.map((g) => `<option ${p.primary_goal === g ? "selected" : ""}>${esc(g)}</option>`).join("")}</select></div>
                 <div class="field"><label>Preferred Intensity</label><select id="p-int">${state.meta.intensities.map((i) => `<option ${p.preferred_intensity === i ? "selected" : ""}>${esc(i)}</option>`).join("")}</select></div>
                 <div class="field"><label>Weekly Frequency (1-7)</label><input id="p-freq" type="number" min="1" max="7" value="${p.weekly_frequency || 4}" /></div>
                 <div class="field"><label>Session Duration (min)</label><input id="p-dur" type="number" min="5" max="180" value="${p.available_duration_min || 25}" /></div>
               </div>
               <div class="field" style="margin-bottom:0.9rem;">
                 <label>Available Equipment</label>
                 <div class="chip-row" style="margin-top:0.3rem;">
                   ${state.meta.equipment
                     .map(
                       (eq) => `<label class="chip" style="cursor:pointer;"><input type="checkbox" class="p-eq" value="${esc(eq)}" ${(p.available_equipment || []).includes(eq) ? "checked" : ""} /> ${esc(eq)}</label>`
                     )
                     .join("")}
                 </div>
               </div>
               <div class="field" style="margin-bottom:1rem;">
                 <label>Movement Restrictions to Avoid (Safety Filter)</label>
                 <div class="chip-row" style="margin-top:0.3rem;">
                   ${Object.entries(state.meta.restrictions)
                     .map(
                       ([lbl, tag]) => `<label class="chip" style="cursor:pointer;"><input type="checkbox" class="p-rest" value="${esc(tag)}" ${(p.physical_restrictions || "").includes(tag) ? "checked" : ""} /> ${esc(lbl)}</label>`
                     )
                     .join("")}
                 </div>
               </div>
               <button class="btn btn-primary" type="submit">Save Athlete Profile</button>
             </form>
           </div>`
        : ""
    }
  `;

  document.getElementById("btn-load-demo").addEventListener("click", async () => {
    const res = await api("/api/auth/demo", { method: "POST" });
    state.user = res.user;
    state.profile = res.profile;
    updateUserBadge();
    showToast("Loaded Portfolio Demo Athlete!");
    renderProfile();
  });

  document.getElementById("btn-register").addEventListener("click", async () => {
    try {
      const res = await api("/api/auth/register", {
        method: "POST",
        body: JSON.stringify({
          full_name: document.getElementById("reg-name").value,
          email: document.getElementById("reg-email").value,
          password: document.getElementById("reg-pw").value,
        }),
      });
      state.user = res.user;
      state.profile = null;
      updateUserBadge();
      showToast("Account created! Complete your profile below.");
      renderProfile();
    } catch (err) {
      showToast(err.message);
    }
  });

  document.getElementById("prof-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const equip = [...document.querySelectorAll(".p-eq:checked")].map((x) => x.value);
    const rest = [...document.querySelectorAll(".p-rest:checked")].map((x) => x.value).join(",");
    const res = await api(`/api/profile/${state.user.id}`, {
      method: "POST",
      body: JSON.stringify({
        full_name: document.getElementById("p-name").value,
        age: Number(document.getElementById("p-age").value),
        primary_sport: document.getElementById("p-sport").value,
        experience_level: document.getElementById("p-exp").value,
        primary_goal: document.getElementById("p-goal").value,
        preferred_intensity: document.getElementById("p-int").value,
        weekly_frequency: Number(document.getElementById("p-freq").value),
        available_duration_min: Number(document.getElementById("p-dur").value),
        available_equipment: equip,
        physical_restrictions: rest,
      }),
    });
    state.profile = res.profile;
    state.generatedRoutine = null;
    updateUserBadge();
    showToast("Profile updated — AI recommendations adapted!");
  });
}

/* ==================== ROUTER & BOOTSTRAP ==================== */

function switchView(view) {
  state.activeView = view;
  document.querySelectorAll(".nav-btn").forEach((b) => b.classList.toggle("active", b.dataset.view === view));
  document.getElementById("sidebar").classList.remove("open");

  const map = {
    dashboard: renderDashboard,
    library: renderLibrary,
    recommendations: () => renderRecommendations(),
    generator: renderGenerator,
    plans: () => renderPlans(),
    sports: () => renderSports(),
    assistant: renderAssistant,
    planner: renderPlanner,
    analytics: renderAnalytics,
    profile: renderProfile,
  };
  (map[view] || renderDashboard)();
}

async function boot() {
  document.querySelectorAll(".nav-btn").forEach((b) => b.addEventListener("click", () => switchView(b.dataset.view)));
  document.querySelectorAll("[data-jump]").forEach((b) => b.addEventListener("click", () => switchView(b.dataset.jump)));
  document.getElementById("menu-toggle").addEventListener("click", () => document.getElementById("sidebar").classList.toggle("open"));

  try {
    const [meta, demo] = await Promise.all([api("/api/meta"), api("/api/auth/demo", { method: "POST" })]);
    state.meta = meta;
    state.user = demo.user;
    state.profile = demo.profile;
    updateUserBadge();
    switchView("dashboard");
  } catch (err) {
    document.getElementById("app-view").innerHTML = `<div class="card">Startup error: ${esc(err.message)}</div>`;
  }
}

boot();
