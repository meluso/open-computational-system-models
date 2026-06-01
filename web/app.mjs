// Browser glue: reads the generated catalog data, wires up the controls, and
// renders entry cards. All non-trivial logic lives in catalog-logic.mjs so it
// can be tested headlessly.
import { CATALOG, DOMAINS, META } from "./catalog-data.mjs";
import { queryCatalog } from "./catalog-logic.mjs";

const DOMAIN_NAME = Object.fromEntries(DOMAINS.map((d) => [d.slug, d.name]));
const DOMAIN_BLURB = Object.fromEntries(DOMAINS.map((d) => [d.slug, d.blurb]));

const ACCESS_LABELS = {
  "permissive-open": "Permissive open source",
  "weak-copyleft-open": "Weak-copyleft open source",
  "copyleft-open": "Copyleft open source",
  "free-closed": "Free, closed source",
  freemium: "Freemium",
  commercial: "Commercial",
  "campus-or-employer-licensed": "Campus / employer licensed",
};

// Plain-language meaning for each access type, shown on hover so a reader from
// any field can understand the licensing jargon. Mirrors the legend in index.html.
const ACCESS_HELP = {
  "permissive-open": "Free and open; use, modify, and share with few conditions (e.g. MIT, BSD, Apache).",
  "weak-copyleft-open": "Free and open; changes to the tool's own files stay open, but you may combine it with closed code (e.g. LGPL, MPL).",
  "copyleft-open": "Free and open, but anything you distribute that builds on it must also be released under the same open license (e.g. GPL).",
  "free-closed": "Free to use, but the source code is not published.",
  freemium: "A free tier exists; full capability needs a paid plan.",
  commercial: "A paid product or license.",
  "campus-or-employer-licensed": "Reached through a university or workplace license (e.g. MATLAB/Simulink), not free to the public.",
};

const STATUS_LABELS = {
  active: "Active",
  maintained: "Maintained",
  dormant: "Dormant",
  abandoned: "Abandoned",
  unknown: "Unknown",
};

const STATUS_HELP = {
  active: "Under ongoing development.",
  maintained: "Kept working with fixes and updates, even if not adding much.",
  dormant: "No recent activity, but still usable.",
  abandoned: "No longer maintained.",
  unknown: "Maintenance status could not be determined.",
};

const CONF_HELP =
  "How sure we are this entry's recorded facts (version, license, scale, …) are correct, based on how directly we could confirm them from primary sources.";

// Plain-language help for field labels that lean on the catalog's own concepts.
const FIELD_HELP = {
  scale:
    "Roughly how many interacting elements the model has, and how they group into subsystems. The catalog focuses on models with many interacting parts (about 25 or more).",
  why:
    "Every entry must be runnable: you can change inputs or parameters and observe different outputs. This says how that works for this tool.",
};

const UNSTATED_HELP =
  "The source did not state this fact, so it was left unstated rather than guessed.";

const state = { query: "", domain: "", accessType: "", sortKey: "maintenance-desc" };

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k === "text") node.textContent = v;
    else if (k === "html") node.innerHTML = v;
    else node.setAttribute(k, v);
  }
  for (const c of [].concat(children)) {
    if (c == null) continue;
    node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
  }
  return node;
}

function field(label, value, help) {
  if (value == null || value === "") return null;
  const labelAttrs = { class: "field-label", text: label };
  if (help) labelAttrs.title = help;
  return el("div", { class: "field" }, [
    el("span", labelAttrs),
    el("span", { class: "field-value" }, [value]),
  ]);
}

// A span whose text may be the "unstated — needs direct verification" sentinel,
// styled and explained on hover when so.
function valueSpan(value) {
  const cls = unstatedClass(value);
  const attrs = {};
  if (cls) {
    attrs.class = cls;
    attrs.title = UNSTATED_HELP;
  }
  return el("span", attrs, [value]);
}

function list(items) {
  const ul = el("ul", { class: "chips" });
  for (const it of items || []) ul.appendChild(el("li", { text: it }));
  return ul;
}

function unstatedClass(value) {
  return typeof value === "string" && value.includes("unstated") ? "unstated" : "";
}

function card(entry) {
  const ms = entry.maintenance_status || {};
  const scale = entry.scale || {};
  const vc = entry.verification_confidence || {};
  const head = el("div", { class: "card-head" }, [
    el("h2", { class: "card-title" }, [
      el("a", { href: entry.access_link, target: "_blank", rel: "noopener", text: entry.name }),
    ]),
    el("div", { class: "badges" }, [
      el("span", { class: "badge domain", title: DOMAIN_BLURB[entry.domain] || "", text: DOMAIN_NAME[entry.domain] || entry.domain }),
      el("span", { class: "badge access", title: ACCESS_HELP[entry.access_type] || "How you obtain and may use the tool.", text: ACCESS_LABELS[entry.access_type] || entry.access_type }),
      el("span", { class: `badge status status-${ms.status || "unknown"}`, title: STATUS_HELP[ms.status] || STATUS_HELP.unknown, text: STATUS_LABELS[ms.status] || "Unknown" }),
      el("span", { class: `badge conf conf-${vc.overall || "low"}`, title: CONF_HELP, text: `confidence: ${vc.overall || "?"}` }),
    ]),
  ]);

  const body = el("div", { class: "card-body" }, [
    el("p", { class: "gloss", text: entry.gloss }),
    field("System represented", el("span", { text: entry.system_represented })),
    field("Inputs you can change", list(entry.inputs_you_can_change)),
    field("Outputs you can observe", list(entry.outputs_you_can_observe)),
    field("Runtime required", el("span", { text: entry.runtime_required })),
    field("License", valueSpan(entry.license)),
    field(
      "Model scale",
      el("span", { class: unstatedClass(scale.element_count), title: unstatedClass(scale.element_count) ? UNSTATED_HELP : "" }, [
        `${scale.element_count}${scale.grouping ? " — " + scale.grouping : ""}`,
      ]),
      FIELD_HELP.scale
    ),
    field(
      "Maintenance",
      el("span", {}, [
        `${STATUS_LABELS[ms.status] || "Unknown"}` +
          (ms.latest_version ? ` · ${ms.latest_version}` : "") +
          (ms.latest_release_date ? ` · ${ms.latest_release_date}` : ""),
      ])
    ),
    field("Suitability", el("span", { text: entry.suitability })),
    field("Why it's in this catalog", el("span", { text: entry.executability_justification }), FIELD_HELP.why),
  ]);

  const foot = el("div", { class: "card-foot" }, [
    el("span", { class: "verified", text: `Last verified ${entry.last_verified}` }),
    (vc.unverified && vc.unverified.length
      ? el("span", { class: "unverified-note", text: `Unverified: ${vc.unverified.join(", ")}` })
      : null),
  ]);

  return el("article", { class: "card", id: `entry-${entry.id}` }, [head, body, foot]);
}

function render() {
  const results = queryCatalog(CATALOG, state);
  const grid = document.getElementById("results");
  grid.innerHTML = "";
  for (const e of results) grid.appendChild(card(e));
  document.getElementById("result-count").textContent =
    `${results.length} of ${CATALOG.length} models`;
}

function populateSelect(id, options, allLabel) {
  const sel = document.getElementById(id);
  sel.appendChild(el("option", { value: "", text: allLabel }));
  for (const [value, label] of options) sel.appendChild(el("option", { value, text: label }));
}

function init() {
  document.getElementById("meta-line").textContent =
    `${CATALOG.length} models · ${DOMAINS.filter((d) => CATALOG.some((e) => e.domain === d.slug)).length} domains · built ${META.built}`;

  // Domain filter ordered as in the registry, only those with entries.
  const domainOpts = DOMAINS.filter((d) => CATALOG.some((e) => e.domain === d.slug)).map(
    (d) => [d.slug, d.name]
  );
  populateSelect("domain-filter", domainOpts, "All domains");

  const accessPresent = [...new Set(CATALOG.map((e) => e.access_type))];
  const accessOpts = Object.entries(ACCESS_LABELS).filter(([k]) => accessPresent.includes(k));
  populateSelect("access-filter", accessOpts, "All access types");

  const q = document.getElementById("search");
  q.addEventListener("input", () => {
    state.query = q.value;
    render();
  });
  document.getElementById("domain-filter").addEventListener("change", (e) => {
    state.domain = e.target.value;
    render();
  });
  document.getElementById("access-filter").addEventListener("change", (e) => {
    state.accessType = e.target.value;
    render();
  });
  document.getElementById("sort").addEventListener("change", (e) => {
    state.sortKey = e.target.value;
    render();
  });
  document.getElementById("reset").addEventListener("click", () => {
    state.query = state.domain = state.accessType = "";
    state.sortKey = "maintenance-desc";
    q.value = "";
    document.getElementById("domain-filter").value = "";
    document.getElementById("access-filter").value = "";
    document.getElementById("sort").value = "maintenance-desc";
    render();
  });

  render();
}

document.addEventListener("DOMContentLoaded", init);
