"""Resource utilization checks for pnr-preflight."""

LUT_CELLS = {f"LUT{i}" for i in range(1, 7)}
FF_CELLS = {"FDRE", "FDSE", "FDCE", "FDPE"}
BRAM_CELLS = {"RAMB36E1", "RAMB18E1"}
DSP_CELLS = {"DSP48E1"}
IO_CELLS = {"IBUF", "OBUF", "IOBUF"}


def _sum_cells(cells, valid_types):
    return sum(count for cell_type, count in cells.items() if cell_type in valid_types)


def _status(used, limit, warn_threshold):
    pct = (used / limit) if limit else 0.0
    if pct > 1.0:
        return pct, "FAIL"
    if pct > warn_threshold:
        return pct, "WARN"
    return pct, "OK"


def check_resources(cells, device):
    resources = [
        ("LUT", _sum_cells(cells, LUT_CELLS), int(device.get("luts", 0))),
        ("FF", _sum_cells(cells, FF_CELLS), int(device.get("ffs", 0))),
        ("BRAM", _sum_cells(cells, BRAM_CELLS), int(device.get("bram_36k", 0))),
        ("DSP", _sum_cells(cells, DSP_CELLS), int(device.get("dsp48", 0))),
        ("IO", _sum_cells(cells, IO_CELLS), int(device.get("io", 0))),
    ]

    warn_threshold = float(device.get("warn_threshold", 0.8))
    results = []
    for name, used, limit in resources:
        pct, status = _status(used, limit, warn_threshold)
        results.append((name, used, limit, pct, status))
    return results