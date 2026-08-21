"""
Generates visualizations of spending patterns:
1. Monthly spending trend (line chart)
2. Spend by category (bar chart + pie chart)
"""

import os
import matplotlib.pyplot as plt
from expense_tracker import ExpenseTracker


def plot_monthly_trend(tracker, output_dir="output"):
    monthly = tracker.spend_by_month()
    months = list(monthly.keys())
    amounts = list(monthly.values())

    plt.figure(figsize=(9, 5))
    plt.plot(months, amounts, marker="o", linewidth=2, color="#2E86AB")
    plt.fill_between(months, amounts, alpha=0.15, color="#2E86AB")
    plt.title("Monthly Spending Trend", fontsize=14, fontweight="bold")
    plt.xlabel("Month")
    plt.ylabel("Total Spend (₹)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/monthly_trend.png", dpi=150)
    plt.close()


def plot_category_breakdown(tracker, output_dir="output"):
    by_cat = tracker.spend_by_category()
    categories = list(by_cat.keys())
    amounts = list(by_cat.values())

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

    # Bar chart
    axes[0].barh(categories[::-1], amounts[::-1], color="#F18F01")
    axes[0].set_title("Spend by Category", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Amount (₹)")

    # Pie chart
    axes[1].pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90,
                colors=plt.cm.Set2.colors)
    axes[1].set_title("Category Share of Total Spend", fontsize=13, fontweight="bold")

    plt.tight_layout()
    plt.savefig(f"{output_dir}/category_breakdown.png", dpi=150)
    plt.close()


def main():
    os.makedirs("output", exist_ok=True)
    tracker = ExpenseTracker()

    if not tracker.transactions:
        print("No transactions found. Run generate_sample_data.py first.")
        return

    plot_monthly_trend(tracker)
    plot_category_breakdown(tracker)

    summary = tracker.summary()
    print("Summary:")
    print(f"  Total transactions: {summary['total_transactions']}")
    print(f"  Total spend: ₹{summary['total_spend']:.2f}")
    print(f"  Top category: {summary['top_category']} ({summary['top_category_share_pct']}% of spend)")
    print("Charts saved to output/monthly_trend.png and output/category_breakdown.png")


if __name__ == "__main__":
    main()
