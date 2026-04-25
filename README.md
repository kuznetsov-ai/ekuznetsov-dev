# ekuznetsov.dev

Personal site of **Evgenii Kuznetsov** — AI Engineer, Cyprus.

**Live:** [https://ekuznetsov.dev](https://ekuznetsov.dev)

## Tech Stack

Static site, plain HTML + CSS + JavaScript — no framework, no build step.

| File | Purpose |
|------|---------|
| `index.html` | Main page (RU + EN via in-page i18n dictionary) |
| `en/index.html` | Legacy stub — redirects to `/?lang=en` |
| `styles.css` | Dark theme, gradients, animations, responsive layout |
| `script.js` | Scroll reveal, 3D card tilt, mobile menu |
| `lang-redirect.js` | Reads `?lang=` param, persists choice in `localStorage` |
| `firebase.json` | Firebase Hosting config (security headers, rewrites) |

## Sections

- **Hero** — AI Engineer pitch
- **Services** (6 cards) — AI agents, voice assistants, automation, AI testing, algo trading, consulting
- **Projects** (5 cards):
  - Alice Assistant 3D — VRM avatar voice AI
  - AI Orchestrator — multi-agent loop
  - BTC Trader — algo trading on Bybit
  - Titan — AI-driven E2E + Visual Regression
  - Cosplay Space — production Next.js marketplace
- **Contact** — email, Telegram, GitHub, LinkedIn

## Internationalization (i18n)

Russian and English share one HTML; strings come from a `T.ru` / `T.en` dictionary at the bottom of `index.html`. Language preference persists in `localStorage` under key `ek_lang`. Legacy `?lang=en` URLs are honored once and cleaned.

## Hosting

Firebase Hosting (project: `ekuznetsov-dev`), domain: `ekuznetsov.dev`.

DNS at Cloudflare (NS-only, no proxy). After Firebase project setup the custom domain wizard issues two TXT/A records to add in Cloudflare.

Security headers configured in `firebase.json`:
- `X-Frame-Options: SAMEORIGIN`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`

## Local Development

No build required. Open `index.html` directly or use any local server:

```bash
npx serve .
# or
python3 -m http.server 8000
```

## Deploy

```bash
./deploy.sh
# or directly
firebase deploy --only hosting
```

First-time setup, see `DEPLOY.md`.

## Contact

- Email: [iam@ekuznetsov.dev](mailto:iam@ekuznetsov.dev)
- Telegram: [@IT_Evgenii_Kuznetsov](https://t.me/IT_Evgenii_Kuznetsov)
- GitHub: [github.com/kuznetsov-ai](https://github.com/kuznetsov-ai)
- LinkedIn: [linkedin.com/in/evgenii-kuznetsov](https://www.linkedin.com/in/evgenii-kuznetsov/)
