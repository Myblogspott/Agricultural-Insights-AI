import { useState, useEffect } from "react";
import axios from "axios";
import { FileUpload } from "@/components/FileUpload";
import { ConfigSidebar } from "@/components/ConfigSidebar";
import { Dashboard } from "@/components/Dashboard";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import Plot from "react-plotly.js";

interface ChartData {
  data: any[];
  layout: any;
}

interface EbitdaCharts {
  waterfall?: ChartData;
  margins?: ChartData;
  components?: ChartData;
}

interface Analysis {
  total_revenue: number;
  average_profit_margin: number;
  top_profit_margin_client: string;
  date_range: string;
}

interface ApiResponse {
  analysis: Analysis;
  charts: {
    region: ChartData;
    product: ChartData;
    timeSeries: ChartData;
    ebitda?: EbitdaCharts;
  };
  report: string;
  ebitdaReport: string | null;
  savedFilename: string;
}

export type ReportConfig = {
  reportType: string;
  metricsToShow: string[];
  ebitdaAnalysisType: string;
  includeEbitda: boolean;
};

const Index = () => {
  const [analysis, setAnalysis] = useState<any>(null);
  const [charts, setCharts] = useState<any>({});
  const [reportMarkdown, setReportMarkdown] = useState("");
  const [ebitdaReport, setEbitdaReport] = useState("");
  const [dataUploaded, setDataUploaded] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const { toast } = useToast();
  const [config, setConfig] = useState<ReportConfig>({
    reportType: "Standard",
    metricsToShow: ["Revenue", "Profit Margin"],
    ebitdaAnalysisType: "Comprehensive",
    includeEbitda: false,
  });

  useEffect(() => {
    if (uploadedFile) {
      handleFileUpload(uploadedFile);
    }
  }, [config]);

  const handleFileUpload = async (file: File) => {
    try {
      setUploadedFile(file); // store uploaded file for reactive updates

      const formData = new FormData();
      formData.append("file", file);
      formData.append("reportType", config.reportType);
      formData.append("metrics", config.metricsToShow.join(","));
      formData.append("caseType", config.ebitdaAnalysisType);
      formData.append("includeEbitda", config.includeEbitda.toString());

      const response = await axios.post<ApiResponse>("http://localhost:8000/api/generate-report", formData);
      const data = response.data;

      setAnalysis(data.analysis);
      setCharts(data.charts);
      setReportMarkdown(data.report);
      setEbitdaReport(data.ebitdaReport || "");
      setDataUploaded(true);

      toast({
        title: "Report generated successfully",
        description: `Saved as ${data.savedFilename}`,
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Upload failed",
        description: "Ensure your CSV has all required columns.",
      });
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="flex">
        <ConfigSidebar config={config} setConfig={setConfig} />

        <main className="flex-1 p-6">
          <h1 className="text-3xl font-bold mb-6 text-primary">
            Agricultural Financial Report Generator
          </h1>

          {!dataUploaded ? (
            <div className="max-w-2xl mx-auto mt-10">
              <FileUpload onUpload={handleFileUpload} />
            </div>
          ) : (
            <Tabs defaultValue="dashboard" className="w-full">
              <TabsList className="mb-6">
                <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
                <TabsTrigger value="report">Report</TabsTrigger>
                <TabsTrigger value="analysis">Analysis</TabsTrigger>
                {config.includeEbitda && (
                  <TabsTrigger value="ebitda">EBITDA</TabsTrigger>
                )}
              </TabsList>

              <TabsContent value="dashboard">
                <Dashboard data={analysis} config={config} />
                {charts.region && <Plot data={charts.region.data} layout={charts.region.layout} />}
                {charts.timeSeries && <Plot data={charts.timeSeries.data} layout={charts.timeSeries.layout} />}
              </TabsContent>

              <TabsContent value="report">
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <h2 className="text-2xl font-semibold">Generated Report</h2>
                    <Button
                      onClick={() => {
                        const blob = new Blob([
                          reportMarkdown + "\n\n" + ebitdaReport,
                        ], { type: "text/plain" });
                        const link = document.createElement("a");
                        link.href = URL.createObjectURL(blob);
                        link.download = `financial_report_${Date.now()}.txt`;
                        link.click();
                      }}
                      disabled={isGenerating}
                    >
                      📥 Download Report
                    </Button>
                  </div>
                  <pre className="whitespace-pre-wrap bg-white p-4 rounded shadow">{reportMarkdown}</pre>
                  {ebitdaReport && (
                    <pre className="whitespace-pre-wrap bg-white p-4 rounded shadow">{ebitdaReport}</pre>
                  )}
                </div>
              </TabsContent>

              <TabsContent value="analysis">
                {charts.product && <Plot data={charts.product.data} layout={charts.product.layout} />}
              </TabsContent>

              {config.includeEbitda && (
                <TabsContent value="ebitda">
                  {charts.ebitda?.waterfall && (
                    <Plot data={charts.ebitda.waterfall.data} layout={charts.ebitda.waterfall.layout} />
                  )}
                  {charts.ebitda?.margins && (
                    <Plot data={charts.ebitda.margins.data} layout={charts.ebitda.margins.layout} />
                  )}
                  {charts.ebitda?.components && (
                    <Plot data={charts.ebitda.components.data} layout={charts.ebitda.components.layout} />
                  )}
                </TabsContent>
              )}
            </Tabs>
          )}
        </main>
      </div>
    </div>
  );
};

export default Index;