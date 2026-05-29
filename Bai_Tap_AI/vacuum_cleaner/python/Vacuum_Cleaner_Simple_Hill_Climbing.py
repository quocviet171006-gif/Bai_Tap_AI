from utils import goal_test, actions, child_node, solution, heuristic

def value_func(state):
    # Định nghĩa giá trị (Value) để tìm cực đại: Càng ít vết bẩn, giá trị càng cao
    return -heuristic(state)

def simple_hill_climbing(initial_state):
    # Khởi tạo node hiện tại từ trạng thái ban đầu
    current_node = {
        "state": initial_state,
        "parent": None,
        "action": None,
        "cost": 0
    }

    while True:
        # Nếu Current_State == Goal: TRẢ VỀ Current_State
        if goal_test(current_node["state"]):
            return solution(current_node)

        # Sinh các trạng thái lân cận của Current_State
        possible_actions = actions(current_node["state"])
        current_value = value_func(current_node["state"])
        
        neighbor_found = False
        
        # Tìm thấy Next_State đầu tiên có Value(Next_State) > Value(Current_State)
        for action in possible_actions:
            child = child_node(current_node, action)
            child_value = value_func(child["state"])
            
            if child_value > current_value:
                current_node = child
                neighbor_found = True
                break  # Lấy ngay lân cận đầu tiên tốt hơn và tiếp tục vòng lặp
        
        # Nếu ĐÃ DUYỆT HẾT lân cận mà không có ai tốt hơn: Dừng vì đã đạt cực đại cục bộ
        if not neighbor_found:
            return solution(current_node)  # Trả về đường đi hiện tại