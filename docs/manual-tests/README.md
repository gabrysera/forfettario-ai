# Manual acceptance tests

These tests are written so a human or browser-capable coding agent can execute them against a preview deployment.

Each behavior-changing PR must update the relevant manual test.

A test should contain:

- requirement IDs;
- preconditions;
- synthetic test data only;
- exact steps;
- expected deterministic results;
- evidence to capture;
- unsupported/error-path expectations.

Manual tests complement, not replace, automated unit/integration/golden tests.
