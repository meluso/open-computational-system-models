// Headless test of the website's search / filter / sort logic. Imports the very
// same module the browser uses (web/catalog-logic.mjs), so a pass here means the
// real site behaviour is exercised without a browser.
//
// Run: node tests/test_site_logic.mjs

import {
  filterEntries,
  sortEntries,
  queryCatalog,
  maintenanceSortValue,
} from "../web/catalog-logic.mjs";

let passed = 0;
let failed = 0;
function check(name, cond) {
  if (cond) {
    passed++;
  } else {
    failed++;
    console.error(`  FAIL: ${name}`);
  }
}

const sample = [
  {
    id: "alpha",
    name: "Alpha Solver",
    gloss: "solves alpha things",
    domain: "mdo",
    system_represented: "an aircraft",
    inputs_you_can_change: ["wing span", "cruise altitude"],
    outputs_you_can_observe: ["range", "fuel burn"],
    runtime_required: "Python",
    license: "Apache-2.0",
    access_type: "permissive-open",
    tags: ["aircraft"],
    maintenance_status: { status: "active", latest_release_date: "2025-03-01" },
  },
  {
    id: "bravo",
    name: "Bravo Sim",
    gloss: "simulates bravo grids",
    domain: "power-energy",
    system_represented: "a distribution grid",
    inputs_you_can_change: ["load profile"],
    outputs_you_can_observe: ["voltage"],
    runtime_required: "Python",
    license: "GPL-3.0",
    access_type: "copyleft-open",
    tags: [],
    maintenance_status: { status: "maintained", latest_release_date: "2024-01-15" },
  },
  {
    id: "charlie",
    name: "Charlie Suite",
    gloss: "commercial multiphysics",
    domain: "equation-based-physical",
    system_represented: "a powertrain",
    inputs_you_can_change: ["gear ratio"],
    outputs_you_can_observe: ["torque"],
    runtime_required: "Windows",
    license: "Proprietary",
    access_type: "commercial",
    tags: [],
    maintenance_status: { status: "active", latest_release_date: "2026-01-10" },
  },
];

// --- filter: domain ---
check("filter by domain", filterEntries(sample, { domain: "mdo" }).length === 1);
check(
  "filter by domain returns the right one",
  filterEntries(sample, { domain: "mdo" })[0].id === "alpha"
);

// --- filter: access type ---
check(
  "filter by access type",
  filterEntries(sample, { accessType: "copyleft-open" }).length === 1
);

// --- filter: query across fields ---
check("query matches name", filterEntries(sample, { query: "bravo" }).length === 1);
check(
  "query matches an input field",
  filterEntries(sample, { query: "wing span" })[0].id === "alpha"
);
check(
  "query matches an output field",
  filterEntries(sample, { query: "voltage" })[0].id === "bravo"
);
check(
  "multi-term query is AND",
  filterEntries(sample, { query: "aircraft range" }).length === 1
);
check(
  "multi-term query AND excludes partial",
  filterEntries(sample, { query: "aircraft voltage" }).length === 0
);
check("empty query returns all", filterEntries(sample, { query: "" }).length === 3);
check("query is case-insensitive", filterEntries(sample, { query: "ALPHA" }).length === 1);

// --- combined filters ---
check(
  "combined domain + access",
  filterEntries(sample, { domain: "power-energy", accessType: "copyleft-open" }).length === 1
);
check(
  "combined filters can exclude all",
  filterEntries(sample, { domain: "mdo", accessType: "commercial" }).length === 0
);

// --- sort: maintenance recency ---
const byRecency = sortEntries(sample, "maintenance-desc");
check("sort maintenance-desc newest first", byRecency[0].id === "charlie");
check("sort maintenance-desc oldest last", byRecency[byRecency.length - 1].id === "bravo");
const byRecencyAsc = sortEntries(sample, "maintenance-asc");
check("sort maintenance-asc oldest first", byRecencyAsc[0].id === "bravo");

// --- sort: name ---
check("sort name-asc", sortEntries(sample, "name-asc")[0].id === "alpha");
check("sort name-desc", sortEntries(sample, "name-desc")[0].id === "charlie");

// --- sort does not mutate input ---
const before = sample.map((e) => e.id).join(",");
sortEntries(sample, "name-desc");
check("sort is non-mutating", sample.map((e) => e.id).join(",") === before);

// --- maintenanceSortValue handles missing dates ---
check(
  "missing date yields zero dateScore",
  maintenanceSortValue({ maintenance_status: { status: "active" } }).dateScore === 0
);
check(
  "status still ranks when dates tie",
  maintenanceSortValue({ maintenance_status: { status: "active" } }).statusScore >
    maintenanceSortValue({ maintenance_status: { status: "dormant" } }).statusScore
);

// --- queryCatalog end to end ---
const e2e = queryCatalog(sample, { query: "python", sortKey: "maintenance-desc" });
check("queryCatalog filters then sorts", e2e.length === 2 && e2e[0].id === "alpha");

console.log(`\nsite logic: ${passed} passed, ${failed} failed`);
process.exit(failed === 0 ? 0 : 1);
