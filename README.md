# Financial Tracker

A simple financial tracking application that helps you manage money more easily and effectively.

## Features
- Track income and expenses
- Set and manage budgets
- View financial data through visual graphs

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/nealbose/Financial-Tracker.git
cd Financial-Tracker
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and go to `http://localhost:5000`

## Project Structure
```
Financial-Tracker/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Dashboard
│   ├── add_transaction.html
│   ├── view_transactions.html
│   ├── budgets.html      # Budget management
│   └── reports.html      # Visual reports
├── static/                # Static files (CSS, JavaScript)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── database.db           # SQLite database (created on first run)
```
