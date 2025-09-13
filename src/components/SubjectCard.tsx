import { LucideIcon } from "lucide-react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface Subject {
  id: string;
  name: string;
  level: string;
  icon: LucideIcon;
  description: string;
  chapters: number;
  mcqs: number;
  color: "chemistry" | "physics" | "mathematics" | "biology";
  gradient: string;
}

interface SubjectCardProps {
  subject: Subject;
  onClick: () => void;
}

const SubjectCard = ({ subject, onClick }: SubjectCardProps) => {
  const { name, level, icon: Icon, description, chapters, mcqs, color, gradient } = subject;

  const colorClasses = {
    chemistry: "chemistry-card",
    physics: "physics-card", 
    mathematics: "mathematics-card",
    biology: "biology-card"
  };

  return (
    <Card 
      className={cn(
        "edu-card cursor-pointer group relative overflow-hidden transition-all duration-300 hover:scale-105 hover:shadow-strong",
        colorClasses[color]
      )}
      onClick={onClick}
    >
      <div className={cn("absolute inset-0 bg-gradient-to-br opacity-5 group-hover:opacity-10 transition-opacity", gradient)}></div>
      
      <CardHeader className="relative z-10 pb-3">
        <div className="flex items-center justify-between">
          <div className={cn("w-12 h-12 rounded-xl flex items-center justify-center", `bg-${color}/10`)}>
            <Icon className={cn("h-6 w-6", `text-${color}`)} />
          </div>
          <Badge 
            variant="secondary" 
            className={cn("text-xs font-medium", `bg-${color}/10 text-${color} border-${color}/20`)}
          >
            Class {level}
          </Badge>
        </div>
        
        <div className="mt-3">
          <h3 className="text-xl font-semibold text-card-foreground mb-1">
            {name}
          </h3>
          <p className="text-sm text-muted-foreground line-clamp-2">
            {description}
          </p>
        </div>
      </CardHeader>
      
      <CardContent className="relative z-10 pt-0">
        <div className="flex items-center justify-between text-sm text-muted-foreground mb-4">
          <div className="flex items-center space-x-4">
            <span className="flex items-center">
              📚 {chapters} Chapters
            </span>
            <span className="flex items-center">
              📝 {mcqs.toLocaleString()} MCQs
            </span>
          </div>
        </div>
        
        <Button 
          className={cn(
            "w-full transition-all duration-200",
            `bg-${color} hover:bg-${color}/90 text-white shadow-md hover:shadow-lg`
          )}
        >
          Start Learning
        </Button>
      </CardContent>
    </Card>
  );
};

export default SubjectCard;