export type Question = {
  id: string;
  subjectId: string;
  text: string;
  options: {
    A: string;
    B: string;
    C: string;
    D: string;
  };
  correctAnswer: 'A' | 'B' | 'C' | 'D';
  explanation?: string;
  difficulty: 'easy' | 'medium' | 'hard';
  tags?: string[];
};

export type Exam = {
  id: string;
  subjectId: string;
  title: string;
  description: string;
  questions: Question[];
  timeLimit?: number; // In minutes
  passingScore?: number; // Percentage
};

export type UserExamResult = {
  userId: string;
  examId: string;
  score: number;
  answers: {
    questionId: string;
    selectedAnswer: string;
    isCorrect: boolean;
  }[];
  startTime: Date;
  endTime: Date;
  completed: boolean;
};

// Sample questions based on MMLU
export const sampleQuestions: Question[] = [
  {
    id: 'q1_photosynthesis',
    subjectId: 'high_school_biology',
    text: 'Which of the following is NOT a product of photosynthesis?',
    options: {
      A: 'Oxygen',
      B: 'Glucose',
      C: 'Carbon dioxide',
      D: 'ATP',
    },
    correctAnswer: 'C',
    explanation: 'Carbon dioxide is a reactant in photosynthesis, not a product. The products of photosynthesis are oxygen, glucose, and ATP.',
    difficulty: 'easy',
    tags: ['photosynthesis', 'cellular processes']
  },
  {
    id: 'q2_newton_law',
    subjectId: 'high_school_physics',
    text: 'A 10 kg object is moving at a constant velocity of 5 m/s. What is the net force acting on the object?',
    options: {
      A: '50 N',
      B: '10 N',
      C: '5 N',
      D: '0 N',
    },
    correctAnswer: 'D',
    explanation: 'According to Newton\'s First Law, an object in motion stays in motion with the same speed and direction unless acted upon by an external force. Since the object is moving at a constant velocity, the net force must be zero.',
    difficulty: 'medium',
    tags: ['newton\'s laws', 'forces']
  },
  {
    id: 'q3_periodic_table',
    subjectId: 'high_school_chemistry',
    text: 'Which element has the highest electronegativity?',
    options: {
      A: 'Oxygen',
      B: 'Chlorine',
      C: 'Fluorine',
      D: 'Nitrogen',
    },
    correctAnswer: 'C',
    explanation: 'Fluorine has the highest electronegativity of all elements in the periodic table.',
    difficulty: 'medium',
    tags: ['periodic table', 'electronegativity']
  }
];

// Sample exams
export const sampleExams: Exam[] = [
  {
    id: 'exam_bio_1',
    subjectId: 'high_school_biology',
    title: 'Biology Fundamentals',
    description: 'Test your knowledge of basic biological concepts.',
    questions: sampleQuestions.filter(q => q.subjectId === 'high_school_biology'),
    timeLimit: 30,
    passingScore: 70
  },
  {
    id: 'exam_physics_1',
    subjectId: 'high_school_physics',
    title: 'Physics: Mechanics',
    description: 'Test your understanding of basic mechanics concepts.',
    questions: sampleQuestions.filter(q => q.subjectId === 'high_school_physics'),
    timeLimit: 45,
    passingScore: 65
  }
];

// Function to get exams by subject
export const getExamsBySubject = (subjectId: string): Exam[] => {
  return sampleExams.filter(exam => exam.subjectId === subjectId);
};

// Function to shuffle question options (for ABCD)
export const shuffleOptions = (question: Question): Question => {
  const options = Object.entries(question.options);
  const shuffledEntries = [...options].sort(() => Math.random() - 0.5);

  const originalCorrectAnswerText = question.options[question.correctAnswer];
  const shuffledOptions = Object.fromEntries(shuffledEntries) as typeof question.options;

  // Find the new key for the correct answer
  const newCorrectAnswer = Object.entries(shuffledOptions).find(
    ([_, value]) => value === originalCorrectAnswerText
  )?.[0] as 'A' | 'B' | 'C' | 'D';

  return {
    ...question,
    options: shuffledOptions,
    correctAnswer: newCorrectAnswer
  };
};