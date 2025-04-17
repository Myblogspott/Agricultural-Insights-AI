
import { Card } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";

interface EBITDAAnalysisProps {
  data: any;
}

export const EBITDAAnalysis = ({ data }: EBITDAAnalysisProps) => {
  const waterfallData = [
    { name: "Revenue", amount: 1000000 },
    { name: "Raw Material", amount: -300000 },
    { name: "Labor", amount: -200000 },
    { name: "Overhead", amount: -150000 },
    { name: "EBITDA", amount: 350000 },
  ];

  // Mock data - replace with real data in production
  const mockWaterfallData = waterfallData.map(item => ({
    ...item,
    color: item.amount > 0 ? "#10B981" : "#EF4444"
  }));

  const mockComponentData = [
    { name: "Raw Material", value: 30 },
    { name: "Labor", value: 25 },
    { name: "Overhead", value: 20 },
    { name: "Interest", value: 15 },
    { name: "Taxes", value: 10 },
  ];

  const COLORS = ['#8B5CF6', '#F97316', '#10B981', '#3B82F6', '#EC4899'];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-4 gap-4">
        <Card className="p-4">
          <h3 className="text-sm font-medium text-muted-foreground">Total EBITDA</h3>
          <p className="text-2xl font-bold mt-2">$350,000</p>
        </Card>
        <Card className="p-4">
          <h3 className="text-sm font-medium text-muted-foreground">EBITDA Margin</h3>
          <p className="text-2xl font-bold mt-2">35%</p>
        </Card>
        <Card className="p-4">
          <h3 className="text-sm font-medium text-muted-foreground">Operating Expenses</h3>
          <p className="text-2xl font-bold mt-2">$650,000</p>
        </Card>
        <Card className="p-4">
          <h3 className="text-sm font-medium text-muted-foreground">Interest Coverage</h3>
          <p className="text-2xl font-bold mt-2">4.2x</p>
        </Card>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">EBITDA Bridge</h3>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={mockWaterfallData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="amount" fill="#8B5CF6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Cost Components</h3>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={mockComponentData}
                  innerRadius={60}
                  outerRadius={120}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {mockComponentData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  );
};
