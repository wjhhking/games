import os
import sys

# Add the script's own directory to the Python path to allow for local imports
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Import the download function from each script
from download_aime2025 import download_aime_dataset
from download_gpqa import download_gpqa_dataset
from download_gsm8k import download_gsm8k_dataset
from download_math import download_math_dataset
from download_mmlu import download_mmlu_dataset
from download_mmmu import download_mmmu_dataset
from download_swe_bench import download_swe_bench_dataset
from download_hle import download_hle_dataset

def run_all_downloads_simple():
    """
    Runs all dataset download functions sequentially, skipping any
    dataset whose data folder already exists.
    """
    # Assumes this script is run from the 'games/' project root
    project_root = os.getcwd()
    base_data_dir = os.path.join(project_root, "learner", "data")

    # A list of tuples: (dataset_name, download_function)
    # The dataset_name must match the directory name created by its script.
    datasets = [
        ("aime", download_aime_dataset),
        ("gpqa", download_gpqa_dataset),
        ("gsm8k", download_gsm8k_dataset),
        ("math", download_math_dataset),
        ("mmlu", download_mmlu_dataset),
        ("mmmu", download_mmmu_dataset),
        ("swe_bench", download_swe_bench_dataset),
        ("hle", download_hle_dataset),
    ]

    print(f"Base data directory: {base_data_dir}")
    print("-" * 50)

    for name, download_func in datasets:
        data_path = os.path.join(base_data_dir, name)
        
        # Check if the directory exists and is not empty
        if os.path.exists(data_path) and os.listdir(data_path):
            print(f"Directory '{data_path}' already exists and is not empty. Skipping download for '{name}'.")
        else:
            print(f"\n{'='*10} Downloading: {name} {'='*10}")
            download_func()
            print(f"{'-'*10} Finished: {name} {'-'*10}")

    print(f"\n{'='*20} ALL DOWNLOADS CHECKED {'='*20}")

if __name__ == "__main__":
    run_all_downloads_simple() 