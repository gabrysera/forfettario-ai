# Regime forfettario — deterministic v0 rules for 2026

This specification is authoritative for the executable 2026 v0 engine.

It deliberately separates:

1. access/exclusion from the regime;
2. reduced 5% startup-rate eligibility;
3. profitability coefficient / taxable-base calculation;
4. current-year exit rules.

A user can satisfy one section and fail another. Never collapse these concepts into one boolean.

## Result contract

Each condition returns exactly one of:

- `PASS` — known facts satisfy the condition;
- `FAIL` — known facts violate the condition;
- `UNKNOWN` — the engine lacks enough facts or the v0 scope does not safely resolve the case.

Overall eligibility is:

- `False` if any condition is `FAIL`;
- `None` if none fail and at least one is `UNKNOWN`;
- `True` only when every required condition is `PASS`.

## Source registry used here

### `LAW190-C54`
Law 23 December 2014 no. 190, art. 1, comma 54, current text.

- previous-year revenues/compensation not above EUR 85,000;
- previous-year gross labour/collaborator expenses not above EUR 20,000.

Primary source: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2014;190

### `LAW190-C57-A` .. `LAW190-C57-DTER`
Law 190/2014, art. 1, comma 57, current exclusion conditions.

Primary source: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2014;190

### `LAW207-2024-C12`
Law 30 December 2024 no. 207, art. 1, comma 12, current text: for 2025 and 2026 the employment-income threshold referenced by comma 57(d-ter) is EUR 35,000.

Primary source: https://www.normattiva.it/eli/id/2024/12/31/24G00229/ORIGINAL

### `LAW190-C65-A` .. `LAW190-C65-C`
Law 190/2014, art. 1, comma 65: reduced 5% substitute-tax rate for the starting tax period plus four subsequent periods, subject to the three statutory conditions.

Primary source: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2014;190

## Access rules

| ID | Deterministic condition | v0 behavior |
| --- | --- | --- |
| `FORF-ACCESS-001` | Previous-year business revenues/compensation <= EUR 85,000 | amount missing -> `UNKNOWN` |
| `FORF-ACCESS-002` | Previous-year labour/collaborator expenses <= EUR 20,000 | amount missing -> `UNKNOWN` |
| `FORF-EXCL-001` | Taxpayer does not use a special VAT regime / other forfettario income regime incompatible under comma 57(a) | fact missing -> `UNKNOWN` |
| `FORF-EXCL-002` | v0 supports Italian tax residents | resident -> `PASS`; non-resident/unknown -> `UNKNOWN`, because comma 57(b) contains exceptions that v0 does not yet model |
| `FORF-EXCL-003` | Taxpayer does not exclusively/prevalently make the real-estate/buildable-land/new-vehicle transactions in comma 57(c) | fact missing -> `UNKNOWN` |
| `FORF-EXCL-004` | No simultaneous participation in partnership/association/family business described by comma 57(d) | fact missing -> `UNKNOWN` |
| `FORF-EXCL-005` | No direct/indirect control of a limited company/participation association whose activity is directly/indirectly related as described by comma 57(d) | fact missing -> `UNKNOWN` |
| `FORF-EXCL-006` | Activity is not carried out prevalently for a current employer, an employer from the two previous tax periods, or related subjects, as described by comma 57(d-bis) | fact missing -> `UNKNOWN` |
| `FORF-EXCL-007` | Previous-year employment/assimilated income <= EUR 35,000 for 2026; threshold check is irrelevant when the employment relationship has ended | missing income/end-state -> `UNKNOWN` |

## Reduced 5% startup rate

The reduced rate is assessed independently from regime access.

| ID | Deterministic condition | Source |
| --- | --- | --- |
| `FORF-STARTUP-001` | No artistic/professional/business activity exercised in the three years before the new activity | comma 65(a) |
| `FORF-STARTUP-002` | New activity is not a mere continuation of prior dependent or self-employed activity, except mandatory professional practice | comma 65(b) |
| `FORF-STARTUP-003` | If continuing an activity previously run by another person, predecessor's prior-year revenues/compensation are not above the comma-54 limit | comma 65(c) |

### Prior occasional work

The engine **must not** infer `FORF-STARTUP-001` or `FORF-STARTUP-002` from the amount of prior occasional income.

In particular, EUR 5,000 is not encoded as a threshold that decides whether an activity was occasional or professional. Classification of the prior activity is a separate fact/research problem. Until that classification is known, the relevant startup-rate fact remains `UNKNOWN`.

This protects the engine from the common but incorrect shortcut `occasional_income <= 5000 => new professional activity`.

## Profitability coefficient

`FORF-PROFIT-001` — **NEEDS_RESEARCH / issue #10**.

Known evidence indicates ATECO division 62 is historically/currently grouped under `Altre attività economiche` with a 67% coefficient. Before this value enters executable v0 code, the repository requires an explicit current 2026 official source and a documented ATECO 2025 `62.10.00` mapping.

Do not infer a 78% coefficient merely because the user is colloquially a "professional".

## Current-year exit

The EUR 100,000 immediate-exit rule is intentionally not part of `assess_forfettario_access()`, because it concerns continuation/exit during the tax year rather than opening/access based on prior-year facts.

It will be implemented as a separate cash-event rule using compensation **perceived/collected**, not invoice issue totals.

Source: Law 29 December 2022 no. 197, art. 1, comma 54, amending law 190/2014 comma 71.

Primary source: https://www.normattiva.it/eli/id/2022/12/29/22G00211/ORIGINAL

## Non-goals of this first executable rule set

- non-resident exceptions;
- nuanced corporate-control determinations;
- automatic legal classification of prior occasional work;
- profitability coefficient until #10 is closed;
- EUR 100,000 current-year exit implementation;
- tax or INPS arithmetic.

Those cases fail closed instead of being guessed.
