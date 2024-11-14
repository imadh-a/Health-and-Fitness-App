import streamlit as st
from utils.db_handler import get_user_activities
from utils.general import common_sidebar, session_sidebar, activity_sidebar


def activity_log():
    if st.session_state.logged_in:
        common_sidebar()
        activity_sidebar()
        session_sidebar()
        # Display all activities for the current user
        user_activities = get_user_activities(st.session_state.user["user_id"])
        if user_activities:
            st.subheader(":green[Activity Log]")
            for activity in user_activities:
                st.write(f"Date: {activity['date']}")
                st.write(f"Steps: {activity['steps']}")
                st.write(f"Distance: {activity['distance']} km")
                st.write(f"Calories: {activity['calories']}")
                st.write(f"Workout: {activity['workout']}")
                st.write("---")
        else:
            st.info("No activity data to display. Please add some activities first.")
    else:
        st.write("Please log in to view activity visualizations.")

