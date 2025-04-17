
import { ChangeEvent, DragEvent, useState } from "react";
import { Card } from "@/components/ui/card";
import { UploadCloud } from "lucide-react";

interface FileUploadProps {
  onUpload: (file: File) => void;
}

export const FileUpload = ({ onUpload }: FileUploadProps) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleDragEnter = (e: DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type === "text/csv") {
      onUpload(file);
    }
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onUpload(file);
    }
  };

  return (
    <Card
      className={`p-8 text-center border-dashed border-2 ${
        isDragging ? "border-primary bg-primary/5" : "border-border"
      }`}
      onDragEnter={handleDragEnter}
      onDragOver={(e) => e.preventDefault()}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <div className="flex flex-col items-center gap-4">
        <UploadCloud className="w-12 h-12 text-muted-foreground" />
        <div>
          <h3 className="text-lg font-semibold mb-1">Upload Financial Data</h3>
          <p className="text-sm text-muted-foreground mb-4">
            Drag and drop your CSV file or click to browse
          </p>
        </div>
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="hidden"
          id="file-upload"
        />
        <label
          htmlFor="file-upload"
          className="cursor-pointer bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90 transition-colors"
        >
          Choose File
        </label>
      </div>

      <div className="mt-6">
        <h4 className="font-medium mb-2">Required Columns:</h4>
        <ul className="text-sm text-muted-foreground list-disc list-inside space-y-1">
          <li>Date (YYYY-MM-DD)</li>
          <li>Client Name, Region, Product</li>
          <li>Revenue, Operating Expenses</li>
          <li>Raw Material Cost, Labor Cost</li>
          <li>EBITDA, EBITDA Margin, Profit Margin</li>
        </ul>
      </div>
    </Card>
  );
};
