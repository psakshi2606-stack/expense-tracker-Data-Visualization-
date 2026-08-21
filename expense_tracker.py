"""
Expense Tracker
----------------
Core module for logging, categorizing, and analyzing personal expenses.
"""

import csv
import os
from datetime import datetime
from collections import defaultdict


CATEGORIES = [
    "Food & Dining",
    "Groceries",
    "Transport",
    "Shopping",
    "Entertainment",
    "Bills & Utilities",
    "Health",
    "Education",
    "Rent",
    "Miscellaneous",
]


class Transaction:
    def __init__(self, date, description, amount, category):
        self.date = date
        self.description = description
        self.amount = float(amount)
        self.category = category

    def to_row(self):
        return [self.date, self.description, f"{self.amount:.2f}", self.category]

    @staticmethod
    def from_row(row):
        return Transaction(row[0], row[1], row[2], row[3])


class ExpenseTracker:
    """Handles storage, categorization, and analysis of transactions."""

    def __init__(self, data_file="data/transactions.csv"):
        self.data_file = data_file
        self.transactions = []
        self._ensure_file()
        self.load()

    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["date", "description", "amount", "category"])

    def load(self):
        self.transactions = []
        with open(self.data_file, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if row:
                    self.transactions.append(Transaction.from_row(row))

    def add_transaction(self, date, description, amount, category=None):
        """Add a new transaction. Auto-categorizes if category is not given."""
        if category is None:
            category = self.categorize(description)
        elif category not in CATEGORIES:
            raise ValueError(f"Unknown category: {category}")

        txn = Transaction(date, description, amount, category)
        self.transactions.append(txn)
        self._append_to_file(txn)
        return txn

    def _append_to_file(self, txn):
        with open(self.data_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(txn.to_row())

    @staticmethod
    def categorize(description):
        """Simple rule-based auto-categorization from keywords in the description."""
        desc = description.lower()
        keyword_map = {
            "Food & Dining": ["restaurant", "cafe", "coffee", "swiggy", "zomato", "dinner", "lunch", "breakfast"],
            "Groceries": ["grocery", "supermarket", "bigbasket", "market", "vegetables"],
            "Transport": ["uber", "ola", "petrol", "fuel", "metro", "bus", "cab", "auto"],
            "Shopping": ["amazon", "flipkart", "myntra", "mall", "clothing", "shoes"],
            "Entertainment": ["movie", "netflix", "spotify", "concert", "game", "prime video"],
            "Bills & Utilities": ["electricity", "water bill", "internet", "recharge", "wifi", "phone bill"],
            "Health": ["pharmacy", "hospital", "doctor", "medicine", "clinic"],
            "Education": ["course", "book", "tuition", "udemy", "college fee"],
            "Rent": ["rent", "landlord"],
        }
        for category, keywords in keyword_map.items():
            if any(kw in desc for kw in keywords):
                return category
        return "Miscellaneous"

    def total_spend(self):
        return sum(t.amount for t in self.transactions)

    def spend_by_category(self):
        totals = defaultdict(float)
        for t in self.transactions:
            totals[t.category] += t.amount
        return dict(sorted(totals.items(), key=lambda x: x[1], reverse=True))

    def spend_by_month(self):
        totals = defaultdict(float)
        for t in self.transactions:
            month = datetime.strptime(t.date, "%Y-%m-%d").strftime("%Y-%m")
            totals[month] += t.amount
        return dict(sorted(totals.items()))

    def top_category_share(self):
        """Returns (top_category, percentage_of_total_spend)."""
        by_cat = self.spend_by_category()
        if not by_cat:
            return None, 0.0
        total = self.total_spend()
        top_cat = next(iter(by_cat))
        return top_cat, (by_cat[top_cat] / total * 100) if total else 0.0

    def summary(self):
        top_cat, share = self.top_category_share()
        return {
            "total_transactions": len(self.transactions),
            "total_spend": round(self.total_spend(), 2),
            "top_category": top_cat,
            "top_category_share_pct": round(share, 1),
            "spend_by_category": {k: round(v, 2) for k, v in self.spend_by_category().items()},
        }


if __name__ == "__main__":
    tracker = ExpenseTracker()
    print(f"Loaded {len(tracker.transactions)} transactions.")
    print(tracker.summary())
