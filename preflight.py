"""CLI entry point for pnr-preflight."""

import argparse
import json
import shlex
import sys

from checks.constraints import check_constraints
from checks.primitives import check_primitives
from checks.resources import check_resources
from parsers.constraints import parse_pcf, parse_xdc
from parsers.netlist import get_cells, load_netlist
from report import print_report
from runner.seed_sweep import sweep_seeds


def _load_device(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run preflight checks before nextpnr-xilinx.")
    parser.add_argument("--netlist", required=True, help="Path to Yosys JSON netlist.")
    parser.add_argument("--top", required=True, help="Top module name in the netlist.")
    parser.add_argument("--device", default="devices/artix7_50t.json", help="Path to device JSON.")
    parser.add_argument("--pcf", help="Path to .pcf constraint file.")
    parser.add_argument("--xdc", help="Path to .xdc constraint file.")
    parser.add_argument("--verbose", action="store_true", help="Print raw cell counts before the report.")
    parser.add_argument("--sweep", action="store_true", help="Run seed sweep when failure suggests PnR retry may help.")
    args = parser.parse_args(argv)

    netlist = load_netlist(args.netlist)
    cells = get_cells(netlist, args.top)
    device = _load_device(args.device)
    resource_results = check_resources(cells, device)
    prim_failures, prim_warnings = check_primitives(cells)

    constraint_issues = []
    if args.pcf:
        constraint_issues = check_constraints(parse_pcf(args.pcf), device)
    elif args.xdc:
        constraint_issues = check_constraints(parse_xdc(args.xdc), device)

    print_report(
        resource_results,
        prim_failures,
        prim_warnings,
        constraint_issues,
        cells=cells,
        verbose=args.verbose,
    )

    resource_or_primitive_fail = any(status == "FAIL" for _, _, _, _, status in resource_results) or bool(prim_failures)
    failed = resource_or_primitive_fail or bool(constraint_issues)
    if args.sweep and resource_or_primitive_fail:
        template_text = input("Enter nextpnr command template with {seed}: ").strip()
        if template_text:
            sweep_seeds(shlex.split(template_text), range(20), "seed_sweep.csv")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
