"""
Expense Tracker CLI
--------------------
Simple command-line interface to log expenses and view spending summaries.

Usage:
    python main.py add "2026-08-15" "Zomato order" 350
    python main.py summary
"""

import sys
from expense_tracker import ExpenseTracker, CATEGORIES


def cmd_add(args):
    if len(args) < 3:
        print("Usage: python main.py add <date YYYY-MM-DD> <description> <amount> [category]")
        return
    date, description, amount = args[0], args[1], args[2]
    category = args[3] if len(args) > 3 else None

    tracker = ExpenseTracker()
    txn = tracker.add_transaction(date, description, amount, category)
    print(f"Added: {txn.date} | {txn.description} | ₹{txn.amount:.2f} | {txn.category}")


def cmd_summary(args):
    tracker = ExpenseTracker()
    summary = tracker.summary()

    print(f"\nTotal transactions: {summary['total_transactions']}")
    print(f"Total spend: ₹{summary['total_spend']:.2f}")
    print(f"Top category: {summary['top_category']} ({summary['top_category_share_pct']}% of spend)\n")

    print("Spend by category:")
    for cat, amt in summary["spend_by_category"].items():
        print(f"  {cat:<20} ₹{amt:>10.2f}")


def cmd_categories(args):
    print("Available categories:")
    for c in CATEGORIES:
        print(f"  - {c}")


COMMANDS = {
    "add": cmd_add,
    "summary": cmd_summary,
    "categories": cmd_categories,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        print(f"Available commands: {', '.join(COMMANDS.keys())}")
        return

    command = sys.argv[1]
    COMMANDS[command](sys.argv[2:])


if __name__ == "__main__":
    main()
