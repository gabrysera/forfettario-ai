# ADR-002 — Fail closed on unsupported or ambiguous tax cases

## Status
Accepted.

## Decision
If a material fiscal fact is missing, ambiguous, contradictory, unsupported by the current ruleset, or requires professional interpretation, the system must not force the case through the supported flow.

Use one of:

- `USER_CONFIRMATION_REQUIRED`
- `PROFESSIONAL_REVIEW_REQUIRED`
- `UNSUPPORTED`

## Rationale
A narrow system that stops reliably is safer and easier to validate than a broad system that guesses.

## Consequences

- Every deterministic eligibility rule must be able to return `unknown` as well as pass/fail where appropriate.
- UI must clearly explain why execution stopped.
- New supported cases are added explicitly through requirements, rules and tests.
