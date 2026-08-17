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

  function initProductExplorer(root) {
    var tabs = Array.prototype.slice.call(root.querySelectorAll("[data-explorer-target]"));
    var panels = Array.prototype.slice.call(root.querySelectorAll("[data-explorer-panel]"));
    if (!tabs.length || !panels.length) return;

    function activate(productId, moveFocus) {
      var activePanel = null;
      tabs.forEach(function (tab) {
        var active = tab.dataset.explorerTarget === productId;
        tab.setAttribute("aria-selected", String(active));
        tab.setAttribute("tabindex", active ? "0" : "-1");
        if (active && moveFocus) tab.focus();
      });
      panels.forEach(function (panel) {
        var active = panel.dataset.productId === productId;
        panel.toggleAttribute("data-active", active);
        panel.setAttribute("aria-hidden", String(!active));
        panel.inert = !active;
        if (active) activePanel = panel;
      });
      if (activePanel) root.dataset.activeEnvironment = activePanel.dataset.environment || "neutral";
    }

    tabs.forEach(function (tab, index) {
      tab.addEventListener("click", function (event) {
        event.preventDefault();
        activate(tab.dataset.explorerTarget, false);
      });
      tab.addEventListener("keydown", function (event) {
        var nextIndex = null;
        if (event.key === "ArrowRight" || event.key === "ArrowDown") nextIndex = (index + 1) % tabs.length;
        if (event.key === "ArrowLeft" || event.key === "ArrowUp") nextIndex = (index - 1 + tabs.length) % tabs.length;
        if (event.key === "Home") nextIndex = 0;
        if (event.key === "End") nextIndex = tabs.length - 1;
        if (nextIndex === null) return;
        event.preventDefault();
        activate(tabs[nextIndex].dataset.explorerTarget, true);
        if (!reduceMotion) tabs[nextIndex].scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
      });
    });

    var selected = tabs.find(function (tab) { return tab.getAttribute("aria-selected") === "true"; }) || tabs[0];
    activate(selected.dataset.explorerTarget, false);
  }

  document.querySelectorAll("[data-product-explorer]").forEach(initProductExplorer);

  function initHeroParallax(hero) {
    if (reduceMotion || !window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
    var layers = Array.prototype.slice.call(hero.querySelectorAll("[data-parallax-depth]"));
    if (!layers.length) return;
    var targetX = 0;
    var targetY = 0;
    var currentX = 0;
    var currentY = 0;
    var frame = 0;

    function render() {
      currentX += (targetX - currentX) * .12;
      currentY += (targetY - currentY) * .12;
      layers.forEach(function (layer) {
        var depth = Number(layer.dataset.parallaxDepth || 1);
        layer.style.setProperty("--parallax-x", (currentX * depth * 10).toFixed(2) + "px");
        layer.style.setProperty("--parallax-y", (currentY * depth * 7).toFixed(2) + "px");
      });
      if (Math.abs(targetX - currentX) > .003 || Math.abs(targetY - currentY) > .003) frame = window.requestAnimationFrame(render);
      else frame = 0;
    }

    function requestRender() {
      if (!frame) frame = window.requestAnimationFrame(render);
    }

    hero.addEventListener("pointermove", function (event) {
      var bounds = hero.getBoundingClientRect();
      targetX = Math.max(-1, Math.min(1, ((event.clientX - bounds.left) / bounds.width - .5) * 2));
      targetY = Math.max(-1, Math.min(1, ((event.clientY - bounds.top) / bounds.height - .5) * 2));
      requestRender();
    }, { passive: true });
    hero.addEventListener("pointerleave", function () {
      targetX = 0;
      targetY = 0;
      requestRender();
    }, { passive: true });
  }

  var homeHero = document.querySelector(".home-hero");
  if (homeHero) initHeroParallax(homeHero);

  function initMatrixField(canvas, staticMode) {
    var hero = canvas.closest(".home-hero");
    var context = canvas.getContext("2d");
    if (!hero || !context) return;

    var width = 0;
    var height = 0;
    var pixelRatio = Math.min(window.devicePixelRatio || 1, 1.5);
    var frame = 0;
    var visible = true;
    var pointer = { x: 0, y: 0, targetX: 0, targetY: 0 };
    var nodes = [];
    var edges = [];
    var seed = 2021428066;

    function random() {
      seed = (seed * 1664525 + 1013904223) % 4294967296;
      return seed / 4294967296;
    }

    function addNode(x, y, z, kind, size) {
      nodes.push({ x: x, y: y, z: z, kind: kind, size: size });
      return nodes.length - 1;
    }

    for (var index = 0; index < 72; index += 1) {
      addNode((random() - .5) * 720, (random() - .5) * 520, (random() - .5) * 520, index % 9 === 0 ? 1 : 0, .8 + random() * 1.8);
    }

    for (var left = 0; left < 72; left += 1) {
      for (var right = left + 1; right < 72; right += 1) {
        var dx = nodes[left].x - nodes[right].x;
        var dy = nodes[left].y - nodes[right].y;
        var dz = nodes[left].z - nodes[right].z;
        var distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
        if (distance < 150 && random() > .28) edges.push([left, right, 0]);
      }
    }

    var strandA = [];
    var strandB = [];
    for (var helix = 0; helix < 34; helix += 1) {
      var progress = helix / 33;
      var angle = helix * .58;
      var vertical = (progress - .5) * 500;
      strandA.push(addNode(Math.cos(angle) * 118, vertical, Math.sin(angle) * 118, 2, 2.5));
      strandB.push(addNode(Math.cos(angle + Math.PI) * 118, vertical, Math.sin(angle + Math.PI) * 118, 3, 2.5));
      if (helix > 0) {
        edges.push([strandA[helix - 1], strandA[helix], 1]);
        edges.push([strandB[helix - 1], strandB[helix], 1]);
      }
      if (helix % 2 === 0) edges.push([strandA[helix], strandB[helix], 2]);
    }

    function resize() {
      var bounds = hero.getBoundingClientRect();
      width = Math.max(1, Math.round(bounds.width));
      height = Math.max(1, Math.round(bounds.height));
      canvas.width = Math.round(width * pixelRatio);
      canvas.height = Math.round(height * pixelRatio);
      canvas.style.width = width + "px";
      canvas.style.height = height + "px";
      context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
      if (staticMode) draw(0);
    }

    function project(node, time) {
      var rotationY = time * .000035 + pointer.x * .22;
      var rotationX = -.1 + pointer.y * .13;
      var cosY = Math.cos(rotationY);
      var sinY = Math.sin(rotationY);
      var cosX = Math.cos(rotationX);
      var sinX = Math.sin(rotationX);
      var rotatedX = node.x * cosY - node.z * sinY;
      var rotatedZ = node.x * sinY + node.z * cosY;
      var rotatedY = node.y * cosX - rotatedZ * sinX;
      rotatedZ = node.y * sinX + rotatedZ * cosX;
      var focalLength = 720;
      var depth = focalLength / Math.max(220, focalLength + rotatedZ);
      var fieldScale = Math.min(width, height) / 710;
      var centerX = width < 900 ? width * .5 : width * .7;
      var centerY = height * .47;
      return {
        x: centerX + rotatedX * depth * fieldScale,
        y: centerY + rotatedY * depth * fieldScale,
        z: rotatedZ,
        scale: depth * fieldScale
      };
    }

    function draw(time) {
      if (!width || !height) return;
      pointer.x += (pointer.targetX - pointer.x) * .045;
      pointer.y += (pointer.targetY - pointer.y) * .045;
      context.clearRect(0, 0, width, height);
      var projected = nodes.map(function (node) { return project(node, time); });

      edges.forEach(function (edge) {
        var start = projected[edge[0]];
        var end = projected[edge[1]];
        var depthAlpha = Math.max(.05, Math.min(.42, .24 - (start.z + end.z) / 3000));
        context.beginPath();
        context.moveTo(start.x, start.y);
        context.lineTo(end.x, end.y);
        context.lineWidth = edge[2] === 1 ? 1.15 : .65;
        context.strokeStyle = edge[2] === 2
          ? "rgba(223,187,120," + (depthAlpha * .72) + ")"
          : edge[2] === 1
            ? "rgba(112,170,140," + depthAlpha + ")"
            : "rgba(248,244,236," + (depthAlpha * .38) + ")";
        context.stroke();
      });

      nodes.forEach(function (node, nodeIndex) {
        var point = projected[nodeIndex];
        var radius = Math.max(.6, node.size * point.scale);
        var isHelix = node.kind >= 2;
        context.beginPath();
        context.arc(point.x, point.y, radius, 0, Math.PI * 2);
        context.fillStyle = node.kind === 2
          ? "rgba(223,187,120,.92)"
          : node.kind === 3 || node.kind === 1
            ? "rgba(136,190,160,.88)"
            : "rgba(248,244,236,.42)";
        if (isHelix && nodeIndex % 7 === 0) {
          context.shadowBlur = 12;
          context.shadowColor = node.kind === 2 ? "rgba(223,187,120,.8)" : "rgba(112,170,140,.8)";
        }
        context.fill();
        context.shadowBlur = 0;

        if (isHelix && nodeIndex % 11 === 0) {
          var pulse = staticMode ? 5 : 5 + ((time * .015 + nodeIndex) % 10);
          context.beginPath();
          context.arc(point.x, point.y, radius + pulse, 0, Math.PI * 2);
          context.strokeStyle = node.kind === 2 ? "rgba(223,187,120,.18)" : "rgba(112,170,140,.18)";
          context.lineWidth = 1;
          context.stroke();
        }
      });

      if (!staticMode && visible && !document.hidden) frame = window.requestAnimationFrame(draw);
    }

    function start() {
      if (staticMode || frame || !visible || document.hidden) return;
      frame = window.requestAnimationFrame(draw);
    }

    function stop() {
      if (!frame) return;
      window.cancelAnimationFrame(frame);
      frame = 0;
    }

    if (!staticMode) {
      hero.addEventListener("pointermove", function (event) {
        var bounds = hero.getBoundingClientRect();
        pointer.targetX = ((event.clientX - bounds.left) / bounds.width - .5) * 2;
        pointer.targetY = ((event.clientY - bounds.top) / bounds.height - .5) * 2;
      }, { passive: true });
      hero.addEventListener("pointerleave", function () {
        pointer.targetX = 0;
        pointer.targetY = 0;
      }, { passive: true });
      document.addEventListener("visibilitychange", function () {
        if (document.hidden) stop(); else start();
      });
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (entries) {
          visible = entries[0].isIntersecting;
          if (visible) start(); else stop();
        }, { threshold: .02 }).observe(hero);
      }
    }

    if ("ResizeObserver" in window) new ResizeObserver(resize).observe(hero);
    else window.addEventListener("resize", resize, { passive: true });
    resize();
    start();
  }

  var matrixCanvas = document.querySelector("[data-matrix-field]");
  if (matrixCanvas) initMatrixField(matrixCanvas, reduceMotion);
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
  var matrixSequence = document.querySelector("[data-matrix-sequence]");
  var matrixProgressPath = document.querySelector("[data-matrix-path-progress]");
  var matrixProgressFrame = 0;

  function updateMatrixProgress() {
    matrixProgressFrame = 0;
    if (!matrixSequence || !matrixProgressPath) return;
    var bounds = matrixSequence.getBoundingClientRect();
    var startLine = window.innerHeight * .72;
    var travel = Math.max(1, bounds.height - window.innerHeight * .46);
    var progress = Math.max(0, Math.min(1, (startLine - bounds.top) / travel));
    matrixProgressPath.style.strokeDashoffset = String(1 - progress);
  }

  function requestMatrixProgress() {
    if (!matrixProgressFrame) matrixProgressFrame = window.requestAnimationFrame(updateMatrixProgress);
  }

  if (matrixSequence && matrixProgressPath) {
    window.addEventListener("scroll", requestMatrixProgress, { passive: true });
    window.addEventListener("resize", requestMatrixProgress, { passive: true });
    updateMatrixProgress();
  }

  if (stages[0]) stages[0].classList.add("is-active");
  var matrixObserver = new IntersectionObserver(function (entries) {
    var visibleEntries = entries.filter(function (entry) { return entry.isIntersecting; }).sort(function (left, right) { return right.intersectionRatio - left.intersectionRatio; });
    if (!visibleEntries.length) return;
    var activeStage = visibleEntries[0].target;
    stages.forEach(function (stage) { stage.classList.toggle("is-active", stage === activeStage); });
    if (matrixSequence) matrixSequence.dataset.activeStage = activeStage.dataset.matrixStage;
  }, { rootMargin: "-20% 0px -38%", threshold: 0.2 });

  stages.forEach(function (stage) { matrixObserver.observe(stage); });
}());
