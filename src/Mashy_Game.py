# jeopardy_game.py
import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "jeopardy_data.json")

class JeopardyGame(tk.Tk):
    def __init__(self, categories, grid):
        super().__init__()
        self.title("Jeopardy Game")
        self.geometry("1280x600")
        self.categories = categories
        self.grid_data = grid
        self.buttons = {}
        self.create_board()
        self.score = 0
        self.score_label = tk.Label(self, text=f"Score: ${self.score}", font=("Helvetica", 14), fg="blue")
        self.score_label.grid(row=6, column=0, columnspan=len(self.categories), pady=10)

    def create_board(self):
        for col, category in enumerate(self.categories):
            label = tk.Label(self, text=category, font=("Helvetica", 14, "bold"), borderwidth=2, relief="ridge", width=20, height=2)
            label.grid(row=0, column=col)

        for row in range(5):
            for col in range(len(self.categories)):
                btn = tk.Button(self, text=f"${(row+1)*100}", width=20, height=4,
                                command=lambda r=row, c=col: self.ask_question(r, c))
                btn.grid(row=row+1, column=col, padx=2, pady=2)
                self.buttons[(row, col)] = btn

    def ask_question(self, row, col):
        data = self.grid_data[row][col]
        if not data:
            messagebox.showinfo("No Data", "No question loaded for this cell.")
            return

        self.buttons[(row, col)].config(state="disabled")

        answer = simpledialog.askstring("Question", data["question"])
        question_value = (row + 1) * 100  # $100 to $500

        if not answer or answer.strip() == "":
            msg = f"You did not provide an answer.\n\nThe correct answer was:\n{data['answer']}\n\n+ $0"
        else:
            user_answer = answer.strip().lower()
            correct_answers = data["answer"]

            # Normalize all correct answers
            if isinstance(correct_answers, list):
                correct_answers_normalized = [ans.strip().lower() for ans in correct_answers]
            else:
                correct_answers_normalized = [correct_answers.strip().lower()]

            if user_answer in correct_answers_normalized:
                self.score += question_value
                self.score_label.config(text=f"Score: ${self.score}")
                msg = f"Correct!\n\nYou earned ${question_value}."
            else:
                msg = f"Incorrect.\nYour answer: {answer}\nCorrect answer: {data['answer']}\n\n+ $0"

        messagebox.showinfo("Result", msg)


if __name__ == "__main__":
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            categories = data["categories"]
            grid = data["grid"]
            app = JeopardyGame(categories, grid)
            app.mainloop()
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not load Jeopardy board data:\n{e}")

