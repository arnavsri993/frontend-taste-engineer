const state = { records: [], eval: null };
let renderTimer = null;

const $ = (selector) => document.querySelector(selector);
const text = (value) => String(value ?? "").trim();

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
  try {
    const response = await fetch("/research/source-registry.yml", { cache: "no-store" });
    if (!response.ok) return null;
    const registry = await response.text();
    const ids = registry.match(/^\s*-?\s*id:\s*[^\s#]+/gm) || [];
    return ids.length;
  } catch (_) {
    return null;
  }
}

function renderRecords() {
  const query = $("#query").value.trim().toLowerCase();
  const importance = $("#importance").value;
  const matches = state.records.filter((item) => {
    const haystack = [item.id, item.title, item.topic, item.subtopic, item.principle, ...item.sources].join(" ").toLowerCase();
    return (!query || haystack.includes(query)) && (!importance || item.importance === importance);
  }).slice(0, 40);
  $("#result-summary").textContent = state.records.length
    ? `${matches.length} shown of ${state.records.length}`
    : "Index unavailable.";
  const list = $("#results-list");
  list.replaceChildren();
  if (!matches.length) {
    const empty = document.createElement("li");
    empty.className = "empty";
    empty.textContent = state.records.length ? "No records match this filter." : "No local knowledge index has been loaded.";
    list.append(empty);
    return;
  }
  for (const item of matches) {
    const li = document.createElement("li");
    li.className = "record";
    const header = document.createElement("header");
    const title = document.createElement("h3");
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
    host.append(Object.assign(document.createElement("p"), { textContent: "No evaluation summary loaded." }));
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
  host.append(entries.length ? dl : Object.assign(document.createElement("p"), { textContent: "Summary exists but contains no scalar release metrics." }));
  return Number(payload.case_count || payload.cases?.length || metrics.case_count || 0);
}

async function init() {
  const [corpusMetadata, generatedIndex, sourceCount, retrievalEval, frontendEval] = await Promise.all([
    loadJson(["/knowledge/index.json"]),
    loadJson(["/ingestion/knowledge-index.json", "/knowledge/index.generated.json"]),
    loadSourceCount(),
    loadJson(["/evals/results/retrieval.json"]),
    loadJson(["/evals/results/frontend.json", "/audits/latest.json"]),
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
  state.records = normalizeRecords(generatedIndex);
  state.eval = evalSummary;
  $("#record-count").textContent = (corpusMetadata?.record_count ?? generatedIndex?.record_count ?? state.records.length) || "—";
  $("#source-count").textContent = sourceCount ?? "—";
  $("#eval-count").textContent = renderEval(evalSummary) || "—";
  $("#load-status").textContent = state.records.length || sourceCount || evalSummary
    ? "Local artifacts loaded"
    : "No generated artifacts found";
  renderRecords();
}

$("#query").addEventListener("input", () => {
  window.clearTimeout(renderTimer);
  renderTimer = window.setTimeout(renderRecords, 120);
});
$("#importance").addEventListener("change", renderRecords);
init();
