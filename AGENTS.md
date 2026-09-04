# AGENTS.md

This file is authoritative for AI coding agents working in this repository.

## Product invariants

1. **Never implement fiscal rules inside UI components or prompts.**
2. **Never use an LLM to perform authoritative tax arithmetic.**
3. **Never silently infer missing fiscal facts.** Missing material information must produce an explicit question or `NEEDS_REVIEW`.
4. **Fail closed.** Unsupported or ambiguous situations must not be forced through the happy path.
5. **Every fiscal rule must be versioned by jurisdiction and applicable period.**
6. **Every fiscal rule must cite a primary or authoritative source.**
7. **Every fiscal rule change must add/update automated tests.**
8. **Every user-visible workflow change must update the corresponding manual test.**
9. **Never mix issued invoices with collected income.** The domain must separately represent documents, payments and tax-relevant cash events.
10. **No user-facing number may be presented as final/authoritative unless the engine can explain how it was derived.**

## Required change discipline

Before implementing a feature:

- read `docs/PRODUCT.md`;
- read `docs/FUNCTIONAL_REQUIREMENTS.md`;
- read relevant files in `rules/`;
- read relevant manual tests;
- identify whether the change affects a fiscal invariant.

A PR that changes behavior must update, where applicable:

- `docs/FUNCTIONAL_REQUIREMENTS.md`;
- `docs/DOMAIN_MODEL.md`;
- one or more `docs/manual-tests/*.md`;
- deterministic tests;
- `rules/.../sources.md` if fiscal logic changed;
- an ADR if an architectural boundary changed.

## AI boundary

Allowed LLM responsibilities:

- conversational onboarding;
- extracting structured facts from user text/documents;
- explaining deterministic engine outputs;
- classifying whether a workflow/tool should be invoked;
- identifying missing information;
- summarizing authoritative sources already provided to the system.

Disallowed LLM responsibilities:

- deciding tax rates from memory;
- computing taxes instead of calling the engine;
- inventing deadlines, codes, thresholds or form values;
- deciding an ambiguous legal/fiscal classification without deterministic validation;
- claiming a filing/payment was completed when it was not.

## Review states

Use this conceptual contract consistently:

```ts
export type ReviewStatus =
  | 'AUTO_VALIDATED'
  | 'USER_CONFIRMATION_REQUIRED'
  | 'PROFESSIONAL_REVIEW_REQUIRED'
  | 'UNSUPPORTED';
```

## Testing

Prefer pure functions for fiscal calculations.

Minimum for a rule change:

- unit test for the rule;
- boundary tests around thresholds/dates;
- at least one golden fixture if end-user output changes;
- manual test update if the UI/workflow changes.

Never weaken or delete a failing fiscal test merely to make CI green unless the requirement/source changed and the PR documents why.

## Security and privacy

Assume all tax profiles, invoices, fiscal codes, addresses and financial information are sensitive.

- no secrets in source control;
- no production personal data in fixtures;
- fixtures must use synthetic identities;
- redact logs by default;
- minimize data sent to LLM providers;
- do not send unnecessary identity fields to the model.
