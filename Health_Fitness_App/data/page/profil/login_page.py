import streamlit as st
from utils.db_handler import authenticate_user
from utils.general import is_valid_email


def login_page(guest_mode=False):
    with st.empty().container(border=True):
        col1, _, col2 = st.columns([10, 1, 10])

        with col1:
            st.write("")
            st.write("")
            # st.video("data/demo.mp4", autoplay=True, loop=True, muted=True)
            st.image("data/demo.png")

        with col2:
            st.title(":green[Login Page]")
            with st.form(key="login"):
                email = st.text_input(":blue[E-mail]")
                password = st.text_input(":blue[Password]", type="password")
                login_submit = st.form_submit_button(":green[Login]")

            if login_submit:
                if not (email and password):
                    st.error("Please provide email and password")

                elif email and not is_valid_email(email):
                    st.error("Please enter a valid email address")

                elif authenticate_user(email, password):
                    st.session_state['page'] = 'app'
                    st.rerun()

                else:
                    st.error("Invalid login credentials")

            bt1, btn2, btn3 = st.columns(3)
            with btn3:
                if st.button(":blue[Sign Up]"):
                    st.session_state['page'] = 'signup'
                    st.rerun()
