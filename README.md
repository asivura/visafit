# Visafit
AI application to roughly assess how a person is qualified for an O-1A immigration visa

## Installation
1. Clone the repository
1. Install Python 3.12.2 
1. Create a virtual environment: `python3 -m venv .venv`
1. Activate the virtual environment: `source .venv/bin/activate`
1. Install the requirements: `pip install -r requirements.txt`

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
    ```


*Important* when you add new packages to the project after you intall it with pip please run the following command to update the requirements.txt file `pip freeze > requirements.txt`
