import streamlit as st
import pandas as pd
from utils.general import common_sidebar, session_sidebar, analysis_sidebar
from utils.db_handler import get_user_nutrition
from utils.db_handler import get_user_workout


def recommendations():
    # Recommendations Section
    if st.session_state.logged_in:
        st.subheader(":green[Personalized Recommendations]")
        common_sidebar()
        session_sidebar()
        analysis_sidebar()

        # Get current user data
        user_workout = get_user_workout(st.session_state.user["user_id"])
        user_nutrition = get_user_nutrition(st.session_state.user["user_id"])
        df_workout, df_nutrition = [], []
        if user_workout:
            df_workout = pd.DataFrame(user_workout)
            df_workout['date'] = pd.to_datetime(df_workout['date'])

        if user_nutrition:
            df_nutrition = pd.DataFrame(user_nutrition)
            df_nutrition['date'] = pd.to_datetime(df_nutrition['date'])

        # Basic recommendation logic
        if user_workout and user_nutrition:
            avg_calories_burned = df_workout['calories'].mean()
            avg_calories_consumed = df_nutrition['calories'].mean()

            if avg_calories_consumed > avg_calories_burned:
                st.write("It looks like you're consuming more calories than you’re burning. "
                         "Consider increasing your activity levels or adjusting your meal plan to stay on track.")
            elif avg_calories_burned > avg_calories_consumed:
                st.write("Great job! You're burning more calories than you're consuming. "
                         "Keep up the good work to reach your fitness goals faster.")
            else:
                st.write("You're balancing calories well. Maintain this balance for steady progress.")
        else:
            st.write("Log more workouts and meals to receive tailored recommendations.")

    else:
        st.write("Please log in to get recommendations.")
