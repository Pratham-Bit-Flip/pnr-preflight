# pnr-preflight

`pnr-preflight` is a Python command-line tool that checks a Yosys JSON netlist before running nextpnr-xilinx. It was built for the Numato Mimas A7 flow to catch resource overuse, unsupported primitives, and bad pin assignments before place-and-route wastes time.

## Why This Matters

On small FPGA projects, nextpnr-xilinx can fail late, fail vaguely, or spend a long time exploring placements before the design is clearly impossible. `pnr-preflight` moves the useful checks earlier so you can see the likely failure mode in seconds instead of re-running full PnR blindly.

I built it because I kept hitting that same wall on the Numato Mimas A7: nextpnr-xilinx would run for a long time, then fail with a cryptic message or no useful message at all. That meant redesign, resynthesize, retry, and lose time on failures that were predictable up front.

I used AI to help draft the first version, but every check was manually reviewed, corrected, and verified against real Yosys output from the workspace.

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

## Quick Start

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

The tool was verified on a real workspace design, the LED blink example in `LED_BLINK/`, using the board constraints from `boards/xillinx/numato_io.xdc`. The negative example `examples/not_for_pnr_mmcm.v` was used to verify the primitive checker.

## Comparison with nextpnr

`pnr-preflight` is a static pre-checker that runs in seconds on a Yosys JSON netlist. It is not a replacement for nextpnr; instead, it identifies likely failure causes before you run PnR. Examples:

- nextpnr: may hang, crash, or print a cryptic "placement failed" after a long run
- pnr-preflight: reports actionable issues like "94% LUT utilization (above the 80% warning threshold)" or "FAIL MMCME2_ADV: MMCM is not reliably placed by nextpnr-xilinx"

Use `pnr-preflight` to reduce wasted PnR runtime and get clearer guidance on design fixes.

## Notes

- The device database in `devices/artix7_50t.json` targets the Numato Mimas A7 / XC7A50T.
- `examples/mimas_a7_minimal.xdc` is a board-specific constraint example.
- `tests/smoke_test.py` is a basic repository smoke check.

## Project Status

Exploration / early-prototype. AI-assisted drafting was used for initial drafts; each check and test was reviewed and validated by the maintainer.

