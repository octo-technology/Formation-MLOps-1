"""Exécute des notebooks, chacun sur une copie isolée, sans modifier le dépôt.

Chaque notebook tourne dans son propre dossier temporaire, avec une copie de input/, models/ et src/.
Un dossier en argument exécute tous ses .ipynb ; un chemin absent est ignoré.
Code de retour non nul si au moins un notebook échoue.

Avec --expect-error MESSAGE, le sens s'inverse : chaque notebook doit échouer avec MESSAGE dans
sa sortie. Sert à vérifier l'état de départ d'un TP, dont le notebook échoue volontairement.

Usage :
    uv run python scripts/run_notebook.py notebook
    uv run python scripts/run_notebook.py --expect-error "NameError: name 'pd'" notebook/titanic.ipynb
"""

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
# Codes couleur ANSI que nbconvert insère dans les tracebacks.
ANSI_CODES = re.compile(r"\x1b\[[0-9;]*m")


def collect_notebooks(paths: list[Path]) -> list[Path]:
    """Renvoie les notebooks désignés par les chemins, en signalant les chemins absents."""
    notebooks = []
    for path in paths:
        if path.is_dir():
            notebooks.extend(sorted(path.glob("*.ipynb")))
        elif path.is_file():
            notebooks.append(path)
        else:
            print(f"⚠️  Chemin absent, ignoré : {path}", flush=True)
    return [notebook.resolve() for notebook in notebooks]


def run_notebook(notebook: Path) -> tuple[int, str]:
    """Exécute une copie isolée du notebook et renvoie le code de retour et la sortie de nbconvert."""
    with tempfile.TemporaryDirectory(prefix="mlops-notebook-") as tmp:
        tmp_dir = Path(tmp)
        (tmp_dir / "notebook").mkdir()
        shutil.copytree(REPO_ROOT / "input", tmp_dir / "input")
        models_dir = REPO_ROOT / "models"
        if models_dir.is_dir():
            shutil.copytree(models_dir, tmp_dir / "models")
        else:
            (tmp_dir / "models").mkdir()
        # Sans packaging (branches de TP 2 à 5), le notebook importe src/ via sys.path.append("..").
        src_dir = REPO_ROOT / "src"
        if src_dir.is_dir():
            shutil.copytree(src_dir, tmp_dir / "src", ignore=shutil.ignore_patterns("__pycache__"))
        notebook_copy = tmp_dir / "notebook" / notebook.name
        shutil.copy(notebook, notebook_copy)

        # nbconvert démarre le kernel dans le dossier du notebook copié.
        command = [
            sys.executable,
            "-m",
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            str(notebook_copy),
            "--output",
            "executed",
            "--output-dir",
            str(tmp_dir),
        ]
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        return result.returncode, result.stdout + result.stderr


def check_result(returncode: int, output: str, expected_error: str | None) -> str | None:
    """Renvoie la raison de l'échec de la vérification, ou None si le résultat est celui attendu."""
    if expected_error is None:
        return None if returncode == 0 else "le notebook a échoué"
    if returncode == 0:
        return f"le notebook s'est exécuté sans erreur, alors qu'il devait échouer sur « {expected_error} »"
    if expected_error not in ANSI_CODES.sub("", output):
        return f"le notebook a échoué, mais sans le message attendu « {expected_error} »"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "paths", type=Path, nargs="+", help="Notebooks ou dossiers contenant des notebooks"
    )
    parser.add_argument(
        "--expect-error",
        metavar="MESSAGE",
        help="Réussit seulement si chaque notebook échoue avec ce message dans sa sortie",
    )
    args = parser.parse_args()

    notebooks = collect_notebooks(args.paths)
    if args.expect_error is not None and not notebooks:
        print("❌ Aucun notebook à vérifier", file=sys.stderr)
        return 1

    failed = []
    for notebook in notebooks:
        print(f"▶️  Exécution de {notebook.name}", flush=True)
        returncode, output = run_notebook(notebook)
        reason = check_result(returncode, output, args.expect_error)
        if reason is None:
            expected = f" (échec attendu : {args.expect_error})" if args.expect_error else ""
            print(f"✅ {notebook.name}{expected}", flush=True)
        else:
            print(output, file=sys.stderr, flush=True)
            print(f"❌ {notebook.name} : {reason}", file=sys.stderr, flush=True)
            failed.append(notebook.name)

    if failed:
        print(f"❌ Notebooks en échec : {', '.join(failed)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
