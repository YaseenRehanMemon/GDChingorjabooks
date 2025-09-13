import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { BookOpen, Users, Trophy, Star, Atom, Calculator, FlaskConical, Dna } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Navigation from "@/components/Navigation";
import SubjectCard from "@/components/SubjectCard";
import StatsCard from "@/components/StatsCard";
import { useToast } from "@/hooks/use-toast";

const Index = () => {
  const { toast } = useToast();
  const navigate = useNavigate();
  
  const subjects = [
    {
      id: "chemistry",
      name: "Chemistry",
      level: "XI",
      icon: FlaskConical,
      description: "Explore the fascinating world of atoms, molecules, and chemical reactions",
      chapters: 12,
      mcqs: 1200,
      color: "chemistry" as const,
      gradient: "from-emerald-500 to-green-600"
    },
    {
      id: "chemistry-xii",
      name: "Chemistry",
      level: "XII",
      icon: FlaskConical,
      description: "Advanced chemistry concepts for intermediate level students",
      chapters: 13,
      mcqs: 1300,
      color: "chemistry" as const,
      gradient: "from-emerald-500 to-green-600"
    },
    {
      id: "physics",
      name: "Physics",
      level: "XI",
      icon: Atom,
      description: "Discover the fundamental laws that govern our universe",
      chapters: 14,
      mcqs: 1400,
      color: "physics" as const,
      gradient: "from-blue-500 to-blue-600"
    },
    {
      id: "physics-xii",
      name: "Physics",
      level: "XII",
      icon: Atom,
      description: "Advanced physics concepts including quantum mechanics and relativity",
      chapters: 14,
      mcqs: 1400,
      color: "physics" as const,
      gradient: "from-blue-500 to-blue-600"
    },
    {
      id: "mathematics",
      name: "Mathematics",
      level: "XI",
      icon: Calculator,
      description: "Master the language of numbers, algebra, and geometry",
      chapters: 12,
      mcqs: 1200,
      color: "mathematics" as const,
      gradient: "from-purple-500 to-violet-600"
    },
    {
      id: "mathematics-xii",
      name: "Mathematics",
      level: "XII",
      icon: Calculator,
      description: "Advanced mathematical concepts including calculus and statistics",
      chapters: 12,
      mcqs: 1200,
      color: "mathematics" as const,
      gradient: "from-purple-500 to-violet-600"
    },
    {
      id: "biology",
      name: "Biology",
      level: "XI",
      icon: Dna,
      description: "Explore the amazing world of living organisms and life processes",
      chapters: 14,
      mcqs: 1400,
      color: "biology" as const,
      gradient: "from-red-500 to-rose-600"
    },
    {
      id: "biology-xii",
      name: "Biology",
      level: "XII",
      icon: Dna,
      description: "Advanced biology including genetics, evolution, and biotechnology",
      chapters: 13,
      mcqs: 1300,
      color: "biology" as const,
      gradient: "from-red-500 to-rose-600"
    }
  ];

  const stats = [
    { label: "Total Chapters", value: "110+", icon: BookOpen },
    { label: "Practice MCQs", value: "11,000+", icon: Trophy },
    { label: "Students Helped", value: "10,000+", icon: Users },
    { label: "Success Rate", value: "95%", icon: Star }
  ];

  const handleSubjectClick = (subjectId: string) => {
    navigate(`/subject/${subjectId}`);
  };

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary via-primary-light to-accent py-20 px-4">
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-gradient-to-br from-primary/90 to-accent/90"></div>
        </div>
        
        <div className="container mx-auto max-w-6xl relative z-10">
          <div className="text-center text-white">
            <Badge variant="secondary" className="mb-4 bg-white/20 text-white border-white/30">
              🎓 Excellence in Education
            </Badge>
            
            <h1 className="text-4xl md:text-6xl font-bold mb-6 text-balance">
              Welcome to
              <span className="block bg-gradient-to-r from-yellow-300 to-orange-300 bg-clip-text text-transparent">
                HingorjaCollege
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto text-white/90 text-balance">
              Your comprehensive online learning platform for Pakistani Intermediate (XI-XII) students. 
              Master Chemistry, Physics, Mathematics, and Biology with our interactive curriculum.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button size="lg" variant="secondary" className="bg-white text-primary hover:bg-white/90 shadow-lg">
                Start Learning Now
              </Button>
              <Button size="lg" variant="outline" className="border-white text-white hover:bg-white/10">
                Take Practice Quiz
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-4 bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {stats.map((stat, index) => (
              <StatsCard key={index} {...stat} />
            ))}
          </div>
        </div>
      </section>

      {/* Subjects Grid */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Choose Your Subject
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-balance">
              Select from our comprehensive curriculum designed specifically for Pakistani 
              Intermediate students. Each subject includes detailed chapters, practice MCQs, 
              and AI-powered assistance.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {subjects.map((subject) => (
              <SubjectCard
                key={`${subject.id}-${subject.level}`}
                subject={subject}
                onClick={() => handleSubjectClick(subject.id)}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Why Choose HingorjaCollege?
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-balance">
              Experience the future of education with our comprehensive learning platform
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="edu-card">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                  <BookOpen className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>Comprehensive Curriculum</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Complete syllabus coverage for all subjects with detailed explanations and examples
                </p>
              </CardContent>
            </Card>
            
            <Card className="edu-card">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-secondary/10 flex items-center justify-center mb-4">
                  <Trophy className="h-6 w-6 text-secondary" />
                </div>
                <CardTitle>Interactive MCQs</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Thousands of practice questions with instant feedback and detailed explanations
                </p>
              </CardContent>
            </Card>
            
            <Card className="edu-card">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center mb-4">
                  <Star className="h-6 w-6 text-accent" />
                </div>
                <CardTitle>AI-Powered Assistant</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Get instant help with our intelligent chatbot that understands your subject context
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-primary to-accent text-white">
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Excel in Your Studies?
          </h2>
          <p className="text-xl mb-8 text-white/90">
            Join thousands of students who have improved their grades with HingorjaCollege
          </p>
          <Button size="lg" variant="secondary" className="bg-white text-primary hover:bg-white/90">
            Get Started Today
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Index;