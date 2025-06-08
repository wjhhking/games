export type Subject = {
  id: string;
  name: string;
  category: 'stem' | 'humanities' | 'social_sciences' | 'other';
  description: string;
  icon?: string;
};

export const subjects: Subject[] = [
  // STEM Subjects
  {
    id: 'high_school_biology',
    name: 'High School Biology',
    category: 'stem',
    description: 'Fundamental concepts in biology taught at the high school level.',
  },
  {
    id: 'high_school_chemistry',
    name: 'High School Chemistry',
    category: 'stem',
    description: 'Basic chemistry concepts including atomic structure, periodic table, and chemical reactions.',
  },
  {
    id: 'high_school_physics',
    name: 'High School Physics',
    category: 'stem',
    description: 'Core physics principles including mechanics, energy, and simple electrical concepts.',
  },
  {
    id: 'high_school_mathematics',
    name: 'High School Mathematics',
    category: 'stem',
    description: 'Mathematics topics covered in high school including algebra, geometry, and basic calculus.',
  },
  {
    id: 'college_biology',
    name: 'College Biology',
    category: 'stem',
    description: 'Advanced biological concepts including cell biology, genetics, and ecology.',
  },
  {
    id: 'college_chemistry',
    name: 'College Chemistry',
    category: 'stem',
    description: 'Advanced chemistry including organic chemistry, thermodynamics, and molecular structures.',
  },
  {
    id: 'college_physics',
    name: 'College Physics',
    category: 'stem',
    description: 'Advanced physics including quantum mechanics, electromagnetism, and thermodynamics.',
  },
  {
    id: 'college_mathematics',
    name: 'College Mathematics',
    category: 'stem',
    description: 'Advanced mathematics including calculus, linear algebra, and differential equations.',
  },
  {
    id: 'computer_science',
    name: 'Computer Science',
    category: 'stem',
    description: 'Principles of computing including algorithms, data structures, and programming concepts.',
  },
  {
    id: 'machine_learning',
    name: 'Machine Learning',
    category: 'stem',
    description: 'Concepts and algorithms in machine learning and artificial intelligence.',
  },
  {
    id: 'astronomy',
    name: 'Astronomy',
    category: 'stem',
    description: 'Study of celestial objects, space, and the physical universe as a whole.',
  },
  // Add more subjects as needed
];

export const getSubjectById = (id: string): Subject | undefined => {
  return subjects.find(subject => subject.id === id);
};

export const getStemSubjects = (): Subject[] => {
  return subjects.filter(subject => subject.category === 'stem');
};