import { notFound } from 'next/navigation';
import Link from 'next/link';
import Layout from '../../components/Layout';
import { getSubjectById } from '../../data/subjects';
import { getConceptsBySubject } from '../../data/learning';
import { getExamsBySubject } from '../../data/exams';

export default function SubjectPage({ params }: { params: { id: string } }) {
  const subject = getSubjectById(params.id);

  if (!subject) {
    return notFound();
  }

  const concepts = getConceptsBySubject(subject.id);
  const exams = getExamsBySubject(subject.id);

  return (
    <Layout>
      <div className="bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto py-16 px-4 sm:px-6 lg:py-20 lg:px-8">
          <div className="lg:grid lg:grid-cols-3 lg:gap-8">
            <div>
              <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white">
                {subject.name}
              </h1>
              <p className="mt-4 text-lg text-gray-500 dark:text-gray-300">
                {subject.description}
              </p>

              <div className="mt-6 flex flex-col space-y-3">
                <Link
                  href={`/learn?subject=${subject.id}`}
                  className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Start Learning
                </Link>

                <Link
                  href={`/exams?subject=${subject.id}`}
                  className="inline-flex items-center justify-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md shadow-sm text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Take Exam
                </Link>
              </div>
            </div>

            <div className="mt-12 lg:mt-0 lg:col-span-2">
              <div className="space-y-8">
                {/* Concepts Section */}
                <div>
                  <h2 className="text-xl font-bold text-gray-900 dark:text-white">Key Concepts</h2>

                  {concepts.length > 0 ? (
                    <ul className="mt-4 space-y-4">
                      {concepts.map(concept => (
                        <li key={concept.id} className="border-l-4 border-indigo-500 pl-4">
                          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                            {concept.title}
                          </h3>
                          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                            {concept.description}
                          </p>
                          <span className="mt-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 dark:bg-indigo-800 text-indigo-800 dark:text-indigo-200">
                            {concept.difficulty}
                          </span>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="mt-4 text-gray-500 dark:text-gray-400">
                      No concepts available for this subject yet.
                    </p>
                  )}
                </div>

                {/* Exams Section */}
                <div>
                  <h2 className="text-xl font-bold text-gray-900 dark:text-white">Available Exams</h2>

                  {exams.length > 0 ? (
                    <ul className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
                      {exams.map(exam => (
                        <li key={exam.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                            {exam.title}
                          </h3>
                          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                            {exam.description}
                          </p>
                          <div className="mt-4 flex items-center text-sm text-gray-500 dark:text-gray-400">
                            <span className="mr-4">{exam.questions.length} questions</span>
                            {exam.timeLimit && <span>{exam.timeLimit} minutes</span>}
                          </div>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="mt-4 text-gray-500 dark:text-gray-400">
                      No exams available for this subject yet.
                    </p>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}