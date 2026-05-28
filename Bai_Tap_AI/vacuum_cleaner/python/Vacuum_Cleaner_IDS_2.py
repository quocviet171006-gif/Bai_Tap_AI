import sys
from utils import goal_test, actions, child_node, solution, in_frontier, heuristic

def iterative_deepening_search(state):

    for depth in range(sys.maxsize):
        result = depth_limit_search(state, depth)
        if result != 'cutoff':
            return result

def depth_limit_search(initial_state, limit):
    node = {
        "state": initial_state,
        "parent": None,
        "action": None,
        "cost": 0
    }

    frontier = [node]
    result = 'failure'

    while frontier:
        node = frontier.pop()

        if node["cost"] >= limit:
            result = 'cutoff'
        else:
            for action in reversed(actions(node["state"])):
                child = child_node(node, action)
                
                if node["parent"] is not None and child["state"] == node["parent"]["state"]:
                    continue

                if goal_test(child["state"]):
                    return solution(child)
                    
                frontier.append(child)

    return result