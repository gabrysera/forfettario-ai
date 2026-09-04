# AA9/12 opening workflow — v0 research map

Status: **research in progress**. This document is intentionally stricter than the form itself: unresolved consequential fields remain unresolved rather than being guessed.

## Scope

This mapping covers only the first supported archetype:

- natural person;
- Italian tax resident;
- first VAT position;
- self-employed professional / software developer;
- one prevalent activity;
- ATECO 2025 `62.10.00` after explicit activity confirmation;
- candidate for regime forfettario;
- no representative;
- no extraordinary business operation;
- no second activity or second place of business;
- no external accounting-record depositary;
- direct submission by the taxpayer, not by this application as an authorized intermediary.

Anything outside these assumptions must not be forced through this mapping.

## Sources reviewed

Primary/authoritative sources:

1. Agenzia delle Entrate, **Modello AA9/12**.
2. Agenzia delle Entrate, **AA9/12 — Istruzioni per la compilazione (2024 revision)**.
3. Agenzia delle Entrate, Provvedimento 21 December 2006, art. 35(15-ter) implementation, published in G.U. Serie Generale n. 3, 4 January 2007.
4. Agenzia delle Entrate, Provvedimento 14 January 2008, update of activity codes requiring additional Quadro I activity information.
5. ISTAT, ATECO 2025 / 2026 technical documentation and correspondence tables.

Page references below refer to the 2024 AA9/12 instructions unless otherwise noted.

## Field-origin vocabulary

Every eventual internal AA9/12 field should have one explicit origin:

- `USER_INPUT`: the user must supply or confirm the fact.
- `DERIVED`: mechanically derived from already confirmed data.
- `DETERMINISTIC_RULE`: filled from a sourced deterministic rule.
- `CONDITIONAL`: required only when a sourced condition is true.
- `NOT_APPLICABLE`: proven not applicable to the supported case.
- `NEEDS_RESEARCH`: source/requiredness is not yet resolved.
- `UNSUPPORTED`: valid tax situation, but outside v0.

`NOT_APPLICABLE` must never mean "the AI assumed no".

## Global form rules

| Field / rule | Origin | v0 behavior | Source |
| --- | --- | --- | --- |
| Taxpayer fiscal code at top of each page | `DERIVED` | Copy confirmed taxpayer fiscal code to every generated form page | Instructions p.1 |
| Page number | `DERIVED` | Generate progressively | Instructions p.1 |
| Total pages | `DERIVED` | Generate from actual completed form packet | Instructions p.1 / signature section |
| Date formatting | `DERIVED` | DD/MM/YYYY in rendered form | Instructions p.1 |
| Full addresses / no abbreviations | `USER_INPUT` + validation | Normalize only presentation; never invent missing address parts | Instructions p.1 |
| Filing deadline | `DETERMINISTIC_RULE` | Opening declaration is due within 30 days of actual activity start | Instructions p.1 |
| Start date later than presentation date | invalid | Reject before export | Instructions p.3 |

## Quadro A — Tipo di dichiarazione

For the v0 opening path only.

| Field | Origin | v0 value / behavior | Notes |
| --- | --- | --- | --- |
| `declaration_type` | `DETERMINISTIC_RULE` | `1` — inizio attività | First VAT position / new activity |
| `start_date` | `USER_INPUT` | Required, explicit confirmation | Must be <= presentation date; filing window checked separately |
| VAT number | `NOT_APPLICABLE` | Blank | Not assigned yet on first opening |
| variation / cessation fields | `NOT_APPLICABLE` | Blank | Different workflow |

The product must explain that `start_date` is a legal/factual date, not a date chosen by the AI to optimize the filing.

## Quadro B — Soggetto d'imposta

### Identity

| Field | Origin | v0 behavior |
| --- | --- | --- |
| Ditta / cognome e nome | `USER_INPUT` / `DERIVED` | Use confirmed legal identity; do not abbreviate |
| Non-resident foreign address | `NOT_APPLICABLE` | Blank for the supported Italian-resident path |
| Foreign VAT identification number | `NOT_APPLICABLE` | Blank |

### Prevalent activity and place of business

| Field | Origin | v0 behavior | Source note |
| --- | --- | --- | --- |
| Activity code | `DERIVED` after confirmation | ATECO current at submission; v0 target is ATECO 2025 `62.10.00` | Instructions p.3 requires classification current at filing |
| Activity description | `DERIVED` | Official description corresponding to the confirmed code | Instructions p.4 |
| Presumed turnover | `DETERMINISTIC_RULE` | **Blank** when the taxpayer intends to use regime forfettario | Instructions pp.4–5 |
| Art. 60-bis intra-EU goods checkbox | `CONDITIONAL` | Ask only if facts can make it relevant; do not conflate with VIES | Instructions p.4 |
| Studio / activity address | `USER_INPUT` | Required confirmation; never assume it equals residence | Instructions p.4 |
| "Scritture contabili" checkbox | `CONDITIONAL` | Requires explicit storage-place fact; exact v0 UX still to specify | Instructions p.4 |
| Regime fiscale agevolato | `DETERMINISTIC_RULE` after eligibility + user intent | Value `2` for regime forfettario | Instructions p.4 |

### Electronic commerce

The section is filled only if the subject **exercises electronic commerce**. Having a website, GitHub profile, portfolio, or remote software-development business is not by itself a reason to fill it.

For v0:

- explicit `does_ecommerce = false` -> `NOT_APPLICABLE`;
- true / ambiguous -> collect the required facts or return `PROFESSIONAL_REVIEW_REQUIRED` until that path is specified.

## Quadro C — Titolare

| Field | Origin | v0 behavior |
| --- | --- | --- |
| Fiscal code | `USER_INPUT` / validated | Required |
| Surname / given name | `USER_INPUT` | Required in profile; form may omit duplicate names where permitted, but internal model keeps them |
| Date of birth | `USER_INPUT` | Required |
| Municipality / foreign state of birth | `USER_INPUT` | Required |
| Province of birth | `USER_INPUT` / conditional | Required where applicable |
| Residence / fiscal domicile address | `USER_INPUT` | Required |
| CAP / municipality / province | `USER_INPUT` | Required |
| "Scritture contabili" checkbox | `CONDITIONAL` | Based on where records are actually kept |

For an Italian resident person, the instructions state that fiscal domicile is in the municipality of anagraphic residence, subject to the special art. 59 exception. v0 must explicitly ask whether a different fiscal domicile has been established by the tax administration; if yes, escalate rather than silently copying residence.

## Quadri D, E, F, G, H — v0 boundary

These are **not globally irrelevant**. They are blank only because the first supported archetype proves their triggering facts absent.

| Quadro | Trigger examples | v0 behavior |
| --- | --- | --- |
| D — representative | representative different from taxpayer, heir, insolvency/judicial roles, fiscal representative | `UNSUPPORTED` / review |
| E — extraordinary operations | business acquisition/donation, succession, lease of business, transformations | `UNSUPPORTED` / review |
| F — accounting records | external depositary / additional record-storage places / foreign electronic invoice storage | v0 supports only simple self-held case; otherwise review |
| G — other activities / locations | multiple VAT-relevant activities or additional places | `UNSUPPORTED` initially |
| H — presumption of transfer / representation relationship | special goods representation relationship | `UNSUPPORTED` |

This boundary should become deterministic onboarding gates, not hidden assumptions.

## Quadro I — Altre informazioni in sede di inizio attività

**Important:** Quadro I is part of the opening workflow. It is not an optional "advanced" form page merely because the taxpayer is a simple professional.

The 21 December 2006 provision introduced additional information for VAT openings. The 2024 instructions dedicate Quadro I to these opening-only facts.

### Contact information

Collect explicitly:

- email address;
- telephone number;
- fax number, if any;
- website, if any and distinct from an e-commerce website already declared in Quadro B.

Do not fabricate empty-but-plausible values. The 2006 provision states that omission of these additional pieces of information is an element for audit-selection purposes rather than a separate rejection rule; the application should nevertheless request the applicable information cleanly.

### Property used for the prevalent activity

The opening packet must model:

- property title: `P` possession or `D` detention;
- cadastral type: `F` building or `T` land;
- cadastral section;
- sheet (`foglio`);
- parcel (`particella`);
- subaltern, where applicable;
- for lease / gratuitous loan: registration date, office, number, sub-number and series.

This is the largest onboarding addition discovered in the first research pass. "I work from home" does not mean these fields can be guessed from the residential address.

### Intra-EU operations / VIES

The Quadro I intra-EU field is for the intention to perform intra-Community operations for VIES inclusion.

v0 needs an explicit question such as:

> Do you expect to buy or sell goods/services in transactions that require you to operate as an intra-EU VAT subject?

The legal wording and UX of that question still require review before implementation. If applicable, expected acquisition/supply amounts are user estimates.

Do **not** reuse the Quadro B art. 60-bis goods checkbox for VIES: the instructions explicitly distinguish them.

### Client type / public place / initial investments

These three activity-specific fields apply only to the activity codes identified by the 21 December 2006 provision as amended on 14 January 2008.

The 2008 ATECO 2007 list is:

- `46.49.90`
- `46.76.90`
- `46.90.00`
- `47.59.99`
- `47.78.99`
- `63.99.00`
- `74.90.99`
- `82.99.99`

ATECO 2025 `62.10.00` corresponds to the prior programming code `62.01.00`, not to one of those special activity codes. Therefore **these three fields are not applicable to the v0 programming path**.

This conclusion should be encoded by a source-backed classification rule, not by an LLM.

## Attachments

The form has an attachments section for documents requested by the office / presented to substantiate facts.

Do not hardcode "no attachments" globally. For the supported direct simple opening path, the app should create a checklist based on submission channel and facts. Postal submission, for example, requires a copy of the declarant's identity document according to the instructions.

## Signature / declaration completion

The application may prepare the document but **must not manufacture the taxpayer's signature**.

Derived fields:

- list of completed quadri;
- total page count;
- fiscal code of signer from confirmed taxpayer profile.

User action:

- review packet;
- confirm declaration data;
- date/sign as required by the chosen submission channel.

Delegation and intermediary sections remain blank in the v0 direct-submission path.

## Submission channels supported by the instructions

For taxpayers not required to register with Registro delle Imprese, the instructions list:

1. direct delivery, also by delegated person, to an Agenzia delle Entrate office;
2. registered post to an Agenzia office, with identity-document copy;
3. telematic submission directly by the taxpayer or through an authorized intermediary.

The application is **not** an authorized intermediary in v0. It prepares a reviewable/exportable packet and guides the taxpayer through a legally available direct channel.

The precise current 2026 online UX/service name must be verified separately before the UI tells a user which buttons to click.

## Proposed internal field contract

Do not make `AA912Draft.fields: dict[str, str]` the long-term authoritative contract. After this research is closed, replace it with typed sections.

Each consequential field specification should carry at least:

```text
field_id
section
value_type
origin
required_when
validation
source_id
review_behavior
```

A renderer consumes only a validated `AA912Draft`; it never applies fiscal logic itself.

## P0 research still open

1. Confirm current 2026 direct electronic submission workflow and technical payload/specification for AA9/12.
2. Decide whether v0 exports only a human-signable PDF/checklist or also a telematic file compatible with Agenzia specifications.
3. Specify exact rules/UX for B/C/F `scritture contabili` in a simple forfettario professional case.
4. Specify the Quadro I VIES question so the user can answer reliably without knowing tax jargon.
5. Confirm the 2026 treatment of Quadro I property data for a professional working from their own residence, including edge cases where no separate "studio" exists.
6. Confirm Gestione Separata registration as a separate post/opening workflow; it is not an AA9/12 field.
7. Verify whether any 2025/2026 administrative update supersedes the 2024 AA9/12 instructions or the older technical submission software/specification.

Until these are resolved, implementation must expose them as incomplete research, not silently choose defaults.

## Engineering acceptance for issue #1

Issue #1 should close only when:

- every AA9/12 field that can appear in the supported opening path is typed and mapped;
- each field has an origin and source;
- unsupported triggering facts are explicit gates;
- the current submission method is documented;
- no consequential field is populated by LLM inference;
- the manual test for opening reflects all required user facts;
- a synthetic taxpayer can be deterministically transformed into a validated internal AA9/12 draft.
