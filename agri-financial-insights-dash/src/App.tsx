import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { Tab } from '@headlessui/react';
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import './index.css';

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
  regionChart: ChartData;
  timeSeriesChart: ChartData;
  productChart: ChartData;
  ebitda?: EbitdaCharts;
}

interface ApiResponse {
  analysis: Analysis;
  report: string;
  ebitdaReport: string | null;
}

const queryClient = new QueryClient();

const App = () => {
  const [file, setFile] = useState<File | null>(null);
  const [reportType, setReportType] = useState('Standard');
  const [metrics, setMetrics] = useState<string[]>(['Revenue', 'Profit Margin']);
  const [caseType, setCaseType] = useState('Comprehensive');
  const [includeEbitda, setIncludeEbitda] = useState(false);

  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [charts, setCharts] = useState<any>({});
  const [reportMarkdown, setReportMarkdown] = useState('');
  const [ebitdaReport, setEbitdaReport] = useState('');
  const [dataUploaded, setDataUploaded] = useState(false);

  useEffect(() => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('reportType', reportType);
    formData.append('metrics', metrics.join(','));
    formData.append('caseType', caseType);
    formData.append('includeEbitda', includeEbitda.toString());

    axios.post<ApiResponse>('http://localhost:8000/api/generate-report', formData)
      .then(res => {
        const data = res.data;
        setAnalysis(data.analysis);
        setCharts({
          region: data.analysis.regionChart,
          timeSeries: data.analysis.timeSeriesChart,
          product: data.analysis.productChart,
          ebitda: data.analysis.ebitda || {},
        });
        setReportMarkdown(data.report);
        setEbitdaReport(data.ebitdaReport || '');
        setDataUploaded(true);
      })
      .catch(err => {
        console.error('API error:', err);
      });
  }, [file, reportType, metrics, caseType, includeEbitda]);

  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Index />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </QueryClientProvider>
  );
};

export default App;
