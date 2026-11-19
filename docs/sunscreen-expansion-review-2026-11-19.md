# Extension locale des solaires Open Beauty Facts — 19 novembre 2026

Cette extension est intégrée uniquement à la copie locale de Swan. Aucun déploiement, push GitHub ou changement Drive. Le catalogue partagé de Loredana n'a pas été remplacé.

## Résultat

- 630 enregistrements renvoyés sur sept pages de l'API publique de la catégorie sunscreen, soit 462 codes uniques après dédoublonnage. Il s'agit d'un instantané de recherche, pas d'une garantie d'exhaustivité de la base.
- 5 nouveaux produits intégrés : Avène Intense Protect SPF50+, La Roche-Posay Anthelios UVMune 400 anti-taches SPF50+, La Roche-Posay Anthelios UVAIR SPF50+, Ducray Keracnyl UV SPF50+, La Rosée lait solaire SPF50+.
- Catalogue local : 499 produits, dont 64 lignes de solaires au niveau mondial. Le modèle prépare 29 solaires France/UE et en autorise 12 après les vérifications de rôle et de SPF, contre 7 dans le premier essai local et 5 dans la version publique.
- 4 options avec une mention sans parfum revue sont disponibles pour le filtre sensibilité/réactivité, contre 2 auparavant dans l'essai local. Une mention sans parfum ne garantit pas la tolérance individuelle.

## Méthode reprise de Loredana

Le fichier scripts/loredana_preparation.py reprend les listes et fonctions de son notebook V2 pour la séparation/normalisation INCI, la texture, les actifs, les signaux et la génération de descriptions. Les cellules d'exécution, décisions et écritures du notebook ne sont pas exécutées. Les exclusions et orientations de la version publique, notamment grossesse/allaitement, sont conservées.

Les nouveaux produits exigent une identification de la variante, un usage visage ou visage/corps, un SPF déclaré >=30 corroboré par une fiche de marque ou de vendeur primaire, un filtre UV identifiable, au moins 5 ingrédients, une couverture CosIng >=50%, un pays France/UE, et aucune exclusion connue de la politique. Le SPF est une déclaration vérifiée dans les sources, pas un test de laboratoire effectué par nous. Aucun prix/budget inconnu n'est inventé.

Les ingrédients d'Open Beauty Facts restent une source communautaire avec des erreurs OCR possibles. La règle de couverture est celle du notebook, pas une garantie de transcription parfaite. Les noms commerciaux et le caractère sans parfum ont été vérifiés séparément. Les usages et la réglementation ne sont pas intégralement validés par un contrôle CosIng.

La matrice d'ingrédients est étendue aux nouveaux codes. Les colonnes existantes sont préservées, et de nouveaux ingrédients reconnus apparaissant dans au moins cinq produits peuvent être ajoutés. Les lignes existantes du catalogue sont conservées. Le script est répétable à partir des sauvegardes baseline dans local_review.

## Interface et exclusions

Les nouvelles descriptions, badges, photos de face sélectionnées par OBF et recherches Google Shopping sont disponibles dans les résultats locaux. Aucun lien de recherche n'est présenté comme un achat ou un stock garanti. L'image peut manquer ou ne pas se charger ; aucune photo de code-barres ou d'ingrédients n'est substituée volontairement. Les photos sélectionnées dans OBF ne constituent pas une validation visuelle complète de chaque contribution.

Le SVR Sun Secure examiné (3662361003204) reste hors catalogue : couverture CosIng inférieure à 50% à cause de l'INCI transcrit. Les autres candidats non intégrés sont conservés dans l'audit avec les motifs : déjà présent, marché hors France/UE, marque/nom manquant, liste courte ou peu reconnue, filtre UV absent, ou variante/usage/SPF non revus. Un statut Hold signifie manque de preuves, pas produit dangereux.

## Sources exactes des cinq ajouts

- Avène 3282770141214 : https://world.openbeautyfacts.org/product/3282770141214 et https://www.pharmacie-place-ronde.fr/protection-solaire-indice-fort/12304-intense-protect-fluide-solaire-sans-parfum-spf-50-avene.html
- Anthelios anti-taches 3337875917407 : https://world.openbeautyfacts.org/product/3337875917407 et https://www.aesiel.com/protection-solaire/3914-la-roche-posay-anthelios-50-uvmune-400-fluide-anti-taches-50ml.html . Cette pharmacie indiquait rupture de stock lors de la consultation, sans conclusion sur les autres vendeurs.
- Anthelios UVAIR 3337875932349 : https://world.openbeautyfacts.org/product/3337875932349 et https://www.laroche-posay.fr/anthelios/anthelios-uvair-spf50-/3337875932349.html
- Ducray 3282770145175 : https://world.openbeautyfacts.org/product/3282770145175 et https://www.easypara.com/fluide-anti-imperfections-spf50-50ml-keracnyl-oily-skin-with-a-tendency-to-acne-ducray.html
- La Rosée 3770000717587 : https://world.openbeautyfacts.org/product/3770000717587 et https://www.parapharmelle.com/fr/parapharmelle/11046-la-rosee-lait-solaire-spf50-3770000717587.html

Source des données : Open Beauty Facts, ODbL. Photos : contributeurs Open Beauty Facts, CC BY-SA. Sources et date 2026-11-19 conservées dans les fichiers d'audit et les lignes ajoutées.

## Fichiers et vérification

- local_review/obf_sunscreen_candidate_audit.csv : audit des 462 candidats uniques.
- local_review/obf_sunscreen_additions.csv : nouvelles lignes et preuves.
- local_review/obf_extension_test_results.json : résultats des 135 combinaisons.
- scripts/expand_obf_sunscreens.py : préparation reproductible.
- tests/test_obf_extension.py : intégrité des données, alignement matrice et contrôles des ajouts.

Les tests vérifient le SPF, le filtre sans parfum pour sensibilité/réactivité, les données contradictoires, les descriptions, les doublons, la conservation des anciens produits et le maintien des choix nettoyant/crème hydratante sur les profils de référence.

Aperçu local : http://127.0.0.1:8530/

## Ajustement demandé après essai local

Les textes « Swan prioritized… » et les alternatives ont été retirés des cartes. Les solaires à égalité après les scores ET critères de profil/qualité sont désormais départagés aléatoirement. Le navigateur conserve le dernier code solaire dans la session et l'évite si une autre option est exactement à égalité. Aucune donnée de santé ni profil n'est conservé dans ce stockage. Si un seul produit est le meilleur classé, il reste sélectionné. Les comptages de premier choix précédents décrivent l'état antérieur à cet ajustement. Deux tests supplémentaires vérifient la variété entre ex-aequo et la conservation d'un meilleur résultat unique.
