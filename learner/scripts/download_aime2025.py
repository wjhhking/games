import os
import json
import sys
from datasets import load_dataset

def download_aime_dataset():
    """
    Downloads the AIME dataset from opencompass/AIME2025, iterating through
    all available configurations and saving them to the project's data directory.
    """
    # --- Configuration ---
    dataset_name = "aime"
    huggingface_id = "opencompass/AIME2025"
    configs = ['AIME2025-I', 'AIME2025-II']
    # ---------------------

    print(f"--- Starting download for {dataset_name} ({huggingface_id}) ---")

    # Construct absolute path to the data directory from the project root (games/)
    project_root = os.getcwd()
    base_data_dir = os.path.join(project_root, "learner", "data", dataset_name)
    os.makedirs(base_data_dir, exist_ok=True)
    print(f"Data will be saved in: {base_data_dir}")

    all_splits_metadata = {}

    # Loop through each configuration and download it
    for config in configs:
        print(f"\n{'='*10} Downloading config: {config} {'='*10}")

        # Create a subdirectory for the config
        config_dir = os.path.join(base_data_dir, config)
        os.makedirs(config_dir, exist_ok=True)

        try:
            dataset = load_dataset(huggingface_id, config)
        except Exception as e:
            print(f"Error loading config {config} for {huggingface_id}: {e}", file=sys.stderr)
            continue # Move to the next config

        all_splits_metadata[config] = {}

        # This dataset seems to have splits directly
        print(f"'{config}' config loaded with splits: {dataset.keys()}")
        for split in dataset:
            print(f"Split '{split}' contains {len(dataset[split])} examples")
            all_splits_metadata[config][split] = len(dataset[split])

            # Save each split to the config's subdirectory
            output_path = os.path.join(config_dir, f"{dataset_name}_{config}_{split}.json")
            dataset[split].to_json(output_path)
            print(f"Saved {split} split to {output_path}")

            # Print the first example
            if len(dataset[split]) > 0:
                print(f"First example from '{split}' split:")
                print(dataset[split][0])
            print("-" * 50)


    # Save a main metadata file for the entire dataset
    metadata = {
        "huggingface_id": huggingface_id,
        "configs_downloaded": configs,
        "splits_info": all_splits_metadata
    }
    metadata_path = os.path.join(base_data_dir, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"\nOverall metadata saved to {metadata_path}")

    print(f"\n--- {dataset_name} download completed successfully! ---")

if __name__ == "__main__":
    download_aime_dataset() 