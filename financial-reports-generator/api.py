# api.py
from flask import Flask, request, jsonify
import pandas as pd
from report_generation import (
    generate_report_from_csv,
    analyze_financial_data,
    generate_ebitda_report
)
from charts import (
    create_region_chart,
    create_time_series_chart,
    create_product_performance_chart,
    create_ebitda_charts
)

app = Flask(__name__)

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    # 1. Grab file + params from request
    uploaded = request.files['file']
    report_type = request.form['reportType']
    metrics = request.form['metrics'].split(',')
    case_type = request.form['caseType']
    include_ebitda = request.form.get('includeEbitda', 'false').lower() == 'true'

    # 2. Read into DataFrame
    df = pd.read_csv(uploaded)

    # 3. Run your existing analysis functions
    analysis = analyze_financial_data(df)
    region_fig = create_region_chart(df)
    time_fig   = create_time_series_chart(df)
    product_fig = create_product_performance_chart(df)

    # 4. Optionally EBITDA
    ebitda_report = None
    ebitda_charts = {}
    if include_ebitda:
        ebitda_report = generate_ebitda_report(df, case_type.lower())
        ebitda_charts = create_ebitda_charts(df)

    # 5. Package everything as JSON, serializing Plotly figures
    payload = {
        'analysis': {
            **analysis,
            'regionChart': region_fig.to_dict(),
            'timeSeriesChart': time_fig.to_dict(),
            'productChart': product_fig.to_dict(),
            'ebitda': {
                'report': ebitda_report,
                **{name: fig.to_dict() for name, fig in ebitda_charts.items()}
            } if include_ebitda else None
        },
        'report': generate_report_from_csv(uploaded, report_type, metrics),
        'ebitdaReport': ebitda_report
    }
    return jsonify(payload)

if __name__ == '__main__':
    app.run(debug=True, port=8000)