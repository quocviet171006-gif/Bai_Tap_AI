import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
import sys

from utils import find_robot, copy_state

def gui_logger(node, frontier, reached):
    if hasattr(sys, 'app_gui') and sys.app_gui:
        sys.app_gui.log_algorithm_step(node, frontier, reached)

try:
    import Vacuum_Cleaner_BFS_1
    bfs1 = Vacuum_Cleaner_BFS_1.breadth_first_search
    Vacuum_Cleaner_BFS_1.GUI_LOGGER = gui_logger
except ImportError:
    bfs1 = None

try:
    import Vacuum_Cleaner_BFS_2
    bfs2 = Vacuum_Cleaner_BFS_2.breadth_first_search
    Vacuum_Cleaner_BFS_2.GUI_LOGGER = gui_logger
except ImportError:
    bfs2 = None

try:
    import Vacuum_Cleaner_DFS_1
    dfs1 = Vacuum_Cleaner_DFS_1.depth_first_search
    Vacuum_Cleaner_DFS_1.GUI_LOGGER = gui_logger
except ImportError:
    dfs1 = None

try:
    import Vacuum_Cleaner_DFS_2
    dfs2 = Vacuum_Cleaner_DFS_2.depth_first_search
    Vacuum_Cleaner_DFS_2.GUI_LOGGER = gui_logger
except ImportError:
    dfs2 = None

try:
    import Vacuum_Cleaner_IDS_1
    ids1 = Vacuum_Cleaner_IDS_1.iterative_deepening_search
    Vacuum_Cleaner_IDS_1.GUI_LOGGER = gui_logger
except ImportError:
    ids1 = None

try:
    import Vacuum_Cleaner_IDS_2
    ids2 = Vacuum_Cleaner_IDS_2.iterative_deepening_search
    Vacuum_Cleaner_IDS_2.GUI_LOGGER = gui_logger
except ImportError:
    ids2 = None

try:
    import Vacuum_Cleaner_UCS
    ucs = Vacuum_Cleaner_UCS.uniform_cost_search
    Vacuum_Cleaner_UCS.GUI_LOGGER = gui_logger
except ImportError:
    ucs = None

try:
    import Vacuum_Cleaner_Greedy_Search
    greedy = Vacuum_Cleaner_Greedy_Search.greedy_search
    Vacuum_Cleaner_Greedy_Search.GUI_LOGGER = gui_logger
except ImportError:
    greedy = None

try:
    import Vacuum_Cleaner_AStar
    astar = Vacuum_Cleaner_AStar.a_star_search
    Vacuum_Cleaner_AStar.GUI_LOGGER = gui_logger
except ImportError:
    astar = None

try:
    import Vacuum_Cleaner_IDAStar
    idastar = Vacuum_Cleaner_IDAStar.ida_star_search
    Vacuum_Cleaner_IDAStar.GUI_LOGGER = gui_logger
except ImportError:
    idastar = None

try:
    import Vacuum_Cleaner_Simple_Hill_Climbing
    shc = Vacuum_Cleaner_Simple_Hill_Climbing.simple_hill_climbing
    Vacuum_Cleaner_Simple_Hill_Climbing.GUI_LOGGER = gui_logger
except ImportError:
    shc = None

try:
    import Vacuum_Cleaner_Steepest_Ascent_Hill_Climbing
    sahc = Vacuum_Cleaner_Steepest_Ascent_Hill_Climbing.steepest_ascent_hill_climbing
    Vacuum_Cleaner_Steepest_Ascent_Hill_Climbing.GUI_LOGGER = gui_logger
except ImportError:
    sahc = None

try:
    import Vacuum_Cleaner_Stochastic_Hill_Climbing
    sthc = Vacuum_Cleaner_Stochastic_Hill_Climbing.stochastic_hill_climbing
    Vacuum_Cleaner_Stochastic_Hill_Climbing.GUI_LOGGER = gui_logger
except ImportError:
    sthc = None

try:
    import Vaccum_Cleaner_Local_Beam_Search
    lbs = Vaccum_Cleaner_Local_Beam_Search.local_beam_search
    Vaccum_Cleaner_Local_Beam_Search.GUI_LOGGER = gui_logger
except ImportError:
    lbs = None

try:
    import Vaccum_Cleaner_Random_Restart_Hill_Climbing
    rrhc = Vaccum_Cleaner_Random_Restart_Hill_Climbing.random_restart_hill_climbing
    Vaccum_Cleaner_Random_Restart_Hill_Climbing.GUI_LOGGER = gui_logger
except ImportError:
    rrhc = None

class Vacuum_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("vacuum_cleaner")
        self.root.geometry("1300x850")
        
        self.BG_APP = "#f8fafc"         # Nền chính xám trắng
        self.BG_PANEL = "#ffffff"       # Khối panel nổi trắng
        self.BG_CARD = "#f1f5f9"        # Nền card xám nhạt
        self.TEXT_MAIN = "#0f172a"      # Chữ đen
        self.TEXT_MUTED = "#475569"     # Chữ xám đậm
        
        self.CYAN = "#0ea5e9"           # Xanh lam
        self.PINK = "#ef4444"           # Đỏ (Màu cảnh báo / Reset)
        self.GREEN = "#10b981"          # Xanh lá (Hoàn thành)
        self.PURPLE = "#8b5cf6"         # Tím (Nhấn nhá)
        
        self.root.configure(bg=self.BG_APP)
        sys.app_gui = self # Đăng ký global để logger gọi được
        

        self.ICON_ROBOT = "🤖"           # Robot
        self.ICON_DIRT = ""
        self.ICON_WALL = ""              # Tường màu nâu
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.initial_room = [
            [1, 1, 1, 0],
            [0, -1, 2, 1],
            [1, 0, -1, 1]
        ]
        self.current_room = copy_state(self.initial_room)
        self.path_solution = []
        self.current_step_idx = 0
        self.is_running_auto = False
        self.map_rows = 4
        self.map_cols = 4
        
        self.setup_ui_layout()
        self.generate_random_map()
        
    def setup_ui_layout(self):

        # HEADER
        header_frame = tk.Frame(self.root, bg=self.BG_PANEL, height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="vacuum_cleaner", font=("Segoe UI Black", 20, "italic"), fg=self.CYAN, bg=self.BG_PANEL).pack(side=tk.LEFT, padx=30, pady=20)
        
        map_tools = tk.Frame(header_frame, bg=self.BG_PANEL)
        map_tools.pack(side=tk.RIGHT, padx=30, pady=20)
        
        tk.Label(map_tools, text="Grid:", font=("Segoe UI", 10, "bold"), fg=self.TEXT_MUTED, bg=self.BG_PANEL).pack(side=tk.LEFT, padx=(0, 10))
        self.spin_rows = tk.Spinbox(map_tools, from_=2, to=20, width=3, font=("Segoe UI", 11, "bold"), bg=self.BG_CARD, fg=self.CYAN, bd=0, buttonbackground=self.BG_CARD)
        self.spin_rows.delete(0, "end")
        self.spin_rows.insert(0, "3")
        self.spin_rows.pack(side=tk.LEFT)
        
        tk.Label(map_tools, text="x", font=("Segoe UI", 12), fg=self.TEXT_MUTED, bg=self.BG_PANEL).pack(side=tk.LEFT, padx=5)
        self.spin_cols = tk.Spinbox(map_tools, from_=2, to=20, width=3, font=("Segoe UI", 11, "bold"), bg=self.BG_CARD, fg=self.CYAN, bd=0, buttonbackground=self.BG_CARD)
        self.spin_cols.delete(0, "end")
        self.spin_cols.insert(0, "3")
        self.spin_cols.pack(side=tk.LEFT, padx=(0, 15))
        
        btn_gen = tk.Button(map_tools, text="GENERATE MAP", bg=self.PURPLE, fg="white", font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2", padx=15, pady=5, command=self.generate_random_map)
        btn_gen.pack(side=tk.LEFT)

        # MAIN CONTENT
        content_frame = tk.Frame(self.root, bg=self.BG_APP)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # LEFT FRAME (MAP)
        left_frame = tk.Frame(content_frame, bg=self.BG_PANEL, bd=0)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        tk.Label(left_frame, text="SIMULATION ENVIRONMENT", font=("Segoe UI", 12, "bold"), fg=self.TEXT_MAIN, bg=self.BG_PANEL).pack(anchor=tk.NW, padx=20, pady=15)
        
        self.canvas = tk.Canvas(left_frame, bg=self.BG_APP, bd=0, highlightthickness=1, highlightbackground=self.BG_CARD)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        status_frame = tk.Frame(left_frame, bg=self.BG_PANEL)
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.lbl_map_status = tk.Label(status_frame, text="Idle.", font=("Segoe UI", 10, "bold"), fg=self.CYAN, bg=self.BG_PANEL)
        self.lbl_map_status.pack(anchor=tk.W)
        
        tk.Label(status_frame, text="SOLUTION PATH:", font=("Segoe UI", 9, "bold"), fg=self.TEXT_MUTED, bg=self.BG_PANEL).pack(anchor=tk.W, pady=(10, 0))
        self.path_text_widget = tk.Text(status_frame, font=("Consolas", 11), bg=self.BG_CARD, fg=self.GREEN, bd=0, relief=tk.FLAT, height=6, wrap=tk.WORD, padx=10, pady=10)
        self.path_text_widget.pack(fill=tk.X, pady=(5, 0))
        self.path_text_widget.config(state=tk.DISABLED)
        
        # RIGHT FRAME (Controls & LOGS
        right_frame = tk.Frame(content_frame, bg=self.BG_APP, width=450)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        
        control_board = tk.Frame(right_frame, bg=self.BG_PANEL, bd=0)
        control_board.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(control_board, text="ALGORITHM SETTINGS", font=("Segoe UI", 12, "bold"), fg=self.TEXT_MAIN, bg=self.BG_PANEL).pack(anchor=tk.NW, padx=20, pady=15)
        
        algo_frame = tk.Frame(control_board, bg=self.BG_PANEL)
        algo_frame.pack(fill=tk.X, padx=20)
        
        self.algo_var = tk.StringVar(value="BFS 1")
        algos = [
            ("BFS 1", "BFS_1"), ("BFS 2", "BFS_2"), 
            ("DFS 1", "DFS_1"), ("DFS 2", "DFS_2"),
            ("IDS 1", "IDS_1"), ("IDS 2", "IDS_2"),
            ("Uniform Cost Search", "UCS"),
            ("Greedy Search", "Greedy"),
            ("A* Search", "AStar"),
            ("IDA* Search", "IDAStar"),
            ("Simple Hill Climbing", "SHC"),
            ("Steepest Ascent Hill Climbing", "SAHC"),
            ("Stochastic Hill Climbing", "StHC"),
            ("Local Beam Search", "LBS"),
            ("Random Restart Hill Climbing", "RRHC")
        ]
        
        self.algo_map = {text: val for text, val in algos}
        
        self.style.configure("TCombobox", fieldbackground=self.BG_CARD, background=self.BG_PANEL, foreground=self.TEXT_MAIN)
        self.algo_cb = ttk.Combobox(algo_frame, textvariable=self.algo_var, values=list(self.algo_map.keys()), state="readonly", style="TCombobox", width=25, font=("Segoe UI", 10, "bold"))
        self.algo_cb.set("BFS 1")
        self.algo_cb.pack(side=tk.LEFT, padx=(0, 15))
            
        action_frame = tk.Frame(control_board, bg=self.BG_PANEL)
        action_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.btn_start = tk.Button(action_frame, text="START SEARCH", bg=self.CYAN, fg="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2", pady=8, command=self.start_search)
        self.btn_start.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.btn_reset = tk.Button(action_frame, text="RESET", bg=self.BG_CARD, fg=self.PINK, font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2", pady=8, command=self.reset_state_only)
        self.btn_reset.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

        sim_frame = tk.Frame(control_board, bg=self.BG_CARD, bd=0)
        sim_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        btn_box = tk.Frame(sim_frame, bg=self.BG_CARD)
        btn_box.pack(fill=tk.X, padx=15, pady=10)
        
        self.btn_next = tk.Button(btn_box, text="⏭ Next Step", bg="#e2e8f0", fg=self.TEXT_MAIN, font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2", command=self.next_step)
        self.btn_next.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.btn_auto = tk.Button(btn_box, text="▶ Auto Play", bg="#e2e8f0", fg=self.TEXT_MAIN, font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2", command=self.toggle_auto_run)
        self.btn_auto.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        scale_box = tk.Frame(sim_frame, bg=self.BG_CARD)
        scale_box.pack(fill=tk.X, padx=15, pady=(0, 15))
        tk.Label(scale_box, text="Speed (ms):", font=("Segoe UI", 8), fg=self.TEXT_MUTED, bg=self.BG_CARD).pack(side=tk.LEFT)
        self.speed_scale = tk.Scale(scale_box, from_=100, to=2000, orient=tk.HORIZONTAL, bg=self.BG_CARD, fg=self.CYAN, highlightthickness=0, bd=0, resolution=100, length=150, troughcolor=self.BG_APP)
        self.speed_scale.set(300)
        self.speed_scale.pack(side=tk.RIGHT)

        # LOGS
        console_frame = tk.Frame(right_frame, bg="#1e293b", bd=1, highlightthickness=1, highlightbackground=self.BG_CARD)
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(console_frame, text="LOGS >_", font=("Consolas", 10, "bold"), fg="#94a3b8", bg="#1e293b").pack(anchor=tk.NW, padx=10, pady=(10, 0))
        
        self.log_text = tk.Text(console_frame, bg="#1e293b", fg="#4ade80", font=("Consolas", 10), bd=0, highlightthickness=0, padx=10, pady=10)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        
        scrollbar = ttk.Scrollbar(console_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.root.bind('<Configure>', self.on_resize)

    def on_resize(self, event):
        if event.widget == self.root:
            self.draw_grid()

    def log_msg(self, msg, clear=False):
        self.log_text.config(state=tk.NORMAL)
        if clear:
            self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def log_algorithm_step(self, node, frontier, reached):

        # Chỉ đếm số node đã duyệt, không in ra màn hình để tránh làm rối log
        if not hasattr(self, 'explored_nodes_count'):
            self.explored_nodes_count = 0
        self.explored_nodes_count += 1

    def generate_random_map(self):
        try:
            self.map_rows = int(self.spin_rows.get())
            self.map_cols = int(self.spin_cols.get())
        except ValueError:
            messagebox.showerror("Error", "Kích thước map không hợp lệ.")
            return
            
        if self.map_rows < 2 or self.map_cols < 2:
            return
            
        new_room = [[0 for _ in range(self.map_cols)] for _ in range(self.map_rows)]
        
        num_walls = int(self.map_rows * self.map_cols * 0.20)
        for _ in range(num_walls):
            r, c = random.randint(0, self.map_rows-1), random.randint(0, self.map_cols-1)
            new_room[r][c] = -1
            
        num_dirt = int(self.map_rows * self.map_cols * 0.25)
        dirt_added = 0
        while dirt_added < num_dirt:
            r, c = random.randint(0, self.map_rows-1), random.randint(0, self.map_cols-1)
            if new_room[r][c] == 0:
                new_room[r][c] = 1
                dirt_added += 1
                
        placed = False
        while not placed:
            r, c = random.randint(0, self.map_rows-1), random.randint(0, self.map_cols-1)
            if new_room[r][c] == 0:
                new_room[r][c] = 2
                placed = True
            elif new_room[r][c] == 1:
                new_room[r][c] = 3
                placed = True
                
        self.initial_room = new_room
        self.reset_state_only(log=False)
        self.lbl_map_status.config(text=f"New Sector Generated: {self.map_rows}x{self.map_cols}. Awaiting Orders.", fg=self.CYAN)
        self.log_msg(f"SYS: Map {self.map_rows}x{self.map_cols} initialized.", clear=True)

    def reset_state_only(self, log=True):
        self.current_room = copy_state(self.initial_room)
        self.path_solution = []
        self.current_step_idx = 0
        self.is_running_auto = False
        self.btn_auto.config(text="▶ Auto Play", fg=self.TEXT_MAIN)
        self.update_path_entry("")
        self.draw_grid()
        if log:
            self.lbl_map_status.config(text="Sector reset. Ready for scan.", fg=self.PINK)
            self.log_msg("SYS: State reverted to initial.")

    def draw_grid(self):
        self.canvas.delete("all")
        if not hasattr(self, 'current_room') or not self.current_room:
            return
            
        rows = len(self.current_room)
        cols = len(self.current_room[0])
        
        c_width = self.canvas.winfo_width()
        c_height = self.canvas.winfo_height()
        
        if c_width <= 1 or c_height <= 1:
            return
            
        padding = 30
        available_w = c_width - padding * 2
        available_h = c_height - padding * 2
        
        cell_size = min(available_w // cols, available_h // rows)
        cell_size = min(cell_size, 110)
        
        start_x = (c_width - (cols * cell_size)) // 2
        start_y = (c_height - (rows * cell_size)) // 2

        for r in range(rows):
            for c in range(cols):
                gap = 5
                x1 = start_x + c * cell_size + gap
                y1 = start_y + r * cell_size + gap
                x2 = start_x + (c + 1) * cell_size - gap
                y2 = start_y + (r + 1) * cell_size - gap

                val = self.current_room[r][c]
                
                bg_color = "#ffffff"     # Màu ô trống: trắng
                outline_color = "#cbd5e1"
                text_label = ""
                text_color = ""
                font_size = max(14, cell_size // 3)
                
                if val == -1: # Wall
                    bg_color = "#1f2937" # Đen/Xám đen
                    outline_color = "#111827"
                    text_label = self.ICON_WALL
                    text_color = "#000000"
                elif val == 1: # Dirt
                    bg_color = "#8B4513" # Màu Nâu
                    outline_color = "#5c2e0b"
                    text_label = self.ICON_DIRT
                    text_color = ""
                elif val == 2: # Robot
                    bg_color = "#ffffff" # Trắng tinh
                    outline_color = self.CYAN
                    text_label = self.ICON_ROBOT
                    text_color = self.CYAN
                elif val == 3: # Robot + Dirt
                    bg_color = "#A0522D" # Màu Nâu
                    outline_color = self.CYAN
                    text_label = self.ICON_ROBOT
                    text_color = self.CYAN

                r_radius = 8
                self.canvas.create_polygon(
                    x1+r_radius, y1, x2-r_radius, y1, x2, y1+r_radius, x2, y2-r_radius,
                    x2-r_radius, y2, x1+r_radius, y2, x1, y2-r_radius, x1, y1+r_radius,
                    fill=bg_color, outline=outline_color, smooth=True, width=2
                )
                
                if text_label:
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=text_label, font=("Segoe UI Emoji", font_size), fill=text_color)

    def update_path_entry(self, text):
        self.path_text_widget.config(state=tk.NORMAL)
        self.path_text_widget.delete(1.0, tk.END)
        self.path_text_widget.insert(tk.END, text)
        self.path_text_widget.config(state=tk.DISABLED)

    def start_search(self):
        self.reset_state_only(log=False)
        algo_display = self.algo_var.get()
        algo = self.algo_map.get(algo_display, algo_display)
        
        self.explored_nodes_count = 0
        
        r, c = find_robot(self.initial_room)
        dirt_count = sum(row.count(1) + row.count(3) for row in self.initial_room)
        
        self.log_msg(f"Bắt đầu tìm kiếm bằng thuật toán {algo_display} ({algo})...")
        self.log_msg(f"Trạng thái ban đầu: Vị trí xuất phát của robot ({r}, {c}) và số lượng vết bẩn hiện tại: {dirt_count}.")
        
        start_time = time.time()
        result = None
        
        try:
            if algo == "BFS_1" and bfs1: result = bfs1(copy_state(self.initial_room))
            elif algo == "BFS_2" and bfs2: result = bfs2(copy_state(self.initial_room))
            elif algo == "DFS_1" and dfs1: result = dfs1(copy_state(self.initial_room))
            elif algo == "DFS_2" and dfs2: result = dfs2(copy_state(self.initial_room))
            elif algo == "IDS_1" and ids1: result = ids1(copy_state(self.initial_room))
            elif algo == "IDS_2" and ids2: result = ids2(copy_state(self.initial_room))
            elif algo == "UCS" and ucs: result = ucs(copy_state(self.initial_room))
            elif algo == "Greedy" and greedy: result = greedy(copy_state(self.initial_room))
            elif algo == "AStar" and astar: result = astar(copy_state(self.initial_room))
            elif algo == "IDAStar" and idastar: result = idastar(copy_state(self.initial_room))
            elif algo == "SHC" and shc: result = shc(copy_state(self.initial_room))
            elif algo == "SAHC" and sahc: result = sahc(copy_state(self.initial_room))
            elif algo == "StHC" and sthc: result = sthc(copy_state(self.initial_room))
            elif algo == "LBS" and lbs: result = lbs(copy_state(self.initial_room))
            elif algo == "RRHC" and rrhc: result = rrhc(copy_state(self.initial_room))
            else:
                self.log_msg(f"ERR: Module {algo} offline!")
                return
        except Exception as e:
            self.log_msg(f"ERR: Core panic -> {e}")
            return
            
        end_time = time.time()
        exec_time = (end_time - start_time) * 1000

        if result == "Failure" or not isinstance(result, list):
            self.lbl_map_status.config(text=f"Scan Failed. No valid path found.", fg=self.PINK)
            self.log_msg(f"[Thất bại] Thuật toán không tìm thấy đường đi khả thi do bị vật cản bao vây.")
        else:
            self.path_solution = result
            self.current_step_idx = 0
            self.lbl_map_status.config(text=f"Path acquired: {len(result)} moves.", fg=self.GREEN)
            self.update_path_entry(" ➔ ".join(result))
            
            self.log_msg(f"Đã tìm thấy đường đi trong {exec_time:.2f}ms.")
            self.log_msg(f"Số lượng Node đã duyệt (Explored/Reached Nodes): {self.explored_nodes_count}")
            self.log_msg(f"Chuỗi hành động tối ưu: {result}")

    def execute_action(self, action):
        r, c = find_robot(self.current_room)
        old_val = self.current_room[r][c]
        
        if action == "Suck":
            if self.current_room[r][c] == 3:
                self.current_room[r][c] = 2
        else:
            nr, nc = r, c
            if action == "Up": nr -= 1
            elif action == "Down": nr += 1
            elif action == "Left": nc -= 1
            elif action == "Right": nc += 1
            
            self.current_room[r][c] = 1 if old_val == 3 else 0
            if self.current_room[nr][nc] == 1:
                self.current_room[nr][nc] = 3
            else:
                self.current_room[nr][nc] = 2
                
        self.draw_grid()

    def next_step(self):
        if not self.path_solution:
            return
            
        if self.current_step_idx < len(self.path_solution):
            action = self.path_solution[self.current_step_idx]
            step_num = self.current_step_idx + 1
            total_steps = len(self.path_solution)
            
            r, c = find_robot(self.current_room)
            
            if action == "Suck":
                self.log_msg(f"Bước {step_num}/{total_steps}: Phát hiện bụi! Robot đang hút [Suck].")
                self.log_msg(f"Thông báo trạng thái ô: Ô ({r}, {c}) đã được làm sạch.")
            else:
                nr, nc = r, c
                if action == "Up": nr -= 1
                elif action == "Down": nr += 1
                elif action == "Left": nc -= 1
                elif action == "Right": nc += 1
                self.log_msg(f"Bước {step_num}/{total_steps}: Robot di chuyển [{action}] sang ô ({nr}, {nc}).")
                
            self.execute_action(action)
            self.current_step_idx += 1
            
            if self.current_step_idx == len(self.path_solution):
                self.log_msg("[Thành công] Robot đã dọn sạch toàn bộ phòng!")
                self.lbl_map_status.config(text="MISSION ACCOMPLISHED. Area clean.", fg=self.CYAN)
                self.is_running_auto = False
                self.btn_auto.config(text="▶ Auto Play", fg=self.TEXT_MAIN)

    def toggle_auto_run(self):
        if not self.path_solution:
            self.log_msg("WRN: No route found. Please START SEARCH.")
            return
            
        if self.current_step_idx >= len(self.path_solution):
            self.log_msg("SYS: Route already completed.")
            return
            
        if self.is_running_auto:
            self.is_running_auto = False
            self.btn_auto.config(text="▶ Auto Play", fg=self.TEXT_MAIN)
            self.log_msg("SYS: Auto execution paused.")
        else:
            self.is_running_auto = True
            self.btn_auto.config(text="⏸ Pause", fg=self.PINK)
            self.log_msg("SYS: Auto execution engaged.")
            self.auto_step()

    def auto_step(self):
        if self.is_running_auto and self.current_step_idx < len(self.path_solution):
            self.next_step()
            speed_ms = int(self.speed_scale.get())
            self.root.after(speed_ms, self.auto_step)

if __name__ == "__main__":
    root = tk.Tk()
    app = Vacuum_GUI(root)
    root.mainloop()