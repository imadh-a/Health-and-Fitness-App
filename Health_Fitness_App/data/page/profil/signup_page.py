import datetime
import streamlit as st
from utils.general import is_valid_email
from utils.otp_handler import verify_password
from utils.db_handler import save_user, verify_duplicate_user
import time


def input_field(input_param, type):
    """Render an input field based on the type and store the value in session state."""
    if type == 'text':
        st.session_state[input_param] = st.text_input(input_param)
    elif type == 'number':
        st.session_state[input_param] = st.number_input(input_param, step=1)


def verifyOTP(otp_input):
    """Verify the OTP input by the user."""
    if otp_input == st.session_state['otp']:
        st.success("OTP verified successfully")
        time.sleep(1)
        st.session_state['verifying'] = False
        st.session_state['otp'] = ""
        save_user(st.session_state['email'], st.session_state['password'], st.session_state['extra_input_params'])
        st.session_state['page'] = 'login'
        st.rerun()
    else:
        st.error("Invalid OTP")


def signup_page():
    # Title of the app
    # st.set_page_config(page_title="Health and Fitness App", initial_sidebar_state="collapsed")
    st.title(":green[Health and Fitness App]")

    # Initialize session state for user profile if not already done
    if 'profile' not in st.session_state:
        st.session_state.profile = {}

    # Profile Management
    st.subheader("Create Account")
    with st.form(key="signup", clear_on_submit=True):
        name = st.text_input(":blue[name]", placeholder="Enter your name")
        email = st.text_input(":blue[Email]")
        password = st.text_input(":blue[Password]", placeholder="Enter your password", type='password')
        confirm_password = st.text_input(":blue[Confirm Password]", placeholder="Confirm your password", value="",
                                         type='password')
        age = st.number_input(":blue[age]", placeholder="Enter your age", min_value=0,
                              value=st.session_state.profile.get("age", 15))
        sex = st.selectbox(":blue[Select your sex]", ["Male", "Female", "Other"],
                           index=["Male", "Female", "Other"].index(st.session_state.profile.get("sex", "Male")))
        fitness_goal = st.text_input(":blue[fitness_goal", placeholder="What are your fitness goals?",
                                     value=st.session_state.profile.get("fitness_goal", ""))
        weight = st.number_input(":blue[weight]", placeholder="Enter your weight (kg)", min_value=0.0,
                                 value=st.session_state.profile.get("weight", 50.0))
        height = st.number_input(":blue[height]", placeholder="Enter your height (cm)", min_value=0.0,
                                 value=st.session_state.profile.get("height", 100.0))

        btn1, btn2, btn3, btn4, btn5 = st.columns(5)

        with btn3:
            submit_button = st.form_submit_button("Save profile")

    with st.sidebar:
        if st.button("Login"):
            st.session_state['page'] = 'login'
            st.rerun()

    # Save profile data
    if submit_button:
        # Check email
        if email and not is_valid_email(email):
            st.error("Please enter a valid email address")
        # Check if the user already exists
        if verify_duplicate_user(email):
            st.error("User already exists")
            time.sleep(1)
            st.rerun()
        # check password confirmation
        if not verify_password(password, confirm_password):
            st.error("Passwords do not match")
            time.sleep(1)
            st.rerun()

        if email and password and name and age and sex \
                and fitness_goal and weight and height:
            save_user(name, email, age, datetime.datetime.now(), sex, fitness_goal, weight, height, password)
            st.session_state['page'] = 'login'
            st.success("Profile created successfully")
            time.sleep(1)
            st.rerun()
        elif st.button("Register"):
            st.error("Please fill in all required fields")
            time.sleep(1)
