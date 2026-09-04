# Security policy

This project handles potentially sensitive tax, identity and financial information.

## Until production readiness

Do not use real taxpayer data in tests, public issues, screenshots or fixtures.

## Principles

- data minimization;
- secrets never committed;
- redacted logs by default;
- least-privilege access;
- encryption in transit and at rest where supported;
- minimize identity/financial data sent to LLM providers;
- keep deterministic fiscal state separate from conversational transcripts;
- auditable consequential actions.

## Before production

The project must define authentication, authorization, retention/deletion, backup/restore, incident response, GDPR roles/lawful basis/subprocessors, provider data-processing settings and a threat model.

Security vulnerabilities should not be disclosed in public issues if they expose an exploitable weakness or sensitive data.
