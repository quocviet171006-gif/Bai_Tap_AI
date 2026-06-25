from collections import deque
from utils_sensorless import *

# Thuật toán DFS cho môi trường Sensorless
def depth_first_search_sensorless(initial_layout):

    # Khởi tạo belief state ban đầu
    initial_belief = generate_initial_belief_state(initial_layout)

    # Tạo node gốc
    node = {
        "belief_state": initial_belief,
        "parent": None,
        "action": None,
        "cost": 0
    }

    # Kiểm tra trạng thái mục tiêu
    if belief_goal_test(node["belief_state"]):
        return solution(node)

    # Frontier hoạt động như ngăn xếp (stack)
    frontier = [node]

    # Lưu các belief state đã duyệt
    reached = set()

    while frontier:
        node = frontier.pop()
        
        frozen_belief = tuple(sorted(node["belief_state"]))

        # Bỏ qua nếu đã thăm trạng thái này
        if frozen_belief in reached:
            continue

        reached.add(frozen_belief)

        # Sinh các hành động có thể thực hiện
        for action in ["Up", "Down", "Left", "Right", "Suck"]:
            next_belief = transition_model(node["belief_state"], action)
            
            child = {
                "belief_state": next_belief,
                "parent": node,
                "action": action,
                "cost": node["cost"] + 1
            }

            frozen_child = tuple(sorted(child["belief_state"]))

            # Thêm trạng thái mới vào frontier
            if frozen_child not in reached:
                if belief_goal_test(child["belief_state"]):
                    return solution(child)

                frontier.append(child)

    return "Failure"


# Chạy thử chương trình
if __name__ == "__main__":
    room_layout = [
        [0, 0],
        [-1, 0]
    ]

    result = depth_first_search_sensorless(room_layout)
    
    if result != "Failure":

        # Khởi tạo belief state ban đầu để theo dõi quá trình
        current_belief = generate_initial_belief_state(room_layout)
        
        print("=============================")
        print("TRẠNG THÁI NIỀM TIN BAN ĐẦU:")
        print_belief_state(current_belief)
        
        # Thực hiện lần lượt các hành động trong lời giải
        for action in result:
            current_belief = transition_model(current_belief, action)

            print(f"Hành động thực hiện: {action}")
            print_belief_state(current_belief)
            
        print("KẾT QUẢ: Chuỗi hành động hoàn chỉnh:", result)
    else:
        print("Không tìm thấy giải pháp!")