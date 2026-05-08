# AI Behavior Contract Demo

This companion repo supports the blog post **["The AI Behavior Contract: How Enterprises Can Detect and Control Model Drift."](https://avinashpoonacha.us/writing/the-model-is-not-yours)**

It demonstrates a lightweight contract-checker pattern for a regulated complaint-triage assistant. The repo is intentionally small: it is not a production complaint-management system, and it does not attempt to solve model alignment in general.

## What this demonstrates

- A behavior contract expressed as YAML.
- A small set of complaint-triage test cases.
- A deterministic contract checker for prohibited phrases, missing sources, escalation gaps, and premature closure recommendations.
- A simple eval runner that produces pass/fail results.

## Repository structure

```text
ai-behavior-contract-demo/
  README.md
  requirements.txt
  data/
    complaint_cases.jsonl
  contracts/
    complaint_triage_contract.yaml
  app/
    assistant_stub.py
    contract_checker.py
  evals/
    run_evals.py
  reports/
    sample_behavior_report.md
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python evals/run_evals.py
```

Expected result: one compliant output should pass; outputs with prohibited phrases, missing sources, premature closure, or missed escalation triggers should fail.

## Why this matters

Enterprises usually cannot inspect or control the reward signals used to train a commercial foundation model. But they can define and enforce the behavior expected inside a specific workflow.

This repo demonstrates the core idea:

> Do not only ask the model to follow the rules. Build a system that checks whether it did.

## Limitations

This demo uses deterministic checks only. A production version would typically include:

- structured outputs;
- source and retrieval-trace validation;
- policy-service integration;
- human-review sampling;
- LLM-as-judge scoring for tone or nuance;
- runtime telemetry and dashboards;
- release gates and rollback workflows;
- audit logging aligned to enterprise governance requirements.
