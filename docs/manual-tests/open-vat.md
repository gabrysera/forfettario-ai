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
- no complex foreign situation;
- one prevalent activity and one activity address;
- accounting records kept at the activity address.

Never use real personal identifiers in automated/manual test evidence.

Install the exact official AA9/12 PDF supported by `app/documents/aa912/template.py`. The installer/validator must reject a different fingerprint even when the replacement also contains five pages.

## Cases

Run the document portion of this test for all three committed synthetic golden profiles:

1. `tests/golden/aa912_home_owned_no_vies.json`
2. `tests/golden/aa912_home_rented_no_vies.json`
3. `tests/golden/aa912_home_owned_vies.json`

These cover the minimum consequential Quadro I branches: possession vs detention and VIES yes/no.

## Steps

1. Start onboarding from an empty profile and verify that material yes/no branch answers are not silently preselected.
2. Describe/confirm the activity as freelance software development.
3. Answer all required eligibility questions with facts that deterministically pass the supported 2026 forfettario access assessment.
4. Confirm the proposed activity classification.
5. Enter required identity/address/start-date fields using synthetic data.
6. Confirm whether the activity is carried out at the residence and where records are kept.
7. Enter the activity-property data requested for Quadro I.
8. If the property is rented/loaned (`D`), enter the contract-registration details.
9. Explicitly choose whether intra-EU operations/VIES are intended; when yes, enter expected purchases and sales in whole euros.
10. Request preparation of the opening package.
11. Open the generated official AA9/12 PDF.
12. Inspect physical page 2 (declaration page 1), physical page 4 (Quadro I) and physical page 5 (compiled-quadri/signature area).
13. Inspect the audit/explanation view when that part of the wider MVP is available.
14. Repeat the PDF generation/review for each golden case above.

## Expected — deterministic/product behavior

- The app does not infer unanswered material facts.
- Material yes/no choices that affect eligibility, activity/address, records location, property tenure or VIES require an explicit user answer.
- Activity and ATECO classification are distinct but linked.
- Classification shown: ATECO 2025 `62.10.00` only when deterministic support exists and the user confirms the supported activity.
- AA9/12 generation calls the deterministic 2026 forfettario access assessment before mapping regime code `2`.
- A failed or unknown eligibility condition blocks document generation and identifies the area that requires review.
- The same structured inputs produce the same deterministic result without an LLM.
- AA9/12 mapping contains no unsupported guessed values.
- Browser-supplied rogue ATECO or regime values cannot override the deterministic mapping.
- A records location outside the supported activity-address path fails closed.
- The output is marked for human review/signature and does not claim that submission occurred or that a VAT number was opened.
- When the wider MVP audit slice is connected, its audit record identifies the ruleset version and sources used.

## Expected — official PDF geometry/content

For every case:

- the output preserves all five physical pages of the official template;
- taxpayer fiscal code is placed in the page headers without overwriting unrelated fields;
- progressive declaration page numbers are correct;
- Quadro A marks an opening declaration and contains the confirmed start date;
- Quadro B contains deterministic ATECO `62.10.00`, the supported activity description, activity address and regime code `2`;
- Quadro C contains the synthetic taxpayer identity/residence data;
- Quadro I contains contact and activity-property data in the intended fields;
- signature summary marks `A`, `B`, `C`, `I` and total declaration pages `4`;
- signer fiscal code is present, but the signature itself remains blank;
- no overlay text visibly crosses a field boundary or label.

Case-specific expectations:

### Home-owned / no VIES

- property tenure is `P`;
- cadastral data are populated;
- contract-registration fields are blank;
- intra-EU expected-volume fields are blank.

### Home-rented / no VIES

- property tenure is `D`;
- cadastral data are populated;
- contract date, office and registration number are populated in their Quadro I fields;
- intra-EU expected-volume fields are blank.

### Home-owned / VIES

- property tenure is `P`;
- expected intra-EU purchases and sales are populated in the corresponding Quadro I fields;
- the two amounts are aligned inside the printed boxes and do not overlap the labels below/above them.

## Negative spot checks

In the same build, verify at least these failures:

- an eligibility fact that makes the deterministic forfettario assessment fail => no PDF is generated;
- supported software activity is not confirmed => no PDF is generated;
- required eligibility fact omitted or invalid => validation error and no PDF;
- invalid Italian fiscal-code checksum => validation error;
- detention without required contract-registration details => validation error;
- VIES yes without both expected volumes => validation error;
- non-whole-euro VIES expected volume => validation error;
- records stored outside the supported activity address => fail closed and no PDF;
- different/modified AA9/12 PDF fingerprint => unsupported template;
- value too wide for its physical field => document generation fails instead of clipping silently.

## Evidence

Capture:

- final onboarding/profile screen;
- eligibility explanation;
- generated AA9/12 PDFs for all three golden cases;
- screenshots/rendered images of physical pages 2, 4 and 5 for each case;
- audit/source view when available in the wider MVP;
- CI run identifier and commit SHA;
- exact supported official-template SHA-256.

## Pass condition

This test passes only when the complete #4 vertical slice is connected and:

- every AA9/12 field reached by the supported archetype is mapped to an authoritative source or explicitly user-provided;
- automated CI is green;
- all three golden cases render successfully against the exact pinned official template;
- the required pages have been visually inspected with no material geometry defect;
- unsupported branches continue to fail closed;
- eligibility/classification/audit requirements from the wider MVP are wired end to end.
