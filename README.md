# Visafit
AI application to roughly assess how a person is qualified for an O-1A immigration visa

## Installation
1. Clone the repository
1. Install Python 3.12.2 
1. Create a virtual environment: `python3 -m venv .venv`
1. Activate the virtual environment: `source .venv/bin/activate`
1. Install the requirements: `pip install -r requirements.txt`
1. Install Pango: `brew install pango`

### Setting up the environment variables
1. Create a `.env` file in the root of the project
1. Add the following environment variables to the `.env` file:
    ```
    DATA_DIR=<absolute path to data directory where we store dataset artifacts. Example: "/Users/alexandersivura/Developer/visafit/data">
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
    LANGCHAIN_API_KEY="<your-api-key>"
    LANGCHAIN_PROJECT="visafit"
    OPENAI_API_KEY="<your api key for openai>"
    UNSTRUCTURED_API_KEY="<your api key for unstructured>"
    ```


*Important* when you add new packages to the project after you intall it with pip please run the following command to update the requirements.txt file `pip freeze > requirements.txt`

## Generation of the dataset with CVs and Labels
1. We parsed information from the USCIS [website](https://www.uscis.gov/policy-manual/volume-2-part-m#) and saved it in a [json file](criteration.json). 
2. We downloaded a [dataset](https://huggingface.co/datasets/ahmedheakl/resume-atlas) of CVs which was published with the paper ResumeAtlas: Revisiting Resume Classification with Large-Scale Datasets and Large Language Models [link](https://arxiv.org/abs/2406.18125)
3. To download the dataset we use this script [dataset/download_huggingface_ds.py](dataset/download_huggingface_ds.py)
4. The dataset contains more than 13k CVs, for the sake of the project we only used 84 CVs from the dataset, to save tiem and budject on using OpenAI API. We randomly sampled two resume per each category in the dataset with the script [dataset/sample_cvs.py](dataset/sample_cvs.py). Sampled output [data/sample.csv](data/sample.csv)
5. CVs in the dataset are present in the text format and do not have any formatting. We used LLM to make CVs well formatted and convert to Markdown format. We used the script [dataset/convert_text_cv_to_markdown.py](dataset/convert_text_cv_to_markdown.py) to format the CVs. The formatted CVs are saved in the [data/formatted_cv](data/formatted_cv) directory. There is a prompt we are using for this task [dataset/convert_text_cv_to_markdown.prompt](dataset/convert_text_cv_to_markdown.prompt)
6. Using LLM we modify markdowns from the previous step to add there some information to satisfy from 1 to 4 criterations. There is a prompt we are using for this task [dataset/generate_cv.prompt](dataset/generate_cv.prompt). You can regenerate the dataset using script [dataset/generate_cv.py](dataset/generate_cv.py). The generated CVs are saved in the [data/generated_cv](data/generated_cv_md) directory.
7. To get PDF formatted differently to test our app we convert markdowns to HTML by asking LLM to apply creative styles there. Here is the prompt we are using for this task [dataset/generate_html_cv.prompt](dataset/generate_html_cv.prompt). You can regenerate the htmls using script [dataset/generate_html_cv.py](dataset/generate_html_cv.py). The generated CVs are saved in the [data/generated_cv_html](data/generated_cv_html) directory.
8. As the last step we convert HTMLs to PDFs using the script [dataset/convert_html_cv_to_pdf.py](dataset/convert_html_cv_to_pdf.py). The generated CVs are saved in the [data/generated_cv_pdf](data/generated_cv_pdf) directory.

## App
1. To retrieve text out of PDF file we using [https://unstructured.io](https://unstructured.io) API. 

2. Fast API app is located in the [app](app) directory. To run the app you need to execute the following command `uvicorn app:app --reload`. The app API will be available at [http://127.0.0.1:8000/check-cv/](http://127.0.0.1:8000/check-cv/)

## Process dataset
To process all examples in the dataset you can use the script [eval/process_ds.py](eval/process_ds.py). The script will process all examples in the dataset and save the results in the [data/predictions](data/predictions) directory.

## Next steps
1. Create a script which calculates precision and recall for the dataset predictions
2. Do error analysis and improve prompt for the LLM model
3. Create evaluation dataset with examples from real people.