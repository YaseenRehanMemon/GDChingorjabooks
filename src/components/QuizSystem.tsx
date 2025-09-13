import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, XCircle, Clock, BookOpen } from 'lucide-react';

// MathJax type declarations
declare global {
  interface Window {
    MathJax: any;
  }
}

interface MCQ {
  id: string;
  question: string;
  question_type: string;
  options: { [key: string]: string };
  correct_answer: string;
  explanation: string;
  difficulty: string;
  topic: string;
  subtopic: string;
  tags: string[];
  learning_objective: string;
  created_date: string;
  source: string;
  ai_generated: boolean;
  reviewed: boolean;
  quality_score: number;
}

interface QuizSystemProps {
  subject: string;
  chapter: string;
  onComplete?: (score: number, total: number) => void;
}

const QuizSystem: React.FC<QuizSystemProps> = ({ subject, chapter, onComplete }) => {
  const [mcqs, setMcqs] = useState<MCQ[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string>('');
  const [showResult, setShowResult] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);
  const [score, setScore] = useState(0);
  const [timeLeft, setTimeLeft] = useState(300); // 5 minutes
  const [quizStarted, setQuizStarted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  // Load MCQs from JSON file
  useEffect(() => {
    const loadMCQs = async () => {
      setLoading(true);
      try {
        // Map subject names to directory names
        const subjectMap: { [key: string]: string } = {
          'chemistry': 'chemistry',
          'chemistry-xii': 'chemistryXII',
          'physics': 'physics',
          'physics-xii': 'physicsXII',
          'mathematics': 'math',
          'mathematics-xii': 'mathsXII',
          'biology': 'biology',
          'biology-xii': 'biologyXII'
        };

        const subjectDir = subjectMap[subject] || subject;
        const response = await fetch(`/mcq_output/${subjectDir}_chapters/${chapter}_mcqs.json`);
        if (!response.ok) {
          throw new Error('MCQ file not found');
        }
        const data = await response.json();
        setMcqs(data);
        setError('');
      } catch (err) {
        setError('Failed to load MCQs. Please try again.');
        console.error('Error loading MCQs:', err);
      } finally {
        setLoading(false);
      }
    };

    if (subject && chapter) {
      loadMCQs();
    }
  }, [subject, chapter]);

  // Initialize MathJax for LaTeX rendering
  useEffect(() => {
    const initializeMathJax = () => {
      // Load MathJax if not already loaded
      if (!window.MathJax && !document.querySelector('script[src*="mathjax"]')) {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
        script.async = true;
        document.head.appendChild(script);

        script.onload = () => {
          if (window.MathJax) {
            window.MathJax.config = {
              tex: {
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true,
                processEnvironments: true
              },
              options: {
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
              }
            };
            window.MathJax.startup = {
              ready: () => {
                window.MathJax.startup.defaultReady();
                // Typeset after MathJax is ready
                setTimeout(() => {
                  if (window.MathJax.typesetPromise) {
                    window.MathJax.typesetPromise().catch((err) => console.error('MathJax typesetting failed:', err));
                  }
                }, 100);
              }
            };
          }
        };
      } else if (window.MathJax) {
        // MathJax already loaded, just trigger typesetting
        setTimeout(() => {
          if (window.MathJax.typesetPromise) {
            window.MathJax.typesetPromise().catch((err) => console.error('MathJax typesetting failed:', err));
          } else if (window.MathJax.typeset) {
            window.MathJax.typeset();
          }
        }, 100);
      }
    };

    initializeMathJax();
  }, []);

  // Trigger MathJax typesetting when question changes or explanation is shown
  useEffect(() => {
    if (mcqs.length > 0 && window.MathJax) {
      setTimeout(() => {
        if (window.MathJax.typesetPromise) {
          window.MathJax.typesetPromise().catch((err) => console.error('MathJax typesetting failed:', err));
        } else if (window.MathJax.typeset) {
          window.MathJax.typeset();
        }
      }, 50);
    }
  }, [currentQuestion, mcqs, showExplanation]);

  // Timer countdown
  useEffect(() => {
    if (quizStarted && timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else if (timeLeft === 0) {
      handleQuizComplete();
    }
  }, [quizStarted, timeLeft]);

  const startQuiz = () => {
    setQuizStarted(true);
    setTimeLeft(300);
    setCurrentQuestion(0);
    setScore(0);
    setSelectedAnswer('');
    setShowResult(false);
  };

  const handleAnswerSelect = (answer: string) => {
    setSelectedAnswer(answer);
  };

  const handleNextQuestion = () => {
    if (selectedAnswer === mcqs[currentQuestion].correct_answer) {
      setScore(score + 1);
    }

    if (currentQuestion < mcqs.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer('');
      setShowResult(false);
      setShowExplanation(false);
    } else {
      handleQuizComplete();
    }
  };

  const handleShowExplanation = () => {
    setShowExplanation(true);
  };

  const handleQuizComplete = () => {
    const finalScore = selectedAnswer === mcqs[currentQuestion].correct_answer ? score + 1 : score;
    setScore(finalScore);
    setShowResult(true);
    setQuizStarted(false);
    if (onComplete) {
      onComplete(finalScore, mcqs.length);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      case 'expert': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <Card className="w-full max-w-4xl mx-auto">
        <CardContent className="p-8 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p>Loading MCQs...</p>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="w-full max-w-4xl mx-auto">
        <CardContent className="p-8 text-center">
          <XCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600">{error}</p>
        </CardContent>
      </Card>
    );
  }

  if (mcqs.length === 0) {
    return (
      <Card className="w-full max-w-4xl mx-auto">
        <CardContent className="p-8 text-center">
          <BookOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p>No MCQs available for this chapter.</p>
        </CardContent>
      </Card>
    );
  }

  if (!quizStarted) {
    return (
      <Card className="w-full max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle className="text-center">Quiz: {subject} - {chapter}</CardTitle>
        </CardHeader>
        <CardContent className="text-center space-y-4">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex items-center justify-center space-x-2">
              <BookOpen className="h-4 w-4" />
              <span>{mcqs.length} Questions</span>
            </div>
            <div className="flex items-center justify-center space-x-2">
              <Clock className="h-4 w-4" />
              <span>5 Minutes</span>
            </div>
          </div>
          <Button onClick={startQuiz} size="lg" className="w-full">
            Start Quiz
          </Button>
        </CardContent>
      </Card>
    );
  }

  if (showResult) {
    const percentage = Math.round((score / mcqs.length) * 100);
    return (
      <Card className="w-full max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle className="text-center">Quiz Complete!</CardTitle>
        </CardHeader>
        <CardContent className="text-center space-y-6">
          <div className="text-6xl font-bold text-primary">{percentage}%</div>
          <div className="text-xl">
            You scored {score} out of {mcqs.length} questions
          </div>
          <div className="flex justify-center space-x-4">
            <Badge variant="secondary">Score: {score}/{mcqs.length}</Badge>
            <Badge variant={percentage >= 70 ? "default" : "destructive"}>
              {percentage >= 70 ? "Passed" : "Needs Improvement"}
            </Badge>
          </div>
          <Button onClick={() => window.location.reload()} size="lg">
            Take Quiz Again
          </Button>
        </CardContent>
      </Card>
    );
  }

  const currentMCQ = mcqs[currentQuestion];

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>Question {currentQuestion + 1} of {mcqs.length}</CardTitle>
          <div className="flex items-center space-x-2">
            <Clock className="h-4 w-4" />
            <span className="font-mono">{formatTime(timeLeft)}</span>
          </div>
        </div>
        <Progress value={(currentQuestion / mcqs.length) * 100} className="w-full" />
        <div className="flex justify-between items-center">
          <Badge className={getDifficultyColor(currentMCQ.difficulty)}>
            {currentMCQ.difficulty}
          </Badge>
          <Badge variant="outline">{currentMCQ.topic}</Badge>
        </div>
      </CardHeader>
       <CardContent className="space-y-6">
         <div className="text-lg font-medium">
           <span dangerouslySetInnerHTML={{ __html: currentMCQ.question }} />
         </div>
        
         <div className="space-y-3">
           {Object.entries(currentMCQ.options).map(([key, value]) => (
             <Button
               key={key}
               variant={selectedAnswer === key ? "default" : "outline"}
               className="w-full justify-start h-auto p-4 text-left"
               onClick={() => handleAnswerSelect(key)}
             >
               <span className="font-semibold mr-3">{key}.</span>
               <span dangerouslySetInnerHTML={{ __html: value }} />
             </Button>
           ))}
         </div>

         {selectedAnswer && (
           <div className="space-y-4">
             <div className="flex items-center justify-between">
               <div className={`flex items-center space-x-2 ${
                 selectedAnswer === currentMCQ.correct_answer
                   ? 'text-green-600'
                   : 'text-red-600'
               }`}>
                 {selectedAnswer === currentMCQ.correct_answer ? (
                   <CheckCircle className="h-5 w-5" />
                 ) : (
                   <XCircle className="h-5 w-5" />
                 )}
                 <span className="font-medium">
                   {selectedAnswer === currentMCQ.correct_answer
                     ? 'Correct!'
                     : `Incorrect. The correct answer is ${currentMCQ.correct_answer}.`}
                 </span>
               </div>
               {!showExplanation && (
                 <Button
                   variant="outline"
                   size="sm"
                   onClick={handleShowExplanation}
                 >
                   Show Explanation
                 </Button>
               )}
             </div>

             {showExplanation && (
               <div className="bg-muted p-4 rounded-lg">
                 <h4 className="font-semibold mb-2">Explanation:</h4>
                 <div dangerouslySetInnerHTML={{ __html: currentMCQ.explanation }} />
               </div>
             )}
           </div>
         )}

         <div className="flex justify-between">
           <Button
             variant="outline"
             onClick={() => setCurrentQuestion(Math.max(0, currentQuestion - 1))}
             disabled={currentQuestion === 0}
           >
             Previous
           </Button>
           <Button
             onClick={handleNextQuestion}
             disabled={!selectedAnswer}
           >
             {currentQuestion === mcqs.length - 1 ? 'Finish Quiz' : 'Next Question'}
           </Button>
         </div>
      </CardContent>
    </Card>
  );
};

export default QuizSystem;