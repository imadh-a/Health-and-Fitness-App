from utils.db_handler import get_exercise_plan
from utils.general import common_sidebar, workout_sidebar, session_sidebar
import streamlit as st
from utils.workout_utils import get_fitness_goal, get_workout_plan


def choose_exercice():
    # Workout Program Section (only visible when logged in)
    if st.session_state.logged_in:
        st.header(":green[Choose Exercice]")
        common_sidebar()
        workout_sidebar()
        session_sidebar()

        # Workout Plan Generator based on goals
        plans = get_exercise_plan(st.session_state.user["user_id"])
        fitness_goal = st.selectbox(
            "Choose Your Fitness Goal",
            plans
        )

        st.write(f"**Selected Goal:** {fitness_goal}")

        # Display a generated workout plan based on the goal
        if plans:
            workout_plan = plans[fitness_goal]
            if workout_plan:
                st.subheader("Your Workout Plan")
                for exercise in workout_plan:
                    st.write("- " + exercise)
    else:
        st.info("Please login.")
