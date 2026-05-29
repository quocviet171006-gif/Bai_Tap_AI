from utils import goal_test, actions, child_node, solution, heuristic

def value_func(state):
    return -heuristic(state)

def steepest_ascent_hill_climbing(initial_state):
    current_node = {
        "state": initial_state,
        "parent": None,
        "action": None,
        "cost": 0
    }

    while True:
        if goal_test(current_node["state"]):
            return solution(current_node)

        # Sinh TẤT CẢ các trạng thái lân cận của Current_State
        possible_actions = actions(current_node["state"])
        if not possible_actions:
            return solution(current_node)

        best_neighbor = None
        best_value = float('-inf')

        # Chọn ra trạng thái lân cận tốt nhất là Best_Neighbor
        for action in possible_actions:
            child = child_node(current_node, action)
            child_value = value_func(child["state"])
            
            if child_value > best_value:
                best_value = child_value
                best_neighbor = child

        # NẾU Value(Best_Neighbor) > Value(Current_State)
        if best_value > value_func(current_node["state"]):
            current_node = best_neighbor  # Quay lại đầu vòng lặp với trạng thái mới
        else:
            # NGƯỢC LẠI: TRẢ VỀ Current_State (Dừng vì đã đạt cực đại cục bộ)
            return solution(current_node)