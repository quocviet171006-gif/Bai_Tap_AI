import random
from utils import goal_test, actions, child_node, solution, heuristic

def value_func(state):
    return -heuristic(state)

def stochastic_hill_climbing(initial_state):
    current_node = {
        "state": initial_state,
        "parent": None,
        "action": None,
        "cost": 0
    }

    while True:
        if goal_test(current_node["state"]):
            return solution(current_node)

        # Sinh tất cả các trạng thái lân cận của Current_State
        possible_actions = actions(current_node["state"])
        current_value = value_func(current_node["state"])
        
        # Lọc ra tập Better_Neighbors = {Neighbor | Value(Neighbor) > Value(Current_State)}
        better_neighbors = []
        for action in possible_actions:
            child = child_node(current_node, action)
            if value_func(child["state"]) > current_value:
                better_neighbors.append(child)

        # NẾU Better_Neighbors RỖNG: Dừng vì đã đạt cực đại cục bộ
        if not better_neighbors:
            return solution(current_node)
        
        # NGƯỢC LẠI: Chọn ngẫu nhiên một trạng thái từ tập Better_Neighbors
        current_node = random.choice(better_neighbors)