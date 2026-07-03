# BanterONE — Session Handoff

Last updated: **2026-07-03**

---

## Links & Repo

- **Live URL:** `banterone.netlify.app` (auto-deploys from GitHub on every push)
- **Repo:** `https://github.com/kingsupreme89/banterone.git` (branch: `main`)
- **Primary file:** `/Users/user/Claude/Projects/BanterONE/redesign/index.html`
- **Always sync after every edit:** `cp redesign/index.html /Users/user/Documents/BanterONE/index.html`
- **Netlify deploys from:** `redesign/` folder (see `netlify.toml`)
- **Preview server config:** `/Users/user/Claude/Projects/BanterONE/.claude/launch.json`
  - Name: `banterone-redesign`, port 4175, serves `/Users/user/Documents/BanterONE/`

---

## What the App Is

BanterONE is a **retail district operations mobile web app** for Banter (Signet jewelry brand). It's a **single HTML file** — no build system, no framework, no bundler. All UI is rendered via `innerHTML` replacement with a `render()` / `setState()` pattern. Data is stored in **Firebase Firestore** and syncs in real time across all users.

---

## Architecture

### HTML DOM structure
```
<main id="app">
  <div id="screen-wrap">   ← scrollable content, persistent (never replaced)
  <div id="nav-wrap">      ← bottom nav bar
  <div id="overlay-wrap">  ← modals and bottom sheets
```

The three wrapper divs are **never removed from the DOM** — only their `innerHTML` is swapped. This preserves scroll position across re-renders.

### Core patterns
- `setState(patch)` → `Object.assign(state, patch)` → `saveState()` → `render()`
- `saveState()` → writes `{email, tab}` to `localStorage`, debounce-saves user fields to Firestore
- `render()` → swaps screen HTML, preserves `scrollTop` on same-tab re-renders, rebuilds nav + overlays
- All click handling via one delegated listener on `#app` using `data-action="..."` attributes
- `data-stop` on sheet overlays blocks click-through; close buttons bypass it via `data-action` check order
- Overlays rendered into `overlayWrap` separately from the main screen — no scroll disruption

### Tech stack
- Vanilla HTML/JS/CSS (no React, no build step)
- Firebase Firestore compat SDK v10.12.2 via CDN
- Netlify for hosting
- PWA (Add to Home Screen) — manifest, apple-touch-icon, `100dvh`, `viewport-fit=cover`

---

## Login / Users

**Password rule:** first + last initials, uppercase
- Brandy A. → `BA`
- Kimberly Toledo → `KT`
- Tasha Gerold → `TG`

| Email | Name | Role | Store |
|---|---|---|---|
| `dm@banter.com` | Tasha Gerold | District Manager | DISTRICT (all stores) |
| `brandy.a@banter.com` | Brandy A. | Store Manager | 3922 Cherry Creek |
| `kimberly.t@banter.com` | Kimberly Toledo | Asst Manager | 3922 Cherry Creek |
| `trinity.b@banter.com` | Trinity B. | Store Manager | 123 |
| `hannah.f@banter.com` | Hannah F. | Store Manager | 242 |
| `estrella.m@banter.com` | Estrella M. | Store Manager | 907 |
| `claudia.g@banter.com` | Claudia G. | Store Manager | 1026 |
| `steven.v@banter.com` | Steven V. | Store Manager | 1241 |
| `marlena.r@banter.com` | Marlena R. | Store Manager | 1332 |
| `evyn.j@banter.com` | Evyn J. | Store Manager | 2595 |
| `dionne.f@banter.com` | Dionne F. | Store Manager | 3709 |
| `emily.m@banter.com` | Emily M. | Store Manager | 3739 |
| `gina.g@banter.com` | Gina G. | Store Manager | 3905 |
| + associates and piercers per store | | | |

---

## Firebase / Firestore

Firebase config is **embedded directly in the HTML** (around line 1090).
**Project:** `banterone-5cb2c`

### Collections

| Collection | Contents | Listener |
|---|---|---|
| `feed` | Shared feed posts, `orderBy("timestamp", "desc")`, limit 50 | Real-time after login |
| `reports` | Disciplinary reports, `orderBy("createdAt", "desc")` | Real-time after login |
| `users/{email}` | Per-user data document | Loaded once on login; saved on change |

### Feed post document shape
```js
{
  name, initials, authorEmail,
  timestamp: Firestore.Timestamp,   // server timestamp
  flair: "shoutout" | "news" | "update",
  pinned: boolean,
  text: string,
  reactions: { like: 0, heart: 0, laugh: 0, fire: 0, party: 0 }
}
```
Post IDs are **Firestore string document IDs** (not numbers).

### Disciplinary report document shape
```js
{
  employeeName, employeeEmail, storeId,
  type: "coaching" | "written-warning" | "final-warning" | "pip",
  date: "YYYY-MM-DD",
  createdAt: Firestore.Timestamp,
  notes, issuedBy
}
```

### Per-user Firestore fields (`users/{email}`)
`buddy`, `charges`, `chargesEarned`, `rubies`, `myReactions`, `toggles`, `userOverrides`, `districtName`, `unread`, `userPhoto`

### Firestore rules
Currently **test mode** (open read/write). Must tighten before production.

---

## State Shape (key fields)

```js
{
  tab: "home",                      // active screen
  selectedUserEmail: "...",         // logged-in user's email
  userPhoto: "",                    // base64 JPEG 120×120

  buddy: { level, xp, xpNext, care, spark, bond },
  charges: { feed, train, cheer },  // earned on login from daily sales
  chargesEarned: bool,
  rubies: "$128",                   // St. Jude counter
  myReactions: { "postId_key": true },
  toggles: { notifPush, notifEmail, notifAchievements, soundOn, ... },
  userOverrides: { "email": { name } },  // profile name edits
  districtName: "District 4 — Colorado",
  disciplinaryReports: [],          // populated by Firestore listener
  feed: [],                         // populated by Firestore listener

  // Ephemeral UI state (not saved to Firestore)
  settingsOpen, settingsView,
  composeOpen, composeText, editingPostId,
  flairOpen, pendingFlair,
  postMenuId,                       // string Firestore doc ID of open ⋯ menu
  reportsOpen, newReportOpen,
  infoOpen, notifOpen,
  calendarOpen, calendarMonth, calendarYear, calendarSelectedDay,
  train,                            // null | { step, lessonId, answers }
  toast,
}
```

---

## Features Built

### Home tab
- KPI cards tap through: District Today + District Rank → Arena tab; Store Today + MTD → Store tab
- Store card with avatar icon (🏪) and calendar button
- Daily Feed — real-time Firestore posts with live timestamps (`timeAgo()`)
- Post ⋯ menu: own posts → Edit / Delete; others' posts → Report
- Reactions (👍❤️😂🔥🎉) glow neon green when active; counts sync via `FieldValue.increment()`

### Store tab
- Full KPI grid: sales, transactions, piercings, ESA/warranty, payment options, St. Jude, conversion, MTD pace
- Weekly targets and MTD progress bars with % attainment
- Team roster with individual metrics per employee, sorted by sales
- FY27 annual goals section
- **Manager Tools → Disciplinary Reports:**
  - Store Manager sees their store only; DM sees all stores
  - Types: Coaching, Written Warning, Final Warning, PIP (color-coded badges)
  - New report form saves to Firestore `reports` collection

### Buddy tab
- Buddy gem character (`buddy-gem.png`) with level pill overlay
- Stat bars: Care, Spark, Bond
- Feed / Train / Cheer charges (earned from daily sales numbers at login)
- Train flow: pick lesson → read article → quiz → XP + stat reward

### Playbook tab
- Lesson list with PDF download links
- Opens lesson article, then advances to quiz

### Arena tab
- District leaderboard ranked by sales
- Today / Week / MTD scope toggle

### Settings
- **Profile:** avatar with 📷 camera badge → pick from photo library → compressed to 120×120 JPEG → saved to Firestore
- Name edit with Save button; shows "Changes saved" toast
- Notifications, Appearance, Security, Language toggle sections
- Workplace Admin: district name, members, roles, integrations, billing, compliance, workflow
- Sign out clears session and unsubscribes all Firestore listeners

### PWA
- `manifest.json` + `icon-192.png`
- `apple-touch-icon`, `theme-color: #0a0a0a`, `apple-mobile-web-app-capable`
- `user-scalable=no, maximum-scale=1, viewport-fit=cover` — no zoom on iPhone
- `100dvh` for true fullscreen (avoids Safari URL bar)
- `html, body { background: var(--bg) }` — no white bars on iPhone safe areas

---

## Files in `redesign/`

| File | Purpose |
|---|---|
| `index.html` | Entire app — all HTML, CSS, JS |
| `manifest.json` | PWA manifest |
| `icon-192.png` | App icon (192×192) |
| `buddy-gem.png` | Buddy character image |
| `buddy-gem2.png` | Alt buddy image |

---

## Known Issues / Pending Work

- **Firestore rules are open** (test mode) — needs real rules before wider rollout
- **Profile photos only show for own posts** — other users' post avatars still show initials. Fix: store `authorPhoto` field on post document at publish time (`state.userPhoto` at moment of posting)
- **No push notifications** — would need Firebase Cloud Messaging
- **App to App Store:** HTML/PWA → wrap with **Capacitor** when ready to ship (few days of work, not a rewrite)
- **Genies Avatar SDK** is Unity-only; cannot be used in this web app. Could be used if the app is rebuilt native

---

## To Resume in a New Session

Start with:

> I'm continuing work on BanterONE. Read `HANDOFF.md` at `/Users/user/Claude/Projects/BanterONE/HANDOFF.md` for full context, then continue from where we left off.
