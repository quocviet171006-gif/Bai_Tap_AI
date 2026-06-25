# Tắt sinh file bytecode để tránh tạo thư mục __pycache__
import sys
sys.dont_write_bytecode = True

import tkinter as tk
from gui.Vacuum_GUI import Vacuum_GUI

# Khởi chạy ứng dụng giao diện đồ họa
if __name__ == "__main__":
    root = tk.Tk()
    app = Vacuum_GUI(root)
    root.mainloop()