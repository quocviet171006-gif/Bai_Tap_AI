import heapq
from utils import goal_test, actions, child_node, solution

def uniform_cost_search(initial_state):

    count = 0 
    node = {
        "state": initial_state, 
        "parent": None,
        "action": None,
        "cost": 0,
        "id": count
    }
    
    frontier = []
    heapq.heappush(frontier, (node["cost"], node["id"], node))
    
    reached = {str(initial_state): 0}
    
    while frontier:
        cost, node_id, node = heapq.heappop(frontier)
        
        if goal_test(node["state"]):
            return solution(node)
            
        for action in actions(node["state"]):
            child = child_node(node, action)
            s_str = str(child["state"])
            
            if s_str not in reached or child["cost"] < reached[s_str]:
                reached[s_str] = child["cost"]
                count += 1
                child["id"] = count
                heapq.heappush(frontier, (child["cost"], child["id"], child))
                
    return None