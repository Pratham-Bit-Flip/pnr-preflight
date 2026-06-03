"""Seed sweep helper for retrying PnR with different seeds."""

import csv
import subprocess


def sweep_seeds(pnr_cmd_template, seeds, log_file):
    results = {}
    with open(log_file, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["seed", "result"])

        for seed in seeds:
            command = [part.format(seed=seed) for part in pnr_cmd_template]
            try:
                completed = subprocess.run(command, capture_output=True, text=True, timeout=120)
                passed = completed.returncode == 0
            except subprocess.TimeoutExpired:
                passed = False

            results[seed] = passed
            writer.writerow([seed, "PASS" if passed else "FAIL"])
            print(f"Seed {seed}: {'PASS' if passed else 'FAIL'}")
            if passed:
                return results

    return results