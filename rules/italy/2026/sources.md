# Italy 2026 — authoritative source registry

This file is a registry, not yet an implementation of all rules.

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

## AA9/12

- Agenzia delle Entrate — AA9/12 instructions / starting, changing or ceasing individual VAT activity.
  - https://www1.agenziaentrate.gov.it/modulistica/altri/aa9istrc_new.pdf

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
