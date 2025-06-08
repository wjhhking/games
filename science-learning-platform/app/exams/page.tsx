'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import Layout from '../components/Layout';
import ExamQuestion from '../components/exam/ExamQuestion';
import { getSubjectById } from '../data/subjects';
import { getExamsBySubject, Exam, shuffleOptions, Question } from '../data/exams';
import { DEFAULT_USER_SETTINGS } from '../utils/config';

export default function ExamsPage() {
  const searchParams = useSearchParams();
  const subjectId = searchParams.get('subject');
  const examId = searchParams.get('exam');

  const [selectedSubject, setSelectedSubject] = useState(subjectId || '');
  const [exams, setExams] = useState<Exam[]>([]);
  const [selectedExam, setSelectedExam] = useState<Exam | null>(null);
  const [shuffledQuestions, setShuffledQuestions] = useState<Question[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState<Record<string, string>>({});
  const [isExamSubmitted, setIsExamSubmitted] = useState(false);
  const [examResult, setExamResult] = useState<any>(null);
  const [timeRemaining, setTimeRemaining] = useState<number | null>(null);
  const [isExamStarted, setIsExamStarted] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Load exams when subject changes
  useEffect(() => {
    if (selectedSubject) {
      const subjectExams = getExamsBySubject(selectedSubject);
      setExams(subjectExams);

      // If examId is provided, select that exam
      if (examId) {
        const exam = subjectExams.find(e => e.id === examId);
        if (exam) {
          setSelectedExam(exam);
        } else {
          setError(`Exam with ID '${examId}' not found`);
        }
      } else if (subjectExams.length > 0) {
        // Otherwise select the first exam
        setSelectedExam(subjectExams[0]);
      } else {
        setSelectedExam(null);
        setError('No exams found for this subject');
      }
    } else {
      setExams([]);
      setSelectedExam(null);
    }
  }, [selectedSubject, examId]);

  // Set up shuffled questions when exam is selected
  useEffect(() => {
    if (selectedExam) {
      // Shuffle the options for each question
      const shuffled = selectedExam.questions.map(question => shuffleOptions(question));
      setShuffledQuestions(shuffled);
      setUserAnswers({});
      setIsExamSubmitted(false);
      setExamResult(null);
      setCurrentQuestionIndex(0);
      setIsExamStarted(false);

      if (selectedExam.timeLimit) {
        setTimeRemaining(selectedExam.timeLimit * 60); // Convert minutes to seconds
      } else {
        setTimeRemaining(null);
      }
    }
  }, [selectedExam]);

  // Timer countdown
  useEffect(() => {
    if (!isExamStarted || timeRemaining === null) return;

    const timer = setInterval(() => {
      setTimeRemaining(prev => {
        if (prev === null || prev <= 1) {
          clearInterval(timer);
          if (prev === 1) {
            handleSubmitExam();
          }
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [isExamStarted, timeRemaining]);

  const handleSubjectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedSubject(e.target.value);
  };

  const handleExamChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const exam = exams.find(exam => exam.id === e.target.value);
    setSelectedExam(exam || null);
  };

  const handleStartExam = () => {
    setIsExamStarted(true);
  };

  const handleAnswerSelected = (questionId: string, answer: string, isCorrect: boolean) => {
    setUserAnswers(prev => ({
      ...prev,
      [questionId]: answer,
    }));
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < shuffledQuestions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const handlePrevQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleSubmitExam = async () => {
    if (!selectedExam) return;

    setLoading(true);
    setError(null);

    try {
      // Format answers for the API
      const formattedAnswers = Object.entries(userAnswers).map(([questionId, selectedAnswer]) => ({
        questionId,
        selectedAnswer,
      }));

      const res = await fetch('/api/exams/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          examId: selectedExam.id,
          answers: formattedAnswers,
        }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || 'Failed to analyze exam results');
      }

      const result = await res.json();
      setExamResult(result);
      setIsExamSubmitted(true);
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds: number): string => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  return (
    <Layout>
      <div className="bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8">
          {!isExamStarted ? (
            <div className="lg:grid lg:grid-cols-12 lg:gap-8">
              <div className="lg:col-span-4">
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                  Exams
                </h1>
                <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                  Test your knowledge with multiple-choice questions.
                </p>

                <div className="mt-6 space-y-6">
                  <div>
                    <label htmlFor="subject" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      Subject
                    </label>
                    <select
                      id="subject"
                      name="subject"
                      className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                      value={selectedSubject}
                      onChange={handleSubjectChange}
                    >
                      <option value="">Select a subject</option>
                      {[
                        { id: 'high_school_biology', name: 'High School Biology' },
                        { id: 'high_school_physics', name: 'High School Physics' },
                        { id: 'high_school_chemistry', name: 'High School Chemistry' },
                      ].map(subject => (
                        <option key={subject.id} value={subject.id}>
                          {subject.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  {selectedSubject && (
                    <div>
                      <label htmlFor="exam" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                        Exam
                      </label>
                      <select
                        id="exam"
                        name="exam"
                        className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                        value={selectedExam?.id || ''}
                        onChange={handleExamChange}
                      >
                        <option value="">Select an exam</option>
                        {exams.map(exam => (
                          <option key={exam.id} value={exam.id}>
                            {exam.title}
                          </option>
                        ))}
                      </select>
                    </div>
                  )}
                </div>
              </div>

              <div className="mt-12 lg:mt-0 lg:col-span-8">
                {selectedExam ? (
                  <div className="bg-white dark:bg-gray-800 shadow overflow-hidden sm:rounded-lg">
                    <div className="px-4 py-5 sm:px-6">
                      <h2 className="text-lg leading-6 font-medium text-gray-900 dark:text-white">
                        {selectedExam.title}
                      </h2>
                      <p className="mt-1 max-w-2xl text-sm text-gray-500 dark:text-gray-400">
                        {selectedExam.description}
                      </p>
                    </div>
                    <div className="border-t border-gray-200 dark:border-gray-700 px-4 py-5 sm:p-6">
                      <dl className="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2">
                        <div className="sm:col-span-1">
                          <dt
</rewritten_file>