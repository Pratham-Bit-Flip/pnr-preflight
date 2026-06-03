"""Netlist loading and cell counting utilities."""

import json


def load_netlist(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def get_cells(netlist, top_module):
    modules = netlist.get("modules", {})
    if top_module not in modules:
        available = ", ".join(sorted(modules)) or "<none>"
        print(f"Top module '{top_module}' not found. Available modules: {available}")
        return {}

    cells = modules[top_module].get("cells", {})
    counts = {}
    for cell in cells.values():
        cell_type = cell.get("type", "UNKNOWN")
        counts[cell_type] = counts.get(cell_type, 0) + 1
    return counts