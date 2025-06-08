import Link from 'next/link';
import Layout from '../components/Layout';
import { subjects, Subject } from '../data/subjects';
import { SUBJECT_CATEGORIES } from '../utils/config';

export default function SubjectsPage() {
  // Group subjects by category
  const subjectsByCategory = subjects.reduce<Record<string, Subject[]>>((acc, subject) => {
    if (!acc[subject.category]) {
      acc[subject.category] = [];
    }
    acc[subject.category].push(subject);
    return acc;
  }, {});

  return (
    <Layout>
      <div className="bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto py-16 px-4 sm:px-6 lg:py-20 lg:px-8">
          <div className="lg:grid lg:grid-cols-3 lg:gap-8">
            <div>
              <h2 className="text-3xl font-extrabold text-gray-900 dark:text-white">
                Explore Subjects
              </h2>
              <p className="mt-4 text-lg text-gray-500 dark:text-gray-300">
                Browse our comprehensive collection of science subjects based on the Massive Multitask Language Understanding (MMLU) benchmark. Choose a subject to start learning.
              </p>
            </div>
            <div className="mt-12 lg:mt-0 lg:col-span-2">
              <dl className="space-y-12">
                {Object.entries(subjectsByCategory).map(([category, categorySubjects]) => (
                  <div key={category}>
                    <dt className="text-lg leading-6 font-medium text-gray-900 dark:text-white">
                      {SUBJECT_CATEGORIES[category as keyof typeof SUBJECT_CATEGORIES]}
                    </dt>
                    <dd className="mt-4">
                      <ul className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                        {categorySubjects.map((subject) => (
                          <li key={subject.id}>
                            <Link
                              href={`/subjects/${subject.id}`}
                              className="block p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                            >
                              <div className="flex items-center">
                                <div className="flex-shrink-0 h-10 w-10 flex items-center justify-center rounded-md bg-indigo-500 text-white">
                                  {subject.icon || subject.name.charAt(0)}
                                </div>
                                <div className="ml-4">
                                  <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                                    {subject.name}
                                  </h3>
                                  <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                                    {subject.description}
                                  </p>
                                </div>
                              </div>
                            </Link>
                          </li>
                        ))}
                      </ul>
                    </dd>
                  </div>
                ))}
              </dl>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}