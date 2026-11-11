# Architecture Decision Records

Ce dossier trace les décisions structurantes prises sur ce dépôt : leur contexte, ce qui a été choisi et pourquoi.
Les contributeurs changent souvent : avant de remettre en cause un choix, lisez l'ADR correspondant.

## Ajouter une décision

1. Copier le dernier ADR et l'incrémenter : `NNNN-titre-court.md`.
2. Remplir les sections Contexte, Décision et Conséquences.
3. Ne jamais réécrire un ADR accepté. Pour changer de décision, créer un nouvel ADR qui remplace l'ancien, et passer l'ancien au statut « Remplacé par NNNN ».

## Index

| # | Décision | Statut |
|---|---|---|
| [0001](0001-scripts-pour-la-logique-du-makefile.md) | Le Makefile délègue toute logique sur plusieurs lignes à des scripts | Accepté |
| [0002](0002-package-construit-avec-uv-build.md) | Le package est construit avec uv_build | Accepté |
