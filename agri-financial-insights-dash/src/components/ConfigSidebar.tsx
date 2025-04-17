
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { ReportConfig } from "@/pages/Index";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface ConfigSidebarProps {
  config: ReportConfig;
  setConfig: (config: ReportConfig) => void;
}

export const ConfigSidebar = ({ config, setConfig }: ConfigSidebarProps) => {
  const metrics = [
    "Revenue",
    "Profit Margin",
    "ROI",
    "Operating Expenses",
    "Time Trends",
  ];

  const reportTypes = [
    "Standard",
    "ROI Focused",
    "Regional Analysis",
    "Product Analysis",
  ];

  const ebitdaTypes = ["Comprehensive", "Regional", "Product", "Client"];

  return (
    <aside className="w-64 border-r bg-card p-6 space-y-6 min-h-screen">
      <div>
        <h2 className="font-semibold mb-4">Report Configuration</h2>
        
        <div className="space-y-4">
          <div className="space-y-2">
            <Label>Report Type</Label>
            <Select
              value={config.reportType}
              onValueChange={(value) =>
                setConfig({ ...config, reportType: value })
              }
            >
              <SelectTrigger>
                <SelectValue placeholder="Select type" />
              </SelectTrigger>
              <SelectContent>
                {reportTypes.map((type) => (
                  <SelectItem key={type} value={type}>
                    {type}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label>Metrics</Label>
            <div className="space-y-2">
              {metrics.map((metric) => (
                <div key={metric} className="flex items-center gap-2">
                  <Switch
                    id={metric}
                    checked={config.metricsToShow.includes(metric)}
                    onCheckedChange={(checked) =>
                      setConfig({
                        ...config,
                        metricsToShow: checked
                          ? [...config.metricsToShow, metric]
                          : config.metricsToShow.filter((m) => m !== metric),
                      })
                    }
                  />
                  <Label htmlFor={metric}>{metric}</Label>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="font-semibold">EBITDA Analysis</h3>
        
        <div className="space-y-2">
          <Label>Analysis Type</Label>
          <Select
            value={config.ebitdaAnalysisType}
            onValueChange={(value) =>
              setConfig({ ...config, ebitdaAnalysisType: value })
            }
          >
            <SelectTrigger>
              <SelectValue placeholder="Select type" />
            </SelectTrigger>
            <SelectContent>
              {ebitdaTypes.map((type) => (
                <SelectItem key={type} value={type}>
                  {type}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="flex items-center gap-2">
          <Switch
            id="include-ebitda"
            checked={config.includeEbitda}
            onCheckedChange={(checked) =>
              setConfig({ ...config, includeEbitda: checked })
            }
          />
          <Label htmlFor="include-ebitda">Include EBITDA Analysis</Label>
        </div>
      </div>
    </aside>
  );
};
