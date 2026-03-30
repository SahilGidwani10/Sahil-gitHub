import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

FILE_NAME = Path(__file__).with_name("expenses.json")


def load_expenses():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_expenses(expenses):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


class ExpenseTrackerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("920x580")
        self.root.minsize(820, 500)

        self.colors = {
            "bg": "#F7F6F3",
            "card": "#FFFFFF",
            "text": "#37352F",
            "muted": "#787774",
            "border": "#E9E9E7",
            "accent": "#2383E2",
        }

        self.root.configure(bg=self.colors["bg"])
        self.expenses = load_expenses()

        self._build_styles()
        self._build_layout()
        self._refresh_table()

    def _build_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background=self.colors["card"],
            fieldbackground=self.colors["card"],
            foreground=self.colors["text"],
            rowheight=34,
            borderwidth=0,
            font=("Helvetica", 11),
        )
        try:
            style.configure(
                "Treeview.Heading",
                background=self.colors["card"],
                foreground=self.colors["muted"],
                borderwidth=0,
                font=("Helvetica", 10, "bold"),
            )
        except tk.TclError:
            pass

        try:
            style.map("Treeview", background=[("selected", "#EEF5FD")])
        except tk.TclError:
            pass

        try:
            style.configure(
                "Vertical.TScrollbar",
                troughcolor=self.colors["bg"],
                background=self.colors["border"],
                borderwidth=0,
                arrowsize=12,
            )
        except tk.TclError:
            pass

    def _build_layout(self):
        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(fill="both", expand=True, padx=26, pady=22)

        header = tk.Frame(container, bg=self.colors["bg"])
        header.pack(fill="x", pady=(0, 16))

        tk.Label(
            header,
            text="Expense Tracker",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=("Georgia", 24, "bold"),
        ).pack(side="left")

        self.total_label = tk.Label(
            header,
            text="Total: 0.00",
            bg=self.colors["bg"],
            fg=self.colors["muted"],
            font=("Helvetica", 12),
        )
        self.total_label.pack(side="right")

        form_card = tk.Frame(
            container,
            bg=self.colors["card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )
        form_card.pack(fill="x", pady=(0, 14))

        form_grid = tk.Frame(form_card, bg=self.colors["card"])
        form_grid.pack(fill="x", padx=14, pady=14)

        tk.Label(
            form_grid,
            text="Amount",
            bg=self.colors["card"],
            fg=self.colors["muted"],
            font=("Helvetica", 10),
        ).grid(row=0, column=0, sticky="w", padx=(0, 10))
        tk.Label(
            form_grid,
            text="Category",
            bg=self.colors["card"],
            fg=self.colors["muted"],
            font=("Helvetica", 10),
        ).grid(row=0, column=1, sticky="w", padx=(0, 10))
        tk.Label(
            form_grid,
            text="Description",
            bg=self.colors["card"],
            fg=self.colors["muted"],
            font=("Helvetica", 10),
        ).grid(row=0, column=2, sticky="w", padx=(0, 10))

        self.amount_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.description_var = tk.StringVar()

        entry_opts = {
            "bg": "#FCFCFB",
            "fg": self.colors["text"],
            "relief": "flat",
            "highlightthickness": 1,
            "highlightbackground": self.colors["border"],
            "highlightcolor": self.colors["accent"],
            "insertbackground": self.colors["text"],
            "font": ("Helvetica", 11),
        }

        amount_entry = tk.Entry(form_grid, textvariable=self.amount_var, **entry_opts)
        amount_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(6, 0))

        category_entry = tk.Entry(form_grid, textvariable=self.category_var, **entry_opts)
        category_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(6, 0))

        description_entry = tk.Entry(form_grid, textvariable=self.description_var, **entry_opts)
        description_entry.grid(row=1, column=2, sticky="ew", padx=(0, 10), pady=(6, 0))

        add_button = tk.Button(
            form_grid,
            text="Add",
            command=self._add_expense,
            bg=self.colors["text"],
            fg="#FFFFFF",
            activebackground="#2A2925",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=18,
            pady=8,
            font=("Helvetica", 10, "bold"),
            cursor="hand2",
        )
        add_button.grid(row=1, column=3, sticky="ew", pady=(6, 0))

        form_grid.columnconfigure(0, weight=1)
        form_grid.columnconfigure(1, weight=1)
        form_grid.columnconfigure(2, weight=2)
        form_grid.columnconfigure(3, weight=0)

        table_card = tk.Frame(
            container,
            bg=self.colors["card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )
        table_card.pack(fill="both", expand=True)

        table_wrap = tk.Frame(table_card, bg=self.colors["card"])
        table_wrap.pack(fill="both", expand=True, padx=12, pady=12)

        self.tree = ttk.Treeview(
            table_wrap,
            columns=("amount", "category", "description"),
            show="headings",
        )
        self.tree.heading("amount", text="Amount")
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")
        self.tree.column("amount", width=140, anchor="e")
        self.tree.column("category", width=180, anchor="w")
        self.tree.column("description", width=420, anchor="w")

        scrollbar = ttk.Scrollbar(
            table_wrap, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar"
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        footer = tk.Frame(container, bg=self.colors["bg"])
        footer.pack(fill="x", pady=(10, 0))

        tk.Button(
            footer,
            text="Delete Selected",
            command=self._delete_selected,
            bg=self.colors["bg"],
            fg=self.colors["muted"],
            activebackground=self.colors["bg"],
            activeforeground=self.colors["text"],
            relief="flat",
            font=("Helvetica", 10),
            cursor="hand2",
        ).pack(side="right")

        amount_entry.focus_set()
        self.root.bind("<Return>", lambda _event: self._add_expense())

    def _refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for index, exp in enumerate(self.expenses):
            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    f"{float(exp.get('amount', 0.0)):.2f}",
                    exp.get("category", ""),
                    exp.get("description", ""),
                ),
            )

        total = sum(float(exp.get("amount", 0.0)) for exp in self.expenses)
        self.total_label.config(text=f"Total: {total:.2f}")

    def _add_expense(self):
        amount_text = self.amount_var.get().strip()
        category = self.category_var.get().strip()
        description = self.description_var.get().strip()

        if not amount_text or not category or not description:
            messagebox.showwarning("Missing fields", "Please fill all fields.")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Invalid amount", "Amount must be a number.")
            return

        if amount < 0:
            messagebox.showerror("Invalid amount", "Amount cannot be negative.")
            return

        self.expenses.append(
            {
                "amount": amount,
                "category": category,
                "description": description,
            }
        )
        save_expenses(self.expenses)
        self._refresh_table()

        self.amount_var.set("")
        self.category_var.set("")
        self.description_var.set("")

    def _delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return

        selected_indexes = sorted((int(item) for item in selected), reverse=True)
        for idx in selected_indexes:
            if 0 <= idx < len(self.expenses):
                self.expenses.pop(idx)

        save_expenses(self.expenses)
        self._refresh_table()


def main():
    root = tk.Tk()
    ExpenseTrackerUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
