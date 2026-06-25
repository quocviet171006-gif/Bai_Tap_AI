from utils import find_robot, child_node, actions, goal_test, solution

GUI_LOGGER = None

# Hàm heuristic đánh giá trạng thái dựa trên số ô bẩn
# và khoảng cách đến ô bẩn gần nhất
def get_heuristic(state):
    rx, ry = find_robot(state)
    dirt_count = 0
    min_dist = float('inf')
    
    for r in range(len(state)):
        for c in range(len(state[0])):
            if state[r][c] in (1, 3):
                dirt_count += 1
                dist = abs(r - rx) + abs(c - ry)
                if dist < min_dist:
                    min_dist = dist
                    
    if dirt_count == 0:
        return 0

    return (dirt_count * 1000) + min_dist


# Thuật toán Hill Climbing
# Luôn chọn trạng thái lân cận có heuristic tốt nhất
def hill_climbing(initial_node):
    current = initial_node
    
    while True:
        if goal_test(current["state"]):
            return current
            
        if GUI_LOGGER:
            GUI_LOGGER(current, [], [])
            
        neighbors = []

        # Sinh các trạng thái lân cận
        for action in actions(current["state"]):
            child = child_node(current, action)
            child["cost"] = get_heuristic(child["state"])
            neighbors.append(child)
        
        # Không còn trạng thái để mở rộng
        if not neighbors:
            return current
            
        # Chọn hàng xóm có heuristic nhỏ nhất
        neighbors.sort(key=lambda x: x["cost"])
        
        # Nếu không tìm được trạng thái tốt hơn thì dừng
        if neighbors[0]["cost"] >= current["cost"]:
            return current  
            
        current = neighbors[0]


# Random Restart Hill Climbing
# Thực hiện Hill Climbing nhiều lần để tránh kẹt tại cực trị cục bộ
def random_restart_hill_climbing(initial_state, max_restarts=10):
    for i in range(max_restarts):

        # Khởi tạo lại trạng thái ban đầu
        initial_node = {
            "state": initial_state,
            "parent": None,
            "action": None,
            "cost": get_heuristic(initial_state)
        }
        
        result_node = hill_climbing(initial_node)

        # Nếu tìm được lời giải thì trả về kết quả
        if goal_test(result_node["state"]):
            return solution(result_node)
            
    return "Failure"