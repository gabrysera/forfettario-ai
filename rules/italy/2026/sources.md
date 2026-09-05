# Italy 2026 — authoritative source registry

This file is a registry, not an implementation of all rules. Fiscal constants and document mappings must point back to the primary material recorded here or to a more specific rule document.

## Activity classification

- ISTAT, ATECO 2025 explanatory notes — `62.10.00 Attività di programmazione informatica`
  - https://www.istat.it/wp-content/uploads/2025/03/Note-esplicative-ATECO-2025-italiano.pdf

## Regime forfettario — access and startup rate

- Law 23 December 2014 no. 190, art. 1, current text, especially commi 54, 57, 64, 65 and 71.
  - https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2014;190
- Law 30 December 2024 no. 207, art. 1, comma 12 — raises the employment-income threshold referenced by comma 57(d-ter) to EUR 35,000 for 2025 and 2026.
  - https://www.normattiva.it/eli/id/2024/12/31/24G00229/ORIGINAL
- Law 29 December 2022 no. 197, art. 1, comma 54 — EUR 85,000 access threshold and EUR 100,000 immediate-exit rule.
  - https://www.normattiva.it/eli/id/2022/12/29/22G00211/ORIGINAL
- Agenzia delle Entrate — REDDITI PF 2026, Quadro LM guidance.
  - https://infoprecompilata.agenziaentrate.gov.it/portale/quadro-lm

See `forfettario.md` for stable rule IDs and exact v0 interpretations.

## Gestione Separata

- INPS Circular no. 8, 3 February 2026 — contribution rates for 2026.
  - https://www.inps.it/it/it/inps-comunica/atti/circolari-messaggi-e-normativa/dettaglio.circolari-e-messaggi.2026.02.circolare-numero-8-del-03-02-2026_15153.html

## AA9/12 opening document

Reviewed for the v0 opening slice on 2026-09-05.

### Official model

- Agenzia delle Entrate — official AA9/12 model for individual businesses and self-employed workers.
  - https://www.agenziaentrate.gov.it/portale/documents/d/guest/modello-aa9_aa9_12-modello-pdf
  - supported PDF SHA-256: `a75a7ddab209b5355dc0ab40f78e6ba27d43806140ab60de1f9c8857dc32c599`
  - renderer contract: five A4 pages with the exact fingerprint and expected geometry recorded in `app/documents/aa912/template.py`.
  - interpretation: the PDF is treated as an immutable official background; any changed fingerprint is unsupported until deliberately reviewed and versioned.

### Official instructions

- Agenzia delle Entrate — AA9/12 instructions for starting, changing or ceasing individual VAT activity.
  - https://www1.agenziaentrate.gov.it/modulistica/altri/aa9istrc_new.pdf
  - interpretation used by v0:
    - the model is used by individual businesses and self-employed workers for start/change/cessation declarations;
    - all declaration pages carry the taxpayer fiscal code and progressive page number;
    - Quadro I is used on initial registration for contact information and data about the property used for the prevalent activity;
    - property tenure code `P` means possession and `D` means detention (lease/loan); detention requires contract-registration details;
    - the intra-EU field expresses the intention to carry out intra-EU operations for VIES inclusion;
    - the client-type/public-place/initial-investment fields are restricted to the activity codes identified by the cited 2006/2008 provisions and are not populated merely because they exist on the generic form;
    - the declaration must be signed by the taxpayer or legal/negotiated representative. The v0 software never generates a signature.

### Compilation/control-software notice

- Agenzia delle Entrate, 4 June 2015 — AA9/12 compilation and control software aligned with technical specifications approved by provvedimento no. 75295/2015.
  - https://telematici.agenziaentrate.gov.it/Main/Avviso?id=20150604120456
  - interpretation used by v0: the forfettario selection is supported by the official AA9/12 compilation path and, when selected, volume of business is not entered in that field set.

The field-by-field supported mapping is documented in `docs/AA912_OPENING.md`.

## Stamp duty on electronic invoices

- Agenzia delle Entrate — guidance on stamp duty for electronic invoices.
  - https://www1.agenziaentrate.gov.it/web_app_entrate/bollo_fatture.html

## Rule-source requirements

Before a fiscal constant is added to code, store:

- source URL/document identifier;
- source title;
- publication/effective date where relevant;
- applicable tax period;
- exact rule interpretation;
- test cases including boundary values;
- reviewer/date.
