import streamlit as st
from utils.db_handler import log_workout
from utils.general import common_sidebar, workout_sidebar, session_sidebar


def add_workout():
    if st.session_state.logged_in:
        st.header(":green[Add Workout]")
        common_sidebar()
        workout_sidebar()
        session_sidebar()

        # Form to log completed workouts and calories burned
        with st.form("workout_form"):
            st.subheader("Log Your Completed Workout")

            exercise_done = st.text_input("Exercise")
            calories_burned = st.number_input("Calories Burned", min_value=0)
            workout_date = st.date_input("Date")

            # Submit button
            workout_submitted = st.form_submit_button("Log Workout")

            # On submit, save the workout data
            if workout_submitted:
                log_workout(st.session_state.user["user_id"], exercise_done, calories_burned, workout_date)
                st.success("Workout logged successfully!")

    else:
        st.write("Please log in to add workout.")