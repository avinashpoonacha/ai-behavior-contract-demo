# Sample Behavior Report

Generated from the demo test set.

| Case | Status | Key finding |
|---|---|---|
| C-001 | Fail | Prohibited tone, missing sources, premature closure recommendation. |
| C-002 | Pass | Neutral, sourced, and escalates due to incomplete evidence. |
| C-003 | Fail | Mentions regulator but does not escalate; contains prohibited phrase. |

## Why this report matters

The report turns subjective review into operational telemetry. In production, the same pattern could feed dashboards for:

- prohibited phrase rate;
- unsupported claim rate;
- escalation miss rate;
- closure recommendation rate;
- retrieval skipped rate;
- human override rate.
