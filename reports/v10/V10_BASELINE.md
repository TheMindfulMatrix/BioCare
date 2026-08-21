# V10 baseline

- BioCare production baseline: `f205890e5e5635d87d6ff77da97eedc96d365041`
- Baseline branch: `main`
- V10 branch: `agent/v10-evidence-library`
- Private source baseline: `de8c7711a5ca4678d92dd0d0a3ebeba06f7334c7`
- Baseline verified: 2026-08-21
- V5.1 rollback tag: `b5d35772e98580e253c08f6319aa8e412fa20aea`

The production baseline was verified directly from `origin/main` before the V10 branch was created. The BioCare starting tree and private source checkout were clean. The private source was audited read-only; it remained unchanged after the audit. No production branch, tag, or deployment was modified.

Baseline website facts: 22 generated public pages, 45 active products, 8 deferred products, 10 published Library guides, passing deterministic build, passing compliance hard gate, and passing V8/V9 fixtures.
