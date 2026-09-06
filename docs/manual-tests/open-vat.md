# MT-001 — Open VAT position happy path

Requirements: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-011, FR-012.

## Preconditions

Use a synthetic user who matches the v0.1 supported archetype:

- Italian tax resident natural person;
- first VAT position;
- freelance software developer;
- intended activity compatible with ATECO 2025 `62.10.00`;
- candidate for regime forfettario;
- Gestione Separata path with no other mandatory pension coverage;
- one prevalent activity and one place of business;
- no representative;
- no extraordinary business operation;
- no external accounting-record depositary;
- no e-commerce activity;
- no known exclusion condition;
- no complex foreign tax situation.

Never use real personal identifiers in automated/manual test evidence.

## Synthetic opening facts

The fixture must explicitly contain, rather than let the AI infer:

- fiscal code and legal name;
- date and place/province of birth;
- full anagraphic residence;
- whether a different fiscal domicile was established by the tax administration (happy path: no);
- actual activity start date;
- confirmed studio/place-of-business address;
- where tax/accounting records are kept;
- email and telephone;
- whether a fax number exists;
- whether a non-e-commerce website exists;
- title to the property used for the activity (`P` possession or `D` detention);
- cadastral data required by Quadro I;
- if detained through lease/gratuitous loan, the contract-registration details;
- whether intra-EU/VIES operations are expected and the required estimates if yes;
- explicit no to e-commerce, additional activities/locations, representative, extraordinary operations and external document depositary.

For the simplest happy-path fixture, choose facts that keep conditional sections small, but never omit a fact solely to make the test easier.

## Steps

1. Start onboarding from an empty profile.
2. Describe the activity in natural language as freelance software development.
3. Answer all required eligibility questions.
4. Confirm the proposed activity classification.
5. Enter the synthetic identity, residence and start-date facts.
6. Confirm the activity/studio address and accounting-record location.
7. Complete the Quadro I opening facts (contact, property/cadastral and intra-EU/VIES intent).
8. Explicitly answer the v0 scope gates (no representative, extraordinary operation, extra activity/location, e-commerce or external depositary).
9. Request preparation of the opening package.
10. Open the generated AA9/12 review representation.
11. Inspect the audit/explanation view.

## Expected

- The app does not infer unanswered material facts.
- Activity and ATECO classification are distinct but linked.
- Classification shown: ATECO 2025 `62.10.00` only when deterministic support exists and the user confirms it.
- Eligibility result includes condition-level outcomes and a review status.
- Quadro A is an opening declaration and contains the explicitly confirmed start date.
- The start date is not after the intended presentation date; filing-window validation is shown.
- Quadro B uses the confirmed activity/studio address rather than silently copying residence.
- Quadro B presumed turnover is blank when the supported user chooses regime forfettario.
- Quadro B regime fiscale agevolato is populated only after deterministic eligibility and user intent are established.
- Quadro C contains the confirmed taxpayer identity/residence facts.
- Quadro I contains the applicable opening contact and property/cadastral facts.
- Activity-specific Quadro I client/public-place/investment fields are not populated for ATECO `62.10.00`.
- Quadro D/E/F/G/H stay blank only because their triggering facts were explicitly ruled out.
- Delegation/intermediary fields remain blank for the direct-submission path.
- The same structured inputs produce the same deterministic result without an LLM.
- AA9/12 mapping contains no unsupported guessed values.
- The output is marked for human review and does not claim that submission occurred.
- The app never generates a taxpayer signature.
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

Open research items are tracked in `docs/research/AA912_OPENING_2026.md`.
