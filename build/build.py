# -*- coding: utf-8 -*-
"""Générateur statique du site VK Swiss (maquette HTML avant reconstruction WordPress/Elementor Pro)."""
import json, os, html
from data import SITE, PRODUCTS, FAQ, STORES

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
U = SITE["url"]
PRICE = SITE["price"]
for p in PRODUCTS:
    p["price"] = PRICE
    p["img"] = "assets/img/pack-%s.jpg" % p["slug"]
    p["ing"] = "assets/img/ing-%s.jpg" % p["slug"]
    p["url"] = "produits/%s.html" % p["slug"]

def e(s): return html.escape(s, quote=True)
def chf(n): return "CHF %.2f" % n

ICONS = {
 "search": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>',
 "user": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>',
 "bag": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 8h14l-1.2 12H6.2z"/><path d="M9 8V6a3 3 0 016 0v2"/></svg>',
 "home": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/></svg>',
 "grid": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="7" height="7"/><rect x="13" y="4" width="7" height="7"/><rect x="4" y="13" width="7" height="7"/><rect x="13" y="13" width="7" height="7"/></svg>',
 "chat": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z"/><path d="M8 10h8M8 13h5"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.5-7-12a7 7 0 0114 0c0 5.5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/></svg>',
 "close": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
 "truck": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 6h12v10H2zM14 10h4l3 3v3h-7"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/></svg>',
 "lock": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="11" width="14" height="10"/><path d="M8 11V8a4 4 0 018 0v3"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 005 5L15 12l5 2v4a2 2 0 01-2 2A16 16 0 013 5a2 2 0 012-2z"/></svg>',
 "mountain": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 20l7-12 4 6 3-4 6 10z"/></svg>',
 "leaf": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15"/><path d="M5 19l8-8"/></svg>',
 "check": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>',
 "pause": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6v12M15 6v12"/></svg>',
}

PAY = '<div class="pay" aria-label="Moyens de paiement acceptés"><span class="twint">TWINT</span><span>VISA</span><span>Mastercard</span><span>AMEX</span><span>Apple&nbsp;Pay</span><span>Google&nbsp;Pay</span><span>PayPal</span><span>PostFinance</span></div>'

NAV = [("boutique.html","La collection","boutique"),("maison.html","La Maison","maison"),("ayurveda.html","Ayurvéda & ghee","ayurveda"),("points-de-vente.html","Points de vente","pdv"),("contact.html","Contact","contact")]

# ---------------- Arbre du conseiller ----------------
def ptxt(slug):
    p = [x for x in PRODUCTS if x["slug"] == slug][0]
    return p
TREE = {
 "start": {"text": "Bonjour, je suis le <strong>conseiller VK Swiss</strong>. Choisissez votre question, je vous guide vers la bonne réponse.",
           "opts": [["Choisir ma formule","choisir"],["Comprendre le ghee suisse","ghee"],["Utilisation & précautions","usage"],["Commande, paiement, livraison","commande"],["Trouver une pharmacie","pdv"],["Je suis pharmacien / revendeur","pro"],["Parler à quelqu'un","humain"]], "topic":"Demande de conseil"},
 "choisir": {"text":"Quelle intention souhaitez-vous accompagner au quotidien ?",
             "opts":[["Énergie & vitalité","f_shilajit"],["Clarté & concentration","f_bacopa"],["Calme & sérénité","f_ashwagandha"],["Bien-être féminin","f_shatavari"],["Vitalité masculine","f_tribulus"],["Un rituel quotidien, digestion","f_curcuma"],["Je ne sais pas encore","hesite"]], "topic":"Choix d'une formule"},
 "hesite": {"text":"Aucun souci. Chaque formule associe une plante ayurvédique à du ghee suisse, à raison d'une gélule par jour. Le plus simple : en parler 5 minutes avec nous, ou découvrir la collection classée par intention.",
            "links":[["Voir la collection par intention","boutique.html"],["Lire le guide : bien choisir sa formule","ayurveda.html#choisir"]], "topic":"Aide au choix d'une formule"},
 "ghee": {"text":"Le ghee est un beurre clarifié : on retire l'eau et les protéines du lait pour ne garder qu'une matière grasse pure et dorée. En ayurvéda, il accompagne traditionnellement les plantes. Le nôtre est produit en Suisse, à partir de lait suisse.",
          "links":[["Notre ghee, de l'alpage à la gélule","maison.html#ghee"],["Pourquoi plantes + ghee ?","ayurveda.html#pourquoi"]], "opts":[["Contient-il du lactose ?","lactose"]], "topic":"Question sur le ghee"},
 "lactose": {"text":"Le ghee est une matière grasse laitière : il figure parmi les allergènes, tout comme la gélatine de poisson de l'enveloppe. En cas d'allergie ou d'intolérance, demandez conseil à votre pharmacien ou appelez-nous avant toute prise.", "topic":"Question allergènes"},
 "usage": {"text":"Une gélule par jour, avec un verre d'eau. Un pot = 30 gélules = un mois. Que souhaitez-vous savoir de plus ?",
           "opts":[["Je suis enceinte ou j'allaite","enceinte"],["Je suis sous traitement","traitement"],["Puis-je combiner deux formules ?","combiner"],["Quand la prendre dans la journée ?","moment"]], "topic":"Question d'utilisation"},
 "enceinte": {"text":"Les formules VK Swiss sont <strong>déconseillées aux femmes enceintes ou allaitantes</strong>. Nous vous recommandons d'en parler à votre médecin ou à votre sage-femme.", "links":[["Lire toutes les précautions","faq.html"]], "topic":"Question précautions"},
 "traitement": {"text":"Toute personne sous traitement médical doit demander conseil à un spécialiste avant la prise. Certaines formules ont des contre-indications précises, détaillées sur chaque fiche produit.", "links":[["Voir les fiches produits","boutique.html"]], "topic":"Question précautions (traitement)"},
 "combiner": {"text":"Chaque formule est pensée pour être prise seule. Avant d'en associer deux, demandez conseil à votre pharmacien, ou appelez-nous : nous vous orientons volontiers.", "topic":"Combiner deux formules"},
 "moment": {"text":"Chaque fiche produit indique un moment conseillé (matin, repas ou soir). L'essentiel est la régularité : même heure, chaque jour, pendant au moins un mois.", "links":[["Voir les fiches produits","boutique.html"]], "topic":"Moment de prise"},
 "commande": {"text":"Paiement sécurisé par TWINT, carte (Visa, Mastercard, Amex), Apple Pay, Google Pay, PayPal ou PostFinance. Expédition depuis la Suisse, livraison offerte dès CHF 80.–.",
              "opts":[["L'abonnement, comment ça marche ?","abo"],["Suivre ou modifier ma commande","suivi"],["Livrez-vous à l'étranger ?","etranger"]], "links":[["Accéder à mon panier","panier.html"]], "topic":"Question commande"},
 "abo": {"text":"Avec l'abonnement, vous économisez <strong>15 % sur chaque pot</strong>, livré tous les 30 jours. Sans engagement : vous pouvez décaler, modifier ou arrêter à tout moment.", "links":[["Choisir ma formule en abonnement","boutique.html"]], "topic":"Abonnement"},
 "suivi": {"text":"Votre numéro de suivi La Poste vous est envoyé par e-mail dès l'expédition. Pour toute modification, contactez-nous avec votre numéro de commande.", "topic":"Suivi de commande"},
 "etranger": {"text":"La boutique en ligne livre la Suisse. VK Swiss est aussi présent en pharmacie en France, à Monaco, en Italie, au Luxembourg et en Belgique. [Livraison internationale à confirmer.]", "links":[["Points de vente à l'étranger","points-de-vente.html#international"]], "topic":"Livraison à l'étranger"},
 "pdv": {"text":"Plus de 120 pharmacies et drogueries proposent VK Swiss en Suisse. Recherchez par ville ou par canton.", "links":[["Trouver un point de vente","points-de-vente.html"]], "topic":"Point de vente"},
 "pro": {"text":"Vous souhaitez référencer VK Swiss dans votre pharmacie, droguerie ou cabinet ? Envoyez-nous une demande : nous vous répondons avec les conditions revendeurs.", "topic":"Demande revendeur / professionnel"},
 "humain": {"text":"Avec plaisir. Appelez-nous au <a href=\"tel:+41792890449\">+41 79 289 04 49</a> ou envoyez une demande écrite : nous vous répondons rapidement.", "topic":"Demande de contact"},
}
for p in PRODUCTS:
    TREE["f_" + p["slug"]] = {
        "text": "Je vous oriente vers <strong>%s</strong> : %s %s<br><br><small>%s</small>" % (p["full"], p["short"], "Conseil de prise : " + p["moment"].lower(), "Précautions : voir la fiche produit."),
        "links": [["Découvrir %s — %s" % (p["name"], chf(PRICE)), p["url"]]],
        "opts": [["Une question sur cette formule ?","humain"]],
        "topic": "Question sur %s" % p["name"],
    }

# ---------------- Gabarit ----------------
def head(title, desc, path, depth, ld, og_img="assets/img/hero-alpes.jpg", extra=""):
    b = "../" * depth
    canon = U + "/" + (path if path != "index.html" else "")
    ROBOTS = '<meta name="robots" content="noindex, nofollow">' if os.environ.get('STAGING','1')=='1' else '<meta name="robots" content="index, follow, max-image-preview:large">'
    ldj = "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld)
    return f'''<!DOCTYPE html>
<html lang="fr-CH" data-base="{b}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
{ROBOTS}
<meta property="og:type" content="website"><meta property="og:site_name" content="VK Swiss">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{U}/{og_img}"><meta property="og:locale" content="fr_CH">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ffffff">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default"><meta name="apple-mobile-web-app-title" content="VK Swiss">
<link rel="manifest" href="{b}manifest.webmanifest">
<link rel="icon" href="{b}assets/img/icon-192.png"><link rel="apple-touch-icon" href="{b}assets/img/icon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{b}assets/css/style.css">
{extra}{ldj}
</head>'''

def header(depth, cur, over=False):
    b = "../" * depth
    nav = "".join(f'<a href="{b}{h}"{" aria-current=\"page\"" if k==cur else ""}>{t}</a>' for h,t,k in NAV)
    logo = f'<a class="logo" href="{b}index.html" aria-label="VK Swiss, accueil"><img src="{b}assets/img/logo.png" alt="VK Swiss" width="54" height="52" onerror="this.outerHTML=\'<b>VK</b><small>SWISS</small>\'"></a>'
    tabs = [("index.html","Accueil","home","home"),("boutique.html","Boutique","grid","boutique"),(None,"Conseiller","chat","ast"),("panier.html","Panier","bag","panier"),("points-de-vente.html","Pharmacies","pin","pdv")]
    tb = ""
    for h,t,i,k in tabs:
        if h is None:
            tb += f'<button type="button" data-ast-open aria-controls="ast" aria-expanded="false">{ICONS[i]}<span>{t}</span></button>'
        elif k == "panier":
            tb += f'<a href="{b}{h}"{" aria-current=\"page\"" if k==cur else ""}>{ICONS[i]}<span class="badge" data-cart-count data-n="0">0</span><span>{t}</span></a>'
        else:
            tb += f'<a href="{b}{h}"{" aria-current=\"page\"" if k==cur else ""}>{ICONS[i]}<span>{t}</span></a>'
    return f'''<body>
<a class="skip" href="#main">Aller au contenu</a>
<div class="util"><div class="wrap"><div class="util__l"><span><span class="swiss" aria-hidden="true"></span>&nbsp; Fabriqué en Suisse</span><span>Livraison offerte dès CHF 80.–</span></div><div class="util__r"><a href="tel:{SITE['tel_href']}">{SITE['tel']}</a><a href="{b}contact.html">Contactez-nous</a><a href="{b}faq.html">Services</a><span>Suisse · FR</span></div></div></div>
<header class="hdr{' hdr--over' if over else ''}">
 <div class="hdr__top"><div class="hdr__search"><a class="ico" href="{b}boutique.html" aria-label="Rechercher un produit">{ICONS['search']}</a></div>{logo}
 <div class="hdr__icons"><button class="ico" type="button" data-ast-open aria-controls="ast" aria-expanded="false" aria-label="Ouvrir le conseiller VK Swiss">{ICONS['chat']}</button><a class="ico" href="{b}contact.html" aria-label="Mon compte">{ICONS['user']}</a><button class="ico" type="button" data-cart-open aria-label="Ouvrir le panier">{ICONS['bag']}<span class="badge" data-cart-count data-n="0">0</span></button></div></div>
 <nav class="nav" aria-label="Navigation principale">{nav}</nav>
</header>
<div class="m-top{' m-top--over' if over else ''}"><a class="ico" href="{b}boutique.html" aria-label="Rechercher">{ICONS['search']}</a>{logo}<button class="ico" type="button" data-cart-open aria-label="Ouvrir le panier">{ICONS['bag']}<span class="badge" data-cart-count data-n="0">0</span></button></div>
<nav class="tabbar" aria-label="Navigation de l'application">{tb}</nav>
'''

def footer(depth):
    b = "../" * depth
    prods = "".join(f'<li><a href="{b}{p["url"]}">{p["name"]}</a></li>' for p in PRODUCTS)
    return f'''<footer class="ftr">
 <div class="wrap">
  <div class="ftr__news"><div><p class="eyebrow" style="color:#9a9a9a">La lettre VK Swiss</p><p class="h3" style="color:#fff;margin-top:10px">Rituels, nouveautés et −10 % sur votre première commande.</p></div>
   <form data-demo novalidate><label class="sr" for="nl">Votre adresse e-mail</label><input id="nl" type="email" required autocomplete="email" placeholder="Votre adresse e-mail"><button type="submit">S'inscrire</button><p data-ok hidden tabindex="-1" style="margin:10px 0 0">Merci ! Votre code de bienvenue arrive par e-mail.</p></form></div>
  <div class="ftr__cols">
   <div><a class="logo" href="{b}index.html" style="align-items:flex-start;color:#fff"><b>VK</b><small>SWISS</small></a><p style="margin-top:20px;max-width:300px">La première maison à unir le ghee des Alpes suisses aux plantes de l'ayurvéda.</p><p>Distribution : {SITE['distrib']}</p><p><a href="tel:{SITE['tel_href']}">{SITE['tel']}</a><br><a href="mailto:{SITE['email']}">{SITE['email']}</a></p></div>
   <div><h4>La collection</h4><ul>{prods}</ul></div>
   <div><h4>La Maison</h4><ul><li><a href="{b}maison.html">Notre histoire</a></li><li><a href="{b}maison.html#ghee">Le ghee suisse</a></li><li><a href="{b}ayurveda.html">Ayurvéda & ghee</a></li><li><a href="{b}points-de-vente.html">Points de vente</a></li><li><a href="{b}contact.html?sujet=Demande%20revendeur#formulaire">Devenir revendeur</a></li></ul></div>
   <div><h4>Services</h4><ul><li><a href="{b}faq.html">Questions fréquentes</a></li><li><a href="{b}livraison-retours.html">Livraison & retours</a></li><li><a href="{b}contact.html">Contact</a></li><li><a href="https://www.instagram.com/vk___swiss/" rel="noopener">Instagram</a> · <a href="https://www.tiktok.com/@vkswiss" rel="noopener">TikTok</a></li></ul><div style="margin-top:22px">{PAY}</div></div>
  </div>
  <div class="ftr__legal"><p>Compléments alimentaires. Ils ne remplacent pas une alimentation variée et équilibrée ni un mode de vie sain. Ne pas dépasser la dose journalière indiquée. Tenir hors de portée des jeunes enfants.</p><p><a href="{b}mentions-legales.html">Mentions légales</a> · <a href="{b}cgv.html">CGV</a> · <a href="{b}confidentialite.html">Confidentialité (nLPD)</a> · © 2026 VK Swiss</p></div>
 </div>
</footer>
<div class="drawer" id="cart" aria-hidden="true" inert role="dialog" aria-modal="true" aria-label="Panier">
 <div class="drawer__bg" data-cart-close></div>
 <div class="drawer__panel"><div class="drawer__head"><span>Votre panier</span><button class="ico" type="button" data-cart-close aria-label="Fermer le panier">{ICONS['close']}</button></div>
  <div class="drawer__body"><div class="ship"><span data-ship-msg></span><div class="bar"><i data-ship-bar></i></div></div><div data-cart-lines></div></div>
  <div class="drawer__foot" data-has-items><div class="sum"><span>Sous-total</span><strong data-sub></strong></div><a class="btn btn--red btn--block" href="{b}panier.html">Commander</a>{PAY}</div></div>
</div>
<section class="ast" id="ast" aria-hidden="true" inert aria-label="Conseiller VK Swiss">
 <div class="ast__head"><span class="swiss" aria-hidden="true" style="width:30px;height:30px"></span><div><strong>Conseiller VK Swiss</strong><small>Réponses immédiates · conseil humain si besoin</small></div><button class="ico" type="button" data-ast-close aria-label="Fermer le conseiller">{ICONS['close']}</button></div>
 <div class="ast__body" aria-live="polite"></div>
 <div class="ast__cta"><a class="btn btn--ghost" href="tel:{SITE['tel_href']}">{ICONS['phone'].replace('<svg','<svg width="16" height="16" style="stroke:currentColor;fill:none"')} Appeler</a><a class="btn btn--red" data-ast-mail href="{b}contact.html#formulaire">Écrire</a></div>
</section>
<button class="ast-fab" type="button" data-ast-open aria-controls="ast" aria-expanded="false"><i aria-hidden="true"></i>Un conseil&nbsp;?</button>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="{b}assets/js/data.js"></script>
<script src="{b}assets/js/app.js" defer></script>
</body></html>'''

ORG = {"@context":"https://schema.org","@type":"Organization","@id":U+"/#org","name":"VK Swiss","url":U,"logo":U+"/assets/img/logo.png","email":SITE["email"],"telephone":SITE["tel"],
       "address":{"@type":"PostalAddress","streetAddress":"Case postale 27","postalCode":"2854","addressLocality":"Bassecourt","addressRegion":"JU","addressCountry":"CH"},
       "sameAs":["https://www.instagram.com/vk___swiss/","https://www.tiktok.com/@vkswiss"],
       "description":"Maison suisse de compléments alimentaires associant le ghee issu de lait suisse aux plantes de la tradition ayurvédique."}
def crumbs_ld(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":U+"/"+h} for i,(n,h) in enumerate(items)]}

def tile(p, depth, cls=""):
    b = "../" * depth
    return f'''<article class="tile rv" data-intent="{p['intent_key']}"><a class="tile__link" href="{b}{p['url']}" aria-label="{e(p['full'])}"></a><span class="tile__tag">{p['intent']}</span>
<div class="tile__img"><img src="{b}{p['img']}" alt="Pot VK Swiss {e(p['name'])} au ghee suisse, 30 gélules" loading="lazy" width="600" height="600"></div>
<span class="tile__dot" style="background:{p['color']}"></span><h3>{p['name']}</h3><p>{e(p['tagline'])}</p><p class="tile__price">{chf(PRICE)} <span style="color:var(--grey)">· 30 gélules</span></p>
<button class="btn btn--ghost tile__add" type="button" data-add="{p['slug']}">Ajouter au panier</button></article>'''

def write(path, s):
    full = os.path.join(OUT, path); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(s)

SERVICES = f'''<div class="services">
<div class="service">{ICONS['mountain']}<h3>Fabriqué en Suisse</h3><p>Ghee produit en Suisse, à partir de lait suisse.</p></div>
<div class="service">{ICONS['truck']}<h3>Livraison offerte</h3><p>Dès CHF 80.–, expédiée depuis la Suisse.</p></div>
<div class="service">{ICONS['lock']}<h3>Paiement sécurisé</h3><p>TWINT, cartes, PayPal, Apple Pay, PostFinance.</p></div>
<div class="service">{ICONS['phone']}<h3>Conseil personnalisé</h3><p>Une question ? <a href="tel:{SITE['tel_href']}" style="border-bottom:1px solid">{SITE['tel']}</a></p></div></div>'''

# ---------------- Accueil ----------------
def page_home():
    ld = [ORG, {"@context":"https://schema.org","@type":"WebSite","name":"VK Swiss","url":U,"inLanguage":"fr-CH"},
          {"@context":"https://schema.org","@type":"ItemList","name":"Collection VK Swiss","itemListElement":[{"@type":"ListItem","position":i+1,"url":U+"/"+p["url"],"name":p["full"]} for i,p in enumerate(PRODUCTS)]}]
    tiles = "".join(tile(p,0) for p in PRODUCTS)
    marquee = "<span>Ghee issu de lait suisse</span><span>Plantes de tradition ayurvédique</span><span>Une gélule par jour</span><span>Fabriqué en Suisse</span><span>Plus de 120 pharmacies</span>"
    s = head("VK Swiss | Compléments ayurvédiques au ghee suisse — Boutique officielle",
             "Ashwagandha, shilajit, bacopa, shatavari, tribulus, curcuma : six plantes ayurvédiques unies au ghee des Alpes suisses. Fabriqué en Suisse. Paiement TWINT. Livraison offerte dès CHF 80.",
             "index.html", 0, ld, extra='<link rel="preload" as="image" href="assets/img/hero-alpes.jpg">\n')
    s += header(0, "home", over=True)
    s += f'''<main id="main">
<section class="hero" aria-label="VK Swiss">
 <video autoplay muted loop playsinline preload="metadata" poster="assets/img/hero-poster.jpg" aria-hidden="true"><source src="assets/video/hero-720.mp4" type="video/mp4" media="(max-width: 860px)"><source src="assets/video/hero.mp4" type="video/mp4"></video>
 <div class="hero__in"><p class="eyebrow">Maison suisse · Ayurvéda</p><h1 class="h1">L'or des Alpes,<br>la sagesse de l'ayurvéda.</h1><p>Six plantes de la tradition ayurvédique, unies au ghee issu de lait suisse. Une gélule par jour.</p>
 <div class="hero__cta"><a class="btn btn--light" href="boutique.html">Découvrir la collection</a><button class="btn btn--light" type="button" data-ast-open aria-controls="ast" style="border-color:transparent;text-decoration:underline;text-underline-offset:6px">Trouver ma formule</button></div></div>
 <button class="ico hero__pause" type="button" aria-label="Mettre la vidéo en pause">{ICONS['pause']}</button>
</section>
<div class="marquee" aria-hidden="true">{marquee*3}</div>
<section class="sec" id="collection"><div class="wrap">
 <div class="sec__head rv"><p class="eyebrow">La collection</p><h2 class="h2">Six plantes. Un seul ghee.</h2><p class="lead">Chaque gélule réunit une plante emblématique de l'ayurvéda et un ghee pur, produit en Suisse à partir de lait suisse. 30 gélules, une cure d'un mois.</p></div>
 <div class="grid">{tiles}</div>
 <p class="center" style="margin-top:48px"><a class="link" href="boutique.html">Voir toute la collection</a></p>
</div></section>
<section class="sec sec--stone"><div class="wrap split">
 <div class="split__media rv"><img src="assets/img/ghee.jpg" alt="Goutte de ghee doré tombant d'une cuillère en laiton dans un bol de porcelaine" loading="lazy" width="1024" height="1280"></div>
 <div class="split__body rv"><p class="eyebrow">Le secret de la Maison</p><h2 class="h2">Le ghee, ce que l'ayurvéda a de plus précieux.</h2>
 <p>Depuis des millénaires, l'ayurvéda n'administre presque jamais une plante seule : elle l'accompagne d'une matière grasse noble, le ghee. VK Swiss a fait de ce geste ancestral sa signature, avec un ghee pur produit en Suisse à partir de lait suisse, réputé pour ses alpages et ses standards de qualité.</p>
 <p>Le résultat : la première gamme au monde à unir le ghee suisse et les joyaux de l'ayurvéda, dans une gélule.</p>
 <a class="link" href="maison.html#ghee">De l'alpage à la gélule</a></div>
</div></section>
<section class="sec"><div class="wrap"><p class="quote rv">« Nous n'avons rien inventé. Nous avons simplement réuni ce que la Suisse et l'ayurvéda font de mieux. »</p><p class="center eyebrow" style="margin-top:28px">La Maison VK Swiss</p></div></section>
<section class="sec sec--stone"><div class="wrap">
 <div class="sec__head rv"><p class="eyebrow">Le rituel</p><h2 class="h2">Simple comme une gélule par jour.</h2></div>
 <div class="steps"><div class="step rv"><b>01</b><h3 class="h3">Choisissez votre intention</h3><p>Énergie, clarté, sérénité, féminin, masculin ou rituel quotidien : une plante pour chacune.</p></div>
 <div class="step rv"><b>02</b><h3 class="h3">Une gélule, chaque jour</h3><p>Avec un verre d'eau, toujours au même moment. Le ghee suisse est déjà dans la gélule.</p></div>
 <div class="step rv"><b>03</b><h3 class="h3">Un mois de régularité</h3><p>30 gélules par pot. En abonnement, −15 % et votre pot arrive avant la fin du précédent.</p></div></div>
 <p class="center" style="margin-top:44px"><button class="btn" type="button" data-ast-open aria-controls="ast">Trouver ma formule en 30 secondes</button></p>
</div></section>
<section class="sec"><div class="wrap split split--rev">
 <div class="split__media rv"><img src="assets/img/alpage.jpg" alt="Alpage suisse au petit matin, vaches dans la prairie" loading="lazy" width="1024" height="1280"></div>
 <div class="split__body rv"><p class="eyebrow">Origine Suisse</p><h2 class="h2">Né du lait des alpages.</h2><p>La Suisse est reconnue pour la qualité de son lait : vaches en bonne santé, alpages préservés, exigences élevées de traçabilité et de bien-être animal. C'est ce lait qui donne naissance à notre ghee.</p><a class="link" href="maison.html">Découvrir la Maison</a></div>
</div></section>
<section class="sec sec--ink"><div class="wrap">{SERVICES}</div></section>
<section class="sec"><div class="wrap split">
 <div class="split__body rv"><p class="eyebrow">En pharmacie et droguerie</p><h2 class="h2">Plus de 120 points de vente en Suisse.</h2><p>De Porrentruy à Genève, de Verbier à Zurich : VK Swiss est conseillé par des pharmaciens et droguistes partout en Suisse, ainsi qu'en France, à Monaco, en Italie, au Luxembourg et en Belgique.</p><a class="btn btn--ghost" href="points-de-vente.html">Trouver un point de vente</a></div>
 <div class="split__media rv" style="aspect-ratio:1/1"><img src="assets/img/rituel.jpg" alt="Main tenant une gélule dorée VK Swiss dans une lumière matinale" loading="lazy" width="1024" height="1024"></div>
</div></section>
</main>'''
    s += footer(0)
    write("index.html", s)

# ---------------- Boutique ----------------
def page_shop():
    ld = [ORG, crumbs_ld([("Accueil",""),("La collection","boutique.html")]),
          {"@context":"https://schema.org","@type":"CollectionPage","name":"La collection VK Swiss","url":U+"/boutique.html"}]
    chips = '<button class="chip" type="button" data-filter="all" aria-pressed="true">Toutes</button>' + "".join(f'<button class="chip" type="button" data-filter="{p["intent_key"]}" aria-pressed="false">{p["intent"]}</button>' for p in PRODUCTS)
    s = head("La collection | Compléments ayurvédiques au ghee suisse — VK Swiss", "Découvrez les six formules VK Swiss : plantes ayurvédiques et ghee suisse en gélules. CHF 39.90 le pot de 30 gélules, −15 % en abonnement, paiement TWINT.", "boutique.html", 0, ld)
    s += header(0, "boutique")
    s += f'''<main id="main"><section class="sec" style="padding-top:64px"><div class="wrap">
<div class="sec__head"><p class="crumbs"><a href="index.html">Accueil</a> / La collection</p><h1 class="h1" style="font-size:clamp(40px,5vw,68px)">La collection</h1><p class="lead">Six plantes de la tradition ayurvédique, une même signature : le ghee suisse. Choisissez par intention.</p></div>
<div class="chips" role="group" aria-label="Filtrer par intention">{chips}</div>
<div class="grid grid--all" style="grid-template-columns:repeat(3,minmax(0,1fr))">{''.join(tile(p,0) for p in PRODUCTS)}</div>
</div></section>
<section class="sec sec--stone"><div class="wrap split"><div class="split__body"><p class="eyebrow">Abonnement</p><h2 class="h2">−15 % sur chaque pot. Sans engagement.</h2><p>Recevez votre formule tous les 30 jours, avant la fin de votre pot. Décalez, modifiez ou arrêtez en un clic.</p></div><div class="split__body"><p class="eyebrow">Hésitation ?</p><h2 class="h3">Notre conseiller vous oriente en quelques questions.</h2><p><button class="btn" type="button" data-ast-open aria-controls="ast">Trouver ma formule</button></p></div></div></section>
<section class="sec sec--ink"><div class="wrap">{SERVICES}</div></section></main>'''
    s += footer(0)
    write("boutique.html", s)

# ---------------- Produit ----------------
def page_product(p):
    others = [x for x in PRODUCTS if x["slug"] != p["slug"]][:3]
    pts = "".join(f"<li>{e(x)}</li>" for x in p["points"])
    ld = [ORG, crumbs_ld([("Accueil",""),("La collection","boutique.html"),(p["name"],p["url"])]),
          {"@context":"https://schema.org","@type":"Product","name":p["full"],"image":[U+"/"+p["img"],U+"/"+p["ing"]],"description":p["short"]+" "+p["story"],
           "sku":"VK-"+p["slug"].upper(),"brand":{"@type":"Brand","name":"VK Swiss"},"countryOfOrigin":"CH",
           "additionalProperty":[{"@type":"PropertyValue","name":"Plante","value":p["latin"]},{"@type":"PropertyValue","name":"Contenance","value":"30 gélules"},{"@type":"PropertyValue","name":"Posologie","value":"1 gélule par jour"}],
           "offers":{"@type":"Offer","url":U+"/"+p["url"],"priceCurrency":"CHF","price":"%.2f"%PRICE,"availability":"https://schema.org/InStock","itemCondition":"https://schema.org/NewCondition",
                     "shippingDetails":{"@type":"OfferShippingDetails","shippingDestination":{"@type":"DefinedRegion","addressCountry":"CH"}},
                     "seller":{"@id":U+"/#org"}}}]
    s = head(f"{p['full']} — 30 gélules | VK Swiss", f"{p['full']} : {p['short']} 1 gélule par jour. Fabriqué en Suisse. {chf(PRICE)}, −15 % en abonnement. Paiement TWINT, livraison offerte dès CHF 80.", p["url"], 1, ld, og_img=p["img"])
    s += header(1, "boutique")
    rel = "".join(tile(x,1) for x in others)
    s += f'''<main id="main" style="--c:{p['color']}"><div class="wrap">
<div class="pdp">
 <div class="gallery"><figure><img src="../{p['img']}" alt="Pot VK Swiss {e(p['name'])} au ghee naturel suisse, 30 gélules" width="900" height="900"></figure><figure><img src="../{p['ing']}" alt="{e(p['name'])} ({e(p['latin'])}), ingrédient de la formule" loading="lazy" width="800" height="1000"></figure><figure><img src="../assets/img/ghee.jpg" alt="Ghee suisse doré, beurre clarifié" loading="lazy" width="800" height="1000"></figure></div>
 <div class="buy" data-buy="{p['slug']}">
  <p class="crumbs"><a href="../index.html">Accueil</a> / <a href="../boutique.html">La collection</a> / {p['name']}</p>
  <p class="eyebrow" style="display:flex;gap:10px;align-items:center"><span class="tile__dot" style="background:{p['color']};margin:0"></span>{p['intent']} · {e(p['latin'])}</p>
  <h1 class="h1" style="font-size:clamp(38px,4vw,58px)">{e(p['full'])}</h1>
  <p class="lead" style="margin:0">{e(p['tagline'])}</p>
  <p style="margin:0">{e(p['short'])}</p>
  <div class="opts" role="radiogroup" aria-label="Mode d'achat">
   <label class="opt"><span style="display:flex;align-items:center"><input type="radio" name="mode" value="sub" checked><span>Abonnement −15 %<small>Livré tous les 30 jours · sans engagement</small></span></span><strong>{chf(PRICE*0.85)}</strong></label>
   <label class="opt"><span style="display:flex;align-items:center"><input type="radio" name="mode" value="unique"><span>Achat unique<small>30 gélules · 1 mois</small></span></span><strong>{chf(PRICE)}</strong></label>
  </div>
  <div class="buyrow"><div class="qty"><button type="button" data-step="-1" aria-label="Diminuer la quantité">−</button><input data-qty type="number" min="1" value="1" aria-label="Quantité" inputmode="numeric"><button type="button" data-step="1" aria-label="Augmenter la quantité">+</button></div>
  <button class="btn btn--red" type="button" data-add="{p['slug']}" data-open>Ajouter · <span data-buy-total>{chf(PRICE*0.85)}</span></button></div>
  {PAY}
  <div class="assure"><span>{ICONS['mountain']}Fabriqué en Suisse</span><span>{ICONS['truck']}Offerte dès CHF 80.–</span><span>{ICONS['lock']}Paiement sécurisé</span><span>{ICONS['phone']}<a href="tel:{SITE['tel_href']}">Conseil : {SITE['tel']}</a></span></div>
  <div class="acc">
   <details open><summary>La formule</summary><div class="acc__b"><ul class="points">{pts}</ul></div></details>
   <details><summary>L'histoire de la plante</summary><div class="acc__b"><p style="margin-top:0">{e(p['story'])}</p><p>Origine de la plante : {p['origin']}. Ghee : produit en Suisse à partir de lait suisse.</p></div></details>
   <details><summary>Conseils d'utilisation</summary><div class="acc__b">1 gélule par jour, avec un liquide. Moment conseillé : {e(p['moment'].lower())} 30 gélules = 1 mois.</div></details>
   <details><summary>Composition</summary><div class="acc__b">{e(p['ingredients'])}<br>Gélule : {e("gélatine (poisson)*, glycérol, eau, sorbitol")}.<br>*Allergènes : lait (ghee), poisson (gélatine).</div></details>
   <details><summary>Précautions d'emploi</summary><div class="acc__b">{e(p['precautions'])} Les compléments alimentaires ne remplacent pas une alimentation variée et équilibrée ni un mode de vie sain. Conserver entre 15 et 25 °C, hors de portée des jeunes enfants.</div></details>
   <details><summary>Livraison & paiement</summary><div class="acc__b">Expédition depuis la Suisse par La Poste, offerte dès CHF 80.–. Paiement TWINT, Visa, Mastercard, American Express, Apple Pay, Google Pay, PayPal ou PostFinance Pay. <a class="link" href="../livraison-retours.html">En savoir plus</a></div></details>
  </div>
 </div>
</div></div>
<section class="sec sec--stone" style="margin-top:80px"><div class="wrap split"><div class="split__media"><img src="../assets/img/ayurveda.jpg" alt="Nature morte ayurvédique : épices, racines et cuillère en laiton sur lin" loading="lazy" width="1024" height="1280"></div><div class="split__body"><p class="eyebrow">Pourquoi le ghee ?</p><h2 class="h2">Le geste ancestral, encapsulé.</h2><p>En ayurvéda, {p['name'].lower() if p['slug']!='curcuma' else 'le curcuma'} est traditionnellement associé à une matière grasse noble : le ghee. Chaque gélule VK Swiss réunit les deux, avec un ghee pur produit en Suisse.</p><a class="link" href="../ayurveda.html#pourquoi">Lire notre guide</a></div></div></section>
<section class="sec"><div class="wrap"><div class="sec__head"><p class="eyebrow">À découvrir aussi</p><h2 class="h2">Compléter votre rituel</h2></div><div class="grid">{rel}</div></div></section>
<div class="sticky-buy"><div><strong style="font-weight:400">{p['name']}</strong><br><small style="color:var(--grey)">{chf(PRICE)} · 30 gélules</small></div><button class="btn btn--red" type="button" data-add="{p['slug']}" data-open>Ajouter au panier</button></div>
</main>'''
    s += footer(1)
    write(p["url"], s)

# ---------------- Maison ----------------
def page_maison():
    ld = [ORG, crumbs_ld([("Accueil",""),("La Maison","maison.html")]), {"@context":"https://schema.org","@type":"AboutPage","name":"La Maison VK Swiss","url":U+"/maison.html"}]
    s = head("La Maison VK Swiss | Le ghee suisse au service de l'ayurvéda", "L'histoire de VK Swiss : la première gamme au monde associant le ghee issu de lait suisse aux plantes de l'ayurvéda. Fabriqué en Suisse, distribué depuis le Jura.", "maison.html", 0, ld)
    s += header(0, "maison")
    s += f'''<main id="main">
<section class="hero" style="height:72svh;min-height:480px"><img class="hero__img" src="assets/img/hero-alpes.jpg" alt="" width="1600" height="900"><div class="hero__in"><p class="eyebrow">La Maison</p><h1 class="h1">Une idée née entre deux mondes.</h1></div></section>
<section class="sec"><div class="wrap"><p class="quote rv">D'un côté, la Suisse et l'excellence de son lait. De l'autre, l'ayurvéda et cinq mille ans de savoir sur les plantes. VK Swiss est né de leur rencontre.</p></div></section>
<section class="sec sec--stone" id="ghee"><div class="wrap split"><div class="split__media rv"><img src="assets/img/ghee.jpg" alt="Ghee suisse doré" loading="lazy" width="1024" height="1280"></div>
<div class="split__body rv"><p class="eyebrow">Le ghee suisse</p><h2 class="h2">De l'alpage à la gélule.</h2><p>Le ghee est un beurre clarifié. On chauffe doucement le beurre pour en séparer l'eau et les protéines du lait, jusqu'à obtenir une matière grasse pure, dorée et stable, au parfum de noisette.</p><p>Notre ghee est produit en Suisse, à partir de lait suisse. Un choix d'exigence : la Suisse est reconnue pour la santé de ses troupeaux, la qualité de ses alpages et ses standards élevés de traçabilité et de bien-être animal.</p><ul class="points"><li>Ghee 100 % naturel</li><li>Issu de lait suisse</li><li>Entre 420 et 510 mg par gélule selon la formule</li></ul></div></div></section>
<section class="sec"><div class="wrap split split--rev"><div class="split__media rv"><img src="assets/img/ayurveda.jpg" alt="Plantes et épices ayurvédiques sur lin" loading="lazy" width="1024" height="1280"></div>
<div class="split__body rv"><p class="eyebrow">Les plantes</p><h2 class="h2">Les joyaux de l'ayurvéda.</h2><p>Ashwagandha KSM-66®, shilajit, bacopa, shatavari, tribulus et curcuma : nous avons retenu six plantes emblématiques, sélectionnées dans leurs régions d'origine, sous forme d'extraits standardisés lorsque c'est pertinent (withanolides, bacosides, acide fulvique, saponines).</p><a class="link" href="boutique.html">Découvrir la collection</a></div></div></section>
<section class="sec sec--ink"><div class="wrap">{SERVICES}</div></section>
<section class="sec"><div class="wrap split"><div class="split__body rv"><p class="eyebrow">Une Maison jurassienne</p><h2 class="h2">Fabriqué en Suisse, conseillé en pharmacie.</h2><p>Les produits VK Swiss sont fabriqués en Suisse et distribués par AXES Sàrl, à Bassecourt, dans le Jura. Ils sont disponibles dans plus de 120 pharmacies et drogueries en Suisse, et à l'international.</p><a class="btn btn--ghost" href="points-de-vente.html">Nos points de vente</a></div><div class="split__media rv" style="aspect-ratio:1/1"><img src="assets/img/gamme.jpg" alt="Les six coffrets de la gamme VK Swiss" loading="lazy" width="1200" height="1200" style="object-fit:contain;background:#fff"></div></div></section>
</main>'''
    s += footer(0)
    write("maison.html", s)

# ---------------- Ayurvéda (GEO) ----------------
def page_ayurveda():
    faqs = FAQ[:4]
    ld = [ORG, crumbs_ld([("Accueil",""),("Ayurvéda & ghee","ayurveda.html")]),
          {"@context":"https://schema.org","@type":"Article","headline":"Ayurvéda et ghee : le guide VK Swiss","author":{"@id":U+"/#org"},"publisher":{"@id":U+"/#org"},"inLanguage":"fr-CH","datePublished":"2026-11-24","image":U+"/assets/img/ayurveda.jpg","mainEntityOfPage":U+"/ayurveda.html"},
          {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}]
    rows = "".join(f'<tr><td style="padding:14px 10px;border-bottom:1px solid var(--line)"><a class="link" style="font-size:12px" href="{p["url"]}">{p["name"]}</a></td><td style="padding:14px 10px;border-bottom:1px solid var(--line)">{e(p["latin"])}</td><td style="padding:14px 10px;border-bottom:1px solid var(--line)">{p["intent"]}</td><td style="padding:14px 10px;border-bottom:1px solid var(--line)">{e(p["points"][0])}</td><td style="padding:14px 10px;border-bottom:1px solid var(--line)">{e(p["moment"])}</td></tr>' for p in PRODUCTS)
    s = head("Ayurvéda et ghee : le guide complet | VK Swiss", "Qu'est-ce que le ghee ? Pourquoi l'ayurvéda associe-t-il plantes et matière grasse ? Comment choisir entre ashwagandha, shilajit, bacopa, shatavari, tribulus et curcuma ? Le guide VK Swiss.", "ayurveda.html", 0, ld)
    s += header(0, "ayurveda")
    s += f'''<main id="main"><article>
<section class="sec" style="padding-bottom:40px"><div class="wrap" style="max-width:860px"><p class="crumbs"><a href="index.html">Accueil</a> / Ayurvéda & ghee</p><h1 class="h1" style="margin:18px 0 24px">Ayurvéda et ghee : le guide.</h1>
<p class="lead"><strong>En bref :</strong> le ghee est un beurre clarifié que l'ayurvéda utilise depuis des millénaires comme support des plantes. VK Swiss associe six plantes ayurvédiques à un ghee produit en Suisse à partir de lait suisse, dans une gélule à prendre une fois par jour.</p></div></section>
<div class="wrap" style="max-width:860px;display:grid;gap:56px;padding-bottom:100px">
<section id="ayurveda"><h2 class="h2" style="margin-bottom:18px">Qu'est-ce que l'ayurvéda ?</h2><p>L'ayurvéda, littéralement « science de la vie » en sanskrit, est le système traditionnel de bien-être né en Inde il y a plusieurs millénaires. Il repose sur l'équilibre du corps et de l'esprit, l'alimentation, le rythme de vie et l'usage des plantes.</p></section>
<section id="ghee"><h2 class="h2" style="margin-bottom:18px">Qu'est-ce que le ghee ?</h2><p>Le ghee est un beurre clarifié. Chauffé lentement, le beurre perd son eau et ses protéines de lait ; il ne reste qu'une matière grasse pure, dorée, au goût de noisette, qui se conserve longtemps. En ayurvéda, il occupe une place centrale, à la fois en cuisine et comme support des préparations à base de plantes.</p><figure style="margin:28px 0 0"><img src="assets/img/ghee.jpg" alt="Ghee doré dans un bol en porcelaine" loading="lazy" width="1024" height="1280" style="aspect-ratio:16/10;object-fit:cover;width:100%"></figure></section>
<section id="pourquoi"><h2 class="h2" style="margin-bottom:18px">Pourquoi associer plantes et ghee ?</h2><p>Dans la tradition ayurvédique, une plante est rarement prise seule : elle est préparée ou consommée avec un « véhicule » (anupana), et le ghee est le plus réputé d'entre eux. De nombreux composés végétaux sont liposolubles, c'est-à-dire qu'ils se dissolvent dans les graisses ; la cuisine indienne associe d'ailleurs depuis toujours le curcuma à une matière grasse et au poivre noir.</p><p>VK Swiss reprend ce principe et le simplifie : chaque gélule contient déjà la plante et le ghee suisse.</p></section>
<section id="choisir"><h2 class="h2" style="margin-bottom:18px">Comment choisir sa formule ?</h2><p>Partez de votre intention. Le tableau ci-dessous résume les six formules VK Swiss.</p><div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:15px;min-width:640px"><thead><tr style="text-align:left;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey)"><th style="padding:10px">Formule</th><th style="padding:10px">Plante</th><th style="padding:10px">Intention</th><th style="padding:10px">Spécificité</th><th style="padding:10px">Moment conseillé</th></tr></thead><tbody>{rows}</tbody></table></div><p style="margin-top:24px"><button class="btn" type="button" data-ast-open aria-controls="ast">Me faire conseiller</button></p></section>
<section id="ksm66"><h2 class="h2" style="margin-bottom:18px">Ashwagandha KSM-66® : que signifie « extrait standardisé » ?</h2><p>Un extrait standardisé garantit une teneur constante en composés caractéristiques de la plante, d'un lot à l'autre. L'ashwagandha VK Swiss utilise l'extrait KSM-66®, issu uniquement de racines et standardisé à 5 % de withanolides. Le bacopa est standardisé à 20 % de bacosides ; le shilajit apporte 170 mg d'acide fulvique par gélule.</p></section>
<section id="faq"><h2 class="h2" style="margin-bottom:18px">Questions fréquentes</h2><div class="acc">{''.join(f'<details><summary>{e(q)}</summary><div class="acc__b">{e(a)}</div></details>' for q,a in faqs)}</div><p style="margin-top:20px"><a class="link" href="faq.html">Toutes les questions</a></p></section>
<p class="note">Les informations de cette page décrivent les usages traditionnels de l'ayurvéda. Elles ne constituent pas un avis médical. Les compléments alimentaires ne remplacent pas une alimentation variée et équilibrée.</p>
</div></article></main>'''
    s += footer(0)
    write("ayurveda.html", s)

# ---------------- Points de vente ----------------
def page_pdv():
    n = sum(len(v) for v in STORES.values())
    opts = "".join(f'<option value="{e(c)}">{e(c)} ({len(v)})</option>' for c,v in STORES.items())
    cards = ""
    for c, lst in STORES.items():
        cards += f'<p class="canton" data-canton-title="{e(c)}">{e(c)}</p>'
        for name, addr in lst:
            q = html.escape("https://www.google.com/maps/search/?api=1&query=" + (name + ", " + addr).replace(" ", "+"))
            cards += f'<div class="store" data-store data-canton="{e(c)}"><h3>{e(name)}</h3><p>{e(addr)}</p><a href="{q}" target="_blank" rel="noopener">Itinéraire</a></div>'
    ld = [ORG, crumbs_ld([("Accueil",""),("Points de vente","points-de-vente.html")]),
          {"@context":"https://schema.org","@type":"ItemList","name":"Pharmacies et drogueries VK Swiss en Suisse","numberOfItems":n,
           "itemListElement":[{"@type":"ListItem","position":i+1,"item":{"@type":"Pharmacy","name":nm,"address":ad}} for i,(nm,ad) in enumerate([x for v in STORES.values() for x in v])]}]
    s = head("Points de vente VK Swiss | Pharmacies et drogueries en Suisse", f"Trouvez VK Swiss près de chez vous : {n} pharmacies et drogueries en Suisse (Jura, Genève, Vaud, Valais, Berne, Neuchâtel, Fribourg, Tessin, Zurich…) et en France, Monaco, Italie, Luxembourg, Belgique.", "points-de-vente.html", 0, ld)
    s += header(0, "pdv")
    s += f'''<main id="main"><section class="sec" style="padding-top:64px"><div class="wrap">
<div class="sec__head"><p class="crumbs"><a href="index.html">Accueil</a> / Points de vente</p><h1 class="h1" style="font-size:clamp(40px,5vw,68px)">Points de vente</h1><p class="lead">{n} pharmacies et drogueries vous conseillent VK Swiss en Suisse.</p></div>
<div class="finder"><div class="finder__side"><label class="field" for="store-q">Ville, NPA ou nom<input id="store-q" type="search" placeholder="ex. Lausanne, 2900…" autocomplete="off"></label>
<label class="field" for="store-canton">Canton<select id="store-canton"><option value="">Tous les cantons</option>{opts}</select></label>
<p class="note">Votre pharmacie n'est pas dans la liste ? <a class="link" style="font-size:11px" href="contact.html?sujet=Demande%20revendeur#formulaire">Proposez-lui VK Swiss</a></p><a class="btn btn--red" href="boutique.html">Commander en ligne</a></div>
<div class="stores">{cards}</div></div>
<div id="international" style="margin-top:90px"><div class="sec__head"><p class="eyebrow">International</p><h2 class="h2">Aussi en France, à Monaco, en Italie, au Luxembourg et en Belgique.</h2><p class="lead">[Listes des points de vente à reprendre depuis le site actuel.]</p></div></div>
</div></section></main>'''
    s += footer(0)
    write("points-de-vente.html", s)

# ---------------- FAQ ----------------
def page_faq():
    ld = [ORG, crumbs_ld([("Accueil",""),("Questions fréquentes","faq.html")]),
          {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}]
    s = head("Questions fréquentes | VK Swiss", "Ghee, prise des gélules, précautions, allergènes, fabrication suisse, paiement TWINT, livraison : toutes les réponses sur les compléments VK Swiss.", "faq.html", 0, ld)
    s += header(0, "faq")
    s += f'''<main id="main"><section class="sec" style="padding-top:64px"><div class="wrap" style="max-width:860px">
<p class="crumbs"><a href="index.html">Accueil</a> / Questions fréquentes</p><h1 class="h1" style="font-size:clamp(40px,5vw,68px);margin:18px 0 40px">Questions fréquentes</h1>
<div class="acc">{''.join(f'<details><summary>{e(q)}</summary><div class="acc__b">{e(a)}</div></details>' for q,a in FAQ)}</div>
<div style="margin-top:56px;display:flex;gap:12px;flex-wrap:wrap"><button class="btn" type="button" data-ast-open aria-controls="ast">Poser ma question au conseiller</button><a class="btn btn--ghost" href="tel:{SITE['tel_href']}">Appeler {SITE['tel']}</a></div>
</div></section></main>'''
    s += footer(0)
    write("faq.html", s)

# ---------------- Contact (formulaire Elementor Pro) ----------------
def page_contact():
    ld = [ORG, crumbs_ld([("Accueil",""),("Contact","contact.html")]), {"@context":"https://schema.org","@type":"ContactPage","name":"Contact VK Swiss","url":U+"/contact.html"}]
    sujets = ["Demande de conseil","Choix d'une formule","Question sur une commande","Abonnement","Demande revendeur","Presse & partenariats","Autre demande"]
    s = head("Contact | VK Swiss — Conseil, commandes et revendeurs", f"Contactez VK Swiss : {SITE['tel']}, {SITE['email']} ou via notre formulaire. Conseil sur les formules, commandes, abonnement et demandes revendeurs.", "contact.html", 0, ld)
    s += header(0, "contact")
    s += f'''<main id="main"><section class="sec" style="padding-top:64px"><div class="wrap split" style="align-items:start">
<div class="split__body"><p class="crumbs"><a href="index.html">Accueil</a> / Contact</p><h1 class="h1" style="font-size:clamp(40px,5vw,68px)">Parlons-en.</h1><p class="lead">Un conseil sur une formule, une question sur une commande, un projet de revente ? Nous vous répondons personnellement.</p>
<div class="acc" style="margin-top:10px"><p style="display:flex;gap:14px;align-items:center;padding:18px 0;border-bottom:1px solid var(--line);margin:0">{ICONS['phone'].replace('<svg','<svg width="22" height="22" style="stroke:currentColor;fill:none;stroke-width:1.3"')}<a href="tel:{SITE['tel_href']}">{SITE['tel']}</a></p><p style="display:flex;gap:14px;align-items:center;padding:18px 0;border-bottom:1px solid var(--line);margin:0">{ICONS['chat'].replace('<svg','<svg width="22" height="22" style="stroke:currentColor;fill:none;stroke-width:1.3"')}<a href="mailto:{SITE['email']}">{SITE['email']}</a></p><p style="padding:18px 0;margin:0;color:var(--grey)">{SITE['distrib']}</p></div></div>
<div id="formulaire">
<!-- Formulaire à reconstruire en widget « Formulaire » Elementor Pro : nom du formulaire « Demande VK Swiss », actions après envoi : Collecter les soumissions (Envois) + E-mail + E-mail 2 (accusé de réception). -->
<form class="form elementor-form" name="Demande VK Swiss" data-demo novalidate aria-labelledby="ft">
<h2 id="ft" class="h3 full">Envoyer une demande</h2>
<label class="field" for="form-field-nom">Nom et prénom *<input id="form-field-nom" name="form_fields[nom]" required autocomplete="name"></label>
<label class="field" for="form-field-email">E-mail *<input id="form-field-email" name="form_fields[email]" type="email" required autocomplete="email"></label>
<label class="field" for="form-field-tel">Téléphone<input id="form-field-tel" name="form_fields[telephone]" type="tel" autocomplete="tel"></label>
<label class="field" for="form-field-sujet">Sujet *<select id="form-field-sujet" name="form_fields[sujet]" required>{''.join(f'<option>{x}</option>' for x in sujets)}</select></label>
<label class="field full" for="form-field-message">Message *<textarea id="form-field-message" name="form_fields[message]" required></textarea></label>
<label class="check full"><input type="checkbox" name="form_fields[rappel]" value="oui"> Je souhaite être rappelé(e)</label>
<label class="check full"><input type="checkbox" required name="form_fields[consentement]"> J'accepte que mes données soient utilisées pour traiter ma demande, conformément à la <a class="link" style="font-size:11px" href="confidentialite.html">politique de confidentialité</a>. *</label>
<div class="full"><button class="btn btn--red" type="submit">Envoyer ma demande</button></div>
<div class="ok full" data-ok hidden tabindex="-1"><strong>Merci, votre demande est bien envoyée.</strong><br>Vous recevez une confirmation par e-mail. Nous vous répondons rapidement.</div>
</form></div>
</div></section></main>'''
    s += footer(0)
    write("contact.html", s)

# ---------------- Panier / Checkout ----------------
def page_cart():
    ld = [ORG]
    pays = [("twint","TWINT","Paiement instantané par l'app"),("card","Carte de crédit / débit","Visa, Mastercard, American Express — via Stripe"),("wallet","Apple Pay / Google Pay","Via Stripe"),("paypal","PayPal","Compte PayPal ou carte"),("postfinance","PostFinance Pay","PostFinance Card / e-finance")]
    radios = "".join(f'<label><input type="radio" name="pay" value="{k}"{" checked" if i==0 else ""} required><span><strong style="font-weight:400">{t}</strong><br><small style="color:var(--grey)">{d}</small></span></label>' for i,(k,t,d) in enumerate(pays))
    s = head("Panier et paiement sécurisé | VK Swiss", "Finalisez votre commande VK Swiss : paiement sécurisé par TWINT, carte, Apple Pay, Google Pay, PayPal ou PostFinance. Livraison offerte dès CHF 80.", "panier.html", 0, ld, extra='<meta name="robots" content="noindex, follow">\n')
    s += header(0, "panier")
    s += f'''<main id="main"><section class="sec" style="padding-top:56px"><div class="wrap">
<p class="steps-co"><b>1. Panier</b> · <b>2. Livraison</b> · <b>3. Paiement</b></p><h1 class="h2" style="margin:14px 0 40px">Votre commande</h1>
<div class="co">
<form class="co__box" data-demo data-checkout novalidate>
 <p class="eyebrow" style="text-align:center">Paiement express</p>
 <div class="express"><button type="button" data-express>TWINT</button><button type="button" data-express>Apple Pay</button><button type="button" data-express class="alt">Google Pay</button></div>
 <p class="note" style="text-align:center;margin:0">ou remplissez vos coordonnées</p>
 <h2 class="h3">Coordonnées</h2>
 <div class="form"><label class="field full" for="c-mail">E-mail *<input id="c-mail" type="email" required autocomplete="email"></label>
 <label class="field" for="c-fn">Prénom *<input id="c-fn" required autocomplete="given-name"></label><label class="field" for="c-ln">Nom *<input id="c-ln" required autocomplete="family-name"></label>
 <label class="field full" for="c-ad">Adresse *<input id="c-ad" required autocomplete="street-address"></label>
 <label class="field" for="c-zip">NPA *<input id="c-zip" required inputmode="numeric" autocomplete="postal-code"></label><label class="field" for="c-city">Localité *<input id="c-city" required autocomplete="address-level2"></label>
 <label class="field full" for="c-tel">Téléphone (pour TWINT et la livraison)<input id="c-tel" type="tel" autocomplete="tel"></label></div>
 <h2 class="h3">Livraison</h2>
 <div class="paym"><label><input type="radio" name="ship" checked> <span>La Poste — PostPac Priority<br><small style="color:var(--grey)">[Délai à confirmer]</small></span><em data-shipping></em></label><label><input type="radio" name="ship"> <span>Retrait à Bassecourt (JU)<br><small style="color:var(--grey)">Sur rendez-vous</small></span><em>Gratuit</em></label></div>
 <h2 class="h3">Paiement</h2>
 <div class="paym" role="radiogroup" aria-label="Moyen de paiement">{radios}</div>
 <p class="note">{ICONS['lock'].replace('<svg','<svg width="14" height="14" style="stroke:currentColor;fill:none;vertical-align:-2px"')} Vous serez redirigé vers la page sécurisée du prestataire choisi. VK Swiss n'a jamais accès à vos données bancaires.</p>
 <label class="check"><input type="checkbox" required> J'accepte les <a class="link" style="font-size:11px" href="cgv.html">conditions générales de vente</a>. *</label>
 <button class="btn btn--red btn--block" type="submit">Payer <span data-total></span></button>
 <div class="ok" data-ok hidden tabindex="-1"><strong>Maquette : commande simulée.</strong><br>Sur le site WordPress/WooCommerce, ce bouton redirige vers TWINT, Stripe, PayPal ou PostFinance.</div>
</form>
<aside class="co__aside" aria-label="Récapitulatif"><h2 class="h3">Récapitulatif</h2><div class="ship"><span data-ship-msg></span><div class="bar"><i data-ship-bar></i></div></div><div data-cart-lines></div>
<label class="field" for="promo">Code promo<span style="display:flex;gap:8px"><input id="promo" style="flex:1"><button class="btn btn--ghost" type="button" style="min-height:50px;padding:0 18px">OK</button></span></label>
<div class="sum"><span>Sous-total</span><span data-sub></span></div><div class="sum"><span>Livraison</span><span data-shipping></span></div><div class="sum sum--total"><span>Total TTC</span><strong data-total></strong></div>
<p class="note" style="margin:0">TVA suisse incluse.</p>{PAY}</aside>
</div></div></section></main>'''
    s += footer(0)
    write("panier.html", s)

# ---------------- Pages légales ----------------
def page_legal(path, title, desc, body):
    s = head(f"{title} | VK Swiss", desc, path, 0, [ORG, crumbs_ld([("Accueil",""),(title,path)])])
    s += header(0, "")
    s += f'<main id="main"><section class="sec" style="padding-top:64px"><div class="wrap" style="max-width:820px"><p class="crumbs"><a href="index.html">Accueil</a> / {title}</p><h1 class="h2" style="margin:18px 0 32px">{title}</h1>{body}</div></section></main>'
    s += footer(0)
    write(path, s)

def legal():
    page_legal("mentions-legales.html","Mentions légales","Mentions légales du site VK Swiss.",
      f"<p><strong>Éditeur et distributeur :</strong> AXES Sàrl, Case postale 27, 2854 Bassecourt, Suisse. [IDE/UID et inscription au registre du commerce à compléter.]</p><p>Contact : <a class='link' style='font-size:12px' href='mailto:{SITE['email']}'>{SITE['email']}</a> · {SITE['tel']}</p><p><strong>Hébergement :</strong> [à compléter].</p><p>Les produits VK Swiss sont des compléments alimentaires au sens de la législation suisse sur les denrées alimentaires. Les informations publiées sur ce site décrivent des usages traditionnels et ne constituent pas un avis médical.</p>")
    page_legal("cgv.html","Conditions générales de vente","Conditions générales de vente de la boutique en ligne VK Swiss.",
      "<p>[Document à rédiger et valider juridiquement : objet, prix en CHF TTC, commande, abonnement (résiliation à tout moment), paiement (TWINT, cartes via Stripe, PayPal, PostFinance), livraison, droit de retour, garantie, protection des données, for juridique.]</p>")
    page_legal("confidentialite.html","Politique de confidentialité","Protection des données personnelles chez VK Swiss, conformément à la nLPD suisse.",
      "<p>VK Swiss traite vos données personnelles conformément à la loi fédérale sur la protection des données (nLPD) et, le cas échéant, au RGPD.</p><p>[À compléter : responsable du traitement, données collectées (commande, formulaire de contact, newsletter), finalités, prestataires (paiement, hébergement, envoi d'e-mails, statistiques), durées de conservation, droits d'accès et de rectification, contact.]</p>")
    page_legal("livraison-retours.html","Livraison & retours","Livraison VK Swiss depuis la Suisse, offerte dès CHF 80, et conditions de retour.",
      "<h2 class='h3'>Livraison</h2><p>Expédition depuis la Suisse par La Poste. Livraison offerte dès CHF 80.– d'achat en Suisse. [Tarif en dessous du seuil et délais à confirmer.]</p><h2 class='h3' style='margin-top:32px'>Retours</h2><p>[Conditions de retour à définir. Pour des raisons d'hygiène, les produits ouverts ne peuvent généralement pas être repris.]</p>")

# ---------------- SEO / GEO / PWA ----------------
def seo():
    pages = ["","boutique.html","maison.html","ayurveda.html","points-de-vente.html","faq.html","contact.html","livraison-retours.html","mentions-legales.html","cgv.html","confidentialite.html"] + [p["url"] for p in PRODUCTS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{U}/{x}</loc><lastmod>2026-11-24</lastmod></url>\n" for x in pages) + "</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /panier.html\n\nSitemap: {U}/sitemap.xml\n")
    llm = f"# VK Swiss\n\n> Maison suisse de compléments alimentaires qui associe le ghee (beurre clarifié) produit en Suisse à partir de lait suisse à six plantes de la tradition ayurvédique. Gélules, 1 par jour, pots de 30. Fabriqué en Suisse, distribué par AXES Sàrl (Bassecourt, Jura). Boutique en ligne : paiement TWINT, cartes, Apple Pay, Google Pay, PayPal, PostFinance. Plus de 120 pharmacies et drogueries en Suisse.\n\n## Produits\n"
    for p in PRODUCTS:
        llm += f"- [{p['full']}]({U}/{p['url']}): {p['short']} Plante : {p['latin']}, origine {p['origin']}. Prix {chf(PRICE)}.\n"
    llm += f"\n## Pages clés\n- [Guide Ayurvéda & ghee]({U}/ayurveda.html)\n- [La Maison et le ghee suisse]({U}/maison.html)\n- [Points de vente]({U}/points-de-vente.html)\n- [FAQ]({U}/faq.html)\n- [Contact]({U}/contact.html): {SITE['tel']}, {SITE['email']}\n"
    write("llms.txt", llm)
    man = {"name":"VK Swiss","short_name":"VK Swiss","start_url":"./index.html","scope":"./","display":"standalone","background_color":"#ffffff","theme_color":"#ffffff","lang":"fr-CH",
           "icons":[{"src":"assets/img/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"assets/img/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}]}
    write("manifest.webmanifest", json.dumps(man, ensure_ascii=False, indent=1))
    write("sw.js", "const C='vk-v1';self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(['./','./index.html','./boutique.html','./assets/css/style.css','./assets/js/app.js','./assets/js/data.js'])).then(()=>self.skipWaiting()))});\nself.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));\nself.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;e.respondWith(fetch(e.request).then(r=>{const cp=r.clone();caches.open(C).then(c=>c.put(e.request,cp));return r}).catch(()=>caches.match(e.request)))});\n")
    data = {"products":[{k:p[k] for k in ("slug","name","full","price","img","url","color")} for p in PRODUCTS],"tree":TREE}
    write("assets/js/data.js", "window.VK=" + json.dumps(data, ensure_ascii=False) + ";\n")

if __name__ == "__main__":
    page_home(); page_shop()
    for p in PRODUCTS: page_product(p)
    page_maison(); page_ayurveda(); page_pdv(); page_faq(); page_contact(); page_cart(); legal(); seo()
    print("ok", OUT)
