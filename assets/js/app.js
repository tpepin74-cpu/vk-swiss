/* VK Swiss — panier, conseiller (arbre de décision), header, mobile app */
(function () {
  "use strict";
  var D = window.VK || {};
  var BASE = document.documentElement.getAttribute("data-base") || "";
  var TEL = "+41792890449", TEL_TXT = "+41 79 289 04 49";
  var FREE = 80;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var chf = function (n) { return "CHF " + n.toFixed(2); };

  /* ---------- Storage (sécurisé) ---------- */
  function load() { try { return JSON.parse(localStorage.getItem("vk_cart") || "[]"); } catch (e) { return []; } }
  function save(c) { try { localStorage.setItem("vk_cart", JSON.stringify(c)); } catch (e) {} }
  var cart = load();

  function prod(slug) { return (D.products || []).filter(function (p) { return p.slug === slug; })[0]; }
  function lineKey(l) { return l.slug + "|" + (l.sub ? "s" : "u"); }
  function unit(l) { var p = prod(l.slug); if (!p) return 0; return l.sub ? p.price * 0.85 : p.price; }
  function totals() {
    var sub = 0, n = 0;
    cart.forEach(function (l) { sub += unit(l) * l.q; n += l.q; });
    var ship = sub === 0 || sub >= FREE ? 0 : 7;
    return { sub: sub, n: n, ship: ship, total: sub + ship };
  }
  function add(slug, q, sub) {
    q = q || 1; var k = slug + "|" + (sub ? "s" : "u"), found = false;
    cart.forEach(function (l) { if (lineKey(l) === k) { l.q += q; found = true; } });
    if (!found) cart.push({ slug: slug, q: q, sub: !!sub });
    save(cart); render();
    var p = prod(slug);
    toast((p ? p.name : "Produit") + " ajouté au panier", true);
  }
  function setQ(k, q) {
    cart = cart.filter(function (l) { if (lineKey(l) === k) l.q = q; return l.q > 0; });
    save(cart); render();
  }

  /* ---------- Render cart ---------- */
  function render() {
    var t = totals();
    $$("[data-cart-count]").forEach(function (b) { b.textContent = t.n; b.setAttribute("data-n", t.n); });
    $$("[data-cart-lines]").forEach(function (box) {
      if (!cart.length) { box.innerHTML = '<p class="empty">Votre panier est vide.<br><a class="link" href="' + BASE + 'boutique.html">Découvrir la collection</a></p>'; return; }
      box.innerHTML = cart.map(function (l) {
        var p = prod(l.slug); if (!p) return "";
        var k = lineKey(l);
        return '<div class="line"><img src="' + BASE + p.img + '" alt="" width="76" height="76"><div><h4>' + p.name + '</h4><small>' + (l.sub ? "Abonnement mensuel −15 %" : "Achat unique") + '</small><div style="margin-top:8px" class="qty"><button type="button" aria-label="Retirer un" data-q="' + k + '" data-d="-1">−</button><input aria-label="Quantité" value="' + l.q + '" readonly><button type="button" aria-label="Ajouter un" data-q="' + k + '" data-d="1">+</button></div></div><strong>' + chf(unit(l) * l.q) + '</strong></div>';
      }).join("");
    });
    var left = Math.max(0, FREE - t.sub);
    $$("[data-ship-msg]").forEach(function (e) { e.textContent = t.sub === 0 ? "Livraison offerte dès " + chf(FREE) : left > 0 ? "Plus que " + chf(left) + " pour la livraison offerte" : "La livraison vous est offerte"; });
    $$("[data-ship-bar]").forEach(function (e) { e.style.width = Math.min(100, t.sub / FREE * 100) + "%"; });
    $$("[data-sub]").forEach(function (e) { e.textContent = chf(t.sub); });
    $$("[data-shipping]").forEach(function (e) { e.textContent = t.ship ? chf(t.ship) : "Offerte"; });
    $$("[data-total]").forEach(function (e) { e.textContent = chf(t.total); });
    $$("[data-has-items]").forEach(function (e) { e.hidden = !cart.length; });
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-q]");
    if (b) { var k = b.getAttribute("data-q"); cart.forEach(function (l) { if (lineKey(l) === k) setQ(k, l.q + (+b.getAttribute("data-d"))); }); }
    var a = e.target.closest("[data-add]");
    if (a) {
      e.preventDefault();
      var slug = a.getAttribute("data-add");
      var form = a.closest("[data-buy]");
      var q = 1, sub = false;
      if (form) { var qi = $("[data-qty]", form); q = qi ? Math.max(1, parseInt(qi.value, 10) || 1) : 1; var s = $('input[name="mode"]:checked', form); sub = s && s.value === "sub"; }
      add(slug, q, sub);
      if (a.hasAttribute("data-open")) openCart();
    }
    if (e.target.closest("[data-cart-open]")) { e.preventDefault(); openCart(); }
    if (e.target.closest("[data-cart-close]")) closeCart();
    var ex = e.target.closest("[data-express]");
    if (ex) { var f = ex.closest("form"), ok = f && f.querySelector("[data-ok]"); if (ok) { ok.hidden = false; ok.focus(); } }
    var st = e.target.closest("[data-step]");
    if (st) { var i = $("[data-qty]", st.closest("[data-buy]") || document); if (i) i.value = Math.max(1, (parseInt(i.value, 10) || 1) + (+st.getAttribute("data-step"))); updateBuy(); }
  });

  /* ---------- Drawer ---------- */
  var drawer = $("#cart"), lastFocus = null;
  function openCart() { if (!drawer) return; lastFocus = document.activeElement; drawer.classList.add("is-open"); drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false"); var c = $("[data-cart-close]", drawer); c && c.focus(); }
  function closeCart() { if (!drawer) return; drawer.classList.remove("is-open"); drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true"); lastFocus && lastFocus.focus && lastFocus.focus(); }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeCart(); closeAst(); } });

  /* ---------- Toast ---------- */
  var tEl = $("#toast"), tT;
  function toast(msg, withCart) {
    if (!tEl) return;
    tEl.innerHTML = "<span>" + msg + "</span>" + (withCart ? '<a href="' + BASE + 'panier.html">Commander</a>' : "");
    tEl.classList.add("is-on"); clearTimeout(tT); tT = setTimeout(function () { tEl.classList.remove("is-on"); }, 3200);
  }

  /* ---------- Fiche produit : prix dynamique ---------- */
  function updateBuy() {
    $$("[data-buy]").forEach(function (f) {
      var p = prod(f.getAttribute("data-buy")); if (!p) return;
      var q = Math.max(1, parseInt(($("[data-qty]", f) || {}).value, 10) || 1);
      var s = $('input[name="mode"]:checked', f); var sub = s && s.value === "sub";
      var v = (sub ? p.price * 0.85 : p.price) * q;
      $$("[data-buy-total]").forEach(function (e) { e.textContent = chf(v); });
    });
  }
  document.addEventListener("change", function (e) { if (e.target.name === "mode" || e.target.hasAttribute("data-qty")) updateBuy(); });

  /* ---------- Filtres boutique ---------- */
  $$("[data-filter]").forEach(function (b) {
    b.addEventListener("click", function () {
      var v = b.getAttribute("data-filter");
      $$("[data-filter]").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      $$("[data-intent]").forEach(function (t) { t.hidden = v !== "all" && t.getAttribute("data-intent") !== v; });
    });
  });
  var h = location.hash.replace("#", "");
  if (h) { var fb = $('[data-filter="' + h + '"]'); fb && fb.click(); }

  /* ---------- Points de vente : recherche ---------- */
  var sq = $("#store-q"), sc = $("#store-canton");
  function filterStores() {
    var q = (sq && sq.value || "").toLowerCase().trim(), c = sc && sc.value || "";
    $$("[data-store]").forEach(function (s) { s.hidden = (c && s.getAttribute("data-canton") !== c) || (q && s.textContent.toLowerCase().indexOf(q) < 0); });
    $$("[data-canton-title]").forEach(function (t) { t.hidden = c && t.getAttribute("data-canton-title") !== c; });
  }
  sq && sq.addEventListener("input", filterStores); sc && sc.addEventListener("change", filterStores);

  /* ---------- Header transparent sur hero ---------- */
  var hdr = $(".hdr--over"), mt = $(".m-top--over");
  function onScroll() { var y = window.scrollY > 60; hdr && hdr.classList.toggle("is-solid", y); mt && mt.classList.toggle("is-solid", y); }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* ---------- Vidéo hero : pause accessible + économie data ---------- */
  var v = $(".hero video"), pb = $(".hero__pause");
  if (v) {
    var lowData = navigator.connection && navigator.connection.saveData;
    if (lowData || matchMedia("(prefers-reduced-motion: reduce)").matches) { v.removeAttribute("autoplay"); v.pause(); }
    pb && pb.addEventListener("click", function () { if (v.paused) { v.play(); pb.setAttribute("aria-label", "Mettre la vidéo en pause"); } else { v.pause(); pb.setAttribute("aria-label", "Lire la vidéo"); } });
  }

  /* ---------- Apparition au scroll ---------- */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } }); }, { rootMargin: "0px 0px -8% 0px" });
    $$(".rv").forEach(function (el) { io.observe(el); });
  } else { $$(".rv").forEach(function (el) { el.classList.add("in"); }); }

  /* ---------- Formulaires (démo maquette) ---------- */
  var params = new URLSearchParams(location.search);
  var subj = $("#form-field-sujet"); if (subj && params.get("sujet")) subj.value = params.get("sujet");
  var msg = $("#form-field-message"); if (msg && params.get("msg")) msg.value = params.get("msg");
  $$("form[data-demo]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!f.checkValidity()) { f.reportValidity(); return; }
      var ok = f.querySelector("[data-ok]"); if (ok) { ok.hidden = false; ok.focus(); }
      if (f.hasAttribute("data-checkout")) { cart = []; save(cart); render(); }
      f.querySelectorAll("input,textarea,select,button").forEach(function (x) { if (!x.closest("[data-ok]")) x.disabled = true; });
    });
  });

  /* ---------- Conseiller VK : arbre de décision ---------- */
  var ast = $("#ast"), body = ast && $(".ast__body", ast), hist = [];
  var T = D.tree || {};
  function openAst() { if (!ast) return; ast.classList.add("is-open"); ast.removeAttribute("inert"); ast.setAttribute("aria-hidden", "false"); if (!hist.length) go("start"); $$("[data-ast-open]").forEach(function (b) { b.setAttribute("aria-expanded", "true"); }); }
  function closeAst() { if (!ast) return; ast.classList.remove("is-open"); ast.setAttribute("inert", ""); ast.setAttribute("aria-hidden", "true"); $$("[data-ast-open]").forEach(function (b) { b.setAttribute("aria-expanded", "false"); }); }
  function link(u) { return /^(https?:|tel:|mailto:)/.test(u) ? u : BASE + u; }
  function mailUrl(topic) { return BASE + "contact.html?sujet=" + encodeURIComponent(topic || "Demande de conseil") + "#formulaire"; }
  function go(id, label) {
    var n = T[id]; if (!n || !body) return;
    if (label) { var y = document.createElement("p"); y.className = "ast__you"; y.textContent = label; body.appendChild(y); }
    hist.push(id);
    var m = document.createElement("div"); m.className = "ast__msg"; m.innerHTML = n.text; body.appendChild(m);
    var o = document.createElement("div"); o.className = "ast__opts";
    (n.links || []).forEach(function (l) { var a = document.createElement("a"); a.href = link(l[1]); a.className = "go"; a.innerHTML = "<span>" + l[0] + "</span><span aria-hidden=\"true\">→</span>"; o.appendChild(a); });
    (n.opts || []).forEach(function (op) { var b = document.createElement("button"); b.type = "button"; b.innerHTML = "<span>" + op[0] + "</span><span aria-hidden=\"true\">›</span>"; b.addEventListener("click", function () { $$("button", o).forEach(function (x) { x.disabled = true; }); go(op[1], op[0]); }); o.appendChild(b); });
    if (id !== "start") { var r = document.createElement("button"); r.type = "button"; r.className = "ast__back"; r.textContent = "↺ Revenir au début"; r.addEventListener("click", function () { body.innerHTML = ""; hist = []; go("start"); }); o.appendChild(r); }
    body.appendChild(o);
    var mail = $("[data-ast-mail]", ast); if (mail) mail.href = mailUrl(n.topic);
    setTimeout(function () { body.scrollTop = body.scrollHeight; }, 30);
  }
  $$("[data-ast-open]").forEach(function (b) { b.addEventListener("click", function (e) { e.preventDefault(); ast && ast.classList.contains("is-open") ? closeAst() : openAst(); }); });
  $$("[data-ast-close]").forEach(function (b) { b.addEventListener("click", closeAst); });
  if (location.hash === "#conseiller") openAst();

  /* ---------- PWA ---------- */
  if ("serviceWorker" in navigator && location.protocol === "https:") { navigator.serviceWorker.register(BASE + "sw.js").catch(function () {}); }

  render(); updateBuy();
})();
