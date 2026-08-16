(function () {
  document.documentElement.classList.add("js");

  var toggle = document.querySelector(".nav-toggle");
  var menu = document.getElementById("primary-links");

  function setMenu(open) {
    if (!toggle || !menu) return;
    toggle.setAttribute("aria-expanded", String(open));
    toggle.querySelector(".visually-hidden").textContent = open ? "Close navigation" : "Open navigation";
    menu.dataset.open = String(open);
  }

  if (toggle && menu) {
    setMenu(false);
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    menu.addEventListener("click", function (event) {
      if (event.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setMenu(false);
        toggle.focus();
      }
    });
  }

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion || !("IntersectionObserver" in window)) return;

  document.documentElement.classList.add("motion-ready");
  var revealObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-visible");
      entry.target.querySelectorAll(".path-draw").forEach(function (path) {
        path.classList.add("is-visible");
      });
      revealObserver.unobserve(entry.target);
    });
  }, { rootMargin: "0px 0px -8%", threshold: 0.08 });

  document.querySelectorAll("[data-reveal]").forEach(function (target) {
    revealObserver.observe(target);
  });

  var stages = Array.prototype.slice.call(document.querySelectorAll("[data-matrix-stage]"));
  var segments = Array.prototype.slice.call(document.querySelectorAll(".matrix-spine span"));
  var matrixObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var index = stages.indexOf(entry.target);
      entry.target.classList.add("is-active");
      if (segments[index]) segments[index].classList.add("is-active");
    });
  }, { rootMargin: "-20% 0px -38%", threshold: 0.2 });

  stages.forEach(function (stage) { matrixObserver.observe(stage); });
}());
