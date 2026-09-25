# Audit complet — Maison L'Émeraude (thème Shopify)

Date : 25 septembre 2026 · Périmètre : tout le code du dépôt (`layout/`, `sections/`, `templates/`, `assets/`, `config/`, `locales/`).

Hors périmètre, car absent du dépôt : l'admin Shopify (pages légales, réductions, paramètres de paiement et de livraison, bannière cookies, apps installées). Les points qui en dépendent sont signalés « à vérifier dans l'admin ».

Légende : 🔴 critique (risque juridique ou fonctionnalité cassée) · 🟠 important · 🟡 amélioration

---

## Statut des corrections (mise à jour)

Tous les points corrigeables dans le code ont été traités. Validation : Shopify Theme Check → **0 erreur, 0 avertissement**. JSON et schémas valides. Sélection de variante et en-tête sticky testés dans Chromium.

| Point | Statut |
|---|---|
| 1.1 Faux `aggregateRating` | ⏸️ **Laissé tel quel à la demande** — à retirer dès que possible |
| 1.2 « goutte d'émeraude » | ✅ reformulé (« cristal vert émeraude ») |
| 1.3 Zircons / peaux sensibles | ✅ « oxydes de zirconium », allégation « peaux sensibles » retirée · ⚠️ « doré à l'or fin » : épaisseur à confirmer auprès du fournisseur |
| 1.4 Offre 1+1 | ✅ réglages globaux `offer_active` + `offer_end_date` (bandeau, fiche, panier, menu) · ⚠️ créer la réduction « Achetez X, obtenez Y » dans l'admin |
| 1.5 Pages légales | ✅ pied de page basé sur les politiques Shopify · ⚠️ remplir Paramètres → Politiques (CGV, mentions légales, médiateur) |
| 1.6 RGPD | ✅ polices auto-hébergées, lien confidentialité newsletter · ⚠️ activer la bannière cookies Shopify |
| 2.1 Email | ✅ `contact@maisonlemeraude.fr` partout (le domaine .com n'existe pas) |
| 2.2 Livraison / retours | ✅ réglages `free_shipping` / `free_returns` (décochés par défaut) pilotant site + schéma · TTC + frais de port au panier |
| 2.3 Divers | ✅ faux bouton retiré de l'image d'offre (recadrée), liens sociaux nettoyés, `twitter:site` en réglage, fautes corrigées |
| 3.x Bugs | ✅ tous corrigés (sticky, variantes, style dupliqué, moyenne des avis, étoiles, padding sticky ATC, scroll-margin, image panier, remises au panier) · microdata supprimée |
| 4.x SEO | ✅ `share_image`, og:image en https + vraies dimensions, logo schema, images produit, templates `search` et `collection`, noindex panier/recherche/404 |
| 5.x Performance | ✅ images ÷ 5 (≈ 5 Mo → ≈ 1 Mo), variantes 600 px + `srcset`, `width`/`height` partout, preload `imagesrcset`, 3 polices variables au lieu de 9 fichiers |
| 6.x Accessibilité | ✅ FAQ en boutons `aria-expanded`, vignettes en boutons, menu mobile (Échap + focus), contrastes ≥ 4,5:1, focus visible, lien d'évitement, bandeau pausable et lu par les lecteurs d'écran, titres |
| 7.x Code | ✅ CSS dupliqué supprimé, `settings_schema.json` complet, `logo_max_width` branché, délais centralisés |

**À faire dans l'admin Shopify** : 1) cocher *Livraison offerte* / *Retours gratuits* si c'est le cas ; 2) saisir la date de fin de l'offre ; 3) créer la réduction automatique BXGY ; 4) remplir les politiques ; 5) ajouter une image de partage ; 6) activer la bannière cookies.

---

## Synthèse

| Domaine | État | Point principal |
|---|---|---|
| Conformité / juridique | 🔴 | Avis clients inventés dans les données structurées (4,9★ / 47 avis) |
| Contenu / cohérence | 🔴 | Deux adresses email différentes (.fr et .com) |
| Fonctionnel | 🟠 | En-tête « sticky » cassé ; choix de variante ignoré |
| SEO | 🟠 | Pas d'image de partage sur l'accueil ; og:image invalide |
| Performance | 🟠 | Environ 5 Mo d'images sur l'accueil (PNG de 2,4 Mo et 1,4 Mo, logo de 285 Ko) |
| Accessibilité | 🟠 | FAQ et vignettes inutilisables au clavier ; contrastes insuffisants |
| Code / maintenance | 🟡 | 130 lignes de CSS dupliquées ; `settings_schema.json` vide |

---

## 1. Conformité & juridique

### 🔴 1.1 Faux avis dans les données structurées Google
`layout/theme.liquid:110-116` injecte sur chaque page produit :
```json
"aggregateRating": { "ratingValue": "4.9", "reviewCount": "47" }
```
Le site indique pourtant (section Avis, `sections/reviews.liquid:126-130`) que « la Maison vient d'ouvrir », que les premiers avis ne sont pas encore arrivés et qu'« aucun avis ne sera inventé ».
- **Risque légal** : un avis fictif est une pratique commerciale trompeuse (Code de la consommation, art. L121-2 et L121-4, 21°). La DGCCRF la sanctionne activement.
- **Risque SEO** : Google peut appliquer une action manuelle pour données structurées trompeuses et retirer tous les extraits enrichis du site.
- **Correctif** : supprimer le bloc `aggregateRating` de `theme.liquid`. La section `reviews.liquid` génère déjà une note calculée à partir des vrais avis, dès qu'il y en aura.

### 🔴 1.2 Description qui présente la pierre comme une émeraude
`templates/index.json` (section `piece-intro`) contient : « Une **goutte d'émeraude** entourée d'un halo de zircons… ». Le même texte sert de valeur par défaut dans `sections/piece-intro.liquid:58`.
Le reste du site explique pourtant, à juste titre, qu'il s'agit d'un cristal synthétique. Le décret n° 2002-65 interdit d'utiliser le nom d'une pierre naturelle pour une pierre synthétique sans le qualificatif « synthétique ».
→ Reformuler, par exemple : « Une goutte de cristal vert émeraude… ».

### 🟠 1.3 Allégations produit à justifier
- **« Zircons blancs »** (`index.json`, FAQ, fiche) : le zircon est une pierre naturelle. S'il s'agit d'oxyde de zirconium (cubic zirconia), la dénomination correcte est « oxyde de zirconium » ou « zirconium synthétique ». À vérifier auprès du fournisseur.
- **« Finition dorée à l'or fin »** : ces mentions sont réglementées et exigent une épaisseur minimale d'or. Demander au fournisseur une fiche technique qui la précise.
- **« Convient aux peaux sensibles »** (FAQ q3) : l'acier inoxydable contient du nickel. Cette allégation doit s'appuyer sur un test de libération du nickel (REACH, annexe XVII). Sinon, l'adoucir.

### 🟠 1.4 Offre « 1 acheté · 1 offert » floue
- Aucune date de fin n'est indiquée (« pendant la période de lancement »). Une promotion doit afficher clairement sa durée et ses conditions.
- Le cas d'une commande de 2 pièces ou plus n'est pas clair : « chaque commande » (FAQ) et « un seul bijou supplémentaire par commande » (disclaimer) se contredisent à moitié.
- La pièce offerte **n'apparaît ni dans le panier ni dans la commande** : c'est du texte seulement. Conséquences : stock Shopify faux, facture incomplète, oubli possible à l'expédition.
  → Créer dans l'admin une réduction automatique « Achetez X, obtenez Y » (Y = même produit, 100 %). La seconde pièce apparaîtra alors comme ligne à 0 €.
- `sections/main-cart.liquid:17` affiche « Votre commande inclut une seconde pièce offerte » sans aucune condition, même si l'offre est terminée.
- `sections/main-product.liquid:43-49` : si un prix barré (`compare_at_price`) est utilisé, le prix de référence doit être le prix le plus bas pratiqué dans les 30 jours précédant la réduction (art. L112-1-1, directive Omnibus).

### 🟠 1.5 Pages légales conditionnelles, à vérifier dans l'admin
`sections/site-footer.liquid:134-137` n'affiche les liens CGV, Confidentialité, Retours et Mentions légales **que si** des pages avec ces handles exactes existent (`cgv`, `privacy`, `returns`, `mentions-legales`). Si l'une manque, le lien disparaît sans avertissement. Obligations à vérifier :
- mentions légales (LCEN art. 6) ;
- CGV avec le droit de rétractation de 14 jours et le formulaire type ;
- garanties légales (conformité et vices cachés) ;
- **médiateur de la consommation** (obligatoire, art. L612-1) ;
- politique de confidentialité.
→ Utiliser plutôt les politiques natives de Shopify (`shop.privacy_policy`, `shop.refund_policy`, `shop.terms_of_service`, `shop.shipping_policy`), qui sont toujours présentes.

### 🟠 1.6 RGPD
- **Google Fonts** est chargé depuis les serveurs de Google (`theme.liquid:194`), ce qui transmet l'adresse IP des visiteurs aux États-Unis sans consentement. La justice européenne a déjà sanctionné cette pratique. → Auto-héberger les polices, par exemple via `assets/`.
- Newsletter (`sections/newsletter.liquid:28`) : il n'y a aucun lien vers la politique de confidentialité à côté du champ d'inscription.
- Bannière cookies : le thème n'en contient pas. Vérifier que la bannière Shopify « Confidentialité des clients » est activée dans l'admin.

---

## 2. Contenu & cohérence

### 🔴 2.1 Deux adresses email différentes
- `contact@maisonlemeraude.**fr**` : `theme.liquid:77` (Organization schema) et `faq.liquid:157`.
- `contact@maisonlemeraude.**com**` : `site-footer.liquid:17,102,176` (visible par les clients).

L'une des deux ne fonctionne probablement pas. Choisir la bonne et l'utiliser partout.

### 🟠 2.2 Informations de livraison et de retour incohérentes avec le schéma
Le schéma produit (`theme.liquid:129-159`) déclare une **livraison gratuite** (`value: 0`) et des **retours gratuits** (`FreeReturn`). Le site ne mentionne nulle part ces deux avantages. Si c'est vrai, l'afficher (c'est un argument de vente). Sinon, corriger le schéma pour éviter une information trompeuse.
Le panier n'indique pas non plus « Frais de livraison calculés à l'étape suivante » ni « TTC ».

### 🟡 2.3 Divers
- `sections/offer.liquid` : l'image `offer-lancement.png` contient un faux bouton « PROFITEZ DE L'OFFRE », non cliquable, juste au-dessus du vrai bouton. Cela prête à confusion.
- Liens sociaux avec paramètres de tracking (`?stkn=…&utm_source=qr`, `?mibextid=…`) dans `site-footer.liquid:106-107`. Les nettoyer.
- `twitter:site = @maisonlemeraude` (`theme.liquid:37`) : vérifier que ce compte existe.
- Faute dans le texte par défaut : « belle à voir, **doux** à porter » (`storytelling.liquid:5`). Elle est masquée par `index.json`, mais réapparaîtrait si le réglage était vidé.
- `site-header.liquid:70` : « 0 article**s** ». En français, on écrit « 0 article ».

---

## 3. Bugs fonctionnels

### 🟠 3.1 L'en-tête « sticky » ne colle pas ✅ vérifié dans Chromium
`assets/theme.css:1` : `overflow-x: hidden` appliqué à la fois sur `html` et `body` transforme `body` en conteneur de défilement, ce qui annule `position: sticky` sur l'en-tête.
Test : après un défilement de 1500 px, l'en-tête est à −1460 px (hors écran). Avec `overflow-x: clip`, il reste bien à 0.
→ Remplacer `overflow-x: hidden` par `overflow-x: clip`.

### 🟠 3.2 Le choix de variante est ignoré
`sections/main-product.liquid:63-76` : les `<select name="options[…]">` ne sont reliés à rien. Le champ caché `id` contient toujours la première variante, donc c'est toujours elle qui est ajoutée au panier. Aucun impact tant que le produit n'a qu'une variante, mais c'est bloquant dès qu'on en ajoute une (longueur, couleur…).

### 🟡 3.3 Autres
- `main-product.liquid:84-85` : l'attribut `style` est dupliqué sur le bouton lorsque le produit est épuisé. Le second est ignoré, donc le bouton perd sa mise en page.
- `main-product.liquid:3` : `content="{{ product.description | strip_html }}"` n'est pas échappé. Un guillemet dans la description casse le HTML. → Ajouter `| escape` (même chose à la ligne 2).
- `reviews.liquid:13` : `rating_sum | divided_by: review_count` fait une division **entière** (par exemple 9/2 = 4 au lieu de 4,5). → Utiliser `rating_sum | times: 1.0 | divided_by: review_count`.
- `reviews.liquid:64-68` : l'en-tête affiche toujours 5 étoiles pleines, et `{{ total }} avis` compte aussi les blocs vides.
- La barre d'ajout au panier fixe (mobile) masque le bas du pied de page, car il n'y a pas de `padding-bottom` compensatoire.
- Les liens d'ancre (`#faq`, `#offre`…) arrivent sous l'en-tête (une fois celui-ci réparé) → ajouter `scroll-margin-top` sur les sections.
- `main-cart.liquid:34` : `item.image` peut être vide, ce qui donne une image cassée.
- Les réductions éventuelles ne sont pas affichées dans le panier (`cart.cart_level_discount_applications`, `item.line_level_discount_allocations`).

---

## 4. SEO

### 🟠 4.1 Pas d'image de partage sur l'accueil
`theme.liquid:29-33` utilise `settings.share_image`, mais `config/settings_schema.json` est vide (`[]`) : ce réglage n'existe pas. Résultat : aucun `og:image` sur la page d'accueil, et un aperçu sans image sur WhatsApp, Facebook et Instagram.

### 🟠 4.2 og:image invalide
- `image_url` renvoie une URL relative au protocole (`//cdn.shopify.com/…`), que Facebook et LinkedIn refusent. → Ajouter `| prepend: 'https:'`, comme c'est déjà fait dans le JSON-LD.
- `og:image:height = 630` est codé en dur alors que les photos sont carrées ou verticales.

### 🟡 4.3 Données structurées
- Le Product est déclaré **deux fois** : en microdata incomplète (`main-product.liquid:1-4`, sans `offers`) et en JSON-LD. Google Search Console signalera des erreurs. → Supprimer la microdata.
- Un second Product JSON-LD, sans `offers` ni `image`, est émis sur l'accueil dès qu'un avis existe (`reviews.liquid:14-48`) → ce n'est pas valide pour les extraits enrichis produit.
- Le logo de l'Organization est déclaré en 400×100 alors qu'il mesure 1090×332.
- La liste `image` du Product répète l'image principale.
- `SearchAction` pointe vers `/search`, mais le thème n'a pas de template `search`. → Le supprimer ou créer ce template.
- FAQPage : depuis 2023, Google n'affiche plus les extraits FAQ que pour les sites officiels et de santé. Ce n'est pas nuisible, mais n'en attendez pas de gain.

### 🟡 4.4 Templates manquants
Il n'existe pas de template `collection`, `search`, `list-collections`, `blog`, `article`, `password`, `gift_card` ni `customers/*`. Les URL `/collections/all`, `/search` et `/account` s'afficheront mal ou avec le rendu par défaut de Shopify.

---

## 5. Performance (Core Web Vitals)

### 🟠 5.1 Images beaucoup trop lourdes
| Fichier | Poids | Remarque |
|---|---|---|
| `ecrin.png` | **2,4 Mo** | photo en PNG → JPG ou WebP, environ 150 Ko |
| `offer-lancement.png` | **1,4 Mo** | idem |
| `logo.png` | **285 Ko** | affiché en 130-160 px → SVG ou PNG à 320 px, moins de 15 Ko |
| `boutique-paris.jpg`, `closeup.jpg`, `paris.jpg` | 200-275 Ko chacun | servis en taille réelle à tous les écrans |

Les fichiers de `assets/` ne sont **pas** redimensionnés par Shopify. → Téléverser ces photos dans *Contenu → Fichiers* et les servir via `image_url` + `srcset`, comme c'est déjà fait pour les réglages `image_picker`.

### 🟠 5.2 Mise en page qui saute (CLS)
Il manque `width`/`height` sur le logo (`site-header.liquid:27-33, 49-66`), l'image principale produit, les vignettes, `piece-intro`, `detail-macro` et `packaging`.
Le héros déclare `width="1920" height="1080"` alors que `paris.jpg` mesure 1145×1374.

### 🟡 5.3 Divers
- Préchargement produit (`theme.liquid:202`) : il précharge la version 1000 px alors que le mobile choisit la version 600 px, donc l'image est téléchargée deux fois. → Utiliser `imagesrcset` et `imagesizes`.
- Google Fonts charge 9 fichiers et bloque le rendu. → Réduire les graisses (300, 400, 400 italique) et auto-héberger (cf. 1.6).
- Le logo est chargé deux fois (versions desktop et mobile, toutes deux en `loading="eager"`).
- Environ 130 lignes de CSS dupliquées (voir 7.1).

---

## 6. Accessibilité (WCAG 2.1 AA)

### 🟠 6.1 Éléments interactifs inaccessibles au clavier
- **FAQ** (`faq.liquid:13`) : chaque question est une `<div onclick>`, sans focus, sans Entrée ni Espace et sans `aria-expanded`. → Utiliser `<details><summary>` ou `<button aria-expanded>`.
- **Vignettes** de l'accueil (`piece-intro.liquid:34-39`) et de la page produit (`main-product.liquid:23-29`) : ce sont des `<div>` ou `<img>` cliquables. → Utiliser des `<button>`.
- **Menu mobile** : pas de fermeture avec Échap, pas de piège de focus, pas d'`aria-controls`.
- Input newsletter : `outline: none` sans style de focus de remplacement.

### 🟠 6.2 Contrastes insuffisants (le minimum est 4,5:1)
| Élément | Ratio |
|---|---|
| Or `#B08D57` sur crème (tous les sur-titres, 10 px) | 2,9:1 |
| Gris `#9c968a` (libellés, dates, « Retirer ») | 2,8:1 |
| Mention légale de la newsletter (`.25` sur fond sombre) | 2,2:1 |
| Copyright et intitulés du footer (`.28`) | 2,4:1 |
| Accroche et email du footer (`.40`) | 3,7:1 |
| Mention « Bientôt » dans les avis | 1,5:1 |

Beaucoup de textes font 9 à 10,5 px, ce qui aggrave le problème.

### 🟡 6.3 Divers
- La bannière défilante est entièrement en `aria-hidden` : l'offre n'est jamais lue par les lecteurs d'écran. Elle ne peut pas non plus être mise en pause sur mobile (WCAG 2.2.2).
- Il n'y a pas de lien « Aller au contenu ».
- La newsletter utilise un `<h3>` sans `<h2>` avant lui dans le pied de page.
- `main-404.liquid` et `main-page.liquid` utilisent `font-weight: 420`, qui n'est pas chargé : le navigateur synthétise la graisse.
- Le texte alternatif du héros décrit bien la photo.

---

## 7. Code & maintenance

### 🟡 7.1 CSS dupliqué
`assets/theme.css:297-425` est une copie exacte des lignes 167-295 (tout le bloc « DESIGN UPGRADE »). → Supprimer la copie.

### 🟡 7.2 Configuration du thème
- `config/settings_schema.json` vaut `[]` : il n'y a pas de `theme_info` ni de réglages globaux (image de partage, couleurs, polices).
- Réglage mort : `logo_max_width` (`site-header.liquid:143-151`) n'est jamais utilisé.
- Les réglages `stone`, `metal` et autres de `detail-macro` sont en double avec ceux de `main-product` : il faut modifier les mêmes informations à deux endroits.
- Les informations « 30 jours », « 24-48 h » et « 3 à 7 jours » sont codées en dur dans environ 8 fichiers, alors que certaines sections ont un réglage. → Les centraliser dans `settings_schema.json`.
- `locales/fr.default.json` existe, mais presque tout le texte est codé en dur dans les sections.
- Beaucoup de styles en ligne (`style="…"`) et de `onmouseover`/`onmouseout`, ce qui complique la maintenance. → Les déplacer dans `theme.css` avec `:hover` et `:focus-visible`.

### 🟡 7.3 Outillage
Il n'y a ni `.shopifyignore`, ni `.theme-check.yml`, ni CI. Lancer `shopify theme check` révélerait automatiquement une bonne partie de ces points.

---

## Plan d'action recommandé

**Tout de suite (moins d'une heure)**
1. Supprimer le faux `aggregateRating` (1.1).
2. Corriger « goutte d'émeraude » (1.2).
3. Unifier l'adresse email (2.1).
4. Réparer l'en-tête sticky : `overflow-x: clip` (3.1).
5. Ajouter `https:` aux og:image et créer le réglage `share_image` (4.1, 4.2).

**Cette semaine**

6. Convertir et compresser les images (5.1), puis ajouter les `width`/`height` (5.2).
7. Réduction automatique « Achetez X, obtenez Y » avec une date de fin affichée (1.4).
8. Vérifier les pages légales et le médiateur dans l'admin, puis passer aux politiques natives de Shopify (1.5).
9. Rendre la FAQ et les vignettes accessibles au clavier (6.1) et relever les contrastes (6.2).

**Ensuite**

10. Auto-héberger les polices (1.6, 5.3).
11. Nettoyer le CSS dupliqué, la microdata et les réglages (7.x, 4.3).
12. Brancher la sélection de variante (3.2) avant d'ajouter une seconde variante.
