import { LucideIcon } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface StatsCardProps {
  label: string;
  value: string;
  icon: LucideIcon;
}

const StatsCard = ({ label, value, icon: Icon }: StatsCardProps) => {
  return (
    <Card className="edu-card text-center group hover:shadow-medium">
      <CardContent className="p-6">
        <div className="w-12 h-12 mx-auto mb-3 rounded-xl bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors">
          <Icon className="h-6 w-6 text-primary" />
        </div>
        <div className="text-2xl md:text-3xl font-bold text-foreground mb-1">
          {value}
        </div>
        <div className="text-sm text-muted-foreground font-medium">
          {label}
        </div>
      </CardContent>
    </Card>
  );
};

export default StatsCard;