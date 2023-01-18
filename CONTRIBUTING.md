# CONTRIBUTING

Quelques règles pour contribuer à ce repo de formation.

- [CONTRIBUTING](#contributing)
  - [:wrench: Pré-requis](#wrench-pr%c3%a9-requis)
  - [:speech_balloon: Proposer des améliorations](#speechballoon-proposer-des-am%c3%a9liorations)
  - [:raising_hand: Prendre une tâche](#raisinghand-prendre-une-t%c3%a2che)
    - [:computer: Quand ça touche au code](#computer-quand-%c3%a7a-touche-au-code)
    - [:page_with_curl: Quand ça touche aux slides](#pagewithcurl-quand-%c3%a7a-touche-aux-slides)
  - [:black_joker: Core committers](#blackjoker-core-committers)

## :wrench: Pré-requis

- Être membre du [groupe cercle-formation][cercle-formation-gitlab]
- Être membre du [repo DSIND][repo-dsind], avec le rôle `Developer`
- Idéalement, avoir déjà suivi ou donné la formation pour les tâches qui touchent au support de slides
- Avoir git et python3 :snake: installés sur ta machine

Pour cela :arrow_right: ping le cercle-formation science@scale !

[cercle-formation-gitlab]:[https://gitlab.com/octo-technology/octo-bda/cercle-formation]
[repo-dsind]:[https://gitlab.com/octo-technology/octo-bda/cercle-formation/dsind]

## :speech_balloon: Proposer des améliorations

Passe par le système d'`issues`, tu peux créer une `issue` pour

- faire un feedback sur cette formation DSIND que tu as suivie ou donnée,
- lancer une discussion :speech_balloon:,
- proposer une amélioration sur ce repo, le code des TPs, le code des exemples ou le contenu des slides

N'hésite pas à mettre des détails ou des captures d'écran pour illustrer ton propos.

Si tu fais des propositions d'améliorations, explicite tes douleurs, propose une tâche et un moyen de la valider.

Si l'équipe de formateurs juge la demande pertinente et suffisamment détaillée, on l'ajoutera [au board des tâches à réaliser][board].

[board]:[https://gitlab.com/octo-technology/octo-bda/cercle-formation/dsind/-/boards]

## :raising_hand: Prendre une tâche

- Avertir l'équipe des [*core committers* :black_joker:](##-:black_joker:-Core-committers)
- La contacter si la tâche n'est pas suffisamment claire pour toi ou si tu as des doutes.

Avant toute modification, tu dois créer une branche depuis `master`.
````bash
$ git checkout -b <branch-name>
````

### :computer: Quand ça touche au code

- Mettre à jour le [changelog du repo](CHANGELOG.md) avec les éléments essentiels dans une liste à puce.
- Soumettre une `merge request` quand tu as fini et l'attacher à l'`issue` liée à la tâche prise.

### :page_with_curl: Quand ça touche aux slides

- Sur le drive, dupliquer la dernière version du doc gslide
- Renommer le nouveau document en incrémentant la version/le semver, par exemple:
  - 1.3.0 :arrow_right: 1.3.1 pour les petits fix,
  - 1.3.0 :arrow_right: 1.4.0 pour de l'ajout de contenu,
  - 1.3.0 :arrow_right: 2.0.0 pour des éditions majeures (ex: une nouvelle partie ajoutée),
  - Ping les core committers au besoin
- Y faire les modifs
- Lister les modifs dans le [changelog des slides](CHANGELOG_SLIDES.md)
- Mettre à jour le [manifeste du support de présentation](manifest.ini) en renseignant
  - un lien vers le support gslide,
  - un lien vers le support pdf pouvant être partagé aux clients de la prochaine formation,

Le manifest est consultable via la commande : 
```bash
$ git config -f manifest.ini --list
```

- Soumettre une `merge request` avec le changelog et le manifeste quand tu as fini, et l'attacher à l'`issue` liée à la tâche prise.

> Pour attacher l'`issue` à la `merge request`, il faut simplement utiliser le caractère `#`(hashtag) suivi du numéro de l'`issue` lorsque tu rédiges la description de ta `merge request`.  
Un numéro est généré à la création d'une nouvelle `issue`.

## :black_joker: Core committers

- [mho@octo.com](https://askbob.octo.com/users/mho)
- [toul@octo.com](https://askbob.octo.com/users/toul)
