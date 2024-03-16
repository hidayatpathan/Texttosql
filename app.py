from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

load_dotenv()  # load all the environment variables

# Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function To Load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function To retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

# Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in the beginning or end and sql word in output
    """
]

# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# if submit is clicked
if submit:
    response_text = get_gemini_response(question, prompt)
    st.subheader("The Response is")
    st.write(response_text)

    # Assuming response_text is the SQL query generated, execute it
    try:
        response = read_sql_query(response_text, "student.db")
        for row in response:
            st.header(row)
    except sqlite3.Error as e:
        st.error(f"Error executing SQL query: {e}")
