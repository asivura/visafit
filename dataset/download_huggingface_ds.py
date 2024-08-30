from dotenv import load_dotenv
import os
import argparse
from datasets import load_dataset

# Load environment variables from .env file
load_dotenv()

def download_hg_dataset(ds_name, data_dir):
    ds = load_dataset(ds_name, download_mode='force_redownload')
    ds.save_to_disk(os.path.join(data_dir, ds_name))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download and save a dataset to a specified directory.')
    parser.add_argument('--data_dir', type=str, default=os.getenv("DATA_DIR"), help='Directory to save the dataset')
    parser.add_argument('--dataset_name', type=str, required=True, help='Name of the dataset to download')
    args = parser.parse_args()

    download_hg_dataset(args.dataset_name, args.data_dir)