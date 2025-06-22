import os
import json
import sys
from datasets import load_dataset

def download_gsm8k_dataset():
    """
    Downloads the GSM8K dataset from openai/gsm8k
    and saves it to the project's data directory.
    """
    # --- Configuration ---
    dataset_name = "gsm8k"
    huggingface_id = "openai/gsm8k"
    huggingface_config = "main"
    # ---------------------

    print(f"--- Starting download for {dataset_name} ---")

    # Construct absolute path to the data directory from the project root (games/)
    project_root = os.getcwd()
    data_dir = os.path.join(project_root, "learner", "data", dataset_name)
    os.makedirs(data_dir, exist_ok=True)
    print(f"Data will be saved in: {data_dir}")

    # Load the dataset
    try:
        dataset = load_dataset(huggingface_id, huggingface_config)
    except Exception as e:
        print(f"Error loading dataset {huggingface_id}: {e}", file=sys.stderr)
        return

    # Print info about the dataset
    print(f"\n'{dataset_name}' dataset loaded with the following splits: {dataset.keys()}")
    for split in dataset:
        print(f"Split '{split}' contains {len(dataset[split])} examples")

        # Save each split to the data directory
        output_path = os.path.join(data_dir, f"{dataset_name}_{split}.json")
        dataset[split].to_json(output_path)
        print(f"Saved {split} split to {output_path}")

        # Print the first example
        if len(dataset[split]) > 0:
            print(f"First example from '{split}' split:")
            print(dataset[split][0])
        print("-" * 50)

    # Save a metadata file
    metadata = {
        "huggingface_id": huggingface_id,
        "huggingface_config": huggingface_config,
        "splits": {split: len(dataset[split]) for split in dataset},
    }
    metadata_path = os.path.join(data_dir, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"\nMetadata saved to {metadata_path}")

    print(f"\n--- {dataset_name} download completed successfully! ---")

if __name__ == "__main__":
    download_gsm8k_dataset() 