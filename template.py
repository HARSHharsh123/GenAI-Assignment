import os
from pathlib import Path
import logging 

logging.basicConfig(level = logging.INFO)

project = 'mcqgen'

list_of_files = [
    "src/__init__.py",
    f"src/{project}/__init__.py",
    f"src/{project}/logger.py",
    f"src/{project}/mcqgenerator.py",
    f"src/{project}/utils.py",
    "experiments/__init__.py",
    "experiments/mcqgenerator.ipynb",
    "setup.py",
    "requirements.txt"
]

for filepath in list_of_files:
    ## Not Compulsory to Convert File Path to Path Object 
    ## but it is recommended to convert File Path to File Object as File Object make file path indepent of Platform
    ## we can manipulate paths , means merge them , seperate them (file name , file directory) etc...
    filepath = Path(filepath)
    ## Seperating FilePath into file name , file directory using os module
    filedir, filename = os.path.split(filepath)

    ## Creating a file Directory 

    ## Checking if File directory doesn't exists them make a file directory 
    if filedir != "":
        ## exist_ok = ture means , if filedir doesn't exits then make directory otherwise skip without any error....

        os.makedirs(filedir, exist_ok=True)

        logging.info(f"Creating directory:{filedir} for the file {filename}")

    ## Creating a File
         
    ## Checking if File doesn't exits or File is empty make a new file
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath,'w') as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    ## if file already Exists then give logging info that file already exists
    else:
        logging.info(f"{filename} is already exists") 