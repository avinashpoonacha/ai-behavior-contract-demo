"""Canned assistant outputs for the behavior-contract demo.

This module intentionally does not call a live LLM. In production, this would be
replaced by the actual assistant invocation plus retrieval/tool traces.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable


def load_cases(path: Path) -> Iterable[Dict[str, Any]]:
    """Yield JSONL test cases from disk."""
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)
