# MT-001 — Open VAT position happy path

Requirements: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-011, FR-012.

## Preconditions

Use a synthetic user who matches the v0.1 supported archetype:

- Italian tax resident natural person;
- freelance software developer;
- intended activity compatible with ATECO 2025 `62.10.00`;
- candidate for regime forfettario;
- Gestione Separata path with no other mandatory pension coverage;
- no known exclusion condition;
- no complex foreign situation.

Never use real personal identifiers in automated/manual test evidence.

## Steps

1. Start onboarding from an empty profile.
2. Describe the activity in natural language as freelance software development.
3. Answer all required eligibility questions.
4. Confirm the proposed activity classification.
5. Enter required identity/address/start-date fields using synthetic data.
6. Request preparation of the opening package.
7. Open the generated AA9/12 review representation.
8. Inspect the audit/explanation view.

## Expected

- The app does not infer unanswered material facts.
- Activity and ATECO classification are distinct but linked.
- Classification shown: ATECO 2025 `62.10.00` only when deterministic support exists and the user confirms it.
- Eligibility result includes condition-level outcomes and a review status.
- The same structured inputs produce the same deterministic result without an LLM.
- AA9/12 mapping contains no unsupported guessed values.
- The output is marked for human review and does not claim that submission occurred.
- An audit record identifies the ruleset version and sources used.

## Evidence

Capture:

- final onboarding/profile screen;
- eligibility explanation;
- AA9/12 review screen/export;
- audit/source view;
- test run identifier and commit SHA.

## Blocking condition

This test must remain incomplete until every AA9/12 field required for the supported archetype is mapped to an authoritative source or explicitly marked as user-provided.
