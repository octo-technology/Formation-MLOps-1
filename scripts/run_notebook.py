"""Exécute un notebook sur une copie isolée, sans modifier le dépôt.

Le notebook est copié dans un répertoire temporaire qui reproduit l'arborescence
attendue (``notebook/``, ``input/``, ``models/``), afin que les chemins relatifs
du notebook fonctionnent et que les modèles du dépôt ne soient pas écrasés.
Le répertoire temporaire est supprimé à la fin, y compris en cas d'échec.

Usage :
    uv run python scripts/run_notebook.py notebook/titanic.ipynb
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_notebook(notebook: Path) -> int:
    """Exécute une copie du notebook et renvoie le code de retour de nbconvert."""
    with tempfile.TemporaryDirectory(prefix="mlops-notebook-") as tmp:
        tmp_dir = Path(tmp)
        (tmp_dir / "notebook").mkdir()
        (tmp_dir / "models").mkdir()
        shutil.copytree(REPO_ROOT / "input", tmp_dir / "input")
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
    parser.add_argument("notebook", type=Path, help="Chemin du notebook à exécuter")
    args = parser.parse_args()

    notebook = args.notebook.resolve()
    if not notebook.is_file():
        print(f"❌ Notebook introuvable : {args.notebook}", file=sys.stderr)
        return 1
    return run_notebook(notebook)


if __name__ == "__main__":
    sys.exit(main())
