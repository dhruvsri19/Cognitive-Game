import tkinter as tk
from tkinter import messagebox
import random
import time
import os

# ---------------- SCORE SYSTEM ----------------
def save_score(game, score):
    with open("brain_scores.txt", "a") as f:
        f.write(f"{game},{score},{time.strftime('%Y-%m-%d')}\n")

def show_history():
    if not os.path.exists("brain_scores.txt"):
        messagebox.showinfo("Progress", "No history yet!")
        return
    
    with open("brain_scores.txt", "r") as f:
        data = f.readlines()[-10:]
    
    history = "\n".join(
        f"{g} • {s} pts • {d}"
        for g, s, d in (line.strip().split(",") for line in data)
    )
    
    messagebox.showinfo("Your Progress", history)

# ---------------- MAIN APP ----------------
class BrainTrainerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GAMES")
        self.root.geometry("430x520")
        self.root.configure(bg="#0f172a")  # deep navy
        self.show_menu()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ---------------- MENU ----------------
    def show_menu(self):
        self.clear()

        tk.Label(
            self.root,
            text="🎮 GAMES 🎮",
            font=("Arial Black", 26),
            bg="#0f172a",
            fg="#38bdf8"
        ).pack(pady=15)

        tk.Label(
            self.root,
            text="Train • React • Type • Improve",
            font=("Arial", 11, "italic"),
            bg="#0f172a",
            fg="#94a3b8"
        ).pack(pady=5)

        self.menu_button("🧠 Memory Challenge", self.memory_game, "#22c55e")
        self.menu_button("⚡ Reaction Speed", self.reaction_game, "#f97316")
        self.menu_button("⌨ Typing Challenge", self.typing_game, "#a855f7")
        self.menu_button("📊 Progress", show_history, "#38bdf8")
        self.menu_button("❌ Exit", self.root.quit, "#64748b")

    def menu_button(self, text, cmd, color):
        tk.Button(
            self.root,
            text=text,
            font=("Arial", 14, "bold"),
            width=24,
            bg=color,
            fg="white",
            activebackground="#020617",
            relief="flat",
            command=cmd
        ).pack(pady=7)

    # ---------------- MEMORY GAME ----------------
    def memory_game(self):
        self.clear()
        self.level = 3
        self.round = 0
        self.score = 0
        
        self.label = tk.Label(
            self.root,
            font=("Arial Black", 20),
            bg="#0f172a",
            fg="#facc15"
        )
        self.label.pack(pady=40)

        self.entry = tk.Entry(
            self.root,
            font=("Arial", 14),
            justify="center"
        )
        self.entry.pack()

        tk.Button(
            self.root, text="Submit",
            font=("Arial", 12, "bold"),
            bg="#22c55e", fg="white",
            command=self.check_memory
        ).pack(pady=10)

        tk.Button(
            self.root, text="⬅ Back",
            bg="#334155", fg="white",
            command=self.show_menu
        ).pack()

        self.next_memory_round()

    def next_memory_round(self):
        if self.round == 5:
            save_score("Memory", self.score)
            messagebox.showinfo("Game Over", f"Score: {self.score}")
            self.show_menu()
            return
        
        self.nums = [random.randint(0, 9) for _ in range(self.level)]
        self.label.config(text=" ".join(map(str, self.nums)))
        self.entry.delete(0, tk.END)
        self.entry.config(state="disabled")

        self.root.after(2000, self.hide_memory)

    def hide_memory(self):
        self.label.config(text="Type the numbers")
        self.entry.config(state="normal")

    def check_memory(self):
        try:
            user = list(map(int, self.entry.get().split()))
        except:
            return
        
        if user == self.nums:
            self.score += 10
            self.level += 1
            self.round += 1
            self.next_memory_round()
        else:
            save_score("Memory", self.score)
            messagebox.showinfo("Wrong", f"Correct: {self.nums}")
            self.show_menu()

    # ---------------- REACTION GAME ----------------
    def reaction_game(self):
        self.clear()
        self.total = 0
        self.attempt = 0

        self.btn = tk.Button(
            self.root,
            text="WAIT...",
            font=("Arial Black", 18),
            width=15,
            height=3,
            bg="#ef4444",
            fg="white",
            state="disabled"
        )
        self.btn.pack(pady=90)

        self.start_reaction_round()

    def start_reaction_round(self):
        if self.attempt == 5:
            avg = self.total / 5
            score = max(0, int(100 - avg * 50))
            save_score("Reaction", score)
            messagebox.showinfo(
                "Result",
                f"Average: {avg:.3f}s\nScore: {score}"
            )
            self.show_menu()
            return

        self.root.after(random.randint(1000, 3000), self.show_go)

    def show_go(self):
        self.start_time = time.time()
        self.btn.config(
            text="CLICK!",
            bg="#22c55e",
            state="normal",
            command=self.reaction_click
        )

    def reaction_click(self):
        self.total += time.time() - self.start_time
        self.attempt += 1
        self.btn.config(
            text="WAIT...",
            bg="#ef4444",
            state="disabled"
        )
        self.start_reaction_round()

    # ---------------- TYPING GAME ----------------
    def typing_game(self):
        self.clear()
        self.points = 0
        self.round = 0

        self.target = tk.Label(
            self.root,
            font=("Courier New", 18, "bold"),
            bg="#0f172a",
            fg="#38bdf8"
        )
        self.target.pack(pady=25)

        self.entry = tk.Entry(
            self.root,
            font=("Courier New", 14),
            justify="center"
        )
        self.entry.pack()

        tk.Button(
            self.root,
            text="Submit",
            font=("Arial", 12, "bold"),
            bg="#a855f7", fg="white",
            command=self.check_typing
        ).pack(pady=10)

        self.next_typing()

    def next_typing(self):
        if self.round == 5:
            save_score("Typing", self.points)
            messagebox.showinfo("Game Over", f"Score: {self.points}")
            self.show_menu()
            return

        self.word = "".join(
            random.choice("abcdefghijklmnopqrstuvwxyz")
            for _ in range(random.randint(6, 12))
        )
        self.target.config(text=self.word)
        self.entry.delete(0, tk.END)
        self.start = time.time()

    def check_typing(self):
        elapsed = time.time() - self.start
        if self.entry.get() == self.word:
            bonus = max(0, 20 - int(elapsed * 2))
            self.points += 15 + bonus
        self.round += 1
        self.next_typing()

# ---------------- RUN ----------------
root = tk.Tk()
BrainTrainerGUI(root)
root.mainloop()