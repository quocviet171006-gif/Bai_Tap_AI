from collections import deque
from utils_sensorless import *

def depth_first_search_sensorless(initial_layout):
    initial_belief = generate_initial_belief_state(initial_layout)

    node = {
        "belief_state": initial_belief,
        "parent": None,
        "action": None,
        "cost": 0
    }

    if belief_goal_test(node["belief_state"]):
        return solution(node)

    frontier = [node]
    reached = set()

    while frontier:
        node = frontier.pop()
        
        frozen_belief = tuple(sorted(node["belief_state"]))
        if frozen_belief in reached:
            continue
        reached.add(frozen_belief)

        for action in ["Up", "Down", "Left", "Right", "Suck"]:
            next_belief = transition_model(node["belief_state"], action)
            
            child = {
                "belief_state": next_belief,
                "parent": node,
                "action": action,
                "cost": node["cost"] + 1
            }

            frozen_child = tuple(sorted(child["belief_state"]))
            if frozen_child not in reached:
                if belief_goal_test(child["belief_state"]):
                    return solution(child)
                frontier.append(child)

    return "Failure"

if __name__ == "__main__":
    room_layout = [
        [0, 0],
        [-1, 0]
    ]

    result = depth_first_search_sensorless(room_layout)
    
    if result != "Failure":
        current_belief = generate_initial_belief_state(room_layout)
        
        print("=============================")
        print("TRẠNG THÁI NIỀM TIN BAN ĐẦU:")
        print_belief_state(current_belief)
        
        for action in result:
            current_belief = transition_model(current_belief, action)
            print(f"Hành động thực hiện: {action}")
            print_belief_state(current_belief)
            
        print("KẾT QUẢ: Chuỗi hành động hoàn chỉnh:", result)
    else:
        print("Không tìm thấy giải pháp!")