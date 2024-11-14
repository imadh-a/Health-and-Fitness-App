import streamlit as st
import pandas as pd
import plotly.express as px
from utils.general import common_sidebar, session_sidebar, analysis_sidebar
from utils.db_handler import get_user_nutrition
from utils.db_handler import get_user_workout


def analysis():
    # Progress Analytics Section
    if st.session_state.logged_in:
        st.header(":green[Progress Analytics and Recommendations]")
        common_sidebar()
        session_sidebar()
        analysis_sidebar()

        # Get current user data
        user_workout = get_user_workout(st.session_state.user["user_id"])
        user_nutrition = get_user_nutrition(st.session_state.user["user_id"])

        if user_workout or user_nutrition:
            st.subheader("Your Activity and Nutrition Progress")

            # Prepare workout and nutrition data for visualization
            df_workout, df_nutrition = [], []
            if user_workout:
                df_workout = pd.DataFrame(user_workout)
                df_workout['date'] = pd.to_datetime(df_workout['date'])

                # Calories Burned Over Time
                st.write("### Calories Burned Over Time")
                st.plotly_chart(
                    px.line(df_workout, x="date", y="calories", title="Calories Burned Over Time",
                            labels={"date": "Date", "calories": "Calories Burned"})
                )

            if user_nutrition:
                df_nutrition = pd.DataFrame(user_nutrition)
                df_nutrition['date'] = pd.to_datetime(df_nutrition['date'])

                # Calories Consumed Over Time
                st.write("### Calories Consumed Over Time")
                st.plotly_chart(
                    px.line(df_nutrition, x="date", y="calories", title="Calories Consumed Over Time",
                            labels={"date": "Date", "calories": "Calories Consumed"})
                )

            # Comparison of calories consumed vs. calories burned
            if user_workout and user_nutrition:
                merged_data = pd.merge(df_workout[['date', 'calories']], df_nutrition[['date', 'calories']],
                                       on='date', how='outer', suffixes=('_burned', '_consumed')).fillna(0)

                st.write("### Calories Consumed vs. Burned")
                st.plotly_chart(
                    px.bar(merged_data, x="date", y=["calories_burned", "calories_consumed"],
                           title="Calories Consumed vs. Burned Over Time", labels={"date": "Date"})
                )
        else:
            st.info("No data available for analytics. Log workouts and meals to start tracking your progress.")
    else:
        st.info("No workouts logged yet. Log some workouts to start tracking your progress.")
