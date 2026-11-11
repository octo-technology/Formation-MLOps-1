# 0002 : Le package est construit avec uv_build

- **Statut :** Accepté
- **Date :** 2026-11-11

## Contexte

Au TP5, les apprenants packagent le code de la formation. Jusqu'ici, `pyproject.toml` déclarait setuptools (`setuptools.build_meta` et `[tool.setuptools] packages = ["src"]`). Or la slide 142 du cours (v1.13) présente le backend d'uv (`[tool.uv.build-backend]`), et le reste de la formation utilise uv pour la version de Python, l'environnement, les dépendances et `uv build`. Les apprenants voyaient donc deux configurations différentes, l'une dans le cours, l'autre dans le TP.

Le package importable s'appelle `src` et se trouve à la racine du dépôt. Ce n'est pas la structure attendue par défaut par `uv_build`, qui cherche `src/<nom_du_projet>/__init__.py` (ici `src/formation_mlops_1/__init__.py`).

## Décision

- Le backend de construction est `uv_build` : `requires = ["uv_build>=0.13.5,<0.14.0"]`, `build-backend = "uv_build"`.
  - Borne basse : la version d'uv de référence (README, CI, `Dockerfile`).
  - Borne haute : la version mineure suivante, comme dans le `pyproject.toml` généré par `uv init --package`. Le backend d'uv peut changer d'une version mineure à l'autre.
- `[tool.uv.build-backend]` déclare `module-name = "src"` et `module-root = ""` (module à la racine du dépôt).
- On garde le nom `src` : les notebooks, les tests et l'API importent `src.feature_engineering` dès le TP1.

## Conséquences

- Le cours, `tp5.md` et le dépôt utilisent la même configuration.
- Le wheel garde le même nom (`formation_mlops_1-0.1.0-py3-none-any.whl`) et le même contenu (`src/`) : la suite de `tp5.md`, la CI (`uv build`) et le `Dockerfile` ne changent pas.
- `uv.lock` ne change pas : les dépendances de construction n'y figurent pas.
- Quand la version d'uv de référence passe à 0.14, il faut aussi relever la borne de `uv_build` dans `pyproject.toml` et dans `tp5.md`.
- Concerne `dev`, la branche `6_start_docker` et `final_state`. Les branches 0 à 5 n'ont pas encore de `[build-system]` : l'apprenant l'ajoute au TP5.
