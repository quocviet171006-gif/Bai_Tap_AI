# 🤖 Vacuum Cleaner AI - Intelligent Pathfinding Agent

**Giải quyết bài toán người quét rác (Vacuum Cleaner) bằng các thuật toán tìm kiếm**

---

## 📋 Mô tả dự án

Dự án xây dựng một **agent thông minh** mô phỏng robot hút bụi (vacuum cleaner) trong môi trường lưới (grid) có chướng ngại vật. Agent phải tìm đường đi tối ưu để dọn sạch tất cả bụi bẩn với chi phí thấp nhất.

Dự án tập trung vào việc **triển khai và so sánh** các thuật toán tìm kiếm cổ điển và heuristic trong AI:

## 1. Tính năng chính
* **Môi trường linh hoạt**: Tùy chỉnh kích thước grid, vị trí bụi và vật cản.
* **Đa dạng thuật toán**: Triển khai đầy đủ các nhóm tìm kiếm:
    * **Uninformed Search**: BFS, DFS, IDS, UCS.
    * **Informed Search**: A*, Greedy Best-First Search.
    * **Local Search**: Hill Climbing, Simulated Annealing, Beam Search.
    * **Nondeterministic**: And-Or Search cho môi trường quan sát một phần.
* **Trực quan hóa**: Giao diện GUI hỗ trợ theo dõi quá trình tìm đường và biểu đồ phân tích hiệu suất

## 2. 📁 Cấu trúc dự án

```bash
vacuum_cleaner/
├── assets/                  # Ảnh, GIF minh họa giao diện và demo
├── jupyter/                 # Các tệp Notebook phân tích thuật toán
├── python/
│   ├── environment/         # Các thuật toán giải bài toán hút bụi
│   │   ├── Informed_Search/ # A*, Greedy, IDS, IDStar...
│   │   ├── Local_Search/    # Hill Climbing, Simulated Annealing, Beam Search...
│   │   ├── Nondeterministic/
│   │   │   ├── Partial_observable/
│   │   │   └── Sensorless/
│   │   └── Uninformed_Search/ # BFS, DFS, UCS...
│   ├── gui/                 # Giao diện đồ họa (Vacuum_GUI.py)
│   ├── main.py              # File chạy chính
└── └── utils.py             # Các hàm tiện ích dùng chung

```

## 3. 🚀 Cách chạy dự án
**3.1. Yêu cầu hệ thống**

## 🛠 Công nghệ sử dụng

Ngôn ngữ: Python

Thư viện:
- pygame / tkinter (GUI)
- numpy (xử lý ma trận)
- matplotlib (vẽ biểu đồ so sánh)
- collections, heapq (các cấu trúc dữ liệu)

Thư viện: 
```bash
pip install pygame numpy matplotlib jupyter
```

Cài đặt

Chạy lệnh sau trong terminal:

```bash
pip install pygame numpy matplotlib jupyter
```

**3.2. Chạy chương trình chính**

cd python

python Vacuum_GUI.py                    # Chạy giao diện đồ họa

**3.3. Chạy Jupyter Notebooks**

cd jupyter

jupyter notebook

Mở các file .ipynb tương ứng với thuật toán muốn phân tích.
 
## 4. 🎥 Minh họa

<img src="vacuum_cleaner/assets/A_Star.gif" alt="A* Search Animation">
<img src="vacuum_cleaner/assets/BFS.gif" alt="BFS Search Animation">
<img src="vacuum_cleaner/assets/DFS.gif" alt="DFS Search Animation">
<img src="vacuum_cleaner/assets/IDA_Star.gif" alt="IDA* Search Animation">
<img src="vacuum_cleaner/assets/UCS.gif" alt="UCS Search Animation">

## 5. 📈 Phân tích kết quả

| Thuật toán | Loại tìm kiếm | Độ tối ưu | Độ phức tạp bộ nhớ | Ghi chú |
| :--- | :---: | :---: | :---: | :--- |
| **BFS** | Uninformed | Tối ưu | Cao ($O(b^d)$) | Đảm bảo tìm thấy đường đi ngắn nhất. |
| **DFS** | Uninformed | Không | Thấp ($O(bm)$) | Có thể bị lặp vô hạn, không tối ưu. |
| **UCS** | Uninformed | Tối ưu | Cao | Tối ưu theo chi phí thực tế của đường đi. |
| **IDS** | Uninformed | Tối ưu | Thấp ($O(bd)$) | Cân bằng hoàn hảo giữa bộ nhớ và thời gian. |
| **Greedy** | Informed | Không | Trung bình | Tốc độ rất nhanh nhưng dễ bị sa vào cục bộ. |
| **A\*** | Informed | Tối ưu | Cao | Hiệu quả cao nhờ hàm Heuristic $f(n)=g(n)+h(n)$. |
| **Hill Climbing** | Local Search | Không | Rất thấp | Nhanh, nhưng dễ rơi vào cực đại địa phương. |
| **Simulated Annealing** | Local Search | Khá | Rất thấp | Khắc phục được nhược điểm của Hill Climbing. |

### Đánh giá chuyên sâu:
### 1. Nhóm tìm kiếm mù (Uninformed Search):

BFS & UCS là lựa chọn an toàn khi môi trường không quá lớn, đảm bảo tìm được nghiệm tối ưu.

IDS là lựa chọn thay thế tốt nhất cho BFS khi bộ nhớ hạn chế nhưng vẫn muốn giữ tính tối ưu.

DFS chỉ nên dùng khi không gian trạng thái rất sâu hoặc có giới hạn độ sâu cụ thể.

### 2. Nhóm tìm kiếm có thông tin (Informed Search - Heuristic):

A* là "tiêu chuẩn vàng" cho bài toán này, đặc biệt khi sử dụng Heuristic Manhattan hoặc Euclidean phù hợp.

Greedy chỉ phù hợp khi yêu cầu tốc độ phản hồi tức thời (real-time) và chấp nhận kết quả không tối ưu.

### 3. Nhóm tìm kiếm cục bộ (Local Search):

Phù hợp cho các môi trường lưới cực lớn hoặc bài toán biến thể yêu cầu tối ưu hóa liên tục mà không cần tìm đường đi từ A đến B một cách tuần tự.
## 6. 👥 Tác giả

Tên sinh viên: Nguyễn Quốc Việt

MSSV: 24110381
đây là readme của tôi nhưng hình thức nó ch đẹp lắm
