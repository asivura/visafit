from dotenv import load_dotenv
import os
import pandas as pd
from tqdm import tqdm
import requests
import json
import shutil

load_dotenv()

def recreate_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        print(f"Removed existing directory: {directory_path}")
    
    os.makedirs(directory_path)
    print(f"Created new directory: {directory_path}")

data_dir = os.getenv("DATA_DIR")
input_dir = os.path.join(data_dir, "generated_cv_pdf")
ds = pd.read_csv(os.path.join(data_dir, "sample.csv"))
output_dir = os.path.join(data_dir, "predictions")
url = "http://127.0.0.1:8000/check-cv/"


def get_predictions(pdf_path):
    pdf_file_path = os.path.join(input_dir, str(row["id"])+".pdf")

    # Open the file in binary mode
    with open(pdf_file_path, "rb") as pdf_file:
        # Prepare the file to be sent as multipart/form-data
        files = {"file": ("file.pdf", pdf_file, "application/pdf")}

        # Send the POST request to the FastAPI endpoint
        response = requests.post(url, files=files)

    # Print the response from the server
    if response.status_code == 200:
        # Assuming the response is a JSON object
        return response.json()
    else:
        raise Exception(f"Failed to get predictions for {pdf_file_path}, Error: {response.status_code} - {response.text}")
    
recreate_directory(output_dir)
for _, row in tqdm(ds.iterrows(), total=len(ds)):
    prediction = get_predictions(os.path.join(input_dir, str(row["id"])+".pdf"))
    with open(os.path.join(output_dir, str(row.id)+".json"), "w") as output_file:
        output_file.write(json.dumps(prediction, indent=4))