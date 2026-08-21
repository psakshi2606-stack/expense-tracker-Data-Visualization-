# Expense Tracker

A Python-based expense tracker that logs and auto-categorizes transactions, then generates visualizations to surface spending trends over time.

## Features

- **Transaction logging** — add expenses via CLI with date, description, and amount
- **Auto-categorization** — rule-based keyword matching sorts transactions into 10 categories (Food & Dining, Groceries, Transport, Shopping, Entertainment, Bills & Utilities, Health, Education, Rent, Miscellaneous)
- **Spending analysis** — total spend, category-wise breakdown, monthly trends
- **Visualizations** — monthly spending trend line chart, category breakdown (bar + pie chart)
- **Sample dataset** — 150+ generated transactions across 7 months for demo purposes

## Demo Insights

Using the included sample dataset (158 transactions, ₹176,968 total spend):
- **Rent accounted for 59.3% of total spend**, the single largest category — consistent with typical spending patterns where fixed costs dominate
- Remaining spend was distributed across 9 categories, with Shopping (7.1%) and Groceries (6.3%) next highest

![Category Breakdown](output/category_breakdown.png)
![Monthly Trend](output/monthly_trend.png)

## Project Structure

```
expense-tracker/
├── expense_tracker.py      # Core logic: Transaction, ExpenseTracker classes
├── generate_sample_data.py # Generates 150+ sample transactions
├── visualize.py             # Matplotlib visualizations
├── main.py                  # CLI entry point
├── data/
│   └── transactions.csv     # Transaction log
├── output/                  # Generated charts
└── requirements.txt
```

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Generate sample data (optional — creates 150+ demo transactions)
python generate_sample_data.py

# Add a transaction (category auto-detected if omitted)
python main.py add "2026-08-21" "Zomato order" 350

# View summary
python main.py summary

# Generate charts
python visualize.py
```

## Tech Stack

- **Python 3** — core application logic
- **matplotlib** — data visualization
- **CSV** — lightweight persistent storage

## How Auto-Categorization Works

Each transaction description is matched against a keyword dictionary (e.g. "uber", "zomato", "netflix") to assign a category automatically. Unmatched transactions fall back to "Miscellaneous". This keeps logging fast — no need to manually pick a category for common expenses.

## Future Improvements

- Migrate storage to SQLite for larger datasets
- Add a budget-vs-actual comparison view
- Web dashboard (Flask/Streamlit) instead of CLI
