# ALAN Hexo + Anzhiyu

Independent Hexo source project. The existing public GitHub Pages repository is preserved.

## Local build

```powershell
npm ci --registry=https://registry.npmjs.org/
npm run build
```

Cloudflare Pages: build command `npm run build`, output directory `public`, Node.js 22 LTS recommended. Preview deployment before production cutover.

Historical content has not yet been migrated. Do not treat generated HTML in the existing public repository as original Markdown source.
