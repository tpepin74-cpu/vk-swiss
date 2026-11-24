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

  /* ---------- Film publicitaire ---------- */
  var pub = $("#pub");
  var vtt = $("#pub-vtt");
  if (pub && vtt) { try { var tr = document.createElement("track"); tr.kind = "captions"; tr.srclang = "fr"; tr.label = "Français"; tr.default = true;
    tr.src = URL.createObjectURL(new Blob([vtt.textContent.trim() + "\n"], { type: "text/vtt" })); pub.appendChild(tr); } catch (e) {} }
  if (pub) {
    var fr = pub.parentNode;
    $$("[data-film-play]").forEach(function (b) { b.addEventListener("click", function () { pub.muted = false; pub.play(); }); });
    pub.addEventListener("play", function () { fr.classList.add("is-playing"); if (v && !v.paused) v.pause(); });
    pub.addEventListener("pause", function () { fr.classList.remove("is-playing"); });
    pub.addEventListener("ended", function () { fr.classList.remove("is-playing"); });
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

  /* ---------- Conseiller VK : chatbot basé sur les contenus du site (100 % local, sans IA externe) ---------- */
  var ast = $("#ast"), body = ast && $(".ast__body", ast), form = ast && $("[data-ast-form]", ast), started = false;
  var KB = D.kb || [], STORES = D.stores || [];
  var STOP = "a au aux avec ce ces c cela comme dans de des du elle en est et etre il ils je j l la le les leur lui ma mais me mes moi mon ne nos notre nous on ou par pas pour qu que qui sa se ses son sur ta te tes toi ton tu un une vos votre vous y d s n m t est-ce quoi bonjour salut merci svp stp peut peux puis faut avoir fait faire bien tres plus quel quelle quels quelles comment pourquoi contre mal marche devenir travail boulot veux voudrais aimerais souhaite cherche besoin savoir dire il elle fait-il est-ce qu ca cest ai suis es sont avez".split(" ");
  var SYN = { fatigue: "energie", fatigu: "energie", creve: "energie", epuis: "energie", tonus: "energie", vitalit: "energie",
    stress: "stress", stresse: "stress", angoiss: "anxiete", calm: "calme", dorm: "sommeil", dors: "sommeil", dodo: "sommeil", reveil: "sommeil", insomni: "sommeil",
    memoir: "memoire", concentr: "concentration", exam: "examen", etud: "etude",
    femm: "femme", regl: "regles", menopaus: "menopause", homm: "homme", libid: "libido", muscl: "muscle",
    enceint: "enceinte", allait: "allaitement", grosses: "grossesse", medic: "medicament", traitem: "traitement",
    cout: "prix", tarif: "prix", combien: "prix", cher: "prix", achet: "acheter", command: "commander",
    livr: "livraison", envoi: "livraison", expedi: "livraison", colis: "livraison", port: "livraison",
    pay: "paiement", paie: "paiement", carte: "carte", twint: "twint", paypal: "paypal",
    pharma: "pharmacie", drogu: "droguerie", magasin: "pharmacie", trouv: "pharmacie", acheter: "acheter",
    compos: "composition", ingredi: "ingredient", conti: "contient", allerg: "allergene", lactos: "lactose",
    abonn: "abonnement", resili: "resilier", prend: "prendre", pris: "prise", dose: "dose", posolog: "posologie",
    ashwa: "ashwagandha", ashvagandha: "ashwagandha", withania: "ashwagandha", shila: "shilajit", brahmi: "bacopa", bacop: "bacopa",
    shatav: "shatavari", tribul: "tribulus", curcum: "curcuma", turmeric: "curcuma", piperin: "curcuma", poivr: "curcuma",
    vegan: "vegan", vegetal: "vegetalien", vegetari: "vegetarien" };
  function norm(t) { return (t || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9\s-]/g, " "); }
  var EXACT = { pharmacien: "revendeur", pharmaciens: "revendeur", pharmacienne: "revendeur", droguiste: "revendeur", revendre: "revendeur", revendeurs: "revendeur", vendre: "revendeur" };
  function toks(t) {
    return norm(t).split(/[\s-]+/).filter(function (w) { return w.length > 1 && STOP.indexOf(w) < 0; }).map(function (w) {
      if (EXACT[w]) return EXACT[w];
      for (var k in SYN) { if (w.indexOf(k) === 0) return SYN[k]; }
      return w.length > 4 ? w.replace(/(es|s|x)$/, "") : w;
    });
  }
  // index TF-IDF léger
  var DOCS = KB.map(function (e) { var m = {}; toks(e.k).forEach(function (w) { m[w] = 1; }); toks(e.t).forEach(function (w) { m[w] = 1.6; }); return m; });
  var DF = {}; DOCS.forEach(function (m) { for (var w in m) DF[w] = (DF[w] || 0) + 1; });
  function idf(w) { return Math.log(1 + KB.length / (DF[w] || 0.5)); }
  function prefixHit(m, w) { if (m[w]) return m[w]; if (w.length < 5) return 0; for (var k in m) { if (k.length > 4 && (k.indexOf(w.slice(0, 5)) === 0)) return 0.6; } return 0; }
  var PRODS = (D.products || []).map(function (p) { return p.slug; });
  var ASPECT = { compo: ["composition", "ingredient", "contient", "allergene", "lactose", "gelatine", "mg", "dosage", "vegan"],
    prec: ["precaution", "anticoagulant", "interaction", "compatible", "pilule", "contraception", "effet", "enceinte", "allaitement", "grossesse", "traitement", "medicament", "danger", "risque", "contre", "secondaire", "enfant", "deconseille"],
    usage: ["prendre", "prise", "dose", "posologie", "quand", "moment", "matin", "soir", "duree", "cure", "gelule"],
    prix: ["prix", "acheter", "commander", "abonnement", "chf"] };
  var GREET = ["bonjour", "salut", "hello", "bonsoir", "coucou", "hey", "merci", "aide", "aidez"];
  function answer(q) {
    var raw = norm(q).split(/\s+/).filter(Boolean);
    if (raw.length && raw.length <= 4 && raw.every(function (w) { return GREET.indexOf(w) >= 0 || STOP.indexOf(w) >= 0 || w.length < 3; })) return KB.filter(function (e) { return e.id === "hello"; });
    var qt = toks(q); if (!qt.length) return null;
    // 1) produit + facette
    var prod = PRODS.filter(function (s) { return qt.indexOf(s) >= 0; })[0];
    if (prod) {
      var asp = "info";
      for (var a in ASPECT) { if (qt.some(function (w) { return ASPECT[a].indexOf(w) >= 0; })) { asp = a; break; } }
      var hit = KB.filter(function (e) { return e.p === prod && e.x === asp; })[0];
      if (hit) return [hit];
    }
    // 2) recherche de pharmacie par ville / NPA
    var wantsStore = qt.some(function (w) { return ["pharmacie", "droguerie", "point", "vente", "pres", "proche", "ou", "trouver", "magasin"].indexOf(w) >= 0; });
    var nq = norm(q), places = [];
    STORES.forEach(function (s) {
      var addr = norm(s[1]).trim(); var m = addr.match(/\b(\d{4})\s+([a-z\s'-]+)$/);
      var city = m ? m[2].trim() : "", npa = m ? m[1] : "";
      var wb = function (t) { return new RegExp('(^|\\s)' + t.replace(/[-']/g, ' ').trim() + '(\\s|$)').test(nq.replace(/[-']/g, ' ')); };
      if ((city && city.length > 2 && wb(city)) || (npa && wb(npa)) || wb(norm(s[2]))) places.push(s);
    });
    if (places.length) return [{ store: places, t: "Points de vente" }];
    var healthWords = ["medicament", "traitement", "maladie", "diabete", "tension", "hypertension", "cancer", "medecin", "soigner", "guerir", "symptome", "douleur"];
    var hEntry = KB.filter(function (e) { return e.id === "sante"; })[0];
    if (hEntry && !prod && qt.some(function (w) { return healthWords.indexOf(w) >= 0; })) return [hEntry];
    // 3) score TF-IDF + couverture de la question
    var qmax = qt.reduce(function (t, w) { return t + idf(w); }, 0);
    var scored = KB.map(function (e, i) {
      var sc = 0, cov = 0; qt.forEach(function (w) { var h = prefixHit(DOCS[i], w); if (h) { sc += h * idf(w); cov += idf(w); } });
      if (prod && e.p === prod) sc += 2;
      return { e: e, sc: sc, cov: qmax ? cov / qmax : 0 };
    }).sort(function (x, y) { return y.sc - x.sc; });
    var top = scored[0];
    if (wantsStore && (!top || top.cov < 0.6)) return [{ store: [], t: "Points de vente" }];
    if (!top || top.sc < 1.2 || top.cov < 0.55) return null;
    var res = [top.e];
    if (scored[1] && scored[1].sc > top.sc * 0.85 && scored[1].cov >= 0.55 && scored[1].e.p !== top.e.p) res.push(scored[1].e);
    // une question de santé commence toujours par l'avertissement
    var health = KB.filter(function (e) { return e.id === "sante"; })[0];
    if (health && qt.some(function (w) { return ["medicament", "traitement", "maladie", "diabete", "tension", "hypertension", "cancer", "medecin", "soigner", "guerir"].indexOf(w) >= 0; })) {
      res = res.filter(function (e) { return e !== health && e.id !== "resultat"; }); res.unshift(health);
    }
    return res;
  }
  function linkTo(u) { return /^(https?:|tel:|mailto:)/.test(u) ? u : BASE + u; }
  function mailUrl(topic, q) { return BASE + "contact.html?sujet=" + encodeURIComponent(topic || "Demande de conseil") + (q ? "&msg=" + encodeURIComponent(q) : "") + "#formulaire"; }
  function bubble(cls, html) { var d = document.createElement("div"); d.className = cls; d.innerHTML = html; body.appendChild(d); return d; }
  function esc(t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function scroll() { setTimeout(function () { body.scrollTop = body.scrollHeight; }, 30); }
  function chips(list) {
    var o = document.createElement("div"); o.className = "ast__chips";
    list.forEach(function (t) { var b = document.createElement("button"); b.type = "button"; b.textContent = t; b.addEventListener("click", function () { ask(t); }); o.appendChild(b); });
    body.appendChild(o);
  }
  function reply(q) {
    var res = answer(q), mail = $("[data-ast-mail]", ast);
    if (!res) {
      bubble("ast__msg", "Je n'ai pas trouvé de réponse précise dans nos contenus. Un membre de l'équipe VK Swiss vous répond personnellement : appelez-nous ou envoyez votre question, elle est déjà pré-remplie.");
      var o = document.createElement("div"); o.className = "ast__opts";
      o.innerHTML = '<a class="go" href="' + mailUrl("Question au conseiller", q) + '"><span>Envoyer ma question par e-mail</span><span aria-hidden="true">→</span></a><a href="tel:' + TEL + '"><span>Appeler le ' + TEL_TXT + '</span><span aria-hidden="true">›</span></a>';
      body.appendChild(o); if (mail) mail.href = mailUrl("Question au conseiller", q); scroll(); return;
    }
    res.forEach(function (e) {
      if (e.store) {
        if (!e.store.length) { bubble("ast__msg", "Indiquez-moi votre ville ou votre NPA (par ex. « pharmacie à Sion » ou « 2900 ») et je vous donne les points de vente les plus proches. Plus de 120 pharmacies et drogueries proposent VK Swiss en Suisse."); }
        else {
          var h = "<strong>" + e.store.length + " point" + (e.store.length > 1 ? "s" : "") + " de vente trouvé" + (e.store.length > 1 ? "s" : "") + " :</strong><ul class=\"ast__list\">" + e.store.slice(0, 6).map(function (s) { return "<li><strong>" + esc(s[0]) + "</strong><br>" + esc(s[1]) + "</li>"; }).join("") + "</ul>";
          bubble("ast__msg", h);
        }
        var o2 = document.createElement("div"); o2.className = "ast__opts"; o2.innerHTML = '<a class="go" href="' + BASE + 'points-de-vente.html"><span>Voir tous les points de vente</span><span aria-hidden="true">→</span></a>'; body.appendChild(o2);
        if (mail) mail.href = mailUrl("Point de vente", q);
        return;
      }
      bubble("ast__msg", e.a);
      if (e.l && e.l.length) { var o = document.createElement("div"); o.className = "ast__opts"; e.l.forEach(function (l) { var a = document.createElement("a"); a.href = linkTo(l[1]); a.className = "go"; a.innerHTML = "<span>" + esc(l[0]) + "</span><span aria-hidden=\"true\">→</span>"; o.appendChild(a); }); body.appendChild(o); }
      if (mail) mail.href = mailUrl(e.topic, q);
    });
    bubble("ast__hint", "Une autre question ? Écrivez-la ci-dessous, ou contactez-nous directement.");
    scroll();
  }
  function ask(q) {
    q = (q || "").trim(); if (!q || !body) return;
    $$(".ast__chips", body).forEach(function (c) { c.remove(); });
    var y = document.createElement("p"); y.className = "ast__you"; y.textContent = q; body.appendChild(y);
    var typing = bubble("ast__typing", "<i></i><i></i><i></i>"); typing.setAttribute("aria-label", "Le conseiller écrit");
    scroll();
    setTimeout(function () { typing.remove(); reply(q); }, 450 + Math.min(700, q.length * 12));
  }
  function start() {
    if (started || !body) return; started = true;
    bubble("ast__msg", "Bonjour, je suis le <strong>conseiller VK Swiss</strong>. Posez-moi votre question sur nos formules, le ghee, les précautions, la livraison ou nos pharmacies : je réponds à partir des contenus du site.");
    chips(D.suggest || []);
  }
  function openAst() { if (!ast) return; ast.classList.add("is-open"); ast.removeAttribute("inert"); ast.setAttribute("aria-hidden", "false"); start(); $$("[data-ast-open]").forEach(function (b) { b.setAttribute("aria-expanded", "true"); }); var i = $("#ast-q"); if (i && matchMedia("(min-width: 861px)").matches) i.focus(); }
  function closeAst() { if (!ast) return; ast.classList.remove("is-open"); ast.setAttribute("inert", ""); ast.setAttribute("aria-hidden", "true"); $$("[data-ast-open]").forEach(function (b) { b.setAttribute("aria-expanded", "false"); }); }
  form && form.addEventListener("submit", function (e) { e.preventDefault(); var i = $("#ast-q"); ask(i.value); i.value = ""; });
  $$("[data-ast-open]").forEach(function (b) { b.addEventListener("click", function (e) { e.preventDefault(); ast && ast.classList.contains("is-open") ? closeAst() : openAst(); }); });
  $$("[data-ast-close]").forEach(function (b) { b.addEventListener("click", closeAst); });
  if (location.hash === "#conseiller") openAst();

  /* ---------- PWA ---------- */
  if ("serviceWorker" in navigator && location.protocol === "https:") { navigator.serviceWorker.register(BASE + "sw.js").catch(function () {}); }

  render(); updateBuy();
})();
