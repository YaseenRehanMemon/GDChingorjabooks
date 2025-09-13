import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, BookOpen, Play, Clock, Trophy } from 'lucide-react';
import QuizSystem from '@/components/QuizSystem';
import ChapterViewer from '@/components/ChapterViewer';
import Chatbot from '@/components/Chatbot';

const SubjectPage: React.FC = () => {
  const { subject } = useParams<{ subject: string }>();
  const navigate = useNavigate();
  const [selectedChapter, setSelectedChapter] = useState<string>('');
  const [viewMode, setViewMode] = useState<'chapters' | 'quiz' | 'chapter'>('chapters');

  // Chapter data for each subject
  const chapterData: { [key: string]: string[] } = {
    'chemistry': ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12'],
    'chemistry-xii': ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12', 'ch13'],
    'physics': ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12', 'ch13', 'ch14'],
    'physics-xii': ['ch15', 'ch16', 'ch17', 'ch18', 'ch19', 'ch20', 'ch21', 'ch22', 'ch23', 'ch24', 'ch25', 'ch26', 'ch27', 'ch28'],
    'mathematics': ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12'],
    'mathematics-xii': ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12'],
    'biology': ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12', 'ch13', 'ch14'],
    'biology-xii': ['ch15', 'ch16', 'ch17', 'ch18', 'ch19', 'ch20', 'ch21', 'ch22', 'ch23', 'ch24', 'ch25', 'ch26', 'ch27']
  };

  const subjectInfo: { [key: string]: { name: string; level: string; color: string } } = {
    'chemistry': { name: 'Chemistry', level: 'XI', color: 'bg-green-500' },
    'chemistry-xii': { name: 'Chemistry', level: 'XII', color: 'bg-green-600' },
    'physics': { name: 'Physics', level: 'XI', color: 'bg-blue-500' },
    'physics-xii': { name: 'Physics', level: 'XII', color: 'bg-blue-600' },
    'mathematics': { name: 'Mathematics', level: 'XI', color: 'bg-purple-500' },
    'mathematics-xii': { name: 'Mathematics', level: 'XII', color: 'bg-purple-600' },
    'biology': { name: 'Biology', level: 'XI', color: 'bg-red-500' },
    'biology-xii': { name: 'Biology', level: 'XII', color: 'bg-red-600' }
  };

  if (!subject || !chapterData[subject]) {
    return (
      <div className="min-h-screen bg-background p-4">
        <div className="container mx-auto max-w-4xl">
          <Card>
            <CardContent className="p-8 text-center">
              <h1 className="text-2xl font-bold mb-4">Subject Not Found</h1>
              <Button onClick={() => navigate('/')}>
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Home
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  const info = subjectInfo[subject];
  const chapters = chapterData[subject];

  const handleChapterSelect = (chapter: string) => {
    setSelectedChapter(chapter);
    setViewMode('chapter');
  };

  const handleQuizStart = () => {
    setViewMode('quiz');
  };

  const handleQuizComplete = (score: number, total: number) => {
    // Handle quiz completion
    console.log(`Quiz completed: ${score}/${total}`);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary to-accent text-white p-4 sm:p-6">
        <div className="container mx-auto max-w-6xl">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div className="flex items-center space-x-3 sm:space-x-4">
              <Button
                variant="ghost"
                onClick={() => navigate('/')}
                className="text-white hover:bg-white/20 flex-shrink-0"
                size="sm"
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                <span className="hidden sm:inline">Back</span>
              </Button>
              <div className="min-w-0 flex-1">
                <h1 className="text-2xl sm:text-3xl font-bold truncate">{info.name} {info.level}</h1>
                <p className="text-white/80 text-sm sm:text-base">Intermediate Level Curriculum</p>
              </div>
            </div>
            <div className="flex space-x-2 justify-center sm:justify-end">
              <Button
                variant={viewMode === 'chapters' ? 'secondary' : 'ghost'}
                onClick={() => setViewMode('chapters')}
                className="text-white hover:bg-white/20 flex-1 sm:flex-none"
                size="sm"
              >
                <BookOpen className="h-4 w-4 sm:mr-2" />
                <span className="hidden sm:inline">Chapters</span>
              </Button>
              <Button
                variant={viewMode === 'quiz' ? 'secondary' : 'ghost'}
                onClick={() => setViewMode('quiz')}
                className="text-white hover:bg-white/20 flex-1 sm:flex-none"
                size="sm"
              >
                <Play className="h-4 w-4 sm:mr-2" />
                <span className="hidden sm:inline">Quiz</span>
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto max-w-6xl p-4 sm:p-6">
        {viewMode === 'chapters' && (
          <div className="space-y-4 sm:space-y-6">
            <div className="text-center">
              <h2 className="text-xl sm:text-2xl font-bold mb-2">Available Chapters</h2>
              <p className="text-muted-foreground text-sm sm:text-base">
                Click on any chapter to start learning
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
              {chapters.map((chapter, index) => (
                <Card
                  key={chapter}
                  className="cursor-pointer hover:shadow-lg transition-shadow"
                  onClick={() => handleChapterSelect(chapter)}
                >
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-base sm:text-lg">
                        {chapter.replace('ch', 'Chapter ')}
                      </CardTitle>
                      <Badge variant="outline" className="text-xs">{index + 1}</Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <div className="flex items-center space-x-3 sm:space-x-4 text-xs sm:text-sm text-muted-foreground">
                      <div className="flex items-center space-x-1">
                        <BookOpen className="h-3 w-3 sm:h-4 sm:w-4" />
                        <span>Study</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Play className="h-3 w-3 sm:h-4 sm:w-4" />
                        <span>Quiz</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}

        {viewMode === 'quiz' && (
          <QuizSystem
            subject={subject}
            chapter={selectedChapter || chapters[0]}
            onComplete={handleQuizComplete}
          />
        )}

        {viewMode === 'chapter' && selectedChapter && (
          <ChapterViewer
            subject={subject}
            chapter={selectedChapter}
            onStartQuiz={() => setViewMode('quiz')}
          />
        )}
      </div>

      {/* Chatbot */}
      <Chatbot subject={subject} chapter={selectedChapter} />
    </div>
  );
};

export default SubjectPage;