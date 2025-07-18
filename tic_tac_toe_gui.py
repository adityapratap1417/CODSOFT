import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title('Tic-Tac-Toe AI')
        self.board = ['' for _ in range(9)]
        self.buttons = []
        self.player_symbol = 'X'
        self.ai_symbol = 'O'
        self.current_player = None
        self.create_widgets()
        self.ask_player_options()

    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text='Tic-Tac-Toe AI', font=('Arial', 28, 'bold'), pady=10)
        title.pack()
        # Instructions
        self.instr = tk.Label(self.root, text='', font=('Arial', 14))
        self.instr.pack()
        # Board Frame with border
        self.board_frame = tk.Frame(self.root, bg='#222', bd=6, relief=tk.RIDGE)
        self.board_frame.pack(pady=10)
        for i in range(9):
            btn = tk.Button(self.board_frame, text='', font=('Arial', 40, 'bold'), width=4, height=2,
                            bg='#fff', fg='#222',
                            command=lambda i=i: self.on_click(i))
            btn.grid(row=i//3, column=i%3, padx=3, pady=3)
            self.buttons.append(btn)
        # Reset Button
        reset_btn = tk.Button(self.root, text='Reset Game', font=('Arial', 14, 'bold'), bg='#4CAF50', fg='white', command=self.reset_game)
        reset_btn.pack(pady=10)

    def ask_player_options(self):
        # Choose symbol
        symbol = simpledialog.askstring('Choose Symbol', 'Do you want to be X or O? (X goes first)', parent=self.root)
        if symbol and symbol.upper() == 'O':
            self.player_symbol = 'O'
            self.ai_symbol = 'X'
        else:
            self.player_symbol = 'X'
            self.ai_symbol = 'O'
        # Who goes first
        first = messagebox.askyesno('First Move', f'Do you want to go first as {self.player_symbol}?')
        self.current_player = self.player_symbol if first else self.ai_symbol
        self.instr.config(text=f'You are {self.player_symbol}. Click a square to make your move.')
        self.reset_game(init=True)

    def on_click(self, idx):
        if self.board[idx] == '' and self.current_player == self.player_symbol:
            self.make_move(idx, self.player_symbol)
            if not self.check_game_over():
                self.current_player = self.ai_symbol
                self.root.after(400, self.ai_move)

    def make_move(self, idx, symbol):
        self.board[idx] = symbol
        color = '#1976D2' if symbol == 'X' else '#D32F2F'
        self.buttons[idx].config(text=symbol, fg=color, state=tk.DISABLED, bg='#e3e3e3')

    def ai_move(self):
        idx = self.best_move()
        if idx is not None:
            self.make_move(idx, self.ai_symbol)
        if not self.check_game_over():
            self.current_player = self.player_symbol

    def best_move(self):
        best_score = -float('inf')
        move = None
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = self.ai_symbol
                score = self.minimax(0, False, -float('inf'), float('inf'))
                self.board[i] = ''
                if score > best_score:
                    best_score = score
                    move = i
        return move

    def minimax(self, depth, is_max, alpha, beta):
        winner = self.check_winner()
        if winner == self.ai_symbol:
            return 10 - depth
        elif winner == self.player_symbol:
            return depth - 10
        elif '' not in self.board:
            return 0
        if is_max:
            max_eval = -float('inf')
            for i in range(9):
                if self.board[i] == '':
                    self.board[i] = self.ai_symbol
                    eval = self.minimax(depth+1, False, alpha, beta)
                    self.board[i] = ''
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(9):
                if self.board[i] == '':
                    self.board[i] = self.player_symbol
                    eval = self.minimax(depth+1, True, alpha, beta)
                    self.board[i] = ''
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def check_winner(self):
        wins = [
            [0,1,2],[3,4,5],[6,7,8], # rows
            [0,3,6],[1,4,7],[2,5,8], # cols
            [0,4,8],[2,4,6]          # diags
        ]
        for a,b,c in wins:
            if self.board[a] == self.board[b] == self.board[c] != '':
                return self.board[a]
        return None

    def check_game_over(self):
        winner = self.check_winner()
        if winner:
            for i in range(9):
                if self.board[i] == winner:
                    self.buttons[i].config(bg='#FFD600')
            msg = 'You win!' if winner == self.player_symbol else 'AI wins!'
            messagebox.showinfo('Game Over', msg)
            self.disable_all()
            return True
        elif '' not in self.board:
            messagebox.showinfo('Game Over', 'It\'s a draw!')
            self.disable_all()
            return True
        return False

    def disable_all(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

    def reset_game(self, init=False):
        self.board = ['' for _ in range(9)]
        for btn in self.buttons:
            btn.config(text='', state=tk.NORMAL, bg='#fff', fg='#222')
        if not init:
            # Ask who goes first again
            first = messagebox.askyesno('First Move', f'Do you want to go first as {self.player_symbol}?')
            self.current_player = self.player_symbol if first else self.ai_symbol
        if self.current_player == self.ai_symbol:
            self.root.after(400, self.ai_move)

if __name__ == '__main__':
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop() 