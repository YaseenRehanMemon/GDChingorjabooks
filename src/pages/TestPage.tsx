import React from 'react';
import { useParams } from 'react-router-dom';

const TestPage: React.FC = () => {
  const { subject } = useParams<{ subject: string }>();
  
  return (
    <div className="min-h-screen bg-background p-8">
      <div className="container mx-auto max-w-4xl">
        <h1 className="text-3xl font-bold mb-4">Test Page</h1>
        <p className="text-lg">Subject: {subject || 'No subject found'}</p>
        <p className="text-sm text-muted-foreground mt-4">
          If you can see this page, the routing is working correctly.
        </p>
      </div>
    </div>
  );
};

export default TestPage;