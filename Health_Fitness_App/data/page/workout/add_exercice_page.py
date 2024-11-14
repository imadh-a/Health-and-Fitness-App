import streamlit as st

from utils.db_handler import add_exercise_to_plan, get_exercise_plan
from utils.general import common_sidebar, workout_sidebar, session_sidebar


def add_exercise_section():
    if st.session_state.logged_in:
        st.subheader(":green[Exercise Plan]")
        common_sidebar()
        workout_sidebar()
        session_sidebar()

        # Form to add exercises to plan
        with st.form("exercise_plan_form", clear_on_submit=True):
            plan_name = st.text_input("Plan Name")
            exercise_name = st.text_input("Exercise Name")
            duration = st.number_input("Duration", min_value=0)

            add_exercise = st.form_submit_button("Add Exercise")

            # When form is submitted, add exercise to plan
            if add_exercise:
                add_exercise_to_plan(st.session_state.user["user_id"], plan_name, f"{exercise_name} ({duration}) ")
                st.success("Exercise added to plan!")

        # Display user's exercise plan
        # st.write("### Current Exercise Plan")
        # exercise_plan = get_exercise_plan(st.session_state.user["user_id"])
        # if exercise_plan:
        #     for exercise in exercise_plan:
        #         st.write(f"**Exercise:** {exercise[0]}")
        #         st.write(f"**Description:** {exercise[1]}")
        #         st.write("---")  # Separator
        # else:
        #     st.info("No exercises added to plan yet.")
    else:
        st.write("Please log in to add workout.")
