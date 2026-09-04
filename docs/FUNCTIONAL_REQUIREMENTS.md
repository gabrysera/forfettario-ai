# Functional requirements

This is the canonical requirements document. IDs are stable and should be referenced by tests and PRs.

## FR-001 — Supported-person check
The system must determine whether the user matches the currently supported taxpayer archetype before producing actionable fiscal outputs.

Output must include a review status and unsupported reasons.

## FR-002 — Structured onboarding
The system must collect the minimum facts needed for eligibility, registration, social-security classification and document generation.

Material missing facts must never be silently inferred.

## FR-003 — Activity classification
The system must represent the user's activity separately from the ATECO code and require confirmation before document generation.

Initial supported activity: software programming, ATECO 2025 `62.10.00`.

## FR-004 — Tax profile
The system must produce a versioned structured profile containing at least:

- jurisdiction;
- tax year / applicable period;
- activity;
- ATECO;
- regime status;
- social-security status;
- start date;
- relevant prior/current income facts;
- review status;
- ruleset version.

## FR-005 — Deterministic eligibility
Regime eligibility checks must be deterministic and explain each passed/failed/unknown condition.

## FR-006 — AA9/12 preparation
The system must map the supported profile to an internal AA9/12 field model, validate required fields and generate a human-reviewable output.

The MVP does not claim to submit the form on behalf of the taxpayer.

## FR-007 — Invoice model
The system must support creating an invoice draft from structured client/service data.

Invoice issuance and payment collection must be separate states.

## FR-008 — Payment / cash ledger
The system must store collections independently from invoices and use tax-relevant cash events where required by the ruleset.

## FR-009 — Tax reserve estimate
The system must provide an explainable estimate of tax and social-security amounts to reserve based only on deterministic calculations.

Every estimate must display:

- applicable period;
- ruleset version;
- inputs used;
- calculation components;
- whether it is an estimate or a final amount.

## FR-010 — Deadlines
The system must represent deadlines as sourced, versioned obligations with status and applicability conditions.

## FR-011 — Review escalation
Any ambiguous, unsupported or incomplete case must produce `PROFESSIONAL_REVIEW_REQUIRED` or `UNSUPPORTED` rather than a guessed answer.

## FR-012 — Auditability
For every consequential output, the system must be able to show the input snapshot, ruleset version, deterministic calculation and source references that produced it.

## FR-013 — Data deletion/export
A user must be able to export their own structured data and request deletion. Exact retention behavior must be specified before production.

## FR-014 — AI trace boundary
The app must distinguish conversational AI text from deterministic engine results in its internal representation so that an LLM response cannot overwrite fiscal state without validation.
