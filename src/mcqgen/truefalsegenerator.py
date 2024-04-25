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

with open(r"C:\Users\hs081\OneDrive\Desktop\mgp\responsetrue.json","r") as f:
    RESPONSE_TRUE=json.load(f)

print(RESPONSE_TRUE)

TEMPLATE_TRUE="""
Text:{text}
You are an expert True and False maker . Given the above text, it is your job to \
create  questions  of {number} True and False for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_TRUE below  and use it as a guide. \
Ensure to make {number} true and false
### RESPONSE_TRUE
{RESPONSE_TRUE}

"""

true_generation_prompt = PromptTemplate(
    input_variables=["text" , 'number' , 'subject' , 'tone' , 'RESPONSE_TRUE'],
    template = TEMPLATE_TRUE
)

true_chain = LLMChain(llm = llm , prompt=true_generation_prompt , output_key='true and false' , verbose=True)

TEMPLATE_v_true="""
You are an expert english grammarian and writer. Given a Ture and False Questions for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the true and false questions. Only use at max 50 words for complexity analysis. 
if the questions is not at per with the cognitive and analytical abilities of the students,\
update the true and false questions which needs to be changed and change the tone such that it perfectly fits the student abilities
True and False:
{true_and_false}

Check from an expert English Writer of the above questions:
"""

true_evaluation_template = PromptTemplate(
    input_variables=['subject' , 'true_and_false'],
    template = TEMPLATE_TRUE
)


review_chain_true = LLMChain(llm = llm , prompt = true_evaluation_template , output_key="review" , verbose = True)

generate_evaluate_chain_true = SequentialChain(chains = [true_chain , review_chain_true] , input_variables=['text' , 'number' , 'subject' ,  'tone' , 'RESPONSE_TRUE'] , output_variables=['true and false' , 'review'] , verbose = True)