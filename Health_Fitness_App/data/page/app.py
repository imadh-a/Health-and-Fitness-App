import streamlit as st
from utils.db_handler import get_user_activities
from utils.general import common_sidebar, activity_sidebar, session_sidebar
import pandas as pd

st.set_page_config(page_title="Health and Fitness App", initial_sidebar_state="expanded")


def app_page():
    # Activity Tracking Section (only visible when logged in)
    if st.session_state.logged_in:
        common_sidebar()
        activity_sidebar()
        session_sidebar()

        # Visualization Section (only visible when logged in)
        st.header(":green[Activity Visualization]")

        # Load user's activities
        user_activities = get_user_activities(st.session_state.user["user_id"])

        if user_activities:
            # Convert activities to a DataFrame for easier manipulation and visualization
            df = pd.DataFrame(user_activities)

            # Convert date column to datetime if not already
            df['date'] = pd.to_datetime(df['date'])

            # Visualize Steps Over Time
            st.subheader("Steps Over Time")
            st.line_chart(df.set_index('date')['steps'])

            # Visualize Distance Covered Over Time
            st.subheader("Distance Covered Over Time (km)")
            st.bar_chart(df.set_index('date')['distance'])

            # Visualize Calories Burned Over Time
            st.subheader("Calories Burned Over Time")
            st.area_chart(df.set_index('date')['calories'])

            # Optional: Pie Chart of Total Activity Types
            st.subheader("Total Steps, Distance, and Calories")
            total_steps = df['steps'].sum()
            total_distance = df['distance'].sum()
            total_calories = df['calories'].sum()
            totals = pd.DataFrame({
                'Activity': ['Steps', 'Distance (km)', 'Calories'],
                'Total': [total_steps, total_distance, total_calories]
            })
            st.write(totals)
        else:
            st.info("No activity data to display. Please add some activities first.")
    else:
        st.write("Please log in to view activity visualizations.")
