import os
import json
import sys
from datasets import load_dataset

def download_gpqa_dataset():
    """
    Downloads the GPQA dataset from idavidrein/gpqa by iterating through
    all available configurations (CSV files).
    """
    # --- Configuration ---
    dataset_name = "gpqa"
    huggingface_id = "idavidrein/gpqa"
    configs = ['gpqa_extended', 'gpqa_main', 'gpqa_diamond', 'gpqa_experts']
    # ---------------------

    print(f"--- Starting download for {dataset_name} ({huggingface_id}) ---")

    # Construct absolute path to the data directory from the project root (games/)
    project_root = os.getcwd()
    data_dir = os.path.join(project_root, "learner", "data", dataset_name)
    os.makedirs(data_dir, exist_ok=True)
    print(f"Data will be saved in: {data_dir}")

    all_splits_metadata = {}

    # Loop through each configuration and download it
    for config in configs:
        print(f"\n{'='*10} Downloading config: {config} {'='*10}")

        try:
            # Each config corresponds to a CSV file and is loaded as a DatasetDict
            dataset_dict = load_dataset(huggingface_id, config)
        except Exception as e:
            print(f"Error loading config {config} for {huggingface_id}: {e}", file=sys.stderr)
            continue # Move to the next config

        # Process each split within the loaded configuration (usually just 'train')
        for split_name, dataset in dataset_dict.items():
            print(f"  Processing split '{split_name}' from config '{config}'...")
            print(f"  Split contains {len(dataset)} examples")

            # Save the file using the config name for clarity (e.g., 'gpqa_main.json')
            output_filename = f"{config}.json"
            output_path = os.path.join(data_dir, output_filename)
            
            dataset.to_json(output_path)
            print(f"  Saved data to {output_path}")

            if config not in all_splits_metadata:
                all_splits_metadata[config] = {}
            all_splits_metadata[config][split_name] = len(dataset)

            if len(dataset) > 0:
                print(f"  First example:")
                print(dataset[0])
            print("-" * 50)

    # Save a main metadata file for the entire dataset
    metadata = {
        "huggingface_id": huggingface_id,
        "configs_downloaded": configs,
        "splits_info": all_splits_metadata
    }
    metadata_path = os.path.join(data_dir, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"\nOverall metadata saved to {metadata_path}")

    print(f"\n--- {dataset_name} download completed successfully! ---")

if __name__ == "__main__":
    download_gpqa_dataset() 