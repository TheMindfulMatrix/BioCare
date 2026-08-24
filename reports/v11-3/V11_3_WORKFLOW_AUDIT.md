# V11.3 Workflow Audit

## Confirmed change

GitHub now documents an optional IANA `timezone` property on scheduled workflow events. The daily audit therefore uses one `0 8 * * *` schedule with `timezone: America/Chicago`, replacing the two UTC triggers and hour guard while retaining DST correctness and `workflow_dispatch`.

Scheduled runs continue to execute from the default branch. Checkout retains `persist-credentials: false`. Permissions remain `contents: read` and `actions: write`, the latter being required for the audit artifact.

## Action runtime modernization

All repository workflow references were updated to official Node 24 action majors:

- `actions/checkout@v6`
- `actions/setup-python@v6`
- `actions/upload-artifact@v6`

GitHub-hosted runners exceed the documented minimum runner version for these releases. No unofficial actions, secrets, or expanded permissions were introduced.

## Authoritative references

- GitHub schedule documentation: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule
- Checkout: https://github.com/actions/checkout
- Setup Python: https://github.com/actions/setup-python
- Upload Artifact: https://github.com/actions/upload-artifact/releases

## Expected operational result

One audit workflow run per local day at 8:00 AM America/Chicago, plus explicit manual reruns. The prior second skipped daily run is eliminated.
