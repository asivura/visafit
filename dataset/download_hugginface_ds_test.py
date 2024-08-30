import os
import pytest
from datasets import load_from_disk
from download_huggingface_ds import download_hg_dataset

from datasets.exceptions import DatasetNotFoundError

def test_download_hg_dataset(tmpdir):
    # Test downloading a dataset and saving it to a specified directory
    dataset_name = "ahmedheakl/resume-atlas"
    data_dir = str(tmpdir)
    
    download_hg_dataset(dataset_name, data_dir)
    
    # Check if the dataset is downloaded and saved to the specified directory
    assert os.path.exists(os.path.join(data_dir, dataset_name))
    
    # Check if the downloaded dataset can be loaded using the datasets library
    ds = load_from_disk(os.path.join(data_dir, dataset_name))
    assert isinstance(ds, dict)
    assert "train" in ds

def test_download_hg_dataset_invalid_dataset(tmpdir):
    # Test downloading an invalid dataset
    dataset_name = "invalid_dataset"
    data_dir = str(tmpdir)
    
    with pytest.raises(DatasetNotFoundError):
        download_hg_dataset(dataset_name, data_dir)