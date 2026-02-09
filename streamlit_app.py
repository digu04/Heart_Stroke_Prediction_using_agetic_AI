# =============================================================
# streamlit_app.py — FINAL VERSION WITH SIDEBAR + NEXT/BACK
# =============================================================

import streamlit as st

from agents.pipeline import (
    process_free_text_input,
    run_full_pipeline,
    run_feedback_agent,
)

from agents.user_manager import register_user, load_users
from agents.history_manager import load_history


# -------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------
st.set_page_config(
    page_title="Heart Disease Prediction - Agentic AI",
    page_icon="❤️",
    layout="wide"
)

# -------------------------------------------------------------
# CSS (Sky Blue Theme + Floating Navigation Buttons)
# -------------------------------------------------------------
st.markdown("""
<style>

body { background-color: #F7FBFF; }

/* Header */
.app-header {
    background: linear-gradient(90deg, #A7D8FF, #44AFFF);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 25px;
}
.app-header h1 {
    color: white;
    font-size: 34px;
    font-weight: 800;
    margin: 0;
}

/* Card */
.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #DDEBFF;
    box-shadow: 0 4px 14px rgba(80,150,255,0.15);
    margin-bottom: 30px;
}

/* Chat box */
.chat-box {
    background: #FFFFFF;
    border: 1px solid #DDEBFF;
    padding: 20px;
    height: 380px;
    overflow-y: auto;
    border-radius: 15px;
}
.user-msg {
    background: #A7D8FF;
    padding: 12px 15px;
    border-radius: 12px;
    margin: 8px 0;
    margin-left: auto;
    max-width: 75%;
}
.ai-msg {
    background: #E9F5FF;
    padding: 12px 15px;
    border-radius: 12px;
    margin: 8px 0;
    margin-right: auto;
    max-width: 75%;
}

/* Floating Nav Buttons */
.nav-next {
    position: fixed;
    right: 40px;
    bottom: 40px;
    background-color: #4DA8FF;
    color: white;
    padding: 16px 26px;
    border-radius: 50px;
    font-size: 18px;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    z-index: 9999;
}
.nav-back {
    position: fixed;
    left: 40px;
    bottom: 40px;
    background-color: #A7D8FF;
    color: white;
    padding: 16px 26px;
    border-radius: 50px;
    font-size: 18px;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    z-index: 9999;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "context" not in st.session_state:
    st.session_state.context = None

if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

if "reasoning" not in st.session_state:
    st.session_state.reasoning = None

if "lifestyle" not in st.session_state:
    st.session_state.lifestyle = None

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "risk" not in st.session_state:
    st.session_state.risk = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_page" not in st.session_state:
    st.session_state.current_page = "Register"


# -------------------------------------------------------------
# PAGE ORDER
# -------------------------------------------------------------
order = ["Register", "Input", "Results", "Chat", "History"]


def next_page():
    idx = order.index(st.session_state.current_page)
    if idx < len(order) - 1:
        st.session_state.current_page = order[idx + 1]


def prev_page():
    idx = order.index(st.session_state.current_page)
    if idx > 0:
        st.session_state.current_page = order[idx - 1]


# -------------------------------------------------------------
# SIDEBAR NAVIGATION (Instant Switch)
# -------------------------------------------------------------
with st.sidebar:
    st.subheader("☰ Navigation")

    selected = st.radio(
        "Go to:",
        order,
        index=order.index(st.session_state.current_page),
        key="sidebar_nav"
    )

    # Sync state
    st.session_state.current_page = selected


# -------------------------------------------------------------
# HEADER
# -------------------------------------------------------------
st.markdown("""
<div class="app-header">
    <h1>Heart Disease Prediction App</h1>
</div>
""", unsafe_allow_html=True)


# ====================================================================
# PAGE 1 — REGISTER
# ====================================================================
if st.session_state.current_page == "Register":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("👤 Register or Continue")

    users = load_users()

    mode = st.radio("Choose:", ["New User", "Existing User"], key="reg_mode")

    # Existing User
    if mode == "Existing User":
        if users:
            emails = [u["email"] for u in users]
            selected = st.selectbox("Select User", emails, key="exist_user")

            if st.button("Continue"):
                for u in users:
                    if u["email"] == selected:
                        st.session_state.user = u
                        st.success(f"Welcome back, {u['name']}!")
                        next_page()
                        st.stop()
        else:
            st.info("No users registered yet.")

    # New User Registration
    else:
        name = st.text_input("Full Name", key="new_name")
        email = st.text_input("Email", key="new_email")
        mobile = st.text_input("Mobile Number", key="new_mobile")

        if st.button("Register New User"):
            ok, user = register_user(name, email, mobile)
            if ok:
                st.session_state.user = user
                st.success("Registration Successful!")
                next_page()
            else:
                st.error(user)

    st.markdown('</div>', unsafe_allow_html=True)


# ====================================================================
# PAGE 2 — INPUT
# ====================================================================
elif st.session_state.current_page == "Input":

    if st.session_state.user is None:
        st.warning("Please register first.")
        st.stop()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📝 Enter Your Details")

    mode = st.radio("Input Type:", ["Form Input", "Free Text"], key="input_type")

    # Form Input
    if mode == "Form Input":
        with st.form("form_data"):
            age = st.number_input("Age", 1, 120)
            sex = st.selectbox("Sex", ["M", "F"])
            cp = st.selectbox("Chest Pain", ["ATA", "NAP", "TA"])
            bp = st.number_input("Resting BP", 0, 250)
            chol = st.number_input("Cholesterol", 0, 600)
            fbs = st.selectbox("Fasting BS >120?", ["0", "1"])
            ecg = st.selectbox("Resting ECG", ["Normal", "ST"])
            maxhr = st.number_input("Max HR", 0, 250)
            exang = st.selectbox("Exercise Angina", ["N", "Y"])
            old = st.number_input("Oldpeak", 0.0, 10.0, step=0.1)
            slope = st.selectbox("ST Slope", ["Up", "Flat"])

            submit = st.form_submit_button("🚀 Predict")

        if submit:
            data = {
                "Age": age, "Sex": sex, "ChestPainType": cp,
                "RestingBP": bp, "Cholesterol": chol, "FastingBS": fbs,
                "RestingECG": ecg, "MaxHR": maxhr,
                "ExerciseAngina": exang, "Oldpeak": old, "ST_Slope": slope
            }

            ctx, pdf = run_full_pipeline(data, user_info=st.session_state.user)

            st.session_state.context = ctx
            st.session_state.pdf_path = pdf
            st.session_state.prediction = ctx["prediction"]
            st.session_state.risk = ctx["risk"]
            st.session_state.reasoning = ctx["reasoning"]
            st.session_state.lifestyle = ctx["lifestyle"]
            st.session_state.chat_history = []

            next_page()

    # Free Text
    else:
        text = st.text_area("Describe your symptoms")

        if st.button("Analyze & Predict"):
            extracted = process_free_text_input(text)
            st.json(extracted)

            if "error" not in extracted:
                ctx, pdf = run_full_pipeline(extracted, user_info=st.session_state.user)

                st.session_state.context = ctx
                st.session_state.pdf_path = pdf
                st.session_state.prediction = ctx["prediction"]
                st.session_state.risk = ctx["risk"]
                st.session_state.reasoning = ctx["reasoning"]
                st.session_state.lifestyle = ctx["lifestyle"]
                st.session_state.chat_history = []

                next_page()

    st.markdown('</div>', unsafe_allow_html=True)


# ====================================================================
# PAGE 3 — RESULTS
# ====================================================================
elif st.session_state.current_page == "Results":

    ctx = st.session_state.context

    if ctx is None:
        st.warning("Please complete prediction first.")
        st.stop()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Prediction Results")

    st.write(f"**Risk:** {ctx['risk']:.2f}%")
    st.write(f"**Prediction:** {'High Risk ⚠️' if ctx['prediction'] == 1 else 'Low Risk ✔️'}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧠 Medical Interpretation")
    st.write(ctx["reasoning"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🥗 Lifestyle Recommendations")
    st.write(ctx["lifestyle"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.download_button(
        "📥 Download Report",
        open(st.session_state.pdf_path, "rb").read(),
        "Heart_Report.pdf",
        mime="application/pdf",
        key="pdf_download"
    )


# ====================================================================
# PAGE 4 — CHAT
# ====================================================================
elif st.session_state.current_page == "Chat":

    if st.session_state.context is None:
        st.warning("Please run a prediction first.")
        st.stop()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💬 Ask Follow-Up Questions")

    msg = st.text_input("Ask something")

    if st.button("Send"):
        reply = run_feedback_agent(msg, st.session_state.context)
        st.session_state.chat_history.append(("You", msg))
        st.session_state.chat_history.append(("AI", reply))

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chat-box">', unsafe_allow_html=True)

    for sender, text in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f'<div class="user-msg">{text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-msg">{text}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ====================================================================
# PAGE 5 — HISTORY
# ====================================================================
elif st.session_state.current_page == "History":

    st.subheader("📚 Your Prediction History")

    hist = load_history()

    # --- CLEAR HISTORY BUTTON ---
    if st.button("🗑 Clear Entire History", key="clear_history_btn"):
        from agents.history_manager import clear_history
        clear_history()
        st.success("History cleared successfully!")
        st.rerun()

    if not hist:
        st.info("No records found.")
    else:
        for i, entry in enumerate(hist):

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write(f"### 🕒 {entry['timestamp']}")
            st.write(f"**Risk:** {entry['risk']}%")
            st.write(
                f"**Prediction:** {'High Risk ⚠️' if entry['prediction']==1 else 'Low Risk ✔️'}"
            )

            with st.expander("Health Features"):
                st.json(entry["features"])

            with st.expander("Medical Interpretation"):
                st.write(entry["reasoning"])

            with st.expander("Lifestyle Advice"):
                st.write(entry["lifestyle"])

            safe_ts = entry["timestamp"].replace(" ", "_").replace(":", "-")
            key = f"hist_dl_{safe_ts}_{i}"

            st.download_button(
                "📄 Download Report",
                open(entry["pdf_path"], "rb").read(),
                f"Report_{safe_ts}.pdf",
                mime="application/pdf",
                key=key
            )

            st.markdown('</div>', unsafe_allow_html=True)

# ====================================================================
# SIMPLE STREAMLIT NAVIGATION BUTTONS (NO JS, NO DOUBLE CLICK)
# ====================================================================

page_index = order.index(st.session_state.current_page)

# BACK button
if page_index > 0:
    if st.button("⬅ Back", key="nav_back"):
        prev_page()
        st.rerun()

# NEXT button
if page_index < len(order) - 1:
    if st.button("Next ➡", key="nav_next"):
        next_page()
        st.rerun()



