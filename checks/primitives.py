"""Primitive compatibility checks for pnr-preflight."""

UNSUPPORTED = {
    "MMCME2_ADV": "Mixed-mode clock manager is not reliably placed by nextpnr-xilinx.",
    "PLLE2_ADV": "Advanced PLL support is not implemented in nextpnr-xilinx.",
    "IDELAYCTRL": "IO delay controller is hard IP and not supported here.",
    "OSERDESE2": "Output serializer cells are not supported for high-speed IO placement.",
    "ISERDESE2": "Input serializer cells are not supported for high-speed IO placement.",
    "GTXE2_CHANNEL": "GTX transceiver hard IP is not supported.",
    "XADC": "On-chip ADC hard IP is not supported.",
    "BUFHCE": "Global clock buffer variants can be problematic in this flow.",
}

WARN_CELLS = {
    "MMCME2_BASE": "Base MMCME2 cells may work, but clocking support can be partial.",
    "RAMB36E1": "Large BRAM instances may need extra care depending on placement and initialization.",
}


def check_primitives(cells):
    failures = []
    warnings = []

    for cell_type in cells:
        if cell_type in UNSUPPORTED:
            failures.append((cell_type, UNSUPPORTED[cell_type]))
        if cell_type in WARN_CELLS:
            warnings.append((cell_type, WARN_CELLS[cell_type]))

    return failures, warnings