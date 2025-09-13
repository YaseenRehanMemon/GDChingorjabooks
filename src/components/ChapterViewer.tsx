import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { BookOpen, Play, Bookmark, MessageCircle } from 'lucide-react';

interface ChapterViewerProps {
  subject: string;
  chapter: string;
  onStartQuiz?: () => void;
}

const ChapterViewer: React.FC<ChapterViewerProps> = ({ subject, chapter, onStartQuiz }) => {
  const [chapterContent, setChapterContent] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const loadChapter = async () => {
      setLoading(true);
      try {
        // Map subject names to directory names
        const subjectMap: { [key: string]: string } = {
          'chemistry': 'chemistrybooks',
          'chemistry-xii': 'chemistryxiibooks',
          'physics': 'physicsbooks',
          'physics-xii': 'physicsxiibooks',
          'mathematics': 'mathbooks',
          'mathematics-xii': 'mathsxiibooks',
          'biology': 'biologybooks',
          'biology-xii': 'biologyxiibooks'
        };

        const subjectDir = subjectMap[subject];
        if (!subjectDir) {
          throw new Error('Invalid subject');
        }

        const response = await fetch(`/${subjectDir}/${chapter}.html`);
        if (!response.ok) {
          throw new Error('Chapter not found');
        }

        let html = await response.text();

        // Fix relative paths to absolute
        html = html.replace(/href="\.\.\/assets\//g, 'href="/assets/');
        html = html.replace(/src="\.\.\/assets\//g, 'src="/assets/');

        // Extract content from HTML (basic extraction)
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const contentElement = doc.querySelector('.content') || doc.querySelector('main') || doc.querySelector('body');

        if (contentElement) {
          setChapterContent(contentElement.innerHTML);
        } else {
          setChapterContent(html);
        }

        setError('');
      } catch (err) {
        setError('Failed to load chapter content. Please try again.');
        console.error('Error loading chapter:', err);
      } finally {
        setLoading(false);
      }
    };

    if (subject && chapter) {
      loadChapter();
    }
  }, [subject, chapter]);

  // Load CSS and trigger MathJax after content is set
  useEffect(() => {
    if (chapterContent) {
      // Load the styles if not already loaded
      if (!document.querySelector('link[href="/assets/css/styles.css"]')) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/assets/css/styles.css';
        document.head.appendChild(link);
      }

      // Trigger MathJax typesetting
      if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise().catch((err) => console.error('MathJax typesetting failed:', err));
      } else if (window.MathJax && window.MathJax.typeset) {
        window.MathJax.typeset();
      }
    }
  }, [chapterContent]);

  if (loading) {
    return (
      <Card className="w-full max-w-4xl mx-auto">
        <CardContent className="p-8 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p>Loading chapter content...</p>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="w-full max-w-4xl mx-auto">
        <CardContent className="p-8 text-center">
          <BookOpen className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600">{error}</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="w-full max-w-4xl mx-auto space-y-4 sm:space-y-6">
      {/* Chapter Header */}
      <Card>
        <CardHeader className="pb-4">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
            <div className="flex-1 min-w-0">
              <CardTitle className="text-xl sm:text-2xl">{chapter.replace('ch', 'Chapter ')}</CardTitle>
              <p className="text-muted-foreground mt-1 sm:mt-2 text-sm sm:text-base">
                {subject.charAt(0).toUpperCase() + subject.slice(1).replace('-', ' ')} - Intermediate Level
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-2 w-full sm:w-auto">
              <Button variant="outline" size="sm" className="w-full sm:w-auto">
                <Bookmark className="h-4 w-4 mr-2" />
                <span className="hidden sm:inline">Bookmark</span>
              </Button>
              <Button variant="outline" size="sm" className="w-full sm:w-auto">
                <MessageCircle className="h-4 w-4 mr-2" />
                <span className="hidden sm:inline">Ask AI</span>
              </Button>
            </div>
          </div>
        </CardHeader>
      </Card>

       {/* Chapter Content */}
       <Card className="overflow-hidden">
         <CardContent className="p-0">
           <div
             className="content prose prose-sm sm:prose lg:prose-lg max-w-none overflow-x-hidden"
             dangerouslySetInnerHTML={{ __html: chapterContent }}
           />
         </CardContent>
       </Card>

      {/* Action Buttons */}
      <Card>
        <CardContent className="p-4 sm:p-6">
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 sm:justify-center">
            <Button onClick={onStartQuiz} size="lg" className="flex items-center justify-center w-full sm:w-auto">
              <Play className="h-4 w-4 mr-2" />
              Take Quiz
            </Button>
            <Button variant="outline" size="lg" className="flex items-center justify-center w-full sm:w-auto">
              <BookOpen className="h-4 w-4 mr-2" />
              Study Notes
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ChapterViewer;