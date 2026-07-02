# BanterONE — Session Handoff

State updated on **2026-07-02**. Everything below is what a new session needs
to pick up cleanly.

## What the app is
A Streamlit district-ops app for Banter (Signet Jewelers) with 5 tabs:
Home Feed · My Store · B / Banter Buddy tab · Playbook · District Arena.
Backend is local CSVs in `data/`. All lime accents (Banter's FY26 rebrand
color `#D5E547`), Instrument Serif italic for major headers, DM Sans for
body. Bottom nav is a rounded floating island; center tab is "**B**"
(Instrument Serif italic, slightly larger) — the Bantagachi tab.

## Runbook
```bash
cd /Users/user/Claude/Projects/BanterONE
pip install -r requirements.txt
streamlit run app.py
# Login: brandy.a@banter.com / Banter123
```

## Architecture
- `app.py` — entry, tab dispatch via `st.session_state.current_tab`
- `lib/auth.py` — mock Outlook login (real MS SSO swap = swap `verify_credentials`)
- `lib/db.py` — local CSV adapter (swap for `st.connection('gsheets')` for persistence)
- `lib/standards.py` — FY27 commission tiers, monthly targets, store bonus scale
- `lib/rpg.py` — jewelry catalog, XP, league ranking, commission countdown
- `lib/buddy.py` — Banter Buddy starters, care meters, evolution rules, local JSON persistence
- `lib/stylist.py` — legacy DiceBear avatar module; no longer the main B tab direction
- `lib/ui.py` — global theme, masthead, bottom nav, store badge, avatar helper
- `tabs/home.py` — store badge + Performance Island + Daily Feed w/ reactions
- `tabs/my_store.py` — KPI strip, Traffic/Conversion/MTD charts, Weekly Targets
- `tabs/leaderboard.py` — Today/Monthly/YTD × Store/Individual leaderboards
- `tabs/playbook.py` — 60+ searchable scripts (Job Aids CCCC, Power Phrases, Core Values, Who to Contact)
- `tabs/me_tab.py` — Banter Buddy starter picker + care/evolution dashboard + stats + PFP + League

## Data files
- `data/users.csv` — 22 seeded users (11 real store managers, DM + associates)
- `data/stores.csv` — all 11 real stores + real mall names + phone numbers
- `data/daily_submissions.csv` — 11 stores × 10 AM check-ins (real 7/1 data)
- `data/individual_metrics.csv` — 14 real employee sales rows
- `data/home_feed.csv` — 25 feed posts (author, content, is_pinned, likes/laughs/fires/party)
- `data/buddy_profiles.json` — Banter Buddy starter/care state, per-email
- `data/stylist_profiles.json` — legacy avatar customizations, per-email

## Real business data seeded
- Fiancée's store: **3922 Cherry Creek** (Brandy A. is the SM). Demo also covers Park Meadows 3905, Aurora 242, Chapel Hills 1241.
- District Manager: **Tasha Gerold**. Region: **Amanda Horn**.
- 11 stores across CO + NM, all real store IDs from field roster photo.
- St. Jude donation tiers seeded from real PDF donation reports (Emily M. leads at $975).
- FY27 commission ladder: L1 at $50k → L7 at $500k, rates 0.5%–3.75%.
- Mall Security phone: (302) 270-4500 (from sticky note in roster photo).

## Deploy state
- Local git initialized on branch `main`, two commits.
- GitHub push status: user was mid-flow. Repo target = `kingsupreme89/BanterONE` (public).
- Streamlit Cloud: user was on the deploy form. Needs repo pushed first.

## Current update (pass #20)
1. ✅ Pivoted away from inconsistent human DiceBear avatars to original Tamagotchi-style Banter Buddy creatures
2. ✅ Added `lib/buddy.py` with three starters: Spark Buddy, Gem Buddy, Glow Buddy
3. ✅ B tab now starts with a three-starter choice, then shows care meters and evolution progress
4. ✅ Character mode small avatars now use Banter Buddy creature chips instead of DiceBear
5. ✅ App shell now behaves fullscreen: wide container, hidden Streamlit header/toolbar/sidebar/footer, full-width content area, fixed bottom nav
6. ✅ Login screen now receives the same global fullscreen shell CSS before the auth gate
7. ✅ Removed the Scan Banter Jewelry camera section and old Wardrobe card from the B/Profile screen
8. ✅ Saved generated starter concept art to `assets/buddies/banter-buddy-starter-concepts.png`
9. ✅ Improved Playbook search with normalized matching and aliases for warranty/ESA, safety/security, Vault/Clienteling, etc.
10. ⚠️ Google Sheets adapter not started. Plan unchanged: `pip install streamlit-gsheets-connection`, wrap `db.read`/`db.write` to try gsheets first with CSV fallback.

## Previous pass notes (pass #19)
1. ✅ Cherry Creek font reverted to Instrument Serif italic
2. ✅ Reactions functional (👍 😂 🔥 🎉) — `home_feed.csv` has `party` column
3. ✅ Me tab renamed to "**B**" in Instrument Serif italic, only slightly larger than sibling tabs
4. ↩️ Human avatar direction has been reversed; current direction is original Banter Buddy creatures
5. ✅ Playbook: `Mall Security` + `FY27 Commission Ladder` titles → lime; search field container has `st-key-playbook_search_wrap` for black-bg CSS
6. ✅ Me tab customizer was replaced by the starter/care/evolution Banter Buddy flow.
7. ⚠️ **Google Sheets adapter not started.** Plan: `pip install streamlit-gsheets-connection`, wrap `db.read`/`db.write` to try gsheets first with CSV fallback. User needs to: create a Google Sheet with worksheets named to match CSV files, create a service account JSON via Google Cloud, share the sheet with the service account email, paste JSON into Streamlit Cloud secrets under `[connections.gsheets]`.

## Answers the user asked but I didn't finish responding to
- **Coworker credentials:** any of the 22 seeded emails + `Banter123`. Cherry Creek team (fiancée's store): `brandy.a@banter.com`, `cc_assoc1@banter.com`, `cc_assoc2@banter.com`, `cc_piercer@banter.com`.
- **Profile-pic click → Me:** already implemented. Whole store badge is clickable via `.st-key-clickable_badge_container` overlay button → `session_state.current_tab = "me"`.
- **Playbook search results:** the search function DOES work (tested); user's confusion may be because results render at the top of the tab. PLAYBOOK has 60+ items; try `piercing`, `credit`, `Vault Rewards`, `Mall Security`.

## Task list (last known state)
1. ✅ Phase 0 · Foundation scaffold
2. ✅ Phase 1 · Home Feed
3. ✅ Phase 2 · My Store
4. ✅ Phase 3 · District Arena
5. ✅ Phase 4 · Playbook
6. ✅ Phase 5 · Bantagachi RPG
7. 🔄 Phase 6 · Deploy + real roster swap (in progress — user actively deploying)
8. ✅ Rebrand + bottom nav + feed stories
9. ✅ Reset XP + Apple-Music nav + facial piercings
10. ✅ Serif headers + masthead + click sound + PFP uploads
11. ✅ Fixed gear + lime radios + gray-mode + lime-inactive tabs
12. ✅ Bantagachi → Stylist rename + emoji purge + lime headers
13. ✅ Stylist customizer with live SVG preview
14. ✅ RPM flow + real Performance Island + Daily Feed rename
15. ✅ Clickable store badge + black Weekly Targets + Playbook search
16. ✅ Playbook expansion + feed→arena + font fixes
17. ✅ DiceBear character + Me center nav + badge→Me
18. ✅ Cherry Creek font revert + reactions + shrink Me + deploy prep
19. 🔄 Bantagachi creature + B tab + Playbook fixes + Sheets setup (this pass)

## To resume in a new Claude session
Paste this prompt to the new session:

> I'm continuing work on `/Users/user/Claude/Projects/BanterONE` — a Streamlit
> district-ops app for Banter Jewelers. Read `HANDOFF.md` at the project root
> for full state. Highest-priority open work:
> (1) continue from the Banter Buddy starter/evolution system in `lib/buddy.py`
> and `tabs/me_tab.py`, and
> (2) wire up Google Sheets as the persistence backend (`lib/db.py`) with a CSV
> fallback so the user can push code changes without wiping demo data.
> Then continue whatever the user asks next.
