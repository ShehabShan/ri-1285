# Enable automatic checks
The GitHub integration used for this hardening cannot publish `.github/workflows`
changes (API reports Resource not accessible by integration). This template was
therefore not installed and no remote CI result is claimed.

An authorized repository maintainer can copy `production-contracts.yml` to
`.github/workflows/production-contracts.yml`, commit it through an account/app with
workflow-write permission, then require the `contracts` check in branch protection.
Until then run the validator/tests locally before each handoff. This file is a
template only; storing YAML under docs does not enable GitHub Actions.
