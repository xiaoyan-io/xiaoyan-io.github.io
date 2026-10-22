# ALAN Hexo + Anzhiyu preview

Work only on `feature/anzhiyu-preview`. Root static production files and workflows are preserved.

## Build

Node.js 22 LTS is the documented CI runtime. From `hexo-source`:

```powershell
npm ci --registry=https://registry.npmjs.org/
npm run build
```

Optional recovery validation (Python 3 and BeautifulSoup4 required):

```powershell
python validation/validate-recovery.py
```

The validator compares generated article bodies, code blocks, titles, dates, taxonomy, anchors and local links against the retained root HTML and verifies the downloadable script byte for byte. It exits nonzero on failure. See `RECOVERY_MANIFEST.json`, `RECOVERY_VALIDATION.json` and `RECOVERY_REPORT.md`.

Only two genuine articles are indexed. Two dated Hexo examples and the empty legacy PVE page remain at their historical URLs as pages. The undated initial template is removed. Markdown is reconstructed from published HTML, not recovered original Markdown.

The existing preview workflow uploads `anzhiyu-preview-static-site`; it does not deploy a website. Never run `npm run deploy`, trigger the production workflow or change main, Secrets or production settings for this recovery.
