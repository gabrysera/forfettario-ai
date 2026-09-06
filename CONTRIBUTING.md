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

## Delivery workflow (GitHub Flow)

Use one short-lived branch and one PR per coherent task. `main` is the integration
branch; there is no permanent `develop` branch. The agent performs the following
steps automatically when asked to implement a change.

1. Inspect `git status`, the current branch, existing PRs and repository guidance.
   Fetch `origin` and start from `origin/main`. Name the branch
   `feat/<topic>`, `fix/<topic>`, `refactor/<topic>`, `docs/<topic>` or `chore/<topic>`.
   Continue the existing branch/PR when the request is a follow-up to that task.
2. Create the branch before editing. If the checkout contains unrelated work,
   use `git worktree add -b <branch> <new-path> origin/main`. Never stash, discard,
   commit or publish unrelated changes. If the task depends on unfinished work,
   identify that dependency explicitly instead of silently including it.
3. Implement the smallest complete change. Follow the change discipline in
   `AGENTS.md`, including fiscal sources, deterministic tests and manual-test
   documentation where applicable. An issue is optional; the PR records the task.
4. Review the full diff for correctness, scope, secrets and fiscal invariants.
   Run the checks below. Record manual checks actually performed separately from
   manual-test instructions merely updated; document any unperformed checks.
5. Stage only task files, inspect the staged diff and commit with a descriptive
   message such as `fix: explain missing onboarding facts`. Push the task branch
   with `git push -u origin <branch>` and create/update its PR against `main` using
   `gh pr create` / `gh pr edit`. Use the PR template and a file for multiline bodies
   (`--body-file`). Create a draft if the work is incomplete or blocked.
6. Watch PR checks with `gh pr checks <number> --watch`. Fix failures caused by the
   change and push again. Report unrelated failures explicitly; never weaken
   checks to pass. Deliver the PR URL and actual validation results.
7. Automatically squash-merge when the task is complete, all required checks pass
   and review conversations are resolved, unless the user asks to hold the PR.
   The user has granted standing authorization: do not ask again. Do not merge
   an incomplete/draft PR just because CI passes. Deployment is a separate action.
   If `main` advanced, merge `origin/main` into the task branch and rerun checks;
   do not force-push. Never bypass protection with an admin merge.
8. After merge, verify the remote result. Fast-forward local `main` with
   `git pull --ff-only`. If it contains local changes, first verify they do not
   overlap incoming paths; otherwise leave that checkout untouched and report it.
   Never stash or discard changes to make the update succeed. Remove task branches and
   worktrees only when merged and clean. Report any retained worktree.

Authentication or network failures do not justify losing local work: finish what
can be validated locally and report the precise blocked remote step. Never claim
a PR, check or merge exists without checking GitHub.

## Validation

With Python 3.13 and the project installed via `python -m pip install -e '.[dev]'`,
run the same checks as `.github/workflows/ci.yml`:

```sh
python -m pip check
ruff format --check .
ruff check .
mypy app function_app.py
pytest -q
git diff --check
```

For documentation-only changes, local diff/link review and `git diff --check`
suffice; the full CI still runs on the PR. Application, fiscal and architecture
changes require the full checks plus relevant acceptance checks.

## GitHub enforcement

Configure branch protection for `main` to require a PR, the GitHub Actions
`quality` check, an up-to-date branch and resolved review conversations. Apply
protection to administrators too; disallow force pushes and branch deletion.
Do not require an approving reviewer in this single-maintainer repository, where
the PR author cannot approve their own PR. Merge authorization follows the
delivery procedure above.

These settings live on GitHub, not in this Markdown file. Verify them through
repository settings or `gh api repos/{owner}/{repo}/branches/main/protection`.
The existing CI supplies the checks; no additional agent runner, paid service or
local hook installation is required. `AGENTS.md` defines agent behavior; GitHub
protection enforces the merge gate independently of the agent.

## Pull request content

Explain:

1. what requirement changes;
2. which source supports any fiscal change;
3. which tests were added/updated;
4. whether any unsupported case became supported;
5. whether the change affects privacy/security.

Small, reviewable PRs are preferred.
