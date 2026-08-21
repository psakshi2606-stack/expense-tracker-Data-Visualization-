"""
Generates 150+ realistic sample transactions for demo purposes, spread across
6 months, with spending intentionally concentrated in one category (Rent)
to mirror real-world spending patterns.
"""

import csv
import random
from datetime import date, timedelta

random.seed(42)

SAMPLE_ITEMS = {
    "Food & Dining": [("Zomato order", 250, 650), ("Cafe Coffee Day", 150, 400), ("Dinner with friends", 400, 1200)],
    "Groceries": [("BigBasket order", 500, 1800), ("Local grocery store", 200, 900)],
    "Transport": [("Uber ride", 100, 400), ("Petrol refill", 500, 1500), ("Metro card recharge", 100, 300)],
    "Shopping": [("Amazon purchase", 300, 3000), ("Myntra order", 500, 2500)],
    "Entertainment": [("Netflix subscription", 199, 649), ("Movie tickets", 300, 800), ("Spotify Premium", 119, 119)],
    "Bills & Utilities": [("Electricity bill", 800, 2200), ("Internet bill", 599, 999), ("Phone recharge", 199, 599)],
    "Health": [("Pharmacy purchase", 150, 700), ("Doctor consultation", 500, 1500)],
    "Education": [("Udemy course", 449, 1499), ("Book purchase", 200, 900)],
    "Rent": [("Monthly rent", 9000, 9000)],
    "Miscellaneous": [("Miscellaneous expense", 100, 500)],
}

def generate_transactions(n_months=7, start_date=None):
    if start_date is None:
        start_date = date(2026, 2, 1)

    transactions = []
    current = start_date

    for month_offset in range(n_months):
        month_start = date(current.year + (current.month - 1 + month_offset) // 12,
                            (current.month - 1 + month_offset) % 12 + 1, 1)

        # Fixed monthly rent transaction (drives top-category concentration)
        transactions.append((month_start.replace(day=1).isoformat(), "Monthly rent payment", 15000, "Rent"))

        # Random number of variable transactions per month (~20-24)
        n_txns = random.randint(20, 24)
        for _ in range(n_txns):
            category = random.choice([c for c in SAMPLE_ITEMS if c != "Rent"])
            desc, low, high = random.choice(SAMPLE_ITEMS[category])
            amount = round(random.uniform(low, high * 0.6), 2)
            day = random.randint(1, 28)
            txn_date = month_start.replace(day=day).isoformat()
            transactions.append((txn_date, desc, amount, category))

    transactions.sort(key=lambda t: t[0])
    return transactions


def main():
    transactions = generate_transactions()
    print(f"Generated {len(transactions)} transactions")

    with open("data/transactions.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "description", "amount", "category"])
        for txn in transactions:
            writer.writerow(txn)

    total = sum(t[2] for t in transactions)
    rent_total = sum(t[2] for t in transactions if t[3] == "Rent")
    print(f"Total spend: {total:.2f}")
    print(f"Rent share: {rent_total/total*100:.1f}%")


if __name__ == "__main__":
    main()
