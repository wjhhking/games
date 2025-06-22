import os
import json
import sys
from collections import defaultdict
from datasets import load_dataset
from PIL import Image

def download_hle_dataset():
    """
    Downloads the HLE (Humanity's Last Exam) dataset from cais/hle,
    processes the images, and saves the problems into separate JSON
    files based on their category.

    NOTE: This dataset requires authentication with a Hugging Face account.
    Please run `huggingface-cli login` from your terminal first.
    """
    # --- Configuration ---
    dataset_name = "hle"
    huggingface_id = "cais/hle"
    # ---------------------

    print(f"--- Starting download for {dataset_name} ({huggingface_id}) ---")
    print("--- This dataset requires you to be logged into Hugging Face. ---")

    # Construct absolute path to the data directory from the project root (games/)
    project_root = os.getcwd()
    data_dir = os.path.join(project_root, "learner", "data", dataset_name)
    images_dir = os.path.join(data_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    print(f"Data will be saved in: {data_dir}")
    print(f"Images will be saved in: {images_dir}")

    # Load the dataset
    try:
        dataset = load_dataset(huggingface_id, split="test")
    except Exception as e:
        print(f"Error loading dataset {huggingface_id}: {e}", file=sys.stderr)
        print("Please ensure you are logged into your Hugging Face account (`huggingface-cli login`).", file=sys.stderr)
        return

    print(f"\n'{dataset_name}' dataset loaded successfully with {len(dataset)} examples.")

    # Process and group problems by category
    categorized_problems = defaultdict(list)
    for i, record in enumerate(dataset):
        processed_record = dict(record)

        if 'image' in processed_record:
            del processed_record['image']

        for key, value in record.items():
            if isinstance(value, Image.Image):
                image_filename = f"image_{i}_{key}.jpg"
                image_path = os.path.join(images_dir, image_filename)
                value.convert('RGB').save(image_path)
                processed_record[key] = os.path.join("images", image_filename)
        
        category = processed_record.get('category', 'Uncategorized')
        categorized_problems[category].append(processed_record)
    
    # Save each category to its own JSON file
    print("\nSaving problems by category...")
    for category, problems in categorized_problems.items():
        # Sanitize category name for use as a filename
        safe_category_name = "".join(c for c in category if c.isalnum() or c in (' ', '_')).rstrip()
        output_filename = f"{safe_category_name}.json"
        output_path = os.path.join(data_dir, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(problems, f, ensure_ascii=True, indent=2)
        print(f"  - Saved {len(problems)} problems to {output_path}")

    # Save a metadata file with category info
    category_info = [
        {"name": cat, "count": len(probs)}
        for cat, probs in categorized_problems.items()
    ]
    
    metadata = {
        "huggingface_id": huggingface_id,
        "huggingface_config": None,
        "total_problems": len(dataset),
        "categories": category_info,
        "notes": "Image data has been extracted and saved into the 'images' subdirectory."
    }
    metadata_path = os.path.join(data_dir, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"\nOverall metadata saved to {metadata_path}")

    print(f"\n--- {dataset_name} download completed successfully! ---")

if __name__ == "__main__":
    download_hle_dataset() 