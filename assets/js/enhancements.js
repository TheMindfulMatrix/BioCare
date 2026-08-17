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

  function initProductUniverse(root) {
    var intentButtons = Array.prototype.slice.call(root.querySelectorAll("[data-universe-intent]"));
    var products = Array.prototype.slice.call(root.querySelectorAll("[data-universe-product]"));
    var rosterButtons = Array.prototype.slice.call(root.querySelectorAll("[data-universe-select]"));
    var stepButtons = Array.prototype.slice.call(root.querySelectorAll("[data-universe-step]"));
    var intentIndex = root.querySelector("[data-universe-intent-index]");
    var intentName = root.querySelector("[data-universe-intent-name]");
    var intentDescription = root.querySelector("[data-universe-intent-description]");
    var position = root.querySelector("[data-universe-position]");
    var total = root.querySelector("[data-universe-total]");
    var status = root.querySelector("[data-universe-status]");
    var stage = root.querySelector(".product-universe__stage");
    if (!intentButtons.length || !products.length || !rosterButtons.length) return;

    var activeIntent = intentButtons[0].dataset.universeIntent;
    var activeProduct = products.find(function (product) { return product.hasAttribute("data-active"); }) || products[0];
    var touchStartX = 0;
    var imageLoadToken = 0;
    var transitionAnimation = null;
    root.dataset.enhanced = "true";

    function productsForIntent(intent) {
      return products.filter(function (product) { return product.dataset.productIntent === intent; });
    }

    function intentButton(intent) {
      return intentButtons.find(function (button) { return button.dataset.universeIntent === intent; });
    }

    function updateIntent(intent) {
      var button = intentButton(intent);
      if (!button) return;
      activeIntent = intent;
      root.dataset.activeIntent = intent;
      root.dataset.activeEnvironment = button.dataset.intentEnvironment || "signal";
      intentButtons.forEach(function (item) {
        item.setAttribute("aria-pressed", String(item === button));
      });
      if (intentIndex) intentIndex.textContent = button.dataset.intentIndex || "";
      if (intentName) intentName.textContent = button.dataset.intentName || "";
      if (intentDescription) intentDescription.textContent = button.dataset.intentDescription || "";
      rosterButtons.forEach(function (item) {
        item.hidden = item.dataset.productIntent !== intent;
      });
    }

    function activateProduct(productId, announce) {
      var next = products.find(function (product) { return product.dataset.universeProduct === productId; });
      if (!next) return;
      if (next.dataset.productIntent !== activeIntent) updateIntent(next.dataset.productIntent);
      activeProduct = next;
      products.forEach(function (product) {
        var active = product === next;
        product.toggleAttribute("data-active", active);
        product.setAttribute("aria-hidden", String(!active));
        product.inert = !active;
        if (!active) product.removeAttribute("aria-busy");
      });
      rosterButtons.forEach(function (button) {
        button.setAttribute("aria-pressed", String(button.dataset.universeSelect === productId));
      });
      var intentProducts = productsForIntent(activeIntent);
      var localIndex = intentProducts.indexOf(next);
      if (position) position.textContent = String(localIndex + 1).padStart(2, "0");
      if (total) total.textContent = String(intentProducts.length).padStart(2, "0");
      var image = next.querySelector("img[data-image-role='official-product-cutout']");
      var token = ++imageLoadToken;
      function settleImage() {
        if (token !== imageLoadToken) return;
        if (stage) stage.removeAttribute("data-loading");
        next.removeAttribute("aria-busy");
      }
      if (image && !image.complete) {
        image.loading = "eager";
        if (stage) stage.dataset.loading = "true";
        next.setAttribute("aria-busy", "true");
        image.addEventListener("load", settleImage, { once: true });
        image.addEventListener("error", settleImage, { once: true });
      } else {
        settleImage();
      }
      if (announce && status) {
        var selectedIntent = intentButton(activeIntent);
        status.textContent = next.querySelector("h3").textContent + " selected. Product " + (localIndex + 1) + " of " + intentProducts.length + " in " + selectedIntent.dataset.intentName + ".";
      }
      if (transitionAnimation) transitionAnimation.cancel();
      if (announce && !reduceMotion) {
        transitionAnimation = next.animate(
          [{ opacity: .55, transform: "translateY(10px) scale(.985)" }, { opacity: 1, transform: "translateY(0) scale(1)" }],
          { duration: 360, easing: "cubic-bezier(.2,.75,.25,1)" }
        );
      }
    }

    function activateIntent(button, moveFocus) {
      updateIntent(button.dataset.universeIntent);
      activateProduct(button.dataset.intentFeatured || productsForIntent(activeIntent)[0].dataset.universeProduct, true);
      if (moveFocus) button.focus();
    }

    function stepProduct(direction) {
      var intentProducts = productsForIntent(activeIntent);
      var index = intentProducts.indexOf(activeProduct);
      var nextIndex = (index + direction + intentProducts.length) % intentProducts.length;
      activateProduct(intentProducts[nextIndex].dataset.universeProduct, true);
    }

    intentButtons.forEach(function (button, index) {
      button.addEventListener("click", function () { activateIntent(button, false); });
      button.addEventListener("keydown", function (event) {
        var nextIndex = null;
        if (event.key === "ArrowRight" || event.key === "ArrowDown") nextIndex = (index + 1) % intentButtons.length;
        if (event.key === "ArrowLeft" || event.key === "ArrowUp") nextIndex = (index - 1 + intentButtons.length) % intentButtons.length;
        if (event.key === "Home") nextIndex = 0;
        if (event.key === "End") nextIndex = intentButtons.length - 1;
        if (nextIndex === null) return;
        event.preventDefault();
        activateIntent(intentButtons[nextIndex], true);
      });
    });

    rosterButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        activateProduct(button.dataset.universeSelect, true);
      });
    });

    stepButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        stepProduct(Number(button.dataset.universeStep));
      });
    });

    if (stage) {
      stage.addEventListener("touchstart", function (event) {
        touchStartX = event.changedTouches[0].clientX;
      }, { passive: true });
      stage.addEventListener("touchend", function (event) {
        var distance = event.changedTouches[0].clientX - touchStartX;
        if (Math.abs(distance) > 48) stepProduct(distance < 0 ? 1 : -1);
      }, { passive: true });
      if (!reduceMotion && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
        stage.addEventListener("pointermove", function (event) {
          var bounds = stage.getBoundingClientRect();
          var x = ((event.clientX - bounds.left) / bounds.width - .5) * 2;
          var y = ((event.clientY - bounds.top) / bounds.height - .5) * 2;
          stage.style.setProperty("--universe-tilt-x", (y * -2.2).toFixed(2) + "deg");
          stage.style.setProperty("--universe-tilt-y", (x * 3).toFixed(2) + "deg");
        }, { passive: true });
        stage.addEventListener("pointerleave", function () {
          stage.style.setProperty("--universe-tilt-x", "0deg");
          stage.style.setProperty("--universe-tilt-y", "0deg");
        }, { passive: true });
      }
    }

    updateIntent(activeProduct.dataset.productIntent);
    activateProduct(activeProduct.dataset.universeProduct, false);
  }

  document.querySelectorAll("[data-product-universe]").forEach(initProductUniverse);

  function initShopFilters(root) {
    var buttons = Array.prototype.slice.call(root.querySelectorAll("[data-shop-brand]"));
    var products = Array.prototype.slice.call(document.querySelectorAll("[data-shop-product]"));
    var groups = Array.prototype.slice.call(document.querySelectorAll("[data-shop-group]"));
    var status = root.querySelector("[data-shop-filter-status]");
    if (!buttons.length || !products.length) return;
    root.dataset.enhanced = "true";

    function applyFilter(manufacturer, announce) {
      var visibleCount = 0;
      root.dataset.activeManufacturer = manufacturer;
      buttons.forEach(function (button) {
        var active = button.dataset.shopBrand === manufacturer;
        button.setAttribute("aria-pressed", String(active));
        button.setAttribute("tabindex", active ? "0" : "-1");
      });
      products.forEach(function (product) {
        var visible = manufacturer === "all" || product.dataset.manufacturer === manufacturer;
        product.hidden = !visible;
        if (visible) visibleCount += 1;
      });
      groups.forEach(function (group) {
        var visibleProducts = Array.prototype.slice.call(group.querySelectorAll("[data-shop-product]:not([hidden])"));
        var counter = group.querySelector("[data-shop-group-count]");
        var empty = group.querySelector("[data-shop-empty]");
        if (counter) counter.textContent = String(visibleProducts.length).padStart(2, "0") + " verified product" + (visibleProducts.length === 1 ? "" : "s");
        if (empty) empty.hidden = visibleProducts.length > 0;
      });
      if (announce && status) status.textContent = manufacturer === "all"
        ? "Showing all " + visibleCount + " active products."
        : "Showing " + visibleCount + " " + manufacturer + " products.";
    }

    buttons.forEach(function (button, index) {
      button.addEventListener("click", function () { applyFilter(button.dataset.shopBrand, true); });
      button.addEventListener("keydown", function (event) {
        var nextIndex = null;
        if (event.key === "ArrowRight" || event.key === "ArrowDown") nextIndex = (index + 1) % buttons.length;
        if (event.key === "ArrowLeft" || event.key === "ArrowUp") nextIndex = (index - 1 + buttons.length) % buttons.length;
        if (event.key === "Home") nextIndex = 0;
        if (event.key === "End") nextIndex = buttons.length - 1;
        if (nextIndex === null) return;
        event.preventDefault();
        applyFilter(buttons[nextIndex].dataset.shopBrand, true);
        buttons[nextIndex].focus();
      });
    });

    applyFilter("all", false);
  }

  document.querySelectorAll("[data-shop-filter-root]").forEach(initShopFilters);

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

  var depthLayers = Array.prototype.slice.call(document.querySelectorAll("[data-scroll-depth]"));
  var depthFrame = 0;

  function updateScrollDepth() {
    depthFrame = 0;
    var viewportCenter = window.innerHeight * .5;
    depthLayers.forEach(function (layer) {
      var bounds = layer.getBoundingClientRect();
      if (bounds.bottom < -120 || bounds.top > window.innerHeight + 120) return;
      var depth = Number(layer.dataset.scrollDepth || .4);
      var distance = viewportCenter - (bounds.top + bounds.height * .5);
      var shift = Math.max(-24, Math.min(24, distance * depth * .035));
      layer.style.setProperty("--scroll-depth-shift", shift.toFixed(2) + "px");
    });
  }

  function requestScrollDepth() {
    if (!depthFrame) depthFrame = window.requestAnimationFrame(updateScrollDepth);
  }

  if (depthLayers.length) {
    window.addEventListener("scroll", requestScrollDepth, { passive: true });
    window.addEventListener("resize", requestScrollDepth, { passive: true });
    updateScrollDepth();
  }

  var testingWorkflow = document.querySelector("[data-testing-workflow]");
  var workflowSteps = testingWorkflow ? Array.prototype.slice.call(testingWorkflow.querySelectorAll("[data-workflow-step]")) : [];
  var workflowFrame = 0;

  function updateTestingWorkflow() {
    workflowFrame = 0;
    if (!testingWorkflow || !workflowSteps.length) return;
    var bounds = testingWorkflow.getBoundingClientRect();
    var travel = Math.max(1, window.innerHeight * .62);
    var progress = Math.max(0, Math.min(1, (window.innerHeight * .82 - bounds.top) / travel));
    testingWorkflow.style.setProperty("--workflow-progress", (progress * 100).toFixed(1) + "%");
    var activeCount = Math.max(1, Math.ceil(progress * workflowSteps.length));
    workflowSteps.forEach(function (step, index) {
      step.classList.toggle("is-active", index < activeCount);
    });
  }

  function requestTestingWorkflow() {
    if (!workflowFrame) workflowFrame = window.requestAnimationFrame(updateTestingWorkflow);
  }

  if (testingWorkflow) {
    window.addEventListener("scroll", requestTestingWorkflow, { passive: true });
    window.addEventListener("resize", requestTestingWorkflow, { passive: true });
    updateTestingWorkflow();
  }

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
