import streamlit as st


all_plan = {
    "Weight Loss": ["Running (30 mins)", "Jump Rope (15 mins)", "Bodyweight Circuit"],
    "Muscle Gain": ["Weightlifting (1 hr)", "Push-Ups", "Pull-Ups"],
    "Endurance": ["Cycling (1 hr)", "Swimming (30 mins)", "Rowing (20 mins)"],
    "Flexibility": ["Yoga (45 mins)", "Pilates (30 mins)", "Stretching (15 mins)"]
}


def get_fitness_goal():
    return all_plan.keys()


def get_workout_plan(plan):
    return ['kk', 'uuu']

