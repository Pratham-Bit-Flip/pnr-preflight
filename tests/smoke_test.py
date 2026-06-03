from pathlib import Path
import json
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from preflight import main


BASE = Path(tempfile.mkdtemp())
NETLIST = BASE / "netlist.json"
DEVICE = BASE / "device.json"
XDC = BASE / "mimas_a7_minimal.xdc"

NETLIST.write_text(
    json.dumps(
        {
            "modules": {
                "top": {
                    "cells": {
                        "u0": {"type": "LUT4"},
                        "u1": {"type": "FDRE"},
                        "u2": {"type": "IBUF"},
                        "u3": {"type": "OBUF"},
                    }
                }
            }
        }
    ),
    encoding="utf-8",
)

DEVICE.write_text(
    json.dumps(
        {
            "luts": 100,
            "ffs": 100,
            "bram_36k": 1,
            "dsp48": 1,
            "io": 100,
            "warn_threshold": 0.75,
            "valid_pins": [
                "E3", "H17", "K15", "K17", "J17", "J18", "T9", "T10",
                "U11", "M18", "P16", "P20", "P15", "M19", "M20", "N20",
                "N19", "H4", "M2", "J21", "K22", "L14", "L15", "L16",
                "K16", "M15", "M16",
            ],
        }
    ),
    encoding="utf-8",
)

XDC.write_text(
    "set_property PACKAGE_PIN E3 [get_ports {osc_clk}]\n"
    "set_property PACKAGE_PIN H17 [get_ports {LED_0}]\n"
    "set_property PACKAGE_PIN K15 [get_ports {LED_1}]\n",
    encoding="utf-8",
)

raise SystemExit(main(["--netlist", str(NETLIST), "--top", "top", "--device", str(DEVICE), "--xdc", str(XDC), "--verbose"]))
