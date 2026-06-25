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


# Cache trạng thái con để giảm số lần tính toán
_memo_child = {}


# Sinh trạng thái mới sau khi thực hiện hành động
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

    # Không cho phép robot đi vào vật cản hoặc ra khỏi bản đồ
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


# Truy vết đường đi từ node đích về node gốc
def solution(node):
    path = []

    while node["parent"] is not None:
        path.append(node["action"])
        node = node["parent"]

    path.reverse()
    return path


# Sinh belief state ban đầu cho môi trường hoàn toàn không quan sát được
# Robot không biết vị trí của mình và cũng không biết ô nào sạch hay bẩn
def generate_initial_belief_state(grid_layout):
    rows = len(grid_layout)
    cols = len(grid_layout[0])
    
    valid_robot_positions = []
    dirt_positions = []
    
    for r in range(rows):
        for c in range(cols):
            if grid_layout[r][c] != -1:
                valid_robot_positions.append((r, c))
                dirt_positions.append((r, c))
                
    initial_belief = set()
    
    # Sinh mọi khả năng sạch/bẩn của môi trường
    for dirt_comb in itertools.product([0, 1], repeat=len(dirt_positions)):
        base_room = [row[:] for row in grid_layout]

        for idx, pos in enumerate(dirt_positions):
            base_room[pos[0]][pos[1]] = dirt_comb[idx]
            
        # Sinh mọi vị trí có thể của robot
        for r_pos in valid_robot_positions:
            room_with_robot = [row[:] for row in base_room]
            curr_val = room_with_robot[r_pos[0]][r_pos[1]]
            
            if curr_val == 0:
                room_with_robot[r_pos[0]][r_pos[1]] = 2
            elif curr_val == 1:
                room_with_robot[r_pos[0]][r_pos[1]] = 3
                
            state_tuple = tuple(tuple(row) for row in room_with_robot)
            initial_belief.add(state_tuple)
            
    return initial_belief


# Hiển thị các trạng thái có thể xảy ra trong belief state
def print_belief_state(belief_state):
    print(f"[Có tất cả {len(belief_state)} kịch bản trạng thái có thể xảy ra]")

    for idx, state_tuple in enumerate(belief_state, 1):
        print(f"  Cấu hình tiềm năng {idx}:")

        for row in state_tuple:
            print(f"    {list(row)}")

    print("-" * 40)