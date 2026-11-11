"""Exécute des notebooks, chacun sur une copie isolée, sans modifier le dépôt.

Chaque notebook tourne dans son propre dossier temporaire, avec une copie de input/ et models/.
Un dossier en argument exécute tous ses .ipynb ; un chemin absent est ignoré.
Code de retour non nul si au moins un notebook échoue.

Usage : uv run python scripts/run_notebook.py notebook
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


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


def run_notebook(notebook: Path) -> int:
    """Exécute une copie isolée du notebook et renvoie le code de retour de nbconvert."""
    with tempfile.TemporaryDirectory(prefix="mlops-notebook-") as tmp:
        tmp_dir = Path(tmp)
        (tmp_dir / "notebook").mkdir()
        shutil.copytree(REPO_ROOT / "input", tmp_dir / "input")
        models_dir = REPO_ROOT / "models"
        if models_dir.is_dir():
            shutil.copytree(models_dir, tmp_dir / "models")
        else:
            (tmp_dir / "models").mkdir()
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
        return subprocess.run(command, check=False).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "paths", type=Path, nargs="+", help="Notebooks ou dossiers contenant des notebooks"
    )
    args = parser.parse_args()

    failed = []
    for notebook in collect_notebooks(args.paths):
        print(f"▶️  Exécution de {notebook.name}", flush=True)
        if run_notebook(notebook) == 0:
            print(f"✅ {notebook.name}", flush=True)
        else:
            print(f"❌ {notebook.name}", file=sys.stderr, flush=True)
            failed.append(notebook.name)

    if failed:
        print(f"❌ Notebooks en échec : {', '.join(failed)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
