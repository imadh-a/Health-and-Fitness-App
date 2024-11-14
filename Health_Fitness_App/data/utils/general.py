import streamlit as st
import openai
import re
from utils.db_handler import logout_user
from utils.init_session import reset_session
import os
from dotenv import load_dotenv

load_dotenv()


def is_valid_email(email):
    """Check if the provided email is valid using regex."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


def common_sidebar():
    with st.sidebar:
        st.sidebar.title(f"Welcome {st.session_state.user['name']}")
        if st.button("Logout"):
            reset_session()
            logout_user()
            st.rerun()
        if st.button("Dashboard"):
            st.session_state['page'] = 'app'
            st.rerun()


def not_subpage_of(page):
    return page not in st.session_state['page']


def session_sidebar():
    with st.sidebar:
        if not_subpage_of('nutrition') and st.button("Nutrition/Diet"):
            st.session_state['page'] = 'nutrition'
            st.rerun()
        if not_subpage_of('workout') and st.button("Workout"):
            st.session_state['page'] = 'workout'
            st.rerun()
        if not_subpage_of('analysis') and st.button("Analysis/Recommendations"):
            st.session_state['page'] = 'analysis'
            st.rerun()
        if st.button("Assistance"):
            st.session_state['page'] = 'assistance'
            st.rerun()


def nutrition_sidebar():
    with st.sidebar:
        if st.button("Nutrition/Diet"):
            st.session_state['page'] = 'nutrition'
            st.rerun()
        if st.button("Add Nutrition/Diet"):
            st.session_state['page'] = 'add_nutrition'
            st.rerun()


def activity_sidebar():
    with st.sidebar:
        if st.button("Add activity"):
            st.session_state['page'] = 'add_activity'
            st.rerun()
        if st.button("Activities logs"):
            st.session_state['page'] = 'activity_log'
            st.rerun()


def workout_sidebar():
    with st.sidebar:
        if st.button("Workout Dashboard"):
            st.session_state['page'] = 'workout'
            st.rerun()
        if st.button("Log workout"):
            st.session_state['page'] = 'add_workout'
            st.rerun()
        if st.button("Choose Exercice"):
            st.session_state['page'] = 'choose_exercice'
            st.rerun()
        if st.button("Add Exercice"):
            st.session_state['page'] = 'add_exercice'
            st.rerun()


def analysis_sidebar():
    with st.sidebar:
        if st.button("Analysis"):
            st.session_state['page'] = 'analysis'
            st.rerun()
        if st.button("Recommendations"):
            st.session_state['page'] = 'recommendations'
            st.rerun()


def get_openai_client():
    openai.api_key = os.getenv('OPENAI_API_KEY')

    completion = openai.chat.completions
    return completion

    # return OpenAI(
    #     api_key=os.getenv('OPENAI_API_KEY')
    # )
