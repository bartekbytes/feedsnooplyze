import streamlit as st
from db import create_user, authenticate_user

def show():

    # -----------------------------------
    # Centered Layout
    # -----------------------------------
    left, center, right = st.columns([1, 2, 1])

    with center:
     
        st.markdown(
            """
            <h1 style="margin:0;">📰<span style="color:#000000;">feed</span><span style="color:#ff4b4b;">snoop</span><span style="color:#1f77b4;">lyze</span></h1>
            """,
            unsafe_allow_html=True
        )
        st.markdown("### feedsnooplyze - be a Well-Informed Person.")

        st.divider()

        st.markdown("""<h3><span style="color:red">Stop scrolling. Start knowing.</span></h3>""", unsafe_allow_html=True)
        st.markdown("""#### feedsnooplyze turns information overload into clarity.""")
        st.markdown("""#### It continuously gathers news from across the web, compares old vs. new content, extracts key insights, and delivers clean, concise summaries — always up to date.""")
        st.markdown("""#### It doesn't just collect information - It <u>understands change</u>.<br/>Be <u>ahead of the feed</u> - Be a WIP (Well-Informed Person).""", unsafe_allow_html=True)

        st.divider()

        # It crawls the web.
        # Hijacks RSS streams.
        # Diff-checks old vs. new.
        # Extracts signal from noise.

        # Auto-refresh every X minutes.
        # Zero scroll fatigue.
        # Only delta. Only relevance.

        # Turn raw data into situational awareness.

        # Become a WIP.
        # Well-Informed. Weaponized.


        # Information moves fast.
        # You move faster.

        # feedsnooplyze scrapes, compares, summarizes, and surfaces what changed — in real time.

        # No duplicates.
        # No recycled headlines.
        # Just fresh signal.

        # Stay updated.
        # Stay ahead.
        # Stay dangerous.        


        login_tab, create_account_tab = st.tabs(["Login", "Create Account"])

        # ------------------------------
        # LOGIN
        # ------------------------------
        with login_tab:

            st.subheader("Welcome back")
            st.text("Please provide your Email and password to log in.")

            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")

            st.write("")

            if st.button("Sign In", use_container_width=True):
                if not email or not password:
                    st.warning("Provide email or password")
                elif email and password:
                    if authenticate_user(email, password):
                        st.session_state["user"] = email
                        st.session_state["needs_customization"] = True
                        st.session_state["logged_in"] = True
                        st.success("Logged in successfully")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")

        # ------------------------------
        # REGISTER
        # ------------------------------
        with create_account_tab:

            st.subheader("Create your account")
            st.text("Please provide your Email and password to create a new account.")

            new_email = st.text_input("Email", key="register_email")
            new_password = st.text_input("Password", type="password", key="register_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

            st.write("")  # spacing

            if st.button("Create Account", use_container_width=True):
                if not new_email or not new_password:
                    st.warning("Please fill in all fields.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, message = create_user(new_email, new_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)