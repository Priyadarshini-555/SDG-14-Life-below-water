# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 09:56:02 2025

@author: priya
"""

# gui.py
import os
import csv
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Optional plotting
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MPL = True
except Exception:
    HAS_MPL = False


DATA_DIR = "data"
ACTIONS_FILE = os.path.join(DATA_DIR, "actions.csv")


SDG14_FACTS = [
    ("What is SDG 14?", "SDG 14 aims to conserve and sustainably use oceans, seas, and marine resources."),
    ("Why it matters", "Oceans produce over half of the world's oxygen and regulate climate while supporting billions of livelihoods."),
    ("Main threats", "Plastic pollution, overfishing, habitat destruction, ocean acidification, and untreated wastewater."),
    ("Plastic facts", "An estimated millions of tons of plastic enter the oceans yearly, harming marine life that ingest or get entangled."),
    ("Overfishing", "Unsustainable fishing reduces fish populations and disrupts ecosystems; sustainable practices can reverse damage."),
    ("Local actions", "Reduce single-use plastic, segregate waste, join clean-ups, use eco-friendly products, and support sustainable seafood."),
    ("Policy matters", "Marine protected areas and strong regulations help ecosystems recover and thrive."),
]

QUIZ_QUESTIONS = [
    {
        "q": "SDG 14 focuses on:",
        "options": ["Life Below Water", "Zero Hunger", "Quality Education", "Climate Action"],
        "answer": 0
    },
    {
        "q": "A major threat to marine life is:",
        "options": ["Solar energy", "Plastic pollution", "Cloud computing", "Wind farms"],
        "answer": 1
    },
    {
        "q": "Overfishing causes:",
        "options": ["Increased biodiversity", "Stable ecosystems", "Population decline of species", "Cleaner oceans"],
        "answer": 2
    },
    {
        "q": "One personal action to help oceans is:",
        "options": ["Use more single-use plastic", "Join local clean-up drives", "Pour oil down drains", "Ignore waste rules"],
        "answer": 1
    },
    {
        "q": "Marine protected areas help by:",
        "options": ["Increasing pollution", "Supporting habitat recovery", "Banning all fishing worldwide", "Raising seawater temperature"],
        "answer": 1
    },
    {
        "q": "Ocean acidification is mainly driven by:",
        "options": ["CO2 absorption by oceans", "Plastic burning at sea", "Salt mining", "Ship noise"],
        "answer": 0
    },
    {
        "q": "Sustainable seafood means:",
        "options": ["Caught or farmed with minimal ecosystem impact", "Any seafood available in markets", "Only expensive fish", "Avoiding all seafood"],
        "answer": 0
    },
    {
        "q": "A good waste practice is:",
        "options": ["Mixing dry and wet waste", "Segregating and recycling", "Throwing e-waste in regular bins", "Dumping waste near rivers"],
        "answer": 1
    },
    {
        "q": "Plastic bags harm marine life because:",
        "options": ["They dissolve into nutrients", "Animals mistake them for food", "They increase oxygen levels", "They are edible"],
        "answer": 1
    },
    {
        "q": "Community impact improves when you:",
        "options": ["Work alone silently", "Collaborate with local groups", "Ignore local policies", "Post misinformation online"],
        "answer": 1
    },
]


class SDG14App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SDG 14: Save Life Below Water")
        self.root.geometry("950x650")
        self.root.minsize(900, 600)

        self._ensure_data_dir()
        self._build_ui()

    def run(self):
        self.root.mainloop()

    def _ensure_data_dir(self):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        if not os.path.exists(ACTIONS_FILE):
            with open(ACTIONS_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["date", "category", "description"])

    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook.Tab", padding=[15, 6])
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Body.TLabel", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 11))
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", rowheight=26)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        # Tabs
        frame_home = ttk.Frame(notebook)
        frame_learn = ttk.Frame(notebook)
        frame_actions = ttk.Frame(notebook)
        frame_quiz = ttk.Frame(notebook)
        frame_charts = ttk.Frame(notebook)

        notebook.add(frame_home, text="Home")
        notebook.add(frame_learn, text="Learn")
        notebook.add(frame_actions, text="Action tracker")
        notebook.add(frame_quiz, text="Quiz")
        notebook.add(frame_charts, text="Charts")

        self._build_home(frame_home)
        self._build_learn(frame_learn)
        self._build_actions(frame_actions)
        self._build_quiz(frame_quiz)
        self._build_charts(frame_charts)

    # --- Home ---
    def _build_home(self, parent):
        header = ttk.Label(parent, text="SDG 14: Life Below Water", style="Header.TLabel")
        header.pack(pady=(20, 10))

        text = (
            "Welcome! This app helps you learn about protecting oceans and freshwater ecosystems.\n"
            "Explore facts, take a quiz, track your personal actions, and see your progress.\n\n"
            "Small steps—like reducing plastic use and proper waste segregation—make a real difference."
        )
        lbl = ttk.Label(parent, text=text, style="Body.TLabel", justify="center")
        lbl.pack(pady=10)

        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Start learning", command=lambda: self._switch_tab(1)).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Track actions", command=lambda: self._switch_tab(2)).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Take the quiz", command=lambda: self._switch_tab(3)).grid(row=0, column=2, padx=10)

    def _switch_tab(self, index):
        notebook = self.root.children.get('!notebook')
        if notebook:
            notebook.select(index)

    # --- Learn ---
    def _build_learn(self, parent):
        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(container, text="Learn: Key facts and actions", style="Header.TLabel").pack(anchor="w", pady=(0, 10))

        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for title, body in SDG14_FACTS:
            card = ttk.Frame(scroll_frame, padding=12, relief="groove")
            card.pack(fill="x", expand=True, pady=8)
            ttk.Label(card, text=title, style="Header.TLabel").pack(anchor="w")
            ttk.Label(card, text=body, style="Body.TLabel", wraplength=800, justify="left").pack(anchor="w", pady=(6, 0))

        tip = (
            "Tip: Start small. Carry a reusable bottle and bag, say no to straws, and share what you learn with friends."
        )
        ttk.Label(scroll_frame, text=tip, style="Body.TLabel").pack(anchor="w", pady=8)

    # --- Action tracker ---
    def _build_actions(self, parent):
        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(container, text="Action tracker", style="Header.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10), columnspan=3)

        # Form
        ttk.Label(container, text="Date (YYYY-MM-DD):", style="Body.TLabel").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.date_var = tk.StringVar(value=datetime.date.today().isoformat())
        ttk.Entry(container, textvariable=self.date_var, width=18).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(container, text="Category:", style="Body.TLabel").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.category_var = tk.StringVar()
        categories = ["Plastic reduction", "Waste segregation", "Community clean-up", "Eco-friendly product", "Awareness sharing", "Sustainable seafood"]
        ttk.Combobox(container, textvariable=self.category_var, values=categories, width=25, state="readonly").grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(container, text="Description:", style="Body.TLabel").grid(row=3, column=0, sticky="ne", padx=5, pady=5)
        self.desc_text = tk.Text(container, width=50, height=4)
        self.desc_text.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(container, text="Add action", command=self.add_action).grid(row=4, column=1, sticky="w", padx=5, pady=10)
        ttk.Button(container, text="Export to CSV", command=self.export_actions).grid(row=4, column=2, sticky="w", padx=5, pady=10)

        # Table
        columns = ("date", "category", "description")
        self.tree = ttk.Treeview(container, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=200 if col != "description" else 400, anchor="w")
        self.tree.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=5, pady=10)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=5, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Grid config
        container.grid_columnconfigure(2, weight=1)
        container.grid_rowconfigure(5, weight=1)

        self.load_actions()

    def add_action(self):
        date = self.date_var.get().strip()
        category = self.category_var.get().strip()
        desc = self.desc_text.get("1.0", "end").strip()

        if not date or not category or not desc:
            messagebox.showwarning("Missing data", "Please fill date, category, and description.")
            return

        # validate date format
        try:
            datetime.date.fromisoformat(date)
        except ValueError:
            messagebox.showerror("Invalid date", "Please enter date in YYYY-MM-DD format.")
            return

        with open(ACTIONS_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([date, category, desc])

        self.tree.insert("", "end", values=(date, category, desc))
        self.desc_text.delete("1.0", "end")
        messagebox.showinfo("Added", "Action logged successfully!")

    def load_actions(self):
        # clear
        for item in self.tree.get_children():
            self.tree.delete(item)
        # load
        if os.path.exists(ACTIONS_FILE):
            with open(ACTIONS_FILE, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.tree.insert("", "end", values=(row["date"], row["category"], row["description"]))

    def export_actions(self):
        save_path = filedialog.asksaveasfilename(
            title="Export actions to CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not save_path:
            return

        # copy data
        with open(ACTIONS_FILE, "r", newline="", encoding="utf-8") as src, \
             open(save_path, "w", newline="", encoding="utf-8") as dst:
            dst.write(src.read())

        messagebox.showinfo("Exported", f"Actions exported to:\n{save_path}")

    # --- Quiz ---
    def _build_quiz(self, parent):
        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(container, text="Quiz: Test your knowledge", style="Header.TLabel").pack(anchor="w", pady=(0, 10))

        self.quiz_index = 0
        self.quiz_score = 0
        self.quiz_var = tk.IntVar(value=-1)

        self.quiz_q_label = ttk.Label(container, text="", style="Body.TLabel", wraplength=800, justify="left")
        self.quiz_q_label.pack(anchor="w", pady=(5, 10))

        self.quiz_option_buttons = []
        for i in range(4):
            rb = ttk.Radiobutton(container, text="", variable=self.quiz_var, value=i)
            rb.pack(anchor="w", pady=3)
            self.quiz_option_buttons.append(rb)

        self.quiz_feedback = ttk.Label(container, text="", style="Body.TLabel")
        self.quiz_feedback.pack(anchor="w", pady=10)

        btn_frame = ttk.Frame(container)
        btn_frame.pack(anchor="w", pady=10)
        ttk.Button(btn_frame, text="Submit", command=self.submit_quiz_answer).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Next", command=self.next_quiz_question).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Restart", command=self.restart_quiz).grid(row=0, column=2, padx=5)

        self.load_quiz_question()

    def load_quiz_question(self):
        qdata = QUIZ_QUESTIONS[self.quiz_index]
        self.quiz_q_label.config(text=f"Q{self.quiz_index + 1}. {qdata['q']}")
        self.quiz_var.set(-1)
        for i, opt in enumerate(qdata["options"]):
            self.quiz_option_buttons[i].config(text=opt)
        self.quiz_feedback.config(text="")

    def submit_quiz_answer(self):
        selected = self.quiz_var.get()
        if selected == -1:
            messagebox.showwarning("No answer", "Please select an option.")
            return

        correct = QUIZ_QUESTIONS[self.quiz_index]["answer"]
        if selected == correct:
            self.quiz_score += 1
            self.quiz_feedback.config(text="Correct! ✅")
        else:
            ans_text = QUIZ_QUESTIONS[self.quiz_index]["options"][correct]
            self.quiz_feedback.config(text=f"Not quite. The correct answer is: {ans_text}")

    def next_quiz_question(self):
        if self.quiz_index < len(QUIZ_QUESTIONS) - 1:
            self.quiz_index += 1
            self.load_quiz_question()
        else:
            self.finish_quiz()

    def restart_quiz(self):
        self.quiz_index = 0
        self.quiz_score = 0
        self.load_quiz_question()
        self.quiz_feedback.config(text="")

    def finish_quiz(self):
        total = len(QUIZ_QUESTIONS)
        percent = int((self.quiz_score / total) * 100)
        messagebox.showinfo("Quiz completed", f"You scored {self.quiz_score}/{total} ({percent}%).")
        if percent >= 70:
            self._show_certificate(percent)
        self.restart_quiz()

    def _show_certificate(self, percent):
        cert = tk.Toplevel(self.root)
        cert.title("Certificate")
        cert.geometry("500x300")
        ttk.Label(cert, text="Certificate of Awareness", style="Header.TLabel").pack(pady=10)
        msg = (
            f"This certifies that you completed the SDG 14 awareness quiz\n"
            f"with a score of {percent}%.\n\n"
            "Keep taking action to protect life below water!"
        )
        ttk.Label(cert, text=msg, style="Body.TLabel", justify="center").pack(pady=10)
        ttk.Button(cert, text="Close", command=cert.destroy).pack(pady=10)

    # --- Charts ---
    def _build_charts(self, parent):
        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(container, text="Charts: Your impact over time", style="Header.TLabel").pack(anchor="w", pady=(0, 10))

        if not HAS_MPL:
            ttk.Label(container, text="Matplotlib not installed. Install it to see charts (pip install matplotlib).", style="Body.TLabel").pack(anchor="w", pady=10)
            return

        # Controls
        ctrl = ttk.Frame(container)
        ctrl.pack(anchor="w", pady=10)
        ttk.Button(ctrl, text="Refresh charts", command=lambda: self.render_charts(container)).grid(row=0, column=0, padx=5)

        self.render_charts(container)

    def render_charts(self, container):
        # Remove old canvases
        for child in container.winfo_children():
            if isinstance(child, tk.Canvas):
                child.destroy()

        actions = self._read_actions()
        if not actions:
            ttk.Label(container, text="No actions yet. Add actions to see charts.", style="Body.TLabel").pack(anchor="w", pady=10)
            return

        # Aggregate: actions per category
        per_cat = {}
        for a in actions:
            per_cat[a["category"]] = per_cat.get(a["category"], 0) + 1

        # Aggregate: actions per week (ISO week)
        per_week = {}
        for a in actions:
            dt = datetime.date.fromisoformat(a["date"])
            year_week = f"{dt.isocalendar().year}-W{dt.isocalendar().week}"
            per_week[year_week] = per_week.get(year_week, 0) + 1

        fig = Figure(figsize=(8, 4), dpi=100)
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        # Bar chart by category
        cats = list(per_cat.keys())
        counts = [per_cat[c] for c in cats]
        ax1.bar(cats, counts, color="#2a9d8f")
        ax1.set_title("Actions by category")
        ax1.set_xticklabels(cats, rotation=30, ha="right")
        ax1.set_ylabel("Count")

        # Line chart per week
        weeks = sorted(per_week.keys())
        week_counts = [per_week[w] for w in weeks]
        ax2.plot(weeks, week_counts, marker="o", color="#264653")
        ax2.set_title("Actions per week")
        ax2.set_xticklabels(weeks, rotation=30, ha="right")
        ax2.set_ylabel("Count")

        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)

    def _read_actions(self):
        if not os.path.exists(ACTIONS_FILE):
            return []
        rows = []
        with open(ACTIONS_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        return rows


if __name__ == "__main__":
    # Allow launching gui.py directly for development
    SDG14App().run()
