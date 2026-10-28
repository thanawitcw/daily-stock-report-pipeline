import sys
import os

# Add project root (one level up from scripts/) to path so config.py can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

from nbconvert import PythonExporter
import nbformat


def run_notebook(notebook_path):
    print(f"Running notebook: {notebook_path}")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    exporter = PythonExporter()
    source, _ = exporter.from_notebook_node(nb)

    code = compile(source, notebook_path, 'exec')
    exec(code, globals())
    print(f"Finished: {notebook_path}\n")


def run_all_notebooks():
    for path in config.NOTEBOOK_PATHS:
        run_notebook(path)


if __name__ == "__main__":
    run_all_notebooks()
