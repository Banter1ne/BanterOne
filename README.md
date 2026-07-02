# BanterONE

Premium gamified district operations app for Banter — district reporting, leaderboards,
and the **Bantagachi** RPG character system. $0 dev + test.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Demo credentials

All demo users share password: `Banter123`

| Role | Email |
|---|---|
| District Manager | `dm@banter.com` |
| Store Manager (any of the 11 SMs) | `brandy.a@banter.com`, `trinity.b@banter.com`, `hannah.f@banter.com`, `estrella.m@banter.com`, `claudia.g@banter.com`, `steven.v@banter.com`, `marlena.r@banter.com`, `evyn.j@banter.com`, `dionne.f@banter.com`, `emily.m@banter.com`, `gina.g@banter.com` |
| Key Sales Associate | `associate1@banter.com` … `associate5@banter.com` |
| Body Piercer | `piercer1@banter.com`, `piercer2@banter.com` |

Edit `data/users.csv` to swap in real emails and add per-store associates before the demo.

## District roster (from field roster photo)

11 stores across CO + NM. Store IDs are real: 3922, 123, 242, 907, 1026, 1241, 1332, 2595, 3709, 3739, 3905.

## Architecture

- `app.py` — entry, session gate, tab dispatch
- `lib/auth.py` — mock Microsoft SSO login (swap for `streamlit-msal` for real Azure AD)
- `lib/db.py` — CSV storage adapter (swap for `st.connection("gsheets")` for real Sheets)
- `lib/standards.py` — FY27 commission tiers, monthly targets, store bonus payout scale
- `lib/ui.py` — global premium theme (rose gold / diamond silver on midnight)
- `tabs/` — one file per app tab
- `data/` — local CSV backend (mimics Google Sheets 1:1)
- `docs/` — source PDFs

## Bantagachi character system

- No preset creatures. Human M / F / Non-binary picker on first login.
- Ready Player Me iframe = full color-wheel hair customization, skin tone, face, outfit.
- Banter jewelry unlocks via camera scan → wardrobe → CSS-overlay layer on top of RPM avatar.
- XP + Level progression driven by real sales metrics. No Pokémon vocabulary.

## Phase status

- ✅ Phase 0 — Foundation, login, tab skeleton, 11-store roster, FY27 commission engine
- ⏳ Phase 1 — Home Feed (Performance Island, check-in drawer, social feed)
- ⏳ Phase 2 — My Store (analytics + editable targets)
- ⏳ Phase 3 — District Arena (nested leaderboards, 11 stores)
- ⏳ Phase 4 — Playbook
- ⏳ Phase 5 — Bantagachi RPG (RPM avatar + Banter jewelry overlay + Commission Countdown)
- ⏳ Phase 6 — Real fiancée-store data + Streamlit Cloud deploy

## Deploy (when ready)

Push to GitHub → connect at [share.streamlit.io](https://share.streamlit.io) →
pick the repo → free public URL. Shareable to any of the 11 stores.
