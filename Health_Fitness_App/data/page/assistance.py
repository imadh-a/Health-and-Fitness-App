import streamlit as st
from openai.types.chat import ChatCompletionMessage

from utils.db_handler import get_user_activities, get_user_nutrition, get_user_workout
from utils.general import get_openai_client, common_sidebar, session_sidebar

import openai


def assistance():
    # AI-Powered Assistance Section
    if st.session_state.logged_in:
        st.header("AI-Powered Fitness Assistance")
        common_sidebar()
        session_sidebar()

        st.write(
            "Ask any question related to fitness, nutrition, or health, and get guidance based on your goals and "
            "progress."
        )

        # Text input for user question
        user_question = st.text_input("Your Question:", placeholder="e.g., What's the best diet for muscle gain?")

        client = get_openai_client()
        if st.button("Get Advice") and user_question:
            with st.spinner("Getting advice..."):
                # Call OpenAI API
                try:
                    # Customizing prompt based on user profile data
                    prompt = (f"User profile: {st.session_state.user}. "
                              f"Based on this profile and recent activity data, please advise on: {user_question} "
                              f"and {get_user_activities(st.session_state.user['user_id'])} ; "
                              f"also diet : {get_user_nutrition(st.session_state.user['user_id'])} "
                              f"and finally these workout {get_user_workout(st.session_state.user['user_id'])}")

                    response = completion = client.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": prompt}
                        ])

                    # Display AI response
                    answer = response.choices[0].message.content
                    st.write("**AI Advice:**", answer)
                except Exception as e:
                    st.error(f"Error fetching AI response: {e}")
    else:
        st.write("Please log in to get assistance.")
