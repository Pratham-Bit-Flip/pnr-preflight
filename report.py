"""Report formatting for pnr-preflight."""


def make_bar(pct, width=20):
	filled = max(0, min(width, int(pct * width)))
	return "[" + ("#" * filled) + ("." * (width - filled)) + "]"


def _section(title):
	print("-" * 72)
	print(title)
	print("-" * 72)


def print_report(resource_results, prim_failures, prim_warnings, constraint_issues, cells=None, verbose=False):
	print("=" * 72)
	print("PREFLIGHT REPORT")
	print("=" * 72)

	if verbose and cells is not None:
		_section("NETLIST CELLS")
		if cells:
			for cell_type in sorted(cells):
				print(f"{cell_type:20} {cells[cell_type]}")
		else:
			print("No cells found.")

	_section("RESOURCE UTILIZATION")
	if resource_results:
		for name, used, limit, pct, status in resource_results:
			print(f"[{status}] {name:5} {used}/{limit} {pct:.1%} {make_bar(pct)}")
	else:
		print("OK")

	_section("PRIMITIVE COMPATIBILITY")
	if prim_failures:
		for cell_type, reason in prim_failures:
			print(f"FAIL {cell_type}: {reason}")
	else:
		print("OK")
	if prim_warnings:
		for cell_type, reason in prim_warnings:
			print(f"WARN {cell_type}: {reason}")

	_section("CONSTRAINT VALIDATION")
	if constraint_issues:
		for signal, pin, issue in constraint_issues:
			print(f"FAIL {signal} -> {pin}: {issue}")
	else:
		print("OK")

	failed = any(status == "FAIL" for _, _, _, _, status in resource_results) or bool(prim_failures) or bool(constraint_issues)
	if failed:
		print("\033[91mPREFLIGHT FAILED — fix errors before PnR\033[0m")
	else:
		print("\033[92mPREFLIGHT PASSED — safe to run PnR\033[0m")
