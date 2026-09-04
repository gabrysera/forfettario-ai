# Golden fiscal fixtures

Golden fixtures represent complete synthetic taxpayer scenarios with expected deterministic outputs.

They are regression contracts, not examples for the LLM.

Each fixture should include:

- ruleset version;
- synthetic input facts;
- expected eligibility condition results;
- expected review status;
- expected calculation components where applicable;
- expected document-field mappings where applicable;
- source references used by the rules.

When a rule legitimately changes, update the fixture in the same PR and document the source that caused the change.
