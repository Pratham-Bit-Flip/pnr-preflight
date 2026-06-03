"""Constraint file parsing helpers."""

import re


_PCF_PATTERN = re.compile(r"^set_io\s+(\S+)\s+(\S+)$")
_XDC_PATTERN = re.compile(r"set_property\s+PACKAGE_PIN\s+(\S+)\s+\[get_ports\s+\{?([^\}\]]+)\}?\]")


def parse_pcf(path):
    pin_map = {}
    with open(path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            match = _PCF_PATTERN.match(line)
            if match:
                signal, pin = match.groups()
                pin_map[signal] = pin
    return pin_map


def parse_xdc(path):
    pin_map = {}
    with open(path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            match = _XDC_PATTERN.search(line)
            if match:
                pin, signal = match.groups()
                pin_map[signal.strip()] = pin.strip()
    return pin_map