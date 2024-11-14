import os
import sqlite3
import bcrypt
import streamlit as st


# Connect to the database (or create if it doesn't exist)
def get_connection():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(ROOT_DIR, "health_fitness_app.db"), 'w') as file:
        file.write("")
    conn = sqlite3.connect("health_fitness_app.db")
    return conn


# Hash a password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


# Verify a password
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password)


# Registration Function
def save_user(name, email, age, user_date, sex, goals, weight, height, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute("""
            INSERT INTO user_profile (name, email, age, date, sex, goals, weight, height, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, email, age, user_date, sex, goals, weight, height, hashed_password))
        conn.commit()


def format_user(user):
    if type(user) is tuple:
        return {
            "user_id": user[0],
            "email": user[1],
            "name": user[2],
            "age": user[3],
            "date": user[4],
            "sex": user[5],
            "goals": user[6],
            "weight": user[7],
            "height": user[8],
            "password": user[9]
        }


def authenticate_user(email, password):
    try:
        with get_connection() as conn:
            # cookies = get_cookie_instance()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_profile WHERE email = ?", (email,))
            user = format_user(cursor.fetchone())
            if user:
                if bcrypt.checkpw(password.encode(encoding="utf-8"), user["password"]):
                    st.session_state.logged_in = True
                    st.session_state.current_user = user["name"]
                    st.session_state.user = {
                        key: value for key, value in user.items() if key != "password"
                    }
                    return True
                else:
                    return False
        return False
    except Exception as e:
        print(e)
        return False


def verify_duplicate_user(email):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_profile WHERE email = ?", (email,))
            if cursor.fetchone():
                return True
        return False
    except Exception as e:
        # print(e)
        return False


# Logout Function
def logout_user():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.user = None
    st.session_state['page'] = 'login'
    st.rerun()


# Save activity data
def save_activity(user_id, date, steps, distance, calories_burned, description):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO activity_tracking (user_id, steps, distance, calories_burned, date, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, steps, distance, calories_burned, date, description))
            conn.commit()
    except:
        return False


def format_activity(activities):
    return [
        {
            "steps": activity[2],
            "distance": activity[3],
            "calories": activity[4],
            "date": activity[5],
            "workout": activity[6]
        }
        for activity in activities
    ]


# Retrieve activity data
def get_user_activities(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activity_tracking WHERE user_id = ?", (user_id,))
        activities = cursor.fetchall()
        if activities:
            return format_activity(activities)
    return None


# Function to add a diet entry
def add_diet(user_id, food, calories, protein, carbs, fat, date):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Insert diet entry for the user
        cursor.execute('''
            INSERT INTO nutrition_tracking (user_id, date, food_item, calories, protein, carbs, fat)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, date, food, calories, protein, carbs, fat))
        conn.commit()
        print("Diet entry added successfully.")


def format_diet(diets):
    return [
        {
            "food": diet[1],
            "calories": diet[2],
            "protein": diet[3],
            "carbs": diet[4],
            "fat": diet[5],
            "date": diet[0],

        }
        for diet in diets
    ]


# Function to retrieve diet entries for a user
def get_user_nutrition(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        # Fetch diet entries for the user
        cursor.execute('''
            SELECT date, food_item, calories, protein, carbs, fat
            FROM nutrition_tracking
            WHERE user_id = ?
            ORDER BY date DESC
        ''', (user_id,))

        diets = cursor.fetchall()
        if diets:
            return format_diet(diets)
    return None


def log_workout(user_id, exercise, calories_burned, workout_date):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO workout_tracking (user_id, date, exercise, calories_burned)
            VALUES (?, ?, ?, ?)
        ''', (user_id, workout_date, exercise, calories_burned))
        conn.commit()


def format_workout(workouts):
    return [
        {
            "date": workout[0],
            "exercise": workout[1],
            "calories": workout[2]
        }
        for workout in workouts
    ]


def get_user_workout(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date, exercise, calories_burned
            FROM workout_tracking
            WHERE user_id = ?
            ORDER BY date DESC
        ''', (user_id,))
        workouts = cursor.fetchall()
        if workouts:
            return format_workout(workouts)
    return None


def add_exercise_to_plan(user_id, exercise_name, description):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
               INSERT INTO exercise_plan (user_id, exercise_name, description)
               VALUES (?, ?, ?)
           ''', (user_id, exercise_name, description))
        conn.commit()


def format_exercice(exercices):
    all_exercises = {}
    for exercise in exercices:
        if exercise[0] not in all_exercises.keys():
            all_exercises[exercise[0]] = []
        all_exercises[exercise[0]].append(exercise[1])
    return all_exercises


def get_exercise_plan(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()

        # cursor.execute('''
        #             SELECT *
        #             FROM exercise_plan
        #         ''')
        # print("all")
        # print(cursor.fetchall())

        cursor.execute('''
            SELECT exercise_name, description 
            FROM exercise_plan
            WHERE user_id = ?
        ''', (user_id,))
        exercises = cursor.fetchall()
        # print((exercises))
        if exercises:
            return format_exercice(exercises)
    return None
