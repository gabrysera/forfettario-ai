# Research backlog before production

These questions are intentionally unresolved. They should become sourced requirements/tests before the corresponding feature ships.

## P0 — required for opening workflow

- Exact supported opening channels for AA9/12 in 2026 and their technical constraints.
- Exact AA9/12 field mapping for the first taxpayer archetype.
- Whether/how the user must separately register with INPS Gestione Separata and the supported digital workflow.
- Eligibility/exclusion conditions for regime forfettario, including prior employment/related-party edge cases.
- Conditions for the reduced 5% substitute-tax rate for new activities.
- Correct profitability coefficient for each supported ATECO classification/version.
- Interaction between prior occasional work and the new VAT activity when the activity is substantively the same.

## P0 — required before invoice issuance

- Current electronic-invoicing obligations for the supported user.
- SdI technical/API strategy and whether a third-party intermediary is needed.
- Mandatory wording/nature codes for forfettario invoices.
- Stamp-duty applicability, deadlines and payment workflow.
- Italian vs EU vs extra-EU client rules.

## P0 — legal/privacy

- Define exactly which features are software assistance vs regulated/intermediary/professional activity.
- Terms of service and limitation-of-scope wording.
- GDPR roles, lawful bases, retention, subprocessors and DPA requirements.
- LLM data-processing configuration and EU data-location requirements.
- Incident-response and breach-notification process.

## P1 — tax lifecycle

- Advance/saldo calculation rules and relevant payment deadlines.
- F24 code generation and validation.
- REDDITI PF / Quadro LM mapping.
- Quadro RR / Gestione Separata mapping.
- Treatment of prior-year contributions deducted in the current return.
- Handling credits, late payments and corrections.

## P1 — product trust

- professional-review workflow;
- rule-source provenance UI;
- immutable calculation snapshots;
- change notifications when a ruleset changes;
- regression corpus reviewed by an accountant.
