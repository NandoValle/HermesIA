# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The marketing site for **HermesIA** (https://hermesia.ia.br) — a Brazilian AI product that delivers ready-made documents (petitions, appeals, reports) for lawyers and self-employed professionals. All content is in Brazilian Portuguese (pt-BR). Commit messages are also written in Portuguese.

It is a **pure static HTML site**: no build system, no package.json, no framework, no tests, no shared CSS/JS files. Every page is a fully self-contained HTML file with inline `<style>` blocks and/or inline `style=` attributes.

## Deployment

- Hosted on **GitHub Pages** with custom domain `hermesia.ia.br` (`CNAME` file).
- Pushing to `main` deploys automatically. There is no build or preview command — verify pages by opening the HTML files directly in a browser.
- `.nojekyll` must be kept: Jekyll processing is disabled because the Jekyll build previously failed on this repo.
- Do not delete `google490ebef767a77d31.html` (Google Search Console verification) or the `facebook-domain-verification` meta tag in `index.html` (Meta Business Manager).

## Site structure

- `index.html` — institutional homepage. Brand style: navy `#0d1b3e` + gold `#c9a84c`, Playfair Display + Inter fonts, CSS classes prefixed `hm-`. Same visual language on `obrigado.html` (thank-you page, `noindex`), `privacidade.html`, `termos.html`.
- `/<nicho>/index.html` (e.g. `aluguel/`, `multa/`, `cnh/`, `golpe-pix/`, `inss/`, ~20 dirs) — direct-response landing pages per legal/consumer niche, served at clean paths like `/multa`. These use a different template: Poppins font, navy `#16243f` + gold `#c9a227`, heavy inline styles, emoji icons, pulsing `.cta` buttons.
- `tutoriais/*.html` — SEO tutorial pages ("X com IA" per profession). These are the only pages besides the homepage listed in `sitemap.xml`.
- `audio/index.html` — product page for HermesIA Áudio (WhatsApp audio transcription), the currently live product.
- `vendas/` — installable PWA sales dashboard: `manifest.json`, minimal pass-through `sw.js` (intentionally no offline cache — the panel needs live data), and an `index.html` that reads real-time data from Supabase via the CDN `@supabase/supabase-js` client (URL and anon key are hardcoded in the page; the anon key is public by design).
- `preparo-pharma/index.html` — a business proposal page, not part of the marketing funnel.

## Conventions

- **CTAs go to WhatsApp**, not forms: links to `wa.me/553172285422` or `api.whatsapp.com/send/?phone=553172285422` with a URL-encoded pre-filled pt-BR message tailored to the page's niche. Keep that phone number and the pre-filled-message pattern when adding or editing CTAs.
- **Meta Pixel calls are guarded no-ops**: CTA links carry `onclick="typeof fbq==='function'&&fbq('track','Lead');"` but no pixel script is currently loaded anywhere. Preserve the guard pattern; don't add an unguarded `fbq` call or assume the pixel exists.
- **Full SEO head on every public page**: title, meta description, canonical URL, Open Graph (`og:locale` `pt_BR`, `og:image` → `/og-image.png`), Twitter card. `index.html` additionally carries Organization JSON-LD structured data.
- **Sitemap discipline**: when adding a page meant to be indexed, add it to `sitemap.xml` with a `lastmod` date; landing-page niches (`/aluguel`, `/multa`, …) are currently *not* in the sitemap — they are ad-traffic pages.
- Fonts and icons come from CDNs (Google Fonts, Tabler icons webfont, jsDelivr). No assets are bundled locally except images (`emblema.png`, `og-image.png`, `fundador.png`) and `video-hermesia.mp4`.
- New pages should follow the existing pattern: one self-contained HTML file, `lang="pt-BR"`, inline styles, mobile-first with a `@media(max-width:600px)` breakpoint where needed.
