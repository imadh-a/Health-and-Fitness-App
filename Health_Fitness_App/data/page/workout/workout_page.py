import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db_handler import get_user_workout
from utils.general import common_sidebar, workout_sidebar, session_sidebar


def workout():
    # Initialize workout data if it doesn't exist
    if 'workout' not in st.session_state:
        st.session_state.workout = {}

    # Workout Program Section (only visible when logged in)
    if st.session_state.logged_in:
        st.header(":green[Workout Program]")
        common_sidebar()
        workout_sidebar()
        session_sidebar()

        user_workout = get_user_workout(st.session_state.user["user_id"])
        if user_workout:
            df_workout = pd.DataFrame(user_workout)

            # Visualize calories burned per exercise as a bar chart
            st.plotly_chart(
                px.bar(df_workout, x="date", y="calories", color="exercise",
                       title="Calories Burned per Workout", labels={"date": "Date", "calories": "Calories Burned"})
            )

            # Display a table of logged workouts
            st.write(df_workout)

            # Calculate and show total calories burned
            total_calories_burned = df_workout['calories'].sum()
            st.write(f"**Total Calories Burned:** {total_calories_burned} kcal")

        else:
            st.info("No workouts logged yet. Log some workouts to start tracking your progress.")

    else:
        st.write("Please log in to view visualizations.")