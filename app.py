import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="Be Well", page_icon="💚", layout="centered")

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
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ──────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "login"

if "cases" not in st.session_state:
    st.session_state.cases = [
        {
            "date": (date.today() - timedelta(days=1)).strftime("%d %b %Y"),
            "child": "Darcy Smith",
            "parent": "Jane Smith",
            "symptom": "High temperature, sore throat, and mild rash on arms.",
        },
        {
            "date": (date.today() - timedelta(days=3)).strftime("%d %b %Y"),
            "child": "Lucy Adam",
            "parent": "Sarah Adam",
            "symptom": "Persistent cough and runny nose for two days.",
        },
    ]

if "user_email" not in st.session_state:
    st.session_state.user_email = ""


# ── Helpers ─────────────────────────────────────────────────────────────
def navigate(page: str):
    st.session_state.page = page


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

    email = st.text_input("Email or Phone", placeholder="you@example.com")

    if st.button("Continue"):
        st.session_state.user_email = email or "carer@bewell.app"
        navigate("home")
        st.rerun()

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
    # Header
    st.markdown(
        """
        <div class="header-bar">
            <div style="font-size:1.4rem;font-weight:800;color:#2B6777;">BeWell</div>
            <div class="icons">
                <span style="font-size:1.3rem;cursor:pointer;">🔔</span>
                <div class="avatar">C</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Carer Home")

    if st.button("＋  New Case"):
        navigate("symptom_entry")
        st.rerun()

    st.markdown("#### Recent Cases")

    if not st.session_state.cases:
        st.info("No cases yet. Tap **New Case** to get started.")
    else:
        for case in st.session_state.cases:
            st.markdown(
                f"""
                <div class="case-card">
                    <div class="date">{case['date']}</div>
                    <div class="child">{case['child']}</div>
                    <div class="symptom">{case['symptom']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ── Screen 3 – Symptom Entry ──────────────────────────────────────────
def symptom_entry_screen():
    if st.button("← Symptom Entry"):
        navigate("home")
        st.rerun()

    st.markdown("### New Symptom Entry")

    children = [
        "Jane Smith - Darcy Smith",
        "Sarah Adam - Lucy Adam",
        "Mark Taylor - Ollie Taylor",
    ]
    selected = st.selectbox("Name Child", children, index=0)

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
            parent_name, child_name = [s.strip() for s in selected.split("-")]
            new_case = {
                "date": entry_date.strftime("%d %b %Y"),
                "child": child_name,
                "parent": parent_name,
                "symptom": symptoms.strip(),
            }
            if photo:
                new_case["photo_name"] = photo.name
            st.session_state.cases.insert(0, new_case)
            st.success(f"Case for {child_name} saved!")
            navigate("home")
            st.rerun()


# ── Router ─────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "login":
    login_screen()
elif page == "home":
    home_screen()
elif page == "symptom_entry":
    symptom_entry_screen()
else:
    navigate("login")
    st.rerun()
