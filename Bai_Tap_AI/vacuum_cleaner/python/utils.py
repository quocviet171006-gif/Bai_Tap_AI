# Hàm tiện ích dùng chung cho tất cả các thuật toán tìm kiếm máy hút bụi
# Quy ước giá trị ô trong lưới:
#   -1 = tường, 0 = ô trống sạch, 1 = ô bẩn, 2 = robot (ô sạch), 3 = robot (ô bẩn)

# Tìm vị trí hiện tại của robot trong lưới
def find_robot(state):
    rows = len(state)
    cols = len(state[0])
    for row in range(rows):
        for col in range(cols):
            if state[row][col] == 2 or state[row][col] == 3:
                return (row, col)

# Kiểm tra xem trạng thái hiện tại có phải trạng thái đích chưa
# Trạng thái đích khi không còn ô bẩn nào trong lưới
def goal_test(state):
    for row in state:
        if 1 in row or 3 in row:
            return False
    return True

# Tạo bản sao độc lập của lưới để tránh thay đổi trạng thái gốc
def copy_state(state):
    return [row[:] for row in state]

# Trả về danh sách hành động hợp lệ từ trạng thái hiện tại
# Robot có thể di chuyển 4 hướng nếu không bị tường chặn, và hút bụi nếu đang đứng trên ô bẩn
def actions(state):
    rows = len(state)
    cols = len(state[0])
    location_row, location_col = find_robot(state)
    move = []

    if location_row > 0 and state[location_row - 1][location_col] != -1:
        move.append("Up")

    if location_row < rows - 1 and state[location_row + 1][location_col] != -1:
        move.append("Down")

    if location_col > 0 and state[location_row][location_col - 1] != -1:
        move.append("Left")

    if location_col < cols - 1 and state[location_row][location_col + 1] != -1:
        move.append("Right")

    if state[location_row][location_col] == 3:
        move.append("Suck")

    return move

# Sinh ra node con từ node cha sau khi thực hiện một hành động
# Trả về node mới gồm trạng thái, con trỏ cha, hành động và chi phí tích lũy
def child_node(parent, action):
    state = parent["state"]
    new_state = copy_state(state)
    lct_row, lct_col = find_robot(state)

    if action == "Suck":
        # Hút bụi tại ô hiện tại, đổi giá trị 3 (robot+bẩn) thành 2 (robot+sạch)
        if new_state[lct_row][lct_col] == 3:
            new_state[lct_row][lct_col] = 2
        return {
            "state": new_state,
            "parent": parent,
            "action": action,
            "cost": parent["cost"] + 1
        }

    # Xác định ô đích khi di chuyển
    nx, ny = lct_row, lct_col
    if action == "Up": nx -= 1
    elif action == "Down": nx += 1
    elif action == "Left": ny -= 1
    elif action == "Right": ny += 1

    # Xóa robot khỏi ô cũ, giữ lại trạng thái bẩn/sạch của ô đó
    if new_state[lct_row][lct_col] == 2:
        new_state[lct_row][lct_col] = 0
    elif new_state[lct_row][lct_col] == 3:
        new_state[lct_row][lct_col] = 1

    # Đặt robot vào ô mới, kết hợp với trạng thái sẵn có của ô đó
    if new_state[nx][ny] == 0:
        new_state[nx][ny] = 2
    elif new_state[nx][ny] == 1:
        new_state[nx][ny] = 3

    return {
        "state": new_state,
        "parent": parent,
        "action": action,
        "cost": parent["cost"] + 1
    }

# Truy vết ngược từ node đích lên node gốc để lấy chuỗi hành động
def solution(node):
    path = []
    while node["parent"] != None:
        path.append(node["action"])
        node = node["parent"]
    path.reverse()
    return path

# Kiểm tra xem một trạng thái có đang nằm trong frontier chưa
# Dùng cho các thuật toán không dùng set để lưu frontier
def in_frontier(frontier, state):
    for node in frontier:
        if node["state"] == state:
            return True
    return False

# Hàm heuristic: đếm số ô bẩn còn lại trong lưới
# Dùng cho các thuật toán tìm kiếm có thông tin (Greedy, A*, IDA*)
def heuristic(state):
    h = 0
    for row in state:
        for cell in row:
            if cell == 1 or cell == 3:
                h += 1
    return h