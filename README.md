```
🌾 Agricultural Financial Report Generator

An intelligent web application for generating financial reports from agricultural datasets. Upload CSVs, configure analysis preferences, and get real-time insights — all powered by a modern React + Flask stack.

📦 Features

An intuitive tool for:

- Uploading agricultural financial data (CSV format)
- Selecting metrics and EBITDA analysis preferences
- Generating dynamic dashboards and markdown reports
- Visualizing trends with interactive Plotly charts
- Downloading structured financial summaries
- Real-time configuration updates and toggles

 🛠️ Prerequisites

- Node.js (v16+)
- Python 3.8+
- npm and pip
- (Optional) Python virtual environment

 🚀 Getting Started

 1. Clone the Repository

```bash
git clone https://github.com/your-username/agri-financial-insights-dash.git
cd agri-financial-insights-dash
```

 2. 🌐 Frontend Setup (React + Vite)

```bash
cd agri-frontend
npm install
```

This will install all required packages including:
- React
- Vite
- PapaParse
- Tailwind CSS
- React Plotly
- Headless UI

Start the development server:

```bash
npm run dev
```

Runs at: [http://localhost:5173](http://localhost:5173)

 3. 🔧 Backend Setup (Flask + Pandas)

From the project root:

```bash
python3 -m venv agri
source agri/bin/activate
```

Then install backend dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask server:

```bash
python app.py
```

Runs at: [http://localhost:8000](http://localhost:8000)

---

 🖥️ Usage Instructions

1. Upload a `.csv` file with fields such as Revenue, Profit Margin, Region, Product, etc.
2. Choose report type, metrics, and EBITDA analysis case
3. View dashboard, charts, and AI-generated reports
4. Download insights for further use or sharing

CSV should contain fields like:

```
Date, Client Name, Region, Product, Revenue, Operating Expenses,
Raw Material Cost, Labor Cost, Overhead Cost, Depreciation, Amortization,
Interest, Taxes, EBITDA, EBITDA Margin, Profit Margin
```

 📊 Tech Stack

- **Frontend**: React, Vite, Tailwind CSS, PapaParse, Plotly.js
- **Backend**: Flask, Pandas, NumPy, Plotly
- **Architecture**: Flask REST API + Modern React UI

 🧠 Real-Time Setup Flow

Make sure both servers are running:

```bash
 Terminal 1 (Backend)
source agri/bin/activate
python app.py

 Terminal 2 (Frontend)
cd agri-frontend
npm run dev
```

Then open: **http://localhost:5173**

Upload → Configure → Analyze → Download

```
