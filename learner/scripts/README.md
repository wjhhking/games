# Dataset Download Scripts

This directory contains Python scripts to download various benchmark datasets for training and evaluation.

## How to Run

First, ensure you have the necessary libraries installed:
```bash
# This command uses the --break-system-packages flag as requested.
# Be aware of the risks of modifying your system's Python packages.
pip3 install --break-system-packages -r requirements.txt
```

To download all datasets at once, run the main script. It will execute all other `download_*.py` scripts in this directory.
```bash
python3 learner/scripts/download_all.py
```
**Note**: Some datasets, like HLE, require you to be logged into a Hugging Face account. Run `huggingface-cli login` from your terminal before executing the scripts.

To download just one specific dataset, run its individual script from the `games` directory:
```bash
# Example for GSM8K
python3 learner/scripts/download_gsm8k.py
```

---

## Dataset Information

### MMLU
- **Script:** `download_mmlu.py`
- **Source:** `cais/mmlu`
- **Description:** The original MMLU (Massive Multitask Language Understanding) is a comprehensive benchmark designed to measure knowledge acquired during pretraining. It covers 57 diverse subjects across STEM, humanities, social sciences, and more, making it a key test of a model's world knowledge and problem-solving abilities.

### GPQA
- **Script:** `download_gpqa.py`
- **Source:** `idavidrein/gpqa`
- **Description:** GPQA (A Graduate-Level Google-Proof Q&A Benchmark) is a challenging dataset of 448 multiple-choice questions written by domain experts in biology, physics, and chemistry. The questions are designed to be difficult for both search engines and non-expert humans to answer.

### MATH
- **Script:** `download_math.py`
- **Source:** `EleutherAI/hendrycks_math`
- **Description:** This is a benchmark of 12,500 challenging competition mathematics problems. It covers subjects like algebra, geometry, number theory, and precalculus.

### AIME
- **Script:** `download_aime.py`
- **Source:** `opencompass/AIME2025`
- **Description:** This dataset contains the problems from the 2025 American Invitational Mathematics Examination (AIME I & II), providing a focused set of high-level math competition problems.

### HLE
- **Script:** `download_hle.py`
- **Source:** `cais/hle`
- **Description:** Humanity's Last Exam (HLE) is a multi-modal benchmark at the frontier of human knowledge. It consists of 2,500 questions across dozens of subjects, including mathematics, humanities, and the natural sciences, designed to be the final closed-ended academic benchmark of its kind.

### Diamond
- **Script:** `download_diamond.py`
- **Source:** `google/gemini-benchmark-2023` (diamond config)
- **Description:** A dataset of in-context reasoning problems where the task is to identify a single sentence in a provided text that does not belong with the others.

### GSM8K
- **Script:** `download_gsm8k.py`
- **Source:** `openai/gsm8k`
- **Description:** GSM8K (Grade School Math 8K) is a dataset of 8,500 high-quality and linguistically diverse grade school math word problems, created to measure a model's ability to perform multi-step mathematical reasoning.

### SWE-bench
- **Script:** `download_swe_bench.py`
- **Source:** `princeton-nlp/swe-bench`
- **Description:** SWE-bench is a software engineering benchmark that tasks language models with resolving real-world GitHub issues from popular Python projects. It provides a realistic test of a model's ability to understand and modify complex codebases.

### MMMU
- **Script:** `download_mmmu.py`
- **Source:** `MM-Upenn/MMMU`
- **Description:** The MMMU (A Massive, Multi-discipline, Multimodal Understanding and Reasoning) benchmark is a comprehensive test containing questions from various disciplines that require college-level knowledge. It is multimodal, incorporating images, diagrams, and formulas in its questions.
- **Important:** This script only downloads the question and answer metadata. The images must be downloaded separately by following the instructions on the [official MMMU GitHub repository](https://github.com/MM-Vid/MMMU).
