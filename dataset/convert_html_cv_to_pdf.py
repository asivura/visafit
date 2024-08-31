from weasyprint import HTML
import os
import shutil
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def convert_html_to_pdf(html_file_path, pdf_file_path):
    # Load the HTML file
    HTML(html_file_path).write_pdf(pdf_file_path)

def recreate_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        print(f"Removed existing directory: {directory_path}")
    
    os.makedirs(directory_path)
    print(f"Created new directory: {directory_path}")

data_dir = os.getenv("DATA_DIR")

input_dir = os.path.join(data_dir, "generated_cv_html")

ds = pd.read_csv(os.path.join(data_dir, "sample.csv"))
output_dir = os.path.join(data_dir, "generated_cv_pdf")
recreate_directory(output_dir)

for i, row in tqdm(ds.iterrows(), total=len(ds)):
    convert_html_to_pdf(os.path.join(input_dir, str(row.id)+".html"), os.path.join(output_dir, str(row.id)+".pdf")) 