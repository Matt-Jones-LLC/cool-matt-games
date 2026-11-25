# AWS deployment preparation

The hosting stack and migration runbook live in [Matt-Jones-LLC/matt-jones.org](https://github.com/Matt-Jones-LLC/matt-jones.org), on branch `codex/aws-migration-review`, at `infra/sites.cloudformation.json` and `docs/aws-migration.md`.

This repository owns only its own `infra/site.json`, public asset packager, deploy script and gated AWS workflow. The workflow is disabled until `AWS_DEPLOY_ENABLED=true` and the site-specific bucket, distribution ID and OIDC role variables are configured. Existing Pages deployment is retained during validation. No DNS change is made by these files.

Run `node scripts/package-aws.cjs` and `bash -n scripts/deploy-aws.sh` before release. Review the `_aws_site/` artifact, including the homepage, game routes, assets and 404 page. Never upload the entire repository root.

Workflow activation: `infra/aws-workflow.yml` is a template. Copy it to `.github/workflows/aws.yml` through an account authorized to write workflows before expecting any AWS deployments. The current CLI token lacks that scope; no workflow permission was broadened.

Domain setup: `coolmatt.games` is canonical. `www.coolmatt.games`, `coolmattgames.io` and `www.coolmattgames.io` share this distribution and redirect to the canonical hostname, preserving paths and query values. The us-east-1 ACM certificate must cover all four names. No separate lab bucket, deployment role or monitor is created. Preserve existing Pages deployments until DNS validation and rollback windows have passed.

The company uses mattjonesllc.com with matt-jones.org as an alias. Flash Is Dead is the future third site, with no repo or resources yet. All three share a $50/month allowance: up to $30 AWS and $20 additional Datadog. Usage alerts are not hard caps; verify projected costs before activation.
