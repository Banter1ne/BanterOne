import streamlit as st
from lib import standards, ui


# ── Structured, searchable playbook content ──────────────────────────────────
# Loaded from the 11 official Banter PDFs in /docs.
PLAYBOOK = [
    # ── Job Aid: CONNECT ─────────────────────────────────────────────────────
    ("Job Aid — CONNECT", "Warm & welcoming greeting",
     "Immediately and warmly acknowledge every customer. Use an appropriate or "
     "preferred banner greeting. Welcome them as if your store is your home."),
    ("Job Aid — CONNECT", "Tablet-in-hand approach",
     "Approach the customer with a tablet in hand as soon as you are able."),
    ("Job Aid — CONNECT", "Positive body language + tone",
     "Show your smile. Make eye contact. Introduce yourself, ask for their name "
     "and use it throughout the interaction."),
    ("Job Aid — CONNECT", "Gratitude + casual conversation",
     "Express gratitude for their visit. Engage in casual conversation to begin "
     "building the relationship. Compliment what they are wearing, ask what "
     "occasion brings them in, or who they are celebrating."),
    ("Job Aid — CONNECT", "Invite them to browse",
     "Invite them to browse with you. If they would like to browse, allow them "
     "space but advise them you are available to assist when ready."),
    ("Job Aid — CONNECT", "Clienteling profile check",
     "Check Clienteling to determine if they have an existing Customer Profile. "
     "If not, create one. 'Have you ever shopped with us before?'"),

    # ── Job Aid: CURATE ──────────────────────────────────────────────────────
    ("Job Aid — CURATE", "Identify a solution to what matters",
     "Identify a product, service, or solution based on what's important to the "
     "customer and the emotional information you've gathered. Honor the price "
     "point the customer expressed. Recommend jewelry based on their style "
     "preferences vs. categories. Provide options versus saying 'no'."),
    ("Job Aid — CURATE", "Partner or turn-over gracefully",
     "Partner or turn-over to another team member when you are unable to meet "
     "the customer's needs. Ensure the customer understands you are bringing "
     "in another team member to help. Stay with the customer and the new "
     "team member when possible."),
    ("Job Aid — CURATE", "Adjust pace, focus, empathy",
     "Adjust your presentation (pace, focus, empathy) to meet the customer's "
     "needs based on the emotional information you observed."),
    ("Job Aid — CURATE", "Accurate product knowledge",
     "Provide accurate product knowledge. Offer personalization and custom."),
    ("Job Aid — CURATE", "Features + benefits + check questions",
     "Present value by giving features, benefits and check questions that are "
     "personalized to that specific customer."),
    ("Job Aid — CURATE", "Overcome objections (style)",
     "If style concern: suggest another piece from your case that eliminates the "
     "concern. Show another piece from your endless aisles of online inventory. "
     "Create a piece of jewelry using custom design if available."),
    ("Job Aid — CURATE", "Overcome objections (price)",
     "If price concern: offer payment options. Show similar merchandise within "
     "the price point. Highlight the rarity, durability, and master craftsmanship."),
    ("Job Aid — CURATE", "Encourage try-on",
     "Encourage the customer to try on or hold the jewelry. The goal is not to "
     "convince them of something they don't want — it's to hear their concern "
     "and find a piece that meets their needs."),

    # ── Job Aid: CLOSE ───────────────────────────────────────────────────────
    ("Job Aid — CLOSE", "Ask for the sale",
     "Upon hearing or observing positive responses to your check questions and "
     "trial closes, ask for the sale or agreement for the recommended solution. "
     "If yes, reassure them of their choices. If they express concern, move back "
     "into presenting solutions."),
    ("Job Aid — CLOSE", "Vault Rewards enrollment",
     "Ensure they are enrolled in the Vault Rewards Program (if applicable). If "
     "not, ask them if they would like to enroll through Clienteling."),
    ("Job Aid — CLOSE", "Jewelry & service package",
     "Present the customer with a professional jewelry & service package for "
     "shopping customers. Include product & service brochures and review details "
     "with the customer. Provide business cards."),
    ("Job Aid — CLOSE", "Set next appointment",
     "Set next appointments and follow-up activities before the customer leaves: "
     "Diamond guarantee inspection, custom, sizing, piercing follow-up, body "
     "piercing consultation."),
    ("Job Aid — CLOSE", "Sincere thank you + Google review ask",
     "Thank the customer with sincerity. Provide a way for them to get directly "
     "in touch with you. Ask if they would be willing to share their experience "
     "and leave feedback in a Google review."),

    # ── Job Aid: CONTINUE ────────────────────────────────────────────────────
    ("Job Aid — CONTINUE", "Follow up after purchase",
     "Follow up with customers to express gratitude and ensure they are happy "
     "with their purchase or service — as soon as possible but without ruining a "
     "surprise."),
    ("Job Aid — CONTINUE", "Congratulate on milestones",
     "Reach out and congratulate customers on special occasions and milestone events."),
    ("Job Aid — CONTINUE", "Enrich the profile",
     "Enrich the customer's profile after each contact. Review their preferences "
     "and purchase history and curate a list of jewelry options and recommendations."),
    ("Job Aid — CONTINUE", "Advance notice of sales",
     "Give your customers advance notice of sales, especially before an important "
     "gift-giving milestone or holiday gift-giving season."),
    ("Job Aid — CONTINUE", "Offer appointment for cleaning + purchase",
     "Offer to set appointments to better serve the customers, especially during "
     "holiday seasons for cleaning and purchasing."),
    ("Job Aid — CONTINUE", "Follow through commitments",
     "Follow through on all customer commitments."),
    ("Job Aid — CONTINUE", "Behaviors to AVOID",
     "Do NOT spoil surprises when following up. Do NOT bombard customers with "
     "emails, especially before major gift-giving occasions. Do NOT make "
     "commitments you can't keep."),

    # ── Exceptional Piercing Experience ──────────────────────────────────────
    ("Piercing Experience", "Piercing greeting",
     "'Hi, welcome to Banter! Are you here to get a piercing today?' / "
     "'Are you here for your piercing appointment?'"),
    ("Piercing Experience", "Add to Clienteling",
     "If they've shopped with us before, welcome them back. Do they have their "
     "Banter card with them? If not, this is the beginning of a beautiful "
     "friendship. Enrich their profile and update their Wishlist during the "
     "interaction."),
    ("Piercing Experience", "Walk to piercing jewelry selection",
     "'Come with me, I can show you our pre-sterilized piercing earrings and "
     "piercing jewelry selection.' Review Best, Better, Good. You're the expert. "
     "Use your knowledge & skills to guide the customer to a selection that is "
     "perfect for them. Mention Payment Options and ESAs."),
    ("Piercing Experience", "Set follow-up appointment",
     "'We want to see you back in x weeks to check on the progress of your "
     "healing. Which day of the week works best for you? We also offer a change "
     "service. Let's pick out another pair of earrings or body jewelry so when "
     "you come back I can make sure they're healed perfectly, change your "
     "earrings and set up your next piercing.'"),

    # ── Power Phrases ────────────────────────────────────────────────────────
    ("Power Phrases", "Phrases to LOSE",
     "AVOID: 'Would you like to…?' / 'Did you want to…?' — The response to "
     "these will almost always be 'no'."),
    ("Power Phrases", "Phrases to USE",
     "USE: 'You should…' · 'You need to…' · 'Let's go ahead and…' · "
     "'Why don't we…' · 'I strongly suggest…' · 'I highly recommend…' · "
     "'You qualify for…'"),
    ("Power Phrases", "Power Phrase examples",
     "'You should pick out another item for half off.' "
     "'You need to get the matching bracelet, they look great together.' "
     "'Let's go ahead and check out our diamond assortment.' "
     "'Why don't we pierce your ears today?' "
     "'I strongly suggest a lobster claw.' "
     "'I highly recommend applying for our Banter Credit Card.' "
     "'You qualify for a replacement credit with the purchase of an ESA.'"),

    # ── Core Values ──────────────────────────────────────────────────────────
    ("Core Values", "People First",
     "Appreciation · Inclusion · Joy. Our people come first. We support and "
     "appreciate each other, embrace differences, celebrate uniqueness, "
     "encourage development, and reward performance. We have fun together and "
     "feel the joy of delivering our mission every day."),
    ("Core Values", "Lead Bravely",
     "Team · Innovative · Agile. We transform our future with courage and "
     "vision by working as a team. We are curious, challenge the status quo, "
     "and innovate. We are agile and fearless, committed to win by focusing on "
     "priorities that make a difference."),
    ("Core Values", "Own It",
     "Accountable · Integrity · Continuous Improvement. We deliver on "
     "commitments because we are personally accountable. We learn from mistakes "
     "and strive for continuous improvement. We are trustworthy, always "
     "operating with the highest integrity."),
    ("Core Values", "Customers",
     "Exceed Expectations · Earn Trust · Build Relationships. We provide truly "
     "memorable experiences, striving to always exceed expectations. We delight "
     "in gaining customer trust, developing lasting relationships, and providing "
     "the best products, service, quality, and value."),
    ("Core Values", "Straight Talk",
     "Honest · Respectful · Collaborative. We listen, seek the truth together, "
     "and tell it like it is, even when it's difficult. We are honest."),

    # ── Who to Contact — key escalation contacts ─────────────────────────────
    ("Who to Contact", "General fallback",
     "If unsure who to reach out to, email banter@signetjewelers.com."),
    ("Who to Contact", "Accounts Payable — bills & expenses",
     "APinvoices@signetjewelers.com · ExpenseReports@signetjewelers.com. "
     "Allow up to 4 weeks after DM approval in Workday. "
     "Send Fire Inspection notices/unpaid fees to APInvoices@signetjewelers.com."),
    ("Who to Contact", "Utility Service Issues",
     "Email both: Karen.Williams@signetjewelers.com and "
     "Alyson.Shirley@signetjewelers.com."),
    ("Who to Contact", "Business Support Services",
     "1 (800) 572-8074. The Loupe and Incentive trips: 1 (330) 668-5000 ext 8074. "
     "MeetingsandIncentives@signetjewelers.com."),
    ("Who to Contact", "Sales Audit + Standards Reporting",
     "Missing sales, questions on standards reporting: "
     "FieldReports@signetjewelers.com. Credit transactions: "
     "BankCardAccounting@signetjewelers.com."),
    ("Who to Contact", "Maintenance Service",
     "Service requests + unpaid bills: 1 (866) 772-8899, option 4. "
     "Light bulbs (Regency Lighting): 1 (800) 284-2024."),
    ("Who to Contact", "Magic Mirror issues",
     "almaz@virtualvisions.com and anmolpreet@virtualvisions.com."),
    ("Who to Contact", "Vacuum repair/replacement",
     "Adrianna Bieniecki: Abieniecki@vsiglobal.com. Return broken vacuum in "
     "replacement box to VSI Global LLC, 9090 Bank St., Cleveland, OH 44125."),
    ("Who to Contact", "New store openings + security bar",
     "Delaina.Gates@signetjewelers.com."),
    ("Who to Contact", "Media inquiries",
     "Review SIGnet's Media Relations Policy first. Then "
     "Mediarelations@signetjewelers.com."),
    ("Who to Contact", "Shipment tracers — DC to store",
     "Include your DM. If the transfer begins with 'S,' email "
     "Cathy.Hugging@signetjewelers.com. If it begins with 'A,' email "
     "Robert.Kinley@signetjewelers.com."),
    ("Who to Contact", "Signet Monitoring Center (SMC) — emergencies",
     "SMC: 1-800-868-0956 · ZMC@zalecorp.com. Partner with your DM for "
     "emergency closure/natural disaster."),
    ("Who to Contact", "Store Maintenance emergency",
     "1-972-580-5400."),
    ("Who to Contact", "Store Operations leadership",
     "Director of Store Operations: Heather.Gardner@signetjewelers.com · "
     "Admin Field Operations: Sheila.Benson@signetjewelers.com · "
     "Communications Coordinator: BobbieJo.Gardner@signetjewelers.com · "
     "Analyst Reporting & Dashboards: Nancy.Lex@signetjewelers.com."),
    ("Who to Contact", "Mall Security (this district)",
     "(302) 270-4500."),

    # ── FY27 balanced business (Comm TK-107) ─────────────────────────────────
    ("FY27 Balanced Business", "Running a balanced business",
     "Balance sales-driving KPIs (Bold, EP, ESA, PO, StJ) with team-development "
     "activities. Coach the metrics that move commission tier, not the vanity ones. "
     "Every associate needs a personal target and a tier-up plan visible on Me tab."),
]


def render() -> None:
    ui.render_store_badge()

    st.markdown("### Playbook")
    st.caption("Scripts, protocols, and reference material. Everything the district needs, one tap away.")

    query = st.text_input(
        "Search",
        placeholder="Search any term across scripts, protocols, promos, talking points…",
        key="playbook_search",
        label_visibility="collapsed",
    )

    if query and query.strip():
        _render_search_results(query.strip())
        return

    # ── Quick-ref cards ──────────────────────────────────────────────────────
    cols = st.columns(2)
    with cols[0]:
        _card(
            "Mall Security",
            [
                ("Phone", "(302) 270-4500"),
                ("When to call", "Any incident, unauthorized entry, medical event."),
                ("Also", "Text updates to the store group chat immediately."),
            ],
        )
    with cols[1]:
        _card(
            "FY27 Commission Ladder",
            [
                ("Piercing", f"{standards.PIERCING_COMMISSION_RATE*100:.0f}% on every dollar. No threshold."),
                ("ESA (warranty)", f"{standards.ESA_COMMISSION_RATE*100:.0f}% on every dollar. No threshold."),
                ("Annual qualifier", f"${standards.ANNUAL_QUALIFY_THRESHOLD:,} in FY26 sales."),
            ],
        )

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    _tier_table()

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    sections: dict[str, list] = {}
    for section, title, body in PLAYBOOK:
        sections.setdefault(section, []).append((title, body))

    for section, items in sections.items():
        with st.expander(section, expanded=False):
            for title, body in items:
                _script(title, body)


def _render_search_results(query: str) -> None:
    q = query.lower()
    hits = [
        (section, title, body) for section, title, body in PLAYBOOK
        if q in title.lower() or q in body.lower() or q in section.lower()
    ]
    if not hits:
        st.markdown(
            f'<div class="glass-card" style="text-align:center;padding:32px;">'
            f'<div style="color:var(--text-dim);font-size:14px;">'
            f'No results for <b style="color:var(--text);">"{query}"</b> in the playbook.'
            f'</div></div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f'<div style="color:var(--text-dim);font-size:12px;letter-spacing:0.18em;'
        f'font-weight:700;text-transform:uppercase;margin:4px 0 12px 0;">'
        f'{len(hits)} RESULT{"S" if len(hits) != 1 else ""}</div>',
        unsafe_allow_html=True,
    )
    for section, title, body in hits:
        body_hl = _highlight(body, query)
        title_hl = _highlight(title, query)
        st.markdown(
            (
                '<div class="glass-card" style="margin-bottom:10px;">'
                f'<div style="color:var(--lime);font-size:10px;letter-spacing:0.22em;'
                f'font-weight:700;text-transform:uppercase;margin-bottom:4px;">{section}</div>'
                f'<div style="font-weight:700;color:var(--text);margin-bottom:6px;'
                f'font-size:15px;">{title_hl}</div>'
                f'<div style="color:var(--text);line-height:1.55;font-size:14px;">{body_hl}</div>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )


def _highlight(text: str, query: str) -> str:
    if not query:
        return text
    import re
    esc = re.escape(query)
    return re.sub(
        f"({esc})",
        r'<span style="background:rgba(213,229,71,0.28);color:var(--lime);'
        r'padding:1px 3px;border-radius:3px;font-weight:700;">\1</span>',
        text,
        flags=re.IGNORECASE,
    )


def _card(title: str, rows: list) -> None:
    body = ""
    for label, value in rows:
        body += (
            '<div style="display:flex;justify-content:space-between;padding:8px 0;'
            'border-top:1px solid var(--border);">'
            f'<span style="color:var(--text-dim);font-size:12px;letter-spacing:0.12em;'
            f'text-transform:uppercase;font-weight:600;">{label}</span>'
            f'<span style="color:var(--text);font-weight:600;text-align:right;'
            f'max-width:60%;">{value}</span>'
            '</div>'
        )
    st.markdown(
        f'<div class="glass-card">'
        f'<h4 style="margin-top:0;letter-spacing:0.2em;">{title.upper()}</h4>'
        f'{body}'
        f'</div>',
        unsafe_allow_html=True,
    )


def _tier_table() -> None:
    rows = ""
    for tier in standards.COMMISSION_TIERS:
        period_target = standards.period_target_for(tier["annual_threshold"], "July")
        rows += (
            '<tr style="border-top:1px solid rgba(229,228,226,0.06);">'
            f'<td style="padding:10px 12px;color:var(--lime);font-weight:800;">L{tier["level"]}</td>'
            f'<td style="padding:10px 12px;color:var(--text);">${tier["annual_threshold"]:,}</td>'
            f'<td style="padding:10px 12px;color:var(--text);">${period_target:,.0f}</td>'
            f'<td style="padding:10px 12px;text-align:right;color:var(--lime);font-weight:800;">'
            f'{tier["rate"]*100:.2f}%</td>'
            '</tr>'
        )
    st.markdown(
        (
            '<div class="glass-card" style="padding:0;overflow:hidden;">'
            '<div style="padding:14px 18px;font-family:\'Instrument Serif\',serif;font-style:italic;'
            'font-size:22px;color:var(--text);">Commission Tiers</div>'
            '<table style="width:100%;border-collapse:collapse;">'
            '<thead><tr style="color:var(--text-dim);font-size:11px;letter-spacing:0.22em;'
            'text-align:left;font-weight:700;">'
            '<th style="padding:10px 12px;">TIER</th>'
            '<th style="padding:10px 12px;">ANNUAL THRESHOLD</th>'
            '<th style="padding:10px 12px;">JULY PERIOD TARGET</th>'
            '<th style="padding:10px 12px;text-align:right;">RATE</th>'
            f'</tr></thead><tbody>{rows}</tbody></table></div>'
        ),
        unsafe_allow_html=True,
    )


def _script(title: str, body: str) -> None:
    st.markdown(
        (
            '<div style="padding:10px 0 14px 0;">'
            f'<div style="font-weight:700;color:var(--lime);margin-bottom:4px;'
            f'letter-spacing:0.02em;">{title}</div>'
            f'<div style="color:var(--text);line-height:1.55;">{body}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )
