"""Constraint validation helpers."""


def check_constraints(pin_map, device):
    valid_pins = set(device.get("valid_pins", []))
    issues = []
    used_pins = {}

    for signal, pin in pin_map.items():
        if valid_pins and pin not in valid_pins:
            issues.append((signal, pin, "Pin is not in the device's valid pin list."))

        if pin in used_pins:
            other_signal = used_pins[pin]
            issues.append((signal, pin, f"Pin already assigned to {other_signal}."))
        else:
            used_pins[pin] = signal

    return issues