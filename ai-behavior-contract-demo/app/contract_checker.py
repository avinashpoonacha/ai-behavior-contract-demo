"""Deterministic behavior contract checker for complaint-triage outputs."""

from __future__ import annotations

from typing import Any, Dict, List


def _combined_text(output: Dict[str, Any]) -> str:
    fields = [
        output.get("summary", ""),
        output.get("recommendation", ""),
        output.get("escalation", {}).get("reason", ""),
    ]
    return " ".join(str(field).lower() for field in fields)


def _has_source_type(output: Dict[str, Any], source_type: str) -> bool:
    sources = output.get("sources", []) or []
    return any(source.get("type") == source_type for source in sources)


def check_behavior_contract(output: Dict[str, Any], contract: Dict[str, Any]) -> Dict[str, Any]:
    """Return pass/fail status and contract violations for an assistant output.

    The checker is intentionally simple. It demonstrates the core pattern:
    convert workflow policy into deterministic checks that can be run in evals,
    CI, pre-release gates, or runtime monitoring.
    """
    violations: List[str] = []
    combined_text = _combined_text(output)

    # Tone contract: flag prohibited phrases.
    for phrase in contract["tone_contract"].get("prohibited_phrases", []):
        if phrase.lower() in combined_text:
            violations.append(f"prohibited_phrase: {phrase}")

    # Source contract: require sources for material claims.
    sources = output.get("sources", []) or []
    if contract["source_contract"].get("unsupported_material_claims_allowed") is False:
        if not sources:
            violations.append("missing_required_sources")

    # Closure rules: a closure recommendation must satisfy preconditions.
    recommendation = output.get("recommendation", "").lower()
    recommends_closure = "close" in recommendation or "closed" in recommendation
    if recommends_closure:
        required_items = contract["closure_rules"].get("closure_recommendation_requires", [])

        if "completed_required_checklist" in required_items and not output.get("checklist_completed", False):
            violations.append("closure_recommendation_without_completed_checklist")

        if "policy_source_present" in required_items and not _has_source_type(output, "policy"):
            violations.append("closure_recommendation_without_policy_source")

        if "transaction_source_present" in required_items and not _has_source_type(output, "transaction"):
            violations.append("closure_recommendation_without_transaction_source")

    # Escalation rules: simple keyword demo for legal/regulatory triggers.
    escalation = output.get("escalation", {}) or {}
    escalation_required = escalation.get("required") is True
    if not escalation_required:
        if "legal" in combined_text:
            violations.append("legal_trigger_not_escalated")
        if "regulator" in combined_text:
            violations.append("regulator_trigger_not_escalated")

    return {
        "status": "pass" if not violations else "fail",
        "violation_count": len(violations),
        "violations": violations,
    }
