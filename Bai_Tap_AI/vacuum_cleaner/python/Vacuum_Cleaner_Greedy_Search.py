from utils import goal_test, actions, child_node, solution, in_frontier, heuristic

def greedy_search(initial_state):

    node = {"state": initial_state,
            "parent": None,
            "action": None,
            "cost": heuristic(initial_state)
    }

    frontier = [node]
    reached = []

    while frontier:
        frontier.sort(key=lambda x: x["cost"])
        node = frontier.pop(0)

        if goal_test(node["state"]):
            return solution(node)
        
        reached.append(node["state"])

        for action in actions(node["state"]):
            child = child_node(node, action)
            child["cost"] = heuristic(child["state"])

            if child["state"] not in reached and not in_frontier(frontier, child["state"]):
                frontier.append(child)
                
    return "Failure"