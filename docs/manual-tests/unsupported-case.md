# MT-002 — Unsupported case fails closed

Requirements: FR-001, FR-005, FR-011.

## Preconditions

Use a synthetic user outside the v0.1 archetype, for example a taxpayer with a professional pension fund or an activity outside the supported ATECO scope.

## Steps

1. Start onboarding.
2. Enter facts that put the user outside the supported path.
3. Continue until the unsupported condition is detected.

## Expected

- The app does not invent a compatible path.
- The result is `PROFESSIONAL_REVIEW_REQUIRED` or `UNSUPPORTED`.
- The blocking reason is explicit.
- No actionable fiscal calculation or AA9/12 output is presented as validated.
- The event is recorded in the audit trail.
