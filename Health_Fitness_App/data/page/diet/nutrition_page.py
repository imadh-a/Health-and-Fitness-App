import streamlit as st
import pandas as pd
import plotly.express as px
from utils.general import common_sidebar, nutrition_sidebar, session_sidebar
from utils.db_handler import get_user_nutrition


def nutrition():
    if st.session_state.logged_in:
        # Display Nutrition Data
        st.subheader(":green[Your Nutrition Log]")
        common_sidebar()
        nutrition_sidebar()
        session_sidebar()

        user_nutrition = get_user_nutrition(st.session_state.user["user_id"])
        if user_nutrition:
            df_nutrition = pd.DataFrame(user_nutrition)

            # Calculate and show total calories and macronutrients
            total_calories = df_nutrition['calories'].sum()
            total_protein = df_nutrition['protein'].sum()
            total_carbs = df_nutrition['carbs'].sum()
            total_fat = df_nutrition['fat'].sum()

            # Visualize the nutrient distribution as a pie chart
            nutrient_totals = pd.DataFrame({
                "Nutrient": ["Protein", "Carbohydrates", "Fat"],
                "Amount": [total_protein, total_carbs, total_fat]
            })
            st.plotly_chart(px.pie(nutrient_totals, names="Nutrient", values="Amount", title="Macronutrient Breakdown"))

            # Display a table of the logged meals
            st.write(df_nutrition)
            st.write(f"**Total Calories:** {total_calories} kcal")
            st.write(f"**Total Protein:** {total_protein} grams")
            st.write(f"**Total Carbohydrates:** {total_carbs} grams")
            st.write(f"**Total Fat:** {total_fat} grams")
        else:
            st.info("No meals logged yet. Add some meals to start tracking your nutrition.")
    else:
        st.write("Please log in to view visualizations.")
