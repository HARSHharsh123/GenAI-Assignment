import os
# import pypdf
import PyPDF2
import json
import traceback
from pypdf import PdfReader
def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PdfReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file suppoted"
            
        )

def get_table_data_fill(fill_str):
    try:
        # convert the quiz from a str to dict
        fill =json.loads(fill_str)
        fill_table_data = []
        for key , value in fill.items():
            fill = value["Fill_in_the_blanks"]
            answer = value["answer"]
            fill_table_data.append({"fill_blank": fill, "Correct": answer})

        return fill_table_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False


def get_table_data_true(true_str):
    try:
        # convert the quiz from a str to dict
        tf =json.loads(true_str)
        tf_table_data = []
        for key,value in tf.items():
            tans = value["True_or_False"]
            answer = value["answer"]
            tf_table_data.append({"T&F": tans, "Correct": answer})
        return tf_table_data
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False


def get_table_data_mcq(quiz_str):
    try:
        # convert the quiz from a str to dict
        quiz_dict=json.loads(quiz_str)
        quiz_table_data=[]
        
        # iterate over the quiz dictionary and extract the required information
        for key,value in quiz_dict.items():
            mcq=value["mcq"]
            options=" || ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value["options"].items()
                 
                 ]
            )
            
            correct=value["correct"]
            quiz_table_data.append({"MCQ": mcq,"Choices": options, "Correct": correct})
        
        return quiz_table_data
        
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False

