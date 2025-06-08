import OpenAI from 'openai';

// Initialize OpenAI client
// In a real application, you would use environment variables for API keys
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || 'your-api-key',
});

export type ActiveLearningFeedback = {
  correctness: number; // 0-100 score
  feedback: string;
  misconceptions: string[];
  suggestedResources?: string[];
  nextSteps?: string[];
};

/**
 * Evaluates a user's response to a concept question
 * @param concept The concept being learned
 * @param userResponse The user's answer or explanation
 * @returns Feedback on the user's response
 */
export async function evaluateUserResponse(
  conceptTitle: string,
  conceptContent: string,
  userQuestion: string,
  userResponse: string
): Promise<ActiveLearningFeedback> {
  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: `You are a science education AI tutor. Your goal is to provide accurate, helpful feedback on student responses about scientific concepts.
          Be encouraging but precise in your feedback. For incorrect or partially correct answers, clearly explain the misconceptions and provide guidance for improvement.
          When evaluating, consider:
          1. Factual accuracy
          2. Completeness of understanding
          3. Proper use of scientific terminology
          4. Logical coherence`
        },
        {
          role: 'user',
          content: `Concept: ${conceptTitle}

          Content: ${conceptContent}

          Student Question: ${userQuestion}

          Student Response: ${userResponse}

          Please provide:
          1. A correctness score (0-100)
          2. Detailed feedback
          3. Identification of any misconceptions
          4. Suggested resources for further learning
          5. Next steps for the student

          Format your response as a JSON object with the following fields:
          {
            "correctness": number,
            "feedback": string,
            "misconceptions": string[],
            "suggestedResources": string[],
            "nextSteps": string[]
          }`
        }
      ],
      response_format: { type: 'json_object' }
    });

    const content = response.choices[0]?.message?.content;

    if (!content) {
      throw new Error('No content returned from AI');
    }

    return JSON.parse(content) as ActiveLearningFeedback;
  } catch (error) {
    console.error('Error evaluating user response:', error);
    return {
      correctness: 0,
      feedback: 'Sorry, we encountered an error evaluating your response. Please try again.',
      misconceptions: [],
      suggestedResources: [],
      nextSteps: []
    };
  }
}

/**
 * Generates an explanation for a concept based on user inputs
 * @param conceptTitle
 * @param userQuestions
 * @returns Detailed explanation
 */
export async function generateConceptExplanation(
  conceptTitle: string,
  userQuestions: string[]
): Promise<string> {
  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: `You are a science education AI specializing in explaining complex scientific concepts in clear, understandable ways.
          Your explanations should be accurate, comprehensive, and tailored to the user's questions.
          Include analogies, examples, and visual descriptions where appropriate.`
        },
        {
          role: 'user',
          content: `Please provide a detailed explanation of the following concept: ${conceptTitle}

          The user has asked the following specific questions:
          ${userQuestions.map(q => `- ${q}`).join('\n')}

          Your explanation should:
          1. Start with a clear overview of the concept
          2. Address each of the user's questions
          3. Include relevant equations or principles
          4. Use examples to illustrate key points
          5. Explain any common misconceptions`
        }
      ]
    });

    return response.choices[0]?.message?.content || 'No explanation could be generated.';
  } catch (error) {
    console.error('Error generating concept explanation:', error);
    return 'Sorry, we encountered an error generating your explanation. Please try again.';
  }
}

/**
 * Analyzes exam results to provide personalized feedback
 * @param examTitle
 * @param questions
 * @param userAnswers
 * @returns Personalized feedback
 */
export async function analyzeExamResults(
  examTitle: string,
  questions: Array<{
    id: string;
    text: string;
    correctAnswer: string;
    userAnswer: string;
    isCorrect: boolean;
  }>
): Promise<string> {
  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: `You are an educational assessment AI specializing in analyzing exam results and providing personalized feedback.
          Your goal is to identify patterns in a student's performance, highlight strengths and weaknesses, and provide actionable recommendations.`
        },
        {
          role: 'user',
          content: `Please analyze the following exam results for: ${examTitle}

          Questions and Answers:
          ${questions.map(q =>
            `Question: ${q.text}
             Correct Answer: ${q.correctAnswer}
             User Answer: ${q.userAnswer}
             Result: ${q.isCorrect ? 'Correct' : 'Incorrect'}`
          ).join('\n\n')}

          Please provide:
          1. An overview of the student's performance
          2. Identification of strength areas
          3. Identification of knowledge gaps or areas for improvement
          4. Specific concepts that need review
          5. Recommended next steps for further study`
        }
      ]
    });

    return response.choices[0]?.message?.content || 'No analysis could be generated.';
  } catch (error) {
    console.error('Error analyzing exam results:', error);
    return 'Sorry, we encountered an error analyzing your exam results. Please try again.';
  }
}