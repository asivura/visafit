from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_core.pydantic_v1 import BaseModel, Field
from tqdm import tqdm
import shutil
from pydantic import BaseModel
from typing import List

# Load environment variables from .env file
load_dotenv()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILEPATH = os.path.join(SCRIPT_DIR, "generate_html_cv.prompt")

with open(TEMPLATE_FILEPATH, "r") as file:
    PROMPT_TEMPLATE = file.read()

def recreate_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        print(f"Removed existing directory: {directory_path}")
    
    os.makedirs(directory_path)
    print(f"Created new directory: {directory_path}")


prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
llm = ChatOpenAI(model="gpt-4o", temperature=1.)

llm_chain = prompt | llm

data_dir = os.getenv("DATA_DIR")

input_dir = os.path.join(data_dir, "generated_cv_md")

ds = pd.read_csv(os.path.join(data_dir, "sample.csv"))
output_dir = os.path.join(data_dir, "generated_cv_html")
recreate_directory(output_dir)

for i, row in tqdm(ds.iterrows(), total=len(ds)):

    with open(os.path.join(input_dir, str(row.id)+".md"), "r") as input_file:
        cv_text = input_file.read()

    cv = llm_chain.invoke({"CV_TEXT": cv_text})
    with open(os.path.join(output_dir, str(row.id)+".html"), "w") as output_file:
        output_file.write(cv.content)