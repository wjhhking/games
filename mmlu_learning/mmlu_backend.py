#!/usr/bin/env python
import os
import json
import pandas as pd

class MMluLearningBackend:
    def __init__(self, data_dir="data"):
        """Initialize the MMLU learning backend."""
        self.data_dir = data_dir
        self.current_questions = None
        self.question_index = 0
        self.user_answers = []
        self.subject = None

    def load_subject(self, subject_name):
        """Load questions for a specific subject."""
        try:
            # Path to the MMLU test data
            file_path = os.path.join(self.data_dir, "mmlu_test.json")

            # Load the data - the JSON file might have lines of JSON objects
            # instead of a single JSON array
            data = []
            with open(file_path, 'r') as f:
                for line in f:
                    try:
                        # Try to parse each line as a separate JSON object
                        item = json.loads(line.strip())
                        data.append(item)
                    except json.JSONDecodeError:
                        # Skip lines that aren't valid JSON
                        continue

            if not data:
                # If that didn't work, try loading as a single JSON array
                with open(file_path, 'r') as f:
                    data = json.load(f)

            # Convert to DataFrame and filter for the specified subject
            df = pd.DataFrame(data)
            subject_df = df[df['subject'] == subject_name]

            if len(subject_df) == 0:
                raise ValueError(f"No {subject_name} questions found in the dataset")

            # Process the data into a consistent format
            processed_data = []
            for _, row in subject_df.iterrows():
                # Convert answer to the correct letter format
                # The dataset might use 0,1,2,3 or A,B,C,D formats
                answer = row['answer']

                # Check if answer is a number or starts with a number (like '0A')
                if isinstance(answer, int) or (isinstance(answer, str) and answer[0].isdigit()):
                    # Convert numerical answers to letters (0->A, 1->B, etc.)
                    if isinstance(answer, str) and answer[0].isdigit():
                        answer_index = int(answer[0])
                    else:
                        answer_index = int(answer)
                    answer_letter = chr(65 + answer_index)  # 65 is ASCII for 'A'
                else:
                    # If it's already a letter, just take the first character
                    answer_letter = answer[0] if answer else 'A'

                question_data = {
                    'question': row['question'],
                    'A': row['choices'][0],
                    'B': row['choices'][1],
                    'C': row['choices'][2],
                    'D': row['choices'][3],
                    'Answer': answer_letter
                }
                processed_data.append(question_data)

            # Store the processed questions
            self.current_questions = pd.DataFrame(processed_data)
            self.subject = subject_name
            self.question_index = 0
            self.user_answers = []

            return len(self.current_questions)

        except Exception as e:
            print(f"Error loading {subject_name} data: {str(e)}")
            # Let's print more diagnostic information
            print(f"File path: {os.path.join(self.data_dir, 'mmlu_test.json')}")
            print(f"Does file exist: {os.path.exists(os.path.join(self.data_dir, 'mmlu_test.json'))}")
            if os.path.exists(os.path.join(self.data_dir, 'mmlu_test.json')):
                with open(os.path.join(self.data_dir, 'mmlu_test.json'), 'r') as f:
                    first_line = f.readline()
                    print(f"First 100 chars of file: {first_line[:100]}")
            return 0

    def get_current_question(self):
        """Get the current question."""
        if self.current_questions is None or self.question_index >= len(self.current_questions):
            return None

        question_data = self.current_questions.iloc[self.question_index]

        return {
            "index": self.question_index,
            "question": question_data['question'],
            "options": {
                "A": question_data["A"],
                "B": question_data["B"],
                "C": question_data["C"],
                "D": question_data["D"]
            },
            "total_questions": len(self.current_questions)
        }

    def submit_answer(self, answer):
        """Submit an answer for the current question."""
        if self.current_questions is None:
            return {"error": "No subject loaded"}

        current_question = self.current_questions.iloc[self.question_index]
        correct_answer = current_question["Answer"]
        is_correct = answer == correct_answer

        self.user_answers.append({
            "question_index": self.question_index,
            "question": current_question['question'],
            "user_answer": answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })

        result = {
            "is_correct": is_correct,
            "correct_answer": correct_answer,
            "correct_text": current_question[correct_answer]
        }

        self.question_index += 1
        return result

    def get_results(self):
        """Get the results for the current session."""
        if not self.user_answers:
            return {"error": "No answers submitted yet"}

        total = len(self.user_answers)
        correct = sum(1 for answer in self.user_answers if answer["is_correct"])

        return {
            "subject": self.subject,
            "total": total,
            "correct": correct,
            "percentage": round(correct / total * 100, 2)
        }

    def reset(self):
        """Reset the current session."""
        self.question_index = 0
        self.user_answers = []

    def jump_to_question(self, question_index):
        """Jump to a specific question index (0-based)."""
        if self.current_questions is None:
            return False

        # Validate the question index
        if question_index < 0 or question_index >= len(self.current_questions):
            return False

        # If we're jumping to a question we haven't answered yet,
        # we need to clear answers for all questions after current index
        if question_index > self.question_index:
            # Keep only answers up to the current question
            self.user_answers = self.user_answers[:self.question_index]

        # Update the question index
        self.question_index = question_index
        return True

    def get_stats(self):
        """Get statistics about the current session."""
        if self.current_questions is None:
            return {
                "current_question": 0,
                "total_questions": 0,
                "correct_count": 0,
                "answered_count": 0
            }

        return {
            "current_question": self.question_index,
            "total_questions": len(self.current_questions),
            "correct_count": sum(1 for answer in self.user_answers if answer["is_correct"]),
            "answered_count": len(self.user_answers)
        }

if __name__ == "__main__":
    # Simple demo of the backend
    backend = MMluLearningBackend()

    # Load formal logic questions
    num_questions = backend.load_subject("formal_logic")
    print(f"Loaded {num_questions} formal_logic questions")

    if num_questions > 0:
        # Get and display the first question
        question = backend.get_current_question()
        print(f"\nQuestion {question['index'] + 1}/{question['total_questions']}:")
        print(question['question'])
        for opt, text in question['options'].items():
            print(f"{opt}. {text}")

        # Simulate answering
        answer = "A"
        result = backend.submit_answer(answer)

        print(f"\nYour answer: {answer}")
        print(f"Correct answer: {result['correct_answer']}")
        print(f"Result: {'Correct!' if result['is_correct'] else 'Incorrect.'}")
    else:
        print("No questions available. Make sure to download the MMLU dataset first.")