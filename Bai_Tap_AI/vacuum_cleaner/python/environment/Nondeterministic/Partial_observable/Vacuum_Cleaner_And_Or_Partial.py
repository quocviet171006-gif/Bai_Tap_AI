import sys
from utils_partial import *


# Mô hình cảm biến trả về vị trí robot và trạng thái ô hiện tại
def percept_model(state):
    res = find_robot(state)

    if res is None:
        return None

    r, c = res
    return (r, c, state[r][c])


# Cập nhật belief state dựa trên thông tin cảm biến
def update_belief_state(predict_belief, percept):
    if percept is None:
        return predict_belief
    
    updated_belief = set()

    # Chỉ giữ lại các trạng thái phù hợp với cảm biến nhận được
    for state_tuple in predict_belief:
        if percept_model(state_tuple) == percept:
            updated_belief.add(state_tuple)

    return updated_belief


# Khởi tạo quá trình AND-OR Graph Search
def and_or_graph_search(initial_layout):
    initial_belief = generate_initial_belief_state(initial_layout)
    path = set()

    return or_search(initial_belief, path)


# Nút OR: lựa chọn hành động phù hợp
def or_search(belief_state, path):

    # Đạt mục tiêu nếu mọi trạng thái trong belief state đều sạch
    if belief_goal_test(belief_state):
        return []
    
    frozen_belief = tuple(sorted(belief_state))

    # Tránh lặp vô hạn
    if frozen_belief in path:
        return None
    
    path.add(frozen_belief)

    actions = ["Up", "Down", "Left", "Right", "Suck"]
    
    for action in actions:
        plan = and_search(belief_state, action, path)

        if plan is not None:
            path.remove(frozen_belief)
            return [action, plan]
            
    path.remove(frozen_belief)
    return None


# Nút AND: xử lý tất cả các khả năng cảm biến có thể xảy ra
def and_search(belief_state, action, path):
    predict_belief = transition_model(belief_state, action)
    
    possible_percepts = set()

    # Thu thập toàn bộ cảm nhận có thể nhận được
    for state_tuple in predict_belief:
        possible_percepts.add(percept_model(state_tuple))
        
    conditional_plan = {}

    # Tạo kế hoạch cho từng kết quả cảm biến
    for percept in possible_percepts:
        actual_belief = update_belief_state(predict_belief, percept)
        sub_plan = or_search(actual_belief, path)
        
        if sub_plan is None:
            return None
            
        conditional_plan[percept] = sub_plan

    return conditional_plan


# Hiển thị kế hoạch có điều kiện được tạo ra
def print_conditional_plan(plan):
    if plan == []:
        print("--> [DAT MUC TIEU]")
        return

    if plan is None:
        print("--> [THAT BAI]")
        return
        
    action, contingencies = plan
    print(f"Hanh dong: {action}")
    
    for percept, sub_plan in contingencies.items():
        r, c, status = percept
        status_str = "BAN" if status == 3 else "SACH"

        print(f"  NEU cam bien tai ({r}, {c}) thay o nay {status_str}:")
        print_conditional_plan(sub_plan)