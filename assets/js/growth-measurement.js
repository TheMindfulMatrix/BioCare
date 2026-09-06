/* Inert integration foundation: deliberately NOT loaded by the public builder.
 * No network, storage, cookie or vendor code. A reviewed transport is required.
 * Confirmed subscriptions/orders/commissions must come from provider reports.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.MatrixMeasurement = api;
})(typeof window === "undefined" ? globalThis : window, function () {
  "use strict";
  const actions = new Set(["page_view", "manufacturer_click", "contact_click", "education_click"]);
  const sources = new Set(["instagram", "threads", "tiktok", "x", "email", "google", "bing"]);
  const merchants = new Set(["zinzino", "biolimitless"]);
  const bindings = new WeakMap();

  function section(pathname) {
    const path = String(pathname || "").replace(/^\/BioCare\//, "/");
    if (path === "/" || path === "/index.html") return "home";
    if (/^\/products\//.test(path) || path === "/shop.html") return "products";
    if (/^\/library\//.test(path) || path === "/library.html") return "library";
    if (path === "/evidence.html") return "evidence";
    if (["/start.html", "/know-your-number.html", "/core-four.html"].includes(path)) return "journeys";
    if (path === "/explore.html" || /^\/departments\//.test(path)) return "explore";
    if (["/about.html", "/privacy.html"].includes(path)) return "business";
    return "other";
  }

  function source(search, referrer) {
    const supplied = new URLSearchParams(String(search || "")).get("utm_source");
    if (sources.has(supplied)) return supplied;
    if (!referrer) return "direct_or_unknown";
    try {
      const host = new URL(referrer).hostname.toLowerCase();
      if (["themindfulmatrixhealth.com", "www.themindfulmatrixhealth.com"].includes(host)) return "internal";
      const known = {"instagram.com":"instagram", "threads.com":"threads", "threads.net":"threads", "tiktok.com":"tiktok", "x.com":"x", "t.co":"x", "google.com":"google", "bing.com":"bing"};
      for (const [domain, label] of Object.entries(known)) {
        if (host === domain || host.endsWith("." + domain)) return label;
      }
    } catch (_) { /* Malformed referrers are never retained. */ }
    return "other_referral";
  }

  function event(action, input = {}) {
    if (!actions.has(action)) return null;
    const result = {action, section:section(input.pathname), source:source(input.search, input.referrer)};
    if (action === "manufacturer_click") {
      if (!merchants.has(input.merchant)) return null;
      result.merchant = input.merchant;
    }
    return Object.freeze(result);
  }

  function createTracker({enabled = false, send, now = Date.now} = {}) {
    const active = enabled === true && typeof send === "function";
    const recent = new Map();
    let viewed = false;
    return Object.freeze({
      active,
      track(action, input) {
        if (!active) return false;
        const payload = event(action, input);
        if (!payload || (action === "page_view" && viewed)) return false;
        const key = JSON.stringify(payload), time = now();
        if (recent.has(key) && time - recent.get(key) < 1000) return false;
        if (action === "page_view") viewed = true;
        recent.set(key, time);
        try {
          // The injected adapter receives ONLY the frozen allowlisted payload.
          const result = send(payload);
          if (result && typeof result.catch === "function") result.catch(() => {});
          return true; // Accepted by the adapter, never a confirmed sale.
        } catch (_) { return false; }
      }
    });
  }

  function bind(document, options = {}) {
    if (bindings.has(document)) return bindings.get(document);
    const tracker = createTracker(options);
    if (!tracker.active) return tracker;
    const view = document.defaultView;
    const context = () => ({pathname:view.location.pathname, search:view.location.search, referrer:document.referrer});
    const click = e => {
      const anchor = e.target.closest && e.target.closest("a[href]");
      if (!anchor) return;
      try {
        const url = new URL(anchor.href, view.location.href);
        const merchant = ["zinzino.com", "www.zinzino.com"].includes(url.hostname) ? "zinzino" : ["biolimitless.com", "www.biolimitless.com"].includes(url.hostname) ? "biolimitless" : null;
        if (merchant && anchor.relList.contains("sponsored")) tracker.track("manufacturer_click", {...context(), merchant});
        else if (url.protocol === "mailto:") tracker.track("contact_click", context());
        else if (url.origin === view.location.origin && /\/library\//.test(url.pathname)) tracker.track("education_click", context());
      } catch (_) { /* Measurement never interferes with link navigation. */ }
    };
    document.addEventListener("click", click);
    document.addEventListener("auxclick", e => { if (e.button === 1) click(e); });
    bindings.set(document, tracker);
    tracker.track("page_view", context());
    return tracker;
  }
  return Object.freeze({event, section, source, createTracker, bind});
});
