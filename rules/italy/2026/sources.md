# Italy 2026 — authoritative source registry

This file is a registry, not yet an implementation of all rules.

## Activity classification

- ISTAT, ATECO 2025 explanatory notes — `62.10.00 Attività di programmazione informatica`.
  - https://www.istat.it/wp-content/uploads/2025/03/Note-esplicative-ATECO-2025-italiano.pdf
- ISTAT, ATECO technical documentation and 2025 ↔ 2022 correspondence tables, updated 15 July 2026.
  - https://www.istat.it/classificazione/documenti-ateco/
  - Relevant v0 correspondence: ATECO 2025 `62.10.00` ↔ ATECO 2022 `62.01.00`.

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

## AA9/12

- Agenzia delle Entrate — AA9/12 model, declaration of start/change/cessation for individual businesses and self-employed workers.
  - Obtain from the official Agenzia delle Entrate forms area and preserve the reviewed revision metadata in research notes.
- Agenzia delle Entrate — AA9/12 instructions, 2024 revision reviewed for the v0 field map.
  - https://www1.agenziaentrate.gov.it/modulistica/altri/aa9istrc_new.pdf
- Agenzia delle Entrate, Provvedimento 21 December 2006 — additional information required at VAT opening under art. 35(15-ter), published in G.U. Serie Generale n. 3 of 4 January 2007.
  - https://www.gazzettaufficiale.it/eli/id/2007/01/04/06A11920/sg
  - Relevant rules: opening contact details, property/cadastral facts, lease/loan registration facts, expected intra-EU amounts, and activity-specific risk information.
- Agenzia delle Entrate, Provvedimento 14 January 2008 — updates the ATECO 2007 activity-code list for activity-specific opening information.
  - Relevant listed codes: `46.49.90`, `46.76.90`, `46.90.00`, `47.59.99`, `47.78.99`, `63.99.00`, `74.90.99`, `82.99.99`.
  - Preserve a primary-source/publication reference before converting the list into executable fiscal configuration.

Research interpretation lives in `docs/research/AA912_OPENING_2026.md`; executable code must not cite that research note in place of the underlying sources.

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
