# -*- coding: utf-8 -*-
"""Base de connaissances du conseiller VK Swiss, générée à partir des contenus du site."""
from data import SITE, PRODUCTS, FAQ, STORES

TEL = SITE["tel"]
PRICE = "CHF %.2f" % SITE["price"]
SUB = "CHF %.2f" % (SITE["price"] * 0.85)

def P(slug): return [p for p in PRODUCTS if p["slug"] == slug][0]

KB = []
def add(id, keys, title, answer, links=None, topic=None, product=None, aspect=None, sensitive=False):
    KB.append({"id": id, "k": keys, "t": title, "a": answer, "l": links or [], "topic": topic or title,
               "p": product, "x": aspect, "s": sensitive})

# --- Produits : 5 facettes chacun ---
ASPECTS = {
  "info":  "presentation decouvrir quoi c'est effet bienfait propriete plante description histoire",
  "compo": "composition ingredient contient dosage mg extrait allergene gelule lactose gelatine poisson",
  "prec":  "precaution contre-indication danger risque enceinte allaitement traitement medicament effet secondaire deconseille enfant anticoagulant interaction compatible pilule contraception",
  "usage": "prendre prise posologie dose combien gelule quand moment matin soir jour duree cure",
  "prix":  "prix tarif cout combien coute chf acheter commander abonnement",
}
for p in PRODUCTS:
    n, s = p["name"], p["slug"]; u = "produits/%s.html" % s
    base = f"{n.lower()} {p['latin'].lower()} {p['intent'].lower()}"
    buy = [[f"Voir {n} — {PRICE}", u]]
    add(f"{s}-info", base + " " + ASPECTS["info"], n,
        f"<strong>{p['full']}</strong><br>{p['short']}<br><br>{p['story']}", buy, f"Question sur {n}", s, "info")
    add(f"{s}-compo", base + " " + ASPECTS["compo"], f"Composition {n}",
        f"<strong>Composition de {n} (par gélule)</strong><br>{p['ingredients']}<br>Gélule : gélatine (poisson), glycérol, eau, sorbitol.<br><em>Allergènes : lait (ghee) et poisson (gélatine).</em> Ne convient pas aux végétaliens.", buy, f"Composition {n}", s, "compo")
    add(f"{s}-prec", base + " " + ASPECTS["prec"], f"Précautions {n}",
        f"<strong>Précautions — {n}</strong><br>{p['precautions']}<br><br>En cas de doute, demandez conseil à votre médecin ou pharmacien, ou appelez-nous.", buy, f"Précautions {n}", s, "prec", True)
    add(f"{s}-usage", base + " " + ASPECTS["usage"], f"Utilisation {n}",
        f"<strong>Comment prendre {n} ?</strong><br>1 gélule par jour, avec un verre d'eau. Moment conseillé : {p['moment'].lower()} Un pot de 30 gélules = 1 mois. Ne pas dépasser la dose journalière indiquée.", buy, f"Utilisation {n}", s, "usage")
    add(f"{s}-prix", base + " " + ASPECTS["prix"], f"Prix {n}",
        f"<strong>{n}</strong> : {PRICE} le pot de 30 gélules (1 mois), ou <strong>{SUB}</strong> en abonnement mensuel (−15 %, sans engagement). Livraison offerte dès CHF 80.–.", buy, f"Commande {n}", s, "prix")

# --- Recommandations par besoin (formulation prudente, usage traditionnel) ---
NEEDS = [
  ("shilajit", "energie fatigue fatigue vitalite tonus forme epuise sport endurance effort coup de barre"),
  ("bacopa", "concentration memoire examen etude etudiant clarte esprit mental intellectuel focus"),
  ("ashwagandha", "stress calme serenite anxiete detente sommeil dormir nerveux zen equilibre adaptogene relaxation"),
  ("shatavari", "femme feminin cycle regles menopause hormone feminine bien-etre feminin"),
  ("tribulus", "homme masculin libido virilite musculation muscle testosterone performance"),
  ("curcuma", "digestion articulation curcumine epice poivre rituel quotidien inflammation"),
]
for slug, kw in NEEDS:
    p = P(slug)
    add(f"need-{slug}", kw + " conseil recommander quel produit choisir formule besoin", f"Conseil : {p['name']}",
        f"Dans notre collection, cette intention correspond à <strong>{p['full']}</strong> : {p['tagline']}<br>{p['short']}<br><br><small>Les compléments alimentaires ne remplacent pas un avis médical : en cas de problème de santé, parlez-en à votre médecin.</small>",
        [[f"Découvrir {p["name"]} — {PRICE}", "produits/%s.html" % slug], ["Comparer les 6 formules", "ayurveda.html#choisir"]], f"Conseil formule ({p['name']})", slug, "need")

# --- FAQ du site ---
for i, (q, a) in enumerate(FAQ):
    add(f"faq-{i}", q.lower() + " " + a.lower(), q, f"<strong>{q}</strong><br>{a}", [["Toutes les questions fréquentes", "faq.html"]], q)

# --- Thèmes généraux ---
add("ghee", "ghee beurre clarifie lait suisse alpage pourquoi matiere grasse vehicule absorption", "Le ghee suisse",
    "Le ghee est un beurre clarifié : chauffé lentement, le beurre perd son eau et ses protéines de lait pour ne garder qu'une matière grasse pure et dorée. En ayurvéda, il accompagne traditionnellement les plantes. Le ghee VK Swiss est produit en Suisse, à partir de lait suisse.",
    [["De l'alpage à la gélule", "maison.html#ghee"], ["Pourquoi plantes + ghee ?", "ayurveda.html#pourquoi"]], "Question sur le ghee")
add("ayurveda", "ayurveda ayurvedique tradition inde medecine traditionnelle plante dosha", "L'ayurvéda",
    "L'ayurvéda, « science de la vie » en sanskrit, est le système traditionnel de bien-être né en Inde il y a plusieurs millénaires. Il repose sur l'équilibre du corps et de l'esprit, l'alimentation, le rythme de vie et l'usage des plantes, très souvent associées au ghee.",
    [["Lire notre guide Ayurvéda & ghee", "ayurveda.html"]], "Question sur l'ayurvéda")
add("ksm66", "ksm-66 ksm66 extrait standardise withanolide bacoside acide fulvique saponine qualite", "Extraits standardisés",
    "Un extrait standardisé garantit une teneur constante en composés caractéristiques de la plante. Ashwagandha : extrait KSM-66®, racines uniquement, 5 % de withanolides. Bacopa : 20 % de bacosides. Shilajit : 170 mg d'acide fulvique par gélule. Tribulus : 315 mg de saponines.",
    [["En savoir plus", "ayurveda.html#ksm66"]], "Question qualité des extraits")
add("suisse", "suisse fabrique fabrication origine qualite provenance swiss made ou produit fabricant axes bassecourt", "Fabrication suisse",
    f"Les compléments VK Swiss sont fabriqués en Suisse. Le ghee est produit en Suisse à partir de lait suisse ; les plantes viennent de leurs régions d'origine (Inde, Asie). Distribution : {SITE['distrib']}.",
    [["Découvrir la Maison", "maison.html"]], "Question origine")
add("paiement", "paiement payer twint carte visa mastercard amex paypal postfinance apple pay google pay stripe securise facture", "Moyens de paiement",
    "Vous pouvez payer par <strong>TWINT</strong>, carte <strong>Visa, Mastercard, American Express</strong>, <strong>Apple Pay</strong>, <strong>Google Pay</strong>, <strong>PayPal</strong> ou <strong>PostFinance Pay</strong>. Le paiement est traité par des prestataires certifiés : nous n'avons jamais accès à vos données bancaires.",
    [["Accéder au panier", "panier.html"]], "Question paiement")
add("livraison", "livraison livrer expedition delai envoi poste frais port gratuit offerte recevoir colis suivi", "Livraison",
    "Les commandes sont expédiées depuis la Suisse par La Poste. La livraison est <strong>offerte dès CHF 80.–</strong> d'achat. Votre numéro de suivi vous est envoyé par e-mail dès l'expédition. Retrait possible à Bassecourt (JU) sur rendez-vous.",
    [["Livraison & retours", "livraison-retours.html"]], "Question livraison")
add("abo", "abonnement abonner mensuel resilier arreter pause modifier engagement reduction 15", "Abonnement",
    f"L'abonnement vous fait économiser <strong>15 % sur chaque pot</strong> ({SUB} au lieu de {PRICE}), livré tous les 30 jours. Sans engagement : vous pouvez décaler, modifier ou arrêter à tout moment depuis votre compte.",
    [["Choisir ma formule", "boutique.html"]], "Question abonnement")
add("retour", "retour rembourser remboursement echange annuler commande satisfait", "Retours",
    "Pour toute question sur une commande, un retour ou une annulation, contactez-nous avec votre numéro de commande. Pour des raisons d'hygiène, les produits ouverts ne peuvent en général pas être repris.",
    [["Livraison & retours", "livraison-retours.html"]], "Question retour / commande")
add("etranger", "etranger france monaco italie luxembourg belgique international europe livrez", "International",
    "VK Swiss est disponible en pharmacie en France, à Monaco, en Italie, au Luxembourg et en Belgique. Pour une livraison hors de Suisse, contactez-nous.",
    [["Points de vente", "points-de-vente.html#international"]], "Livraison à l'étranger")
add("pro", "revendeur pharmacie pharmacien droguerie droguiste professionnel distributeur grossiste b2b referencer cabinet therapeute", "Revendeurs",
    "Vous souhaitez référencer VK Swiss dans votre pharmacie, droguerie ou cabinet ? Envoyez-nous une demande : nous vous transmettons les conditions revendeurs.",
    [["Faire une demande revendeur", "contact.html?sujet=Demande%20revendeur#formulaire"]], "Demande revendeur")
add("contact", "contact telephone appeler numero mail email adresse joindre horaire parler conseiller humain", "Nous contacter",
    f"Appelez-nous au <a href=\"tel:{SITE['tel_href']}\">{TEL}</a> ou écrivez à <a href=\"mailto:{SITE['email']}\">{SITE['email']}</a>. Vous pouvez aussi envoyer une demande via notre formulaire, nous vous répondons rapidement.",
    [["Formulaire de contact", "contact.html#formulaire"]], "Demande de contact")
add("collection", "produit gamme collection catalogue liste formule tous quels", "La collection",
    "La collection VK Swiss compte six formules, toutes associées au ghee suisse : <strong>Ashwagandha</strong> (sérénité), <strong>Shilajit</strong> (énergie), <strong>Bacopa</strong> (concentration), <strong>Shatavari</strong> (féminin), <strong>Tribulus</strong> (masculin) et <strong>Curcuma + pipérine</strong> (rituel quotidien). " + PRICE + " le pot de 30 gélules.",
    [["Voir la collection", "boutique.html"]], "Question collection")
add("combiner", "combiner associer plusieurs deux ensemble cumuler melanger meme temps", "Combiner des formules",
    "Chaque formule est pensée pour être prise seule, à raison d'une gélule par jour. Avant d'en associer plusieurs, surtout en cas de traitement, demandez conseil à votre pharmacien ou appelez-nous.", [], "Combiner des formules", sensitive=True)
add("resultat", "resultat efficace effet combien temps quand sentir marche fonctionne", "Régularité",
    "Les compléments s'inscrivent dans la durée : l'essentiel est la régularité, une gélule chaque jour à la même heure, pendant au moins un mois. Chaque personne est différente ; nous ne promettons pas de résultat.", [["Choisir ma formule", "boutique.html"]], "Question régularité")
add("conservation", "conserver conservation temperature frigo peremption date stocker", "Conservation",
    "À conserver à température ambiante (15–25 °C), hors de portée des jeunes enfants. La date de durabilité figure sur l'emballage.", [], "Conservation")
add("vegan", "vegan vegetalien vegetarien halal casher gelatine poisson animal", "Régimes alimentaires",
    "Les gélules contiennent du ghee (matière grasse laitière) et une enveloppe en gélatine de poisson : elles ne conviennent pas aux régimes végétaliens. Pour les régimes religieux, contactez-nous.", [], "Question régime alimentaire")
add("sante", "maladie medicament traitement medecin diagnostic douleur diabete tension hypertension cancer grossesse soigner guerir symptome",
    "Santé", "Je ne peux pas donner d'avis médical. Les compléments alimentaires ne remplacent ni un traitement ni une alimentation variée. Si vous suivez un traitement, êtes enceinte ou avez un problème de santé, demandez conseil à votre médecin ou pharmacien avant toute prise. Chaque fiche produit détaille ses contre-indications.",
    [["Voir les précautions par produit", "boutique.html"]], "Question santé", sensitive=True)

add("poids", "maigrir mincir minceur poids kilo regime perte perdre graisse brule", "Poids",
    "Aucune formule VK Swiss n'est conçue pour la perte de poids, et nous ne faisons pas de promesse en ce sens. Pour un accompagnement, parlez-en à votre médecin ou à un diététicien. Nous pouvons en revanche vous présenter nos six formules et leurs usages traditionnels.",
    [["Voir la collection", "boutique.html"]], "Question poids")
add("choisir", "choisir choix aide aider hesite hesitation conseil conseiller quelle formule laquelle prendre recommander debuter commencer", "Choisir sa formule",
    "Chaque formule correspond à une intention : <strong>Shilajit</strong> pour l'énergie, <strong>Bacopa</strong> pour la concentration, <strong>Ashwagandha</strong> pour la sérénité, <strong>Shatavari</strong> pour le bien-être féminin, <strong>Tribulus</strong> pour la vitalité masculine et <strong>Curcuma</strong> pour un rituel quotidien. Dites-moi ce que vous recherchez (par ex. « je manque d'énergie ») et je vous oriente.",
    [["Comparer les 6 formules", "ayurveda.html#choisir"]], "Aide au choix d'une formule")
add("hello", "bonjour salut hello bonsoir coucou aide aider", "Bonjour",
    "Bonjour ! Je réponds à vos questions sur les formules VK Swiss, le ghee suisse, les précautions d'emploi, la commande, la livraison et nos points de vente. Que souhaitez-vous savoir ?", [], "Demande de conseil")

# --- Points de vente (index pour la recherche par ville / NPA) ---
STORE_LIST = [[n, a, c] for c, lst in STORES.items() for n, a in lst]

SUGGEST = ["Quelle formule contre la fatigue ?", "Qu'est-ce que le ghee ?", "Je suis enceinte, puis-je en prendre ?",
           "Payer avec TWINT ?", "Pharmacie à Lausanne", "Prix de l'ashwagandha"]
