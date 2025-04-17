# app.py

import os
import io
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

import matplotlib
matplotlib.use('Agg')  # Must be called before other matplotlib imports

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from flask import Flask, request, jsonify
from flask_cors import CORS

import numpy as np

import plotly.graph_objects as go

def _sanitize(obj):
    """
    Recursively walk through lists/dicts and convert any numpy scalars/arrays
    or plotly Figures into native Python types.
    """
    # 1) Figure → dict **and** sanitize its contents
    if isinstance(obj, go.Figure):
        return _sanitize(obj.to_dict())

    # 2) dict → sanitize each value
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    # 3) list → sanitize each element
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    # 4) numpy scalar → native Python
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    # 5) numpy array → list
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    # 6) everything else (str, bool, None, int, float) as‑is
    return obj

from report_generation import (
    generate_report_from_csv,
    analyze_financial_data,
    generate_ebitda_report
)

# Debug mode flag
DEBUG = True

def debug_print(message: str):
    """Helper function for debug printing"""
    if DEBUG:
        print(f"DEBUG - {message}")

# Project paths
PROJECT_ROOT = Path('/Users/raghu/Desktop/huggingface_proj/finance-generator-react/financial-reports-generator')
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"
DEFAULT_DATA_PATH = DATA_DIR / "sample_financial_data.csv"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Caching state to mimic Streamlit session_state
previous_report: str = None
previous_params: str = None
previous_file_hash: int = None
previous_df: pd.DataFrame = None

# Helper functions (removing @st.cache_data decorators)

def load_and_process_data(file_content) -> pd.DataFrame:
    """Load the data from a file path or file-like object"""
    debug_print("Loading and processing data...")
    if isinstance(file_content, (str, Path)):
        return pd.read_csv(file_content)
    else:
        return pd.read_csv(file_content)


def generate_cached_report(_file_content, report_type: str, metrics: List[str]) -> str:
    """Generate report text using the existing logic"""
    debug_print("Generating cached report...")
    return generate_report_from_csv(_file_content, report_type, metrics)


def create_region_chart(df: pd.DataFrame) -> go.Figure:
    """Create enhanced region-wise performance chart with both revenue and profit margin"""
    debug_print("Creating region chart")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    revenue_by_region = df.groupby('Region')['Revenue'].sum()
    debug_print(f"Revenue by region: {revenue_by_region}")
    fig.add_trace(
        go.Bar(
            name="Revenue",
            x=revenue_by_region.index,
            y=revenue_by_region.values,
            marker_color='rgb(26, 118, 255)'
        ),
        secondary_y=False,
    )
    profit_by_region = df.groupby('Region')['Profit Margin'].mean()
    debug_print(f"Profit margin by region: {profit_by_region}")
    fig.add_trace(
        go.Scatter(
            name="Profit Margin",
            x=profit_by_region.index,
            y=profit_by_region.values,
            mode='lines+markers',
            line=dict(color='rgb(255, 127, 14)', width=3),
            marker=dict(size=10)
        ),
        secondary_y=True,
    )
    fig.update_layout(
        title="Regional Performance Overview",
        hovermode='x unified',
        barmode='group',
        height=500
    )
    fig.update_yaxes(title_text="Revenue ($)", secondary_y=False)
    fig.update_yaxes(title_text="Profit Margin (%)", secondary_y=True)
    return fig


def create_product_performance_chart(df: pd.DataFrame) -> go.Figure:
    """Create enhanced product performance analysis"""
    debug_print("Creating product performance chart")
    df_product = df.groupby('Product').agg({
        'Revenue': 'sum',
        'Profit Margin': 'mean',
        'Operating Expenses': 'sum'
    }).reset_index()
    debug_print("Calculating ROI")
    df_product['ROI'] = (
        (df_product['Revenue'] - df_product['Operating Expenses'])
        / df_product['Operating Expenses'] * 100
    )
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Revenue by Product", "Profit Margin by Product",
            "ROI by Product", "Revenue vs. Profit Margin"
        )
    )
    fig.add_trace(
        go.Bar(x=df_product['Product'], y=df_product['Revenue'], name="Revenue"),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(
            x=df_product['Product'], y=df_product['Profit Margin'],
            name="Profit Margin", marker_color='rgb(255, 127, 14)'
        ),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(x=df_product['Product'], y=df_product['ROI'], name="ROI", marker_color='rgb(44, 160, 44)'),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=df_product['Revenue'],
            y=df_product['Profit Margin'],
            mode='markers+text', name="Products",
            text=df_product['Product'], textposition="top center",
            marker=dict(size=15)
        ),
        row=2, col=2
    )
    fig.update_layout(height=800, title_text="Product Performance Analysis", showlegend=False)
    return fig


def create_time_series_chart(df: pd.DataFrame) -> go.Figure:
    """Create time series analysis chart"""
    debug_print("Creating time series chart")
    df_time = df.groupby('Date').agg({
        'Revenue': 'sum',
        'Profit Margin': 'mean'
    }).reset_index()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=df_time['Date'], y=df_time['Revenue'], name="Revenue", mode='lines+markers'),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=df_time['Date'], y=df_time['Profit Margin'],
            name="Profit Margin", mode='lines+markers',
            line=dict(color='rgb(255, 127, 14)')
        ),
        secondary_y=True,
    )
    fig.update_layout(title="Time Series Analysis",
                     xaxis_title="Date", height=400)
    fig.update_yaxes(title_text="Revenue ($)", secondary_y=False)
    fig.update_yaxes(title_text="Profit Margin (%)", secondary_y=True)
    return fig


def create_ebitda_charts(df: pd.DataFrame) -> Dict[str, go.Figure]:
    """Create comprehensive EBITDA analysis visualizations"""
    debug_print("Creating EBITDA charts")
    # Waterfall chart
    latest_month = df['Date'].max()
    month_data = df[df['Date'].dt.to_period('M') == pd.Period(latest_month, freq='M')]
    measures = ['Revenue', 'Raw Material Cost', 'Labor Cost', 'Overhead Cost', 'EBITDA']
    values = [
        month_data['Revenue'].sum(),
        -month_data['Raw Material Cost'].sum(),
        -month_data['Labor Cost'].sum(),
        -month_data['Overhead Cost'].sum(),
        month_data['EBITDA'].sum()
    ]
    wf = go.Figure(go.Waterfall(
        name="EBITDA Bridge", orientation="v",
        measure=["relative"]*4 + ["total"],
        x=measures, y=values
    ))
    wf.update_layout(title="EBITDA Bridge Analysis", height=500)
    # Margin trends
    df_monthly = df.groupby(df['Date'].dt.to_period('M')).agg({
        'EBITDA Margin': 'mean', 'Profit Margin': 'mean'
    }).reset_index()
    df_monthly['Date'] = df_monthly['Date'].astype(str)
    mt = go.Figure()
    mt.add_trace(go.Scatter(x=df_monthly['Date'], y=df_monthly['EBITDA Margin'], name='EBITDA Margin'))
    mt.add_trace(go.Scatter(x=df_monthly['Date'], y=df_monthly['Profit Margin'], name='Net Profit Margin'))
    mt.update_layout(title='EBITDA vs Net Profit Margin Trends', height=400)
    # Component analysis pie
    components = ['Raw Material Cost', 'Labor Cost', 'Overhead Cost', 'Depreciation', 'Amortization', 'Interest', 'Taxes']
    total_revenue = df['Revenue'].sum()
    percentages = [df[c].sum() / total_revenue * 100 for c in components]
    cp = go.Figure(go.Pie(labels=components, values=percentages, hole=.3))
    cp.update_layout(title='Cost Components as % of Revenue', height=500)
    return {'waterfall': wf, 'margins': mt, 'components': cp}

# Flask app initialization
app = Flask(__name__)
CORS(app)

@app.route('/api/generate-report', methods=['POST'])
def generate_report_endpoint():
    global previous_report, previous_params, previous_file_hash, previous_df

    # 1) Retrieve file and form params
    uploaded = request.files.get('file')
    report_type = request.form.get('reportType', 'Standard')
    metrics = request.form.get('metrics', '')
    metrics_to_show = metrics.split(',') if metrics else []
    case_type = request.form.get('caseType', 'Comprehensive')
    include_ebitda = request.form.get('includeEbitda', 'false').lower() == 'true'

    debug_print(f"Params received: type={report_type}, metrics={metrics_to_show}, case={case_type}, includeEbitda={include_ebitda}")

    # 2) Compute file hash and params string for caching
    uploaded.stream.seek(0)
    data_bytes = uploaded.read()
    file_hash = hashlib.md5(data_bytes).hexdigest()
    params_str = f"{report_type}-{'-'.join(sorted(metrics_to_show))}-{case_type}-{include_ebitda}"
    debug_print(f"file_hash={file_hash}, params={params_str}")

    # 3) Load or reuse DataFrame and report
    if previous_file_hash == file_hash and previous_params == params_str:
        debug_print("Using cached report and data")
        df = previous_df
        report_text = previous_report
    else:
        debug_print("Processing new upload")
        df = pd.read_csv(io.StringIO(data_bytes.decode('utf-8')))
        df['Date'] = pd.to_datetime(df['Date'])
        # Validate required columns
        required_columns = [
            'Date','Client Name','Region','Product','Revenue','Operating Expenses',
            'Raw Material Cost','Labor Cost','Overhead Cost','Depreciation',
            'Amortization','Interest','Taxes','EBITDA','EBITDA Margin','Profit Margin'
        ]
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            return jsonify({"error": f"Missing columns: {missing}"}), 400
        report_text = generate_cached_report(uploaded, report_type, metrics_to_show)
        # Cache state
        previous_df = df
        previous_report = report_text
        previous_file_hash = file_hash
        previous_params = params_str

    # 4) Analysis
    analysis = analyze_financial_data(df)

    # 5) Charts
    region_fig = create_region_chart(df).to_dict()
    prod_fig   = create_product_performance_chart(df).to_dict()
    ts_fig     = create_time_series_chart(df).to_dict()
    ebitda_figs = create_ebitda_charts(df) if include_ebitda else {}

    # 6) EBITDA text
    ebitda_text = generate_ebitda_report(df, case_type) if include_ebitda else None

    # If report text generation failed
    if report_text is None:
        debug_print("Report generation returned None")
        return jsonify({"error": "Report generation failed"}), 500

    # 7) Save report
    combined = report_text + ("\n\n" + ebitda_text if ebitda_text else "")
    digest = hashlib.md5(combined.encode('utf-8')).hexdigest()[:6]
    fname = f"agri_report_{datetime.now():%Y%m%d_%H%M%S}_{digest}.txt"
    fp = REPORTS_DIR / fname
    fp.write_text(combined, encoding='utf-8')
    debug_print(f"Saved report to {fp}")

    # 8) JSON response
    payload={
        'analysis':analysis,
        'report':report_text,
        'ebitdaReport':ebitda_text,
        'charts':{
            'region':region_fig,
            'product':prod_fig,
            'timeSeries':ts_fig,
            'ebitda':ebitda_figs
        },
        'savedFilename':fname
    }
    return jsonify(_sanitize(payload)),200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)), debug=DEBUG)
