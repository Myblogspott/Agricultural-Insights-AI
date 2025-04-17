import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class EBITDAMetrics:
    """Class to hold EBITDA calculation components"""
    revenue: float
    operating_expenses: float
    depreciation: float
    amortization: float
    interest: float
    taxes: float
    ebitda: float
    ebitda_margin: float
    
class EBITDAAnalyzer:
    """Class to handle EBITDA analysis and report generation"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.metrics = {}
        
    def calculate_base_ebitda(self, row: pd.Series) -> float:
        """Calculate basic EBITDA for a row of data"""
        return (row['Revenue'] - row['Operating Expenses'] + 
                row.get('Depreciation', 0) + 
                row.get('Amortization', 0) + 
                row.get('Interest', 0) + 
                row.get('Taxes', 0))

    def calculate_metrics_by_segment(self, segment_column: str) -> Dict[str, EBITDAMetrics]:
        """Calculate EBITDA metrics segmented by a specific column"""
        metrics = {}
        
        for segment in self.df[segment_column].unique():
            segment_data = self.df[self.df[segment_column] == segment]
            
            revenue = segment_data['Revenue'].sum()
            expenses = segment_data['Operating Expenses'].sum()
            depreciation = segment_data.get('Depreciation', pd.Series([0])).sum()
            amortization = segment_data.get('Amortization', pd.Series([0])).sum()
            interest = segment_data.get('Interest', pd.Series([0])).sum()
            taxes = segment_data.get('Taxes', pd.Series([0])).sum()
            
            ebitda = revenue - expenses + depreciation + amortization + interest + taxes
            ebitda_margin = (ebitda / revenue * 100) if revenue != 0 else 0
            
            metrics[segment] = EBITDAMetrics(
                revenue=revenue,
                operating_expenses=expenses,
                depreciation=depreciation,
                amortization=amortization,
                interest=interest,
                taxes=taxes,
                ebitda=ebitda,
                ebitda_margin=ebitda_margin
            )
            
        return metrics

    def analyze_trends(self, period_column: str = 'Date') -> Dict[str, Any]:
        """Analyze EBITDA trends over time"""
        self.df[period_column] = pd.to_datetime(self.df[period_column])
        
        trends = {
            'monthly': {},
            'quarterly': {},
            'growth_rates': {},
            'seasonality': {}
        }
        
        # Monthly analysis
        monthly_data = self.df.groupby(self.df[period_column].dt.to_period('M')).agg({
            'Revenue': 'sum',
            'Operating Expenses': 'sum'
        })
        trends['monthly'] = monthly_data.to_dict()
        
        # Quarterly analysis
        quarterly_data = self.df.groupby(self.df[period_column].dt.to_period('Q')).agg({
            'Revenue': 'sum',
            'Operating Expenses': 'sum'
        })
        trends['quarterly'] = quarterly_data.to_dict()
        
        return trends

    def generate_segment_report(self, segment_column: str) -> str:
        """Generate detailed EBITDA report for segments"""
        metrics = self.calculate_metrics_by_segment(segment_column)
        
        report = f"""
EBITDA Analysis Report by {segment_column}
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}

Summary:
"""
        total_ebitda = sum(m.ebitda for m in metrics.values())
        
        for segment, metric in metrics.items():
            contribution = (metric.ebitda / total_ebitda * 100) if total_ebitda != 0 else 0
            
            report += f"""
{segment} Segment Analysis:
---------------------------
Revenue: ${metric.revenue:,.2f}
Operating Expenses: ${metric.operating_expenses:,.2f}
EBITDA: ${metric.ebitda:,.2f}
EBITDA Margin: {metric.ebitda_margin:.2f}%
Contribution to Total EBITDA: {contribution:.2f}%

Detailed Components:
- Depreciation: ${metric.depreciation:,.2f}
- Amortization: ${metric.amortization:,.2f}
- Interest: ${metric.interest:,.2f}
- Taxes: ${metric.taxes:,.2f}

"""
        return report

    def analyze_by_case(self, case_type: str) -> Dict[str, Any]:
        """Analyze EBITDA based on specific business case"""
        analysis = {}
        
        if case_type == "regional":
            analysis = {
                'metrics': self.calculate_metrics_by_segment('Region'),
                'trends': self.analyze_trends(),
                'report': self.generate_segment_report('Region')
            }
            
        elif case_type == "product":
            analysis = {
                'metrics': self.calculate_metrics_by_segment('Product'),
                'trends': self.analyze_trends(),
                'report': self.generate_segment_report('Product')
            }
            
        elif case_type == "client":
            analysis = {
                'metrics': self.calculate_metrics_by_segment('Client Name'),
                'trends': self.analyze_trends(),
                'report': self.generate_segment_report('Client Name')
            }
            
        return analysis

    def get_recommendations(self, metrics: Dict[str, EBITDAMetrics]) -> list:
        """Generate recommendations based on EBITDA analysis"""
        recommendations = []
        
        for segment, metric in metrics.items():
            if metric.ebitda_margin < 10:
                recommendations.append(f"Review cost structure for {segment} - low EBITDA margin of {metric.ebitda_margin:.2f}%")
            if metric.operating_expenses / metric.revenue > 0.8:
                recommendations.append(f"High operating expenses in {segment} - consider cost optimization")
                
        return recommendations
