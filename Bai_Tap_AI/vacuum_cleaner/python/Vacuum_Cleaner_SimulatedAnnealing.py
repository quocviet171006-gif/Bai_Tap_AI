import math
import random
from utils import goal_test, actions, child_node, solution, heuristic

GUI_LOGGER = None

def simulated_annealing(initial_state):
    current_node = {
        "state": initial_state,
        "parent": None,
        "action": None,
        "cost": 0
    }
    
    T = 100.0
    Tmin = 0.01
    alpha = 0.95
    
    while T > Tmin:
        if goal_test(current_node["state"]):
            return solution(current_node)
            
        possible_actions = actions(current_node["state"])
        if not possible_actions:
            return solution(current_node)
            
        action = random.choice(possible_actions)
        next_node = child_node(current_node, action)
        
        current_h = heuristic(current_node["state"])
        next_h = heuristic(next_node["state"])
        delta = next_h - current_h
        
        if delta < 0:
            current_node = next_node
        else:
            p = math.exp(-delta / T)
            if random.random() < p:
                current_node = next_node
                
        if GUI_LOGGER:
            GUI_LOGGER(current_node, None, None)
            
        T = alpha * T
        
    return solution(current_node)
