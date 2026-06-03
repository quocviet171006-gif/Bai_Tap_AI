from utils import actions, child_node, goal_test, solution, find_robot

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

def local_beam_search(initial_state, k=3):
    initial_node = {
        "state": initial_state,
        "parent": None,
        "action": None,
        "cost": get_heuristic(initial_state)
    }
    beam = [initial_node]
    
    while True:
        candidates = []
        for node in beam:
            if goal_test(node["state"]):
                return solution(node)
                
            if GUI_LOGGER:
                GUI_LOGGER(node, beam, [])
            
            for action in actions(node["state"]):
                child = child_node(node, action)
                child["cost"] = get_heuristic(child["state"])
                candidates.append(child)
        
        if not candidates:
            return "Failure"
            
        candidates.sort(key=lambda x: x["cost"])
        beam = candidates[:k]
