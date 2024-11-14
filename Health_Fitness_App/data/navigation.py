import streamlit as st

from page.activity.activity_log_page import activity_log
from page.activity.add_activity_page import add_activity
from page.diet.add_nutrition import add_nutrition
from page.workout.add_exercice_page import add_exercise_section
from page.workout.add_workout import add_workout
from page.analysis.analiysis_page import analysis
from page.assistance import assistance
from page.workout.choose_exercice_page import choose_exercice
from page.profil.login_page import login_page
from page.diet.nutrition_page import nutrition
from page.analysis.recommendations_page import recommendations
from page.profil.signup_page import signup_page
from page.app import app_page
from page.workout.workout_page import workout

from utils.init_session import init_session, reset_session

init_session()
# Initialize session state for user accounts if not already done
if 'users' not in st.session_state:
    st.session_state.users = {}  # A dictionary to store user data, e.g., {"username": {"password": "password",
    # "profile": {...}}}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

st.session_state['extra_input_params'] = {
}

for input_param in st.session_state['extra_input_params'].keys():
    if input_param not in st.session_state:
        st.session_state[input_param] = None

if st.session_state.logged_in:
    if st.session_state['page'] == 'add_activity':
        add_activity()
    elif st.session_state['page'] == 'activity_log':
        activity_log()
    elif st.session_state['page'] == 'nutrition':
        nutrition()
    elif st.session_state['page'] == 'add_nutrition':
        add_nutrition()
    elif st.session_state['page'] == 'workout':
        workout()
    elif st.session_state['page'] == 'add_workout':
        add_workout()
    elif st.session_state['page'] == 'choose_exercice':
        choose_exercice()
    elif st.session_state['page'] == 'analysis':
        analysis()
    elif st.session_state['page'] == 'recommendations':
        recommendations()
    elif st.session_state['page'] == 'assistance':
        assistance()
    elif st.session_state['page'] == 'add_exercice':
        add_exercise_section()
    else:
        app_page()
else:
    if st.session_state['page'] == 'login':
        reset_session()
        login_page(guest_mode=True)
    elif st.session_state['page'] == 'signup':
        signup_page()
