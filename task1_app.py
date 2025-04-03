import streamlit as st
from openai import OpenAI
import re
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

def clean_response(text):
   text = re.sub("```python","",text) 
   text = re.sub("```","",text)
   return text.strip()

def code_commentor(code):

    # step 2: get code with comments and doc

    prompt = f""" you are an expert programmer, code reviewer and commentor.
    you need to read the below code in triple backticks and add comments and docstring
    Do not modify the code or logic, only add comments and doc string.
    Only provide code as output, do not add any additional text or explanation
    Code:
    ```{code}``
    """
    messages = [{'role':'user','content':prompt},]
    response = client.chat.completions.create(model='gpt-4o', messages=messages, temperature=0)
    response = response.choices[0].message.content
    response = clean_response(response)
 
    return response

st.title("Code Commentor App")
st.header("Welcome to Code Commentor App")
st.write("This app can be used to add comments and doc string to any python code file")
 
file = st.file_uploader("Pick a .py file")

if file:
    st.write("File Uploaded")

    # create a button for user to click "Process Code"
    if st.button("Process Code"):

        input_file = file.name # extracting the name of file
        input_code = file.read().decode('utf-8') # reading code content

        st.subheader("Original Code")
        st.code(input_code,language='python') # show the code on frontend

        # get comments
        outputcode = code_commentor(input_code) # add comments, docstring to the code

        st.subheader("Modified Code")
        st.code(outputcode,language='python') # show the code on frontend
        output_file = input_file[:-3]+"_c"+".py"

        st.download_button("Download Code",data=outputcode,
                           file_name=output_file,mime="text/plain")

