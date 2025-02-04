import sqlite3

def create_quiz_table():
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        questions TEXT,
        correct_answers TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

# Call the function at the beginning of the script
create_quiz_table()
