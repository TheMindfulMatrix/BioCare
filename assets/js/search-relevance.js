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

  function specificityFor(text, terms) {
    var fieldTerms = normalize(text).split(" ").filter(Boolean);
    return terms.length * 1000 - Math.abs(fieldTerms.length - terms.length);
  }

  function score(record, rawQuery) {
    var query = normalize(rawQuery);
    if (!query) return { matched: false, matchTier: 0, specificity: 0, priority: 0, reason: "empty-query" };
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
    var matchTier = 0;
    var specificity = 0;
    var reason = "no-match";

    function consider(tier, label, matchedText) {
      var candidateSpecificity = specificityFor(matchedText, terms);
      if (tier > matchTier || (tier === matchTier && candidateSpecificity > specificity)) {
        matchTier = tier;
        specificity = candidateSpecificity;
        reason = label;
      }
    }

    if (title === query) consider(13, "exact-title", title);
    if (compact(title) === queryCompact) consider(12, "exact-title-compact", title);
    if (title.indexOf(query) === 0) consider(11, "title-prefix", title);
    if (allWholeTermsIn(title, terms)) consider(10, "all-title-terms", title);
    aliases.forEach(function (alias) {
      if (alias === query || compact(alias) === queryCompact) consider(9, "exact-alias", alias);
      else if (alias.indexOf(query) === 0) consider(8, "alias-prefix", alias);
      else if (allTermsIn(alias, terms)) consider(7, "alias-terms", alias);
    });
    verifiedTerms.forEach(function (value) {
      if (value === query || compact(value) === queryCompact) consider(6, "verified-term-exact", value);
      else if (allTermsIn(value, terms)) consider(5, "verified-term", value);
    });
    if (allTermsIn(titleAndManufacturer, terms)) consider(4, "manufacturer-title", titleAndManufacturer);
    if (allTermsIn(category, terms)) consider(3, "category-intent-kind", category);
    if (allTermsIn(summary, terms)) consider(2, "summary", summary);
    if (allTermsIn(broader, terms)) consider(1, "broader-metadata", broader);

    if (!matchTier) return { matched: false, matchTier: 0, specificity: 0, priority: 0, reason: "no-match" };
    var priorityApplies = aliases.some(function (alias) { return alias === query || compact(alias) === queryCompact; });
    var priority = priorityApplies ? Number(record.searchPriority || 0) : 0;
    if (!Number.isFinite(priority)) priority = 0;
    return { matched: true, matchTier: matchTier, specificity: specificity, priority: priority, reason: reason };
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
      return right.result.matchTier - left.result.matchTier ||
        right.result.specificity - left.result.specificity ||
        right.result.priority - left.result.priority ||
        left.canonicalOrder - right.canonicalOrder ||
        String(left.record.id || "").localeCompare(String(right.record.id || ""));
    });
  }

  return { normalize: normalize, score: score, rank: rank };
}));
