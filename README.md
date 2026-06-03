# pnr-preflight

`pnr-preflight` is a Python command-line tool that checks a Yosys JSON netlist before running nextpnr-xilinx. It was built for the Numato Mimas A7 flow to catch resource overuse, unsupported primitives, and bad pin assignments before place-and-route wastes time.

## Problem

On small FPGA projects, nextpnr-xilinx can fail late, fail vaguely, or spend a long time exploring placements before the design is clearly impossible. This tool moves the useful checks earlier so you can see the likely failure mode in seconds instead of re-running full PnR blindly.

## What It Checks

- Resource utilization against device limits
- Unsupported or risky Xilinx primitives
- Pin constraint validity for the target board
- Optional seed sweep retries for failed PnR attempts

## Project Layout

- `parsers/netlist.py` loads a Yosys JSON netlist and counts cell types
- `checks/resources.py` compares resource counts against device limits
- `checks/primitives.py` flags unsupported Xilinx cells
- `parsers/constraints.py` reads `.pcf` or `.xdc` constraints
- `checks/constraints.py` validates pins and duplicate assignments
- `report.py` prints the terminal report
- `preflight.py` wires everything together
- `runner/seed_sweep.py` retries nextpnr with multiple seeds

## Requirements

- Python 3.8+
- Yosys
- A Yosys-generated JSON netlist

## Usage

Generate a netlist from an existing design:

```bash
yosys -p "read_verilog ../LED_BLINK/top.v ../LED_BLINK/led_blink.v; synth_xilinx -flatten -top top; write_json netlist.json"
```

Run preflight:

```bash
python preflight.py --netlist netlist.json --top top --device devices/artix7_50t.json --xdc ../boards/xillinx/numato_io.xdc
```

Enable verbose cell listing:

```bash
python preflight.py --netlist netlist.json --top top --device devices/artix7_50t.json --xdc ../boards/xillinx/numato_io.xdc --verbose
```

## Example Output

```text
========================================================================
PREFLIGHT REPORT
========================================================================
------------------------------------------------------------------------
NETLIST CELLS
------------------------------------------------------------------------
BUFG                 1
CARRY4               7
FDCE                 27
IBUF                 2
INV                  28
LUT4                 1
LUT5                 27
LUT6                 3
MUXF7                4
MUXF8                2
OBUF                 1
------------------------------------------------------------------------
RESOURCE UTILIZATION
------------------------------------------------------------------------
[OK] LUT   31/32600 0.1% [....................]
[OK] FF    27/65200 0.0% [....................]
[OK] BRAM  0/75 0.0% [....................]
[OK] DSP   0/120 0.0% [....................]
[OK] IO    3/250 1.2% [....................]
------------------------------------------------------------------------
PRIMITIVE COMPATIBILITY
------------------------------------------------------------------------
OK
------------------------------------------------------------------------
CONSTRAINT VALIDATION
------------------------------------------------------------------------
OK
PREFLIGHT PASSED — safe to run PnR
```

## Validation

The tool was verified on a real workspace design, the LED blink example in `LED_BLINK/`, using the board constraints from `boards/xillinx/numato_io.xdc`. That run passed all checks.

## Notes

- The device database in `devices/artix7_50t.json` is tuned for the Numato Mimas A7 / XC7A50T target.
- `examples/mimas_a7_minimal.xdc` is a small board-specific constraint example you can adapt.
- `tests/smoke_test.py` is a repository smoke check for the local toolchain.
- `examples/not_for_pnr_mmcm.v` is a deliberate failure case that synthesizes to `MMCME2_ADV` so you can confirm the primitive checker rejects it.
