#!/usr/bin/env python
import os
import json
import pandas as pd

def prepare_data(data_dir="data", output_dir="public/data"):
    """Process MMLU data and save as static JSON files."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Path to the MMLU test data
    file_path = os.path.join(data_dir, "mmlu_test.json")

    try:
        # Load the data
        print(f"Loading data from {file_path}...")
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                # Try loading as JSONL if that fails
                f.seek(0)
                data = [json.loads(line) for line in f if line.strip()]

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Get unique subjects
        subjects = df['subject'].unique()
        print(f"Found {len(subjects)} subjects")

        # Process each subject
        for subject in subjects:
            subject_data = df[df['subject'] == subject]
            if len(subject_data) == 0:
                continue

            # Save subject data to JSON file
            output_file = os.path.join(output_dir, f"{subject}.json")
            subject_data.to_json(output_file, orient='records')
            print(f"Saved {len(subject_data)} questions for {subject}")

        # Create an index file with subject information
        subject_info = [
            {
                "id": subject,
                "name": subject.replace("_", " ").title(),
                "count": len(df[df['subject'] == subject])
            }
            for subject in subjects if len(df[df['subject'] == subject]) > 0
        ]

        with open(os.path.join(output_dir, "subjects.json"), 'w') as f:
            json.dump(subject_info, f)

        print("Data preparation complete!")

    except Exception as e:
        print(f"Error preparing data: {str(e)}")

if __name__ == "__main__":
    prepare_data()