# report_generation.py
import os
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
from typing import Optional, Dict, Any
from datetime import datetime
import io
from pathlib import Path
from ebitda_analysis import EBITDAAnalyzer
from financial_analysis import FinancialAnalyzer

# Debug mode flag
DEBUG = True

def debug_print(message):
    """Helper function for debug printing"""
    if DEBUG:
        print(f"\nDEBUG - {message}")

# Update PROJECT_ROOT for Hugging Face compatibility
if os.getenv('SPACE_ID'):  # Check if running on Hugging Face Spaces
    PROJECT_ROOT = Path('/Users/raghu/Desktop/huggingface_proj/finance-generator-react/financial-reports-generator')
else:
    PROJECT_ROOT = Path(__file__).parent.parent

# OpenAI client setup with environment check
load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_financial_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze agricultural client financial data using FinancialAnalyzer."""
    debug_print("Starting financial data analysis")
    try:
        analyzer = FinancialAnalyzer(df)
        analysis = analyzer.analyze_financial_data()
        debug_print("Financial analysis completed successfully")
        return analysis
    except Exception as e:
        debug_print(f"Error in financial analysis: {str(e)}")
        raise
    
def generate_financial_report(prompt: str) -> Optional[str]:
    """Generate a financial report using GPT-4 based on the given prompt."""
    debug_print("Starting report generation with GPT-4")
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": (
                    "You are a financial analyst specialized in agricultural business analysis. "
                    "Create detailed reports focusing on regional performance, product profitability, and client performance."
                )},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        debug_print("Report generated successfully")
        return response.choices[0].message.content.strip()
    except Exception as e:
        debug_print(f"Error generating report: {str(e)}")
        return None


def generate_report_from_csv(file_input, report_type: str = "Standard", metrics_to_show: list = None) -> Optional[str]:
    """Generate a comprehensive agricultural financial report based on report type and selected metrics."""
    debug_print("Starting CSV processing")
    try:
        # Handle DataFrame, path, or uploaded file-like
        if isinstance(file_input, pd.DataFrame):
            df = file_input.copy()
            debug_print("Received DataFrame directly")
        elif isinstance(file_input, (str, Path)):
            if not os.path.exists(file_input):
                raise FileNotFoundError(f"CSV file not found: {file_input}")
            debug_print(f"Reading from file path: {file_input}")
            df = pd.read_csv(file_input)
        elif hasattr(file_input, 'read'):
            debug_print("Reading from file-like object")
            # Flask FileStorage or similar
            try:
                file_input.stream.seek(0)
            except Exception:
                pass
            raw = file_input.read()
            if isinstance(raw, bytes):
                raw = raw.decode('utf-8')
            df = pd.read_csv(io.StringIO(raw))
        else:
            raise TypeError(f"Unsupported file_input type: {type(file_input)}")

        # Add column validation here
        required_columns = [
            'Revenue', 'Operating Expenses', 'Raw Material Cost', 'Labor Cost',
            'Overhead Cost', 'Depreciation', 'Amortization', 'Interest', 
            'Taxes', 'EBITDA', 'EBITDA Margin', 'Profit Margin'
        ]

        debug_print("Checking required columns")
        if not all(col in df.columns for col in required_columns):
            missing_cols = [col for col in required_columns if col not in df.columns]
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Convert date column
        debug_print("Converting Date column")
        df['Date'] = pd.to_datetime(df['Date'])

        # Default metrics if none selected
        if not metrics_to_show:
            metrics_to_show = ["Revenue", "Profit Margin"]

        # Initialize analyzers
        financial_analyzer = FinancialAnalyzer(df)
        analysis = financial_analyzer.analyze_financial_data()
        
        # Generate analysis based on report type and metrics
        detailed_analysis = ""
        
        if report_type == "ROI Focused":
            roi_by_product = financial_analyzer.calculate_roi().groupby(df['Product']).mean()
            detailed_analysis += f"\nROI Analysis by Product:\n{roi_by_product.to_string()}\n"
            if 'Operating Expenses' in metrics_to_show:
                detailed_analysis += "\nCost Impact on ROI by Product:\n"
                for product in roi_by_product.index:
                    product_data = df[df['Product'] == product]
                    ratio = product_data['Operating Expenses'].sum() / product_data['Revenue'].sum() * 100
                    detailed_analysis += f"{product} Operating Cost Ratio: {ratio:.2f}%\n"

        elif report_type == "Regional Analysis":
            regional_analysis = financial_analyzer.analyze_by_region()
            for metric in metrics_to_show:
                if metric == "Revenue":
                    detailed_analysis += f"\nRegional Revenue Distribution:\n{regional_analysis['revenue'].to_string()}\n"
                elif metric == "Operating Expenses":
                    detailed_analysis += f"\nRegional Operating Expenses:\n{regional_analysis['expenses'].to_string()}\n"
                elif metric == "Profit Margin":
                    detailed_analysis += f"\nRegional Profit Margins:\n{regional_analysis['profit_margin'].to_string()}\n"

        elif report_type == "Product Analysis":
            product_analysis = financial_analyzer.analyze_by_product()
            for metric in metrics_to_show:
                if metric == "Revenue":
                    detailed_analysis += f"\nProduct Revenue Analysis:\n{product_analysis['revenue'].to_string()}\n"
                elif metric == "Profit Margin":
                    detailed_analysis += f"\nProduct Profit Margins:\n{product_analysis['profit_margin'].to_string()}\n"
                elif metric == "ROI":
                    roi_by_product = financial_analyzer.calculate_roi().groupby(df['Product']).mean()
                    detailed_analysis += f"\nProduct ROI Analysis:\n{roi_by_product.to_string()}\n"

        # Add time trends if selected
        if "Time Trends" in metrics_to_show:
            monthly_trends = df.groupby(df['Date'].dt.strftime('%Y-%m')).agg({
                'Revenue': 'sum',
                'Profit Margin': 'mean',
                'Operating Expenses': 'sum'
            }).tail(3)
            detailed_analysis += f"\nRecent Performance Trends:\n{monthly_trends.to_string()}\n"

        # Create prompt for report generation
        prompt = f"""
        Please analyze the following agricultural client data focusing on {report_type} analysis with emphasis on {', '.join(metrics_to_show)}:

        Dataset Overview:
        - Time Period: {analysis['date_range']}
        - Total Revenue: ${analysis['total_revenue']:,.2f}
        - Total Expenses: ${analysis['total_expense']:,.2f}
        - Average Profit Margin: {analysis['average_profit_margin']:.2f}%

        {detailed_analysis}

        Please generate a detailed financial report that prioritizes {report_type} insights and includes:
        1. Executive Summary (emphasizing {report_type} metrics)
        2. {'Regional Performance Analysis' if report_type == 'Regional Analysis' else 'Regional Overview'}
        3. {'Product Performance Analysis' if report_type == 'Product Analysis' else 'Product Overview'}
        4. {'ROI Analysis' if report_type == 'ROI Focused' else 'Performance Metrics'}
        5. Recommendations focused on:
           {'- ROI improvement strategies' if report_type == 'ROI Focused' else ''}
           {'- Regional optimization' if report_type == 'Regional Analysis' else ''}
           {'- Product mix enhancement' if report_type == 'Product Analysis' else ''}
           - Revenue growth opportunities
           - Cost reduction strategies
        6. Risk Assessment
        """

        debug_print(f"Generating {report_type} report with metrics: {metrics_to_show}")
        return generate_financial_report(prompt)
        
    except Exception as e:
        debug_print(f"Error processing file: {str(e)}")
        return None
    
    
def generate_ebitda_report(df: pd.DataFrame, case_type: str = None) -> str:
    """Generate a detailed EBITDA report based on specific case type"""
    debug_print("Starting EBITDA report generation")
    try:
        total_ebitda = "${:,.2f}".format(df['EBITDA'].sum())
        avg_margin = "{:.2f}%".format(df['EBITDA Margin'].mean())
        total_revenue = "${:,.2f}".format(df['Revenue'].sum())
        total_expenses = "${:,.2f}".format(df['Operating Expenses'].sum())

        analyzer = EBITDAAnalyzer(df)
        analysis = analyzer.analyze_by_case(case_type)

        prompt = f"""
        You are a financial analyst specializing in EBITDA analysis. Please provide a detailed analysis of the following financial data:

        Overall Performance Metrics:
        - Total EBITDA: {total_ebitda}
        - Average EBITDA Margin: {avg_margin}
        - Total Revenue: {total_revenue}
        - Total Operating Expenses: {total_expenses}

        Detailed Analysis:
        {analysis.get('report', '')}

        Please structure your report to include:
        1. Executive Summary of overall EBITDA performance
        2. Analysis of the provided metrics and their implications
        3. Key performance insights and trends
        4. Areas of strength and potential improvement
        5. Specific recommendations based on the data
        6. Risk factors and mitigation strategies
        7. Forward-looking considerations

        Focus on actionable insights and strategic recommendations.
        """

        return generate_financial_report(prompt)
    
    except Exception as e:
        debug_print(f"Error generating EBITDA report: {str(e)}")
        return f"Error generating EBITDA report: {str(e)}"

if __name__ == "__main__":
    debug_print("Running report_generation.py standalone")
    sample = PROJECT_ROOT / 'data' / 'sample_financial_data.csv'
    report = generate_report_from_csv(str(sample))
    if report:
        out = PROJECT_ROOT / 'reports' / f"report_{datetime.now().strftime('%Y%m%d')}.txt"
        out.parent.mkdir(exist_ok=True)
        out.write_text(report)
        print(f"Report saved to {out}")
    else:
        print("Report generation failed.")
