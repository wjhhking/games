#!/usr/bin/env python
import os
import json
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from tabulate import tabulate

def load_json_data(file_path):
    """Load JSON data from a file, handling both line-by-line and array formats."""
    try:
        # First try to load as a complete JSON array
        with open(file_path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # If that fails, try line-by-line parsing
                f.seek(0)  # Reset file pointer to beginning
                data = []
                for line in f:
                    try:
                        item = json.loads(line.strip())
                        data.append(item)
                    except json.JSONDecodeError:
                        continue
                return data
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")
        return []

def analyze_file(file_path):
    """Analyze a single MMLU data file."""
    print(f"\nAnalyzing {file_path}...")
    data = load_json_data(file_path)

    if not data:
        print(f"  No data found or could not parse {file_path}")
        return None

    print(f"  Total questions: {len(data)}")

    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(data)

    # Count questions by subject
    if 'subject' in df.columns:
        subject_counts = df['subject'].value_counts().to_dict()
        print(f"  Number of subjects: {len(subject_counts)}")

        # Create a table of subject counts
        subject_table = [(subject, count) for subject, count in subject_counts.items()]
        subject_table.sort(key=lambda x: x[1], reverse=True)  # Sort by count descending

        print("\n  Questions per Subject:")
        print(tabulate(subject_table, headers=["Subject", "Count"], tablefmt="plain"))

        return {
            "file_name": os.path.basename(file_path),
            "total_questions": len(data),
            "total_subjects": len(subject_counts),
            "subject_counts": subject_counts
        }
    else:
        print("  No 'subject' column found in the data")
        return {
            "file_name": os.path.basename(file_path),
            "total_questions": len(data),
            "total_subjects": 0,
            "subject_counts": {}
        }

def plot_subjects_distribution(results):
    """Plot the distribution of questions across subjects in all files."""
    # Combine subject counts from all files
    all_subjects = Counter()
    for result in results:
        if result and "subject_counts" in result:
            all_subjects.update(result["subject_counts"])

    # Sort by count and get top 20 for better visualization
    top_subjects = dict(sorted(all_subjects.items(), key=lambda x: x[1], reverse=True)[:20])

    # Create a bar chart
    plt.figure(figsize=(15, 8))
    plt.bar(top_subjects.keys(), top_subjects.values(), color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.title('Number of Questions per Subject (Top 20)')
    plt.xlabel('Subject')
    plt.ylabel('Number of Questions')
    plt.tight_layout()

    # Save the plot
    plot_path = "subject_distribution.png"
    plt.savefig(plot_path)
    print(f"\nPlot saved to {plot_path}")

    # Try to display the plot if running in an interactive environment
    try:
        plt.show()
    except:
        pass

def analyze_mmlu_data(data_dir="data"):
    """Analyze all MMLU data files in the specified directory."""
    print(f"Analyzing MMLU data in '{data_dir}'...")

    # Identify MMLU data files
    mmlu_files = [
        os.path.join(data_dir, "mmlu_test.json"),
        os.path.join(data_dir, "mmlu_validation.json"),
        os.path.join(data_dir, "mmlu_dev.json"),
        os.path.join(data_dir, "mmlu_auxiliary_train.json")
    ]

    # Analyze metadata
    metadata_path = os.path.join(data_dir, "metadata.json")
    try:
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            print("\nMetadata:")
            print(f"  Splits: {metadata.get('splits', {})}")
            print(f"  Total subjects: {len(metadata.get('subjects', []))}")
            print("  Subjects:")
            for subject in metadata.get('subjects', []):
                if subject:  # Skip empty subject string
                    print(f"    - {subject}")
    except Exception as e:
        print(f"Error loading metadata: {str(e)}")

    # Analyze each file
    results = []
    for file_path in mmlu_files:
        if os.path.exists(file_path):
            result = analyze_file(file_path)
            if result:
                results.append(result)
        else:
            print(f"\n{file_path} does not exist, skipping.")

    # Summary table
    print("\nSummary of MMLU Dataset:")
    summary_table = []
    for result in results:
        summary_table.append([
            result["file_name"],
            result["total_questions"],
            result["total_subjects"]
        ])

    print(tabulate(summary_table, headers=["File", "Questions", "Subjects"], tablefmt="grid"))

    # Plot subject distribution
    plot_subjects_distribution(results)

    return results

if __name__ == "__main__":
    analyze_mmlu_data()