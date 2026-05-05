"""Top-level orchestrator for the headline Agent Bazaar experiments.

Each experiment is implemented in its own ``scripts/exp*.py`` runner, with
its own filtering / parallelism / model-selection CLI. This module is a
thin dispatcher: it selects which runner(s) to invoke and forwards any
extra CLI arguments through to them.

Usage examples (run from the project root)::

    # List the registered experiments and exit
    python -m experiments.run_experiments --list

    # Run THE_CRASH main sweep, forwarding flags to scripts/exp1.py
    python -m experiments.run_experiments --experiment crash -- --dlc 3 --n-stab 3 --seeds 8

    # Run LEMON_MARKET main sweep with 3 parallel workers
    python -m experiments.run_experiments --experiment lemon -- --workers 3 \\
        --seller-llm google/gemma-3-12b-it

    # Run every registered experiment in order (long; respects --skip-existing)
    python -m experiments.run_experiments --experiment all -- --skip-existing

For per-experiment options run the underlying script with ``--help``,
e.g. ``python scripts/exp1.py --help``.
"""

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

# (alias, script filename, one-line description). The aliases are stable;
# rename the underlying scripts freely without touching callers.
EXPERIMENTS: list[tuple[str, str, str]] = [
    ("crash",            "exp1.py",                     "THE_CRASH main sweep (B2C; firms x discovery x stabilizers x seeds)"),
    ("crash_eas",        "exp1_eas_sweep.py",           "THE_CRASH x open-weight model size sweep (3B-405B)"),
    ("lemon",            "exp2.py",                     "LEMON_MARKET main sweep (C2C; Sybil saturation x reputation visibility)"),
    ("lemon_no_seller",  "exp2_2.py",                   "LEMON_MARKET no-seller-IDs ablation"),
    ("lemon_eas",        "exp2_eas_sweep.py",           "LEMON_MARKET x buyer model capability sweep"),
    ("shocks",           "exp3.py",                     "Adversarial shocks (mid-episode unit-cost shock; Sybil flood)"),
    ("shocks_eas",       "exp3_open_weights_sweep.py",  "Adversarial shocks x open-weight model sweep"),
    ("dlf",              "exp5.py",                     "Discovery-limit-firms ablation (firm-side info, mirrors exp1)"),
    ("personas",         "exp6.py",                     "Consumer procedural persona ablation"),
]
ALIASES = [alias for alias, _, _ in EXPERIMENTS]
SCRIPT_BY_ALIAS = {alias: script for alias, script, _ in EXPERIMENTS}


def _print_table() -> None:
    print("Available experiments:")
    print(f"  {'alias':<18}  {'script':<32}  description")
    print(f"  {'-' * 18}  {'-' * 32}  {'-' * 11}")
    for alias, script, desc in EXPERIMENTS:
        print(f"  {alias:<18}  scripts/{script:<24}  {desc}")


def _run_one(alias: str, forwarded: list[str]) -> int:
    script = SCRIPTS_DIR / SCRIPT_BY_ALIAS[alias]
    cmd = [sys.executable, str(script), *forwarded]
    print(f"\n>>> [{alias}] {' '.join(cmd)}", flush=True)
    return subprocess.call(cmd, cwd=PROJECT_ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Anything after `--` is forwarded verbatim to the chosen runner. "
               "Use scripts/<runner>.py --help for per-experiment flags.",
    )
    parser.add_argument(
        "--experiment",
        choices=ALIASES + ["all"],
        default=None,
        help="Which experiment to run. Use --list to see all aliases.",
    )
    parser.add_argument(
        "--list", action="store_true",
        help="Print the registered experiments and exit.",
    )
    args, forwarded = parser.parse_known_args()

    if args.list or args.experiment is None:
        _print_table()
        return 0

    if args.experiment == "all":
        results: list[tuple[str, int]] = []
        for alias in ALIASES:
            rc = _run_one(alias, forwarded)
            results.append((alias, rc))
        failed = [alias for alias, rc in results if rc != 0]
        if failed:
            print(f"\nFailed: {failed}", file=sys.stderr)
            return 1
        return 0

    return _run_one(args.experiment, forwarded)


if __name__ == "__main__":
    sys.exit(main())
