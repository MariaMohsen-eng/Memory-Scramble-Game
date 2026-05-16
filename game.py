import random
import tkinter as tk
from tkinter import messagebox, simpledialog

class MemoryGame:
    def __init__(self, root, rows, cols, timeout):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.timeout = timeout
        self.cards = []
        self.buttons = []
        self.first_selected = None
        self.matched = []
        self.time_left = timeout
        self.game_running = True
        self.waiting = False
        
        total_cards = rows * cols
        if total_cards % 2 != 0:
            raise ValueError("Board size must be even")
        
        symbols = list(range(total_cards // 2)) * 2
        random.shuffle(symbols)
        
        self.cards = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(symbols[i * cols + j])
            self.cards.append(row)
        
        self.matched = [[False] * cols for _ in range(rows)]
        
        self.create_board()
        self.update_timer()
    
    def create_board(self):
        for i in range(self.rows):
            row_buttons = []
            for j in range(self.cols):
                btn = tk.Button(
                    self.root, 
                    text="?", 
                    width=8, 
                    height=3,
                    font=("Arial", 14),
                    command=lambda r=i, c=j: self.on_card_click(r, c)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        
        self.timer_label = tk.Label(
            self.root, 
            text=f"⏱️ Time left: {self.time_left}s", 
            font=("Arial", 16, "bold")
        )
        self.timer_label.grid(row=self.rows, column=0, columnspan=self.cols, pady=10)
    
    def update_timer(self):
        if not self.game_running:
            return
        
        if self.time_left <= 0:
            self.game_running = False
            messagebox.showinfo("Game Over", "⏰ Time's up! You lost 😢")
            self.root.quit()
        elif all(all(row) for row in self.matched):
            self.game_running = False
            messagebox.showinfo("Congratulations!", "🎉 You won! 🎉")
            self.root.quit()
        else:
            self.timer_label.config(text=f"⏱️ Time left: {self.time_left}s")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
    
    def on_card_click(self, r, c):
        if not self.game_running or self.matched[r][c] or self.waiting:
            return
        
        if self.first_selected is None:
            self.first_selected = (r, c)
            self.buttons[r][c].config(text=str(self.cards[r][c]), bg="lightyellow")
        else:
            r1, c1 = self.first_selected
            
            if (r1, c1) == (r, c):
                return
            
            self.buttons[r][c].config(text=str(self.cards[r][c]), bg="lightyellow")
            self.root.update()
            
            self.waiting = True
            
            if self.cards[r1][c1] == self.cards[r][c]:
                self.matched[r1][c1] = True
                self.matched[r][c] = True
                self.buttons[r1][c1].config(state="disabled", bg="lightgreen")
                self.buttons[r][c].config(state="disabled", bg="lightgreen")
                self.first_selected = None
                self.waiting = False
            else:
                self.root.after(1000, self.reset_cards, r1, c1, r, c)
            
            if all(all(row) for row in self.matched):
                self.game_running = False
                messagebox.showinfo("Congratulations!", "🎉 You won! 🎉")
                self.root.quit()
    
    def reset_cards(self, r1, c1, r2, c2):
        if not self.matched[r1][c1]:
            self.buttons[r1][c1].config(text="?", bg="SystemButtonFace")
        if not self.matched[r2][c2]:
            self.buttons[r2][c2].config(text="?", bg="SystemButtonFace")
        self.first_selected = None
        self.waiting = False


def get_player_config():
    root = tk.Tk()
    root.withdraw()
    
    while True:
        rows = simpledialog.askinteger("Configuration", "Enter number of rows (even number):")
        cols = simpledialog.askinteger("Configuration", "Enter number of columns (even number):")
        timeout = simpledialog.askinteger("Configuration", "Enter timeout in seconds:")
        
        if rows and cols and timeout:
            if (rows * cols) % 2 == 0:
                break
            else:
                messagebox.showerror("Error", "Total cards must be even! Try again.")
        else:
            messagebox.showerror("Error", "Invalid input! Try again.")
    
    root.destroy()
    return rows, cols, timeout


if __name__ == "__main__":
    print("🎮 Welcome to Memory Scramble Game!")
    rows, cols, timeout = get_player_config()
    root = tk.Tk()
    root.title("🧠 Memory Scramble Game")
    game = MemoryGame(root, rows, cols, timeout)
    root.mainloop()