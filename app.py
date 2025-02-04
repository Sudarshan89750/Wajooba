import streamlit as st
import sqlite3
import openai
from datetime import datetime


openai.api_key = "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"

def create_quiz_table():
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            questions TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def generate_quiz(topic):
    prompt = f"Create a multiple-choice quiz on {topic}. Include 5 questions with 4 options each, and specify the correct answer."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use latest OpenAI model
        messages=[
            {"role": "system", "content": "You are a quiz expert."},
            {"role": "user", "content": prompt}
        ]
    )

    return response["choices"][0]["message"]["content"]


def save_quiz(topic, questions):
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO quiz (topic, questions) VALUES (?, ?)", (topic, questions))
    conn.commit()
    conn.close()


def get_quiz_history():
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute("SELECT topic, questions, timestamp FROM quiz ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return data

st.set_page_config(page_title="AI Quiz Generator", layout="wide")

st.title(" AI-Based Quiz Generator")


topic = st.text_input("Enter a topic for the quiz:")

if st.button("Generate Quiz"):
    if topic.strip():
        quiz_content = generate_quiz(topic)
        save_quiz(topic, quiz_content)
        st.success(" Quiz Generated Successfully!")
        st.subheader("Quiz Questions:")
        st.write(quiz_content)
    else:
        st.warning("⚠️ Please enter a topic!")


st.subheader(" Previous Quizzes")
quiz_history = get_quiz_history()

for quiz in quiz_history:
    st.write(f"**Topic:** {quiz[0]}")
    st.text_area("Quiz Questions", quiz[1], height=200)
    st.caption(f" Generated on: {quiz[2]}")
    st.markdown("---")
