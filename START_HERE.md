# Start here

The repository is ready for implementation only after the following P0 decisions are resolved and encoded as requirements/tests.

## 1. Lock the first supported taxpayer archetype

Proposed v0.1 archetype:

- natural person;
- Italian tax resident;
- freelance software developer;
- ATECO 2025 62.10.00;
- regime forfettario candidate;
- Gestione Separata, no other mandatory pension coverage;
- no employees/collaborators;
- no participation/control situations that create exclusion issues;
- no complex foreign tax situation.

Anything else must initially escalate to review.

## 2. Complete the opening workflow research

Before implementing AA9/12 generation, resolve every P0 item in `docs/RESEARCH_BACKLOG.md`, then convert answers into:

- explicit FR requirements;
- deterministic validation rules;
- source registry entries;
- boundary tests;
- `MT-001` acceptance-test updates.

## 3. Define v0.1 data contracts

Create versioned schemas for:

- `TaxpayerProfile`;
- `ActivityClassification`;
- `TaxRegimeAssessment`;
- `SocialSecurityAssessment`;
- `ReviewStatus`;
- `AA912Draft`;
- `SourceReference`.

Use Zod or equivalent runtime validation.

## 4. Implement the first vertical slice

Recommended order:

1. bootstrap Next.js/TypeScript workspace;
2. implement domain schemas;
3. implement deterministic eligibility engine;
4. add synthetic golden fixtures;
5. implement onboarding UI;
6. add AI extraction behind structured schemas;
7. implement AA9/12 internal mapping;
8. run Playwright/manual acceptance tests in preview deployment.

## 5. Definition of done for v0.1

The first milestone is complete only when a synthetic supported user can go from empty account to a reviewable AA9/12 draft and the exact same result can be reproduced without using an LLM.

The LLM may improve the interaction, but removing the LLM must not change fiscal truth.
