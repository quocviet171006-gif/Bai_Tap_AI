import tkinter as tk
from tkinter import messagebox
import math
import time
from Adversarial_Search import AIPlayer

class CaroUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe AI - Pro UI")
        self.ai = AIPlayer()
        self.board = [' ' for _ in range(9)]
        self.game_over = False
        
        # Cấu hình lưới để các thành phần nằm ngay ngắn
        self.root.columnconfigure(1, weight=1)
        
        # 1. Panel Điều khiển (Trái)
        ctrl_frame = tk.LabelFrame(root, text="Cấu hình", padx=10, pady=10)
        ctrl_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        
        tk.Label(ctrl_frame, text="Thuật toán:").pack(anchor="w")
        self.algo_var = tk.StringVar(value="Minimax")
        for m in ["Minimax", "Alpha-Beta", "Expectimax"]:
            tk.Radiobutton(ctrl_frame, text=m, variable=self.algo_var, value=m).pack(anchor="w")
        
        tk.Label(ctrl_frame, text="\nChế độ:").pack(anchor="w")
        self.mode_var = tk.StringVar(value="Người vs AI")
        tk.Radiobutton(ctrl_frame, text="Người vs AI", variable=self.mode_var, value="Người vs AI").pack(anchor="w")
        tk.Radiobutton(ctrl_frame, text="AI vs AI", variable=self.mode_var, value="AI vs AI").pack(anchor="w")
        
        tk.Button(ctrl_frame, text="Bắt đầu", command=self.start_game, width=15, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(ctrl_frame, text="Chơi lại", command=self.reset_board, width=15).pack()

        # 2. Panel Bàn cờ (Giữa)
        board_frame = tk.Frame(root)
        board_frame.grid(row=0, column=1, padx=10, pady=10)
        self.buttons = []
        for i in range(9):
            btn = tk.Button(board_frame, text=" ", width=5, height=2, font=('Arial', 24, 'bold'),
                            command=lambda i=i: self.on_click(i))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(btn)
        
        # 3. Panel Log (Phải)
        log_frame = tk.LabelFrame(root, text="Nhật ký trận đấu", padx=5, pady=5)
        log_frame.grid(row=0, column=2, sticky="ns", padx=10, pady=10)
        self.log = tk.Text(log_frame, width=22, height=12, font=('Consolas', 10))
        self.log.pack()

    def check_game_over(self):
        if self.ai.check_winner(self.board, 'X'):
            messagebox.showinfo("Kết quả", "Bạn (X) đã thắng!")
            self.game_over = True
        elif self.ai.check_winner(self.board, 'O'):
            messagebox.showinfo("Kết quả", "AI (O) đã thắng!")
            self.game_over = True
        elif self.ai.is_full(self.board):
            messagebox.showinfo("Kết quả", "Hòa cờ!")
            self.game_over = True
        return self.game_over

    def on_click(self, i):
        if self.game_over or self.board[i] != ' ': return
        if self.mode_var.get() == "Người vs AI":
            # Ghi lại nước đi của người chơi vào board
            self.board[i] = 'X'
            self.buttons[i].config(text="X", fg="red")
            
            # --- THÊM DÒNG NÀY ĐỂ HIỂN THỊ VÀO LOG ---
            self.log.insert(tk.END, f"Người (X): vị trí {i}\n")
            self.log.see(tk.END)
            # ----------------------------------------
            
            if not self.check_game_over():
                self.ai_turn('O')
                self.check_game_over()

    def ai_turn(self, player):
        algo = self.algo_var.get()
        best_move = -1
        best_val = -math.inf if player == 'O' else math.inf
        
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = player
                if algo == "Minimax": val = self.ai.min_value(self.board) if player == 'O' else self.ai.max_value(self.board)
                elif algo == "Alpha-Beta": val = self.ai.ab_min(self.board, -math.inf, math.inf) if player == 'O' else self.ai.ab_max(self.board, -math.inf, math.inf)
                else: val = self.ai.ex_max(self.board)
                self.board[i] = ' '
                if (player == 'O' and val > best_val) or (player == 'X' and val < best_val):
                    best_val = val; best_move = i
        
        if best_move != -1:
            self.board[best_move] = player
            self.buttons[best_move].config(text=player, fg="blue" if player == "O" else "red")
            self.log.insert(tk.END, f"Lượt {player}: vị trí {best_move}\n")
            self.log.see(tk.END) # Tự động cuộn xuống dưới

    def start_game(self):
        self.reset_board()
        if self.mode_var.get() == "AI vs AI":
            while not self.game_over:
                self.ai_turn('X'); self.root.update(); time.sleep(0.5)
                if not self.check_game_over():
                    self.ai_turn('O'); self.root.update(); time.sleep(0.5)
                    self.check_game_over()

    def reset_board(self):
        self.board = [' ' for _ in range(9)]
        self.game_over = False
        for b in self.buttons: b.config(text=" ")
        self.log.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CaroUI(root)
    root.mainloop()