from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import os
import pandas as pd
from dotenv import load_dotenv
from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from tqdm import tqdm
import shutil

# Load environment variables from .env file
load_dotenv()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILEPATH = os.path.join(SCRIPT_DIR, "convert_text_cv_to_markdown.prompt")

with open(TEMPLATE_FILEPATH, "r") as file:
    PROMPT_TEMPLATE = file.read()

def recreate_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        print(f"Removed existing directory: {directory_path}")
    
    os.makedirs(directory_path)
    print(f"Created new directory: {directory_path}")


class Resume(BaseModel):
    """Joke to tell user."""

    md: str = Field(description="Resume in markdown format.")

prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
llm = ChatOpenAI(model="gpt-4o", temperature=0.)
structured_llm = llm.with_structured_output(Resume)

llm_chain = prompt | structured_llm

data_dir = os.getenv("DATA_DIR")

ds = pd.read_csv(os.path.join(data_dir, "sample.csv"))
output_dir = os.path.join(data_dir, "formatted_cv")
recreate_directory(output_dir)

for i, row in tqdm(ds.iterrows(), total=len(ds)):
    cv_text = row['Text']
    cv = llm_chain.invoke({"CV_TEXT": cv_text})
    with open(os.path.join(output_dir, str(row.id)+".md"), "w") as output_file:
        output_file.write(cv.md)