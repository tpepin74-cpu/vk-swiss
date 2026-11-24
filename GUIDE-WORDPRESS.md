# VK Swiss — Reconstruction WordPress / Elementor Pro / WooCommerce

Maquette de référence : ce dépôt (HTML statique). Cible : `vk-swiss.ch` (pré-prod conseillée : `vk.cerfalunettes.fr`).

## 1. Socle
- WordPress + thème **Hello Elementor** + **Elementor Pro** (header, footer, fiche produit et archive en *Theme Builder*).
- **WooCommerce** (devise CHF, TVA suisse 2,6 % taux réduit pour denrées alimentaires, à valider avec la fiduciaire).
- **Rank Math Pro** (SEO + schémas), **UpdraftPlus**, **WP Umbrella**, cache (LiteSpeed/WP Rocket), WebP.
- Réglages globaux Elementor (pas de CSS ad hoc) :
  - Couleurs : Encre `#111111`, Rouge suisse `#E30F23`, Gris `#6F6F6F`, Ligne `#E8E6E6`, Pierre `#F6F5F3`, + couleurs plantes : Ashwagandha `#42C0EF`, Shilajit `#634897`, Bacopa `#61A331`, Shatavari `#D78AB5`, Tribulus `#F5D94C`, Curcuma `#E77F0A`.
  - Typo : titres **Cormorant Garamond** 300 ; interface **Jost** 300/400, capitales espacées 0.2em pour nav, boutons, sur-titres.
  - Boutons : rectangulaires, 52 px, capitales 13 px espacées (desktop) ; arrondis 12 px sur mobile.

## 2. Pages
Accueil · La collection (archive produits) · 6 fiches produits · La Maison · Ayurvéda & ghee (guide GEO) · Points de vente · FAQ · Contact · Panier/Commande (WooCommerce) · Mentions légales · CGV · Confidentialité (nLPD) · Livraison & retours.
Points de vente : CPT JetEngine « Point de vente » (nom, adresse, canton, pays) + Listing + filtres JetSmartFilters (canton, recherche).

## 3. Paiements suisses (WooCommerce)
| Moyen | Extension recommandée |
|---|---|
| TWINT | **Datatrans** ou **Payrexx** (passerelle suisse, TWINT + PostFinance + cartes) — ou plugin TWINT officiel via le PSP |
| Cartes Visa / Mastercard / Amex, Apple Pay, Google Pay | **WooCommerce Stripe Gateway** (Payment Request Buttons activés) |
| PayPal | **WooCommerce PayPal Payments** |
| PostFinance Pay | Datatrans / Payrexx / PostFinance Checkout |
| Abonnement −15 % | **WooCommerce Subscriptions** (ou *Subscriptions for WooCommerce*) + Stripe/Datatrans tokenisé |
Paiement express (TWINT / Apple Pay / Google Pay) sur fiche produit et panier : boutons express Stripe + bouton TWINT du PSP.
Livraison : « Livraison gratuite » dès CHF 80 (montant à valider), La Poste PostPac Priority en dessous ; retrait à Bassecourt.

## 4. Formulaire de contact (Elementor Pro)
Widget **Formulaire**, nom « Demande VK Swiss », champs (ID) :
`nom` (texte, requis) · `email` (e-mail, requis) · `telephone` (tél.) · `sujet` (liste : Demande de conseil, Choix d'une formule, Question sur une commande, Abonnement, Demande revendeur, Presse & partenariats, Autre demande) · `message` (zone de texte, requis) · `rappel` (case) · `consentement` (acceptation, requise).
**Actions après envoi :**
1. **Collecter les soumissions** → toutes les demandes sont stockées dans *Elementor › Envois*.
2. **E-mail** → à `info@vk-swiss.ch`, objet `[VK Swiss] [field id="sujet"] — [field id="nom"]`, Reply-To `[field id="email"]`.
3. **E-mail 2** → accusé de réception au client.
4. (optionnel) Webhook / Mailchimp.
Pré-remplissage du sujet depuis le conseiller : valeur par défaut du champ `sujet` = `[elementor-tag name="request-arg"]`… ou via *Dynamic Tags › Request Parameter* (`sujet`). reCAPTCHA v3 (clés gérées par l'agence). SMTP : WP Mail SMTP.

## 5. Conseiller VK (arbre de décision)
- Fichiers `assets/js/data.js` (arbre `tree`) et `assets/js/app.js` (moteur) à enqueue via un snippet (Code Snippets) ou widget HTML global dans le footer Theme Builder.
- Chaque nœud : texte, options, liens vers pages, `topic` → le bouton « Écrire » ouvre `/contact/?sujet=<topic>#formulaire` (pré-rempli), le bouton « Appeler » `tel:+41792890449`.
- Aucune IA, aucune donnée stockée : 100 % déterministe, conforme nLPD.

## 6. Version mobile « application »
- Barre d'onglets fixe (Accueil, Boutique, Conseiller, Panier, Pharmacies) : section Elementor *sticky bottom*, visible < 860 px.
- Header mobile compact, carrousels produits en *scroll-snap*, panier et conseiller en *bottom sheet*, bouton d'achat collant au-dessus de la barre.
- PWA : `manifest.webmanifest` + `sw.js` (plugin *Super PWA* ou fichiers à la racine), `theme-color`, icônes 192/512 → « Ajouter à l'écran d'accueil » = vraie app.

## 7. SEO / GEO
- Rank Math : titres et métas repris de la maquette, schémas Product (prix CHF, disponibilité), Organization, BreadcrumbList, FAQPage (FAQ + guide), ItemList (points de vente).
- `llms.txt` à la racine (résumé factuel pour les moteurs IA).
- Guide « Ayurvéda & ghee » : réponses courtes en tête de section, tableau comparatif des formules → très bien repris par les moteurs génératifs.
- hreflang fr-CH, puis versions DE / IT / EN (WPML ou Polylang).

## 8. Conformité (à valider avant mise en ligne)
- Allégations : textes rédigés en « usage traditionnel » ; retirer « FDA Approved » et le « +85 % d'absorption » tant qu'ils ne sont pas étayés (ODALOUs / OIDAl).
- Placeholders `[…]` : délais et tarifs de livraison, IDE/UID, hébergeur, CGV, politique de confidentialité, points de vente internationaux.
