import { NextRequest, NextResponse } from 'next/server';
import { analyzeExamResults } from '../../../utils/ai';
import { sampleExams } from '../../../data/exams';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { examId, answers } = body;

    if (!examId || !answers || !Array.isArray(answers)) {
      return NextResponse.json(
        { error: 'Missing required fields or invalid answers format' },
        { status: 400 }
      );
    }

    // Find the exam
    // In a real app, you would fetch this from a database
    const exam = sampleExams.find(e => e.id === examId);

    if (!exam) {
      return NextResponse.json(
        { error: 'Exam not found' },
        { status: 404 }
      );
    }

    // Validate and format answers
    const questionsMap = new Map(exam.questions.map(q => [q.id, q]));
    const formattedAnswers = answers.map(answer => {
      const { questionId, selectedAnswer } = answer;
      const question = questionsMap.get(questionId);

      if (!question) {
        throw new Error(`Question ${questionId} not found in exam ${examId}`);
      }

      return {
        id: questionId,
        text: question.text,
        correctAnswer: question.correctAnswer,
        userAnswer: selectedAnswer,
        isCorrect: selectedAnswer === question.correctAnswer
      };
    });

    // Calculate score
    const correctCount = formattedAnswers.filter(a => a.isCorrect).length;
    const totalCount = formattedAnswers.length;
    const score = Math.round((correctCount / totalCount) * 100);

    // Get AI analysis
    const analysis = await analyzeExamResults(exam.title, formattedAnswers);

    return NextResponse.json({
      examId,
      title: exam.title,
      score,
      correctCount,
      totalCount,
      isPassing: score >= (exam.passingScore || 70),
      analysis
    });
  } catch (error) {
    console.error('Error analyzing exam results:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}