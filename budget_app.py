class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        total = 0
        for entry in self.ledger:
            items += f"{entry['description'][:23]:23}{entry['amount']:>7.2f}\n"
            total += entry['amount']
        return title + items + f"Total: {total:.2f}"

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(entry["amount"] for entry in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()


def create_spend_chart(categories):
    # 1. Calculate withdrawals and percentages
    withdrawals = []
    for cat in categories:
        spent = sum(-entry["amount"] for entry in cat.ledger if entry["amount"] < 0)
        withdrawals.append(spent)

    total_spent = sum(withdrawals)
    # The test specifically wants rounding down to the nearest 10
    percentages = [int((spent / total_spent) * 10) * 10 for spent in withdrawals]

    # 2. Build the top of the chart (the "o" bars)
    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += f"{i:>3}|"
        for percent in percentages:
            if percent >= i:
                chart += " o "
            else:
                chart += "   "
        chart += " \n" # Note the single space after the last "o" before the newline

    # 3. The horizontal separator line
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # 4. Vertical category names
    max_len = max(len(cat.name) for cat in categories)
    names = [cat.name for cat in categories]

    for i in range(max_len):
        chart += "     " # 5 spaces of initial padding
        for name in names:
            if i < len(name):
                chart += f"{name[i]}  "
            else:
                chart += "   " # Fill with 3 spaces if name is shorter
        
        # This prevents an extra newline at the very end of the string
        if i < max_len - 1:
            chart += "\n"

    return chart

