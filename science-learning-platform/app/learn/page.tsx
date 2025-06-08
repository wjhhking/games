'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import Layout from '../components/Layout';
import ActiveLearningForm from '../components/learning/ActiveLearningForm';
import { getSubjectById } from '../data/subjects';
import { getConceptsBySubject, Concept } from '../data/learning';
import { ActiveLearningFeedback } from '../utils/ai';

export default function LearnPage() {
  const searchParams = useSearchParams();
  const subjectId = searchParams.get('subject');
  const conceptId = searchParams.get('concept');

  const [selectedSubject, setSelectedSubject] = useState(subjectId || '');
  const [selectedConcept, setSelectedConcept] = useState<Concept | null>(null);
  const [concepts, setConcepts] = useState<Concept[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load concepts when subject changes
  useEffect(() => {
    if (selectedSubject) {
      const subjectConcepts = getConceptsBySubject(selectedSubject);
      setConcepts(subjectConcepts);

      // If conceptId is provided, select that concept
      if (conceptId) {
        const concept = subjectConcepts.find(c => c.id === conceptId);
        if (concept) {
          setSelectedConcept(concept);
        } else {
          setError(`Concept with ID '${conceptId}' not found`);
        }
      } else if (subjectConcepts.length > 0) {
        // Otherwise select the first concept
        setSelectedConcept(subjectConcepts[0]);
      } else {
        setSelectedConcept(null);
        setError('No concepts found for this subject');
      }
    } else {
      setConcepts([]);
      setSelectedConcept(null);
    }
  }, [selectedSubject, conceptId]);

  const handleSubjectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedSubject(e.target.value);
  };

  const handleConceptChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const concept = concepts.find(c => c.id === e.target.value);
    setSelectedConcept(concept || null);
  };

  const handleSubmitResponse = async (question: string, response: string): Promise<ActiveLearningFeedback> => {
    if (!selectedConcept) {
      throw new Error('No concept selected');
    }

    setLoading(true);
    setError(null);

    try {
      const res = await fetch('/api/learning/evaluate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conceptId: selectedConcept.id,
          question,
          response,
        }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || 'Failed to evaluate response');
      }

      return await res.json();
    } catch (err: any) {
      setError(err.message || 'An error occurred');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8">
          <div className="lg:grid lg:grid-cols-12 lg:gap-8">
            <div className="lg:col-span-3">
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                Active Learning
              </h1>
              <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                Select a subject and concept to start learning actively.
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
                      { id: 'college_biology', name: 'College Biology' },
                      { id: 'college_physics', name: 'College Physics' },
                      { id: 'college_chemistry', name: 'College Chemistry' },
                    ].map(subject => (
                      <option key={subject.id} value={subject.id}>
                        {subject.name}
                      </option>
                    ))}
                  </select>
                </div>

                {selectedSubject && (
                  <div>
                    <label htmlFor="concept" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                      Concept
                    </label>
                    <select
                      id="concept"
                      name="concept"
                      className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                      value={selectedConcept?.id || ''}
                      onChange={handleConceptChange}
                    >
                      <option value="">Select a concept</option>
                      {concepts.map(concept => (
                        <option key={concept.id} value={concept.id}>
                          {concept.title}
                        </option>
                      ))}
                    </select>
                  </div>
                )}
              </div>
            </div>

            <div className="mt-12 lg:mt-0 lg:col-span-9">
              {selectedConcept ? (
                <div>
                  <div className="bg-white dark:bg-gray-800 shadow overflow-hidden sm:rounded-lg">
                    <div className="px-4 py-5 sm:px-6">
                      <h2 className="text-lg leading-6 font-medium text-gray-900 dark:text-white">
                        {selectedConcept.title}
                      </h2>
                      <p className="mt-1 max-w-2xl text-sm text-gray-500 dark:text-gray-400">
                        {selectedConcept.description}
                      </p>
                      <span className="mt-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 dark:bg-indigo-800 text-indigo-800 dark:text-indigo-200">
                        {selectedConcept.difficulty}
                      </span>
                    </div>
                    <div className="border-t border-gray-200 dark:border-gray-700 px-4 py-5 sm:p-6">
                      <div className="prose prose-indigo dark:prose-invert max-w-none">
                        <div className="whitespace-pre-line">
                          {selectedConcept.content}
                        </div>

                        {selectedConcept.equations && selectedConcept.equations.length > 0 && (
                          <div className="mt-6">
                            <h3 className="text-lg font-medium text-gray-900 dark:text-white">Key Equations</h3>
                            <ul className="mt-2 space-y-2">
                              {selectedConcept.equations.map((equation, index) => (
                                <li key={index} className="bg-gray-50 dark:bg-gray-700 p-2 rounded font-mono">
                                  {equation}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {selectedConcept.examples && selectedConcept.examples.length > 0 && (
                          <div className="mt-6">
                            <h3 className="text-lg font-medium text-gray-900 dark:text-white">Examples</h3>
                            <ul className="mt-2 space-y-2">
                              {selectedConcept.examples.map((example, index) => (
                                <li key={index} className="text-gray-700 dark:text-gray-300">
                                  {example}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  <ActiveLearningForm
                    concept={selectedConcept}
                    onSubmit={handleSubmitResponse}
                  />
                </div>
              ) : (
                <div className="text-center py-12">
                  {error ? (
                    <div className="text-red-500 dark:text-red-400">
                      {error}
                    </div>
                  ) : selectedSubject ? (
                    <p className="text-gray-500 dark:text-gray-400">
                      No concept selected. Please select a concept from the menu.
                    </p>
                  ) : (
                    <p className="text-gray-500 dark:text-gray-400">
                      Please select a subject to start learning.
                    </p>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}