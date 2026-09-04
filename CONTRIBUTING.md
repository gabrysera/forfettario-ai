# Contributing

Contributions are welcome, including AI-assisted contributions.

Before changing behavior, read `AGENTS.md`, `docs/PRODUCT.md`, `docs/FUNCTIONAL_REQUIREMENTS.md`, the relevant source registry and manual tests.

## Rules

- Keep fiscal logic deterministic and outside prompts/UI.
- Cite authoritative sources for fiscal changes.
- Add/update automated tests for fiscal behavior.
- Update manual acceptance tests for user-visible workflow changes.
- Use synthetic data only in tests and screenshots.
- Unsupported cases must fail closed.

## Pull requests

Explain:

1. what requirement changes;
2. which source supports any fiscal change;
3. which tests were added/updated;
4. whether any unsupported case became supported;
5. whether the change affects privacy/security.

Small, reviewable PRs are preferred.
