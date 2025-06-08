import { NextRequest, NextResponse } from 'next/server';
import { evaluateUserResponse } from '../../../utils/ai';
import { getConceptsBySubject } from '../../../data/learning';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { conceptId, question, response } = body;

    if (!conceptId || !question || !response) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    // Find the concept
    // In a real app, you would fetch this from a database
    const allConcepts = [
      ...getConceptsBySubject('high_school_biology'),
      ...getConceptsBySubject('high_school_physics'),
      ...getConceptsBySubject('high_school_chemistry'),
      ...getConceptsBySubject('college_biology'),
      ...getConceptsBySubject('college_physics'),
      ...getConceptsBySubject('college_chemistry'),
    ];

    const concept = allConcepts.find(c => c.id === conceptId);

    if (!concept) {
      return NextResponse.json(
        { error: 'Concept not found' },
        { status: 404 }
      );
    }

    const feedback = await evaluateUserResponse(
      concept.title,
      concept.content,
      question,
      response
    );

    return NextResponse.json(feedback);
  } catch (error) {
    console.error('Error evaluating response:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}