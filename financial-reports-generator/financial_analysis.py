# financial_analysis.py
import pandas as pd
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class FinancialMetrics:
    """Class to hold financial calculation components"""
    total_revenue: float
    total_expense: float
    average_profit_margin: float
    top_profit_margin_client: str
    top_revenue_client: str
    date_range: str

class FinancialAnalyzer:
    """Class to handle financial data analysis"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.metrics = {}

    def analyze_financial_data(self) -> Dict[str, Any]:
        """Analyze agricultural client financial data to extract key metrics and trends."""
        try:
            analysis = {
                'total_revenue': self.df['Revenue'].sum(),
                'total_expense': self.df['Operating Expenses'].sum(),
                'average_profit_margin': self.df['Profit Margin'].mean(),
                'revenue_by_region': self.df.groupby('Region')['Revenue'].sum().to_dict(),
                'profit_margin_by_region': self.df.groupby('Region')['Profit Margin'].mean().to_dict(),
                'revenue_by_product': self.df.groupby('Product')['Revenue'].sum().to_dict(),
                'profit_margin_by_product': self.df.groupby('Product')['Profit Margin'].mean().to_dict(),
                'top_profit_margin_client': self.df.nlargest(1, 'Profit Margin')['Client Name'].iloc[0],
                'top_revenue_client': self.df.nlargest(1, 'Revenue')['Client Name'].iloc[0],
                'date_range': f"{self.df['Date'].min()} to {self.df['Date'].max()}"
            }
            return analysis
        except Exception as e:
            print(f"\nDEBUG - Error in financial analysis: {str(e)}")
            raise

    def analyze_by_region(self) -> Dict[str, Any]:
        """Analyze financial data by region"""
        try:
            regional_analysis = {
                'revenue': self.df.groupby('Region')['Revenue'].sum(),
                'profit_margin': self.df.groupby('Region')['Profit Margin'].mean(),
                'expenses': self.df.groupby('Region')['Operating Expenses'].sum()
            }
            return regional_analysis
        except Exception as e:
            print(f"\nDEBUG - Error in regional analysis: {str(e)}")
            raise

    def analyze_by_product(self) -> Dict[str, Any]:
        """Analyze financial data by product"""
        try:
            product_analysis = {
                'revenue': self.df.groupby('Product')['Revenue'].sum(),
                'profit_margin': self.df.groupby('Product')['Profit Margin'].mean(),
                'expenses': self.df.groupby('Product')['Operating Expenses'].sum()
            }
            return product_analysis
        except Exception as e:
            print(f"\nDEBUG - Error in product analysis: {str(e)}")
            raise

    def calculate_roi(self) -> pd.Series:
        """Calculate ROI for the data"""
        try:
            roi = ((self.df['Revenue'] - self.df['Operating Expenses']) / 
                   self.df['Operating Expenses'] * 100)
            return roi
        except Exception as e:
            print(f"\nDEBUG - Error calculating ROI: {str(e)}")
            raise

    def generate_metrics_report(self, metrics_to_show: List[str]) -> str:
        """Generate a report based on selected metrics"""
        try:
            report = "Financial Metrics Report\n"
            report += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            report += "=" * 80 + "\n\n"

            analysis = self.analyze_financial_data()
            
            if "Revenue" in metrics_to_show:
                report += f"Revenue Analysis:\n"
                report += f"Total Revenue: ${analysis['total_revenue']:,.2f}\n"
                report += f"Revenue by Region: {analysis['revenue_by_region']}\n\n"
                
            if "Profit Margin" in metrics_to_show:
                report += f"Profit Margin Analysis:\n"
                report += f"Average Profit Margin: {analysis['average_profit_margin']:.2f}%\n"
                report += f"Profit Margin by Region: {analysis['profit_margin_by_region']}\n\n"
                
            if "ROI" in metrics_to_show:
                roi_by_product = ((self.df.groupby('Product')['Revenue'].sum() - 
                                 self.df.groupby('Product')['Operating Expenses'].sum()) / 
                                 self.df.groupby('Product')['Operating Expenses'].sum() * 100)
                report += f"ROI Analysis:\n"
                report += f"ROI by Product: {roi_by_product.to_dict()}\n\n"

            return report
            
        except Exception as e:
            print(f"\nDEBUG - Error generating metrics report: {str(e)}")
            raise