# 0003 : Les ADR du dépôt sont dans adr/, hors de la documentation Sphinx

- **Statut :** Accepté
- **Date :** 2026-11-12

## Contexte

Les ADR de ce dépôt tracent les décisions prises sur le matériel de formation (Makefile, packaging, organisation du dépôt). Ils sont réservés aux formateurs et ne vont dans aucune branche de TP.
Ils étaient rangés dans `docs/adr/`, à l'intérieur de `docs/`, le dossier de la documentation Sphinx du projet Titanic, objet du TP3.

Le TP3 propose maintenant d'écrire des pages en Markdown avec MyST, et la solution de `dev` l'active pour la page d'architecture et son schéma Mermaid. Dès que MyST est actif, Sphinx lit tous les fichiers `.md` de `docs/`, y compris les ADR. Comme ils ne figurent dans aucun `toctree`, `sphinx-build -W` (`make sphinx`, `make test-tps`, la CI des branches 5 et suivantes) échoue : « document isn't included in any toctree ».

Les ajouter au `toctree` les publierait dans la documentation du projet Titanic, qui n'est pas leur place. Les exclure (`exclude_patterns`) laisserait dans la solution des apprenants une ligne qui ne concerne que le dépôt de formation. Enfin, les branches 4, 5, 6 et `final_state` reçoivent le dossier `docs/` de `dev`, à condition d'en retirer `docs/adr/` à la main.

## Décision

- Les ADR du dépôt sont dans `adr/`, à la racine.
- `docs/` ne contient que la documentation du projet Titanic, celle que construisent les apprenants. Il peut être copié tel quel dans les branches de TP.

## Conséquences

- La documentation Sphinx ne dépend plus d'aucun fichier réservé aux formateurs, et n'a rien à exclure.
- Les liens vers les ADR (`CONTRIBUTING.md`, commentaire en tête du `Makefile`) pointent vers `adr/`.
- Dans les projets des apprenants, la convention enseignée reste `docs/adr/`, publiée avec le reste de leur documentation : ces ADR-là documentent leur projet. Ceux de ce dossier documentent le dépôt de formation.
