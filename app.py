import streamlit as st
import streamlit.components.v1 as components
from datetime import date, datetime
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

st.set_page_config(page_title="Be Well", page_icon="💚", layout="centered")

# ── Supabase client ────────────────────────────────────────────────────
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Missing SUPABASE_URL or SUPABASE_KEY in .env file.")
    st.stop()


def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


sb = get_supabase_client()

# Restore auth session if we have tokens stored
if st.session_state.get("access_token") and st.session_state.get("refresh_token"):
    try:
        sb.auth.set_session(
            st.session_state["access_token"],
            st.session_state["refresh_token"],
        )
    except Exception:
        pass

# ── Global CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Montserrat font ── */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');

    .stApp, .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2,
    .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    .stButton > button, .stTextInput input, .stTextArea textarea,
    .stSelectbox, .stDateInput input, .stCheckbox label,
    .stFileUploader, .stAlert, .block-container,
    .stPopover > button {
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Hide Streamlit chrome */
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {
        max-width: 420px !important;
        padding: 1rem 1.5rem !important;
    }

    /* Brand colours */
    :root {
        --brand: #2B6777;
        --brand-light: #52AB98;
        --bg: #F5F5F5;
        --card-bg: #FFFFFF;
        --text-dark: #1E1E1E;
        --text-muted: #888888;
        --red: #D32F2F;
    }

    /* ── Primary buttons (teal filled) ── */
    .stButton > button[kind="primary"] {
        background-color: var(--brand) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        width: 100%;
        transition: background-color 0.2s;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: var(--brand-light) !important;
    }

    /* ── Secondary buttons (case entries – look like text links) ── */
    .stButton > button[kind="secondary"] {
        background: transparent !important;
        color: var(--text-dark) !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0.2rem 0 !important;
        text-align: left !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        width: auto !important;r
    }
    .stButton > button[kind="secondary"]:hover {
        background: transparent !important;
        color: var(--brand) !important;
    }

    /* Social / outline buttons */
    .social-btn {
        display: inline-flex; align-items: center; justify-content: center; gap: 8px;
        border: 1.5px solid #ddd; border-radius: 25px;
        padding: 10px 0; width: 48%; text-align: center;
        font-size: 0.9rem; font-weight: 500; color: var(--text-dark);
        background: white; cursor: pointer;
    }
    .social-btn:hover {background: #f9f9f9;}
    .social-row {display: flex; gap: 4%; justify-content: center; margin: 0.5rem 0;}

    /* Divider */
    .or-divider {
        display: flex; align-items: center; gap: 12px;
        color: var(--text-muted); margin: 1rem 0; font-size: 0.85rem;
    }
    .or-divider::before, .or-divider::after {
        content: ""; flex: 1; height: 1px; background: #ddd;
    }

    /* Header bell icon */
    .header-bell {
        display: flex; align-items: center; justify-content: center;
        padding-top: 0.3rem;
    }
    .header-bell svg {width: 24px; height: 24px;}

    /* Avatar logout button – circle style for primary buttons inside columns */
    [data-testid="column"] .stButton > button[kind="primary"] {
        border-radius: 50% !important;
        width: 42px !important;
        height: 42px !important;
        min-width: 42px !important;
        max-width: 42px !important;
        min-height: 42px !important;
        padding: 0 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        background: var(--brand-light) !important;
    }
    [data-testid="column"] .stButton > button[kind="primary"]:hover {
        background: var(--brand) !important;
    }

    /* ── File uploader – smaller drag-and-drop text ── */
    .stFileUploader section {
        padding: 0.5rem !important;
    }
    .stFileUploader section > div {
        font-size: 0.7rem !important;
    }
    .stFileUploader small {
        font-size: 0.65rem !important;
    }
    .stFileUploader section button {
        font-size: 0.72rem !important;
        padding: 0.2rem 0.8rem !important;
    }

    /* Links */
    .link-text {color: var(--brand); font-weight: 600; text-decoration: none;}
    .muted {color: var(--text-muted); font-size: 0.82rem; text-align: center;}

    /* Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stDateInput > div > div > input {
        border-radius: 12px !important;
    }

    /* Symptom bubble */
    .symptom-bubble {
        background: var(--brand);
        color: white;
        border-radius: 16px;
        padding: 0.7rem 1rem;
        font-size: 0.88rem;
        line-height: 1.4;
        margin: 0.5rem 0 1rem 0;
        display: inline-block;
    }

    /* AI Guidance card (light - carer view) */
    .ai-card {
        background: #F0F4F5;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
    }
    /* AI Guidance card (dark - parent view) */
    .ai-card-dark {
        background: var(--brand);
        color: white;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
    }
    .ai-card-dark a {color: #FFD6D6; font-weight: 600;}
    .ai-card h4, .ai-card-dark h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        font-weight: 700;
    }
    .ai-card-dark h4 {color: white;}
    .ai-label {font-weight: 700; font-size: 0.88rem;}
    .ai-text {font-size: 0.85rem; color: #444; line-height: 1.5; margin-top: 0.5rem;}
    .ai-card-dark .ai-text {color: #E0E0E0;}

    /* Category tag */
    .cat-tag {
        display: inline-block;
        background: var(--brand);
        color: white;
        border-radius: 20px;
        padding: 3px 14px;
        font-size: 0.78rem;
        font-weight: 600;
    }

    /* Red flags */
    .red-flags-card {
        background: var(--card-bg);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .red-flag-title {
        color: var(--red);
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    .red-flag-item {
        display: flex; align-items: center; gap: 8px;
        font-size: 0.88rem; color: #333;
        padding: 4px 0; font-weight: 600;
    }
    .red-dot {
        width: 22px; height: 22px; border-radius: 50%;
        background: var(--red); color: white;
        display: inline-flex; align-items: center; justify-content: center;
        font-size: 0.7rem; font-weight: 700; flex-shrink: 0;
    }

    /* Submitted meta */
    .submitted-meta {
        font-size: 0.78rem;
        color: var(--text-muted);
        margin: -0.3rem 0 1rem 0;
    }

    /* Parent update card */
    .update-card {
        background: var(--card-bg);
        border-radius: 14px;
        padding: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin: 1rem 0;
    }
    .update-card h4 {margin: 0 0 4px 0; font-size: 1.05rem;}
    .update-card .update-time {
        font-size: 0.78rem; color: var(--text-muted);
        border-bottom: 1px solid #eee; padding-bottom: 8px; margin-bottom: 8px;
    }
    .update-desc {
        font-size: 0.88rem;
        color: #555;
        line-height: 1.5;
        margin: 0.5rem 0 0 0;
    }

    /* Symptom section card */
    .symptom-section-card {
        background: var(--card-bg);
        border-radius: 14px;
        padding: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin: 0.5rem 0 1rem 0;
    }

    /* Carer home title */
    .carer-home-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: var(--text-dark);
        margin-bottom: 1rem;
    }

    /* Disclaimer text */
    .disclaimer {
        color: var(--text-muted);
        font-size: 0.72rem;
        text-align: center;
        margin-top: 2rem;
        line-height: 1.4;
    }

    /* ── Recent-cases bordered container ── */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07) !important;
        border: none !important;
    }

    /* ── Hide back-nav trigger buttons (preceded by .hide-next-btn marker) ── */
    *:has(.hide-next-btn) + * .stButton {
        height: 0 !important;
        max-height: 0 !important;
        overflow: hidden !important;
        margin: 0 !important;
    }

    /* Case entry name button inside the recent-cases card – tighter spacing */
    [data-testid="stVerticalBlockBorderWrapper"] .stButton > button[kind="secondary"] {
        padding: 0 !important;
        margin: 0 !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
        height: auto !important;
        min-height: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ──────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "login"
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "display_name" not in st.session_state:
    st.session_state.display_name = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "centre_ids" not in st.session_state:
    st.session_state.centre_ids = []
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = None
if "selected_case_id" not in st.session_state:
    st.session_state.selected_case_id = None


# ── Helpers ─────────────────────────────────────────────────────────────
def navigate(page: str):
    st.session_state.page = page


def require_auth():
    if not st.session_state.user_id:
        navigate("login")
        st.rerun()


def do_logout():
    try:
        sb.auth.sign_out()
    except Exception:
        pass
    for key in ["user_id", "display_name", "role", "centre_ids", "access_token", "refresh_token"]:
        st.session_state[key] = None if key != "centre_ids" else []
    st.session_state.display_name = ""
    st.session_state.role = ""
    navigate("login")
    st.rerun()


def render_header():
    initial = (st.session_state.display_name or "U")[0].upper()
    bell_svg = '''<div class="header-bell"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg></div>'''
    spacer, bell_col, avatar_col = st.columns([6, 1, 1])
    with bell_col:
        st.markdown(bell_svg, unsafe_allow_html=True)
    with avatar_col:
        if st.button(initial, key="avatar_btn", type="primary"):
            do_logout()


def render_back_nav(label, button_key):
    """Render a clickable h2 back nav that triggers a hidden Streamlit button."""
    # Marker to hide the next button via CSS
    st.markdown('<span class="hide-next-btn"></span>', unsafe_allow_html=True)
    clicked = st.button(button_key, key=button_key)

    # Clickable h2 via components.html (supports onclick JS)
    components.html(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800&display=swap');
            .back-h2 {{
                font-family: 'Montserrat', sans-serif;
                font-size: 1.5rem;
                font-weight: 800;
                color: #1E1E1E;
                cursor: pointer;
                margin: 0;
                padding: 0;
                user-select: none;
            }}
            .back-h2:hover {{ color: #2B6777; }}
        </style>
        <h2 class="back-h2" onclick="
            const buttons = window.parent.document.querySelectorAll('button');
            for (const b of buttons) {{
                if (b.innerText.trim() === '{button_key}') {{ b.click(); break; }}
            }}
        ">‹ {label}</h2>
        """,
        height=45,
    )

    if clicked:
        navigate("home")
        st.rerun()


def format_date_display(date_str):
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d %B %Y")
    except Exception:
        return date_str or ""


def format_time_display(created_at):
    try:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        return f"Submitted {dt.strftime('%I:%M %p')}"
    except Exception:
        return ""


# ── Screen 1 – Login ───────────────────────────────────────────────────
def login_screen():
    st.markdown("<div style='height:3rem;'></div>", unsafe_allow_html=True)

    st.markdown(
        "<h2 style='text-align:center;font-weight:800;margin-bottom:0.2rem;'>Welcome Back!</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#888;margin-top:0;font-size:0.9rem;'>Sign in to your account to access</p>",
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    st.markdown(
        "<p style='font-size:0.85rem;font-weight:500;margin-bottom:2px;'>Email or Phone number</p>",
        unsafe_allow_html=True,
    )
    email = st.text_input("Email", placeholder="hello@gmail.com", label_visibility="collapsed")
    password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

    if st.button("Continue", type="primary"):
        if not email or not password:
            st.warning("Please enter both email and password.")
        else:
            try:
                res = sb.auth.sign_in_with_password({"email": email, "password": password})
                user = res.user
                session = res.session

                st.session_state.user_id = user.id
                st.session_state.access_token = session.access_token
                st.session_state.refresh_token = session.refresh_token

                profile = (
                    sb.table("users")
                    .select("display_name, role, centre_ids")
                    .eq("id", user.id)
                    .maybe_single()
                    .execute()
                )
                if profile.data:
                    st.session_state.display_name = profile.data.get("display_name", email)
                    st.session_state.role = profile.data.get("role", "")
                    st.session_state.centre_ids = profile.data.get("centre_ids", []) or []
                else:
                    st.session_state.display_name = email.split("@")[0].title()

                navigate("home")
                st.rerun()
            except Exception as e:
                error_msg = str(e)
                if "Invalid login credentials" in error_msg:
                    st.error("Invalid email or password. Please try again.")
                else:
                    st.error(f"Login failed: {error_msg}")

    st.markdown(
        "<p style='text-align:center;margin-top:0.5rem;font-size:0.85rem;'>"
        "<a href='#' class='link-text'>Forgot Password?</a></p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='muted' style='margin-top:0.25rem;'>"
        "Don't have an account? <a href='#' class='link-text'>Sign up</a></p>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='or-divider'>Or</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="social-row">
            <div class="social-btn">🍎</div>
            <div class="social-btn">
                <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
                     width="20" style="vertical-align:middle;">
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p class='disclaimer'>"
        "This guidance is not a medical diagnosis and<br>replace professional medical advice</p>",
        unsafe_allow_html=True,
    )


# ── Screen 2 – Carer Home ─────────────────────────────────────────────
def home_screen():
    require_auth()

    render_header()

    role = st.session_state.role

    if role == "parent":
        st.markdown("<div class='carer-home-title'>Parent Home</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='carer-home-title'>Carer Home</div>", unsafe_allow_html=True)

    # New Case button (only for non-parents)
    if role != "parent":
        if st.button("New Case  ➕", type="primary"):
            navigate("symptom_entry")
            st.rerun()

    st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)

    # Fetch cases
    try:
        user_id = st.session_state.user_id

        if role == "parent":
            children_res = (
                sb.table("children")
                .select("id, first_name, last_name")
                .contains("parent_ids", [user_id])
                .execute()
            )
            parent_children = children_res.data or []
            child_ids = [ch["id"] for ch in parent_children]
            child_map = {ch["id"]: f"{ch['first_name']} {ch['last_name']}" for ch in parent_children}

            if child_ids:
                cases_res = (
                    sb.table("cases")
                    .select("id, child_id, symptom_date, symptom_description, status, created_at, photo_url")
                    .in_("child_id", child_ids)
                    .order("created_at", desc=True)
                    .limit(20)
                    .execute()
                )
                cases = cases_res.data or []
            else:
                cases = []
        else:
            cases_res = (
                sb.table("cases")
                .select("id, child_id, symptom_date, symptom_description, status, created_at, photo_url")
                .eq("reported_by", user_id)
                .order("created_at", desc=True)
                .limit(20)
                .execute()
            )
            cases = cases_res.data or []

            child_ids_set = list({c["child_id"] for c in cases if c.get("child_id")})
            child_map = {}
            if child_ids_set:
                children_res = (
                    sb.table("children")
                    .select("id, first_name, last_name")
                    .in_("id", child_ids_set)
                    .execute()
                )
                for ch in children_res.data or []:
                    child_map[ch["id"]] = f"{ch['first_name']} {ch['last_name']}"

        if not cases:
            st.info("No cases yet. Tap **New Case** to get started." if role != "parent" else "No cases to review.")
        else:
            # Recent Cases inside a single bordered container (card)
            with st.container(border=True):
                st.markdown(
                    "<div style='font-size:1rem;font-weight:700;display:flex;align-items:center;gap:8px;'>"
                    "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#333' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><polyline points='12 6 12 12 16 14'/></svg>"
                    " Recent Cases</div>",
                    unsafe_allow_html=True,
                )

                for case in cases:
                    child_name = child_map.get(case.get("child_id"), "Unknown Child")
                    display_date = format_date_display(case.get("symptom_date", ""))
                    symptom = case.get("symptom_description", "")
                    photo_url = case.get("photo_url", "")
                    case_id = case["id"]

                    img_col, info_col = st.columns([1, 2.5])

                    with img_col:
                        if photo_url:
                            st.markdown(
                                f'<img src="{photo_url}" style="width:80px;height:80px;object-fit:cover;border-radius:14px;">',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                '<div style="width:80px;height:80px;border-radius:14px;background:#e8e8e8;"></div>',
                                unsafe_allow_html=True,
                            )

                    with info_col:
                        st.markdown(
                            f"<div style='font-size:0.75rem;color:#2B6777;font-weight:500;margin-bottom:1px;'>{display_date}</div>",
                            unsafe_allow_html=True,
                        )
                        if st.button(child_name, key=f"case_{case_id}"):
                            st.session_state.selected_case_id = case_id
                            if role == "parent":
                                navigate("acknowledge_report")
                            else:
                                navigate("case_details")
                            st.rerun()
                        st.markdown(
                            f"<div style='font-size:0.85rem;color:#555;margin-top:-0.6rem;'>{symptom}</div>",
                            unsafe_allow_html=True,
                        )

    except Exception as e:
        st.error(f"Failed to load cases: {e}")


# ── Screen 3 – Symptom Entry ──────────────────────────────────────────
def symptom_entry_screen():
    require_auth()

    # Block parent access
    if st.session_state.role == "parent":
        navigate("home")
        st.rerun()

    render_header()

    render_back_nav("Symptom Entry", "back_symptom")

    st.markdown(
        "<p style='color:#888;font-size:0.88rem;margin-top:-0.5rem;'>Describe what you're seeing</p>",
        unsafe_allow_html=True,
    )

    # Fetch children
    user_id = st.session_state.user_id
    children = []
    parent_map = {}

    try:
        children_res = (
            sb.table("children")
            .select("id, first_name, last_name, centre_id, parent_ids")
            .or_(f"carer_ids.cs.{{{user_id}}},parent_ids.cs.{{{user_id}}}")
            .execute()
        )
        children = children_res.data or []
    except Exception:
        pass

    if not children:
        try:
            centre_ids = st.session_state.centre_ids or []
            if centre_ids:
                children_res = (
                    sb.table("children")
                    .select("id, first_name, last_name, centre_id, parent_ids")
                    .in_("centre_id", centre_ids)
                    .execute()
                )
                children = children_res.data or []
        except Exception:
            pass

    if not children:
        try:
            children_res = (
                sb.table("children")
                .select("id, first_name, last_name, centre_id, parent_ids")
                .execute()
            )
            children = children_res.data or []
        except Exception as e:
            st.error(f"Failed to load children: {e}")

    if not children:
        st.warning("No children assigned to you.")
        return

    # Fetch parent names for "Parent Name - Child Name" format
    all_parent_ids = set()
    for ch in children:
        for pid in (ch.get("parent_ids") or []):
            all_parent_ids.add(pid)

    if all_parent_ids:
        try:
            parents_res = (
                sb.table("users")
                .select("id, display_name")
                .in_("id", list(all_parent_ids))
                .execute()
            )
            for p in parents_res.data or []:
                parent_map[p["id"]] = p["display_name"]
        except Exception:
            pass

    child_options = {}
    for ch in children:
        child_full = f"{ch['first_name']} {ch['last_name']}"
        parent_ids = ch.get("parent_ids") or []
        if parent_ids and parent_ids[0] in parent_map:
            label = f"{parent_map[parent_ids[0]]} - {child_full}"
        else:
            label = child_full
        child_options[label] = ch

    st.markdown("<p style='font-weight:700;font-size:0.95rem;margin-bottom:2px;'>Name Child</p>", unsafe_allow_html=True)
    selected_name = st.selectbox("Name Child", list(child_options.keys()), label_visibility="collapsed")
    selected_child = child_options[selected_name]

    st.markdown("<p style='font-weight:700;font-size:0.95rem;margin-bottom:2px;margin-top:1rem;'>Date</p>", unsafe_allow_html=True)
    entry_date = st.date_input("Date", value=date.today(), label_visibility="collapsed")

    st.markdown("<p style='font-weight:700;font-size:0.95rem;margin-bottom:2px;margin-top:1rem;'>Symptom Description</p>", unsafe_allow_html=True)
    symptoms = st.text_area(
        "Symptom Description",
        placeholder="e.g Darcy has a cough and seens tired.",
        height=100,
        label_visibility="collapsed",
    )

    st.markdown("<p style='font-weight:700;font-size:0.95rem;margin-bottom:2px;margin-top:1rem;'>Upload Photo (optional)</p>", unsafe_allow_html=True)
    photo = st.file_uploader("Upload Photo", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    if st.button("Submit", type="primary"):
        if not symptoms.strip():
            st.warning("Please describe the symptoms before submitting.")
        else:
            try:
                photo_url = None
                if photo:
                    try:
                        file_path = f"cases/{user_id}/{entry_date.isoformat()}_{photo.name}"
                        sb.storage.from_("case-photos").upload(
                            file_path,
                            photo.getvalue(),
                            {"content-type": photo.type},
                        )
                        photo_url = sb.storage.from_("case-photos").get_public_url(file_path)
                    except Exception:
                        pass

                case_data = {
                    "child_id": selected_child["id"],
                    "centre_id": selected_child.get("centre_id"),
                    "reported_by": user_id,
                    "symptom_date": entry_date.isoformat(),
                    "symptom_description": symptoms.strip(),
                    "status": "pending",
                }
                if photo_url:
                    case_data["photo_url"] = photo_url

                sb.table("cases").insert(case_data).execute()
                st.success(f"Case for {selected_child['first_name']} {selected_child['last_name']} saved!")
                navigate("home")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to save case: {e}")


# ── Screen 4 – Case Details (Carer view) ─────────────────────────────
def case_details_screen():
    require_auth()

    case_id = st.session_state.selected_case_id
    if not case_id:
        navigate("home")
        st.rerun()

    render_header()

    render_back_nav("Case Details", "back_case")

    # Fetch case
    try:
        case_res = (
            sb.table("cases")
            .select("*")
            .eq("id", case_id)
            .maybe_single()
            .execute()
        )
        case = case_res.data
    except Exception as e:
        st.error(f"Failed to load case: {e}")
        return

    if not case:
        st.warning("Case not found.")
        return

    # Fetch child name
    child_name = "Child"
    first_name = ""
    try:
        child_res = (
            sb.table("children")
            .select("first_name, last_name")
            .eq("id", case["child_id"])
            .maybe_single()
            .execute()
        )
        if child_res.data:
            first_name = child_res.data["first_name"]
            child_name = f"{first_name} {child_res.data['last_name']}"
    except Exception:
        pass

    # Submitted time
    submitted_str = format_time_display(case.get("created_at", ""))
    st.markdown(f"<p class='submitted-meta'>{submitted_str}</p>", unsafe_allow_html=True)

    # Symptoms section in card
    symptom_text = case.get("symptom_description", "")
    st.markdown(
        f"""
        <div class="symptom-section-card">
            <p style="font-weight:700;font-size:1.05rem;margin:0 0 0.5rem 0;">{first_name or child_name.split()[0]}'s Symptoms</p>
            <div class="symptom-bubble">{symptom_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # AI Guidance
    ai_recommendation = case.get("ai_recommendation", "")
    ai_category = case.get("ai_category", "")
    ai_guidance = case.get("ai_guidance", "")
    red_flags = case.get("red_flags", []) or []

    if ai_recommendation or ai_guidance:
        category_html = f'<span class="cat-tag">{ai_category}</span>' if ai_category else "—"
        st.markdown(
            f"""
            <div class="ai-card">
                <h4>AI Guidance</h4>
                <p style="margin:0;"><span class="ai-label">Recommended :</span>&nbsp; {ai_recommendation or "—"}</p>
                <p style="margin:6px 0;">
                    <span class="ai-label">Category :</span>&nbsp; {category_html}
                </p>
                <p class="ai-text">{ai_guidance}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="ai-card">
                <h4>AI Guidance</h4>
                <p class="ai-text" style="color:#888;">No AI guidance available for this case yet.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Red Flags
    if red_flags:
        flags_html = "".join(
            f'<div class="red-flag-item"><span class="red-dot">✓</span> {flag}</div>'
            for flag in red_flags
        )
        st.markdown(
            f"""
            <div class="red-flags-card">
                <div class="red-flag-title">🚩 Red Flags</div>
                {flags_html}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Screen 5 – Acknowledge Report (Parent view) ─────────────────────
def acknowledge_report_screen():
    require_auth()

    case_id = st.session_state.selected_case_id
    if not case_id:
        navigate("home")
        st.rerun()

    render_header()

    render_back_nav("Acknowledge Report", "back_ack")

    # Fetch case
    try:
        case_res = (
            sb.table("cases")
            .select("*")
            .eq("id", case_id)
            .maybe_single()
            .execute()
        )
        case = case_res.data
    except Exception as e:
        st.error(f"Failed to load case: {e}")
        return

    if not case:
        st.warning("Case not found.")
        return

    # Fetch child name
    child_name = "Child"
    first_name = ""
    try:
        child_res = (
            sb.table("children")
            .select("first_name, last_name")
            .eq("id", case["child_id"])
            .maybe_single()
            .execute()
        )
        if child_res.data:
            first_name = child_res.data["first_name"]
            child_name = f"{first_name} {child_res.data['last_name']}"
    except Exception:
        pass

    # Health Update card
    created = case.get("created_at", "")
    submitted_str = format_time_display(created)

    st.markdown(
        f"""
        <div class="update-card">
            <h4>{first_name or child_name.split()[0]}'s Health Update</h4>
            <div class="update-time">{submitted_str}</div>
            <p class="update-desc">
                Guidance has been provided for {first_name or child_name.split()[0]}'s
                symptoms. Please review the information and let us know you've seen it
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # AI Guidance (dark card)
    ai_guidance = case.get("ai_guidance", "")
    symptom_text = case.get("symptom_description", "")
    red_flags = case.get("red_flags", []) or []

    guidance_body = ai_guidance or symptom_text or "No guidance available yet."
    red_flag_note = ""
    if red_flags:
        red_flag_note = "Watch for any <a href='#'>Red Flags</a>."

    st.markdown(
        f"""
        <div class="ai-card-dark">
            <h4>AI Guidance</h4>
            <p class="ai-text">{guidance_body}</p>
            {f"<p class='ai-text' style='margin-top:0.5rem;'>{red_flag_note}</p>" if red_flag_note else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

    # Acknowledge button
    if st.button("Acknowledge", type="primary"):
        if not st.session_state.get("ack_checked"):
            st.warning("Please confirm you have read and understood this update.")
        else:
            try:
                sb.table("cases").update({
                    "acknowledged_by_parent": True,
                    "status": "acknowledged",
                }).eq("id", case_id).execute()
                st.success("Report acknowledged. Thank you!")
                navigate("home")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to acknowledge: {e}")

    acknowledged = st.checkbox("I have read and understood this update.")
    st.session_state["ack_checked"] = acknowledged


# ── Router ─────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "login":
    login_screen()
elif page == "home":
    home_screen()
elif page == "symptom_entry":
    symptom_entry_screen()
elif page == "case_details":
    case_details_screen()
elif page == "acknowledge_report":
    acknowledge_report_screen()
else:
    navigate("login")
    st.rerun()
