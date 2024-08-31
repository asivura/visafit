from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_core.pydantic_v1 import BaseModel, Field
from tqdm import tqdm
import shutil
import random
import json
from pydantic import BaseModel
from typing import List, Literal

# Load environment variables from .env file
load_dotenv()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILEPATH = os.path.join(SCRIPT_DIR, "generate_cv.prompt")

with open(TEMPLATE_FILEPATH, "r") as file:
    PROMPT_TEMPLATE = file.read()

def recreate_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        print(f"Removed existing directory: {directory_path}")
    
    os.makedirs(directory_path)
    print(f"Created new directory: {directory_path}")



class Criteration(BaseModel):
    criteration: str
    rating: Literal['low', 'medium', 'high']
    reference: str
    reasoning: str

class Edit(BaseModel):
    type: Literal['added', 'removed']
    text: str

class GeneratedResume(BaseModel):
    generated_cv: str =  Field(description="The full text of the generated CV in markdown format.")
    criterations: List[Criteration]
    edits: List[Edit]

CRITERATIONS = ["Awards", "Memberships", "Press", "Judging", "Original contribution", "Scholarly articles", "Critical employment", "High remuneration"]
RATING = ["low", "medium", "high"]

prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
llm = ChatOpenAI(model="gpt-4o", temperature=0.)
structured_llm = llm.with_structured_output(GeneratedResume)

llm_chain = prompt | structured_llm

data_dir = os.getenv("DATA_DIR")

input_dir = os.path.join(data_dir, "formatted_cv")

ds = pd.read_csv(os.path.join(data_dir, "sample.csv"))
output_dir_md = os.path.join(data_dir, "generated_cv_md")
recreate_directory(output_dir_md)

output_dir_json = os.path.join(data_dir, "generated_cv_json")
recreate_directory(output_dir_json)

for i, row in tqdm(ds.iterrows(), total=len(ds)):
    criterations = []
    for criteration in random.sample(CRITERATIONS, k=random.randint(1, 4)):
        criterations.append({
            "criteration": criteration,
            "rating": random.choice(RATING),
        })

    criteration = json.dumps(criterations, indent=4)

    with open(os.path.join(input_dir, str(row.id)+".md"), "r") as input_file:
        cv_text = input_file.read()

    cv = llm_chain.invoke({"CV_TEXT": cv_text, "CRITERATINS": json.dumps(criterations, indent=4)})
    with open(os.path.join(output_dir_md, str(row.id)+".md"), "w") as output_file:
        output_file.write(cv.generated_cv)

    with open(os.path.join(output_dir_json, str(row.id)+".json"), "w") as output_file:
        output_file.write(json.dumps(cv.model_dump(), indent=4))