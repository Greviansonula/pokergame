import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function GET() {
  try {
    console.log('API Route: GET /api/hands called');
    console.log('API Route: Proxying to backend:', `${BACKEND_URL}/api/v1/hands/`);
    
    const response = await fetch(`${BACKEND_URL}/api/v1/hands/`);
    
    if (!response.ok) {
      console.error('API Route: Backend returned error:', response.status, response.statusText);
      return NextResponse.json(
        { error: `Backend error: ${response.statusText}` }, 
        { status: response.status }
      );
    }
    
    const data = await response.json();
    console.log('API Route: Successfully fetched hands from backend, count:', data.length);
    return NextResponse.json(data);
  } catch (error) {
    console.error('API Route: Error proxying to backend:', error);
    return NextResponse.json(
      { error: 'Failed to fetch hands from backend' }, 
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    console.log('API Route: POST /api/hands called');
    const body = await request.json();
    console.log('API Route: Request body:', body);
    
    const response = await fetch(`${BACKEND_URL}/api/v1/hands/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
    
    if (!response.ok) {
      console.error('API Route: Backend returned error:', response.status, response.statusText);
      return NextResponse.json(
        { error: `Backend error: ${response.statusText}` }, 
        { status: response.status }
      );
    }
    
    const data = await response.json();
    console.log('API Route: Successfully created hand in backend');
    return NextResponse.json(data);
  } catch (error) {
    console.error('API Route: Error proxying to backend:', error);
    return NextResponse.json(
      { error: 'Failed to create hand in backend' }, 
      { status: 500 }
    );
  }
}
