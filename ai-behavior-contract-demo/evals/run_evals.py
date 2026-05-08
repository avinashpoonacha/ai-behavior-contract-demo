"""Run behavior-contract evals for the complaint-triage demo."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

# Allow running from repo root without installing as a package.
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from app.assistant_stub import load_cases  # noqa: E402
from app.contract_checker import check_behavior_contract  # noqa: E402


def load_contract(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def main() -> int:
    contract = load_contract(REPO_ROOT / "contracts" / "complaint_triage_contract.yaml")
    cases = list(load_cases(REPO_ROOT / "data" / "complaint_cases.jsonl"))

    results: List[Dict[str, Any]] = []
    for case in cases:
        result = check_behavior_contract(case["assistant_output"], contract)
        results.append({
            "case_id": case["case_id"],
            "description": case["description"],
            **result,
        })

    print(json.dumps(results, indent=2))

    failures = sum(1 for result in results if result["status"] == "fail")
    passes = len(results) - failures
    print(f"\nSummary: {passes} passed, {failures} failed, {len(results)} total")

    # This demo returns 0 so readers can inspect the report without CI failing.
    # In a real release gate, you may return non-zero if blocker violations exist.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
