import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = params;
    console.log('API Route: GET /api/hands/[id] called with ID:', id);
    console.log('API Route: Proxying to backend:', `${BACKEND_URL}/api/v1/hands/${id}`);
    
    const response = await fetch(`${BACKEND_URL}/api/v1/hands/${id}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        return NextResponse.json(
          { error: 'Hand not found' }, 
          { status: 404 }
        );
      }
      console.error('API Route: Backend returned error:', response.status, response.statusText);
      return NextResponse.json(
        { error: `Backend error: ${response.statusText}` }, 
        { status: response.status }
      );
    }
    
    const data = await response.json();
    console.log('API Route: Successfully fetched hand from backend');
    return NextResponse.json(data);
  } catch (error) {
    console.error('API Route: Error proxying to backend:', error);
    return NextResponse.json(
      { error: 'Failed to fetch hand from backend' }, 
      { status: 500 }
    );
  }
}
