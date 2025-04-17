
import { Card } from "@/components/ui/card";
import { ReportConfig } from "@/pages/Index";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

interface DashboardProps {
  data: any;
  config: ReportConfig;
}

export const Dashboard = ({ data, config }: DashboardProps) => {
  // In a real app, process the data based on the config
  const mockKPIs = {
    totalRevenue: "$1,234,567",
    avgProfitMargin: "23.4%",
    topClient: "AgriCorp Inc.",
    period: "2023-2024",
  };

  const mockTimeData = [
    { month: "Jan", revenue: 4000, profitMargin: 24 },
    { month: "Feb", revenue: 3000, profitMargin: 22 },
    { month: "Mar", revenue: 5000, profitMargin: 26 },
    { month: "Apr", revenue: 4500, profitMargin: 25 },
    { month: "May", revenue: 6000, profitMargin: 28 },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-4 gap-4">
        <Card className="p-4">
          <h3 className="text-sm font-medium text-muted-foreground">Total Revenue</h3>
          <p className="text-2xl font-bold mt-2">{mockKPIs.totalRevenue}</p>
        </Card>
        <Card className="p-4">
          <h3 className="text-sm font-medium text-muted-foreground">Avg Profit Margin</h3>
          <p className="text-2xl font-bold mt-2">{mockKPIs.avgProfitMargin}</p>
        </Card>
        <Card className="p-4">
          <h3 className="text-sm font-medium text-muted-foreground">Top Client</h3>
          <p className="text-2xl font-bold mt-2">{mockKPIs.topClient}</p>
        </Card>
        <Card className="p-4">
          <h3 className="text-sm font-medium text-muted-foreground">Analysis Period</h3>
          <p className="text-2xl font-bold mt-2">{mockKPIs.period}</p>
        </Card>
      </div>

      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Revenue & Profit Margin Trends</h3>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={mockTimeData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="revenue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.1}/>
                  <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <XAxis dataKey="month" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <CartesianGrid strokeDasharray="3 3" />
              <Tooltip />
              <Area
                yAxisId="left"
                type="monotone"
                dataKey="revenue"
                stroke="#8B5CF6"
                fillOpacity={1}
                fill="url(#revenue)"
              />
              <Area
                yAxisId="right"
                type="monotone"
                dataKey="profitMargin"
                stroke="#F97316"
                fill="none"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  );
};
