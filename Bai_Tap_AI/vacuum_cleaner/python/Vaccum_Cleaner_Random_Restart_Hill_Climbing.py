from utils import find_robot, child_node, actions, goal_test, solution

GUI_LOGGER = None

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

def hill_climbing(initial_node):
    current = initial_node
    
    while True:
        if goal_test(current["state"]):
            return current
            
        if GUI_LOGGER:
            GUI_LOGGER(current, [], [])
            
        neighbors = []
        for action in actions(current["state"]):
            child = child_node(current, action)
            child["cost"] = get_heuristic(child["state"])
            neighbors.append(child)
        
        if not neighbors:
            return current
            
        # Chọn hàng xóm tốt nhất (giá trị heuristic thấp nhất)
        neighbors.sort(key=lambda x: x["cost"])
        
        # Nếu chi phí của trạng thái sinh ra không tốt hơn trạng thái đang xét thì dừng
        if neighbors[0]["cost"] >= current["cost"]:
            return current  
            
        current = neighbors[0]

def random_restart_hill_climbing(initial_state, max_restarts=10):
    for i in range(max_restarts):
        initial_node = {
            "state": initial_state,
            "parent": None,
            "action": None,
            "cost": get_heuristic(initial_state)
        }
        
        result_node = hill_climbing(initial_node)
        
        if goal_test(result_node["state"]):
            return solution(result_node)
            
    return "Failure"