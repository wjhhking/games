// Configuration settings for the application

// API Settings
export const API_CONFIG = {
  // OpenAI API configuration
  openai: {
    apiKey: process.env.OPENAI_API_KEY || '',
    model: 'gpt-4',
    temperature: 0.7,
    maxTokens: 2000,
  },

  // Rate limiting (requests per minute)
  rateLimit: {
    learningEvaluations: 20,
    examQuestions: 40,
  },
};

// App settings
export const APP_CONFIG = {
  // Website information
  site: {
    name: 'Science Learning Platform',
    description: 'Learn science concepts with active learning and adaptive testing',
    url: 'https://science-learning.example.com',
  },

  // Learning features
  learning: {
    minUserInputLength: 20, // Minimum characters for user input
    maxUserInputLength: 2000, // Maximum characters for user input
    feedbackThresholds: {
      excellent: 90, // Score for excellent understanding
      good: 75, // Score for good understanding
      fair: 60, // Score for fair understanding
      needsImprovement: 40, // Score for needs improvement
    },
  },

  // Testing features
  testing: {
    defaultTimeLimit: 60, // Default time limit for exams in minutes
    defaultQuestionsPerExam: 10, // Default number of questions per exam
    defaultPassingScore: 70, // Default passing score (%)
  },
};

// Default user settings
export const DEFAULT_USER_SETTINGS = {
  difficulty: 'medium', // easy, medium, hard
  showExplanations: true, // Show explanations for answers
  enableTimedExams: true, // Enable timed exams
  enableActiveAssistance: true, // Enable AI assistance during learning
  theme: 'light', // light, dark, auto
};

// MMLU subject categories for organization
export const SUBJECT_CATEGORIES = {
  stem: 'Science, Technology, Engineering & Mathematics',
  humanities: 'Humanities',
  social_sciences: 'Social Sciences',
  other: 'Other Disciplines',
};