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

with open(r"C:\Users\hs081\OneDrive\Desktop\mgp\responsemcq.json","r") as f:
    RESPONSE_MCQ=json.load(f)

print(RESPONSE_MCQ)

TEMPLATE_MCQ="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_MCQ below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_MCQ
{RESPONSE_MCQ}

"""

mcq_generation_prompt = PromptTemplate(
    input_variables=["text" , 'number' , 'subject' , 'tone' , 'RESPONSE_MCQ'],
    template = TEMPLATE_MCQ
)

mcq_chain = LLMChain(llm = llm , prompt = mcq_generation_prompt , output_key="quiz" , verbose = True)

TEMPLATE_v_mcq="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

mcq_evaluation_template = PromptTemplate(
    input_variables=['subject' , 'quiz'],
    template = TEMPLATE_MCQ
)


review_chain_mcq = LLMChain(llm = llm , prompt = mcq_evaluation_template , output_key="review" , verbose = True)

generate_evaluate_chain_mcq= SequentialChain(chains = [mcq_chain , review_chain_mcq] , input_variables=['text' , 'number' , 'subject' ,  'tone' , 'RESPONSE_MCQ'] , output_variables=['quiz' , 'review'] , verbose = True)