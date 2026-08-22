(function (global, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  global.MatrixSearchRelevance = api;
}(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  function normalize(value) {
    var text = String(value == null ? "" : value);
    if (text.normalize) text = text.normalize("NFKD").replace(/[\u0300-\u036f]/g, "");
    return text.toLowerCase().replace(/&/g, " and ").replace(/\+/g, " ").replace(/[^a-z0-9]+/g, " ").trim().replace(/\s+/g, " ");
  }

  function compact(value) {
    return normalize(value).replace(/\s+/g, "");
  }

  function list(value) {
    if (Array.isArray(value)) return value;
    return value == null ? [] : [value];
  }

  function normalizedList(value) {
    return list(value).map(normalize).filter(Boolean);
  }

  function allTermsIn(text, terms) {
    return terms.length > 0 && terms.every(function (term) { return text.indexOf(term) >= 0; });
  }

  function allWholeTermsIn(text, terms) {
    var padded = " " + text + " ";
    return terms.length > 0 && terms.every(function (term) { return padded.indexOf(" " + term + " ") >= 0; });
  }

  function score(record, rawQuery) {
    var query = normalize(rawQuery);
    if (!query) return { matched: false, score: 0, reason: "empty-query" };
    var queryCompact = compact(query);
    var terms = query.split(" ").filter(Boolean);
    var title = normalize(record.title);
    var aliases = normalizedList(record.searchAliases || record.aliases);
    var verifiedTerms = normalizedList(record.searchTerms)
      .concat(normalizedList(record.topicIds))
      .concat(normalizedList(record.verifiedIngredients || record.ingredients));
    var titleAndManufacturer = normalize([record.manufacturer, record.title].join(" "));
    var category = normalize([record.category, record.intent, record.department, record.productKind, record.type, record.searchGroup].join(" "));
    var summary = normalize([record.summary, record.description].join(" "));
    var broader = normalize([
      record.publisher, record.resourceType, record.evidenceRole, record.independence,
      list(record.keywords).join(" "), list(record.terms).join(" "),
      list(record.topics).join(" "), list(record.products).join(" "), list(record.intents).join(" ")
    ].join(" "));
    var base = 0;
    var reason = "";

    function consider(value, label) {
      if (value > base) { base = value; reason = label; }
    }

    if (title === query) consider(1300, "exact-title");
    if (compact(title) === queryCompact) consider(1260, "exact-title-compact");
    if (title.indexOf(query) === 0) consider(1050, "title-prefix");
    if (allWholeTermsIn(title, terms)) consider(920, "all-title-terms");
    aliases.forEach(function (alias) {
      if (alias === query || compact(alias) === queryCompact) consider(900, "exact-alias");
      else if (alias.indexOf(query) === 0) consider(820, "alias-prefix");
      else if (allTermsIn(alias, terms)) consider(780, "alias-terms");
    });
    if (allWholeTermsIn(title, terms)) consider(760 + Math.min(terms.length, 5) * 8, "whole-word-title");
    if (verifiedTerms.some(function (value) { return value === query || compact(value) === queryCompact; })) consider(700, "verified-term-exact");
    if (verifiedTerms.some(function (value) { return allTermsIn(value, terms); })) consider(640, "verified-term");
    if (allTermsIn(titleAndManufacturer, terms)) consider(520, "manufacturer-title");
    if (allTermsIn(category, terms)) consider(360, "category-intent-kind");
    if (allTermsIn(summary, terms)) consider(230, "summary");
    if (allTermsIn(broader, terms)) consider(120, "broader-metadata");

    if (!base) return { matched: false, score: 0, reason: "no-match" };
    var priority = Number(record.searchPriority || 0);
    if (!Number.isFinite(priority)) priority = 0;
    return { matched: true, score: base + priority, baseScore: base, priority: priority, reason: reason };
  }

  function rank(records, query) {
    var seen = {};
    return records.map(function (record, index) {
      var result = score(record, query);
      return { record: record, result: result, canonicalOrder: Number.isFinite(Number(record.order)) ? Number(record.order) : index };
    }).filter(function (entry) {
      if (!entry.result.matched) return false;
      var key = String(entry.record.type || "record") + ":" + String(entry.record.id || entry.canonicalOrder);
      if (seen[key]) return false;
      seen[key] = true;
      return true;
    }).sort(function (left, right) {
      return right.result.score - left.result.score || left.canonicalOrder - right.canonicalOrder || String(left.record.id || "").localeCompare(String(right.record.id || ""));
    });
  }

  return { normalize: normalize, score: score, rank: rank };
}));
