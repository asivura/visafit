import pandas as pd
from datasets import load_from_disk
from dotenv import load_dotenv
import os
import argparse

# Load environment variables from .env file
load_dotenv()

def sample_cvs(data_dir, n_examples_per_category):
    dataset_name = "ahmedheakl/resume-atlas"
    ds = load_from_disk(os.path.join(data_dir, dataset_name))

    df = ds['train'].to_pandas()
    selected_examples = []

    for _, group in df.groupby('Category'):
        examples = group.sample(2, random_state=42)
        selected_examples.append(examples)

    final_selection = pd.concat(selected_examples)

    # Reset the index and rename the 'index' column to 'id'
    final_selection.reset_index(drop=False, inplace=True)
    final_selection.rename(columns={'index': 'id'}, inplace=True)

    # Save the final selection to a CSV file
    output_path = os.path.join(data_dir, "sample.csv")
    final_selection.to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to process dataset and sample examples.")
    parser.add_argument('--data_dir', type=str, default=os.getenv("DATA_DIR"), help="Directory where the dataset is stored")
    parser.add_argument('--n_examples_per_category', type=int, default=2, help="Number of examples to sample per category")
    args = parser.parse_args()

    sample_cvs(args.data_dir, args.n_examples_per_category)