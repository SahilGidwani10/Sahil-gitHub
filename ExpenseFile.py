import json

FILE_NAME = "expenses.json"


def load_expenses():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


def add_expense(expenses):
    amount = float(input("Enter amount: "))
    category = input("Enter category (Food, Travel, etc.): ")
    description = input("Enter description: ")

    expense = {
        "amount": amount,
        "category": category,
        "description": description
    }

    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added successfully!\n")


def view_expenses(expenses):
    if not expenses:
        print("No expenses found.\n")
        return

    print("\nAll Expenses:")
    for i, exp in enumerate(expenses, start=1):
        print(f"{i}. {exp['amount']} | {exp['category']} | {exp['description']}")
    print()


def total_expense(expenses):
    total = sum(exp["amount"] for exp in expenses)
    print(f"\nTotal Spending: {total}\n")


def main():
    expenses = load_expenses()

    while True:
        print("Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Spending")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            total_expense(expenses)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()

