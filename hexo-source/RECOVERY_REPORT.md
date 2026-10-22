# Content recovery evidence — 2026-10-22 (Asia/Rangoon)

## Scope and baseline

Verified checkout: `H:/ALAN_MM_AI_V1_ISOLATED/PROJECTS/05_PROJECTS/ALAN_HEXO_GITHUB_PREVIEW`. Initial checkout clean; branch `feature/anzhiyu-preview`, head `e86013fed263bcba371da9e12fac741a5a9cb55b`. GitHub-connected tree and branch inspection confirmed this head. Original article HTML and files are identical to production main commit `3956562057d8c53dbe8fa2febbf60f71bb34c79a` (scoped Git comparison). This is a production-repository HTML comparison, not proof of live hosting state. Recursive inventory excluded Git internals, dependencies, themes and archive listings from active article ranking; archive provenance remains untouched. Original source timestamps are checkout timestamps, not approval dates. SHA-256 provenance is in the manifest.

## Recovered material

- PVE9 upgrade article: original URL, UTC instants, Proxmox/PVE9 category hierarchy, four tags and three code blocks retained.
- Alan Cloud Agent Hub: original URL, publication date, Alan category, five tags and 21 code blocks retained. No separate updated timestamp was available; front matter uses publication time rather than current recovery time.
- Two Hello World pages are duplicate Hexo examples, not genuine authored articles. Both dated URLs and four code blocks each are retained outside the article index.
- `pve9-upgrade-kit-1` has no body; retained as an empty legacy page, without invented content or redirect.
- No article-body images were present in the five HTML inputs. All 32 code blocks match exactly. Whitespace-normalized body text matches after excluding the added functional download anchor.
- `/files/pve9-upgrade-kit.sh` is copied unchanged into source/files and skip_render protects its bytes. SHA-256: `cb532b866ce69b7c3bd59a971e5981d0fe4bfc281a397e99ced052126f9cabff`.
- An actual download link is added beside the original HTML code example, which was not a clickable button in the old site.
- Historical heading anchors survive Markdown reconstruction; disableNunjucks prevents literal article template markers from executing. Checked lists and details remain.
- Hexo URL uses the original canonical GitHub site and timezone Asia/Yangon preserves the observed +06:30 display dates. These are preview source configuration changes, not hosting settings.
- Tags/categories index pages repair generated navigation. Preview-only overrides disable sample homepage categories and the absent donation page. Vendored theme files remain unchanged.

## Verification and limits

Documented npm ci completed (276 packages). npm run build passed locally under Node 25.9.0; Node 22 CI remains a separate check. No repository test script exists. Python recovery validation PASS: 5 URLs, 32 exact code blocks, titles, article timestamps, category/tag membership, original anchors, body links, script bytes and generated site local href/src paths. Example/empty page dates are retained in front matter; the theme page layout does not display timestamps. External URLs, remote CDN assets and browser interaction have not been validated. Original domain placeholder `https://你的域名/` and incomplete inline installer sample are intentionally retained and unresolved; the full downloadable file is preserved, not substituted for the published sample. Recovered prose is historical content, not a validation of engineering claims or safe script execution; the script was never executed.

npm audit reported 9 dependency vulnerabilities (2 moderate, 7 high); no dependency upgrades or lockfile changes made. These are a known preview limitation, not an installation/build failure.

## Reversibility and delivery

All source changes are under hexo-source. Root static HTML/assets, main, workflows, Secrets and production settings remain unchanged. Git parent e86013f is the exact rollback baseline; only explicit source files are eligible for the recovery commit. Build output and dependencies are ignored. Preview workflow can upload an artifact on a feature-branch push; no production deployment is requested. Final remote commit, CI and artifact evidence are reported separately after publication to the feature branch.
