'use client';

import { useState, FormEvent } from 'react';
import { Concept } from '../../data/learning';
import { ActiveLearningFeedback } from '../../utils/ai';
import { APP_CONFIG } from '../../utils/config';

interface ActiveLearningFormProps {
  concept: Concept;
  onSubmit: (question: string, response: string) => Promise<ActiveLearningFeedback>;
}

export default function ActiveLearningForm({ concept, onSubmit }: ActiveLearningFormProps) {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<ActiveLearningFeedback | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (question.trim().length < 10) {
      setError('Please enter a more specific question (at least 10 characters).');
      return;
    }

    if (response.length < APP_CONFIG.learning.minUserInputLength) {
      setError(`Your response needs to be at least ${APP_CONFIG.learning.minUserInputLength} characters.`);
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);

      const result = await onSubmit(question, response);
      setFeedback(result);
    } catch (err) {
      setError('An error occurred while evaluating your response. Please try again.');
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const getFeedbackColor = () => {
    if (!feedback) return 'bg-gray-100 dark:bg-gray-800';

    const score = feedback.correctness;
    if (score >= APP_CONFIG.learning.feedbackThresholds.excellent) {
      return 'bg-green-50 dark:bg-green-900 border-green-200 dark:border-green-800';
    } else if (score >= APP_CONFIG.learning.feedbackThresholds.good) {
      return 'bg-blue-50 dark:bg-blue-900 border-blue-200 dark:border-blue-800';
    } else if (score >= APP_CONFIG.learning.feedbackThresholds.fair) {
      return 'bg-yellow-50 dark:bg-yellow-900 border-yellow-200 dark:border-yellow-800';
    } else {
      return 'bg-red-50 dark:bg-red-900 border-red-200 dark:border-red-800';
    }
  };

  return (
    <div className="mt-8 space-y-8">
      <div className="bg-white dark:bg-gray-800 shadow-sm rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white">Active Learning</h3>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Test your understanding by asking questions and providing explanations about this concept.
        </p>

        <form onSubmit={handleSubmit} className="mt-6 space-y-6">
          <div>
            <label htmlFor="question" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Your Question
            </label>
            <div className="mt-1">
              <input
                type="text"
                id="question"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask a specific question about this concept..."
                className="block w-full rounded-md border-gray-300 dark:border-gray-700 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-700 dark:text-white"
              />
            </div>
          </div>

          <div>
            <label htmlFor="response" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Your Response
            </label>
            <div className="mt-1">
              <textarea
                id="response"
                rows={6}
                value={response}
                onChange={(e) => setResponse(e.target.value)}
                placeholder="Explain the concept in your own words or answer your question based on what you've learned..."
                className="block w-full rounded-md border-gray-300 dark:border-gray-700 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-700 dark:text-white"
              />
            </div>
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
              {response.length}/{APP_CONFIG.learning.maxUserInputLength} characters
            </p>
          </div>

          {error && (
            <div className="p-4 bg-red-50 dark:bg-red-900 text-red-700 dark:text-red-100 rounded-md text-sm">
              {error}
            </div>
          )}

          <div>
            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? 'Evaluating...' : 'Submit for Evaluation'}
            </button>
          </div>
        </form>
      </div>

      {feedback && (
        <div className={`rounded-lg border p-6 ${getFeedbackColor()}`}>
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">AI Feedback</h3>
            <span className="text-sm font-semibold px-2.5 py-0.5 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-300">
              Score: {feedback.correctness}/100
            </span>
          </div>

          <div className="mt-4 text-gray-700 dark:text-gray-300">
            <h4 className="font-semibold mb-2">Feedback:</h4>
            <p className="text-sm whitespace-pre-line">{feedback.feedback}</p>
          </div>

          {feedback.misconceptions && feedback.misconceptions.length > 0 && (
            <div className="mt-4">
              <h4 className="font-semibold text-gray-700 dark:text-gray-300 mb-2">Misconceptions:</h4>
              <ul className="list-disc pl-5 text-sm text-gray-700 dark:text-gray-300 space-y-1">
                {feedback.misconceptions.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
          )}

          {feedback.suggestedResources && feedback.suggestedResources.length > 0 && (
            <div className="mt-4">
              <h4 className="font-semibold text-gray-700 dark:text-gray-300 mb-2">Suggested Resources:</h4>
              <ul className="list-disc pl-5 text-sm text-gray-700 dark:text-gray-300 space-y-1">
                {feedback.suggestedResources.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
          )}

          {feedback.nextSteps && feedback.nextSteps.length > 0 && (
            <div className="mt-4">
              <h4 className="font-semibold text-gray-700 dark:text-gray-300 mb-2">Next Steps:</h4>
              <ul className="list-disc pl-5 text-sm text-gray-700 dark:text-gray-300 space-y-1">
                {feedback.nextSteps.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="mt-6">
            <button
              onClick={() => {
                setFeedback(null);
                setQuestion('');
                setResponse('');
              }}
              className="px-4 py-2 bg-white dark:bg-gray-700 text-gray-700 dark:text-white text-sm font-medium rounded-md border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-600"
            >
              Try Another Question
            </button>
          </div>
        </div>
      )}
    </div>
  );
}