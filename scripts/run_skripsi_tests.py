#!/usr/bin/env python3
"""Unified Test Runner for nyekripsi (Milestone 4 E2E Testing Infrastructure).

Executes the multi-tier verification pyramid:
- Tier 1: Static Linters & Repository Invariants (13 linters & write-scope guard tests)
- Tier 2: Algorithmic Unit Tests (M1 core, M1 adversarial, M2 methodologies, M3 commands/agents)
- Tier 3 & Tier 4: Real-World Thesis Workload Scenarios (test_skripsi_e2e_workloads.py)
- Tier 5: Adversarial Stress Testing (test_skripsi_m4_adversarial.py)

Pure standard library Python implementation without third-party dependencies.
Compatible with Python 3.8+ on Linux, Termux/Android, macOS, and Windows.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import os
import pathlib
import re
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


@dataclasses.dataclass
class TestTarget:
    name: str
    tier: int
    command: List[str]
    description: str
    is_unittest: bool = False
    optional: bool = False


@dataclasses.dataclass
class TargetResult:
    target: TestTarget
    status: str  # "PASS", "FAIL", "SKIPPED"
    returncode: int
    duration_sec: float
    stdout: str
    stderr: str
    tests_run: int = 1
    tests_failed: int = 0
    tests_skipped: int = 0


# ==============================================================================
# TARGET REGISTRY ACROSS ALL 5 TIERS
# ==============================================================================

TIER_1_TARGETS: List[TestTarget] = [
    TestTarget(
        name="check_command_frontmatter_name",
        tier=1,
        command=[sys.executable, "scripts/check_command_frontmatter_name.py"],
        description="Verify all command frontmatter 'name:' matches stem (#633)",
    ),
    TestTarget(
        name="check_command_skill_dispatch",
        tier=1,
        command=[sys.executable, "scripts/check_command_skill_dispatch.py"],
        description="Verify 21 mode commands invoke skill with rooted references (#857)",
    ),
    TestTarget(
        name="check_command_invariants",
        tier=1,
        command=[
            sys.executable,
            "tools/release-discipline/scripts/check_command_invariants.py",
            "--manifest",
            ".command-invariants.toml",
        ],
        description="Verify release discipline command invariants and announce tokens",
    ),
    TestTarget(
        name="check_agents_mirror_sync",
        tier=1,
        command=[sys.executable, "scripts/check_agents_mirror_sync.py"],
        description="Verify byte-identical mirroring of plugin agents in agents/ (#413)",
    ),
    TestTarget(
        name="check_write_scope",
        tier=1,
        command=[sys.executable, "scripts/check_v3_10_134_write_scope.py"],
        description="Verify Bucket A write scope roster and Bucket B/C/D exemptions (#134)",
    ),
    TestTarget(
        name="check_phase_boundary",
        tier=1,
        command=[sys.executable, "scripts/check_v3_9_2_phase_boundary.py"],
        description="Verify phase boundary instruction tags on Bucket A agents",
    ),
    TestTarget(
        name="check_model_tiering",
        tier=1,
        command=[sys.executable, "scripts/check_model_tiering.py"],
        description="Verify 45 agent model tiering classifications (31 judgment / 14 execution)",
    ),
    TestTarget(
        name="check_distribution_surface_claims",
        tier=1,
        command=[sys.executable, "scripts/check_distribution_surface_claims.py"],
        description="Verify distribution surface claims stay within evidence record",
    ),
    TestTarget(
        name="check_version_consistency",
        tier=1,
        command=[sys.executable, "scripts/check_version_consistency.py"],
        description="Verify repository version consistency across manifests and files",
    ),
    TestTarget(
        name="check_spec_consistency",
        tier=1,
        command=[sys.executable, "scripts/check_spec_consistency.py"],
        description="Verify specification consistency and cross-references",
    ),
    TestTarget(
        name="check_ci_pytest_manifest",
        tier=1,
        command=[sys.executable, "scripts/check_ci_pytest_manifest.py"],
        description="Verify CI pytest manifest integrity and target existence",
    ),
    TestTarget(
        name="check_preprint_venues_consistency",
        tier=1,
        command=[sys.executable, "scripts/check_preprint_venues_consistency.py"],
        description="Verify PREPRINT_VENUES list consistency across agents and signals (#105)",
    ),
    TestTarget(
        name="test_ars_write_scope_guard",
        tier=1,
        command=[sys.executable, "-m", "unittest", "scripts/test_ars_write_scope_guard.py"],
        description="Verify ARS write scope guard hooks and dual namespace support (71 tests)",
        is_unittest=True,
    ),
]

TIER_2_TARGETS: List[TestTarget] = [
    TestTarget(
        name="test_skripsi_m1_core",
        tier=2,
        command=[sys.executable, "-m", "unittest", "tests/test_skripsi_m1_core.py"],
        description="Milestone 1 Core Guidelines & Templates (F1-F7, 44 unit tests)",
        is_unittest=True,
    ),
    TestTarget(
        name="test_skripsi_m1_adversarial",
        tier=2,
        command=[sys.executable, "-m", "unittest", "tests/test_skripsi_m1_adversarial.py"],
        description="Milestone 1 Adversarial & Boundary Math (F4, F6, F15, 14 adversarial tests)",
        is_unittest=True,
    ),
    TestTarget(
        name="test_skripsi_m2_methodologies",
        tier=2,
        command=[sys.executable, "-m", "unittest", "tests/test_skripsi_m2_methodologies.py"],
        description="Milestone 2 Quant, Qual, IT/SE Methodologies & 7 Presets (F8-F10, F15-F16, 35 unit tests)",
        is_unittest=True,
    ),
    TestTarget(
        name="test_skripsi_m3_commands_agents",
        tier=2,
        command=[sys.executable, "-m", "unittest", "tests/test_skripsi_m3_commands_agents.py"],
        description="Milestone 3 Commands, Personas, Rebranding & Custom TOC (F11-F13, F17, 31 unit tests)",
        is_unittest=True,
    ),
]

TIER_3_4_TARGETS: List[TestTarget] = [
    TestTarget(
        name="test_skripsi_e2e_workloads",
        tier=3,
        command=[sys.executable, "-m", "unittest", "tests/test_skripsi_e2e_workloads.py"],
        description="Real-World Thesis Workloads (Scenarios 1-5 across IT, Quant, Qual, Edu/Health, Custom TOC)",
        is_unittest=True,
        optional=False,
    ),
]

TIER_5_TARGETS: List[TestTarget] = [
    TestTarget(
        name="test_skripsi_m4_adversarial",
        tier=5,
        command=[sys.executable, "-m", "unittest", "tests/test_skripsi_m4_adversarial.py"],
        description="Milestone 4 Adversarial Stress Testing & Coverage Hardening",
        is_unittest=True,
        optional=False,
    ),
]

ALL_TARGETS: List[TestTarget] = (
    TIER_1_TARGETS + TIER_2_TARGETS + TIER_3_4_TARGETS + TIER_5_TARGETS
)


# ==============================================================================
# EXECUTION & PARSING HELPERS
# ==============================================================================

def parse_unittest_output(stdout: str, stderr: str) -> tuple[int, int, int]:
    """Extracts (ran_count, failed_count, skipped_count) from unittest output."""
    combined = stdout + "\n" + stderr
    ran_count = 1
    failed_count = 0
    skipped_count = 0

    ran_match = re.search(r"Ran\s+(\d+)\s+tests?\s+in", combined)
    if ran_match:
        ran_count = int(ran_match.group(1))

    fail_match = re.search(r"FAILED\s*\((?:failures=(\d+))?(?:,\s*)?(?:errors=(\d+))?\)", combined)
    if fail_match:
        failures = int(fail_match.group(1) or 0)
        errors = int(fail_match.group(2) or 0)
        failed_count = failures + errors

    skip_match = re.search(r"skipped=(\d+)", combined)
    if skip_match:
        skipped_count = int(skip_match.group(1))

    return ran_count, failed_count, skipped_count


def execute_target(target: TestTarget, verbose: bool = False) -> TargetResult:
    """Executes a single TestTarget, recording duration and parsing results."""
    # Check if target script or test file exists when optional
    script_or_module = target.command[-1]
    if script_or_module.endswith(".py"):
        target_path = REPO_ROOT / script_or_module
        if not target_path.exists():
            if target.optional:
                return TargetResult(
                    target=target,
                    status="SKIPPED",
                    returncode=0,
                    duration_sec=0.0,
                    stdout="",
                    stderr=f"Target file {script_or_module} not present (optional).",
                    tests_run=0,
                    tests_failed=0,
                )
            else:
                return TargetResult(
                    target=target,
                    status="FAIL",
                    returncode=1,
                    duration_sec=0.0,
                    stdout="",
                    stderr=f"Target file {script_or_module} not found.",
                    tests_run=1,
                    tests_failed=1,
                )

    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)

    t0 = time.perf_counter()
    proc = subprocess.run(
        target.command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        env=env,
    )
    duration = time.perf_counter() - t0

    if target.is_unittest:
        ran, failed, skipped = parse_unittest_output(proc.stdout, proc.stderr)
        status = "PASS" if (proc.returncode == 0 and failed == 0) else "FAIL"
        return TargetResult(
            target=target,
            status=status,
            returncode=proc.returncode,
            duration_sec=duration,
            stdout=proc.stdout,
            stderr=proc.stderr,
            tests_run=ran,
            tests_failed=failed if proc.returncode != 0 and failed == 0 else failed,
            tests_skipped=skipped,
        )
    else:
        status = "PASS" if proc.returncode == 0 else "FAIL"
        return TargetResult(
            target=target,
            status=status,
            returncode=proc.returncode,
            duration_sec=duration,
            stdout=proc.stdout,
            stderr=proc.stderr,
            tests_run=1,
            tests_failed=0 if proc.returncode == 0 else 1,
            tests_skipped=0,
        )


def render_scorecard(results: List[TargetResult], total_time: float) -> str:
    """Renders an aligned ASCII execution scorecard."""
    lines = []
    lines.append("=" * 80)
    lines.append(f"{'NYEKRIPSI MULTI-TIER TEST EXECUTION SCORECARD':^80}")
    lines.append("=" * 80)
    lines.append(f"{'Tier / Category':<30} {'Targets':<10} {'Tests':<10} {'Passed':<10} {'Failed':<10} {'Duration':<10}")
    lines.append("-" * 80)

    tier_labels = {
        1: "Tier 1: Static Linters",
        2: "Tier 2: Algorithmic Unit",
        3: "Tier 3 & 4: E2E Workloads",
        5: "Tier 5: Adversarial Stress",
    }

    tier_groups: Dict[int, List[TargetResult]] = {}
    for r in results:
        tier_groups.setdefault(r.target.tier, []).append(r)

    total_targets = len(results)
    total_tests = sum(r.tests_run for r in results)
    total_passed = sum(r.tests_run - r.tests_failed for r in results)
    total_failed = sum(r.tests_failed for r in results)

    for tier, label in tier_labels.items():
        if tier not in tier_groups:
            continue
        t_results = tier_groups[tier]
        t_targets = len(t_results)
        t_tests = sum(r.tests_run for r in t_results)
        t_passed = sum(r.tests_run - r.tests_failed for r in t_results)
        t_failed = sum(r.tests_failed for r in t_results)
        t_dur = sum(r.duration_sec for r in t_results)
        lines.append(f"{label:<30} {t_targets:<10} {t_tests:<10} {t_passed:<10} {t_failed:<10} {t_dur:>7.2f}s")

    lines.append("-" * 80)
    lines.append(f"{'TOTAL':<30} {total_targets:<10} {total_tests:<10} {total_passed:<10} {total_failed:<10} {total_time:>7.2f}s")
    lines.append("=" * 80)

    if total_failed == 0:
        lines.append(f"{'OVERALL RESULT: [SUCCESS] ALL TEST SUITES PASSED (EXIT CODE 0)':^80}")
    else:
        lines.append(f"{f'OVERALL RESULT: [FAILURE] {total_failed} TESTS/TARGETS FAILED (EXIT CODE 1)':^80}")
    lines.append("=" * 80)

    return "\n".join(lines)


# ==============================================================================
# MAIN CLI ENTRYPOINT
# ==============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Unified pure Python test runner for nyekripsi testing infrastructure."
    )
    parser.add_argument(
        "--tier",
        choices=["1", "2", "3", "4", "5", "all"],
        default="all",
        help="Specify which tier to run (default: all). Note: 3 and 4 map to E2E workloads.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Display verbose stdout and stderr for all passing tests (failures always displayed).",
    )
    parser.add_argument(
        "-x",
        "--fail-fast",
        action="store_true",
        help="Stop execution immediately upon first failure.",
    )
    parser.add_argument(
        "--json-report",
        type=str,
        default=None,
        help="Dump comprehensive test execution report to specified JSON file path.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all registered test targets and exit.",
    )

    args = parser.parse_args()

    # Filter targets
    if args.tier == "all":
        selected_targets = ALL_TARGETS
    elif args.tier in ("3", "4"):
        selected_targets = TIER_3_4_TARGETS
    elif args.tier == "1":
        selected_targets = TIER_1_TARGETS
    elif args.tier == "2":
        selected_targets = TIER_2_TARGETS
    elif args.tier == "5":
        selected_targets = TIER_5_TARGETS
    else:
        selected_targets = ALL_TARGETS

    if args.list:
        print("Registered Test Targets:")
        for t in selected_targets:
            print(f"  [Tier {t.tier}] {t.name:<35} - {t.description}")
        return 0

    print("=" * 80)
    print(f"{'NYEKRIPSI UNIFIED TEST RUNNER — E2E TEST TRACK':^80}")
    print("=" * 80)
    print(f"Repository : {REPO_ROOT}")
    print(f"Python     : {sys.version.split()[0]} ({sys.platform})")
    print(f"Selected   : Tier {args.tier.upper()} ({len(selected_targets)} targets)")
    print("=" * 80)
    print()

    results: List[TargetResult] = []
    start_all = time.perf_counter()
    any_failed = False

    current_tier = -1
    for target in selected_targets:
        if target.tier != current_tier:
            current_tier = target.tier
            tier_name = {
                1: "Tier 1: Static Linters & Repository Invariants",
                2: "Tier 2: Algorithmic Unit Tests",
                3: "Tier 3 & 4: Real-World E2E Thesis Workloads",
                5: "Tier 5: Adversarial Stress Testing",
            }.get(current_tier, f"Tier {current_tier}")
            print(f"\n>>> Running {tier_name}...")

        print(f"  * {target.name:<36} ... ", end="", flush=True)
        res = execute_target(target, verbose=args.verbose)
        results.append(res)

        if res.status == "PASS":
            unit_str = f" ({res.tests_run} tests)" if target.is_unittest else ""
            print(f"PASS [{res.duration_sec:5.2f}s]{unit_str}")
            if args.verbose and res.stdout.strip():
                for line in res.stdout.strip().splitlines():
                    print(f"      | {line}")
        elif res.status == "SKIPPED":
            print(f"SKIPPED [{res.duration_sec:5.2f}s]")
        else:
            any_failed = True
            unit_str = f" ({res.tests_failed}/{res.tests_run} failed)" if target.is_unittest else ""
            print(f"FAIL [{res.duration_sec:5.2f}s]{unit_str}")
            print("\n" + "!" * 80)
            print(f"FAILURE IN TARGET: {target.name}")
            print(f"Command: {' '.join(target.command)}")
            if res.stdout.strip():
                print("--- STDOUT ---")
                print(res.stdout.strip())
            if res.stderr.strip():
                print("--- STDERR ---")
                print(res.stderr.strip())
            print("!" * 80 + "\n")

            if args.fail_fast:
                print("Aborting early due to --fail-fast flag.")
                break

    total_time = time.perf_counter() - start_all
    print("\n" + render_scorecard(results, total_time))

    if args.json_report:
        report_data = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "repository": str(REPO_ROOT),
            "python_version": sys.version,
            "overall_status": "FAIL" if any_failed else "PASS",
            "exit_code": 1 if any_failed else 0,
            "total_duration_sec": total_time,
            "targets": [
                {
                    "name": r.target.name,
                    "tier": r.target.tier,
                    "status": r.status,
                    "returncode": r.returncode,
                    "duration_sec": r.duration_sec,
                    "tests_run": r.tests_run,
                    "tests_failed": r.tests_failed,
                    "description": r.target.description,
                }
                for r in results
            ],
        }
        report_path = pathlib.Path(args.json_report)
        report_path.write_text(json.dumps(report_data, indent=2), encoding="utf-8")
        print(f"\nJSON report written to: {report_path.resolve()}")

    return 1 if any_failed else 0


if __name__ == "__main__":
    sys.exit(main())
