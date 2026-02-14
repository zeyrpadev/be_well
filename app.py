import streamlit as st
from datetime import date, timedelta
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


@st.cache_resource
def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


sb = get_supabase_client()

# ── Global CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
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
    }

    /* Teal primary buttons */
    .stButton > button {
        background-color: var(--brand) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        width: 100%;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: var(--brand-light) !important;
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

    /* Case card */
    .case-card {
        background: var(--card-bg);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .case-card .date {font-size: 0.75rem; color: var(--text-muted);}
    .case-card .child {font-weight: 700; font-size: 1rem; margin: 2px 0;}
    .case-card .symptom {font-size: 0.85rem; color: #555;}

    /* Header bar */
    .header-bar {
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 0.5rem;
    }
    .header-bar .icons {display: flex; gap: 12px; align-items: center;}
    .avatar {
        width: 36px; height: 36px; border-radius: 50%;
        background: var(--brand-light); color: white;
        display: flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 0.9rem;
    }

    /* Back button */
    .back-link {
        font-size: 1.05rem; font-weight: 600; color: var(--brand);
        cursor: pointer; text-decoration: none;
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
    }

    /* AI Guidance card */
    .ai-card {
        background: #F0F4F5;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
    }
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
        color: #D32F2F;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    .red-flag-item {
        display: flex; align-items: center; gap: 8px;
        font-size: 0.88rem; color: #333;
        padding: 4px 0;
    }
    .red-dot {
        width: 20px; height: 20px; border-radius: 50%;
        background: #D32F2F; color: white;
        display: inline-flex; align-items: center; justify-content: center;
        font-size: 0.7rem; font-weight: 700; flex-shrink: 0;
    }

    /* Submitted meta */
    .submitted-meta {
        font-size: 0.78rem;
        color: var(--text-muted);
        margin: -0.3rem 0 1rem 0;
    }

    /* Parent update description */
    .update-desc {
        font-size: 0.88rem;
        color: #555;
        line-height: 1.5;
        margin: 0.5rem 0 1rem 0;
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
if "selected_case_id" not in st.session_state:
    st.session_state.selected_case_id = None


# ── Helpers ─────────────────────────────────────────────────────────────
def navigate(page: str):
    st.session_state.page = page


def require_auth():
    """Redirect to login if not authenticated."""
    if not st.session_state.user_id:
        navigate("login")
        st.rerun()


def do_logout():
    """Sign out of Supabase and clear session."""
    try:
        sb.auth.sign_out()
    except Exception:
        pass
    for key in ["user_id", "display_name", "role", "centre_ids", "access_token"]:
        st.session_state[key] = None if key != "centre_ids" else []
    st.session_state.display_name = ""
    st.session_state.role = ""
    navigate("login")
    st.rerun()


# ── Screen 1 – Login ───────────────────────────────────────────────────
def login_screen():
    st.markdown("<div style='text-align:center;margin-top:2rem;'>", unsafe_allow_html=True)
    st.markdown(
        "<span style='font-size:2.4rem;font-weight:800;color:#2B6777;'>Be</span>"
        "<span style='font-size:2.4rem;font-weight:800;color:#52AB98;'>Well</span>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## Welcome Back!")
    st.markdown(
        "<p style='color:#888;margin-top:-0.8rem;'>Log in to continue caring for your little ones.</p>",
        unsafe_allow_html=True,
    )

    email = st.text_input("Email", placeholder="you@example.com")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Continue"):
        if not email or not password:
            st.warning("Please enter both email and password.")
        else:
            try:
                res = sb.auth.sign_in_with_password({"email": email, "password": password})
                user = res.user
                session = res.session

                st.session_state.user_id = user.id
                st.session_state.access_token = session.access_token

                # Fetch user profile from users table
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
        "<p style='text-align:right;margin-top:-0.5rem;'>"
        "<a href='#' class='link-text' style='font-size:0.85rem;'>Forgot Password?</a></p>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='or-divider'>Or</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="social-row">
            <div class="social-btn">🍎&nbsp; Apple</div>
            <div class="social-btn">
                <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
                     width="18" style="vertical-align:middle;"> Google
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p class='muted' style='margin-top:1rem;'>"
        "Don't have an account? <a href='#' class='link-text'>Sign up</a></p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p class='muted' style='margin-top:2rem;font-size:0.72rem;'>"
        "By continuing you agree to our <a href='#' class='link-text'>Terms of Service</a> "
        "and <a href='#' class='link-text'>Privacy Policy</a>.</p>",
        unsafe_allow_html=True,
    )


# ── Screen 2 – Carer Home ─────────────────────────────────────────────
def home_screen():
    require_auth()

    initial = (st.session_state.display_name or "C")[0].upper()

    # Header with logout
    col1, col2, col3 = st.columns([6, 1, 1])
    with col1:
        st.markdown(
            "<div style='font-size:1.4rem;font-weight:800;color:#2B6777;'>BeWell</div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"<div class='avatar'>{initial}</div>",
            unsafe_allow_html=True,
        )
    with col3:
        if st.button("↩", help="Logout"):
            do_logout()

    st.markdown("### Carer Home")

    if st.button("＋  New Case"):
        navigate("symptom_entry")
        st.rerun()

    st.markdown("#### Recent Cases")

    # Fetch cases from Supabase
    try:
        user_id = st.session_state.user_id
        cases_res = (
            sb.table("cases")
            .select("id, child_id, symptom_date, symptom_description, status, created_at")
            .eq("reported_by", user_id)
            .order("created_at", desc=True)
            .limit(20)
            .execute()
        )
        cases = cases_res.data or []

        if not cases:
            st.info("No cases yet. Tap **New Case** to get started.")
        else:
            # Collect child IDs to fetch names
            child_ids = list({c["child_id"] for c in cases if c.get("child_id")})
            child_map = {}
            if child_ids:
                children_res = (
                    sb.table("children")
                    .select("id, first_name, last_name")
                    .in_("id", child_ids)
                    .execute()
                )
                for ch in children_res.data or []:
                    child_map[ch["id"]] = f"{ch['first_name']} {ch['last_name']}"

            for case in cases:
                child_name = child_map.get(case.get("child_id"), "Unknown Child")
                case_date = case.get("symptom_date", "")
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(case_date)
                    display_date = dt.strftime("%d %b %Y")
                except Exception:
                    display_date = case_date or ""
                symptom = case.get("symptom_description", "")

                st.markdown(
                    f"""
                    <div class="case-card">
                        <div class="date">{display_date}</div>
                        <div class="child">{child_name}</div>
                        <div class="symptom">{symptom}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                case_id = case["id"]
                if st.button("View details", key=f"case_{case_id}"):
                    st.session_state.selected_case_id = case_id
                    role = st.session_state.role
                    if role == "parent":
                        navigate("acknowledge_report")
                    else:
                        navigate("case_details")
                    st.rerun()
    except Exception as e:
        st.error(f"Failed to load cases: {e}")


# ── Screen 3 – Symptom Entry ──────────────────────────────────────────
def symptom_entry_screen():
    require_auth()

    if st.button("← Symptom Entry"):
        navigate("home")
        st.rerun()

    st.markdown("### New Symptom Entry")

    # Fetch children assigned to this carer
    user_id = st.session_state.user_id
    children = []
    try:
        children_res = (
            sb.table("children")
            .select("id, first_name, last_name, centre_id")
            .or_(f"carer_ids.cs.{{{user_id}}},parent_ids.cs.{{{user_id}}}")
            .execute()
        )
        children = children_res.data or []
    except Exception as e:
        st.error(f"Failed to load children: {e}")

    if not children:
        st.warning("No children assigned to you.")
        return

    child_options = {
        f"{ch['first_name']} {ch['last_name']}": ch for ch in children
    }
    selected_name = st.selectbox("Child Name", list(child_options.keys()))
    selected_child = child_options[selected_name]

    entry_date = st.date_input("Date", value=date.today())

    symptoms = st.text_area(
        "Symptom Description",
        placeholder="Describe the symptoms you have observed…",
        height=120,
    )

    photo = st.file_uploader("Upload Photo (optional)", type=["png", "jpg", "jpeg"])

    if st.button("Submit"):
        if not symptoms.strip():
            st.warning("Please describe the symptoms before submitting.")
        else:
            try:
                photo_url = None
                if photo:
                    # Upload photo to Supabase Storage
                    try:
                        file_path = f"cases/{user_id}/{entry_date.isoformat()}_{photo.name}"
                        sb.storage.from_("case-photos").upload(
                            file_path,
                            photo.getvalue(),
                            {"content-type": photo.type},
                        )
                        photo_url = sb.storage.from_("case-photos").get_public_url(file_path)
                    except Exception:
                        # Storage may not be configured; continue without photo
                        pass

                case_data = {
                    "child_id": selected_child["id"],
                    "centre_id": selected_child.get("centre_id"),
                    "reported_by": user_id,
                    "symptom_date": entry_date.isoformat(),
                    "symptom_description": symptoms.strip(),
                    "status": "open",
                }
                if photo_url:
                    case_data["photo_url"] = photo_url

                sb.table("cases").insert(case_data).execute()
                st.success(f"Case for {selected_name} saved!")
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

    # Header
    initial = (st.session_state.display_name or "C")[0].upper()
    col_back, col_spacer, col_avatar = st.columns([6, 2, 1])
    with col_back:
        if st.button("← Case Details"):
            navigate("home")
            st.rerun()
    with col_avatar:
        st.markdown(f"<div class='avatar'>{initial}</div>", unsafe_allow_html=True)

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
    created = case.get("created_at", "")
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
        submitted_str = f"Submitted {dt.strftime('%I:%M %p')}"
    except Exception:
        submitted_str = ""

    st.markdown(f"<p class='submitted-meta'>{submitted_str}</p>", unsafe_allow_html=True)

    # Symptoms section
    st.markdown(f"**{first_name or child_name.split()[0]}'s Symptoms**")
    symptom_text = case.get("symptom_description", "")
    st.markdown(
        f"<div class='symptom-bubble'>{symptom_text}</div>",
        unsafe_allow_html=True,
    )

    # AI Guidance
    ai_recommendation = case.get("ai_recommendation", "")
    ai_category = case.get("ai_category", "")
    ai_guidance = case.get("ai_guidance", "")
    red_flags = case.get("red_flags", []) or []

    if ai_recommendation or ai_guidance:
        st.markdown(
            f"""
            <div class="ai-card">
                <h4>AI Guidance</h4>
                <p style="margin:0;"><span class="ai-label">Recommended :</span> {ai_recommendation or "—"}</p>
                <p style="margin:6px 0;">
                    <span class="ai-label">Category :</span>
                    {"<span class='cat-tag'>" + ai_category + "</span>" if ai_category else "—"}
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
            f'<div class="red-flag-item"><span class="red-dot">✕</span> {flag}</div>'
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

    # Header
    initial = (st.session_state.display_name or "P")[0].upper()
    col_back, col_spacer, col_avatar = st.columns([6, 2, 1])
    with col_back:
        if st.button("← Acknowledge Report"):
            navigate("home")
            st.rerun()
    with col_avatar:
        st.markdown(f"<div class='avatar'>{initial}</div>", unsafe_allow_html=True)

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

    # Title & meta
    st.markdown(f"### {first_name or child_name.split()[0]}'s Health Update")

    created = case.get("created_at", "")
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
        submitted_str = f"Submitted {dt.strftime('%I:%M %p')}"
    except Exception:
        submitted_str = ""

    st.markdown(f"<p class='submitted-meta'>{submitted_str}</p>", unsafe_allow_html=True)

    st.markdown(
        f"<p class='update-desc'>Guidance has been provided for {first_name or child_name.split()[0]}'s "
        f"symptoms. Please review the information and let us know you've seen it.</p>",
        unsafe_allow_html=True,
    )

    # AI Guidance (dark card for parent view)
    ai_guidance = case.get("ai_guidance", "")
    symptom_text = case.get("symptom_description", "")
    red_flags = case.get("red_flags", []) or []

    guidance_body = ai_guidance or symptom_text or "No guidance available yet."
    red_flag_note = ""
    if red_flags:
        red_flag_note = f"Watch for any <a href='#'>Red Flags</a>."

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

    # Acknowledge checkbox + button
    acknowledged = st.checkbox("I have read and understood this update.")

    if st.button("Acknowledge"):
        if not acknowledged:
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
