# Deploy ekuznetsov.dev (Firebase Hosting)

Static site deployed to Firebase Hosting at the custom domain `ekuznetsov.dev`.

---

## 1. Firebase project setup (one-time)

```bash
# Install Firebase CLI (one-time, system-wide)
npm install -g firebase-tools

# Log in with the Google account that owns the project
firebase login
```

Create the project (if it doesn't exist yet):

1. Open https://console.firebase.google.com.
2. **Add project** → name `ekuznetsov-dev` → continue without Analytics.
3. Inside the project, **Build → Hosting → Get started**.

If the project ID Firebase assigns differs from `ekuznetsov-dev`, update `.firebaserc`:

```json
{ "projects": { "default": "<actual-project-id>" } }
```

---

## 2. Custom domain setup (one-time)

In Firebase Console → **Hosting → Add custom domain**:

1. Enter `ekuznetsov.dev` → continue.
2. Firebase displays a TXT record for verification → add it in **Cloudflare DNS** for `ekuznetsov.dev` (Type: TXT, Name: `@`, Value: as shown).
3. After verification (a few minutes), Firebase shows two A records → add both in Cloudflare:
   - `@ → 199.36.158.100`
   - `@ → 199.36.158.101`
4. Repeat for `www.ekuznetsov.dev` (CNAME or A pair).
5. Cloudflare proxy stays **off** (DNS only) — Firebase manages TLS itself.
6. SSL provisioning takes up to 24h. Status visible in Firebase Hosting panel.

---

## 3. Deploy

From the project root:

```bash
./deploy.sh
```

or directly:

```bash
firebase deploy --only hosting
```

Deploy uploads everything in the project root except entries in `firebase.json` `ignore` list.

---

## 4. Local preview before deploy

```bash
npx serve .
# open http://localhost:3000
```

For Firebase emulator (matches headers/rewrites):

```bash
firebase emulators:start --only hosting
# open http://localhost:5000
```

---

## 5. Rollback

Firebase keeps last N releases. Roll back from Console → Hosting → release history → **Rollback**.

Or via CLI:

```bash
firebase hosting:clone <site>:<version> <site>:live
```
