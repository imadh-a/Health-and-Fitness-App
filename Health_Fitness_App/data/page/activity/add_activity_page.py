import streamlit as st
import datetime
from utils.db_handler import save_activity
from utils.general import common_sidebar, session_sidebar, activity_sidebar


def add_activity():
    if st.session_state.logged_in:
        st.header(":green[Activity Tracking]")
        common_sidebar()
        activity_sidebar()
        session_sidebar()

        date = st.date_input("Date", datetime.date.today())
        steps = st.number_input("Steps Walked", min_value=0)
        distance = st.number_input("Distance Covered (km)", min_value=0.0)
        calories = st.number_input("Calories Burned", min_value=0)
        workout = st.text_area("Workout Description")

        if st.button("Save Activity"):
            save_activity(st.session_state.user["user_id"], date, steps, distance, calories, workout)
            st.success("Workout logged successfully!")
    else:
        st.write("Please log in to add activity.")
