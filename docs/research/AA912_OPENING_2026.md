# AA9/12 opening workflow — v0 research map

Status: **research in progress**.

This document covers only the first supported opening path and must be derived from Agenzia delle Entrate material. A field being visible on the paper form does **not** by itself prove that it is mandatory in every electronic opening.

## Source hierarchy

Use sources in this order:

1. current Agenzia delle Entrate product/model page;
2. current AA9/12 model and official instructions;
3. Agenzia provvedimenti and technical transmission specifications;
4. Agenzia compilation/control software behavior or release notes;
5. legislation referenced by the above material.

Third-party articles may help locate an official source but must never determine a production rule.

Current confirmed official baseline:

- AA9/12 is the form for VAT start/change/cessation by individual businesses and self-employed people;
- Provvedimento 3 June 2015 no. 75295 approved AA9/12 and its electronic transmission specifications;
- Agenzia's telematic-software notice confirms that the forfettario regime can be selected and, when selected, presumed turnover must not be entered;
- the official instructions currently available in the repository/library are the 2024 revision.

Before v0 production use, verify that no later Agenzia instruction/specification changes the fields used by our supported path.

## Supported archetype

The mapping is deliberately narrow:

- natural person;
- Italian tax resident;
- first VAT position;
- self-employed software developer;
- one prevalent activity;
- ATECO 2025 `62.10.00` after explicit confirmation;
- regime forfettario candidate;
- no representative;
- no extraordinary operation;
- no second VAT-relevant activity;
- no additional business location;
- no external accounting-record depositary;
- direct filing by the taxpayer, not filing by this application as an authorized intermediary.

A fact outside this boundary produces review/unsupported status instead of an invented default.

## Field-state vocabulary

Every field has one explicit state:

- `USER_INPUT` — user supplies or confirms the fact;
- `DERIVED` — mechanically derived from confirmed data;
- `DETERMINISTIC_RULE` — populated from a sourced rule;
- `CONDITIONAL` — requested only if a sourced condition is true;
- `NOT_APPLICABLE` — proven irrelevant to this supported case;
- `NEEDS_RESEARCH` — requiredness/meaning not sufficiently verified;
- `UNSUPPORTED` — legitimate case intentionally outside v0.

`NOT_APPLICABLE` must never mean "the model assumed no".

## Global form rules

| Field / rule | State | v0 behavior |
| --- | --- | --- |
| taxpayer fiscal code on form pages | `DERIVED` | copy validated fiscal code |
| page number / total pages | `DERIVED` | calculate from rendered packet |
| dates | `DERIVED` presentation | render in official form format |
| addresses | `USER_INPUT` | validate; never invent missing components |
| opening declaration timing | `DETERMINISTIC_RULE` | validate against official 30-day filing rule |
| future start date relative to filing | invalid | reject before export |

## Quadro A — declaration type

For first opening:

| Field | State | Value / behavior |
| --- | --- | --- |
| declaration type | `DETERMINISTIC_RULE` | `1` — start of activity |
| activity start date | `USER_INPUT` | explicit factual date; never tax-optimized by AI |
| VAT number | `NOT_APPLICABLE` | blank before attribution |
| variation/cessation | `NOT_APPLICABLE` | separate workflows |

## Quadro B — taxpayer and prevalent activity

### Identity

- legal name: confirmed user identity, no invented abbreviations;
- nonresident address/foreign VAT id: `NOT_APPLICABLE` for v0 Italian-resident path.

### Activity

| Field | State | v0 behavior |
| --- | --- | --- |
| activity code | `DERIVED` after confirmation | current ATECO code at filing; target `62.10.00` |
| activity description | `DERIVED` | official description corresponding to code |
| presumed turnover | `DETERMINISTIC_RULE` | blank for a taxpayer choosing forfettario |
| art. 60-bis intra-EU goods checkbox | `CONDITIONAL` | separate from VIES; ask only if relevant |
| activity/studio address | `USER_INPUT` | confirm where the professional ordinarily exercises the activity |
| accounting-records checkbox | `CONDITIONAL` | based on actual record-storage facts |
| subsidized tax regime | `DETERMINISTIC_RULE` after eligibility + intent | code `2` for forfettario |

### What "studio / activity address" means for our user

The regime forfettario does **not** require the taxpayer to own or rent a separate office.

For a software developer working from home, the home can be the place where the professional activity is exercised. The UI should therefore ask a human question such as:

> Where do you normally carry out your freelance activity?
> - my home
> - a separate office/studio
> - coworking/other place
> - I do not have one stable place

The answer is then mapped deterministically to the form/review flow. Never tell a user they need to acquire an office or property merely because AA9/12 contains address/property fields.

### Electronic commerce

Remote software development, having a website, GitHub profile or portfolio is not by itself electronic commerce for this form section.

- explicit supported `does_ecommerce = false` -> blank;
- true/ambiguous -> collect the dedicated facts or require review until that path is specified.

## Quadro C — holder

Collect/validate:

- fiscal code;
- legal name;
- birth date;
- birth municipality/state and province where applicable;
- anagraphic residence;
- fiscal domicile when legally different.

For the ordinary Italian resident path, residence and fiscal-domicile municipality generally align under the rule cited by the official instructions. If the user has an exceptional fiscal domicile established under art. 59, v0 escalates instead of silently copying residence.

## Quadri D–H — explicit v0 gates

These sections are not "ignored"; their triggering conditions are checked.

| Quadro | Trigger | v0 |
| --- | --- | --- |
| D — representative | representative/heir/judicial/fiscal representative | `UNSUPPORTED` / review |
| E — extraordinary operations | acquisition, donation, succession, business lease, transformation | `UNSUPPORTED` / review |
| F — accounting records | external depositary/additional or foreign storage places | simple self-held path only; otherwise review |
| G — other activities/locations | multiple VAT activities or other places | `UNSUPPORTED` initially |
| H — special representation relationship | goods-representation case under cited rule | `UNSUPPORTED` |

## Quadro I — opening-only information

The official instructions contain Quadro I for start-of-activity information. We must model its possible fields, but **must not treat every visible field as universally mandatory**.

### Contact fields

Potential fields:

- email;
- telephone;
- fax;
- website distinct from an e-commerce site already reported in Quadro B.

Exact mandatory/optional validation status follows the official technical specification/control behavior, not UI guesswork.

### Property / cadastral fields — current status

Official instructions describe data relating to the property used for the prevalent activity, including possession/detention, cadastral identifiers and, for lease/free-loan cases, registration details.

This does **not** imply that every single home-based forfettario programmer must always be asked for all cadastral fields.

Until issue #8 verifies the current AA9/12 transmission/control specification, v0 classifies these fields as:

`NEEDS_RESEARCH -> CONDITIONAL`

not `REQUIRED_FOR_V0`.

Required UX principle:

1. first establish the actual place-of-activity fact;
2. determine from official validation rules whether property information is required for that fact pattern;
3. reveal only the required fields;
4. if official requiredness remains unresolved, block final export/filing guidance rather than guessing.

### VIES / intra-EU operations

Quadro I's intra-EU operation information is conceptually separate from Quadro B's art. 60-bis checkbox.

The user-facing question must describe the actual business situation rather than ask "Do you need VIES?". Exact wording remains P0 research.

### Activity-specific client/public-place/investment information

These additional fields apply only to activity codes identified by the relevant Agenzia provisions.

The historical special-code list does not include programming code `62.01.00`, the predecessor of ATECO 2025 `62.10.00`. Before encoding `NOT_APPLICABLE`, retain the source-backed ATECO correspondence in the rule registry.

## Signatures and attachments

The app may prepare a draft/review packet but never fabricate the taxpayer's signature.

Derived:

- completed-quadri list;
- page count;
- signer fiscal code from confirmed profile.

User action:

- review;
- confirm;
- sign/date as required by the filing channel.

Attachments are channel/fact dependent. For example, the official instructions require an identity-document copy for postal submission. Do not globally hardcode "no attachments".

## Submission

Official instructions permit, for taxpayers not required to register with Registro delle Imprese, direct office delivery, registered post, or telematic filing directly/by an authorized intermediary.

Agenzia's telematic material confirms that AA9/12 has an official compilation/control path and technical file specifications.

v0 is **not** an authorized intermediary. We must decide separately whether v0:

- only produces a reviewable human-signable packet/checklist; or
- also produces a technically valid telematic payload for direct taxpayer submission.

The latter requires exact specification/control tests before implementation.

## Internal contract direction

`AA912Draft.fields: dict[str, str]` is only temporary scaffolding.

The final document module should own typed sections such as:

```text
AA912Draft
├── header
├── declaration
├── taxpayer
├── holder
├── opening_information
└── completion
```

Every consequential field definition carries:

```text
field_id
value_type
state/origin
required_when
validation
source_id
review_behavior
```

The renderer receives an already validated draft and contains **zero fiscal decision logic**.

## P0 open work

1. #8 — verify Quadro I property-field requiredness for the home-based professional path against Agenzia technical validation.
2. Verify current direct electronic filing UX and the applicable AA9/12 technical payload/control package.
3. Define exact accounting-record-storage UX for a simple professional.
4. Define plain-language VIES questions and edge cases.
5. Confirm the source-backed ATECO correspondence used for activity-specific Quadro I fields.
6. Keep Gestione Separata registration as a separate workflow; it is not an AA9/12 field.
7. Confirm no newer Agenzia update supersedes the current model/instructions/specification used by v0.

Issue #1 closes only when every field reachable by the supported path is typed, sourced and deterministically required/conditional/not-applicable, and a synthetic taxpayer can produce the same validated draft without an LLM.
