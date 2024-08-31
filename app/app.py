from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
import tempfile
from langchain_unstructured import UnstructuredLoader
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import List, Literal
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILEPATH = os.path.join(SCRIPT_DIR, "check_cv.prompt")
with open(TEMPLATE_FILEPATH, "r") as file:
    PROMPT_TEMPLATE = file.read()

class Criteration(BaseModel):
    criteration: str
    rating: Literal['low', 'medium', 'high']
    reference: str
    reasoning: str

class Output(BaseModel):
    criterations: List[Criteration]


app = FastAPI()

@app.post("/check-cv/")
async def parse_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file format. Only PDFs are allowed.")
    
    try:
        # Read the PDF file content
        pdf_content = await file.read()

        with tempfile.NamedTemporaryFile(suffix=file.filename) as temp_pdf:
            temp_pdf.write(pdf_content)
            temp_pdf_path = temp_pdf.name
            loader = UnstructuredLoader(
                file_path=[temp_pdf_path], 
                strategy="fast",
                partition_via_api=True
            ) 
            docs = await loader.aload()

        text_content = "\n".join([doc.page_content for doc in docs])
        prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
        llm = ChatOpenAI(model="gpt-4o", temperature=0.)
        structured_llm = llm.with_structured_output(Output)
        llm_chain = prompt | structured_llm

        res = await llm_chain.ainvoke({"CV_TEXT": text_content})

        return res.dict()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
