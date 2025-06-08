#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from mmlu_backend import MMluLearningBackend

app = Flask(__name__)
app.secret_key = 'mmlu_secret_key'  # For flash messages

# Initialize the backend
backend = MMluLearningBackend()

@app.route('/')
def index():
    """Main page with subject selection."""
    # List of available subjects from metadata.json
    subjects = [
        "abstract_algebra", "anatomy", "astronomy", "business_ethics", "clinical_knowledge",
        "college_biology", "college_chemistry", "college_computer_science", "college_mathematics",
        "college_medicine", "college_physics", "computer_security", "conceptual_physics",
        "econometrics", "electrical_engineering", "elementary_mathematics", "formal_logic",
        "global_facts", "high_school_biology", "high_school_chemistry", "high_school_computer_science",
        "high_school_european_history", "high_school_geography", "high_school_government_and_politics",
        "high_school_macroeconomics", "high_school_mathematics", "high_school_microeconomics",
        "high_school_physics", "high_school_psychology", "high_school_statistics",
        "high_school_us_history", "high_school_world_history", "human_aging", "human_sexuality",
        "international_law", "jurisprudence", "logical_fallacies", "machine_learning",
        "management", "marketing", "medical_genetics", "miscellaneous", "moral_disputes",
        "moral_scenarios", "nutrition", "philosophy", "prehistory", "professional_accounting",
        "professional_law", "professional_medicine", "professional_psychology", "public_relations",
        "security_studies", "sociology", "us_foreign_policy", "virology", "world_religions"
    ]

    return render_template('index.html', subjects=subjects)

@app.route('/load_subject', methods=['POST'])
def load_subject():
    """Load a specific subject."""
    subject = request.form.get('subject')
    if not subject:
        flash('Please select a subject')
        return redirect(url_for('index'))

    num_questions = backend.load_subject(subject)
    if num_questions == 0:
        flash(f'Failed to load questions for {subject}')
        return redirect(url_for('index'))

    # Reset the session and redirect to the first question
    backend.reset()
    return redirect(url_for('question'))

@app.route('/question')
def question():
    """Display the current question."""
    question_data = backend.get_current_question()

    if not question_data:
        # If there are no more questions, show results
        flash('All questions completed!')
        return redirect(url_for('results'))

    return render_template('question.html', question=question_data)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """Submit an answer for the current question."""
    answer = request.form.get('answer')
    if not answer:
        flash('Please select an answer')
        return redirect(url_for('question'))

    result = backend.submit_answer(answer)
    # Pass the backend object to the template
    return render_template('result.html', result=result, answer=answer, backend=backend)

@app.route('/next_question')
def next_question():
    """Move to the next question."""
    return redirect(url_for('question'))

@app.route('/jump_question', methods=['POST'])
def jump_question():
    """Jump to a specific question."""
    question_number = request.form.get('question_number')
    try:
        question_number = int(question_number)
        if backend.jump_to_question(question_number - 1):  # Convert to 0-based index
            return redirect(url_for('question'))
        else:
            flash(f'Invalid question number: {question_number}')
    except ValueError:
        flash('Please enter a valid question number')

    return redirect(url_for('question'))

@app.route('/results')
def results():
    """Show the final results."""
    results = backend.get_results()
    return render_template('results.html', results=results)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)

    # In development
    app.run(debug=True)
else:
    # In production
    # Disable debugging
    app.debug = False
    # Use a secure secret key in production
    app.secret_key = os.environ.get('SECRET_KEY', 'mmlu_secret_key')