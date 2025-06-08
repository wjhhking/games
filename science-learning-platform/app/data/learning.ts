export type Concept = {
  id: string;
  subjectId: string;
  title: string;
  description: string;
  content: string;
  examples?: string[];
  equations?: string[];
  diagrams?: string[];
  difficulty: 'beginner' | 'intermediate' | 'advanced';
};

export type UserProgress = {
  userId: string;
  conceptId: string;
  completed: boolean;
  score?: number;
  lastAttempt?: Date;
  notes?: string;
};

export type LearningSession = {
  id: string;
  userId: string;
  subjectId: string;
  conceptIds: string[];
  startTime: Date;
  endTime?: Date;
  active: boolean;
  progress: number; // Percentage completed
};

// Sample concepts for demonstration
export const sampleConcepts: Concept[] = [
  {
    id: 'photosynthesis_101',
    subjectId: 'high_school_biology',
    title: 'Photosynthesis',
    description: 'The process by which green plants and some other organisms use sunlight to synthesize foods with carbon dioxide and water.',
    content: `
      Photosynthesis is a process used by plants and other organisms to convert light energy into chemical energy that can later be released to fuel the organism's activities. This chemical energy is stored in carbohydrate molecules, such as sugars, which are synthesized from carbon dioxide and water.

      In most cases, oxygen is also released as a waste product. Most plants, algae, and cyanobacteria perform photosynthesis; such organisms are called photoautotrophs.
    `,
    equations: [
      '6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂'
    ],
    difficulty: 'beginner'
  },
  {
    id: 'newton_first_law',
    subjectId: 'high_school_physics',
    title: 'Newton\'s First Law of Motion',
    description: 'An object at rest stays at rest, and an object in motion stays in motion with the same speed and direction unless acted upon by an external force.',
    content: `
      Newton's First Law of Motion states that an object will remain at rest or in uniform motion in a straight line unless acted upon by an external force. This law is often called the law of inertia.

      Inertia is the tendency of an object to resist changes in its state of motion. The more mass an object has, the greater its inertia and the more force it takes to change its state of motion.
    `,
    examples: [
      'A book lying on a table will remain there unless a force (like a push or pull) moves it.',
      'Passengers in a car tend to continue moving forward when the car suddenly stops.'
    ],
    difficulty: 'beginner'
  }
];

// Function to get concepts by subject ID
export const getConceptsBySubject = (subjectId: string): Concept[] => {
  return sampleConcepts.filter(concept => concept.subjectId === subjectId);
};