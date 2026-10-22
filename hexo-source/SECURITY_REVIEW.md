# Dependency security review (2026-10-22)

Scope: isolated Hexo 8.1.2 / Anzhiyu build on `feature/anzhiyu-preview` only. This report is not a production security approval.

## Verified scan

From `hexo-source/`, using the official registry for the audit endpoint:

```sh
npm audit --registry=https://registry.npmjs.org/
npm audit fix --dry-run --registry=https://registry.npmjs.org/
```

Result: **9 findings (7 high, 2 moderate)**. Affected packages reported: `braces`, `chokidar`, `hexo`, `hexo-cli`, `hexo-fs`, `hexo-i18n`, `micromatch`, `nunjucks`, and `sprintf-js`.

Two transitive advisories:
- `braces <=3.0.3`: GHSA-vfj7-8cjw-p6xm (stack exhaustion). Latest published version returned by the registry during this scan: 3.0.3.
- `sprintf-js <=1.1.3`: GHSA-hp3w-g68c-fv3c (denial of service). Latest published version returned during this scan: 1.1.3.

`npm audit fix --dry-run` changed no packages and left all 9 findings. Its suggested forced fix involves `hexo@3.9.0`, which is a major downgrade from the verified Hexo 8.1.2 build and was **not applied**.

## Risk boundaries and next actions

The current workflow generates static HTML and uploads a build artifact; it does not expose `hexo server` publicly. Vulnerable Node dependencies still affect the build environment and should not be dismissed. Avoid processing untrusted posts/templates in this build, maintain locked dependency installs, and review updated upstream Hexo dependency releases and fixes before production cutover.

No package updates, overrides, registry settings, or production permissions were changed during this review. An audit finding is not considered remediated until a subsequent official audit verifies the result. Preview-only UI cleanup and historical content validation are independent of this unresolved security finding.
