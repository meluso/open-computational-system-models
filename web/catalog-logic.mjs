// Pure, dependency-free catalog logic shared by the browser app (app.mjs) and
// the headless Node test (tests/test_site_logic.mjs). No DOM access here, so the
// search / filter / sort behaviour can be tested without a browser.

// Rank maintenance recency for sorting. Higher = more recent / more active.
// Falls back to status when no parseable date is present.
const STATUS_RANK = {
  active: 4,
  maintained: 3,
  dormant: 2,
  abandoned: 1,
  unknown: 0,
};

export function maintenanceSortValue(entry) {
  const ms = entry.maintenance_status || {};
  const dateStr = ms.latest_release_date || "";
  // Pull a leading 4-digit year if present (handles "2025-03-01" and "2025").
  const m = /(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?/.exec(String(dateStr));
  let dateScore = 0;
  if (m) {
    const year = parseInt(m[1], 10);
    const month = m[2] ? parseInt(m[2], 10) : 1;
    const day = m[3] ? parseInt(m[3], 10) : 1;
    // Encode as a sortable integer YYYYMMDD.
    dateScore = year * 10000 + month * 100 + day;
  }
  const statusScore = STATUS_RANK[ms.status] ?? 0;
  return { dateScore, statusScore };
}

function matchesQuery(entry, query) {
  if (!query) return true;
  const q = query.trim().toLowerCase();
  if (!q) return true;
  const haystack = [
    entry.name,
    entry.gloss,
    entry.system_represented,
    entry.suitability,
    entry.runtime_required,
    entry.license,
    (entry.inputs_you_can_change || []).join(" "),
    (entry.outputs_you_can_observe || []).join(" "),
    (entry.tags || []).join(" "),
  ]
    .filter(Boolean)
    .join("  ")
    .toLowerCase();
  // All whitespace-separated terms must be present (AND search).
  return q.split(/\s+/).every((term) => haystack.includes(term));
}

export function filterEntries(entries, { query = "", domain = "", accessType = "" } = {}) {
  return entries.filter((e) => {
    if (domain && e.domain !== domain) return false;
    if (accessType && e.access_type !== accessType) return false;
    if (!matchesQuery(e, query)) return false;
    return true;
  });
}

export function sortEntries(entries, sortKey = "maintenance-desc") {
  const copy = entries.slice();
  switch (sortKey) {
    case "maintenance-desc":
    case "maintenance-asc": {
      const dir = sortKey === "maintenance-desc" ? -1 : 1;
      copy.sort((a, b) => {
        const va = maintenanceSortValue(a);
        const vb = maintenanceSortValue(b);
        if (va.dateScore !== vb.dateScore) return dir * (va.dateScore - vb.dateScore);
        if (va.statusScore !== vb.statusScore) return dir * (va.statusScore - vb.statusScore);
        return a.name.localeCompare(b.name);
      });
      break;
    }
    case "name-asc":
      copy.sort((a, b) => a.name.localeCompare(b.name));
      break;
    case "name-desc":
      copy.sort((a, b) => b.name.localeCompare(a.name));
      break;
    case "domain":
      copy.sort(
        (a, b) => a.domain.localeCompare(b.domain) || a.name.localeCompare(b.name)
      );
      break;
    default:
      break;
  }
  return copy;
}

// Convenience: apply filter then sort in one call (used by the app).
export function queryCatalog(entries, opts = {}) {
  const { sortKey = "maintenance-desc", ...filterOpts } = opts;
  return sortEntries(filterEntries(entries, filterOpts), sortKey);
}
