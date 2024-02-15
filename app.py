from dotenv import load_dotenv
from read_db import read_database
from excel_to_sqldb import excel_to_sqlite
import pandas as pd
import shutil
import base64

load_dotenv()

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))


def get_gemini_response(question, prompt):
    generation_config = {"temperature": 0.7,
                         "top_p": 1,
                         "top_k": 1,
                         "max_output_tokens": 2048
                         }
    safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
]

    model = genai.GenerativeModel('gemini-1.0-pro', generation_config=generation_config, safety_settings=safety_settings)
    response = model.generate_content([prompt, question])
    return response.text

## Read sql query
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    curr = conn.cursor()
    curr.execute(sql)
    rows = curr.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row[0])
    return rows

## Streamlit Code

st.set_page_config(
    page_title="SQL code solution",
    page_icon="SQL.png",
    layout='centered',
    initial_sidebar_state="expanded" )

#left_sidebar, main_content, right_sidebar = st.columns([1, 4, 1])

def clear_directories():
    shutil.rmtree('uploads', ignore_errors=True)
    shutil.rmtree('upload_database', ignore_errors=True)
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('upload_database', exist_ok=True)

clear_directories()

st.header("SQL Web-App")

instructions = {
    "1": "Select whether you have dataset or not",
    "2": "If you have the dataset then",
    "3": "You can upload CSV, Excel or database (.db) file",
    "4": "If you dont have dataset then",
    "5": "You can retrieve sql query by providing table name and column name",
    "6": "Inside input box, write you question to get query with output"
}

# Create an expander for instructions
with st.sidebar.expander("Read Instruction Carefully"):
    for title, description in instructions.items():
        st.write(f"**{title}.** {description}")
## Dataset Question

dataset = st.selectbox('Do you have your own dataset', ('Choose an option', 'Yes, I have', 'No, I just want to get sql code'), placeholder="Choose an option")

## File extenson question
fileextensions = {"Excel":'xlsx', "CSV":'csv', ".db":".db"}
columns, table_name = None, None

## if dataset available
if dataset == 'Yes, I have':
    st.write('You selected:', dataset)
    uploaded_file = st.file_uploader("Upload a file",type=['xlsx','csv','.db'])
    

    if uploaded_file == None:
        st.markdown("""<img src="data:image/png;base64,{}" width="15">
                    Waiting to upload file""".format(base64.b64encode(open("waiting.png", "rb").read()).decode()),unsafe_allow_html=True)
        st.write("")
    elif uploaded_file is not None:
        if uploaded_file.name.endswith('.db'):
            save_path = os.path.join("upload_database", uploaded_file.name)
            with open(save_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            sql_db_path = save_path
            table_name, columns = read_database(save_path)
        else:
            save_path = os.path.join('uploads', uploaded_file.name)
            with open(save_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            st.write('file uploaded successfully!')
            columns, table_name, sql_db_path = excel_to_sqlite(f'{save_path}', 'upload_database/data.db','my_table')

    prompt = f"""You are an expert in converting english text to SQL query.
         I have a database with table named {table_name} & have columns {columns}. 
         Please help me with this task. Sql code should not have these signs ``` before and after query.
         """
    print(prompt)

    st.write()
    question = st.text_input("Ask your question:", key='input')
    submit = st.button("Get Result")

    try: 
        if submit:
            sql_code = get_gemini_response(question, prompt)
            st.subheader(f"SQL code:")
            st.code(sql_code, language="sql")
            print(sql_code)
            print(len(sql_code))
            response = read_sql_query(sql_code, sql_db_path)
            
            st.subheader("Output: ")
            for row in response:
                print(response)
                print(row)
                st.code(row[0], language='bash')
            st.markdown("<p><em>if not satisfied with the result. Click on 'Get Result' Again<em></p>", unsafe_allow_html=True)
    except Exception as e:
        st.write("Output not possible for this code")
        st.markdown("<p><em>if not satisfied with the result. Click on 'Get Result' Again<em></p>", unsafe_allow_html=True)
elif dataset=='No, I just want to get sql code':
    
    st.write('You selected:', dataset)
    table_name = st.text_input("Table name")
    col_name = st.text_input("col_name: Provide spaces between col names")
    prompt = f"""You are an expert in converting english text to SQL query.
            I have a database with table named {table_name} & have columns {col_name}. 
            Please help me with this task. Sql code should not have these signs ``` before and after query.
            Just return the sql code.
            """
    st.write()
    question = st.text_input("Ask your question: ", key='input')
    submit = st.button("Get Result")
    if submit:
        sql_code = get_gemini_response(question, prompt)
        st.subheader(f"SQL code:")
        st.code(sql_code, language="sql")
        st.markdown("<p><em>if not satisfied with the result. Click on 'Get Result' Again<em></p>", unsafe_allow_html=True)





## Footer Follow code

st.sidebar.markdown("<h3>If you like this app. You can follow me on</h3>", unsafe_allow_html=True)

linkedin, github,l,m,n = st.sidebar.columns(5)
with linkedin:
    st.markdown(
        """<a href="https://www.linkedin.com/in/sanchit-singla/">
        <img src="data:image/png;base64,{}" width="40">
        </a>""".format(base64.b64encode(open("linkedin.png", "rb").read()).decode()
        ),
        unsafe_allow_html=True)

with github:
    st.markdown(
        """<a href="https://github.com/sa-1-2/">
        <img src="data:image/png;base64,{}" width="40">
        </a>""".format(base64.b64encode(open("github.PNG", "rb").read()).decode()
        ),
        unsafe_allow_html=True)

st.sidebar.write("")
st.sidebar.write("BY: Sanchit Singla")

st.sidebar.write("")
st.sidebar.write("You can report Bug at Email")
email_address = "your_email@example.com"
email_link = f'<a href="mailto:{email_address}">{email_address}</a>'
st.markdown(email_link, unsafe_allow_html=True)








        