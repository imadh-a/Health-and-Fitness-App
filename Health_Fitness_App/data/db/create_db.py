import sqlite3


# Connect to the database (or create if it doesn't exist)
def get_connection():
    conn = sqlite3.connect("health_fitness_app.db")
    return conn


# Initialize database tables
def create_tables():
    with get_connection() as conn:
        cursor = conn.cursor()

        # Table for user profiles
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profile (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                name TEXT,
                age INTEGER,
                date DATE,
                sex TEXT,
                goals TEXT,
                weight REAL,
                height REAL,
                password TEXT
            )
        """)

        # Table for activity tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                steps INTEGER,
                distance REAL,
                calories_burned REAL,
                date DATE,
                description TEXT,
                FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
            )
        """)

        # Table for nutrition tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nutrition_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                food_item TEXT,
                calories INTEGER,
                protein REAL,
                carbs REAL,
                fat REAL,
                date DATE,
                FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
            )
        """)

        cursor.execute('''
                   CREATE TABLE IF NOT EXISTS workout_tracking (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER,
                       date TEXT,
                       exercise TEXT,
                       calories_burned REAL,
                       FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
                   )
               ''')

        cursor.execute('''
                   CREATE TABLE IF NOT EXISTS exercise_plan (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER,
                       exercise_name TEXT,
                       description TEXT,
                       FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
                   )
               ''')

        # Commit changes
        conn.commit()


create_tables()  # Call this function once to set up tables
