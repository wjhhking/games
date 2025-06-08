'use client';

import { useState } from 'react';
import { Question } from '../../data/exams';

interface ExamQuestionProps {
  question: Question;
  onAnswerSelected: (questionId: string, answer: string, isCorrect: boolean) => void;
  showExplanation: boolean;
  isSubmitted?: boolean;
  selectedAnswer?: string;
}

export default function ExamQuestion({
  question,
  onAnswerSelected,
  showExplanation,
  isSubmitted = false,
  selectedAnswer
}: ExamQuestionProps) {
  const [localSelectedAnswer, setLocalSelectedAnswer] = useState<string | undefined>(selectedAnswer);

  const handleAnswerSelect = (answer: string) => {
    if (isSubmitted) return;

    setLocalSelectedAnswer(answer);
    const isCorrect = answer === question.correctAnswer;
    onAnswerSelected(question.id, answer, isCorrect);
  };

  const getOptionClass = (option: string) => {
    if (!isSubmitted || !localSelectedAnswer) {
      return localSelectedAnswer === option
        ? 'bg-indigo-50 dark:bg-indigo-900 border-indigo-200 dark:border-indigo-800'
        : 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700';
    }

    if (option === question.correctAnswer) {
      return 'bg-green-50 dark:bg-green-900 border-green-200 dark:border-green-800';
    }

    if (localSelectedAnswer === option && option !== question.correctAnswer) {
      return 'bg-red-50 dark:bg-red-900 border-red-200 dark:border-red-800';
    }

    return 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700';
  };

  return (
    <div className="bg-white dark:bg-gray-800 shadow-sm rounded-lg overflow-hidden">
      <div className="p-6">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white">{question.text}</h3>

        <div className="mt-6 space-y-3">
          {Object.entries(question.options).map(([key, value]) => (
            <button
              key={key}
              onClick={() => handleAnswerSelect(key)}
              disabled={isSubmitted}
              className={`w-full text-left p-4 border rounded-md transition-colors ${getOptionClass(key)}`}
            >
              <div className="flex items-start">
                <span className="flex items-center justify-center h-6 w-6 rounded-full border border-gray-300 dark:border-gray-600 text-sm font-medium mr-3">
                  {key}
                </span>
                <span className="text-gray-900 dark:text-white">{value}</span>
              </div>
            </button>
          ))}
        </div>

        {showExplanation && isSubmitted && (
          <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900 rounded-md">
            <h4 className="font-semibold text-blue-800 dark:text-blue-200">Explanation</h4>
            <p className="mt-1 text-blue-700 dark:text-blue-300 text-sm">{question.explanation || 'No explanation available.'}</p>
          </div>
        )}

        {isSubmitted && (
          <div className="mt-6 flex items-center">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Correct answer: {question.correctAnswer}
            </span>
            <span className="ml-auto text-sm font-medium">
              {localSelectedAnswer === question.correctAnswer ? (
                <span className="text-green-600 dark:text-green-400">Correct</span>
              ) : (
                <span className="text-red-600 dark:text-red-400">Incorrect</span>
              )}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}