# AA9/12 opening — supported v0 path

This document is the source-of-truth mapping for the first AA9/12 vertical slice.

It covers only a narrow case:

- Italian resident natural person;
- autonomous professional / software developer;
- one prevalent activity;
- ATECO 2025 `62.10.00`;
- regime forfettario selected through the supported deterministic path;
- activity records kept at the activity address;
- no representative, extraordinary operation, foreign permanent establishment, additional activity or additional place of business.

Anything outside this path must fail closed or be routed to review. The renderer must never infer missing facts.

## Authoritative sources

Primary references:

1. Agenzia delle Entrate — official AA9/12 model:
   `https://www.agenziaentrate.gov.it/portale/documents/d/guest/modello-aa9_aa9_12-modello-pdf`
2. Agenzia delle Entrate — AA9/12 instructions:
   `https://www1.agenziaentrate.gov.it/modulistica/altri/aa9istrc_new.pdf`
3. Agenzia delle Entrate — 4 June 2015 compilation/control-software notice, referring to technical specifications approved with provvedimento 75295/2015:
   `https://telematici.agenziaentrate.gov.it/Main/Avviso?id=20150604120456`
4. Agenzia delle Entrate — 21 December 2006 / 14 January 2008 provisions defining the restricted activity list for the special Quadro I fields.
5. ISTAT — ATECO 2007 and ATECO 2025 classifications used to prove that software programming is outside that restricted activity list.

The exact PDF bytes supported by the renderer are additionally pinned by SHA-256 in `app/documents/aa912/template.py`.

## Mapping contract

`Origin` has the following meanings:

- **user** — the application must collect/confirm the fact;
- **derived** — directly derived from confirmed user facts without fiscal judgement;
- **deterministic** — fixed by the supported product path and source-backed mapping;
- **conditional** — required only when the stated condition is true;
- **unsupported** — the v0 app must refuse to produce a completed output for that case.

| User concept | AA9/12 target | Origin | v0 requiredness / rule |
| --- | --- | --- | --- |
| declaration type | Quadro A, inizio attività | deterministic | always `inizio attività` |
| start date | Quadro A | user | required |
| taxpayer fiscal code | page headers + Quadro C + signer CF | user | required; formal checksum validated |
| surname / given name | Quadro B/C | user | required |
| birth date / municipality / province | Quadro C | user | required |
| residence | Quadro C | user | required |
| prevalent activity | Quadro B | deterministic | software programming only in v0 |
| ATECO | Quadro B | deterministic | `62.10.00` only in v0; cannot be supplied by browser |
| activity description | Quadro B | deterministic | canonical supported description |
| activity address | Quadro B | user/derived | residence when user confirms home-based work; otherwise explicit address required |
| accounting-records checkbox | Quadro B/C | user + scope gate | v0 supports records kept at the activity address only; any other location fails closed |
| fiscal regime | Quadro B | deterministic | AA9/12 code `2` for the supported forfettario path; browser cannot override it |
| email | Quadro I | user | required by the v0 product flow; the instructions request contact information; this is not a claim that email is independently a telematic blocking field |
| telephone | Quadro I | user | required by the v0 product flow; prefix and number are collected separately to match the model geometry |
| fax | Quadro I | user | optional in v0; if supplied, prefix and number must both be present |
| website | Quadro I | user | optional |
| activity-property tenure | Quadro I | user | required for the activity property; `P` possession or `D` detention |
| cadastral type | Quadro I | user | required; `F` building or `T` land |
| cadastral section | Quadro I | user | optional when not applicable |
| cadastral sheet | Quadro I | user | required in the supported path |
| cadastral parcel | Quadro I | user | required in the supported path |
| cadastral subunit | Quadro I | user | optional when not applicable |
| contract registration details | Quadro I | user | conditional: required for `D` detention; date, office and number required; subnumber/series optional when absent |
| VIES intent | Quadro I | user | user explicitly chooses whether to request inclusion for intra-EU operations |
| expected intra-EU purchases/sales | Quadro I | user | conditional on VIES request; both values collected as whole euro amounts and may be zero |
| special client/public-place/investment fields | Quadro I | not applicable | not populated for this software-developer path; the official 2008 replacement list does not include software programming |
| compiled sections | signature summary | deterministic | `A`, `B`, `C`, `I` for this path |
| total declaration pages | signature summary | deterministic | `4`; physical PDF page 1 is the privacy notice, declaration pages are numbered 1–4 |
| declaration date | signature summary | user | optional while drafting; if supplied it cannot precede the declared start date |
| signature | signature summary | user only | **never generated by software** |
| representative / delegate / intermediary | other sections | unsupported | not supported by this v0 path |

## Quadro I interpretation

The official instructions state that Quadro I is used at initial registration, request contact information, and require data for the property used for the prevalent activity, including cadastral data. They define `P` as possession and `D` as detention (lease/loan); for detention, contract-registration details are requested.

The same instructions state that the intra-EU field is used by taxpayers who want to express the intention to carry out intra-EU operations for VIES inclusion.

### Why the special activity fields are not asked

The additional Quadro I fields for prevalent customer type, place open to the public and initial investments are explicitly restricted to activities identified by the 21 December 2006 provision as updated for ATECO 2007 by the 14 January 2008 provision.

The 2008 replacement list is:

- `46.49.90`
- `46.76.90`
- `46.90.00`
- `47.59.99`
- `47.78.99`
- `63.99.00`
- `74.90.99`
- `82.99.99`

Software programming was classified as `62.01.00` under ATECO 2007 and is `62.10.00` under ATECO 2025. It is therefore outside the restricted list. For the supported software-programming path, the customer-type/public-place/initial-investment fields stay blank and are not shown in onboarding.

This conclusion is part of the supported-archetype contract, not a generic rule that those fields are always optional for every taxpayer.

## Accounting-record location boundary

The `SCRITTURE CONTABILI` checkbox is tied to the address shown in the relevant AA9/12 section. The official instructions also provide Quadro F for depositaries and other places where accounting records are kept.

For that reason, v0 supports only records kept at the activity address. If the user says the documentation is stored elsewhere, the application does not improvise a second address or silently omit Quadro F: it fails closed and requires a more complete path.

## Template contract

The official PDF is not an AcroForm. Rendering therefore uses the official bytes as an immutable background and overlays values at version-specific coordinates.

Rendering is allowed only when all of the following match the template profile:

- exact SHA-256;
- exact page count;
- expected page geometry.

A new Agenzia PDF, even if it still has five pages, must be treated as unsupported until its layout is reviewed and a new explicit profile/layout is added.

Raw coordinates live only in `layout.py`. Fiscal/form decisions live only in `mapping.py`. `renderer.py` may format and draw a draft but must not decide which fiscal value should be used.

## Output status

The generated file is a **document to review and sign**, not evidence of submission.

The application must not claim that a VAT number has been opened until an Agenzia receipt confirms successful presentation. Automatic telematic-file generation/submission is outside this vertical slice.

## Known boundary

Current v0 asks for email and telephone as product-required inputs because the official instructions ask for those contact details. The project has not yet encoded a claim that each contact item is an independent blocking field in the current Agenzia telematic-control software. That distinction must remain explicit if/when automatic telematic submission is implemented.
