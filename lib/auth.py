"""Mock Microsoft Outlook SSO login.

Swap to `streamlit-msal` (Azure AD) later — `verify_credentials` is the only
call site that changes.
"""
from __future__ import annotations
import hashlib
import streamlit as st
from . import db


def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


def verify_credentials(email: str, password: str) -> dict | None:
    users = db.read("users")
    hit = users[users["email"].str.lower() == email.strip().lower()]
    if hit.empty:
        return None
    row = hit.iloc[0]
    if row["password_hash"] != _hash(password):
        return None
    return row.to_dict()


def logout() -> None:
    st.session_state.pop("user", None)
    st.rerun()


def require_role(*allowed_roles: str) -> bool:
    user = st.session_state.get("user")
    return bool(user) and user.get("role") in allowed_roles


def is_leader() -> bool:
    return require_role("Store Manager", "Assistant Manager", "District Manager")


def is_admin() -> bool:
    return require_role("District Manager")


def render_login_page() -> None:
    st.markdown(_LOGIN_CSS, unsafe_allow_html=True)
    st.markdown(_BRAND_HEADER, unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        with st.form("login_form", clear_on_submit=False):
            st.markdown(
                f'{_MS_LOGO}'
                '<div class="sso-title">Sign in with Microsoft</div>'
                '<div class="sso-sub">Use your Banter corporate account</div>',
                unsafe_allow_html=True,
            )
            email = st.text_input("Work email", label_visibility="collapsed",
                                  placeholder="you@banter.com")
            password = st.text_input("Password", type="password",
                                     label_visibility="collapsed",
                                     placeholder="Password")
            submitted = st.form_submit_button("Continue", use_container_width=True)

        if submitted:
            user = verify_credentials(email, password)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("We couldn't find that account. Check your email and password.")

        with st.expander("Demo credentials"):
            st.code(
                "District Manager:  dm@banter.com          / Banter123\n"
                "Store Manager:     brandy.a@banter.com    / Banter123\n"
                "Associate:         associate1@banter.com  / Banter123",
                language="text",
            )


_BRAND_HEADER = """
<div class="brand-wrap">
  <div class="brand-shimmer"><em>Banter</em>ONE</div>
  <div class="brand-tag">District Operations · Powered By Signet</div>
</div>
"""

_MS_LOGO = """
<div style="display:flex;justify-content:center;margin-bottom:12px;">
<svg width="26" height="26" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  <rect width="11" height="11" fill="#F25022"/>
  <rect x="13" width="11" height="11" fill="#7FBA00"/>
  <rect y="13" width="11" height="11" fill="#00A4EF"/>
  <rect x="13" y="13" width="11" height="11" fill="#FFB900"/>
</svg>
</div>
"""

_LOGIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@400;500;600;700;800&display=swap');
[data-testid="stAppViewContainer"], [data-testid="stHeader"] {
  background: #000000 !important;
}
[data-testid="stAppViewContainer"] { background:
  radial-gradient(ellipse at 50% 30%, rgba(213,229,71,0.16) 0%, #000 65%) !important;
}
[data-testid="stMainBlockContainer"] { padding-top: 3rem; }

.brand-wrap {
  text-align: center;
  margin: 40px 0 44px 0;
  font-family: 'Instrument Serif', Georgia, serif;
}
.brand-shimmer {
  font-family: 'Instrument Serif', Georgia, serif;
  font-size: clamp(72px, 10vw, 132px);
  font-weight: 400;
  letter-spacing: -0.035em;
  line-height: 1;
  background: linear-gradient(
    100deg,
    #ffffff 0%,
    #F5F3EE 22%,
    #D5E547 44%,
    #E4F26A 50%,
    #D5E547 56%,
    #F5F3EE 78%,
    #ffffff 100%
  );
  background-size: 220% auto;
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent; color: transparent;
  animation: banterShimmer 3.4s linear infinite;
  filter: drop-shadow(0 0 32px rgba(213,229,71,0.32));
}
.brand-shimmer em { font-style: italic; }
@keyframes banterShimmer {
  0%   { background-position: 0% center; }
  100% { background-position: 220% center; }
}
.brand-tag {
  margin-top: 14px;
  color: #8B8B8B;
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  font-weight: 500;
}

[data-testid="stForm"] {
  background: linear-gradient(180deg, rgba(17,17,17,0.9), rgba(11,11,11,0.9));
  border: 1px solid rgba(213,229,71,0.22) !important;
  border-radius: 20px !important;
  padding: 32px 32px 26px 32px !important;
  backdrop-filter: blur(14px);
  box-shadow: 0 24px 70px rgba(0,0,0,0.65), 0 0 40px rgba(213,229,71,0.10);
  font-family: 'DM Sans', -apple-system, sans-serif;
}
.sso-title {
  font-family: 'DM Sans', sans-serif;
  font-size: 18px; font-weight: 700; text-align: center;
  color: #F5F3EE;
}
.sso-sub {
  font-family: 'DM Sans', sans-serif;
  font-size: 12px; text-align: center; color: #8B8B8B;
  margin: 4px 0 22px 0;
  letter-spacing: 0.04em;
}
[data-testid="stForm"] [data-testid="stTextInput"] input {
  background: #000000 !important;
  color: #F5F3EE !important;
  border: 1px solid rgba(245,243,238,0.15) !important;
  border-radius: 12px !important;
  padding: 12px 14px !important;
  font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stForm"] [data-testid="stTextInput"] input:focus {
  border-color: #D5E547 !important;
  box-shadow: 0 0 0 2px rgba(213,229,71,0.25) !important;
}
[data-testid="stForm"] .stFormSubmitButton button {
  background: linear-gradient(135deg, #D5E547, #E4F26A) !important;
  color: #0B0B0B !important;
  border: none !important;
  border-radius: 12px !important;
  height: 44px !important;
  font-weight: 800 !important;
  font-family: 'DM Sans', sans-serif !important;
  letter-spacing: 0.02em;
  transition: transform .15s ease, box-shadow .15s ease;
}
[data-testid="stForm"] .stFormSubmitButton button:hover {
  transform: translateY(-1px);
  box-shadow: 0 12px 32px rgba(213,229,71,0.42) !important;
}
[data-testid="stExpander"] {
  background: transparent !important;
  border: 1px dashed rgba(229,228,226,0.12) !important;
  border-radius: 10px;
  margin-top: 22px;
}
[data-testid="stExpander"] summary { color: #94A3B8 !important; }
</style>
"""
