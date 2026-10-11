"""Remote-only clean-kernel execution; numeric cells call the installed studies."""
import json
from pathlib import Path
from nbclient import NotebookClient
import nbformat


def main():
    out = Path("proof/notebooks")
    out.mkdir(parents=True, exist_ok=True)
    records = []
    for path in sorted(Path("notebooks").glob("*.ipynb")):
        nb = nbformat.read(path, as_version=4)
        for cell in nb.cells:
            if cell.cell_type == "code":
                cell.outputs = []
                cell.execution_count = None
        client = NotebookClient(nb, timeout=180, kernel_name="python3",
                                resources={"metadata": {"path": "notebooks"}})
        client.execute()
        for cell in nb.cells:
            if cell.cell_type == "code":
                if cell.execution_count is None or any(o.output_type == "error" for o in cell.outputs):
                    raise ValueError("Unexecuted or failed cell")
        nbformat.write(nb, out / path.name)
        records.append({"notebook": path.name, "clean_kernel": True,
                        "executed_code_cells": sum(c.cell_type == "code" for c in nb.cells)})
    if len(records) != 4:
        raise ValueError("Expected exactly four selected notebooks")
    (out / "execution.json").write_text(json.dumps(records, indent=2) + "\n")


if __name__ == "__main__":
    main()
