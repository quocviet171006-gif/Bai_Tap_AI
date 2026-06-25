import itertools


# Tìm vị trí hiện tại của robot trong môi trường
def find_robot(state):
    rows = len(state)
    cols = len(state[0])

    for row in range(rows):
        for col in range(cols):
            if state[row][col] == 2 or state[row][col] == 3:
                return (row, col)

    return None


# Kiểm tra một trạng thái đơn đã đạt mục tiêu hay chưa
def goal_test_single(state):
    for row in state:
        if 1 in row or 3 in row:
            return False
    return True


# Kiểm tra toàn bộ belief state đã đạt mục tiêu hay chưa
def belief_goal_test(belief_state):
    for state_tuple in belief_state:
        state = [list(row) for row in state_tuple]

        if not goal_test_single(state):
            return False

    return True


# Sao chép trạng thái để tránh thay đổi dữ liệu gốc
def copy_state(state):
    return [row[:] for row in state]


# Bộ nhớ đệm giúp giảm số lần tính toán trạng thái con
_memo_child = {}


# Sinh trạng thái mới sau khi thực hiện một hành động
def child_node_single(state, action):
    state_tuple = tuple(tuple(row) for row in state)
    key = (state_tuple, action)

    if key in _memo_child:
        return _memo_child[key]

    new_state = copy_state(state)
    res = find_robot(state)

    if res is None:
        _memo_child[key] = new_state
        return new_state
    
    lct_row, lct_col = res
    rows = len(state)
    cols = len(state[0])

    # Hành động hút bụi
    if action == "Suck":
        if new_state[lct_row][lct_col] == 3:
            new_state[lct_row][lct_col] = 2
        return new_state

    # Xác định vị trí mới của robot
    nx, ny = lct_row, lct_col

    if action == "Up":
        nx -= 1
    elif action == "Down":
        nx += 1
    elif action == "Left":
        ny -= 1
    elif action == "Right":
        ny += 1

    # Không cho phép đi ra ngoài bản đồ hoặc vào vật cản
    if nx < 0 or nx >= rows or ny < 0 or ny >= cols or new_state[nx][ny] == -1:
        return new_state

    # Cập nhật ô cũ của robot
    if new_state[lct_row][lct_col] == 2:
        new_state[lct_row][lct_col] = 0
    elif new_state[lct_row][lct_col] == 3:
        new_state[lct_row][lct_col] = 1

    # Cập nhật ô mới của robot
    if new_state[nx][ny] == 0:
        new_state[nx][ny] = 2
    elif new_state[nx][ny] == 1:
        new_state[nx][ny] = 3

    _memo_child[key] = new_state
    return new_state


# Mô hình chuyển trạng thái cho belief state
def transition_model(belief_state, action):
    new_belief = set()

    for state_tuple in belief_state:
        state = [list(row) for row in state_tuple]
        next_state = child_node_single(state, action)

        next_state_tuple = tuple(tuple(row) for row in next_state)
        new_belief.add(next_state_tuple)

    return new_belief


# Sinh belief state ban đầu cho bài toán Sensorless Vacuum World
# Robot biết vị trí của mình nhưng không biết các ô khác sạch hay bẩn
def generate_initial_belief_state(grid_layout):
    rows = len(grid_layout)
    cols = len(grid_layout[0])

    robot_pos = None
    dirt_positions = []

    for r in range(rows):
        for c in range(cols):
            if grid_layout[r][c] in [2, 3]:
                robot_pos = (r, c)

            if grid_layout[r][c] != -1:
                dirt_positions.append((r, c))

    initial_belief = set()

    # Sinh tất cả các khả năng sạch/bẩn của môi trường
    for dirt_comb in itertools.product([0, 1], repeat=len(dirt_positions)):
        base_room = [row[:] for row in grid_layout]

        for idx, pos in enumerate(dirt_positions):
            base_room[pos[0]][pos[1]] = dirt_comb[idx]

        # Đặt lại vị trí robot vào môi trường
        r_row, r_col = robot_pos
        curr_val = base_room[r_row][r_col]

        base_room[r_row][r_col] = 2 if curr_val == 0 else 3

        state_tuple = tuple(tuple(row) for row in base_room)
        initial_belief.add(state_tuple)

    return initial_belief


# Hiển thị toàn bộ các trạng thái có thể xảy ra trong belief state
def print_belief_state(belief_state):
    print(f"[Co tat ca {len(belief_state)} kich ban trang thai co the xay ra]")

    for idx, state_tuple in enumerate(belief_state, 1):
        print(f"  Cau hinh tiem nang {idx}:")

        for row in state_tuple:
            print(f"    {list(row)}")

    print("-" * 40)