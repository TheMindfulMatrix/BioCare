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
    var rosterButtons = Array.prototype.slice.call(root.querySelectorAll("[data-universe-select]"));
    var stepButtons = Array.prototype.slice.call(root.querySelectorAll("[data-universe-step]"));
    var dataNode = root.querySelector("[data-universe-data]");
    var productContainer = root.querySelector("#universe-products");
    var intentIndex = root.querySelector("[data-universe-intent-index]");
    var intentName = root.querySelector("[data-universe-intent-name]");
    var intentDescription = root.querySelector("[data-universe-intent-description]");
    var position = root.querySelector("[data-universe-position]");
    var total = root.querySelector("[data-universe-total]");
    var status = root.querySelector("[data-universe-status]");
    var stage = root.querySelector(".product-universe__stage");
    if (!intentButtons.length || !rosterButtons.length || !dataNode || !productContainer) return;
    var products;
    try { products = JSON.parse(dataNode.textContent || "[]"); } catch (error) { return; }
    if (!products.length) return;
    var initialArticle = productContainer.querySelector("[data-universe-product]");
    var initialId = initialArticle ? initialArticle.dataset.universeProduct : products[0].id;
    var activeProduct = products.find(function (product) { return product.id === initialId; }) || products[0];
    var activeIntent = activeProduct.intent;
    var touchStartX = 0;
    var transitionAnimation = null;
    root.dataset.enhanced = "true";

    function e(value) { return String(value == null ? "" : value).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/\"/g,"&quot;").replace(/'/g,"&#39;"); }
    function money(value) { var number=Number(value); return new Intl.NumberFormat("en-US",{style:"currency",currency:"USD",minimumFractionDigits:Number.isInteger(number)?0:2,maximumFractionDigits:2}).format(number); }
    function priceItem(value,label,role) { return '<span class="product-price__item product-price__item--'+role+'" data-price-role="'+role+'"><strong>'+value+'</strong> '+label+'</span>'; }
    function priceMarkup(product) {
      var price=product.price, items=[];
      if (price.pricing_model === "starter_subscription") items=[priceItem(money(price.start_price),e(price.start_label),"primary"),priceItem(money(price.recurring_price)+"/mo",e(price.recurring_label),"supporting")];
      else if (price.pricing_model === "retail_premier") items=price.premier_price!=null?[priceItem(money(price.premier_price),"Premier price","primary"),priceItem(money(price.retail_price),"retail","reference")]:[priceItem(money(price.retail_price),"retail","primary")];
      else if (price.pricing_model === "one_time_autoship") items=[priceItem(money(price.autoship_price)+"/mo","Subscribe &amp; Save","primary"),priceItem(money(price.one_time_price),"one-time","reference")];
      else if (price.pricing_model === "one_time_range") items=[priceItem(money(price.one_time_price_min)+"–"+money(price.one_time_price_max),"one-time · format varies","primary")];
      else items=[priceItem(money(price.one_time_price),"one-time","primary")];
      var helper=product.manufacturer==="Zinzino"&&price.premier_price!=null?"<small>Premier pricing may require an eligible Premier purchase or customer status. Checkout reflects the current applicable price.</small>":"";
      return '<div>'+items.join("")+'</div>'+helper+'<a class="product-price__source" href="'+e(price.affiliate_price_source)+'" target="_blank" rel="sponsored noopener noreferrer" aria-describedby="shelf-affiliate-disclosure" aria-label="Official price source for '+e(product.name)+' (opens in a new tab)">Official price source ↗<span class="visually-hidden"> (opens in a new tab)</span></a>';
    }
    function productsForIntent(intent) {
      var filteredIds=(root.dataset.universeFilterIds||"").split(",").filter(Boolean);
      if(filteredIds.length){return filteredIds.map(function(id){return products.find(function(product){return product.id===id;});}).filter(function(product){return product&&product.intent===intent;});}
      return products.filter(function(product){return product.intent===intent;});
    }
    function intentButton(intent) { return intentButtons.find(function(button){return button.dataset.universeIntent===intent;}); }
    function replaceArtwork(article, product) {
      var old=article.querySelector(".shelf-card__artwork"); if(!old)return;
      var node;
      if(product.artwork&&product.artwork.src){node=document.createElement("img");node.className="shelf-card__artwork artwork-stage__background";node.src=product.artwork.src;node.alt="";node.width=Number(product.artwork.width);node.height=Number(product.artwork.height);node.loading="lazy";node.decoding="async";node.dataset.artworkState="ready";}
      else{node=document.createElement("span");node.className="shelf-card__artwork artwork-stage__background";node.dataset.artworkState="placeholder";node.setAttribute("aria-hidden","true");}
      old.replaceWith(node);
    }
    function renderProduct(product, announce) {
      var article=productContainer.querySelector("[data-universe-product]"); if(!article)return;
      activeProduct=product;
      article.className="product-universe__product"+(product.name.length>=42?" product-name--very-long":product.name.length>=30?" product-name--long":"");
      article.dataset.universeProduct=product.id;article.dataset.productIntent=product.intent;article.dataset.manufacturer=product.manufacturer;article.dataset.environment=product.environment;article.dataset.active="true";article.id="";
      var titleId="universe-product-title-"+product.id;article.setAttribute("aria-labelledby",titleId);
      replaceArtwork(article,product);
      var cutout=article.querySelector("img[data-image-role='official-product-cutout']");
      if(cutout&&product.cutout){cutout.src=product.cutout.src;cutout.alt=product.cutout.alt;cutout.width=Number(product.cutout.width);cutout.height=Number(product.cutout.height);cutout.loading="eager";}
      var sku=article.querySelector(".product-universe__sku");if(sku)sku.textContent=product.sku?"SKU "+product.sku:"BioLimitless product";
      var number=article.querySelector(".product-universe__number");if(number)number.textContent=String(product.index).padStart(2,"0");
      var label=article.querySelector(".product-universe__content .interface-label");if(label)label.textContent=product.category+" / "+product.productKind;
      var title=article.querySelector(".product-universe__content h3");if(title){title.id=titleId;title.textContent=product.name;}
      var description=article.querySelector(".product-universe__description");if(description)description.textContent=product.description;
      var facts=article.querySelectorAll(".product-universe__facts dd");if(facts[0])facts[0].textContent=product.manufacturer;if(facts[1])facts[1].textContent=product.variantLabel;
      var price=article.querySelector(".product-price");if(price){price.dataset.priceModel=product.price.pricing_model;price.dataset.priceVerified=product.price.price_verified_at;price.innerHTML=priceMarkup(product);}
      var why=article.querySelector(".product-universe__why p");if(why)why.textContent=product.whyItsHere;
      var existingBio=article.querySelector("[data-biolimitless-disclosure]");if(existingBio)existingBio.remove();
      if(product.manufacturer==="BioLimitless"){var bio=document.createElement("p");bio.className="fine product-material-connection";bio.dataset.biolimitlessDisclosure="";bio.textContent="BioLimitless links use the Matrix partner referral. I may earn compensation from qualifying purchases.";article.querySelector(".product-universe__why").after(bio);}
      var row=article.querySelector(".product-universe__content .button-row");if(row){var related=product.relatedEducation?'<a class="product-universe__learn" href="'+e(product.relatedEducation.href)+'" aria-label="'+e(product.relatedEducation.label)+' for '+e(product.name)+'">'+e(product.relatedEducation.label)+' →</a>':"";row.innerHTML='<a class="button button-primary" href="'+e(product.destination)+'" target="_blank" rel="sponsored noopener noreferrer" aria-label="'+e(product.cta)+': '+e(product.name)+' (opens in a new tab)">'+e(product.cta)+' ↗<span class="visually-hidden"> (opens in a new tab)</span></a>'+related;}
      var intentProducts=productsForIntent(activeIntent), localIndex=intentProducts.indexOf(product);
      if(position)position.textContent=String(localIndex+1).padStart(2,"0");if(total)total.textContent=String(intentProducts.length).padStart(2,"0");
      rosterButtons.forEach(function(button){button.setAttribute("aria-pressed",String(button.dataset.universeSelect===product.id));});
      if(announce&&status){var selectedIntent=intentButton(activeIntent);status.textContent=product.name+" selected. Product "+(localIndex+1)+" of "+intentProducts.length+" in "+selectedIntent.dataset.intentName+".";}
      if(transitionAnimation)transitionAnimation.cancel();if(announce&&!reduceMotion&&article.animate)transitionAnimation=article.animate([{opacity:.55,transform:"translateY(10px) scale(.985)"},{opacity:1,transform:"translateY(0) scale(1)"}],{duration:360,easing:"cubic-bezier(.2,.75,.25,1)"});
    }
    function updateIntent(intent){var button=intentButton(intent);if(!button)return;var filteredIds=(root.dataset.universeFilterIds||"").split(",").filter(Boolean);activeIntent=intent;root.dataset.activeIntent=intent;root.dataset.activeEnvironment=button.dataset.intentEnvironment||"signal";intentButtons.forEach(function(item){item.setAttribute("aria-pressed",String(item===button));});if(intentIndex)intentIndex.textContent=button.dataset.intentIndex||"";if(intentName)intentName.textContent=button.dataset.intentName||"";if(intentDescription)intentDescription.textContent=button.dataset.intentDescription||"";rosterButtons.forEach(function(item){item.hidden=item.dataset.productIntent!==intent||(filteredIds.length>0&&filteredIds.indexOf(item.dataset.universeSelect)<0);});}
    function activateProduct(id,announce){var product=products.find(function(item){return item.id===id;});if(!product)return;if(product.intent!==activeIntent)updateIntent(product.intent);renderProduct(product,announce);}
    function activateIntent(button,focus){var candidates=productsForIntent(button.dataset.universeIntent);if(!candidates.length){if(focus)button.focus();return;}updateIntent(button.dataset.universeIntent);var featured=candidates.find(function(product){return product.id===button.dataset.intentFeatured;})||candidates[0];activateProduct(featured.id,true);if(focus)button.focus();}
    function stepProduct(direction){var list=productsForIntent(activeIntent);if(!list.length)return;var index=list.indexOf(activeProduct);if(index<0)index=0;var next=(index+direction+list.length)%list.length;activateProduct(list[next].id,true);}
    intentButtons.forEach(function(button,index){button.addEventListener("click",function(){activateIntent(button,false);});button.addEventListener("keydown",function(event){var next=null;if(event.key==="ArrowRight"||event.key==="ArrowDown")next=(index+1)%intentButtons.length;if(event.key==="ArrowLeft"||event.key==="ArrowUp")next=(index-1+intentButtons.length)%intentButtons.length;if(event.key==="Home")next=0;if(event.key==="End")next=intentButtons.length-1;if(next===null)return;event.preventDefault();activateIntent(intentButtons[next],true);});});
    rosterButtons.forEach(function(button){button.addEventListener("click",function(){activateProduct(button.dataset.universeSelect,true);});});stepButtons.forEach(function(button){button.addEventListener("click",function(){stepProduct(Number(button.dataset.universeStep));});});
    if(stage){stage.addEventListener("touchstart",function(event){touchStartX=event.changedTouches[0].clientX;},{passive:true});stage.addEventListener("touchend",function(event){var distance=event.changedTouches[0].clientX-touchStartX;if(Math.abs(distance)>48)stepProduct(distance<0?1:-1);},{passive:true});if(!reduceMotion&&window.matchMedia("(hover: hover) and (pointer: fine)").matches){stage.addEventListener("pointermove",function(event){var bounds=stage.getBoundingClientRect(),x=((event.clientX-bounds.left)/bounds.width-.5)*2,y=((event.clientY-bounds.top)/bounds.height-.5)*2;stage.style.setProperty("--universe-tilt-x",(y*-2.2).toFixed(2)+"deg");stage.style.setProperty("--universe-tilt-y",(x*3).toFixed(2)+"deg");},{passive:true});stage.addEventListener("pointerleave",function(){stage.style.setProperty("--universe-tilt-x","0deg");stage.style.setProperty("--universe-tilt-y","0deg");},{passive:true});}}
    updateIntent(activeProduct.intent);renderProduct(activeProduct,false);
  }

  document.querySelectorAll("[data-product-universe]").forEach(initProductUniverse);

  function initUniverseDiscovery(form) {
    var root=document.querySelector("[data-product-universe]"), data=root&&root.querySelector("[data-universe-data]");
    if(!root||!data)return; var products=JSON.parse(data.textContent), roster=root.querySelector("[data-universe-roster]");
    var search=form.querySelector("[data-universe-search]"),manufacturer=form.querySelector("[data-universe-manufacturer]"),intent=form.querySelector("[data-universe-intent-filter]"),category=form.querySelector("[data-universe-category]"),sort=form.querySelector("[data-universe-sort]"),status=form.querySelector("[data-universe-results]"),empty=form.querySelector("[data-universe-empty]"),reset=form.querySelector("[data-universe-reset]");
    function apply(){var terms=search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);var matches=products.filter(function(p){var text=[p.name,p.manufacturer,p.category,p.intent,p.productKind,p.variantLabel,p.description].join(" ").toLowerCase();return terms.every(function(t){return text.indexOf(t)>=0;})&&(manufacturer.value==="all"||p.manufacturer===manufacturer.value)&&(intent.value==="all"||p.intent===intent.value)&&(category.value==="all"||p.category===category.value);});
      matches.sort(function(a,b){if(sort.value==="name")return a.name.localeCompare(b.name);if(sort.value==="manufacturer")return a.manufacturer.localeCompare(b.manufacturer)||a.name.localeCompare(b.name);return a.index-b.index;});
      var ids=matches.map(function(p){return p.id;}),buttons=Array.prototype.slice.call(roster.querySelectorAll("[data-universe-select]")),availableIntents=matches.map(function(p){return p.intent;});root.dataset.universeFilterIds=ids.join(",");buttons.forEach(function(b){b.hidden=ids.indexOf(b.dataset.universeSelect)<0;});Array.prototype.slice.call(root.querySelectorAll("[data-universe-intent]")).forEach(function(b){b.disabled=availableIntents.indexOf(b.dataset.universeIntent)<0;});matches.forEach(function(p){var b=roster.querySelector('[data-universe-select="'+p.id+'"]');if(b)roster.appendChild(b);});
      status.textContent="Showing "+matches.length+" of "+products.length+" active products.";empty.hidden=matches.length!==0;root.hidden=matches.length===0;reset.hidden=terms.length===0&&manufacturer.value==="all"&&intent.value==="all"&&category.value==="all"&&sort.value==="canonical";if(matches[0]){var first=roster.querySelector('[data-universe-select="'+matches[0].id+'"]');if(first)first.click();}}
    [search,manufacturer,intent,category,sort].forEach(function(control){control.addEventListener(control===search?"input":"change",apply);});form.addEventListener("reset",function(){window.setTimeout(apply,0);});apply();
  }
  document.querySelectorAll("[data-universe-discovery]").forEach(initUniverseDiscovery);

  function initShopFilters(root) {
    var buttons = Array.prototype.slice.call(root.querySelectorAll("[data-shop-brand]"));
    var products = Array.prototype.slice.call(document.querySelectorAll("[data-shop-product]"));
    var groups = Array.prototype.slice.call(document.querySelectorAll("[data-shop-group]"));
    var status = root.querySelector("[data-shop-filter-status]");
    var search = root.querySelector("[data-shop-search]");
    var sort = root.querySelector("[data-shop-sort]");
    var clear = root.querySelector("[data-shop-clear]");
    var activeManufacturer = "all";
    if (!buttons.length || !products.length) return;
    root.dataset.enhanced = "true";

    function applyFilter(manufacturer, announce) {
      var visibleCount = 0;
      var query = search ? search.value.trim().toLowerCase().replace(/\s+/g, " ") : "";
      var terms = query ? query.split(" ") : [];
      activeManufacturer = manufacturer;
      root.dataset.activeManufacturer = manufacturer;
      buttons.forEach(function (button) {
        var active = button.dataset.shopBrand === manufacturer;
        button.setAttribute("aria-pressed", String(active));
        button.setAttribute("tabindex", active ? "0" : "-1");
      });
      products.forEach(function (product) {
        var brandMatch = manufacturer === "all" || product.dataset.manufacturer === manufacturer;
        var haystack = product.dataset.searchText || "";
        var searchMatch = terms.every(function (term) { return haystack.indexOf(term) !== -1; });
        var visible = brandMatch && searchMatch;
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
      if (status) status.textContent = "Showing " + visibleCount + " of " + products.length + " active products" + (query ? " matching “" + query + "”" : "") + (manufacturer === "all" ? "." : " from " + manufacturer + ".");
      if (clear) clear.hidden = !query && manufacturer === "all" && (!sort || sort.value === "curated");
    }

    function applySort() {
      var mode = sort ? sort.value : "curated";
      groups.forEach(function (group) {
        var grid = group.querySelector(".shop-group__grid");
        if (!grid) return;
        Array.prototype.slice.call(grid.querySelectorAll("[data-shop-product]")).sort(function (left, right) {
          if (mode === "name-asc") return left.dataset.productName.localeCompare(right.dataset.productName);
          if (mode === "manufacturer") return left.dataset.manufacturer.localeCompare(right.dataset.manufacturer) || left.dataset.productName.localeCompare(right.dataset.productName);
          return Number(left.dataset.curatedIndex) - Number(right.dataset.curatedIndex);
        }).forEach(function (product) { grid.appendChild(product); });
      });
      applyFilter(activeManufacturer, true);
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

    if (search) search.addEventListener("input", function () { applyFilter(activeManufacturer, true); });
    if (sort) sort.addEventListener("change", applySort);
    if (clear) clear.addEventListener("click", function () {
      if (search) search.value = "";
      if (sort) sort.value = "curated";
      applySort();
      applyFilter("all", true);
      if (search) search.focus();
    });

    applyFilter("all", false);
  }

  document.querySelectorAll("[data-shop-filter-root]").forEach(initShopFilters);

  function normalize(value) { return String(value || "").trim().toLowerCase().replace(/\s+/g, " "); }
  function htmlSafe(value) { return String(value == null ? "" : value).replace(/[&<>"']/g,function(character){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[character];}); }

  function initMatrixSearch(root) {
    var input=root.querySelector("[data-search-input]"),results=root.querySelector("[data-search-results]"),status=root.querySelector("[data-search-status]"),clear=root.querySelector("[data-search-clear]"),form=root.querySelector("[data-search-form]");
    var modes=Array.prototype.slice.call(root.querySelectorAll("[data-search-mode]")),records=JSON.parse(root.querySelector("[data-search-index]").textContent),mode="everything",prefix=root.dataset.prefix||"";
    function searchable(record){return normalize([record.title,record.summary,record.manufacturer,record.department,record.category,record.productKind,record.variant].concat(record.ingredients||[],record.keywords||[],record.terms||[]).join(" "));}
    function allowed(record){return mode==="everything"||(mode==="products"&&record.type==="product")||(mode==="learn"&&(record.type==="guide"||record.type==="journey"||record.type==="department"));}
    function save(replace){if(!location.pathname.endsWith("explore.html"))return;var params=new URLSearchParams(location.search),q=normalize(input.value);if(q)params.set("q",q);else params.delete("q");if(mode!=="everything")params.set("mode",mode);else params.delete("mode");history[replace?"replaceState":"pushState"]({},"",location.pathname+(params.toString()?"?"+params:""));}
    function resultCard(item){var visual="";if(item.image&&item.image.src)visual='<span class="search-result__visual"><img src="'+prefix+htmlSafe(item.image.src)+'" alt="'+htmlSafe(item.image.alt||"")+'" loading="lazy" decoding="async"></span>';else visual='<span class="search-result__visual search-result__visual--signal" aria-hidden="true"><i></i><i></i><i></i></span>';var meta=item.type==="product"?htmlSafe(item.manufacturer)+" / "+htmlSafe(item.productKind):item.type==="guide"?"Evidence guide"+(item.evidenceReviewed?" / reviewed "+htmlSafe(item.evidenceReviewed):""):item.type==="department"?htmlSafe(item.productCount)+" products / "+htmlSafe(item.guideCount)+" guides":"Guided measurement pathway";return '<li class="search-result search-result--'+htmlSafe(item.type)+'" data-environment="'+htmlSafe(item.environment||item.intent||"matrix")+'"><a href="'+prefix+htmlSafe(item.href)+'">'+visual+'<span class="search-result__content"><b class="search-result__type">'+meta+'</b><strong>'+htmlSafe(item.title)+'</strong><small>'+htmlSafe(item.summary)+'</small><em>Open '+(item.type==="product"?"product details":htmlSafe(item.type))+' →</em></span></a></li>';}
    function render(updateUrl){var query=normalize(input.value),terms=query.split(" ").filter(Boolean);modes.forEach(function(button){button.setAttribute("aria-pressed",String(button.dataset.searchMode===mode));});if(!query){results.hidden=true;results.innerHTML="";status.textContent="Enter a term or browse the departments below.";clear.hidden=true;if(updateUrl)save(true);return;}
      var matches=records.filter(function(record){var text=searchable(record);return allowed(record)&&terms.every(function(term){return text.indexOf(term)>=0;});}).slice(0,24);var groups=[{id:"product",label:"Products"},{id:"guide",label:"Learn"},{id:"journey",label:"Journeys"},{id:"department",label:"Departments"}];var html=[];groups.forEach(function(group){var items=matches.filter(function(item){return item.type===group.id;});if(!items.length)return;html.push('<section aria-labelledby="search-group-'+group.id+'"><h3 id="search-group-'+group.id+'"><span class="signal-node" aria-hidden="true"></span>'+group.label+'</h3><ul>'+items.map(resultCard).join("")+'</ul></section>');});results.innerHTML=html.join("")||'<div class="search-empty"><span aria-hidden="true"></span><p>No verified products or education match this search.</p><small>Try a product, department, ingredient, or guide title.</small></div>';results.hidden=false;status.textContent=matches.length+" result"+(matches.length===1?"":"s")+" for “"+query+"”.";clear.hidden=false;if(updateUrl)save(true);}
    modes.forEach(function(button){button.addEventListener("click",function(){mode=button.dataset.searchMode;render(true);});});input.addEventListener("input",function(){render(true);});clear.addEventListener("click",function(){input.value="";render(true);input.focus();});form.addEventListener("submit",function(event){if(location.pathname.endsWith("explore.html")){event.preventDefault();render(false);}});root.addEventListener("keydown",function(event){if(event.key==="Escape"&&!results.hidden){input.value="";render(true);input.focus();}});
    function restore(){var params=new URLSearchParams(location.search);input.value=params.get("q")||"";mode=["everything","products","learn"].indexOf(params.get("mode"))>=0?params.get("mode"):"everything";render(false);}window.addEventListener("popstate",restore);restore();
  }
  document.querySelectorAll("[data-matrix-search]").forEach(initMatrixSearch);

  function initExplore(root){var cards=Array.prototype.slice.call(root.querySelectorAll("[data-discovery-product]")),controls={manufacturer:root.querySelector('[data-filter="manufacturer"]'),intent:root.querySelector('[data-filter="intent"]'),category:root.querySelector('[data-filter="category"]'),sort:root.querySelector('[data-filter="sort"]')},count=root.querySelector("[data-explore-count]"),empty=root.querySelector("[data-explore-empty]"),load=root.querySelector("[data-load-more]"),reset=root.querySelector("[data-filter-reset]"),chips=root.querySelector("[data-filter-chips]"),limit=12;
    function apply(update){var matches=cards.filter(function(card){return (controls.manufacturer.value==="all"||card.dataset.manufacturer===controls.manufacturer.value)&&(controls.intent.value==="all"||card.dataset.intent===controls.intent.value)&&(controls.category.value==="all"||card.dataset.category===controls.category.value);});matches.sort(function(a,b){if(controls.sort.value==="name")return a.dataset.name.localeCompare(b.dataset.name);if(controls.sort.value==="manufacturer-sort")return a.dataset.manufacturer.localeCompare(b.dataset.manufacturer)||a.dataset.name.localeCompare(b.dataset.name);return Number(a.dataset.order)-Number(b.dataset.order);});matches.forEach(function(card){card.parentNode.appendChild(card);});cards.forEach(function(card){var index=matches.indexOf(card);card.hidden=index<0||index>=limit;});count.textContent="Showing "+Math.min(limit,matches.length)+" of "+matches.length+" matching products ("+cards.length+" active total).";empty.hidden=matches.length!==0;load.hidden=matches.length<=limit;reset.hidden=!Object.keys(controls).some(function(key){return controls[key].value!==(key==="sort"?"canonical":"all");});chips.textContent=Object.keys(controls).filter(function(key){return key!=="sort"&&controls[key].value!=="all";}).map(function(key){return controls[key].selectedOptions[0].text;}).join(" · ");if(update){var p=new URLSearchParams(location.search);Object.keys(controls).forEach(function(key){var value=controls[key].value,defaultValue=key==="sort"?"canonical":"all";if(value!==defaultValue)p.set(key==="intent"?"department":key,value);else p.delete(key==="intent"?"department":key);});history.replaceState({},"",location.pathname+(p.toString()?"?"+p:""));}}
    var params=new URLSearchParams(location.search);controls.manufacturer.value=params.get("manufacturer")||"all";controls.intent.value=params.get("department")||"all";controls.category.value=params.get("category")||"all";controls.sort.value=params.get("sort")||"canonical";Object.keys(controls).forEach(function(key){controls[key].addEventListener("change",function(){limit=12;apply(true);});});load.addEventListener("click",function(){limit+=12;apply(false);});reset.addEventListener("click",function(){controls.manufacturer.value="all";controls.intent.value="all";controls.category.value="all";controls.sort.value="canonical";limit=12;apply(true);});window.addEventListener("popstate",function(){location.reload();});apply(false);
  }
  var exploreRoot=document.querySelector(".explore-results");if(exploreRoot)initExplore(exploreRoot);

  var matrixVisuals=Array.prototype.slice.call(document.querySelectorAll("[data-matrix-visual]"));
  function syncMatrixVisuals(){matrixVisuals.forEach(function(visual){visual.dataset.visualRunning=String(!document.hidden&&visual.dataset.visualVisible!=="false");});}
  if(matrixVisuals.length){if("IntersectionObserver" in window){var visualObserver=new IntersectionObserver(function(entries){entries.forEach(function(entry){entry.target.dataset.visualVisible=String(entry.isIntersecting);});syncMatrixVisuals();},{rootMargin:"80px",threshold:.01});matrixVisuals.forEach(function(visual){visualObserver.observe(visual);});}document.addEventListener("visibilitychange",syncMatrixVisuals);syncMatrixVisuals();}

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
