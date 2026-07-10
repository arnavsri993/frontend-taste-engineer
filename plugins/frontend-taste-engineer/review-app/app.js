const state = { records: [], eval: null };
let renderTimer = null;

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
const text = (value) => String(value ?? "").trim();

const demoModes = {
  editorial: {
    context: "Editorial field journal",
    logo: "Field / Note",
    nav: "Issue 08 · High desert",
    eyebrow: "An observation in three parts",
    title: "The wind<br>edits first.",
    copy: "Long-form hierarchy. Quiet rhythm. Paper tactility.",
    action: "Read the note",
    feedback: "Note open. No external content loaded.",
    asideLabel: "Coordinates",
    asideValue: "34.611° N",
  },
  civic: {
    context: "High-trust public service",
    logo: "Northline Services",
    nav: "Permit desk · Step 3 of 5",
    eyebrow: "Your application is ready to review",
    title: "Check it once.<br>Send with confidence.",
    copy: "Plain language. Visible status. Predictable recovery.",
    action: "Review details",
    feedback: "Review open. No application data submitted.",
    asideLabel: "Current step",
    asideValue: "Review details",
  },
  developer: {
    context: "Focused developer tool",
    logo: "TRACE / LOCAL",
    nav: "session_04 · connected",
    eyebrow: "State, without the noise",
    title: "See what<br>changed.",
    copy: "Fast hierarchy. Precise data. Motion only for state.",
    action: "Inspect trace",
    feedback: "Trace open. No remote session contacted.",
    asideLabel: "Active branch",
    asideValue: "feature/render",
  },
};

function setDemoMode(mode) {
  const data = demoModes[mode];
  if (!data) return;
  const frame = $(".demo-frame");
  frame.dataset.demoMode = mode;
  $("#demo-context").textContent = data.context;
  $("#demo-logo").textContent = data.logo;
  $("#demo-nav-label").textContent = data.nav;
  $("#demo-eyebrow").textContent = data.eyebrow;
  $("#demo-title").innerHTML = data.title;
  $("#demo-copy").textContent = data.copy;
  $("#demo-action").firstChild.textContent = `${data.action} `;
  $("#demo-action").setAttribute("aria-expanded", "false");
  $("#demo-feedback").hidden = true;
  $("#demo-feedback").textContent = data.feedback;
  $("#demo-aside-label").textContent = data.asideLabel;
  $("#demo-aside-value").textContent = data.asideValue;
  $$(".mode-button").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.mode === mode));
  });
}

function normalizeRecords(payload) {
  const candidates = Array.isArray(payload)
    ? payload
    : payload?.records || payload?.items || payload?.entries || [];
  return candidates.map((item) => ({
    id: text(item.id || item.record_id),
    title: text(item.title || item.principle || item.id),
    topic: text(item.topic),
    subtopic: text(item.subtopic),
    importance: text(item.importance).toLowerCase(),
    principle: text(item.principle || item.summary),
    sources: Array.isArray(item.sources) ? item.sources.map(text) : [],
  })).filter((item) => item.id || item.title);
}

async function loadJson(paths) {
  for (const path of paths) {
    try {
      const response = await fetch(path, { cache: "no-store" });
      if (response.ok) return await response.json();
    } catch (_) {
      // Try the next documented location.
    }
  }
  return null;
}

async function loadSourceCount() {
  for (const path of ["./data/source-registry.yml", "../research/source-registry.yml"]) {
    try {
      const response = await fetch(path, { cache: "no-store" });
      if (!response.ok) continue;
      const registry = await response.text();
      const ids = registry.match(/^\s*-?\s*id:\s*[^\s#]+/gm) || [];
      return ids.length;
    } catch (_) {
      // Try the next documented location.
    }
  }
  return null;
}

async function loadCanonicalRecords(indexPayload) {
  const origins = [...new Set((indexPayload?.records || []).map((item) => item.origin).filter(Boolean))];
  const payloads = await Promise.all(origins.map((origin) => loadJson([
    `./data/${origin}`,
    `../knowledge/${origin}`,
  ])));
  const canonical = payloads.flatMap((payload) => Array.isArray(payload) ? payload : payload?.records || []);
  const merged = new Map((indexPayload?.records || []).map((item) => [item.id, item]));
  canonical.forEach((item) => merged.set(item.id, { ...merged.get(item.id), ...item }));
  return [...merged.values()];
}

function renderRecords() {
  const queryTerms = $("#query").value.trim().toLowerCase().split(/\s+/).filter(Boolean);
  const importance = $("#importance").value;
  const matches = state.records.filter((item) => {
    const haystack = [item.id, item.title, item.topic, item.subtopic, item.principle, ...item.sources].join(" ").toLowerCase();
    return queryTerms.every((term) => haystack.includes(term)) && (!importance || item.importance === importance);
  }).slice(0, 40);
  $("#result-summary").textContent = state.records.length
    ? `${matches.length} shown of ${state.records.length}`
    : "Index unavailable.";
  const list = $("#results-list");
  list.replaceChildren();
  if (!matches.length) {
    const empty = document.createElement("li");
    empty.className = "empty";
    empty.textContent = state.records.length ? "No matching rules." : "No local index loaded.";
    list.append(empty);
    return;
  }
  for (const item of matches) {
    const li = document.createElement("li");
    li.className = "record";
    const header = document.createElement("header");
    const title = document.createElement("h4");
    title.textContent = item.title;
    const meta = document.createElement("span");
    meta.className = `meta ${item.importance === "mandatory" ? "mandatory" : ""}`;
    meta.textContent = item.importance || item.topic || "record";
    header.append(title, meta);
    const id = document.createElement("p");
    id.className = "meta";
    id.textContent = [item.id, item.topic, item.subtopic].filter(Boolean).join(" · ");
    const principle = document.createElement("p");
    principle.textContent = item.principle || "Open the canonical record for implementation and verification details.";
    li.append(header, id, principle);
    list.append(li);
  }
}

function renderEval(payload) {
  const host = $("#eval-summary");
  host.replaceChildren();
  if (!payload) {
    host.append(Object.assign(document.createElement("p"), { textContent: "No eval summary." }));
    return 0;
  }
  const metrics = payload.metrics || payload.summary || payload;
  const entries = Object.entries(metrics).filter(([, value]) => ["string", "number", "boolean"].includes(typeof value)).slice(0, 8);
  const dl = document.createElement("dl");
  for (const [name, value] of entries) {
    const row = document.createElement("div");
    const dt = document.createElement("dt");
    const dd = document.createElement("dd");
    dt.textContent = name.replaceAll("_", " ");
    dd.textContent = String(value);
    row.append(dt, dd);
    dl.append(row);
  }
  host.append(entries.length ? dl : Object.assign(document.createElement("p"), { textContent: "No scalar metrics." }));
  return Number(payload.case_count || payload.cases?.length || metrics.case_count || 0);
}

async function copyInstallCommands() {
  const button = $("#copy-install");
  const status = $("#copy-status");
  const command = $("#install-command").innerText.trim();
  button.disabled = true;
  status.textContent = "Copying…";
  try {
    if (!navigator.clipboard?.writeText) throw new Error("Clipboard API unavailable");
    await Promise.race([
      navigator.clipboard.writeText(command),
      new Promise((_, reject) => window.setTimeout(() => reject(new Error("Clipboard timed out")), 900)),
    ]);
    button.textContent = "Copied";
    status.textContent = "Copied.";
  } catch (_) {
    button.textContent = "Copy commands";
    status.textContent = "Copy blocked. Select the commands manually.";
  } finally {
    button.disabled = false;
  }
}

function toggleDemoAction() {
  const button = $("#demo-action");
  const feedback = $("#demo-feedback");
  const opening = button.getAttribute("aria-expanded") !== "true";
  button.setAttribute("aria-expanded", String(opening));
  feedback.hidden = !opening;
}

async function init() {
  const [corpusMetadata, generatedIndex, sourceCount, retrievalEval, frontendEval] = await Promise.all([
    loadJson(["./data/index.json", "../knowledge/index.json"]),
    loadJson(["./data/knowledge-index.json", "../ingestion/knowledge-index.json", "../knowledge/index.generated.json"]),
    loadSourceCount(),
    loadJson(["./data/retrieval.json", "../evals/results/retrieval.json"]),
    loadJson(["./data/frontend.json", "../evals/results/frontend.json", "../audits/latest.json"]),
  ]);
  const hybrid = retrievalEval?.aggregates?.hybrid;
  const evalSummary = (retrievalEval || frontendEval) ? {
    case_count: frontendEval?.case_count || retrievalEval?.cases?.length || 0,
    metrics: {
      retrieval_passed: retrievalEval?.passed ?? "not loaded",
      hybrid_quality: hybrid?.quality_score ?? "not loaded",
      mandatory_recall: hybrid?.mandatory_rule_recall ?? "not loaded",
      provenance_correctness: hybrid?.provenance_correctness ?? "not loaded",
      frontend_evidence: frontendEval ? `${frontendEval.scored_cases}/${frontendEval.case_count} scored` : "not loaded",
    },
  } : null;
  state.records = normalizeRecords(await loadCanonicalRecords(generatedIndex));
  state.eval = evalSummary;
  $("#record-count").textContent = generatedIndex?.record_count || state.records.length || corpusMetadata?.record_count || "—";
  $("#source-count").textContent = sourceCount ?? "—";
  $("#eval-count").textContent = renderEval(evalSummary) || "—";
  $("#load-status").textContent = state.records.length || sourceCount || evalSummary
    ? "Local artifacts loaded"
    : "Artifacts unavailable. Demo remains usable.";
  renderRecords();
}

$$(".mode-button").forEach((button) => {
  button.addEventListener("click", () => setDemoMode(button.dataset.mode));
});
$("#query").addEventListener("input", () => {
  window.clearTimeout(renderTimer);
  renderTimer = window.setTimeout(renderRecords, 120);
});
$("#importance").addEventListener("change", renderRecords);
$("#copy-install").addEventListener("click", copyInstallCommands);
$("#demo-action").addEventListener("click", toggleDemoAction);
setDemoMode("editorial");
init();
