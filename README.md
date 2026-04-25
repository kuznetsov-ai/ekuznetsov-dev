# ekuznetsov.dev

Personal site of **Evgenii Kuznetsov** — AI Engineer.

**Live:** https://ekuznetsov.dev (also `www.ekuznetsov.dev`)

---

## Tech stack

Static site, plain HTML + CSS + JavaScript — no framework, no build step.

| File | Purpose |
|------|---------|
| `index.html` | Main page with full RU+EN i18n via in-page dictionary |
| `en/index.html` | Legacy stub — redirects to `/?lang=en` |
| `styles.css` | Dark theme, gradient orbs, scroll reveal, mobile drawer, per-channel contact hover |
| `script.js` | Scroll reveal, 3D card tilt, mobile burger drawer, smooth-scroll-anchored navigation |
| `lang-redirect.js` | Reads `?lang=`, persists in `localStorage`, picks RU only if `navigator.languages` says so |
| `firebase.json` | Firebase Hosting config — security headers, `/en` rewrite |
| `testMe/` | Titan E2E test suite (9 scenarios across 3 viewports) |

---

## Sections

- **Hero** — `AI Engineer` label + "AI agents, voice assistants, production LLM systems"
- **What I do** (6 cards) — AI agents, voice assistants, AI-driven automation, AI-driven testing, algo trading & analytics, AI consulting
- **Projects** (11 cards, all from public github.com/kuznetsov-ai):
  1. **Alice Assistant 3D** — Three.js + VRM voice assistant
  2. **AI Orchestrator** — dual-agent loop (writer + reviewer)
  3. **BTC Trader** — algo trading bot for BTC/USDT on Bybit
  4. **Titan** — E2E + Visual Regression with Claude analysis
  5. **Alice Assistant** — main Alice (PWA + Chrome ext, OpenClaw runtime)
  6. **Sentinel Cyber** — anti-fraud monitoring dashboard
  7. **Mafia Website** — Django mafia-club platform with EN/RU/UK i18n
  8. **Mafia Parser** — stats analyzer for mafgame.org / imafia.org
  9. **Claude TG Bot** — Telegram wrapper over `claude -p` with voice transcription
  10. **Studio CRM** — full-featured CRM for outstaff agencies (Django 5 + React 19 + WebSocket chat + AI assistant), public demo with daily-reset shared sandbox
  11. **Fast Whisper** — local 1h-interview transcription in ~2.5 min on M5 Pro (mlx-whisper Apple Metal + `claude -p` semantic diarization → Google Doc), Fireflies replacement for hiring interviews
- **Contact** — Email / Telegram / GitHub / LinkedIn (each with its own brand-coloured SVG icon and hover accent)
- **Floating CTA** — `Поговорить с Алисой 🦊` → opens https://alice.ekuznetsov.dev (the public guest assistant)

---

## Internationalisation (i18n)

One HTML, two languages.

`<elem data-i18n="key">…</elem>` references entries in a `T = {ru: {...}, en: {...}}` dictionary
at the bottom of `index.html`. `lang-redirect.js` decides the active language:

1. If `?lang=en` or `?lang=ru` in URL — use that, persist, clean the URL.
2. Else read `localStorage['ek_lang']`.
3. Else look at `navigator.languages` — RU only if a Russian locale is explicitly preferred,
   otherwise default to **English** (corrects the previous "always RU" bug).

The `EN`/`RU` toggle in the header swaps `document.documentElement.lang` and re-applies the dictionary.

---

## Mobile drawer

`@media (max-width: 900px), (pointer: coarse) and (max-width: 1100px)` — burger replaces the
horizontal nav. `(pointer: coarse)` part catches **iOS Safari "Request Desktop Site"** mode where
viewport reads as 980+ px on mobile.

Drawer specifics:

- `position: fixed; inset: 0` (`width: 100vw, height: 100dvh`) — covers viewport
- Solid `#0a0a0c` background, `z-index: 9999` — above sticky header (z=102)
- `body.menu-open { overflow: hidden }` — locks page scroll behind it
- **Smooth-scroll fix**: when an anchor link is tapped from inside the drawer, the burger toggles
  closed FIRST, then `requestAnimationFrame` × 2 + 320 ms delay, then `window.scrollTo` with
  header-height offset. Earlier the scroll fired while `body.menu-open` still locked the page —
  visual no-op.

---

## Hosting

- **Firebase Hosting** project `ekuznetsov-dev` (Google account `i.want.balance.it@gmail.com`)
- DNS at **Cloudflare** (zone `0f07fe3451a105e11f0360844edc197b`, NS-only — no proxy on this domain)
- Auto-deploy disabled — workflow file removed because no `FIREBASE_TOKEN` secret was provisioned
- Manual deploy via `firebase deploy --only hosting` (see `DEPLOY.md`)

Security headers in `firebase.json`:
- `X-Frame-Options: SAMEORIGIN`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`

---

## Local development

No build required:

```bash
npx serve .
# or
python3 -m http.server 8000
```

For Firebase emulator (matches headers/rewrites):

```bash
firebase emulators:start --only hosting
```

---

## Deploy

```bash
./deploy.sh
# or directly
firebase deploy --only hosting
```

First-time setup (custom domain, DNS): see `DEPLOY.md`.

---

## Tests (Titan)

E2E suite is in `testMe/ui_test_scenarios.py`. Covers 3 viewports:

```bash
cd ~/Projects/Personal\ projects/titan
python3 cli.py test --system config/systems/ekuznetsov-dev.yaml --scenario ekuznetsov-dev
```

| Scenario | What it asserts |
|---|---|
| `s01_hero` | Hero title + 2 CTA buttons on desktop/tablet/mobile, no "Cyprus" / "Open to work" leftovers |
| `s02_mobile_drawer` | Drawer fills the viewport, ≥4 nav links visible, z-index above header |
| `s03_drawer_projects_scroll` | Tapping "Projects" in drawer closes it and scrolls to the section under sticky header |
| `s04_projects_no_cosplay` | Exactly 4 (now 9) project cards, no `cosplay` / `cyprus` substring on the page |
| `s05_alice_cta` | Floating Alice button visible on every viewport, links to `alice.ekuznetsov.dev` |

Last run: **9 / 9 PASS**.

---

## Contact

- Email: [iam@ekuznetsov.dev](mailto:iam@ekuznetsov.dev)
- Telegram: [@IT_Evgenii_Kuznetsov](https://t.me/IT_Evgenii_Kuznetsov)
- GitHub: [github.com/kuznetsov-ai](https://github.com/kuznetsov-ai)
- LinkedIn: [linkedin.com/in/evgenii-kuznetsov](https://www.linkedin.com/in/evgenii-kuznetsov/)
- AI Assistant: [alice.ekuznetsov.dev](https://alice.ekuznetsov.dev) (talk to Alice 🦊)
