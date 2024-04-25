import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgen.utils import read_file,get_table_data_mcq ,get_table_data_fill , get_table_data_true
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgen.mcqgenerator import generate_evaluate_chain_mcq
from src.mcqgen.fillblankgenerator import generate_evaluate_chain_fill
from src.mcqgen.truefalsegenerator import generate_evaluate_chain_true
from src.mcqgen.logger import logging

#loading json files
with open('responsemcq.json', 'r') as f1:
    RESPONSE_MCQ = json.load(f1)

with open('responsefill.json' , 'r') as f2:
    RESPONSE_FILL= json.load(f2)

with open('responsetrue.json' , 'r') as f3:
    RESPONSE_TRUE= json.load(f3)

#creating a title for the app

st.markdown("<h2 style='text-align: center;'>LLM Assignment by Harsh Shukla 🦜⛓️</h2>", unsafe_allow_html=True)

with st.form("user input"):
    uploaded_file = st.file_uploader("upload pdf or text")
    
    options = ['MCQ', 'Fill in the Blanks', 'True and False']

    selected_option = st.radio('Select which type of output you want : ', options)

    count = st.number_input("no of questions you have to generate", min_value=3, max_value=50)

    subject=st.text_input("Insert Subject",max_chars=20)

    options = ['Simple', 'Medium', 'Hard']

    selected_option_tone = st.radio('Select Level of Complexity of Questions : ', options)

    button=st.form_submit_button("Create MCQs")

    if selected_option == 'MCQ':
        if button and uploaded_file is not None and count and subject and selected_option_tone:
            with st.spinner("loading..."):
                try:
                    text=read_file(uploaded_file)
                    #Count tokens and the cost of API call
                    with get_openai_callback() as cb:
                        response=generate_evaluate_chain_mcq(
                                {
                                "text": text,
                                "number": count,
                                "subject":subject,
                                "tone": selected_option_tone,
                                "RESPONSE_MCQ": json.dumps(RESPONSE_MCQ)
                                    }
                            )
                        #st.write(response)
                        response['quiz'] = response['quiz'].replace('### RESPONSE_MCQ\n' , '')

                except Exception as e:
                        traceback.print_exception(type(e), e, e.__traceback__)
                        st.error("Error")

                else:
                        print(f"Total Tokens:{cb.total_tokens}")
                        print(f"Prompt Tokens:{cb.prompt_tokens}")
                        print(f"Completion Tokens:{cb.completion_tokens}")
                        print(f"Total Cost:{cb.total_cost}")
                        if isinstance(response, dict):
                            #Extract the quiz data from the response
                            quiz=response.get("quiz", None)
                            if quiz is not None:
                                table_data=get_table_data_mcq(quiz)
                                if table_data is not None:
                                    df=pd.DataFrame(table_data)
                                    df.index=df.index+1
                                    st.table(df)
                                else:
                                    st.error("Error in the table data")

                        else:
                            st.write(response)
    if selected_option == 'Fill in the Blanks':
        if button and uploaded_file is not None and count and subject and selected_option_tone:
            with st.spinner("loading..."):
                try:
                    text=read_file(uploaded_file)
                    #Count tokens and the cost of API call
                    with get_openai_callback() as cb:
                        response = generate_evaluate_chain_fill(
                            {
                                "text" : text,
                                "number" : count,
                                "subject" : subject,
                                "tone" : selected_option_tone,
                                "RESPONSE_FILL" : json.dumps(RESPONSE_FILL)
                            }
                        )
                        #st.write(response)
                        response['Fill in blanks'] =  response['Fill in blanks'].replace('### RESPONSE_FILL\n' , '')

                except Exception as e:
                        traceback.print_exception(type(e), e, e.__traceback__)
                        st.error("Error")

                else:
                        print(f"Total Tokens:{cb.total_tokens}")
                        print(f"Prompt Tokens:{cb.prompt_tokens}")
                        print(f"Completion Tokens:{cb.completion_tokens}")
                        print(f"Total Cost:{cb.total_cost}")
                        if isinstance(response, dict):
                            #Extract the quiz data from the response
                            fill=response.get("Fill in blanks", None)
                            if fill is not None:
                                table_data=get_table_data_fill(fill)
                                if table_data is not None:
                                    df=pd.DataFrame(table_data)
                                    df.index=df.index+1
                                    st.table(df)
                                else:
                                    st.error("Error in the table data")

                        else:
                            st.write(response)
    if selected_option == 'True and False':
        if button and uploaded_file is not None and count and subject and selected_option_tone:
            with st.spinner("loading..."):
                try:
                    text=read_file(uploaded_file)
                    #Count tokens and the cost of API call
                    with get_openai_callback() as cb:
                        response=generate_evaluate_chain_true(
                                {
                                "text": text,
                                "number": count,
                                "subject":subject,
                                "tone": selected_option_tone,
                                "RESPONSE_TRUE": json.dumps(RESPONSE_TRUE)
                                }
                            )
                        #st.write(response)
                        response['true and false'] =  response['true and false'].replace('### RESPONSE_TRUE\n' , '')

                except Exception as e:
                        traceback.print_exception(type(e), e, e.__traceback__)
                        st.error("Error")

                else:
                        print(f"Total Tokens:{cb.total_tokens}")
                        print(f"Prompt Tokens:{cb.prompt_tokens}")
                        print(f"Completion Tokens:{cb.completion_tokens}")
                        print(f"Total Cost:{cb.total_cost}")
                        if isinstance(response, dict):
                            #Extract the quiz data from the response
                            truefalse=response.get("true and false", None)
                            if truefalse is not None:
                                table_data=get_table_data_true(truefalse)
                                if table_data is not None:
                                    df=pd.DataFrame(table_data)
                                    df.index=df.index+1
                                    st.table(df)
                                else:
                                    st.error("Error in the table data")

                        else:
                            st.write(response)