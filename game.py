import tkinter as tk
from tkinter import messagebox, ttk
import random

# Words for different levels
levels = {
    1: ["CAT", "DOG", "SUN", "BAT", "HAT"],
    2: ["APPLE", "HOUSE", "RIVER", "MUSIC", "SMILE"],
    3: ["PYTHON", "ORANGE", "FLOWER", "GARDEN", "MARKET"],
    4: ["ELEPHANT", "COMPUTER", "NOTEBOOK", "MOUNTAIN"],
    5: ["KNOWLEDGE", "ADVENTURE", "CHALLENGE", "EDUCATION"],
    6: ["PHENOMENON", "EXTRAVAGANT", "INTELLIGENCE", "MAGNIFICENT"],
    7: ["CONSCIENTIOUS", "ENTHUSIASTIC", "COMMUNICATION"],
    8: ["METAMORPHOSIS", "MISINTERPRETATION", "EXCEPTIONALITY"],
    9: ["INCOMPREHENSIBLE", "INTERNATIONALIZATION"],
    10: ["PSEUDOPSEUDOHYPOPARATHYROIDISM"]
}

class WordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Master Challenge")
        self.root.geometry("760x560")
        self.root.configure(bg="#FFD166")
        self.root.resizable(False, False)

        self.max_level = 10
        self.time_limit = 18
        self.level = 1
        self.score = 0
        self.streak = 0
        self.hints_left = 3
        self.timer_id = None

        header = tk.Label(
            root,
            text="WORD MASTER CHALLENGE",
            font=("Comic Sans MS", 28, "bold"),
            bg="#FFD166",
            fg="#EF476F"
        )
        header.pack(pady=(15, 5))

        subtitle = tk.Label(
            root,
            text="Crack the scramble, keep your streak, and climb every level!",
            font=("Arial", 12, "italic"),
            bg="#FFD166",
            fg="#073B4C"
        )
        subtitle.pack(pady=(0, 15))

        status_frame = tk.Frame(root, bg="#FFD166")
        status_frame.pack(pady=5)

        self.level_label = tk.Label(
            status_frame,
            text=f"Level: {self.level}",
            font=("Arial", 16, "bold"),
            bg="#FFD166",
            fg="#073B4C",
            width=12
        )
        self.level_label.grid(row=0, column=0, padx=10)

        self.score_label = tk.Label(
            status_frame,
            text=f"Score: {self.score}",
            font=("Arial", 16, "bold"),
            bg="#FFD166",
            fg="#073B4C",
            width=12
        )
        self.score_label.grid(row=0, column=1, padx=10)

        self.streak_label = tk.Label(
            status_frame,
            text=f"Streak: {self.streak}",
            font=("Arial", 16, "bold"),
            bg="#FFD166",
            fg="#073B4C",
            width=12
        )
        self.streak_label.grid(row=0, column=2, padx=10)

        self.timer_label = tk.Label(
            status_frame,
            text=f"Time: {self.time_limit}s",
            font=("Arial", 16, "bold"),
            bg="#FFD166",
            fg="#EF476F",
            width=12
        )
        self.timer_label.grid(row=0, column=3, padx=10)

        self.progress = ttk.Progressbar(
            root,
            length=720,
            maximum=self.max_level,
            value=self.level - 1,
            mode="determinate"
        )
        self.progress.pack(pady=(10, 20))

        self.word_label = tk.Label(
            root,
            text="",
            font=("Arial", 34, "bold"),
            bg="#073B4C",
            fg="#F9F7F7",
            width=18,
            padx=15,
            pady=20,
            relief="ridge",
            bd=6
        )
        self.word_label.pack(pady=10)

        self.entry = tk.Entry(
            root,
            font=("Arial", 20),
            justify="center",
            width=20,
            bd=4,
            relief="solid"
        )
        self.entry.pack(pady=10)
        self.entry.focus()
        self.root.bind("<Return>", lambda event: self.check_answer())

        button_frame = tk.Frame(root, bg="#FFD166")
        button_frame.pack(pady=10)

        submit_btn = tk.Button(
            button_frame,
            text="Submit",
            font=("Arial", 14, "bold"),
            bg="#06D6A0",
            fg="#073B4C",
            width=12,
            activebackground="#05c596",
            command=self.check_answer
        )
        submit_btn.grid(row=0, column=0, padx=8, pady=5)

        skip_btn = tk.Button(
            button_frame,
            text="Skip",
            font=("Arial", 14, "bold"),
            bg="#FFD166",
            fg="#073B4C",
            width=12,
            activebackground="#f4c42b",
            command=self.skip_word
        )
        skip_btn.grid(row=0, column=1, padx=8, pady=5)

        self.hint_btn = tk.Button(
            button_frame,
            text=f"Hint ({self.hints_left})",
            font=("Arial", 14, "bold"),
            bg="#118AB2",
            fg="white",
            width=12,
            activebackground="#0d6d94",
            command=self.show_hint
        )
        self.hint_btn.grid(row=0, column=2, padx=8, pady=5)

        self.feedback_label = tk.Label(
            root,
            text="Solve the scramble before time runs out!",
            font=("Arial", 14, "italic"),
            bg="#FFD166",
            fg="#073B4C"
        )
        self.feedback_label.pack(pady=15)

        self.generate_word()

    def scramble(self, word):
        word = list(word)
        random.shuffle(word)
        return ''.join(word)

    def generate_word(self):
        self.current_word = random.choice(levels[self.level])
        scrambled = self.scramble(self.current_word)

        while scrambled == self.current_word:
            scrambled = self.scramble(self.current_word)

        self.word_label.config(text=scrambled)
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.reset_timer()

    def reset_timer(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)

        self.remaining_time = self.time_limit
        self.timer_label.config(text=f"Time: {self.remaining_time}s")
        self.timer_id = self.root.after(1000, self.update_timer)

    def update_timer(self):
        self.remaining_time -= 1
        self.timer_label.config(text=f"Time: {self.remaining_time}s")

        if self.remaining_time <= 0:
            self.out_of_time()
        else:
            self.timer_id = self.root.after(1000, self.update_timer)

    def out_of_time(self):
        self.streak = 0
        self.score = max(0, self.score - 5)
        self.feedback_label.config(
            text="Time's up! New scramble unlocked...",
            fg="#EF476F"
        )
        self.update_status()
        self.generate_word()

    def show_hint(self):
        if self.hints_left <= 0:
            self.feedback_label.config(
                text="No hints left — sharpen your focus!",
                fg="#EF476F"
            )
            return

        self.hints_left -= 1
        self.hint_btn.config(text=f"Hint ({self.hints_left})")
        hint_text = f"This word starts with '{self.current_word[0]}' and has {len(self.current_word)} letters."
        messagebox.showinfo("Hint", hint_text)
        self.feedback_label.config(
            text="Hint used — keep going!",
            fg="#073B4C"
        )

    def check_answer(self):
        answer = self.entry.get().upper().strip()

        if not answer:
            self.feedback_label.config(
                text="Type your answer and press Submit.",
                fg="#073B4C"
            )
            return

        if answer == self.current_word:
            self.score += 10 + self.streak * 2
            self.streak += 1
            self.feedback_label.config(
                text=f"Nice! Streak x{self.streak} — level up!",
                fg="#06D6A0"
            )

            if self.level < self.max_level:
                self.level += 1
            else:
                messagebox.showinfo(
                    "Champion!",
                    f"You conquered all levels!\nFinal Score: {self.score}"
                )
                self.root.quit()
                return

            self.update_status()
            self.generate_word()
        else:
            self.score = max(0, self.score - 2)
            self.streak = 0
            self.feedback_label.config(
                text="Oops! That was not it — try again.",
                fg="#EF476F"
            )
            self.update_status()
            self.entry.delete(0, tk.END)

    def skip_word(self):
        if messagebox.askyesno(
            "Skip Word",
            "Skip this scrambled word for a 5-point penalty?"
        ):
            self.score = max(0, self.score - 5)
            self.streak = 0
            self.feedback_label.config(
                text="Skipped! New scramble on the way...",
                fg="#073B4C"
            )
            self.update_status()
            self.generate_word()

    def update_status(self):
        self.level_label.config(text=f"Level: {self.level}")
        self.score_label.config(text=f"Score: {self.score}")
        self.streak_label.config(text=f"Streak: {self.streak}")
        self.progress['value'] = self.level - 1

root = tk.Tk()
game = WordGame(root)
root.mainloop()
