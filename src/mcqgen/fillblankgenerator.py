from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback
import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
import PyPDF2


load_dotenv()

key=os.getenv("OPEN_AI_KEY")
print(key)

llm=ChatOpenAI(openai_api_key=key,model_name="gpt-3.5-turbo",temperature=0.7)

with open(r"C:\Users\hs081\OneDrive\Desktop\mgp\responsefill.json","r") as f:
    RESPONSE_FILL=json.load(f)

print(RESPONSE_FILL)

TEMPLATE_FILL="""
Text:{text}
You are an expert Fill in blanks maker . Given the above text, it is your job to \
create  questions  of {number} Fill in the blanks for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_FILL below  and use it as a guide. \
Ensure to make {number} fill in the blanks
### RESPONSE_FILL
{RESPONSE_FILL}

"""

fill_generation_prompt = PromptTemplate(
    input_variables=["text" , 'number' , 'subject' , 'tone' , 'RESPONSE_FILL'],
    template = TEMPLATE_FILL
)

fill_chain = LLMChain(llm = llm , prompt=fill_generation_prompt , output_key='Fill in blanks' , verbose=True)

TEMPLATE_v_fill="""
You are an expert english grammarian and writer. Given a Fill in the blank Questions for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the Fill in the blanks questions. Only use at max 50 words for complexity analysis. 
if the questions is not at per with the cognitive and analytical abilities of the students,\
update the Fill in the blank questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Fill in the blanks:
{fill_blanks}

Check from an expert English Writer of the above questions:
"""
fill_evaluation_template = PromptTemplate(
    input_variables=['subject' , 'fill_blanks'],
    template = TEMPLATE_FILL
)

review_chain_fill = LLMChain(llm = llm , prompt = fill_evaluation_template , output_key="review" , verbose = True)

generate_evaluate_chain_fill = SequentialChain(chains = [fill_chain , review_chain_fill] , input_variables=['text' , 'number' , 'subject' ,  'tone' , 'RESPONSE_FILL'] , output_variables=['Fill in blanks','review'] , verbose = True)