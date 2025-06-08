from datasets import load_dataset
import os
import json

# Create a data directory if it doesn't exist
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

# Load the MMLU dataset with the 'all' config
mmlu_dataset = load_dataset("cais/mmlu", "all")

# Print info about the dataset
print(f"MMLU dataset loaded with the following splits: {mmlu_dataset.keys()}")
for split in mmlu_dataset:
    print(f"Split '{split}' contains {len(mmlu_dataset[split])} examples")

    # Save each split to the data directory
    output_path = os.path.join(data_dir, f"mmlu_{split}.json")
    mmlu_dataset[split].to_json(output_path)
    print(f"Saved {split} split to {output_path}")

    # Print the first example
    print(f"First example from '{split}' split:")
    print(mmlu_dataset[split][0])
    print("-" * 50)

# Also save a metadata file with information about the dataset
subjects = set()
for split in mmlu_dataset:
    if "subject" in mmlu_dataset[split].features:
        subjects.update(set(mmlu_dataset[split]["subject"]))

metadata = {
    "splits": {split: len(mmlu_dataset[split]) for split in mmlu_dataset},
    "subjects": sorted(list(subjects)) if subjects else "No subject field found"
}

with open(os.path.join(data_dir, "metadata.json"), "w") as f:
    json.dump(metadata, f, indent=2)

print(f"All MMLU data has been saved to the '{data_dir}' folder")
print("Script completed successfully!")
