# Architecture — ekuznetsov.dev

Static personal site for Evgenii Kuznetsov — AI Engineer. Hosted on Firebase, served via Fastly
CDN (Firebase's transport), DNS at Cloudflare.

---

## 1. Topology

```
visitor browser
     │
     │ HTTPS  (Google Trust Services cert, valid 90 days, auto-renew)
     ▼
ekuznetsov.dev (DNS A 199.36.158.100)  ──── Cloudflare DNS-only (no proxy)
     │
     ▼
Firebase Hosting (project: ekuznetsov-dev)
     ├ /              → index.html       (RU+EN in one file)
     ├ /styles.css
     ├ /script.js
     ├ /lang-redirect.js
     ├ /sitemap.xml, /robots.txt
     ├ /favicon.ico, /favicon.svg
     └ /en            → /en/index.html   (legacy stub redirect)
```

`alice.ekuznetsov.dev` is a separate deployment (Caddy on Silver Server) — see
`alice-assistant-3d/docs/ARCHITECTURE.md`.

---

## 2. Page anatomy

```
┌────────────────────────────────────────────────────────────────────┐
│                            HEADER (sticky, z=102)                  │
│  EK•                          What I do · Projects · GitHub · ... ·│
│                                                              [EN]  │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│                            HERO (100vh)                            │
│  // AI ENGINEER                                                    │
│                                                                    │
│  AI agents, voice assistants,                                      │
│  production LLM systems  ◄─ gradient text                          │
│                                                                    │
│  I build LLM-powered products …                                    │
│                                                                    │
│  [View projects]  [Get in touch]                                   │
│                                                                    │
│  Scroll down ↓                                                     │
├────────────────────────────────────────────────────────────────────┤
│  // STACK                                                           │
│  WHAT I DO                                                          │
│                                                                    │
│  ┌─────────┬─────────┬─────────┐    desktop: 3 cols                │
│  │ AI      │ Voice   │ Auto    │    tablet:  2 cols                │
│  │ agents  │ assist. │ -mation │    mobile:  1 col                 │
│  ├─────────┼─────────┼─────────┤                                   │
│  │ AI test │ Algo    │ Consult │                                   │
│  └─────────┴─────────┴─────────┘                                   │
├────────────────────────────────────────────────────────────────────┤
│  // WORKS                                                           │
│  PROJECTS                                                           │
│                                                                    │
│  ┌───────────────────────┬─────────┐  desktop:                     │
│  │ Alice Assistant 3D    │ AI Orch │  1st card span 8 (featured)   │
│  │ (featured tile)       │         │  2nd card span 4              │
│  ├───────────┬───────────┼─────────┤  rest: span 4 (3 per row)     │
│  │ BTC Trader│ Titan     │ Alice A.│                               │
│  ├───────────┼───────────┼─────────┤                               │
│  │ Sentinel C│ Mafia Web │ Mafia P │                               │
│  ├───────────┴───────────┴─────────┤                               │
│  │ Claude TG Bot                   │                               │
│  └─────────────────────────────────┘                               │
├────────────────────────────────────────────────────────────────────┤
│  // CONTACT                                                         │
│  CONTACT                                                            │
│                                                                    │
│  [✉ Email] [✈ Telegram] [⌨ GitHub] [in LinkedIn]                  │
│   each with brand-coloured hover                                   │
├────────────────────────────────────────────────────────────────────┤
│            © 2026 Evgenii Kuznetsov                                │
└────────────────────────────────────────────────────────────────────┘

   Floating bottom-right (all viewports):
   ┌─────────────────────────┐
   │ 🦊  Поговорить с Алисой │  → https://alice.ekuznetsov.dev
   └─────────────────────────┘
```

---

## 3. CSS architecture

### 3.1 Custom properties (design tokens)

```css
:root {
  --bg: #0a0a0c;
  --text: #e8e8ec;
  --text-muted: #8888a0;
  --accent-cyan:    #00e5cc;
  --accent-magenta: #e040b0;
  --accent-amber:   #f0a020;
  --border: rgba(255,255,255,0.06);
  --radius: 16px;
  --radius-lg: 24px;
  --header-h: 72px;
  --font-heading: 'Unbounded', sans-serif;
  --font-body: 'Manrope', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

### 3.2 Breakpoints

| Range | What kicks in |
|---|---|
| `< 901 px` OR `(pointer: coarse) and < 1101 px` | Burger drawer, single-col layouts, larger tap targets, vertical CTA stack |
| `≥ 901 px AND (pointer: fine)` | Horizontal nav, drawer reset (no fixed positioning) |
| `≥ 1024 px` | 3-col services grid, featured project tile (span 8 + span 4) |
| `≥ 1280 px` | Section max-width 1280, denser padding |

### 3.3 Mobile drawer — the lessons learned

**Final paradigm:** drawer is just a full-viewport opaque overlay. Body scroll is **NOT locked**.
This is the simplest design that doesn't fight any iOS Safari quirk.

```css
header.header .nav {
  position: fixed !important;
  inset: 0 !important;
  width: 100vw !important;
  height: 100dvh !important;     /* dynamic viewport — accounts for iOS bars */
  z-index: 9999 !important;
  background: #0a0a0c !important; /* fully opaque — body underneath invisible */
  transform: translateX(100%);
  transition: transform 0.3s ease;
}
header.header .nav.open { transform: translateX(0) !important; }
```

#### Failed approaches and why

| Tried | Why it broke |
|---|---|
| `body.menu-open { position: fixed; top: -scrollY }` | Worked on most browsers, but on iOS Safari it broke sticky header rendering, broke pull-to-refresh, and made scroll-up jittery. |
| `body.menu-open { overflow: hidden }` only | iOS Safari quietly resets `window.scrollY` to 0 when overflow becomes hidden. User opens drawer → page scrolls to top behind the drawer → they close the drawer and find themselves at top of page, drawer "disappeared". |
| `body.menu-open { overflow: hidden; position: fixed; top: -y }` + restore on close | Functionally correct but breaks `scrollIntoView` for anchor links; needs `setTimeout + RAF×2 + window.scrollTo` work-around per click. Lots of edge-cases. |
| **No body lock at all (current)** | Body can technically scroll behind the drawer if the user dragged through it. But the drawer is fully opaque so they can't see it. Sticky header still works, pull-to-refresh still works, scroll-y is preserved by the browser, anchor links use a plain `setTimeout(320ms)` after close. |

#### Tap handling

Burger button has `touch-action: manipulation` (kills the 300 ms tap-delay) and a JS-level
throttle (`drawerLock` + `lastTap`) to absorb the iOS Safari `tap → click` double-fire that
sometimes left the drawer in a half-toggled state.

#### Anchor links

```js
anchor.click → e.preventDefault()
              → if (drawer.open) closeDrawer()
              → setTimeout(scrollToEl, 320)        // matches drawer transition
              → window.scrollTo({top: target.y - headerH - 8, behavior: 'smooth'})
```

`scrollToEl` accounts for the sticky header height so the section title doesn't sit hidden
behind the bar.

### 3.4 Per-channel contact icons

Each contact link gets `.contact-link--{email,tg,gh,li}` and inline SVG. Hover changes border /
text / box-shadow to the brand colour:

| Channel | Hover accent | SVG used |
|---|---|---|
| Email | `var(--accent-cyan)` | Stroked envelope |
| Telegram | `#2AABEE` (Telegram blue) | Filled paper-plane |
| GitHub | `#fff` | Octocat |
| LinkedIn | `#0a66c2` (LinkedIn blue) | "in" mark |

The Email/Telegram pair uses the cyan accent already defined in `--accent-cyan`; the GitHub and
LinkedIn pair pulls in their corresponding brand colours inline. Inline SVG is preferred over
icon fonts (no extra request, perfect retina, easy to recolor with `currentColor`).

### 3.5 Project cards — uniform grid

Earlier the first project (Alice Assistant 3D) was rendered as a featured "wide tile"
(`grid-column: span 8`) with the rest as `span 4`. Now **all 9 cards are equal** —
`span 4` on desktop (3 per row), `span 6` on tablet (2 per row), `span 1` on mobile (1 column).
This was an explicit design call after the first deploys felt unbalanced.

Two cards have an extra Live link on top of the GitHub link:

- **Alice Assistant 3D** → `Live →` `https://alice.ekuznetsov.dev` + `GitHub →` (muted)
- **Mafia Parser** → `Live →` `https://mafia.ekuznetsov.dev` + `GitHub →` (muted)

Markup pattern:

```html
<div class="project-card__links">
  <a class="project-card__link"               href="...live...">Live →</a>
  <a class="project-card__link project-card__link--ghost" href="...github...">GitHub →</a>
</div>
```

Cyan link first (primary CTA), muted-grey link second (secondary).

---

## 4. JavaScript

`script.js` is the only runtime script (~80 LOC):

1. **Scroll reveal** — `IntersectionObserver` adds `.revealed` to `.service-card`, `.project-card`,
   `.section__title`, `.section__subtitle`, `.contact__text`, `.contact__links`. Triggers fade-up animations.
2. **Tilt effect** — desktop only (`(hover: hover)` skips touch devices). `mousemove` over a
   `[data-tilt]` card writes `transform: perspective(800px) rotateX/rotateY/translateZ`.
3. **Burger menu** — toggles `.open` on burger + nav, `.menu-open` on body and html.
4. **Smooth scroll** — robust anchor handler (see §3.3).

`lang-redirect.js` runs before `index.html` body parses; sets `document.documentElement.lang` and
exposes `window.__ekLang` so the inline `<script>` at the bottom of body picks up the right
dictionary on first paint.

---

## 5. SEO / metadata

- `<title>` and `<meta description>` in both languages, updated by the i18n script
- `<link rel="canonical">` to `https://ekuznetsov.dev/`
- `hreflang="ru|en|x-default"` `<link rel="alternate">` set
- Open Graph & Twitter Card meta tags
- JSON-LD `Person` schema with name, jobTitle, email, sameAs (GitHub/LinkedIn), knowsAbout array
- `sitemap.xml` and `robots.txt` (disallow `?lang=`)

---

## 6. Hosting & DNS

### 6.1 Firebase project

- Project ID: `ekuznetsov-dev`
- Hosting site: `ekuznetsov-dev` (default URL: `ekuznetsov-dev.web.app`)
- Owner Google account: `i.want.balance.it@gmail.com` (Eugene's "balance" account)
- Configured locally via `.firebaserc` + `firebase login:use i.want.balance.it@gmail.com` for this directory

### 6.2 Custom domain attach (REST flow used)

```
POST https://firebasehosting.googleapis.com/v1beta1/
     projects/ekuznetsov-dev/sites/ekuznetsov-dev/customDomains?customDomainId=ekuznetsov.dev
```

Firebase returns required DNS:

```
A    ekuznetsov.dev                  → 199.36.158.100
TXT  ekuznetsov.dev                  → "hosting-site=ekuznetsov-dev"
TXT  _acme-challenge.ekuznetsov.dev  → <ACME challenge>
CNAME www.ekuznetsov.dev             → ekuznetsov-dev.web.app
TXT  _acme-challenge.www.ekuznetsov.dev → <www ACME challenge>
```

All written to Cloudflare via the Cloudflare REST API.

> **CF account migration (2026-04-26):** zone moved from iDev account
> (`idev43674@gmail.com`, NS `anuj/gemma.ns.cloudflare.com`) to balance account
> (`i.want.balance.it@gmail.com`, NS `dane/melody.ns.cloudflare.com`). Zone id
> in balance: `c2e05117a2493a207835c1e8966d4f13`. Old iDev zone deleted after
> activation. Auth for new zone uses balance Global API Key
> (`X-Auth-Email: i.want.balance.it@gmail.com` + `X-Auth-Key`).

### 6.3 Existing DNS at Cloudflare zone `ekuznetsov.dev`

| Type | Name | Value | Proxy |
|---|---|---|---|
| A | `ekuznetsov.dev` | 199.36.158.100 (Firebase) | off |
| CNAME | `www.ekuznetsov.dev` | ekuznetsov-dev.web.app | off |
| A | `mafia.ekuznetsov.dev` | 89.167.108.210 (Silver) | off |
| A | `mf.ekuznetsov.dev` | 89.108.78.194 (S1LveRus) | off |
| A | `alice.ekuznetsov.dev` | 89.167.108.210 (Silver, Caddy → Aliska) | off |
| MX | `ekuznetsov.dev` | route1/2/3.mx.cloudflare.net | — |
| TXT | `ekuznetsov.dev` | SPF for Cloudflare email routing | — |
| TXT | `cf2024-1._domainkey` | DKIM | — |

Email routing: `iam@ekuznetsov.dev` → forwarded to `i.want.balance.it@gmail.com` via Cloudflare
Email Routing.

### 6.4 SSL

Firebase auto-provisions a Google Trust Services certificate (`WR3` intermediate, 90-day rotation).
Initial provisioning takes 15–30 minutes; status visible in Firebase Console → Hosting.

---

## 7. Deploy & rollback

```bash
# from project root
firebase deploy --only hosting
```

Firebase keeps the last N releases; rollback via Console → Hosting → release history → Rollback.

`deploy.sh` is a thin wrapper that runs the above with `cd $(dirname "$0")` for safety.

GitHub Actions workflow was removed because we never provisioned `FIREBASE_TOKEN` in repo Secrets
— deploys are manual until that's set up.

---

## 8. Testing

`testMe/ui_test_scenarios.py` is loaded by Titan via `config/systems/ekuznetsov-dev.yaml`. Five
scenarios across desktop / tablet / mobile, see `README.md` for the table.

Latest run: **9 passed, 0 failed** at viewport coverage 1440×900, 768×1024, 393×852.

---

## 9. Repo layout

```
ekuznetsov-dev/
├── README.md
├── DEPLOY.md
├── deploy.sh
├── firebase.json
├── .firebaserc
├── index.html
├── en/index.html             # legacy redirect stub
├── styles.css
├── script.js
├── lang-redirect.js
├── sitemap.xml
├── robots.txt
├── favicon.ico, favicon.svg
├── docs/
│   └── ARCHITECTURE.md       # this file
└── testMe/
    └── ui_test_scenarios.py  # Titan E2E suite
```

---

## 10. Known gotchas

- **iOS Safari "Request Desktop Site"** can read viewport as 980+ px even on a 6-inch phone.
  CSS uses `(pointer: coarse) and (max-width: 1100px)` as the second mobile-rule trigger so
  the burger drawer still appears.
- **Never lock body scroll** behind the drawer (no `position: fixed`, no `overflow: hidden`
  on body or html). It looks like the right thing to do but breaks iOS scroll-y, sticky header,
  pull-to-refresh, and anchor smooth-scroll. The drawer being fully opaque is enough to hide
  the body underneath.
- **`hash` change** on anchor links must run AFTER drawer close — the close transition is
  300 ms, our timer is 320 ms before `scrollToEl`.
- **Burger double-tap** on iOS — handled by `touch-action: manipulation` + a 300 ms JS throttle
  (`drawerLock` + `lastTap`).
- **Firebase TLS provisioning** is asynchronous and slow. The `web.app` URL works immediately;
  the custom domain takes 10–30 minutes for the Google-Trust-Services cert.
- **Cloudflare DNS-only mode** — proxy is off on the apex/www. If we ever need WAF / rate-limit
  at the edge, enable proxy and verify Firebase still recognises the cert (it does — they share
  Google CDN / Fastly transport).
- **Removing projects from the page**: also clean references in JSON-LD, social meta-tags, and
  `SOUL.md` / `PROJECTS.md` in `alice-assistant-3d/workspace_guest/` so Aliska doesn't talk about
  things that are no longer on the page.
- **English plural** — the section title and tag use `Contacts` (plural). Russian is `Контакты`.
  Single-form `Contact` was pre-2026-04-25.
