import streamlit as st
from utils.db_handler import add_diet
from utils.general import common_sidebar, nutrition_sidebar, session_sidebar


def add_nutrition():
    # Initialize a dictionary to store users' nutrition data if it doesn't exist
    if 'nutrition' not in st.session_state:
        st.session_state.nutrition = {}

    # Nutrition Tracking Section (only visible when logged in)
    if st.session_state.logged_in:
        st.header(":green[Nutrition/Diet Tracking]")
        common_sidebar()
        nutrition_sidebar()
        session_sidebar()

        # Form for entering nutrition data
        with st.form("nutrition_form"):
            st.subheader("Log Your Meals")

            # Fields for nutrition input
            food = st.text_input("Food Item")
            calories = st.number_input("Calories", min_value=0)
            protein = st.number_input("Protein (grams)", min_value=0.0)
            carbs = st.number_input("Carbohydrates (grams)", min_value=0.0)
            fat = st.number_input("Fat (grams)", min_value=0.0)
            date = st.date_input("Date")

            # Submit button
            submitted = st.form_submit_button("Add Meal")

            # On submit, save the meal data
            if submitted:
                add_diet(st.session_state.user["user_id"], food, calories, protein, carbs, fat, date)
                st.success("Meal added successfully!")
    else:
        st.write("Please log in to view activity visualizations.")
