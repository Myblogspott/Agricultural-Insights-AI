
import { Card } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ScatterChart, Scatter, ZAxis } from "recharts";
import { DataTable } from "@/components/DataTable";

interface DetailedAnalysisProps {
  data: any;
}

export const DetailedAnalysis = ({ data }: DetailedAnalysisProps) => {
  // Mock data - replace with real data in production
  const mockProductData = [
    { product: "Corn", revenue: 400000, profitMargin: 25, roi: 35 },
    { product: "Wheat", revenue: 300000, profitMargin: 22, roi: 30 },
    { product: "Soybeans", revenue: 500000, profitMargin: 28, roi: 40 },
    { product: "Cotton", revenue: 450000, profitMargin: 24, roi: 32 },
  ];

  return (
    <div className="space-y-6">
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Product Performance</h3>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={mockProductData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="product" />
              <YAxis yAxisId="left" orientation="left" stroke="#8B5CF6" />
              <YAxis yAxisId="right" orientation="right" stroke="#F97316" />
              <Tooltip />
              <Bar yAxisId="left" dataKey="revenue" fill="#8B5CF6" />
              <Bar yAxisId="right" dataKey="profitMargin" fill="#F97316" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">ROI Analysis</h3>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="revenue" name="Revenue" unit="$" />
              <YAxis dataKey="profitMargin" name="Profit Margin" unit="%" />
              <ZAxis dataKey="roi" range={[100, 1000]} name="ROI" unit="%" />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} />
              <Scatter
                name="Products"
                data={mockProductData}
                fill="#8B5CF6"
              />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Detailed Data</h3>
        <DataTable data={mockProductData} />
      </Card>
    </div>
  );
};
