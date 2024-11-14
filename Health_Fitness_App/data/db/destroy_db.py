import sqlite3
import os


# Connect to the database (or create if it doesn't exist)
def get_connection():
    conn = sqlite3.connect("health_fitness_app.db")
    return conn


# Clear all data from user_profile, activity_tracking, and nutrition_tracking tables
def clear_all_data():
    with get_connection() as conn:
        cursor = conn.cursor()

        # Clear each table's data
        cursor.execute("DELETE FROM user_profile")
        cursor.execute("DELETE FROM activity_tracking")
        cursor.execute("DELETE FROM nutrition_tracking")

        conn.commit()
        print("All data cleared from database tables.")


# Drop all tables
def drop_all_tables():
    with get_connection() as conn:
        cursor = conn.cursor()

        # Drop each table
        cursor.execute("DROP TABLE IF EXISTS user_profile")
        cursor.execute("DROP TABLE IF EXISTS activity_tracking")
        cursor.execute("DROP TABLE IF EXISTS nutrition_tracking")

        conn.commit()
        print("All tables dropped from database.")


# Delete the database file
def delete_database():
    db_path = "health_fitness_app.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Database file deleted.")
    else:
        print("Database file not found.")


clear_all_data()
drop_all_tables()
delete_database()
