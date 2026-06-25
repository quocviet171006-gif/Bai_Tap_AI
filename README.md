# 🤖 Vacuum Cleaner AI - Intelligent Pathfinding Agent

**Giải quyết bài toán người quét rác (Vacuum Cleaner) bằng các thuật toán tìm kiếm**

---

## 📋 Mô tả dự án

Dự án xây dựng một **agent thông minh** mô phỏng robot hút bụi (vacuum cleaner) trong môi trường lưới (grid) có chướng ngại vật. Agent phải tìm đường đi tối ưu để dọn sạch tất cả bụi bẩn với chi phí thấp nhất.

Dự án tập trung vào việc **triển khai và so sánh** các thuật toán tìm kiếm cổ điển và heuristic trong AI:

- **Uninformed Search**: BFS, DFS, IDS, UCS
- **Informed Search**: Greedy Best-First Search, A* Search

---

## ✨ Tính năng chính

- Mô hình môi trường grid động (có thể thay đổi kích thước, vị trí bụi và chướng ngại vật)
- Triển khai đầy đủ nhiều biến thể của các thuật toán tìm kiếm
- Giao diện đồ họa (GUI) sử dụng Pygame hoặc Tkinter để minh họa quá trình tìm đường
- Jupyter Notebooks phân tích từng thuật toán
- So sánh hiệu suất (số node mở rộng, chi phí đường đi, thời gian chạy)
- Hỗ trợ nhiều loại heuristic (Manhattan, Euclidean, v.v.)

---

## 📁 Cấu trúc dự án

```bash
vacuum_cleaner/
├── assets/                  # Ảnh, GIF minh họa giao diện và demo
├── jupyter/                 # Các tệp Notebook phân tích thuật toán
├── python/
│   ├── environment/         # Các thuật toán giải bài toán hút bụi
│   │   ├── Informed_Search/ # A*, Greedy, IDS, IDStar...
│   │   ├── Local_Search/    # Hill Climbing, Simulated Annealing, Beam Search...
│   │   ├── Nondeterministic/
│   │   │   ├── Partial_observable/
│   │   │   └── Sensorless/
│   │   └── Uninformed_Search/ # BFS, DFS, UCS...
│   ├── gui/                 # Giao diện đồ họa (Vacuum_GUI.py)
│   ├── main.py              # File chạy chính
└── └── utils.py             # Các hàm tiện ích dùng chung

```

## 🚀 Cách chạy dự án
**1. Yêu cầu hệ thống**

Python 3.8+
Thư viện:Bashpip install pygame numpy matplotlib jupyter

**2. Chạy chương trình chính**

cd python
python Vacuum_GUI.py                    # Chạy giao diện đồ họa
python Vacuum_Cleaner_AStar.py          # Chạy thuật toán A*

**3. Chạy Jupyter Notebooks**

cd jupyter
jupyter notebook
Mở các file .ipynb tương ứng với thuật toán muốn phân tích.

## 📊 Các thuật toán đã triển khai

- BFS: Tìm đường đi ngắn nhất.
- DFS: Tìm đường sâu
- Iterative Deepending Search (IDS): Kết hợp ưu điểm của BFS và DFS
- Uniform Cost Search (UCS): Tối ưu theo chi phí
- Greedy Search: Dựa vào heiristic
- A* Search: Tối ưu
 
## 🎥 Minh họa

(Thêm GIF từ thư mục assets/ vào đây)
<img src="assets/demo_gui.gif" alt="Vacuum Cleaner GUI">
<img src="assets/astar_demo.gif" alt="A* Search Animation">
<img src="assets/comparison.gif" alt="BFS vs A* Comparison">

## 📈 Phân tích kết quả

A* thường cho kết quả tối ưu nhất về chi phí và số node mở rộng.
BFS đảm bảo tìm đường ngắn nhất (về số bước) nhưng tốn bộ nhớ.
IDS là giải pháp cân bằng tốt khi không biết độ sâu.
Greedy nhanh nhưng không đảm bảo tối ưu.

(Chi tiết so sánh nằm trong các Jupyter Notebook)

## 🛠 Công nghệ sử dụng

Ngôn ngữ: Python
Thư viện:
- pygame / tkinter (GUI)
- numpy (xử lý ma trận)
- matplotlib (vẽ biểu đồ so sánh)
- collections, heapq (các cấu trúc dữ liệu)

## 👥 Tác giả

Tên sinh viên: Nguyễn Quốc Việt
MSSV: 24110381
